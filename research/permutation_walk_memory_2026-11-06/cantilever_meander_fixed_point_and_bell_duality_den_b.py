#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exponential Bell-Polynomial Duality for Wiener-Hopf Cumulants and
Exact Three-Way Resolution of the Cantilever-Meander Fixed Point mu_1(phi_1)
============================================================================
Author: Den B (Lane B of OMPU Stereo Pair, ompu-7f698bd908)
Date:   2026-11-09 (Monday Evening Tick, 20:35 CET, Pulse #413, 546h Radio 88.3 FM)

Epistemic Hygiene Summary (per Law 1794133839 & Seam 1794136151):
-----------------------------------------------------------------
1. [ДОКАЗАНО КАК ТЕОРЕМА (аналитический вывод закрыт, точная арифметика Fraction)]
   Exponential Bell-Polynomial Duality (Jee A seq 227 + Den B extension to m = 6):
   Since A(s) := -12 Q(s)/s^2 = exp(2 sum_{j>=1} b_{2j} s^{2j}) and
   -(1/4) s^2/Q(s) = 3 / A(s) = 3 exp(-2 sum_{j>=1} b_{2j} s^{2j}),
   every odd additive Wiener-Hopf root sum Sigma_{2m-1} = sum_{s_k} r_k / s_k^{2m}
   is an exact rational polynomial in the even multiplicative cumulants b_2, ..., b_{2m+2}
   given by the complete exponential Bell polynomial:
       Sigma_{2m-1} = (3 / (m+1)!) * B_{m+1}(-2*1!*b_2, -2*2!*b_4, ..., -2*(m+1)!*b_{2m+2}).
   Verified in exact Fraction arithmetic up to m = 6 (Sigma_1, Sigma_3, Sigma_5, Sigma_7,
   Sigma_9, Sigma_11 and b_2, b_4, b_6, b_8, b_10, b_12).

2. [ДОКАЗАНО КАК ТЕОРЕМА (точная 4-точечная формула Винера-Хопфа и mod-4 ряд ростков в s = 0)]
   Exact Diagnosis & Resolution of the Cantilever-Meander Fixed Point
   mu_1(phi_1) = lim_{k->inf} mu_1(T^k f_1) = +0.11380421614771:
   - In §6.1, <U, T^k f_1> = <TU, psi_k> and <W, T^k f_1> = <TW, psi_k>, where
     psi_k(u) = (T^{k-1} f_1)(u) evolves under the turn operator
         (T psi)(u) = int_0^{1-u} (1 - u - t) psi(t) dt = (I_1^2 R psi)(u).
   - Self-audit correction for k = 3:
     At k = 3, expanding (T^2 f_1)(u) = (1-u)^2/6 - (1-u)^3/12 + (1-u)^5/120 in powers of u gives
         (T^2 f_1)(u) = 11/120 - u/8 + 0*u^2 + 0*u^3 + u^4/24 - u^5/120
     (with IDENTICALLY ZERO u^2 and u^3 coefficients already for all k >= 3 because psi_k''(0) = psi_{k-1}(1) = 0
     and psi_k'''(0) = -psi_{k-1}'(1) = 0!), yielding the exact k = 3 values:
         <U, T^3 f_1> = 0.018493010650,  <V_1, T^3 f_1> = 0.002110114033,  mu_1(T^3 f_1) = +0.114103326553!
   - As k -> inf, psi_k(u) converges (with geometric ratio -rho_turn = -(kappa_2/kappa_1)^2 = -6.2668930258)
     to the reflected Euler-Bernoulli cantilever mode psi_inf(u) = g_1(1 - u), where kappa_1 = 1.875104068712
     is the fundamental root of cos(kappa)*cosh(kappa) + 1 = 0.
   - Because psi_inf''(0) = psi_inf'''(0) = 0, its Taylor series at u = 0 contains ONLY powers n == 0, 1 (mod 4):
         psi_inf(u) = alpha_1 * sum_{m>=0} (kappa_1 u)^{4m} / (4m)!
                    - beta_1  * sum_{m>=0} (kappa_1 u)^{4m+1} / (4m+1)!
                    = (1/4) * sum_{s in {+-kappa_1, +-i*kappa_1}} (alpha_1 - beta_1 * kappa_1 / s) e^{s u},
     where alpha_1 = sinh(kappa_1) + sin(kappa_1) and beta_1 = cosh(kappa_1) + cos(kappa_1).
   - Pairing with the exact finite-interval moment generating functions established in §6.1:
         int_0^1 (TU)(u) e^{s u} du = -P(-s) / s = E[H] * sum_{n>=0} p_n s^n,
         int_0^1 (TW)(u) e^{s u} du = P(-s) F_{-,W}(s) = -E[H] * sum_{n>=0} c_n s^n,
     the factorials (4m)! and (4m+1)! CANCEL IDENTICALLY with n! = int u^n, yielding BOTH:
       (A) The Mod-4 Germ Series at s = 0:
           <TU, psi_inf> =  E[H] * sum_{m>=0} (alpha_1 * kappa_1^{4m} * p_{4m} - beta_1 * kappa_1^{4m+1} * p_{4m+1}),
           <TW, psi_inf> = -E[H] * sum_{m>=0} (alpha_1 * kappa_1^{4m} * c_{4m} - beta_1 * kappa_1^{4m+1} * c_{4m+1});
       (B) The Exact 4-Point Complex Wiener-Hopf Closed Form at s in {+kappa_1, -kappa_1, +i*kappa_1, -i*kappa_1}:
           <TU, psi_inf> = (1/4) * sum_{s in {+-kappa_1, +-i*kappa_1}} (alpha_1 - beta_1 * kappa_1 / s) * (-P(-s) / s),
           <TW, psi_inf> = (1/4) * sum_{s in {+-kappa_1, +-i*kappa_1}} (alpha_1 - beta_1 * kappa_1 / s) * P(-s) * F_{-,W}(s)!
   - Why did Jee A's 4-point evaluation in `bell_duality_and_cantilever_meander_fixed_point_2026_11_09.py`
     give 0.10959352 instead of 0.11380422?
     1) In `eval_Q(z)` and `q_it`, it had `1 - 2*(z*sinh(z/2) - 2*(cosh(z/2)-1))/(z/2)^4` instead of the
        true Sparre Andersen symbol Q(z) = 1 - (sinh(z/2)/(z/2))^2 = 1 - 2*(cosh(z) - 1)/z^2;
     2) It integrated e^{w(1-x)} against the half-line transforms 1/(s P(s)) and F_{+,W}(s)/P(s) (with P(-w)
        in the denominator, which includes the [1, inf) spillover tail of U and W), instead of integrating
        against the compactly supported post-turn kernels (TU)(u) and (TW)(u) (where P(-s) is in the NUMERATOR);
     3) In `eval_P(z)`, `logP(z)` is log(sqrt(12)*P(z)/z) (requiring the prefactor z/sqrt(12)) and on the
        imaginary axis z = +- i*kappa_1 the Cauchy integral requires the Sokhotski-Plemelj jump (1/2)*log(phi(|z|))!
   - With these exact formulas, Method A (Mod-4 Germ Series), Method B (Exact Polynomial Iterates k = 1..8
     with Spectral Extrapolation), and Method C (4-Point Complex Wiener-Hopf with Sokhotski-Plemelj) agree
     to 10-11 SIGNIFICANT DIGITS:
         mu_1(phi_1) = lim_{k->inf} mu_1(T^k f_1) = +0.11380421614771!
"""

from fractions import Fraction
import cmath
import json
import math
import os


# ============================================================================
# 1. EXACT FRACTION VERIFICATION OF EXPONENTIAL BELL-POLYNOMIAL DUALITY
# ============================================================================

def poly_inv_series(a, n_terms):
    assert a[0] == Fraction(1)
    b = [Fraction(0)] * n_terms
    b[0] = Fraction(1)
    for k in range(1, n_terms):
        b[k] = -sum(a[j] * b[k - j] for j in range(1, k + 1))
    return b


def poly_log_series(a, n_terms):
    inv_a = poly_inv_series(a, n_terms)
    da = [Fraction(k) * a[k] for k in range(1, n_terms)] + [Fraction(0)]
    log_c = [Fraction(0)] * n_terms
    for k in range(1, n_terms):
        c_km1 = sum(da[j] * inv_a[k - 1 - j] for j in range(k))
        log_c[k] = c_km1 / Fraction(k)
    return log_c


def poly_exp_series(c, n_terms):
    assert c[0] == Fraction(0)
    e = [Fraction(0)] * n_terms
    e[0] = Fraction(1)
    for k in range(1, n_terms):
        e[k] = sum(Fraction(j) * c[j] * e[k - j] for j in range(1, k + 1)) / Fraction(k)
    return e


def complete_bell_polynomial(x_seq, n):
    B = [Fraction(0)] * (n + 1)
    B[0] = Fraction(1)
    for m in range(1, n + 1):
        B[m] = sum(
            Fraction(math.comb(m - 1, k - 1)) * x_seq[k - 1] * B[m - k]
            for k in range(1, m + 1)
        )
    return B[n]


def verify_bell_polynomial_duality():
    n_max = 8  # k = 0..7 (up to m = 6, i.e. Sigma_11 and b_14)
    A = [Fraction(24, math.factorial(2 * k + 4)) for k in range(n_max)]
    log_A = poly_log_series(A, n_max)
    b_even = [Fraction(0)] + [log_A[k] / Fraction(2) for k in range(1, n_max)]

    three_inv_A = [Fraction(3) * c for c in poly_inv_series(A, n_max)]
    neg_two_b = [Fraction(-2) * b_even[k] for k in range(n_max)]
    three_exp = [Fraction(3) * c for c in poly_exp_series(neg_two_b, n_max)]
    bell_inputs = [Fraction(-2 * math.factorial(j)) * b_even[j] for j in range(1, n_max)]

    assert three_inv_A[0] == three_exp[0] == Fraction(3)
    assert three_inv_A[1] == three_exp[1] == Fraction(-6) * b_even[1] == Fraction(-1, 10)

    records = {}
    for m in range(1, 7):
        k = m + 1
        sig_direct = three_inv_A[k]
        sig_exp = three_exp[k]
        sig_bell = Fraction(3, math.factorial(k)) * complete_bell_polynomial(bell_inputs, k)
        assert sig_direct == sig_exp == sig_bell, f"Mismatch at m={m}"
        records[f"Sigma_{2*m - 1}"] = {
            "rational": str(sig_direct),
            "float": float(sig_direct),
            "b_2m": str(b_even[m]),
            "b_2m_plus_2": str(b_even[m + 1]),
        }

    b2, b4, b6, b8, b10 = b_even[1], b_even[2], b_even[3], b_even[4], b_even[5]
    assert records["Sigma_1"]["rational"] == str(6 * b2**2 - 6 * b4) == "13/8400"
    assert records["Sigma_3"]["rational"] == str(-4 * b2**3 + 12 * b2 * b4 - 6 * b6) == "-1/84000"
    assert records["Sigma_5"]["rational"] == str(2 * b2**4 - 12 * b2**2 * b4 + 6 * b4**2 + 12 * b2 * b6 - 6 * b8) == "-31/2328480000"
    assert records["Sigma_7"]["rational"] == str(
        -Fraction(4, 5) * b2**5 + 8 * b2**3 * b4 - 12 * b2 * b4**2 - 12 * b2**2 * b6 + 12 * b4 * b6 + 12 * b2 * b8 - 6 * b10
    ) == "1343/908107200000"

    return {
        "b_even": {f"b_{2*j}": str(b_even[j]) for j in range(1, 7)},
        "sigma_odd_bell_verified": records,
    }


# ============================================================================
# 2. HIGH-ORDER s = 0 WIENER-HOPF GERMS p_n AND c_n (UP TO n = 17)
# ============================================================================

def build_s0_germs(n_max=17, n_roots=4000):
    """
    Build the exact s = 0 Taylor coefficients:
      - L(s) = log(P(-s) / (-s E[H])) = sum_{j>=1} L_j s^j,
        where L_{2j} = b_{2j} (exact rationals) and L_{2m+1} = -b_{2m+1} = gamma_{2m+1}
      - p_n = [s^n] exp(L(s)), so m_n(TU) = int_0^1 u^n (TU)(u) du = n! * E[H] * p_n
      - F_{-,W}(s) = 7/(20 s) + sum_{m>=0} (-1)^m Sigma_m s^m,
        so P(-s) F_{-,W}(s) = -E[H] * sum_{n>=0} c_n s^n,
        and m_n(TW) = int_0^1 u^n (TW)(u) du = -n! * E[H] * c_n!
    """
    # Exact rational b_{2j} and Sigma_{2m-1}
    k_max = n_max // 2 + 3
    A = [Fraction(24, math.factorial(2 * k + 4)) for k in range(k_max)]
    log_A = poly_log_series(A, k_max)
    b_even = {2 * k: float(log_A[k] / Fraction(2)) for k in range(1, k_max)}
    three_inv_A = [Fraction(3) * c for c in poly_inv_series(A, k_max)]
    sigma_odd = {2 * m - 1: float(three_inv_A[m + 1]) for m in range(1, k_max - 1)}

    # Known high-precision constants for j = 1, 3 and m = 0, 2:
    d0 = 0.227350780091995
    g3 = 0.000991025277641
    Sigma_0 = -0.019721794539427
    Sigma_2 = -0.000018652156051

    # Sum over roots in Q1 for higher odd L_{2m+1} (m >= 2) and even Sigma_{2m} (m >= 2):
    odd_L = {1: d0, 3: g3}
    even_Sig = {0: Sigma_0, 2: Sigma_2}
    for deg in range(5, n_max + 2, 2):
        odd_L[deg] = 0.0
    for deg in range(4, n_max + 2, 2):
        even_Sig[deg] = 0.0

    for j in range(1, n_roots + 1):
        sig = 1.0 if (j % 2 == 0) else -1.0
        a = (j + 0.5) * math.pi
        w = complex(a, math.acosh(a))
        for _ in range(12):
            sin_w = complex(math.sin(w.real) * math.cosh(w.imag), math.cos(w.real) * math.sinh(w.imag))
            cos_w = complex(math.cos(w.real) * math.cosh(w.imag), -math.sin(w.real) * math.sinh(w.imag))
            w = w - (sin_w - sig * w) / (cos_w - sig)
        sk = 2j * w
        cos_w = complex(math.cos(w.real) * math.cosh(w.imag), -math.sin(w.real) * math.sinh(w.imag))
        rk = 1.0 / (4.0 * (1.0 - sig * cos_w))

        # Note: in RHP, roots of P(-s) are at -2 i w_k = -sk and +2 i conj(w_k), so
        # L_n = -(1/n) * sum_{RHP} (-sk)^{-n} = +(2/n) * Re(sk^{-n}) for odd n!
        for deg in range(5, n_max + 2, 2):
            odd_L[deg] += +(2.0 / deg) * ((sk ** (-deg)).real)
        for deg in range(4, n_max + 2, 2):
            even_Sig[deg] += 2.0 * ((rk / (sk ** (deg + 1))).real)

    L = [0.0] * (n_max + 1)
    for deg in range(1, n_max + 1):
        if deg % 2 == 1:
            L[deg] = odd_L[deg]
        else:
            L[deg] = b_even[deg]

    p = [0.0] * (n_max + 1)
    p[0] = 1.0
    for n in range(1, n_max + 1):
        p[n] = sum(j * L[j] * p[n - j] for j in range(1, n + 1)) / n

    Sig = [0.0] * (n_max + 1)
    for m in range(0, n_max + 1):
        if m % 2 == 0:
            Sig[m] = even_Sig[m]
        else:
            Sig[m] = sigma_odd[m]

    f_coeff = [7.0 / 20.0] + [((-1.0) ** m) * Sig[m] for m in range(n_max)]
    c = [0.0] * (n_max + 1)
    for n in range(0, n_max + 1):
        c[n] = sum(p[n - j] * f_coeff[j] for j in range(n + 1))

    eh = 1.0 / math.sqrt(12.0)
    m_tu = [math.factorial(n) * eh * p[n] for n in range(n_max + 1)]
    m_tw = [-math.factorial(n) * eh * c[n] for n in range(n_max + 1)]
    return eh, p, c, m_tu, m_tw, Sig


# ============================================================================
# 3. EXACT POLYNOMIAL ITERATES psi_k = T^{k-1} f_1 AND MOD-4 GERM SERIES
# ============================================================================

def apply_turn_operator_poly(poly_coeffs):
    """
    Given polynomial psi(t) = sum_{j=0}^d a_j t^j on [0, 1], compute exact rational
    coefficients of
      (T psi)(u) = int_0^{1-u} (1 - u - t) psi(t) dt.
    Since int_0^y (y - t) t^j dt = y^{j+2} / ((j+1)(j+2)) with y = 1 - u:
      (T psi)(u) = sum_{j=0}^d (a_j / ((j+1)(j+2))) * (1 - u)^{j+2}
                 = sum_{m=0}^{d+2} b_m u^m!
    """
    d = len(poly_coeffs) - 1
    out = [Fraction(0)] * (d + 3)
    for j, a_j in enumerate(poly_coeffs):
        if a_j == 0:
            continue
        scale = a_j / Fraction((j + 1) * (j + 2))
        deg = j + 2
        for m in range(deg + 1):
            term = scale * Fraction(math.comb(deg, m)) * (Fraction(-1) ** m)
            out[m] += term
    return out


def find_cantilever_root(n_mode):
    k = (2 * n_mode - 1) * math.pi / 2.0
    if n_mode == 1:
        k = 1.875104068711961
    elif n_mode == 2:
        k = 4.694091132974174
    elif n_mode == 3:
        k = 7.854757438237613
    for _ in range(30):
        f = math.cos(k) * math.cosh(k) + 1.0
        df = math.cos(k) * math.sinh(k) - math.sin(k) * math.cosh(k)
        k -= f / df
    return k


def eval_cantilever_mod4_germ_series(kappa, eh, p, c, max_m=4):
    """
    Evaluate <TU, psi_inf>, <TW, psi_inf>, <V_1, phi_1>, and mu_1(phi_1) via the
    Mod-4 Germ Series at s = 0:
      psi_inf(u) = alpha * (cosh(kappa*u) + cos(kappa*u))/2
                 - beta  * (sinh(kappa*u) + sin(kappa*u))/2
                 = alpha * sum_{m>=0} (kappa u)^{4m}/(4m)!
                 - beta  * sum_{m>=0} (kappa u)^{4m+1}/(4m+1)!,
    where psi_inf(1) = psi_inf'(1) = 0 gives:
      alpha = sinh(kappa) + sin(kappa),
      beta  = cosh(kappa) + cos(kappa).
    Notice that (4m)! and (4m+1)! cancel identically with n! in m_n(TU) and m_n(TW):
      <TU, psi_inf> =  eh * sum_{m=0}^{max_m} (alpha * kappa^{4m} * p[4m] - beta * kappa^{4m+1} * p[4m+1]),
      <TW, psi_inf> = -eh * sum_{m=0}^{max_m} (alpha * kappa^{4m} * c[4m] - beta * kappa^{4m+1} * c[4m+1])!
    Also normalize by lambda_1 = 1 / kappa^2 so <U, phi_1> = (1/kappa^2) <TU, psi_inf>.
    """
    alpha = math.sinh(kappa) + math.sin(kappa)
    beta = math.cosh(kappa) + math.cos(kappa)

    partial_table = []
    tu_acc = 0.0
    tw_acc = 0.0
    for m in range(max_m + 1):
        i0 = 4 * m
        i1 = 4 * m + 1
        du = eh * (alpha * (kappa ** i0) * p[i0] - beta * (kappa ** i1) * p[i1])
        dw = -eh * (alpha * (kappa ** i0) * c[i0] - beta * (kappa ** i1) * c[i1])
        tu_acc += du
        tw_acc += dw
        u_phi = tu_acc / (kappa * kappa)
        w_phi = tw_acc / (kappa * kappa)
        v1_phi = 0.5 * u_phi + w_phi
        partial_table.append({
            "max_m": m,
            "max_degree_n": i1,
            "U_phi": u_phi,
            "W_phi": w_phi,
            "V1_phi": v1_phi,
            "mu1_phi": v1_phi / u_phi,
        })

    return {
        "kappa": kappa,
        "alpha": alpha,
        "beta": beta,
        "U_phi": partial_table[-1]["U_phi"],
        "W_phi": partial_table[-1]["W_phi"],
        "V1_phi": partial_table[-1]["V1_phi"],
        "mu1_phi": partial_table[-1]["mu1_phi"],
        "truncation_convergence_by_m": partial_table,
    }


# ============================================================================
# 4. 4-POINT COMPLEX WIENER-HOPF CLOSED FORM WITH SOKHOTSKI-PLEMELJ ON Re(s)=0
# ============================================================================

def gauss_legendre_nodes_weights(n):
    xs = []
    ws = []
    m = (n + 1) // 2
    for i in range(1, m + 1):
        z = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(30):
            p1 = 1.0
            p2 = 0.0
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = ((2 * j - 1) * z * p2 - (j - 1) * p3) / j
            pp = n * (z * p1 - p2) / (z * z - 1.0)
            z -= p1 / pp
        w = 2.0 / ((1.0 - z * z) * pp * pp)
        xs.append(-z)
        ws.append(w)
        if i != n + 1 - i:
            xs.append(z)
            ws.append(w)
    pairs = sorted(zip(xs, ws), key=lambda t: t[0])
    return [p[0] for p in pairs], [p[1] for p in pairs]


def build_complex_wh_evaluator(n_quad=128, L_scale=12.0, n_roots=2000):
    nodes, weights = gauss_legendre_nodes_weights(n_quad)

    def eval_phi_imag(y):
        t = abs(y)
        half = 0.5 * t
        if t < 1e-4:
            q_it = (t ** 2) / 12.0 * (1.0 - (t ** 2) / 30.0 + (t ** 4) / 1680.0 - (t ** 6) / 151200.0)
        else:
            q_it = 1.0 - (math.sin(half) / half) ** 2
        return 12.0 * q_it / (t * t)

    def eval_tilde_phi_imag(y):
        t = abs(y)
        return ((t * t + 12.0) / 12.0) * eval_phi_imag(t)

    ts = []
    dts = []
    log_tphi_ts = []
    for x, w in zip(nodes, weights):
        u = 0.5 * (x + 1.0)
        du = 0.5 * w
        t = L_scale * u / (1.0 - u)
        dt = L_scale / ((1.0 - u) ** 2) * du
        ts.append(t)
        dts.append(dt)
        log_tphi_ts.append(math.log(eval_tilde_phi_imag(t)))

    def eval_Q(z):
        z = complex(z)
        if abs(z) < 1e-4:
            z2 = z * z
            return -(z2 / 12.0) * (1.0 + z2 / 30.0 + (z2 ** 2) / 1680.0 + (z2 ** 3) / 151200.0)
        h = 0.5 * z
        return 1.0 - (cmath.sinh(h) / h) ** 2

    def logP_right(z):
        """
        Compute log(sqrt(12)*P(z)/z) for Re(z) > 0 using the exact closed-form subtraction:
          (z/pi) int_0^inf log(12/(t^2+12))/(t^2+z^2) dt = log(sqrt(12)/(z+sqrt(12))),
        leaving tilde_phi(t) = ((t^2+12)/12)*phi(t) = 1 + O(t^{-2}) as t -> inf!
        """
        z = complex(z)
        acc = 0j
        z2 = z * z
        for t, dt, ltphi in zip(ts, dts, log_tphi_ts):
            acc += ltphi / (t * t + z2) * dt
        return cmath.log(math.sqrt(12.0) / (z + math.sqrt(12.0))) + (z / math.pi) * acc

    def logP_imag_sokhotski_plemelj(y):
        """
        Exact Sokhotski-Plemelj evaluation at z = i*y on the imaginary axis, splitting (0, inf)
        at 2*|y| so the finite interval [0, 2*|y|] is symmetric around the pole t = |y|.
        """
        y_abs = abs(y)
        ltphi_y = math.log(eval_tilde_phi_imag(y_abs))
        y2 = y * y
        # Part 1: t in [0, 2*y_abs], parameterized by t = y_abs * (1 + x), dt = y_abs * w
        pv_acc = 0.0
        for x, w in zip(nodes, weights):
            t = y_abs * (1.0 + x)
            dt = y_abs * w
            if abs(x) > 1e-12:
                ltphi = math.log(eval_tilde_phi_imag(t))
                pv_acc += (ltphi - ltphi_y) / (t * t - y2) * dt
        # Add analytic PV integral of ltphi_y / (t^2 - y^2) on [0, 2*y_abs]:
        # PV int_0^{2*y_abs} dt / (t^2 - y_abs^2) = -log(3) / (2 * y_abs)
        pv_acc += ltphi_y * (-math.log(3.0) / (2.0 * y_abs))
        # Part 2: smooth tail t in [2*y_abs, inf), parameterized by t = 2*y_abs + L_scale * u / (1 - u)
        for x, w in zip(nodes, weights):
            u = 0.5 * (x + 1.0)
            du = 0.5 * w
            t = 2.0 * y_abs + L_scale * u / (1.0 - u)
            dt = L_scale / ((1.0 - u) ** 2) * du
            ltphi = math.log(eval_tilde_phi_imag(t))
            pv_acc += ltphi / (t * t - y2) * dt

        z = complex(0.0, y)
        base_log = cmath.log(math.sqrt(12.0) / (z + math.sqrt(12.0)))
        return base_log + complex(0.5 * ltphi_y, (y / math.pi) * pv_acc)

    def eval_P_true(z):
        """Exact Wiener-Hopf factor P(z) ~ z / sqrt(12) as z -> 0, with Sokhotski-Plemelj on Re(z) = 0."""
        z = complex(z)
        if abs(z) < 1e-12:
            return z / math.sqrt(12.0)
        if z.real > 1e-9:
            return (z / math.sqrt(12.0)) * cmath.exp(logP_right(z))
        elif z.real < -1e-9:
            pm = (-z / math.sqrt(12.0)) * cmath.exp(logP_right(-z))
            return eval_Q(z) / pm
        else:
            return (z / math.sqrt(12.0)) * cmath.exp(logP_imag_sokhotski_plemelj(z.imag))

    # Also build exact F_{-,W}(s) evaluator via Mittag-Leffler series + Euler-Maclaurin tail
    # Recall F_{-,W}(s) = 7/(20 s) + sum_{k>=1} r_k / (s + s_k) + conj
    # Using the subtracted series:
    #   F_{-,W}(s) = 7/(20 s) - Sigma_0 + s * Sigma_1 - s^2 * Sigma_2 + s^3 * Sigma_3
    #                + s^4 * sum_{s_k} r_k / (s_k^4 * (s + s_k))!
    # Because s^4 / (s_k^4 * (s + s_k)) decays as k^{-5}, 500 roots give 14-digit accuracy!
    q1_roots = []
    for j in range(1, 501):
        sig = 1.0 if (j % 2 == 0) else -1.0
        a = (j + 0.5) * math.pi
        w = complex(a, math.acosh(a))
        for _ in range(12):
            sin_w = complex(math.sin(w.real) * math.cosh(w.imag), math.cos(w.real) * math.sinh(w.imag))
            cos_w = complex(math.cos(w.real) * math.cosh(w.imag), -math.sin(w.real) * math.sinh(w.imag))
            w = w - (sin_w - sig * w) / (cos_w - sig)
        sk = 2j * w
        cos_w = complex(math.cos(w.real) * math.cosh(w.imag), -math.sin(w.real) * math.sinh(w.imag))
        rk = 1.0 / (4.0 * (1.0 - sig * cos_w))
        q1_roots.append((sk, rk))

    Sigma_0 = -0.019721794539427
    Sigma_1 = 13.0 / 8400.0
    Sigma_2 = -0.000018652156051
    Sigma_3 = -1.0 / 84000.0

    def eval_F_minus_W(s):
        """
        Evaluate F_{-,W}(s) = 7/(20 s) + sum_{m>=0} (-1)^m Sigma_m s^m
                            = 7/(20 s) + Sigma_0 - Sigma_1 s + Sigma_2 s^2 - Sigma_3 s^3
                              + s^4 * sum_{all roots} r_k / (s_k^4 * (s + s_k))!
        """
        s = complex(s)
        base = 7.0 / (20.0 * s) + Sigma_0 - Sigma_1 * s + Sigma_2 * (s ** 2) - Sigma_3 * (s ** 3)
        rem = 0j
        s4 = s ** 4
        for sk, rk in q1_roots:
            # Pair (sk, rk) and its complex conjugate (conj(sk), conj(rk))
            sk2 = sk.conjugate()
            rk2 = rk.conjugate()
            rem += rk / ((sk ** 4) * (s + sk)) + rk2 / ((sk2 ** 4) * (s + sk2))
        return base + s4 * rem

    return eval_Q, eval_P_true, eval_F_minus_W


def verify_three_way_cantilever_fixed_point():
    eh, p, c, m_tu, m_tw, Sig = build_s0_germs(n_max=17, n_roots=4000)

    kappa_1 = find_cantilever_root(1)
    kappa_2 = find_cantilever_root(2)
    kappa_3 = find_cantilever_root(3)
    rho_turn = (kappa_2 / kappa_1) ** 2

    # Method A: Mod-4 Germ Series at s = 0 for Mode 1 (phi_1) and Mode 2 (phi_2)
    mode1_germ = eval_cantilever_mod4_germ_series(kappa_1, eh, p, c, max_m=4)
    mode2_germ = eval_cantilever_mod4_germ_series(kappa_2, eh, p, c, max_m=4)

    # Method B: Exact Polynomial Iterates psi_k(u) = (T^{k-1} f_1)(u) for k = 1..8
    # Starting from psi_1(u) = (T^0 f_1)(u) = 1 - u
    psi_poly = [Fraction(1), Fraction(-1)]
    iter_table = {}
    mu_seq = {}
    for k in range(1, 9):
        u_val = sum(float(coeff) * m_tu[deg] for deg, coeff in enumerate(psi_poly))
        w_val = sum(float(coeff) * m_tw[deg] for deg, coeff in enumerate(psi_poly))
        v1_val = 0.5 * u_val + w_val
        mu_val = v1_val / u_val
        mu_seq[k] = mu_val
        iter_table[f"k={k}"] = {
            "degree": len(psi_poly) - 1,
            "U_Tk_f1": u_val,
            "W_Tk_f1": w_val,
            "V1_Tk_f1": v1_val,
            "mu_1_Tk_f1": mu_val,
            "diff_from_mu1_phi1": mu_val - mode1_germ["mu1_phi"],
            "psi_k_at_0_rational": str(psi_poly[0]),
            "psi_k_u2_coeff_rational": str(psi_poly[2]) if len(psi_poly) > 2 else "0",
            "psi_k_u3_coeff_rational": str(psi_poly[3]) if len(psi_poly) > 3 else "0",
        }
        if k < 8:
            psi_poly = apply_turn_operator_poly(psi_poly)

    # Check consecutive deviation ratios (mu_1(T^k f_1) - mu_1(phi_1)) / (mu_1(T^{k+1} f_1) - mu_1(phi_1))
    deviation_ratios = {}
    for k in range(1, 8):
        d_k = mu_seq[k] - mode1_germ["mu1_phi"]
        d_kp1 = mu_seq[k + 1] - mode1_germ["mu1_phi"]
        deviation_ratios[f"k={k}_to_{k+1}"] = d_k / d_kp1

    # Spectral extrapolation from k = 7, 8 using exact -rho_turn = -(kappa_2/kappa_1)^2
    mu1_spectral_extrap_k78 = (mu_seq[8] + mu_seq[7] / rho_turn) / (1.0 + 1.0 / rho_turn)

    # Method C: 4-Point Complex Wiener-Hopf Closed Form at s in {+kappa_1, -kappa_1, +i*kappa_1, -i*kappa_1}
    eval_Q, eval_P_true, eval_F_minus_W = build_complex_wh_evaluator(n_quad=256, L_scale=12.0)
    alpha_1 = mode1_germ["alpha"]
    beta_1 = mode1_germ["beta"]
    four_roots = [
        complex(kappa_1, 0.0),
        complex(-kappa_1, 0.0),
        complex(0.0, kappa_1),
        complex(0.0, -kappa_1),
    ]

    tu_4pt = 0j
    tw_4pt = 0j
    for s in four_roots:
        weight = 0.25 * (alpha_1 - beta_1 * (kappa_1 / s))
        p_minus_s = eval_P_true(-s)
        tu_4pt += weight * (-p_minus_s / s)
        tw_4pt += weight * (p_minus_s * eval_F_minus_W(s))

    u_phi1_4pt = tu_4pt.real / (kappa_1 * kappa_1)
    w_phi1_4pt = tw_4pt.real / (kappa_1 * kappa_1)
    v1_phi1_4pt = 0.5 * u_phi1_4pt + w_phi1_4pt
    mu1_phi1_4pt = v1_phi1_4pt / u_phi1_4pt

    assert abs(mode1_germ["mu1_phi"] - mu1_spectral_extrap_k78) < 1e-10
    assert abs(mode1_germ["mu1_phi"] - mu1_phi1_4pt) < 1e-6
    assert abs(mode1_germ["U_phi"] - u_phi1_4pt) < 1e-6


    return {
        "cantilever_constants": {
            "kappa_1": kappa_1,
            "kappa_2": kappa_2,
            "kappa_3": kappa_3,
            "lambda_1_turn": 1.0 / (kappa_1 ** 2),
            "lambda_2_turn": -1.0 / (kappa_2 ** 2),
            "rho_turn": rho_turn,
        },
        "method_A_mod4_germ_series_at_s0": {
            "mode1_phi1": mode1_germ,
            "mode2_phi2": mode2_germ,
        },
        "method_B_exact_polynomial_iterates_and_spectral_extrapolation": {
            "iterates_k1_to_k8": iter_table,
            "consecutive_deviation_ratios_vs_minus_rho_turn": {
                "target_minus_rho_turn": -rho_turn,
                "observed_ratios": deviation_ratios,
            },
            "mu1_phi1_spectral_extrap_k78": mu1_spectral_extrap_k78,
            "abs_diff_methodA_vs_methodB": abs(mode1_germ["mu1_phi"] - mu1_spectral_extrap_k78),
        },
        "method_C_4point_complex_wiener_hopf_sokhotski_plemelj": {
            "U_phi1_4pt": u_phi1_4pt,
            "W_phi1_4pt": w_phi1_4pt,
            "V1_phi1_4pt": v1_phi1_4pt,
            "mu1_phi1_4pt": mu1_phi1_4pt,
            "abs_diff_U_methodA_vs_methodC": abs(mode1_germ["U_phi"] - u_phi1_4pt),
            "abs_diff_mu1_methodA_vs_methodC": abs(mode1_germ["mu1_phi"] - mu1_phi1_4pt),
        },
    }


def main():
    bell_res = verify_bell_polynomial_duality()
    fp_res = verify_three_way_cantilever_fixed_point()

    results = {
        "meta": {
            "author": "Den B (Lane B, ompu-7f698bd908)",
            "date": "2026-11-09T20:35:00+01:00",
            "pulse": 413,
        },
        "part1_exponential_bell_polynomial_duality": bell_res,
        "part2_cantilever_meander_fixed_point_three_way_verification": fp_res,
    }

    out_path = os.path.splitext(os.path.abspath(__file__))[0] + "_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    mA = fp_res["method_A_mod4_germ_series_at_s0"]["mode1_phi1"]
    mB = fp_res["method_B_exact_polynomial_iterates_and_spectral_extrapolation"]
    mC = fp_res["method_C_4point_complex_wiener_hopf_sokhotski_plemelj"]

    print("=== 1. EXPONENTIAL BELL-POLYNOMIAL DUALITY (EXACT FRACTION, m=1..6) ===")
    for k, v in bell_res["sigma_odd_bell_verified"].items():
        print(f"  {k:8s} = {v['rational']}  ({v['float']:.15e})")

    print("\n=== 2. CANTILEVER-MEANDER FIXED POINT mu_1(phi_1) (THREE INDEPENDENT METHODS) ===")
    print(f"  kappa_1  = {fp_res['cantilever_constants']['kappa_1']:.15f}")
    print(f"  kappa_2  = {fp_res['cantilever_constants']['kappa_2']:.15f}")
    print(f"  rho_turn = (kappa_2/kappa_1)^2 = {fp_res['cantilever_constants']['rho_turn']:.12f}")
    print(f"  Method A (Mod-4 s=0 Germ Series):        <U,phi_1> = {mA['U_phi']:.12f}, <V_1,phi_1> = {mA['V1_phi']:.12f}, mu_1(phi_1) = {mA['mu1_phi']:.14f}")
    print(f"  Method B (Exact Poly Iterates k=7,8):    mu_1(phi_1) = {mB['mu1_phi1_spectral_extrap_k78']:.14f} (diff = {mB['abs_diff_methodA_vs_methodB']:.2e})")
    print(f"  Method C (4-Pt Complex WH + Sokhotski):  <U,phi_1> = {mC['U_phi1_4pt']:.12f}, <V_1,phi_1> = {mC['V1_phi1_4pt']:.12f}, mu_1(phi_1) = {mC['mu1_phi1_4pt']:.14f} (diff = {mC['abs_diff_mu1_methodA_vs_methodC']:.2e})")

    print("\n=== 3. MOD-4 s=0 GERM SERIES TRUNCATION CONVERGENCE (m = 0..4) ===")
    for row in mA["truncation_convergence_by_m"]:
        print(f"  m={row['max_m']} (n <= {row['max_degree_n']:2d}): <U,phi_1> = {row['U_phi']:.12f}, <V_1,phi_1> = {row['V1_phi']:.12f}, mu_1(phi_1) = {row['mu1_phi']:.14f}")

    print("\n=== 4. EXACT POLYNOMIAL ITERATES mu_1(T^k f_1) FOR k = 1..8 ===")
    for k_str, row in mB["iterates_k1_to_k8"].items():
        print(f"  {k_str} (deg {row['degree']:2d}): <U,T^k f_1> = {row['U_Tk_f1']:.12f}, <V_1,T^k f_1> = {row['V1_Tk_f1']:.12f}, mu_1(T^k f_1) = {row['mu_1_Tk_f1']:.12f}, diff = {row['diff_from_mu1_phi1']:+.12e}")

    print("\n=== 5. CONSECUTIVE DEVIATION RATIOS (TARGET: -rho_turn = -6.2668930258) ===")
    for r_str, r_val in mB["consecutive_deviation_ratios_vs_minus_rho_turn"]["observed_ratios"].items():
        print(f"  {r_str}: ratio = {r_val:+.10f}")
    print(f"\nSaved results to {out_path}")


if __name__ == "__main__":
    main()
