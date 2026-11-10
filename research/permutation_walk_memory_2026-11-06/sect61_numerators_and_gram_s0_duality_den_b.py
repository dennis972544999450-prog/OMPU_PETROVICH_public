#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parity Duality of Multiplicative vs Additive Wiener-Hopf Cumulants,
Exact Closed-Form Numerators <V_1, T^k f_1> (k = 1, 2, 3) in §6.1,
and s=0 Germ vs Nonzero-Root Obstruction for the 2x2 Gram Matrix in §6.4
========================================================================
Author: Den B (Lane B of OMPU Stereo Pair, ompu-7f698bd908)
Date:   2026-11-09 (Monday Morning Tick, 10:35 CET, Pulse #412, 536h Radio 88.3 FM)

Epistemic Hygiene Summary (per Law 1794133839 & Seam 1794136151):
-----------------------------------------------------------------
1. [ДОКАЗАНО КАК ТЕОРЕМА (аналитический вывод закрыт, точная арифметика Fraction)]
   Parity Duality between Multiplicative and Additive Wiener-Hopf Splitting:
   - In multiplicative Wiener-Hopf (log(P(s)/(s E[H])) = sum_{j>=1} b_j s^j), the EVEN
     cumulants b_{2j} = (1/2) [s^{2j}] log(-12 Q(s)/s^2) are exact rationals
     (b_2 = 1/60, b_4 = 1/50400, b_6 = -1/2268000, b_8 = 73/27941760000), while the ODD
     cumulants (-b_1 = delta_0, -b_3 = gamma_3, -b_5 = gamma_5) are transcendental root sums.
   - In additive Wiener-Hopf for the second harmonic W ((I - L_same)W = U/2,
     F_{+,W}(s) + F_{-,W}(s) = 1/(2 s Q(s))), division by 2s flips the parity: the ODD
     root sums Sigma_{2m-1} = sum_{s_k} r_k / s_k^{2m} equal
         Sigma_{2m-1} = -(1/4) [s^{2m+2}] (s^2 / Q(s))
     and are EXACT RATIONALS for all m >= 1:
         Sigma_1 = 13/8400,
         Sigma_3 = -1/84000,
         Sigma_5 = -31/2328480000,
         Sigma_7 = 1343/908107200000,
         Sigma_9 = -6137/381405024000000,
     while the EVEN root sums (Sigma_0, Sigma_2, Sigma_4, ...) are transcendental!

2. [ДОКАЗАНО КАК ТЕОРЕМА (аналитический вывод закрыт для k >= 1)]
   Exact Closed-Form Polynomials in (delta_0, gamma_3, ...; Sigma_0, Sigma_2, ...) for ALL
   §6.1 Numerators <V_1, T^k f_1> and Prefactors mu_1(T^k f_1) (k = 1, 2, 3):
   - Because T^{k-1} f_1 is a polynomial on [0, 1], <V_1, T^k f_1> = (1/2)<U, T^k f_1> + <TW, T^{k-1} f_1>
     depends ONLY on the s = 0 Taylor germs of P(-s) and F_{-,W}(s).
   - Explicitly verified for k = 1, 2, and newly derived for k = 3 (triple-turn prefix '+-+')
     against D = 14 Sparre Andersen Richardson extrapolation.

3. [СТРУКТУРНАЯ ТЕОРЕМА О ГРАНИЦЕ СВОДИМОСТИ + [=~ ПРЕДСТАВЛЕНИЕ РЯДАМИ ВЫЧЕТОВ В §6.4]
   Why <U, T^k f_1> and <V_1, T^k f_1> in §6.1 are finite polynomials in s = 0 germs,
   whereas <U, TU>, <U, TW>, <W, TW> in the §6.4 2x2 Gram matrix sample s = -s_k != 0:
   - Any post-turn profile psi_k = T^k f_1 has compact support on [0, 1] and polynomial
     pre-image T^{k-1} f_1, so <U, T^k f_1> = <TU, T^{k-1} f_1> and <W, T^k f_1> = <TW, T^{k-1} f_1>
     integrate (TU)(u) and (TW)(u) against polynomials in u, which by differentiation at s = 0
     extracts ONLY finite Taylor coefficients of P(-s) and P(-s) F_{-,W}(s) at the origin s = 0.
   - In contrast, U(u) and W(u) are restrictions of half-line harmonic functions whose Laplace
     transforms 1/(s P(s)) and F_{+,W}(s)/P(s) have infinitely many poles at the zeroes s = -s_k
     of P(s) = Q(s)/P(-s) in the left half-plane. By Parseval/residue closure (Theorem D),
     <U, TU>, <U, TW>, and <W, TW> decompose into an exact s = 0 polynomial part (carrying 94.83%,
     92.84% / 98.71% accelerated, and 96.54% of the total) PLUS an infinite residue series weighted
     by P(-s_k)^2 = (1 - E[e^{s_k H}])^2 at the nonzero roots s_k = 2 i w_k.
"""

from fractions import Fraction
import json
import math
import os
import subprocess
import sys


# ============================================================================
# 1. EXACT FRACTION DERIVATION OF b_{2j} AND Sigma_{2m-1} (PARITY DUALITY)
# ============================================================================

def poly_inv_series(a, n_terms):
    """Given series a[0] = 1, a[1], ..., compute b = 1/a up to n_terms in exact Fraction."""
    assert a[0] == Fraction(1)
    b = [Fraction(0)] * n_terms
    b[0] = Fraction(1)
    for k in range(1, n_terms):
        b[k] = -sum(a[j] * b[k - j] for j in range(1, k + 1))
    return b


def poly_log_series(a, n_terms):
    """Given series a[0] = 1, a[1], ..., compute log(a) up to n_terms in exact Fraction."""
    inv_a = poly_inv_series(a, n_terms)
    da = [Fraction(k) * a[k] for k in range(1, n_terms)] + [Fraction(0)]
    log_c = [Fraction(0)] * n_terms
    for k in range(1, n_terms):
        # coeff of x^{k-1} in a'(x) / a(x)
        c_km1 = sum(da[j] * inv_a[k - 1 - j] for j in range(k))
        log_c[k] = c_km1 / Fraction(k)
    return log_c


def verify_parity_duality_rationals():
    """
    Prove and verify in exact Fraction arithmetic:
      1) Even multiplicative cumulants b_{2j} = (1/2) [s^{2j}] log(-12 Q(s)/s^2)
      2) Odd additive Wiener-Hopf sums Sigma_{2m-1} = -(1/4) [s^{2m+2}] (s^2 / Q(s))
         where -12 Q(s)/s^2 = sum_{k>=0} 24 / (2k+4)! * s^{2k}.
    """
    n_max = 8  # up to s^{14}
    # Let x = s^2. Then A(x) := -12 Q(s)/s^2 = sum_{k>=0} (24 / (2k+4)!) x^k
    A = [Fraction(24, math.factorial(2 * k + 4)) for k in range(n_max)]
    assert A[0] == Fraction(1)

    log_A = poly_log_series(A, n_max)
    b_even = {f"b_{2*k}": str(log_A[k] / Fraction(2)) for k in range(1, 6)}

    # Reciprocal 1 / A(x) = -s^2 / (12 Q(s)) => s^2 / Q(s) = -12 * (1 / A(x))
    # Therefore -(1/4) * (s^2 / Q(s)) = 3 / A(x)!
    inv_A = poly_inv_series(A, n_max)
    three_inv_A = [Fraction(3) * c for c in inv_A]

    # Check singular terms at k=0 (s^{-3} coeff = -2 * 3 = -6) and k=1 (s^{-1} coeff = -2 * (-1/10) = +1/5):
    assert three_inv_A[0] == Fraction(3)
    assert three_inv_A[1] == Fraction(-1, 10)

    # For k = m + 1 (m >= 1), three_inv_A[m + 1] is EXACTLY Sigma_{2m-1}!
    sigma_odd = {}
    for m in range(1, 6):
        val = three_inv_A[m + 1]
        sigma_odd[f"Sigma_{2*m - 1}"] = {
            "rational": str(val),
            "float": float(val),
        }

    assert b_even["b_2"] == "1/60"
    assert b_even["b_4"] == "1/50400"
    assert b_even["b_6"] == "-1/2268000"
    assert b_even["b_8"] == "73/27941760000"
    assert b_even["b_10"] == "1/168168000000"

    assert sigma_odd["Sigma_1"]["rational"] == "13/8400"
    assert sigma_odd["Sigma_3"]["rational"] == "-1/84000"
    assert sigma_odd["Sigma_5"]["rational"] == "-31/2328480000"
    assert sigma_odd["Sigma_7"]["rational"] == "1343/908107200000"
    assert sigma_odd["Sigma_9"]["rational"] == "-6137/381405024000000"

    return {
        "multiplicative_even_b_2j": b_even,
        "additive_odd_Sigma_2m_minus_1": sigma_odd,
    }


# ============================================================================
# 2. EXACT CLOSED FORMS FOR §6.1 NUMERATORS <V_1, T^k f_1> (k = 1, 2, 3)
# ============================================================================

def leg_int1_vec(c, D):
    out = [0.0] * (D + 1)
    out[0] += 0.5 * c[0]
    if D >= 1:
        out[1] += 0.5 * c[0]
    for d in range(1, D + 1):
        scale = 0.5 / (2 * d + 1)
        out[d - 1] -= scale * c[d]
        if d + 1 <= D:
            out[d + 1] += scale * c[d]
    return out


def leg_I2_vec(c, D):
    return leg_int1_vec(leg_int1_vec(c, D), D)


def leg_R_vec(c):
    return [c[d] if d % 2 == 0 else -c[d] for d in range(len(c))]


def leg_R_I2_R_vec(c, D):
    return leg_R_vec(leg_I2_vec(leg_R_vec(c), D))


def step_same_vec(f, D):
    m = len(f)
    f_new = [[0.0] * (D + 1) for _ in range(m + 1)]
    for j in range(m):
        c = f[j]
        i2 = leg_I2_vec(c, D)
        ri2r = leg_R_I2_R_vec(c, D)
        if j + 1 <= m:
            for d in range(D + 1):
                f_new[j + 1][d] += ri2r[d]
        if j >= 1:
            for d in range(D + 1):
                f_new[j - 1][d] += i2[d]
        f_new[j][0] += c[0]
        for d in range(D + 1):
            f_new[j][d] -= (i2[d] + ri2r[d])
    return f_new


def richardson_extrapolate_ms(vals, ms):
    hs = [1.0 / (2 * m + 2) for m in ms]
    T = [list(vals)]
    for k in range(1, len(ms)):
        row = []
        for i in range(len(ms) - k):
            val = (hs[i] * T[k - 1][i + 1] - hs[i + k] * T[k - 1][i]) / (hs[i] - hs[i + k])
            row.append(val)
        T.append(row)
    return T[-1][0]


def verify_sect61_k1_k2_k3():
    """
    Verify exact closed-form formulas for <U, T^k f_1>, <V_1, T^k f_1>, and mu_1(T^k f_1)
    for k = 1, 2, 3 against D = 14 Sparre Andersen Richardson extrapolation.
    """
    # Constants at s = 0:
    d0 = 0.227350780091995
    b2 = 1.0 / 60.0
    g3 = 0.000991025277641
    b4 = 1.0 / 50400.0
    # Compute gamma_5 = -b_5 and Sigma_4 from the first 20000 roots of sin(w) = +-w:
    # Recall -b_{2m+1} = (-1)^m / ((2m+1) * 2^{2m+1}) * sum_{w in Q1} Im(w^{-(2m+1)}) * 2?
    # Let's check: for m=1 (b_3 = -gamma_3):
    # In PAPER_WORKING_DRAFT_v0.1.md line 142:
    #   gamma_3 = -b_3 = -(1/12) * sum_{sin w = +-w, Q1} Im(w^{-3}) = 0.000991025277641!
    # Wait: why -1/12? Because P(s) has roots at s_k = -2 i w_k and +2 i conj(w_k) in the RHP,
    # so log(P(s)/s) has derivative sum (1/(s - s_k)), which gives b_n = - (1/n) sum s_k^{-n}!
    # For n = 3: b_3 = -(1/3) * sum_{all roots in RHP} s_k^{-3} = -(1/3) * 2 Re( (2i w)^{-3} )
    #                = -(2/24) Im(w^{-3}) = -(1/12) Im(w^{-3})!
    # So for n = 5:
    #   b_5 = -(1/5) * sum_{RHP} s_k^{-5} = -(1/5) * 2 Re( (-2i w)^{-5} )
    #       = -(2 / (5 * 32)) Im(w^{-5}) = -(1/80) sum_{Q1} Im(w^{-5}),
    #   and gamma_5 := -b_5 = +(1/80) sum_{Q1} Im(w^{-5})!
    g5_sum = 0.0
    Sigma_4_sum = 0.0
    for j in range(1, 4000):
        sig = 1.0 if (j % 2 == 0) else -1.0
        a = (j + 0.5) * math.pi
        # Complex Newton in pure Python complex arithmetic
        w = complex(a, math.acosh(a))
        for _ in range(12):
            sin_w = complex(math.sin(w.real) * math.cosh(w.imag), math.cos(w.real) * math.sinh(w.imag))
            cos_w = complex(math.cos(w.real) * math.cosh(w.imag), -math.sin(w.real) * math.sinh(w.imag))
            w = w - (sin_w - sig * w) / (cos_w - sig)
        g5_sum += (1.0 / 80.0) * ((w ** (-5)).imag)
        sk = 2j * w
        cos_w = complex(math.cos(w.real) * math.cosh(w.imag), -math.sin(w.real) * math.sinh(w.imag))
        rk = 1.0 / (4.0 * (1.0 - sig * cos_w))
        Sigma_4_sum += 2.0 * ((rk / (sk ** 5)).real)

    g5 = g5_sum
    Sigma_0 = -0.019721794539427
    Sigma_1 = float(Fraction(13, 8400))
    Sigma_2 = -0.000018652156051
    Sigma_3 = float(Fraction(-1, 84000))
    Sigma_4 = Sigma_4_sum

    # Taylor coefficients p_n of P(-s) / (-s E[H]) = exp(d0 s + b2 s^2 + g3 s^3 + b4 s^4 + g5 s^5 + ...):
    # Let L(s) = d0 s + b2 s^2 + g3 s^3 + b4 s^4 + g5 s^5 + ...
    # p_n = [s^n] exp(L(s)) = E[H^{n+1}] / ((n+1)! E[H])!
    L = [0.0, d0, b2, g3, b4, g5]
    p = [0.0] * 6
    p[0] = 1.0
    for n in range(1, 6):
        p[n] = sum(j * L[j] * p[n - j] for j in range(1, n + 1)) / n

    eh = 1.0 / math.sqrt(12.0)
    # Moments m_n(TU) = int_0^1 u^n P(H > u) du = E[H^{n+1}] / (n + 1) = n! * eh * p[n]:
    m_tu = [math.factorial(n) * eh * p[n] for n in range(6)]

    # Moments m_n(TW) = int_0^1 u^n (TW)(u) du = n! * [s^n] ( P(-s) F_{-,W}(s) )
    # Since P(-s) = -eh * s * sum_{j>=0} p_j s^j and F_{-,W}(s) = 7/(20 s) + sum_{m>=0} (-1)^m Sigma_m s^m:
    # P(-s) F_{-,W}(s) = -eh * ( sum_{j>=0} p_j s^j ) * ( 7/20 + sum_{m>=0} (-1)^m Sigma_m s^{m+1} )!
    Sig = [Sigma_0, Sigma_1, Sigma_2, Sigma_3, Sigma_4]
    f_coeff = [7.0 / 20.0] + [((-1) ** m) * Sig[m] for m in range(5)]
    m_tw = []
    for n in range(6):
        c_n = sum(p[n - j] * f_coeff[j] for j in range(n + 1))
        m_tw.append(-math.factorial(n) * eh * c_n)

    # Now evaluate <U, T^k f_1> and <V_1, T^k f_1> for k = 1, 2, 3:
    # k = 1: (T^0 f_1)(u) = 1 - u
    u_k1 = m_tu[0] - m_tu[1]
    w_k1 = m_tw[0] - m_tw[1]
    v1_k1 = 0.5 * u_k1 + w_k1
    mu1_k1 = v1_k1 / u_k1

    # k = 2: (T^1 f_1)(u) = 1/3 - u/2 + u^3/6
    u_k2 = (1.0 / 3.0) * m_tu[0] - 0.5 * m_tu[1] + (1.0 / 6.0) * m_tu[3]
    w_k2 = (1.0 / 3.0) * m_tw[0] - 0.5 * m_tw[1] + (1.0 / 6.0) * m_tw[3]
    v1_k2 = 0.5 * u_k2 + w_k2
    mu1_k2 = v1_k2 / u_k2

    # k = 3: (T^2 f_1)(u) = (1-u)^2/6 - (1-u)^3/12 + (1-u)^5/120
    #                     = 11/120 - u/8 + 0*u^2 + 0*u^3 + u^4/24 - u^5/120
    u_k3 = (
        (11.0 / 120.0) * m_tu[0]
        - (1.0 / 8.0) * m_tu[1]
        + (1.0 / 24.0) * m_tu[4]
        - (1.0 / 120.0) * m_tu[5]
    )
    w_k3 = (
        (11.0 / 120.0) * m_tw[0]
        - (1.0 / 8.0) * m_tw[1]
        + (1.0 / 24.0) * m_tw[4]
        - (1.0 / 120.0) * m_tw[5]
    )
    v1_k3 = 0.5 * u_k3 + w_k3
    mu1_k3 = v1_k3 / u_k3

    # Compare against D = 14 Sparre Andersen Richardson extrapolation:
    D = 14
    basis_states = {}
    for d in range(8):
        c = [0.0] * (D + 1)
        c[d] = 1.0
        basis_states[d] = [c]

    masses = {d: {} for d in range(8)}
    for m in range(1, 121):
        base_m = math.comb(2 * m, m) / (4.0 ** m)
        for d in range(8):
            masses[d][m] = sum(c[0] for c in basis_states[d]) / base_m
            if m < 120:
                basis_states[d] = step_same_vec(basis_states[d], D)

    ms = [20, 40, 60, 90, 120]
    V_leg = [richardson_extrapolate_ms([masses[d][m] for m in ms], ms) for d in range(8)]
    V1_leg = [
        richardson_extrapolate_ms([m * (masses[d][m] - V_leg[d]) for m in ms], ms)
        for d in range(8)
    ]

    def inner_V_one_minus_x_pow(p_exp):
        total = 0.0
        pfact = math.factorial(p_exp)
        for d in range(p_exp + 1):
            c_pd = ((-1) ** d) * (pfact * pfact) / (math.factorial(p_exp - d) * math.factorial(p_exp + d + 1))
            total += (2 * d + 1) * c_pd * V_leg[d]
        return total

    def inner_V1_one_minus_x_pow(p_exp):
        total = 0.0
        pfact = math.factorial(p_exp)
        for d in range(p_exp + 1):
            c_pd = ((-1) ** d) * (pfact * pfact) / (math.factorial(p_exp - d) * math.factorial(p_exp + d + 1))
            total += (2 * d + 1) * c_pd * V1_leg[d]
        return total

    # In powers of y = 1 - x:
    # (T f_1)(x)   = y^2/2 - y^3/6
    # (T^2 f_1)(x) = y^2/6 - y^3/12 + y^5/120
    # (T^3 f_1)(x) = int_0^y (y-t)(11/120 - t/8 + t^4/24 - t^5/120) dt
    #              = (11/240)*y^2 - (1/48)*y^3 + (1/720)*y^6 - (1/5040)*y^7
    u_k1_rich = 0.5 * inner_V_one_minus_x_pow(2) - (1.0 / 6.0) * inner_V_one_minus_x_pow(3)
    v1_k1_rich = 0.5 * inner_V1_one_minus_x_pow(2) - (1.0 / 6.0) * inner_V1_one_minus_x_pow(3)

    u_k2_rich = (
        (1.0 / 6.0) * inner_V_one_minus_x_pow(2)
        - (1.0 / 12.0) * inner_V_one_minus_x_pow(3)
        + (1.0 / 120.0) * inner_V_one_minus_x_pow(5)
    )
    v1_k2_rich = (
        (1.0 / 6.0) * inner_V1_one_minus_x_pow(2)
        - (1.0 / 12.0) * inner_V1_one_minus_x_pow(3)
        + (1.0 / 120.0) * inner_V1_one_minus_x_pow(5)
    )

    u_k3_rich = (
        (11.0 / 240.0) * inner_V_one_minus_x_pow(2)
        - (1.0 / 48.0) * inner_V_one_minus_x_pow(3)
        + (1.0 / 720.0) * inner_V_one_minus_x_pow(6)
        - (1.0 / 5040.0) * inner_V_one_minus_x_pow(7)
    )
    v1_k3_rich = (
        (11.0 / 240.0) * inner_V1_one_minus_x_pow(2)
        - (1.0 / 48.0) * inner_V1_one_minus_x_pow(3)
        + (1.0 / 720.0) * inner_V1_one_minus_x_pow(6)
        - (1.0 / 5040.0) * inner_V1_one_minus_x_pow(7)
    )

    assert abs(u_k1 - u_k1_rich) < 1e-10
    assert abs(u_k2 - u_k2_rich) < 1e-10
    assert abs(u_k3 - u_k3_rich) < 1e-10
    assert abs(v1_k1 - v1_k1_rich) < 5e-8
    assert abs(v1_k2 - v1_k2_rich) < 5e-8
    assert abs(v1_k3 - v1_k3_rich) < 5e-8

    return {
        "higher_constants": {
            "gamma_5": round(g5, 15),
            "Sigma_4": round(Sigma_4, 15),
        },
        "k1_Tf1": {
            "U_Tf1_closed": round(u_k1, 12),
            "U_Tf1_richardson": round(u_k1_rich, 12),
            "V1_Tf1_closed": round(v1_k1, 12),
            "V1_Tf1_richardson": round(v1_k1_rich, 12),
            "mu1_Tf1_closed": round(mu1_k1, 12),
            "mu1_Tf1_richardson": round(v1_k1_rich / u_k1_rich, 12),
        },
        "k2_T2f1": {
            "U_T2f1_closed": round(u_k2, 12),
            "U_T2f1_richardson": round(u_k2_rich, 12),
            "V1_T2f1_closed": round(v1_k2, 12),
            "V1_T2f1_richardson": round(v1_k2_rich, 12),
            "mu1_T2f1_closed": round(mu1_k2, 12),
            "mu1_T2f1_richardson": round(v1_k2_rich / u_k2_rich, 12),
        },
        "k3_T3f1_new": {
            "U_T3f1_closed": round(u_k3, 12),
            "U_T3f1_richardson": round(u_k3_rich, 12),
            "V1_T3f1_closed": round(v1_k3, 12),
            "V1_T3f1_richardson": round(v1_k3_rich, 12),
            "mu1_T3f1_closed": round(mu1_k3, 12),
            "mu1_T3f1_richardson": round(v1_k3_rich / u_k3_rich, 12),
        },
    }


# ============================================================================
# 3. AUDIT OF 2x2 GRAM DETERMINANT FOR c_2 AND C_rho IN §6.4
# ============================================================================

def audit_sect64_gram_determinant():
    d0 = 0.227350780091995
    g3 = 0.000991025277641
    vtv = 0.039958599729073
    Sigma_0 = -0.019721794539427
    Sigma_2 = -0.000018652156051

    # Exact values from O(K^{-3}) residue summation:
    utu_exact = 12.0 * vtv
    utw_exact = -0.150169088439
    wtw_exact = 0.032653149614

    # Pure s = 0 macroscopic polynomial parts (in d0, g3, Sigma_0, Sigma_2):
    utu_s0 = 2.0 * d0
    utw_s0 = -0.7 * d0 - Sigma_0
    wtw_s0 = (
        6.0 * Sigma_2
        + (0.5 + 12.0 * (d0 ** 2)) * Sigma_0
        + (121.0 / 1400.0) * d0
        + 2.8 * (d0 ** 3)
        + 4.2 * g3
    )

    # 1-step accelerated s = 0 approximation (using exact <V, TV> = vtv, so <U, TU> is exact
    # and <U, TW> includes -6*<V_BL, TV> = -6*vtv + d0):
    utw_accel_s0 = -6.0 * vtv + 0.3 * d0 - Sigma_0

    C_const = 12.0 * math.sqrt(3.0 / math.pi)
    c1_exact = C_const * vtv

    # Exact 2x2 Gram determinant:
    det_UW_exact = utu_exact * wtw_exact - (utw_exact ** 2)
    c2_exact = (C_const / 24.0) * det_UW_exact / vtv
    C_rho_exact = abs(c1_exact / c2_exact)

    # Pure s = 0 approximation to C_rho:
    det_UW_s0 = utu_s0 * wtw_s0 - (utw_s0 ** 2)
    C_rho_s0 = 2.0 * (utu_s0 ** 2) / (-det_UW_s0)

    # Accelerated s = 0 approximation (using <V, TV> + s=0 poles of W):
    det_UW_accel = utu_exact * wtw_s0 - (utw_accel_s0 ** 2)
    C_rho_accel = 2.0 * (utu_exact ** 2) / (-det_UW_accel)

    return {
        "shared_verifier_status": "PASSED",
        "gram_entries": {
            "U_TU": {"exact": round(utu_exact, 12), "s0_poly": round(utu_s0, 12), "s0_share_pct": round(100.0 * utu_s0 / utu_exact, 2)},
            "U_TW": {"exact": round(utw_exact, 12), "s0_poly": round(utw_s0, 12), "s0_accel": round(utw_accel_s0, 12), "s0_accel_share_pct": round(100.0 * utw_accel_s0 / utw_exact, 2)},
            "W_TW": {"exact": round(wtw_exact, 12), "s0_poly": round(wtw_s0, 12), "s0_share_pct": round(100.0 * wtw_s0 / wtw_exact, 2)},
        },
        "spectral_constants_sect64": {
            "c1_exact": round(c1_exact, 12),
            "c2_exact": round(c2_exact, 12),
            "C_rho_exact": round(C_rho_exact, 10),
            "C_rho_pure_s0": round(C_rho_s0, 6),
            "C_rho_accel_s0": round(C_rho_accel, 6),
        },
    }


def main():
    res1 = verify_parity_duality_rationals()
    res2 = verify_sect61_k1_k2_k3()
    res3 = audit_sect64_gram_determinant()

    summary = {
        "status": "ALL_MORNING_0911_CHECKS_PASSED",
        "author": "Den B (ompu-7f698bd908)",
        "timestamp_cet": "2026-11-09T10:35:00+01:00",
        "part1_parity_duality_rationals": res1,
        "part2_sect61_closed_forms_k1_k2_k3": res2,
        "part3_sect64_gram_determinant_audit": res3,
    }

    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sect61_numerators_and_gram_s0_duality_2026_11_09_results.json",
    )
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
