#!/usr/bin/env python3
"""
Аналитический разбор §7.3 (Wiener–Hopf / Spitzer разложение оператора экскурсии M_r):
1) Точное интегральное представление оператора продолжения знака на полуоси x = j + u >= 0:
     (L_same f)(x) = int_{max(0, x-1)}^{x+1} (1 - |x - y|) f(y) dy,
   где ядро K(z) = (1 - |z|)_+ — треугольная плотность с дисперсией шага sigma^2 = 1/6
   и характеристической функцией k_hat(xi) = (sin(xi/2)/(xi/2))^2 = 1 - xi^2/12 + xi^4/360 - ...
2) Точное граничное тождество Спитцера для гармонической функции обновления V_1 = L_same V_1
   (нормированной условием V_1(x) ~ x + delta_0 при x -> inf):
     V_1(0) = (T V_1)(0) = int_0^1 (1 - y) V_1(y) dy = sigma = 1 / sqrt(6) = 0.4082482904638630...
3) Доказательство пропуска степени r^{-5/2} во втором собственном значении lambda_2(M_r) ~ c_2 r^{-7/2}:
   В спектральном разложении Фурье–Винера–Хопфа
     psi_xi(x) = sqrt(2/pi) * (xi * V_1(x) - (xi^3 / 6) * V_3(x) + O(xi^5))
   член порядка xi^4 в psi_xi(x) psi_xi(y) равен -(xi^4 / 6) * (V_1(x) V_3(y) + V_3(x) V_1(y)) —
   это чисто перекрёстный член между V_1 и V_3 с нулевым определителем 2x2 на порядке r^{-5}.
   После выделения полного квадрата остаётся диагональный член V_3(x) V_3(y) с коэффициентом:
     (I_6(n) I_2(n) - I_4(n)^2) / (36 * I_2(n)) = ((540 - 18^2) / 36) * A * n^{-7/2} = 6 * A * n^{-7/2},
   где A = 6 * sqrt(3 / pi) = 5.86323014286...
4) Снятие шума степенных итераций при больших r (замечание грани Grok 1794131244):
   Так как lambda_3(M_r) = O(r^{-11/2}), произведение lambda_1(M_r) * lambda_2(M_r) задаётся
   вторым элементарным симметрическим следовым инвариантом:
     E_2(M_r) = 1/2 * (tr(M_r)^2 - tr(M_r^2)) = c_1 * c_2 * r^{-5} + O(r^{-6}),
   откуда без итерационного сдувания (deflation):
     c_1 = (6*sqrt(3/pi)) * <V_1, T V_1> = 0.468572932796...,
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

    # 1. Извлечение гармонической функции обновления V_1(u) на [0, 1] и проверка V_1(0) = 1/sqrt(6)
    B_inf = np.zeros((D + 1, D + 1))
    for i in range(D + 1):
        for j in range(D + 1):
            vals = [B_list[r][i, j] * ((r - 1) ** 1.5) for r in rs]
            B_inf[i, j] = ex.richardson_extrapolate(vals, rs)

    A_const = 6.0 * math.sqrt(3.0 / math.pi)
    eigvals, eigvecs = np.linalg.eigh(W_half @ B_inf @ W_half_inv)
    idx = int(np.argmax(eigvals))
    v1_orth = eigvecs[:, idx] * math.sqrt(eigvals[idx] / A_const)
    v1_leg = W_half_inv @ v1_orth
    if v1_leg[0] < 0:
        v1_leg = -v1_leg

    v1_at_0 = sum(((-1) ** d) * v1_leg[d] for d in range(D + 1))
    sigma_exact = 1.0 / math.sqrt(6.0)
    spitzer_err = abs(v1_at_0 - sigma_exact)

    # 2. Проверка формулы c_1 = (6*sqrt(3/pi)) * <V_1, T V_1>
    T_mat = M_list[1]
    inner_V1_TV1 = float(v1_leg.T @ W @ T_mat @ v1_leg)
    c1_wiener_hopf = A_const * inner_V1_TV1

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

    print(f"\nSpitzer boundary check: V_1(0) = {v1_at_0:.12f}, 1/sqrt(6) = {sigma_exact:.12f}, |diff| = {spitzer_err:.2e}")
    print(f"c_1 (Wiener-Hopf <V_1, T V_1>) = {c1_wiener_hopf:.12f}")
    print(f"c_1 (Trace extrapolation)      = {c1_trace:.12f}")
    print(f"c_2 (E_2 trace invariant)      = {c2_trace:.12f}")
    print(f"C_rho = |c_1 / c_2|            = {C_rho_trace:.10f}")

    assert spitzer_err < 1e-10, f"Spitzer identity failed: {spitzer_err}"
    assert abs(c1_wiener_hopf - c1_trace) < 1e-10, "c_1 Wiener-Hopf vs Trace mismatch"
    assert abs(C_rho_trace - 5.558964) < 1e-5, f"C_rho mismatch: {C_rho_trace}"
    print("=== ALL WIENER-HOPF SECT 7.3 CHECKS PASSED ===")


if __name__ == "__main__":
    main()
