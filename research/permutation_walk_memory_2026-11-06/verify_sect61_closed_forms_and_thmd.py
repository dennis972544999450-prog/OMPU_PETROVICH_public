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

    # 3. Точная аналитическая формула вычетов для <U, 1> = f_H(0) и <V_1^{§6.1}, 1> (все 12 знаков, без кругов Коши)
    print("\n=== 3. Exact Analytic Residue Formulas for <U, 1> = f_H(0) and <V_1^{§6.1}, 1> (12 digits) ===")
    with open(
        "/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/wh_turn_constants_2026-11-08-anthropic-1645/vtv_residue.py"
    ) as f:
        code = f.read().split("# sanity:")[0]
    ns: dict = {}
    exec(code, ns)
    logP = ns["logP"]
    T_quad = ns["T"]
    G_quad = ns["G"]
    TMAX_quad = ns["TMAX"]

    def logP_deriv(s: complex) -> complex:
        I_d = np.sum(G_quad * (T_quad * T_quad - s * s) / ((s * s + T_quad * T_quad) ** 2)) - 1.0 / (6.0 * (TMAX_quad ** 3))
        return 1.0 / (s * (s + 1.0)) + (2.0 / math.pi) * I_d

    M_inner = 30000
    rm_sm = r_k[:M_inner] / s_k[:M_inner]
    crm_csm = np.conj(rm_sm)
    sk_M = s_k[:M_inner]
    csk_M = np.conj(sk_M)

    def Fm_fast(z: complex) -> complex:
        return 7.0 / (20.0 * z) + Sigma_0 - z * np.sum(rm_sm / (z + sk_M) + crm_csm / (z + csk_M))

    def Fm_deriv(z: complex) -> complex:
        return -7.0 / (20.0 * (z ** 2)) - np.sum(
            rm_sm * sk_M / ((z + sk_M) ** 2) + crm_csm * csk_M / ((z + csk_M) ** 2)
        )

    K_u = 600
    den_k = 1j * 2.0 * w[:K_u] * (1.0 - sig[:K_u] * np.cos(w[:K_u]))
    u1_terms = np.array([np.exp(s_k[k]) * np.exp(logP(-s_k[k])) / (2.0 * den_k[k]) for k in range(K_u)])
    u1_res0 = math.sqrt(12.0) * (0.5 * ((1.0 + d0) ** 2) - 1.0 / 60.0)
    u1_total = u1_res0 + 2.0 * float(np.real(np.sum(u1_terms)))

    # Для <V_1^{§6.1}, 1> при Q(s_k) = 0 имеем точное тождество Q''(s_k) / Q'(s_k) = -1 / Q'(s_k) - 4 / s_k
    # и убывание членов вычетов O(k^{-4}) (остаток O(K^{-3})):
    u = 1.0 + d0
    v1_res0 = math.sqrt(12.0) * (
        -0.25 * (u ** 4) + (9.0 / 40.0) * (u ** 2) - (6.0 * g3 + Sigma_0) * u - 17.0 / 2100.0
    )
    K_v = 800
    res_v1 = np.empty(K_v, float)
    res_utw = np.empty(K_v, float)
    res_wtw = np.empty(K_v, float)

    for k in range(K_v):
        sk = s_k[k]
        Pms = np.exp(logP(-sk))
        dlogP_ms = -logP_deriv(-sk)
        fms = Fm_fast(sk)
        dfms = Fm_deriv(sk)
        Qp = 2.0 * (sk - np.sinh(sk)) / (sk ** 2)
        Qpp_over_Qp = -1.0 / Qp - 4.0 / sk

        # 1) Вычет для <V_1^{§6.1}, 1>:
        Hs = np.exp(sk) * Pms / (sk ** 2)
        dlogH = 1.0 + dlogP_ms - 2.0 / sk
        r_v1_double = (Hs / (2.0 * (Qp ** 2))) * (dlogH - Qpp_over_Qp)
        r_v1_simple = (np.exp(sk) * Pms / (sk * Qp)) * (1.0 / (2.0 * sk) - fms)
        res_v1[k] = 2.0 * float(np.real(r_v1_double + r_v1_simple))

        # 2) Вычет для <U, TW> (ускоренный до O(k^{-4}) выделением 1/(2s)):
        res_utw[k] = -2.0 * float(np.real(2.0 * r_k[k] * (Pms ** 2) * (1.0 / (2.0 * sk) - fms)))

        # 3) Вычет для <W, TW>:
        Ms = (Pms ** 2) * fms / sk
        dlogM = 2.0 * dlogP_ms + dfms / fms - 1.0 / sk
        r_ww_double = (Ms / (2.0 * (Qp ** 2))) * (dlogM - Qpp_over_Qp)
        r_ww_simple = -(Pms ** 2) * (fms ** 2) / Qp
        res_wtw[k] = 2.0 * float(np.real(r_ww_double + r_ww_simple))

    v1_400 = v1_res0 + float(np.sum(res_v1[:400]))
    v1_800 = v1_res0 + float(np.sum(res_v1[:800]))
    v1_total = (8.0 * v1_800 - v1_400) / 7.0
    print(f"  <U, 1> = f_H(0) residue                = {u1_total:.12f} (grid:  2.551317222276)")
    print(f"  <V_1^{{§6.1}}, 1> raw K=800             = {v1_800:.12f}")
    print(f"  <V_1^{{§6.1}}, 1> O(K^-3) extrapolated  = {v1_total:.12f} (grid: -0.760599353809, |diff|={abs(v1_total - (-0.760599353809)):.2e})")
    assert abs(u1_total - 2.551317222276) < 1e-11
    assert abs(v1_total - (-0.760599353809)) < 1e-12

    # 4. Точное представление Винера–Хопфа для c_2 и C_rho в §6.4 через определитель Грама–поворота 2x2
    print("\n=== 4. Exact Wiener-Hopf 2x2 Gram-Turn Determinant for c_2 and C_rho (§6.4) ===")
    vtv = 0.039958599729073
    utu = 12.0 * vtv
    lead_utw = -6.0 * vtv + 0.3 * d0 - Sigma_0
    utw_400 = lead_utw + float(np.sum(res_utw[:400]))
    utw_800 = lead_utw + float(np.sum(res_utw[:800]))
    utw_total = (8.0 * utw_800 - utw_400) / 7.0

    res0_wtw = 6.0 * Sigma_2 + (0.5 + 12.0 * (d0 ** 2)) * Sigma_0 + (121.0 / 1400.0) * d0 + 2.8 * (d0 ** 3) + 4.2 * g3
    wtw_400 = res0_wtw + float(np.sum(res_wtw[:400]))
    wtw_800 = res0_wtw + float(np.sum(res_wtw[:800]))
    wtw_total = (8.0 * wtw_800 - wtw_400) / 7.0

    alpha = -(3.0 * (d0 ** 2) + 1.0 / 20.0)
    v_tv3_wh = (utw_total - alpha * utu) / 12.0
    v3_tv3_wh = (wtw_total - 2.0 * alpha * utw_total + (alpha ** 2) * utu) / 12.0
    det_VV3 = (utu * wtw_total - (utw_total ** 2)) / 144.0
    C_const = 12.0 * math.sqrt(3.0 / math.pi)
    c1_wh = C_const * vtv
    c2_wh = 6.0 * C_const * det_VV3 / vtv
    C_rho_wh = abs(c1_wh / c2_wh)

    print(f"  <U, TW>   (Wiener-Hopf residue) = {utw_total:.12f} (grid Rich: -0.150169088439)")
    print(f"  <W, TW>   (Wiener-Hopf residue) = {wtw_total:.12f} (grid Rich:  0.032653149614)")
    print(f"  <V, TV_3> (Wiener-Hopf residue) = {v_tv3_wh:.12f} (grid Rich: -0.004319975190)")
    print(f"  <V_3,TV_3>(Wiener-Hopf residue) = {v3_tv3_wh:.12f} (grid Rich: -0.000730984137)")
    print(f"  c_2 = 6*C*det_2(V,V_3)/<V,TV>   = {c2_wh:.12f} (grid Rich: -0.084291356072)")
    print(f"  C_rho = |c_1/c_2| (C-invariant) = {C_rho_wh:.10f} (grid Rich:  5.5589677830)")
    assert abs(utw_total - (-0.150169088439)) < 2e-12
    assert abs(v_tv3_wh - (-0.004319975190)) < 1e-12
    assert abs(v3_tv3_wh - (-0.000730984137)) < 5e-12
    assert abs(c2_wh - (-0.084291356072)) < 5e-10
    print("\n=== ALL §6.1, THEOREM D, AND §6.4 (c_2, C_rho) CLOSED-FORM/RESIDUE CHECKS PASSED ===")


if __name__ == "__main__":
    main()

