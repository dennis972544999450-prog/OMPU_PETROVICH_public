#!/usr/bin/env python3
"""
Single-Term Closed-Form Coefficients for All-Order Syzygies & Edge-to-Bulk Defect Duality (COKER-0003)
======================================================================================================
Date: 2026-11-15 (Sunday Evening Pass, 20:30 CET, Continuity Rev 102)
Author: Jee A (ompu-d6a8af238c, Lane A), extending Den B (seq 240, 1794736594),
        Cloud Jee & Jee-AGY (READ-0087..0089, 1794756477 / 1794769918),
        Petrovich (1794757250), and Φ-Hausmaster (1794757443 / 1794769990).

Summary of Exact Results Verified Here (Pure Python `fractions.Fraction` + `math`, `python3 -I -B`):
1. Theorem 1 (Single-Term Closed-Form Coefficients for Q_{4K}(x) and P_{4K+1}(x) at Arbitrary K >= 1):
   In Petrovich's Gaussian barycentric coordinate w(x) = x + i(1 - x), observe the exact algebraic
   factorization around x = 0:
       w(x) = i * (1 - (1 + i)*x).
   Since i^(4K) = +1 for every K >= 1, raising w(x) to power 4K eliminates i^(4K) completely:
       w(x)^(4K) = (1 - (1 + i)*x)^(4K) = sum_{j=0}^{4K} C(4K, j) (-1)^j (1 + i)^j x^j.
   Combining this with (2x - 1)^(4K) = (1 - 2x)^(4K) = sum_{j=0}^{4K} C(4K, j) (-1)^j 2^j x^j
   yields a SINGLE-TERM (nested-sum-free, matrix-inversion-free!) closed-form formula for every
   coefficient of the monic beam-orthogonal polynomial Q_{4K}(x) = sum_{j=0}^{4K} q_{K,j} x^j:
       q_{K,0} = K / ((4K + 1) * 2^(4K - 2)),
       q_{K,j} = (-1)^j * C(4K, j) * 2^(-(4K - j)) * [ 1 + 2^(-j - 1) * Im[(1 + i)^j] ]   (1 <= j <= 4K),
   and, via (1/4) P'_{4K+1}(x) = Q_{4K}(x) with P_{4K+1}(0) = 0, a single-term closed-form formula
   for every coefficient of Cloud Jee's boundary-pinned polynomial P_{4K+1}(x) = sum_{j=1}^{4K+1} p_{K,j} x^j:
       p_{K,1}   = K / ((4K + 1) * 2^(4K - 4)),
       p_{K,j+1} = (4 / (j + 1)) * (-1)^j * C(4K, j) * 2^(-(4K - j)) * [ 1 + 2^(-j - 1) * Im[(1 + i)^j] ].
   This closes Den B's open seam (seq 240) across all orders K >= 1 in closed binomial form.

2. Theorem 2 (Explicit Central-Moment Syzygy Formula & Canonical Triangular Elimination at u = x - 1/4):
   In the barycenter coordinate u = x - 1/4 (where 2x - 1 = 2u - 1/2), every primary syzygy polynomial
   S_{4K+1}(u) := 2^(-(4K+1)) Q_K(2u - 1/2) - c_{K,1} u = sum_{j=0}^{4K+1} c_{K,j} u^j (with c_{K,1} = 0)
   has the explicit closed-form coefficient formula for all j != 1:
       c_{K,j} = C(4K + 1, j) * 2^(-(4K + 1 - j)) * [ (-1/2)^(4K + 1 - j)
                 + ((-1)^K / (2 * 4^K)) * Im[(-1/2 + i)^(4K + 1 - j)] ].
   Since S_{4K+1}(u) is monic of degree 4K + 1, triangular elimination in steps of 4:
       S^{red}_{4K+1}(u) := S_{4K+1}(u) - sum_{m=1}^{K-1} L_{K,m} S^{red}_{4m+1}(u)
   eliminates all intermediate (4m + 1)-th central moments mu_{4m+1,cent} (1 <= m < K), recovering
   the exact K = 1 (p = 5) and Den B's K = 2 (p = 9) reduced syzygies and extending them to K = 3, 4 (p = 13, 17).

3. Theorem 3 (Quantitative Edge-to-Bulk Defect Duality for Cloud Jee's COKER-0003):
   Subtracting the boundary Bernoulli(1/4) expectation (3/4)P(0) + (1/4)P(1) = P(0) + (1/4)*int_0^1 P'(x) dx
   from Cloud Jee's finite-r IBP identity int_0^1 P(x) rho_hat_r(x) dx = P(0) + (1/4)*int_0^1 P'(x) psi_hat_r(x)^2 dx
   yields the universal Edge-to-Bulk Defect Duality Identity for every polynomial P(x) and every mode r >= 1:
       int_0^1 P(x) rho_hat_r(x) dx - [ (3/4)*P(0) + (1/4)*P(1) ]
           = (1/4) * int_0^1 P'(x) * (psi_hat_r(x)^2 - 1) dx.
   Consequently:
   (a) Edge concentration (rho_hat_r -> (3/4) delta_0 + (1/4) delta_1) and bulk equidistribution
       (psi_hat_r^2 -> Unif([0, 1])) are exact quarter-derivative transposes of one another;
   (b) On the syzygy subspace P in span{P_{4K+1}}_{K>=1}, both the boundary term (3/4)P(0) + (1/4)P(1)
       and the bulk defect (1/4)*int_0^1 P'(x)(psi_hat_r^2 - 1) dx vanish identically at EVERY finite r >= 1;
   (c) For P(x) = x^p (p = 1, 2, 3, 4), the exact mode-r edge-concentration defect equals (p/4) times
       the (p-1)-th bulk equidistribution defect under the exact staircase-to-beam dictionary
       (I_0^{(2n+2)}/m_0^{(2n)}, H_0^{(2n+3)}/m_0^{(2n)}, m_0^{(2n+2)}/m_0^{(2n)}) <-> (t_r^2/kappa_r^2, t_r/kappa_r^3, 1/kappa_r^4):
       0 (p=1), -t_r^2/kappa_r^2 (p=2), -15*t_r^2/(8*kappa_r^2) + 3*t_r/(4*kappa_r^3) (p=3),
       and -15*t_r^2/(4*kappa_r^2) + 15*t_r/(2*kappa_r^3) - 6/kappa_r^4 (p=4).
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path


def gauss_pow_int(re: int, im: int, e: int) -> tuple[int, int]:
    """Exact Gaussian integer power (re + i*im)^e."""
    rr, ri = 1, 0
    br, bi = re, im
    while e > 0:
        if e & 1:
            rr, ri = rr * br - ri * bi, rr * bi + ri * br
        br, bi = br * br - bi * bi, 2 * br * bi
        e >>= 1
    return rr, ri


def gauss_pow_frac(re: Fraction, im: Fraction, e: int) -> tuple[Fraction, Fraction]:
    """Exact Gaussian rational power (re + i*im)^e."""
    rr, ri = Fraction(1), Fraction(0)
    br, bi = Fraction(re), Fraction(im)
    while e > 0:
        if e & 1:
            rr, ri = rr * br - ri * bi, rr * bi + ri * br
        br, bi = br * br - bi * bi, 2 * br * bi
        e >>= 1
    return rr, ri


def single_term_Q_4K_coeffs(K: int) -> list[Fraction]:
    """
    Theorem 1: Single-term closed-form coefficients of monic Q_{4K}(x) = sum_{j=0}^{4K} q_{K,j} x^j
    without any nested sum or polynomial multiplication.
    """
    deg = 4 * K
    coeffs: list[Fraction] = [Fraction(0)] * (deg + 1)
    coeffs[0] = Fraction(K, (4 * K + 1) * (2 ** (4 * K - 2)))
    for j in range(1, deg + 1):
        _, im_1_plus_i_j = gauss_pow_int(1, 1, j)
        sign = -1 if (j & 1) else 1
        binom = math.comb(deg, j)
        scale = Fraction(sign * binom, 2 ** (deg - j))
        bracket = Fraction(1) + Fraction(im_1_plus_i_j, 2 ** (j + 1))
        coeffs[j] = scale * bracket
    return coeffs


def single_term_P_4K_plus_1_coeffs(K: int) -> list[Fraction]:
    """
    Theorem 1: Single-term closed-form coefficients of Cloud Jee's boundary-pinned
    P_{4K+1}(x) = sum_{j=1}^{4K+1} p_{K,j} x^j without any nested sum.
    """
    q_coeffs = single_term_Q_4K_coeffs(K)
    p_coeffs = [Fraction(0)] * (4 * K + 2)
    for j, q_j in enumerate(q_coeffs):
        p_coeffs[j + 1] = Fraction(4, j + 1) * q_j
    return p_coeffs


def single_term_central_S_coeffs(K: int) -> list[Fraction]:
    """
    Theorem 2: Closed-form coefficients of primary central-moment syzygy polynomial
    S_{4K+1}(u) = sum_{j=0}^{4K+1} c_{K,j} u^j (u = x - 1/4, with linear chord removed so c_{K,1} = 0).
    """
    deg = 4 * K + 1
    coeffs = [Fraction(0)] * (deg + 1)
    pref = Fraction((-1) ** K, 2 * (4 ** K))
    for j in range(deg + 1):
        if j == 1:
            coeffs[j] = Fraction(0)
            continue
        r = deg - j
        _, im_part = gauss_pow_frac(Fraction(-1, 2), Fraction(1, 1), r)
        binom_scale = Fraction(math.comb(deg, j), 2 ** r)
        bracket = (Fraction(-1, 2) ** r) + pref * im_part
        coeffs[j] = binom_scale * bracket
    return coeffs


def build_reduced_central_syzygy_hierarchy(K_max: int) -> dict[int, list[Fraction]]:
    """
    Theorem 2: Canonical triangular elimination of S_{4K+1}(u) in steps of 4,
    producing S^{red}_{4K+1}(u) in which the coefficients of u^1 and u^{4m+1} (1 <= m < K) all vanish.
    """
    red: dict[int, list[Fraction]] = {}
    for K in range(1, K_max + 1):
        cur = single_term_central_S_coeffs(K)
        for m in range(1, K):
            deg_m = 4 * m + 1
            factor = cur[deg_m]
            if factor != 0:
                prev = red[m]
                for idx in range(len(prev)):
                    cur[idx] -= factor * prev[idx]
        red[K] = cur
    return red


def poly_eval_frac(a: list[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    for c in reversed(a):
        acc = acc * x + c
    return acc


def apply_turn_T(poly: list[Fraction]) -> list[Fraction]:
    """Exact polynomial action (Tf)(x) = int_0^{1-x} (1 - x - t) f(t) dt."""
    out = [Fraction(0)] * (len(poly) + 2)
    for i, coeff in enumerate(poly):
        if coeff == 0:
            continue
        deg_u = i + 2
        scale = coeff / Fraction((i + 1) * (i + 2))
        for r in range(deg_u + 1):
            out[r] += scale * math.comb(deg_u, r) * ((-1) ** r)
    return out


def solve_beam_kappa(r: int) -> float:
    kap = (r - 0.5) * math.pi
    if r == 1:
        kap = 1.8751040687119611
    elif r == 2:
        kap = 4.6940911329741745
    for _ in range(30):
        em = math.exp(-kap)
        sech_k = 2.0 * em / (1.0 + em * em)
        tanh_k = (1.0 - em * em) / (1.0 + em * em)
        f = math.cos(kap) + sech_k
        fp = -math.sin(kap) - tanh_k * sech_k
        kap -= f / fp
    return kap


def eval_psi_hat_sq(x: float, kap: float) -> float:
    u = 1.0 - x
    em = math.exp(-kap)
    em2 = em * em
    sk, ck = math.sin(kap), math.cos(kap)
    denom = 1.0 - em2 + 2.0 * em * sk
    grow_damped = ((sk - ck - em) / denom) * math.exp(-kap * (1.0 - u))
    half_one_minus_sig = ((sk - ck - em) * em) / denom
    decay = (1.0 - half_one_minus_sig) * math.exp(-kap * u)
    trig = -math.cos(kap * u) + (1.0 - 2.0 * half_one_minus_sig) * math.sin(kap * u)
    phi = grow_damped + decay + trig
    return phi * phi


def eval_rho_hat(x: float, kap: float) -> float:
    """Exact chiral mode density rho_hat_r(x) = -(1/4) d/dx [psi_hat_r(x)^2]."""
    u = 1.0 - x
    em = math.exp(-kap)
    em2 = em * em
    sk, ck = math.sin(kap), math.cos(kap)
    denom = 1.0 - em2 + 2.0 * em * sk
    grow_damped = ((sk - ck - em) / denom) * math.exp(-kap * (1.0 - u))
    half_one_minus_sig = ((sk - ck - em) * em) / denom
    decay = (1.0 - half_one_minus_sig) * math.exp(-kap * u)
    sig = 1.0 - 2.0 * half_one_minus_sig
    phi = grow_damped + decay - math.cos(kap * u) + sig * math.sin(kap * u)
    # d(phi)/du = kap * (grow_damped - decay + sin(kap*u) + sig*cos(kap*u)), and du/dx = -1
    dphi_du = kap * (grow_damped - decay + math.sin(kap * u) + sig * math.cos(kap * u))
    return 0.5 * phi * dphi_du


def gauss_legendre_0_1(n: int = 44) -> tuple[list[float], list[float]]:
    nodes: list[float] = []
    weights: list[float] = []
    m = (n + 1) // 2
    for i in range(1, m + 1):
        z = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(30):
            p1, p2 = 1.0, 0.0
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = ((2 * j - 1) * z * p2 - (j - 1) * p3) / j
            pp = n * (z * p1 - p2) / (z * z - 1.0)
            z -= p1 / pp
        w = 2.0 / ((1.0 - z * z) * pp * pp)
        x_left = 0.5 * (1.0 - z)
        x_right = 0.5 * (1.0 + z)
        nodes.append(x_left)
        weights.append(0.5 * w)
        if x_left != x_right:
            nodes.append(x_right)
            weights.append(0.5 * w)
    pairs = sorted(zip(nodes, weights))
    return [p[0] for p in pairs], [p[1] for p in pairs]


def verify_all() -> dict:
    # Build finite-n C_{2n}(x) polynomials for n = 0..5
    g_polys: list[list[Fraction]] = [[Fraction(1), Fraction(-1)]]
    for _ in range(10):
        g_polys.append(apply_turn_T(g_polys[-1]))
    C_2n_polys: list[list[Fraction]] = []
    for n in range(6):
        c_poly = [Fraction(0)] * (2 * len(g_polys[2 * n]))
        for j in range(2 * n + 1):
            gj = g_polys[j]
            gk = g_polys[2 * n - j]
            sign = Fraction((-1) ** j)
            for a, ca in enumerate(gj):
                if ca == 0:
                    continue
                for b, cb in enumerate(gk):
                    if cb != 0:
                        c_poly[a + b] += sign * ca * cb
        C_2n_polys.append(c_poly)

    # Compute raw moments m_p^{(2n)} and central moments mu_{p,cent}^{(2n)} around x = 1/4 for p = 0..25
    raw_moments: dict[tuple[int, int], Fraction] = {}
    cent_moments: dict[tuple[int, int], Fraction] = {}
    for n in range(6):
        c_poly = C_2n_polys[n]
        for p in range(26):
            raw_moments[(n, p)] = sum(
                c_coeff / Fraction(p + deg + 1) for deg, c_coeff in enumerate(c_poly) if c_coeff != 0
            )
        for p in range(26):
            acc = Fraction(0)
            for j in range(p + 1):
                acc += math.comb(p, j) * (Fraction(-1, 4) ** (p - j)) * raw_moments[(n, j)]
            cent_moments[(n, p)] = acc

    # 1. Verify Theorem 1: Single-term closed-form coefficients for K = 1..6 (degrees 5..25)
    for K in range(1, 7):
        q_coeffs = single_term_Q_4K_coeffs(K)
        p_coeffs = single_term_P_4K_plus_1_coeffs(K)
        assert q_coeffs[-1] == Fraction(1), f"Q_{{4K}} not monic at K={K}"
        assert poly_eval_frac(p_coeffs, Fraction(0)) == 0, f"P_{{4K+1}}(0) != 0 at K={K}"
        assert poly_eval_frac(p_coeffs, Fraction(1)) == 0, f"P_{{4K+1}}(1) != 0 at K={K}"
        # Verify Unif([0, 1]) integral of Q_{4K} is 0
        unif_int = sum(q_j / Fraction(j + 1) for j, q_j in enumerate(q_coeffs))
        assert unif_int == 0, f"int_0^1 Q_{{4K}}(x) dx != 0 at K={K}"
        # Verify raw-moment syzygy sum_{j=1}^{4K+1} p_{K,j} m_j^{(2n)} == 0 for all n = 0..5
        for n in range(6):
            syz_val = sum(p_j * raw_moments[(n, j)] for j, p_j in enumerate(p_coeffs) if p_j != 0)
            assert syz_val == 0, f"Raw-moment syzygy failed at K={K}, n={n}: {syz_val}"

    # Check K = 1 and K = 2 explicit single-term coefficients
    assert single_term_P_4K_plus_1_coeffs(1) == [
        Fraction(0),
        Fraction(1, 5),
        Fraction(-5, 4),
        Fraction(5, 2),
        Fraction(-9, 4),
        Fraction(4, 5),
    ]
    assert single_term_Q_4K_coeffs(1) == [
        Fraction(1, 20),
        Fraction(-5, 8),
        Fraction(15, 8),
        Fraction(-9, 4),
        Fraction(1, 1),
    ]

    # 2. Verify Theorem 2: Central-moment syzygies and canonical triangular elimination for K = 1..4 (p = 5, 9, 13, 17)
    red_syzygies = build_reduced_central_syzygy_hierarchy(4)
    for K in range(1, 5):
        s_primary = single_term_central_S_coeffs(K)
        s_red = red_syzygies[K]
        assert s_red[4 * K + 1] == Fraction(1)
        assert s_red[1] == Fraction(0)
        for m in range(1, K):
            assert s_red[4 * m + 1] == Fraction(0), f"Intermediate mu_{{4m+1}} not eliminated at K={K}, m={m}"
        for n in range(6):
            val_prim = sum(c * cent_moments[(n, j)] for j, c in enumerate(s_primary) if c != 0)
            val_red = sum(c * cent_moments[(n, j)] for j, c in enumerate(s_red) if c != 0)
            assert val_prim == 0, f"Primary central syzygy failed at K={K}, n={n}"
            assert val_red == 0, f"Reduced central syzygy failed at K={K}, n={n}"

    # Verify K = 1 and K = 2 match our morning rev 101 and Den B's seq 240 byte-for-byte
    assert red_syzygies[1] == [
        Fraction(15, 4096),
        Fraction(0),
        Fraction(-15, 128),
        Fraction(15, 16),
        Fraction(-25, 16),
        Fraction(1),
    ]
    assert red_syzygies[2] == [
        Fraction(-13605, 4194304),
        Fraction(0),
        Fraction(3861, 32768),
        Fraction(-3339, 4096),
        Fraction(2205, 2048),
        Fraction(0),
        Fraction(-357, 256),
        Fraction(63, 32),
        Fraction(-135, 64),
        Fraction(1),
    ]

    # 3. Verify Theorem 3: Quantitative Edge-to-Bulk Defect Duality for COKER-0003 across modes r = 1..5
    xs, ws = gauss_legendre_0_1(44)
    max_duality_err = 0.0
    max_moment_defect_err = 0.0
    max_syzygy_defect_err = 0.0
    r1_defects: dict[str, float] = {}

    for r in range(1, 6):
        kap = solve_beam_kappa(r)
        em = math.exp(-kap)
        # Cancellation-free t_r = (cosh + cos)/(sinh + sin)
        t_r = (1.0 + em * em + 2.0 * em * math.cos(kap)) / (1.0 - em * em + 2.0 * em * math.sin(kap))
        psi2_vals = [eval_psi_hat_sq(x, kap) for x in xs]
        rho_vals = [eval_rho_hat(x, kap) for x in xs]

        # (a) Test Edge-to-Bulk Defect Duality on x^p for p = 1..6
        for p in range(1, 7):
            edge_lhs = sum(w * (x ** p) * rv for x, w, rv in zip(xs, ws, rho_vals)) - 0.25
            bulk_rhs = 0.25 * p * sum(w * (x ** (p - 1)) * (pv - 1.0) for x, w, pv in zip(xs, ws, psi2_vals))
            max_duality_err = max(max_duality_err, abs(edge_lhs - bulk_rhs))

            # Closed-form analytic formulas for p = 1, 2, 3, 4 via (I0, H0, m0) -> (t_r^2/kap^2, t_r/kap^3, 1/kap^4)
            if p == 1:
                exact_def = 0.0
            elif p == 2:
                exact_def = -(t_r * t_r) / (kap * kap)
            elif p == 3:
                exact_def = -1.875 * (t_r * t_r) / (kap * kap) + 0.75 * t_r / (kap ** 3)
            elif p == 4:
                exact_def = -3.75 * (t_r * t_r) / (kap * kap) + 7.5 * t_r / (kap ** 3) - 6.0 / (kap ** 4)
            else:
                exact_def = bulk_rhs
            max_moment_defect_err = max(max_moment_defect_err, abs(edge_lhs - exact_def))
            if r == 1 and p in (1, 2, 3, 4):
                r1_defects[f"p={p}"] = round(edge_lhs, 15)

        # (b) Test simultaneous vanishing of Edge and Bulk defects on P_{4K+1}(x) for K = 1, 2, 3
        for K in (1, 2, 3):
            p_coeffs_flt = [float(c) for c in single_term_P_4K_plus_1_coeffs(K)]
            q_coeffs_flt = [float(c) for c in single_term_Q_4K_coeffs(K)]
            edge_syz = sum(
                w * sum(c * (x ** j) for j, c in enumerate(p_coeffs_flt)) * rv
                for x, w, rv in zip(xs, ws, rho_vals)
            )
            bulk_syz = sum(
                w * sum(c * (x ** j) for j, c in enumerate(q_coeffs_flt)) * (pv - 1.0)
                for x, w, pv in zip(xs, ws, psi2_vals)
            )
            max_syzygy_defect_err = max(max_syzygy_defect_err, abs(edge_syz), abs(bulk_syz))

    assert max_duality_err < 1e-13, f"Edge-to-bulk duality error too large: {max_duality_err}"
    assert max_moment_defect_err < 1e-13, f"Analytic moment defect error too large: {max_moment_defect_err}"
    assert max_syzygy_defect_err < 1e-13, f"Syzygy defect error too large: {max_syzygy_defect_err}"

    return {
        "script": "all_order_gaussian_syzygy_and_coker0003_bridge_2026_11_15.py",
        "theorem_1_single_term_Q4K_and_P4K1_K_1_to_6": True,
        "theorem_2_central_syzygy_hierarchy_K_1_to_4": True,
        "K3_p13_reduced_central_syzygy_coeffs_ascending": [str(c) for c in red_syzygies[3]],
        "theorem_3_coker0003_edge_to_bulk_duality_r_1_to_5": True,
        "r1_edge_bulk_defects_p_1_to_4": r1_defects,
        "max_edge_to_bulk_duality_error": float(f"{max_duality_err:.3e}"),
        "max_analytic_moment_defect_error": float(f"{max_moment_defect_err:.3e}"),
        "max_syzygy_equilibrium_error": float(f"{max_syzygy_defect_err:.3e}"),
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    res = verify_all()
    out_path = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out_path.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
