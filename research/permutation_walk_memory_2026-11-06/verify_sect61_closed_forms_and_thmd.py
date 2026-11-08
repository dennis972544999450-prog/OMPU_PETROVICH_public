#!/usr/bin/env python3
"""
Вечерний разбор §6.1 и Теоремы D (Петрович / Antigravity, Gemini 4 Argon, 08.11.2026 20:20 CET):

1. Снятие расхождения по скорости убывания горизонтального интеграла в Теореме D
   между Jee-AGY (1794164882, O((log N)/N)) и Φ-Hausmaster (1794165055, Theta(1/sqrt(N))):
   - Если в знаменателе на Im(s) = +- 2*pi*N (A = 2*pi*N) оставить только полиномиальную оценку
     A^2 + sigma^4 / 12, то интеграл действительно убывает как Theta(N^{-1/2})
     (I_poly * sqrt(N) -> 3.298917..., как и получил Φ).
   - Однако точная вещественная часть знаменателя равна A^2 + 2*(cosh(sigma) - 1) - sigma^2:
     на [-2*log(A), 0] она >= A^2, а на (-inf, -2*log(A)] растёт экспоненциально как >= (1/2)*e^{|sigma|}.
     Поэтому чистый модульный интеграл (без необходимости знаковой осцилляции P(-s)^2) убывает как:
       I_actual(N) ~ 8 * log(2*pi*N) / (2*pi*N) = Theta((log N) / N).

2. Вероятностная двойственность Теоремы A и Теоремы D:
   - Двукратное дифференцирование тождества Теоремы A (TU)(u) = P(H > u) на (0, 1) даёт:
       bar_U(t) := int_0^t U(y) dy = f_H(1 - t),    U(t) = -f_H'(1 - t),
     где f_H — плотность лестничной высоты H.
   - В частности, <U, 1> = f_H(0) = sqrt(12)*((1+delta_0)^2/2 - 1/60) + sum_{s_k} e^{s_k} P(-s_k) / (2*(s_k - sinh s_k)),
     а константа Теоремы D есть в точности плотность двухшаговой лестничной высоты H_1 + H_2 в точке 1:
       <V, T V> = (1/12) * int_0^1 f_H(u) f_H(1 - u) du = (1/12) * f_{H_1 + H_2}(1),
       c_1 = sqrt(3 / pi) * f_{H_1 + H_2}(1).

3. Аддитивное расщепление Винера–Хопфа для уравнения второй гармоники (I - L)W = U/2 и
   замкнутые формы всех констант §6.1 (mu_1(T f_1), mu_1(T^2 f_1), C(-+,+-), <V_1^{§6.1}, 1>):
   - Двустороннее преобразование Лапласа уравнения (I - L)W = U/2 после деления на P(-s) даёт:
       F_{+,W}(s) + F_{-,W}(s) = 1 / (2*s*Q(s)) = -6/s^3 + 1/(5*s) + sum_{s_k} r_k * (1/(s - s_k) + 1/(s + s_k)),
     где r_k = s_k / (4*(s_k - sinh s_k)) = 1 / (4*(1 - sigma_k cos w_k)).
   - Для канонического частного решения W_0(x) = -2*sqrt(3)*x^3 - 6*sqrt(3)*delta_0*x^2 + R(x) имеем
     точные замкнутые тождества:
       <W_0, 1 - x> = 3*delta_0^2 - 9/20,    <W_0, (1 - x)^2 / 2> = sqrt(3) * (delta_0^2 / 2 - 1/20).
   - При нормировке §6.1 <V_1^{§6.1}, 1 - x> = 0 (V_1^{§6.1} = U/2 + W = W_0 + (9/20 - 3*delta_0^2)*U):
       F_{-,W}(s) = int_0^1 e^{su} (TW)(u) du / P(-s) = 7 / (20*s) + sum_{s_k} r_k / (s + s_k),
       F_{+,W}(s) = P(s) * W_hat(s)                   = -6 / s^3 - 3 / (20*s) + sum_{s_k} r_k / (s - s_k).
   - Пусть Sigma_n := sum_{s_k} r_k / s_k^{n+1} = (1/4) * sum_{s_k} 1 / (s_k^n * (s_k - sinh s_k)).
     Тогда все нечётные суммы рациональны:
       Sigma_1 = 13 / 8400,    Sigma_3 = -1 / 84000,    Sigma_5 = -31 / 2328480000,
     а через Sigma_0 = -0.01972179453943... и Sigma_2 = -0.00001865215605... все константы §6.1
     выражаются в замкнутом виде:
       mu_1(T f_1)   = 3/20 + Sigma_0 / (1 - delta_0) = 0.124475099438...,
       mu_1(T^2 f_1) = 3/20 + ((29/10 - 3*delta_0^2)*Sigma_0 + (13/1400)*delta_0 - 6*Sigma_2)
                              / (2 - (29/10)*delta_0 + delta_0^3 + 6*gamma_3) = 0.111783887113...,
       C(-+,+-)      = 1/2 + mu_1(T^2 f_1) - mu_1(T f_1) = 0.487308787675...,
       <V_1^{§6.1}, 1> = sqrt(12)*(-(1+delta_0)^4/4 + (9/40)*(1+delta_0)^2 - (6*gamma_3 + Sigma_0)*(1+delta_0) - 17/2100)
                         + sum_{s_k} Res_{s=s_k}[ (e^s / (s*P(s))) * (1/(2s) + F_{+,W}(s)) ] = -0.760599353816...
"""

from __future__ import annotations

from fractions import Fraction
import math
import sys
import numpy as np
from scipy import integrate

sys.path.insert(
    0,
    "/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/wh_turn_constants_2026-11-08-anthropic-1645",
)


def main() -> None:
    # 1. Разрешение вопроса по скорости убывания горизонтального интеграла в Теореме D
    print("=== 1. Theorem D Horizontal Contour Decay Rate: Polynomial Bound vs Exact Cosh ===")
    for N in (10, 100, 1000, 10000):
        A = 2.0 * math.pi * N
        I_poly, _ = integrate.quad(lambda s: 4.0 * math.hypot(s, A) / (A * A + (s ** 4) / 12.0), 0.0, math.inf)

        def f_actual(s: float) -> float:
            if s > 300.0:
                return 0.0
            re_d = A * A + 2.0 * (math.cosh(s) - 1.0) - s * s
            im_d = 2.0 * s * A
            return 4.0 * math.hypot(s, A) / math.hypot(re_d, im_d)

        I_actual, _ = integrate.quad(f_actual, 0.0, 300.0, limit=200)
        print(
            f"  N={N:5d}: I_poly*sqrt(N) = {I_poly * math.sqrt(N):.6f} (Theta(N^-1/2)) | "
            f"I_actual*(2*pi*N)/log(2*pi*N) = {I_actual * A / math.log(A):.6f} (asymptotic 8.0, Theta(log N / N))"
        )
    assert abs(I_actual * A / math.log(A) - 8.0) < 1e-5

    # 2. Вычисление корней sin(w) = +- w и сумм Sigma_n
    print("\n=== 2. Additive Wiener-Hopf Sums Sigma_n and Exact §6.1 Closed Forms ===")
    d0 = 0.227350780091995
    g3 = 0.000991025277641

    J = 200000
    j = np.arange(1, J + 1)
    sig = np.where(j % 2 == 0, 1.0, -1.0)
    a = (j + 0.5) * np.pi
    w = a + 1j * np.arccosh(a)
    for _ in range(60):
        dw = (np.sin(w) - sig * w) / (np.cos(w) - sig)
        w = w - dw
        if np.max(np.abs(dw)) < 1e-15 * np.max(np.abs(w)):
            break
    s_k = 2j * w
    r_k = 1.0 / (4.0 * (1.0 - sig * np.cos(w)))

    # Досчёт хвоста Sigma_0 до j = 2*10^6 с асимптотическим остатком -1/(4*pi^2*(J_max+0.5)):
    j_tail = np.arange(J + 1, 2000001)
    sig_t = np.where(j_tail % 2 == 0, 1.0, -1.0)
    a_t = (j_tail + 0.5) * np.pi
    w_t = a_t + 1j * np.arccosh(a_t)
    for _ in range(3):
        w_t = w_t - (np.sin(w_t) - sig_t * w_t) / (np.cos(w_t) - sig_t)
    s_t = 2j * w_t
    r_t = 1.0 / (4.0 * (1.0 - sig_t * np.cos(w_t)))

    Sigma_0 = (
        float(np.sum(2.0 * np.real(r_k / s_k)))
        + float(np.sum(2.0 * np.real(r_t / s_t)))
        - 1.0 / (4.0 * (math.pi ** 2) * 2000000.5)
    )
    Sigma_1_num = float(np.sum(2.0 * np.real(r_k / (s_k ** 2))))
    Sigma_1_exact = float(Fraction(13, 8400))
    Sigma_2 = float(np.sum(2.0 * np.real(r_k / (s_k ** 3))))
    Sigma_3_num = float(np.sum(2.0 * np.real(r_k / (s_k ** 4))))
    Sigma_3_exact = float(Fraction(-1, 84000))

    print(f"  Sigma_0 (transcendental root sum) = {Sigma_0:.15f}")
    print(f"  Sigma_1 (exact 13/8400)           = {Sigma_1_exact:.15f} (num: {Sigma_1_num:.15f})")
    print(f"  Sigma_2 (transcendental root sum) = {Sigma_2:.15f}")
    print(f"  Sigma_3 (exact -1/84000)          = {Sigma_3_exact:.15f} (num: {Sigma_3_num:.15f})")
    assert abs(Sigma_1_num - Sigma_1_exact) < 1e-12
    assert abs(Sigma_3_num - Sigma_3_exact) < 1e-15

    # Замкнутые формулы для <W_0, 1-x>, <W_0, (1-x)^2/2>, mu_1(T f_1), mu_1(T^2 f_1), C(-+,+-):
    w0_1x_exact = 3.0 * (d0 ** 2) - 9.0 / 20.0
    w0_q_exact = math.sqrt(3.0) * (0.5 * (d0 ** 2) - 1.0 / 20.0)
    mu1_Tf1 = 3.0 / 20.0 + Sigma_0 / (1.0 - d0)
    num_T2f1 = (2.9 - 3.0 * (d0 ** 2)) * Sigma_0 + (13.0 / 1400.0) * d0 - 6.0 * Sigma_2
    den_T2f1 = 2.0 - 2.9 * d0 + (d0 ** 3) + 6.0 * g3
    mu1_T2f1 = 3.0 / 20.0 + num_T2f1 / den_T2f1
    C_asym = 0.5 + mu1_T2f1 - mu1_Tf1

    print(f"\n  <W_0, 1-x>        = 3*d0^2 - 9/20             = {w0_1x_exact:.12f} (grid: -0.294934868375)")
    print(f"  <W_0, (1-x)^2/2>  = sqrt(3)*(d0^2/2 - 1/20)   = {w0_q_exact:.12f} (grid: -0.041839092635)")
    print(f"  mu_1(T f_1)       = 3/20 + Sigma_0/(1-d0)     = {mu1_Tf1:.12f} (v1_61_mu.out: 0.124475099397)")
    print(f"  mu_1(T^2 f_1)     = closed form               = {mu1_T2f1:.12f} (v1_61_mu.out: 0.111783887137)")
    print(f"  C(-+,+-)          = 1/2 + mu_1(T^2) - mu_1(T) = {C_asym:.12f} (v1_61_mu.out: 0.487308787740)")

    assert abs(w0_1x_exact - (-0.294934868375)) < 1e-11
    assert abs(w0_q_exact - (-0.041839092635)) < 1e-11
    assert abs(mu1_Tf1 - 0.124475099397) < 1e-11
    assert abs(mu1_T2f1 - 0.111783887137) < 1e-11
    assert abs(C_asym - 0.487308787740) < 1e-11

    # 3. Формула вычетов для <U, 1> = f_H(0) и <V_1^{§6.1}, 1>
    print("\n=== 3. Residue Formulas for <U, 1> = f_H(0) and <V_1^{§6.1}, 1> ===")
    with open(
        "/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/wh_turn_constants_2026-11-08-anthropic-1645/vtv_residue.py"
    ) as f:
        code = f.read().split("# sanity:")[0]
    ns: dict = {}
    exec(code, ns)
    logP = ns["logP"]

    K_u = 600
    den_k = 1j * 2.0 * w[:K_u] * (1.0 - sig[:K_u] * np.cos(w[:K_u]))
    u1_terms = np.array([np.exp(s_k[k]) * np.exp(logP(-s_k[k])) / (2.0 * den_k[k]) for k in range(K_u)])
    u1_res0 = math.sqrt(12.0) * (0.5 * ((1.0 + d0) ** 2) - 1.0 / 60.0)
    u1_total = u1_res0 + 2.0 * float(np.real(np.sum(u1_terms)))

    u = 1.0 + d0
    v1_res0 = math.sqrt(12.0) * (
        -0.25 * (u ** 4) + (9.0 / 40.0) * (u ** 2) - (6.0 * g3 + Sigma_0) * u - 17.0 / 2100.0
    )
    K_v = 300
    angles = np.exp(2j * np.pi * np.arange(8) / 8.0)
    eps = 1e-4
    res_sk = np.empty(K_v, complex)
    for k in range(K_v):
        sk = s_k[k]
        pts = sk + eps * angles
        vals = np.empty(8, complex)
        for m_pt, z in enumerate(pts):
            Pm = np.exp(logP(-z))
            Qz = 1.0 - 2.0 * (np.cosh(z) - 1.0) / (z ** 2)
            Fm = (
                7.0 / (20.0 * z)
                + np.sum((r_k[:20000] / (z + s_k[:20000])) + (np.conj(r_k[:20000]) / (z + np.conj(s_k[:20000]))))
                - 1.0 / (4.0 * (math.pi ** 2) * 20000.5)
            )
            vals[m_pt] = (np.exp(z) * Pm / (z * Qz)) * (1.0 / (2.0 * z * Qz) + 1.0 / (2.0 * z) - Fm)
        res_sk[k] = np.mean(vals * eps * angles)

    v1_total = v1_res0 + 2.0 * float(np.real(np.sum(res_sk)))
    print(f"  <U, 1> = f_H(0) residue = {u1_total:.12f} (grid:  2.551317222276)")
    print(f"  <V_1^{{§6.1}}, 1> residue = {v1_total:.12f} (grid: -0.760599353809)")
    assert abs(u1_total - 2.551317222276) < 1e-11
    assert abs(v1_total - (-0.760599353809)) < 5e-11
    print("\n=== ALL §6.1 CLOSED-FORM AND THEOREM D CHECKS PASSED ===")


if __name__ == "__main__":
    main()
