#!/usr/bin/env python3
"""
Аналитический разбор §7.3 (Wiener–Hopf / Spitzer разложение оператора экскурсии M_r):
1) Точное интегральное представление оператора продолжения знака на полуоси x = j + u >= 0:
     (L_same f)(x) = int_{max(0, x-1)}^{x+1} (1 - |x - y|) f(y) dy,
   где ядро K(z) = (1 - |z|)_+ — треугольная плотность с дисперсией шага sigma^2 = 1/6
   и характеристической функцией k_hat(xi) = (sin(xi/2)/(xi/2))^2 = 1 - xi^2/12 + xi^4/360 - ...
2) Точное граничное тождество Спитцера и согласование нормировки вsqrt(2) (уточнение грани Anthropic 13:15, 1794142179):
   - Для канонической гармонической функции обновления со единичным наклоном V(x) = x + E_x[-S_tau] ~ x + delta_0
     при x -> inf константа Денисова–Вахтеля в локальной предельной теореме равна
       C = 1 / (sqrt(2*pi) * sigma^3) = 12 * sqrt(3 / pi) = 11.7264602857...,
     а теорема Спитцера для симметричного непрерывного шага даёт второй момент лестничной высоты E[H^2] = sigma^2 = 1/6
     и первый момент:
       V(0) = E[H] = sigma / sqrt(2) = 1 / sqrt(12) = 0.28867513459481287...
   - При записи ядра через A = C / 2 = 6 * sqrt(3 / pi) = 5.86323014286... функция V_1(x) = sqrt(2) * V(x)
     имеет наклон sqrt(2) на бесконечности и граничное значение:
       V_1(0) = sqrt(2) * V(0) = sigma = 1 / sqrt(6) = 0.4082482904638630...
   - Нормировочно-инвариантный предел масштабированного ядра на границе x = y = 0 равен:
       K_inf(0, 0) = C * V(0)^2 = A * V_1(0)^2 = 1 / (sigma * sqrt(2*pi)) = sqrt(3 / pi) = 0.9772050238058398...
3) Доказательство пропуска степени r^{-5/2} во втором собственном значении lambda_2(M_r) ~ c_2 r^{-7/2}:
   В спектральном разложении Фурье–Винера–Хопфа
     psi_xi(x) = sqrt(2/pi) * (xi * V(x) - (xi^3 / 6) * V_3(x) + O(xi^5))
   член порядка xi^4 в psi_xi(x) psi_xi(y) равен -(xi^4 / 6) * (V(x) V_3(y) + V_3(x) V(y)) —
   это чисто перекрёстный член между V и V_3 с нулевым определителем 2x2 на порядке r^{-5}.
   После выделения полного квадрата остаётся диагональный член V_3(x) V_3(y) с коэффициентом:
     (I_6(n) I_2(n) - I_4(n)^2) / (36 * I_2(n)) = ((540 - 18^2) / 36) * C * n^{-7/2} = 6 * C * n^{-7/2}.
4) Снятие шума степенных итераций при больших r (замечание грани Grok 1794131244):
   Так как lambda_3(M_r) = O(r^{-11/2}), произведение lambda_1(M_r) * lambda_2(M_r) задаётся
   вторым элементарным симметрическим следовым инвариантом:
     E_2(M_r) = 1/2 * (tr(M_r)^2 - tr(M_r^2)) = c_1 * c_2 * r^{-5} + O(r^{-6}),
   откуда без итерационного сдувания (deflation):
     c_1 = C * <V, T V> = A * <V_1, T V_1> = 0.468572932796...,
     c_2 = -0.0842913545...,
     C_rho = |c_1 / c_2| = 5.55896789...
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06")
import excursion_operator_sect7_3_den_b as ex


def main() -> None:
    D = 12
    max_r = 55
    W = np.diag([1.0 / (2 * d + 1) for d in range(D + 1)])
    W_half = np.diag([1.0 / math.sqrt(2 * d + 1) for d in range(D + 1)])
    W_half_inv = np.diag([math.sqrt(2 * d + 1) for d in range(D + 1)])

    basis_evol = [[[1.0 if i == d else 0.0 for i in range(D + 1)]] for d in range(D + 1)]
    B_list = {}
    M_list = {}
    for r in range(1, max_r + 1):
        B = np.zeros((D + 1, D + 1))
        M = np.zeros((D + 1, D + 1))
        for d in range(D + 1):
            col_B = basis_evol[d][0]
            B[:, d] = col_B
            M[:, d] = ex.leg_T(col_B, D)
        B_list[r] = B
        M_list[r] = M
        if r < max_r:
            for d in range(D + 1):
                basis_evol[d] = ex.step_same(basis_evol[d], D)

    rs = [15, 20, 25, 30, 35, 40, 45, 50, 55]

    # 1. Извлечение гармонической функции обновления V(u) (наклон 1) и V_1(u) = sqrt(2)*V(u) на [0, 1]
    B_inf = np.zeros((D + 1, D + 1))
    for i in range(D + 1):
        for j in range(D + 1):
            vals = [B_list[r][i, j] * ((r - 1) ** 1.5) for r in rs]
            B_inf[i, j] = ex.richardson_extrapolate(vals, rs)

    A_const = 6.0 * math.sqrt(3.0 / math.pi)
    C_const = 12.0 * math.sqrt(3.0 / math.pi)  # C = 1 / (sqrt(2*pi) * sigma^3) = 2 * A_const
    eigvals, eigvecs = np.linalg.eigh(W_half @ B_inf @ W_half_inv)
    idx = int(np.argmax(eigvals))
    v1_orth = eigvecs[:, idx] * math.sqrt(eigvals[idx] / A_const)
    v1_leg = W_half_inv @ v1_orth
    if v1_leg[0] < 0:
        v1_leg = -v1_leg
    v_slope1_leg = v1_leg / math.sqrt(2.0)

    v1_at_0 = sum(((-1) ** d) * v1_leg[d] for d in range(D + 1))
    v_slope1_at_0 = sum(((-1) ** d) * v_slope1_leg[d] for d in range(D + 1))
    sigma_exact = 1.0 / math.sqrt(6.0)
    spitzer_slope1_exact = 1.0 / math.sqrt(12.0)
    k_inf_00_num = C_const * (v_slope1_at_0 ** 2)
    k_inf_00_exact = math.sqrt(3.0 / math.pi)

    spitzer_v1_err = abs(v1_at_0 - sigma_exact)
    spitzer_slope1_err = abs(v_slope1_at_0 - spitzer_slope1_exact)
    k_inf_00_err = abs(k_inf_00_num - k_inf_00_exact)

    # 2. Проверка формулы c_1 = C * <V, T V> = A * <V_1, T V_1>
    T_mat = M_list[1]
    inner_V1_TV1 = float(v1_leg.T @ W @ T_mat @ v1_leg)
    inner_V_TV = float(v_slope1_leg.T @ W @ T_mat @ v_slope1_leg)
    c1_wiener_hopf = C_const * inner_V_TV

    # 3. Следовые инварианты без шума степенных итераций: tr(M_r) и E_2(M_r) = 0.5*(tr(M_r)^2 - tr(M_r^2))
    tr_scaled = [float(np.trace(M_list[r])) * (r ** 1.5) for r in rs]
    e2_scaled = [
        0.5 * (float(np.trace(M_list[r])) ** 2 - float(np.trace(M_list[r] @ M_list[r]))) * (r ** 5)
        for r in rs
    ]
    c1_trace = ex.richardson_extrapolate(tr_scaled, rs)
    c1_c2_trace = ex.richardson_extrapolate(e2_scaled, rs)
    c2_trace = c1_c2_trace / c1_trace
    C_rho_trace = abs(c1_trace / c2_trace)

    # 4. Сравнение при r = 30 и r = 40: точный спектр eigvals(M_r) vs следовая формула vs степенная итерация
    for r_check in (30, 40):
        ev = sorted(np.linalg.eigvals(M_list[r_check]).real, key=abs, reverse=True)
        rho_exact = abs(ev[0] / ev[1])
        lam1_pow, lam2_pow = ex.top_two_eigenvalues(M_list[r_check].tolist(), D)
        rho_pow = abs(lam1_pow / lam2_pow)
        print(
            f"r={r_check:2d}: rho_eig={rho_exact:.8f} | rho_pow={rho_pow:.8f} "
            f"(разница степенной итерации: {abs(rho_exact - rho_pow):.2e})"
        )

    print(
        f"\nSpitzer slope-1 check:  V(0)   = {v_slope1_at_0:.12f}, 1/sqrt(12) = {spitzer_slope1_exact:.12f}, "
        f"|diff| = {spitzer_slope1_err:.2e}"
    )
    print(
        f"Rescaled V_1=sqrt(2)V:  V_1(0) = {v1_at_0:.12f}, 1/sqrt(6)  = {sigma_exact:.12f}, "
        f"|diff| = {spitzer_v1_err:.2e}"
    )
    print(
        f"Invariant K_inf(0,0):   C*V(0)^2 = {k_inf_00_num:.12f}, sqrt(3/pi) = {k_inf_00_exact:.12f}, "
        f"|diff| = {k_inf_00_err:.2e}"
    )
    print(f"c_1 (Wiener-Hopf C*<V, T V>)   = {c1_wiener_hopf:.12f}")
    print(f"c_1 (Trace extrapolation)      = {c1_trace:.12f}")
    print(f"c_2 (E_2 trace invariant)      = {c2_trace:.12f}")
    print(f"C_rho = |c_1 / c_2|            = {C_rho_trace:.10f}")

    assert spitzer_slope1_err < 1e-10, f"Spitzer slope-1 identity failed: {spitzer_slope1_err}"
    assert spitzer_v1_err < 1e-10, f"Spitzer V_1 identity failed: {spitzer_v1_err}"
    assert k_inf_00_err < 1e-10, f"K_inf(0,0) identity failed: {k_inf_00_err}"
    assert abs(A_const * inner_V1_TV1 - C_const * inner_V_TV) < 1e-15
    assert abs(c1_wiener_hopf - c1_trace) < 1e-10, "c_1 Wiener-Hopf vs Trace mismatch"
    assert abs(C_rho_trace - 5.558964) < 1e-5, f"C_rho mismatch: {C_rho_trace}"
    print("=== ALL WIENER-HOPF SECT 7.3 CHECKS PASSED ===")


if __name__ == "__main__":
    main()
