#!/usr/bin/env python3
"""Gaussian Barycentric Parity Decomposition & Master Laplace-Krylov Integral Symmetries.

Date: 2026-11-15 (Afternoon Pass, 16:20 CET)
Author: Petrovich (ompu-e1dd503f59), extending Cloud Jee & Jee-AGY (READ-0087, 1794756477),
        Φ-Hausmaster (1794739445), Jee A (1794736035), and Den B (1794736594).

Summary of New Exact Results Verified Here (`python3 -I -B`, zero external deps required):
1. Theorem 1 (Gaussian Barycentric Factorization & Complete Cancellation of (-4)^K):
   Introducing the complex barycentric coordinate w(x) := x + i*(1 - x) on [0, 1] alongside
   y = 2x - 1, we have the exact algebraic identity:
       y + i = (2x - 1) + i = (1 + i) * w(x).
   Since (1 + i)^(4K) = (-4)^K and (1 + i)^(4K+1) = (-4)^K * (1 + i), raising to power
   4K or 4K+1 cancels ALL alternating signs (-1)^K and ALL denominators 4^K in Q_K, B_K, P_{4K+1}:
       Q_K(2x - 1) = (2x - 1)^(4K+1) + (1/2) * Im[(1 + i) * w(x)^(4K+1)]         (for all K >= 0),
       B_K(2x - 1) = (2x - 1)^(4K) - 1/(4K + 1) + (1/2) * Im[w(x)^(4K)]          (for all K >= 1),
       P_{4K+1}(x) = [(2x - 1)^(4K+1) - (2x - 1)
                      + (1/2) * Im[(1 + i) * (w(x)^(4K+1) - w(x))]] / ((4K + 1) * 2^(4K - 1)).

2. Theorem 2 (Canonical Reflection-Parity Decomposition & 2-Line Mirror Doubling Proof):
   Under reflection x <-> 1 - x, w(1 - x) = (1 - x) + i*x = i * conj(w(x)).
   Since i^(4K) = +1 for every K >= 1, we have w(1 - x)^(4K) = conj(w(x)^(4K)), whence:
       Im[w(1 - x)^(4K)] = -Im[w(x)^(4K)]   (strictly ODD under x <-> 1 - x for all K >= 1!).
   Therefore:
   (a) integral_0^1 Im[w(x)^(4K)] dx = 0 identically under Unif([0, 1]) for all K >= 1;
   (b) B_K(2x - 1) = B_K^even(x) + B_K^odd(x) is the canonical parity decomposition into
           B_K^even(x) := (2x - 1)^(4K) - 1/(4K + 1)   and   B_K^odd(x) := (1/2) * Im[w(x)^(4K)];
   (c) Orthogonality B_K perp psi_hat_r^2 is equivalent to the exact Parity Balance Law:
           integral_0^1 [(2x - 1)^(4K) - 1/(4K + 1)] psi_hat_r(x)^2 dx
               = -(1/2) * integral_0^1 Im[w(x)^(4K)] psi_hat_r(x)^2 dx   (for all r >= 1, K >= 1),
       immediately implying B_K(2(1 - x) - 1) = B_K^even(x) - B_K^odd(x) integrates to TWICE
       the even central-moment excess on every mode r >= 1 without any calculus!

3. Theorem 3 (Master Laplace-Krylov Integral Symmetries Across All Orders Simultaneously):
   Let E_0(u) := (cosh u + cos u)/2 = sum_{K>=0} u^(4K)/(4K)! and
       E_1(u) := (sinh u + sin u)/2 = sum_{K>=0} u^(4K+1)/(4K+1)! be the 4-periodic Krylov kernels.
   Summing Theorem 1 over all K >= 0 yields two global two-parameter continuum laws:
   (a) Finite-z Wick-Darboux Master Symmetry (for ALL s in C and ALL z in C):
           integral_0^1 { E_1(s(2x - 1)) + (1/2) * Im[(1 + i) * E_1(s * w(x))] } rho_{z^2}(x) dx = 0;
   (b) Clamped-Free Beam Master Law (for ALL r >= 1 and ALL s in C):
           integral_0^1 { E_0(s(2x - 1)) + (1/2) * Im[E_0(s * w(x))] } psi_hat_r(x)^2 dx
               = (sinh s + sin s) / (2s) = integral_0^1 E_0(s(2x - 1)) dx.
       That is, adding the odd Gaussian shadow (1/2)*Im[E_0(s*w(x))] makes EVERY individual
       beam mode psi_hat_r(x)^2 (already at r = 1!) match the exact Unif([0, 1]) E_0-transform
       identically at all s in C!
"""

from __future__ import annotations

import cmath
from fractions import Fraction
import json
import math
from pathlib import Path


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_scale(a: list[Fraction], s: Fraction) -> list[Fraction]:
    s = Fraction(s)
    if s == 0:
        return [Fraction(0)]
    return [c * s for c in a]


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] += ca * cb
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_pow(a: list[Fraction], e: int) -> list[Fraction]:
    res = [Fraction(1)]
    base = a[:]
    while e > 0:
        if e & 1:
            res = poly_mul(res, base)
        base = poly_mul(base, base)
        e >>= 1
    return res


def cpoly_mul(
    ar: list[Fraction], ai: list[Fraction], br: list[Fraction], bi: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    rr = poly_add(poly_mul(ar, br), poly_scale(poly_mul(ai, bi), Fraction(-1)))
    ri = poly_add(poly_mul(ar, bi), poly_mul(ai, br))
    return rr, ri


def cpoly_pow(
    ar: list[Fraction], ai: list[Fraction], e: int
) -> tuple[list[Fraction], list[Fraction]]:
    rr, ri = [Fraction(1)], [Fraction(0)]
    br, bi = ar[:], ai[:]
    while e > 0:
        if e & 1:
            rr, ri = cpoly_mul(rr, ri, br, bi)
        br, bi = cpoly_mul(br, bi, br, bi)
        e >>= 1
    return rr, ri


def poly_eval_frac(a: list[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    for c in reversed(a):
        acc = acc * x + c
    return acc


def poly_reflect(a: list[Fraction]) -> list[Fraction]:
    """Compute P(1 - x) in exact Fraction arithmetic."""
    one_minus_x = [Fraction(1), Fraction(-1)]
    acc = [Fraction(0)]
    for i, c in enumerate(a):
        if c != 0:
            acc = poly_add(acc, poly_scale(poly_pow(one_minus_x, i), c))
    return acc


def poly_int_0_1(a: list[Fraction]) -> Fraction:
    return sum(c / Fraction(i + 1) for i, c in enumerate(a))


def build_morning_Q_K_in_x(K: int) -> list[Fraction]:
    """Morning definition: y^(4K+1) + ((-1)^K / (2 * 4^K)) * Im[(y + i)^(4K+1)], y = 2x - 1."""
    y_poly = [Fraction(-1), Fraction(2)]
    deg = 4 * K + 1
    yr, yi = cpoly_pow(y_poly, [Fraction(1)], deg)
    return poly_add(poly_pow(y_poly, deg), poly_scale(yi, Fraction((-1) ** K, 2 * (4 ** K))))


def build_barycentric_Q_K_in_x(K: int) -> list[Fraction]:
    """New (-4)^K-free form: (2x - 1)^(4K+1) + (1/2) * Im[(1 + i) * (x + i(1 - x))^(4K+1)]."""
    y_poly = [Fraction(-1), Fraction(2)]
    wr = [Fraction(0), Fraction(1)]       # x
    wi = [Fraction(1), Fraction(-1)]      # 1 - x
    deg = 4 * K + 1
    pr, pi = cpoly_pow(wr, wi, deg)
    # Im[(1 + i) * (pr + i*pi)] = pr + pi
    im_part = poly_add(pr, pi)
    return poly_add(poly_pow(y_poly, deg), poly_scale(im_part, Fraction(1, 2)))


def build_morning_B_K_in_x(K: int) -> list[Fraction]:
    y_poly = [Fraction(-1), Fraction(2)]
    deg = 4 * K
    yr, yi = cpoly_pow(y_poly, [Fraction(1)], deg)
    even_part = poly_add(poly_pow(y_poly, deg), [Fraction(-1, 4 * K + 1)])
    return poly_add(even_part, poly_scale(yi, Fraction((-1) ** K, 2 * (4 ** K))))


def build_barycentric_B_K_parts_in_x(K: int) -> tuple[list[Fraction], list[Fraction]]:
    """Return (B_K^even(x), B_K^odd(x)) where B_K^odd(x) = (1/2) * Im[(x + i(1 - x))^(4K)]."""
    y_poly = [Fraction(-1), Fraction(2)]
    wr = [Fraction(0), Fraction(1)]
    wi = [Fraction(1), Fraction(-1)]
    deg = 4 * K
    _, pi = cpoly_pow(wr, wi, deg)
    even_part = poly_add(poly_pow(y_poly, deg), [Fraction(-1, 4 * K + 1)])
    odd_part = poly_scale(pi, Fraction(1, 2))
    return even_part, odd_part


def E0_complex(u: complex) -> complex:
    return 0.5 * (cmath.cosh(u) + cmath.cos(u))


def E1_complex(u: complex) -> complex:
    return 0.5 * (cmath.sinh(u) + cmath.sin(u))


def eval_F_z_meromorphic(x: float, z: complex) -> complex:
    """Exact meromorphic solution of F''(x) = z F(1 - x), F(1) = 0, F'(1) = -1 for ALL z in C."""
    if abs(z) < 1e-12:
        return complex(1.0 - x, 0.0)
    mu = 0.5 * cmath.sqrt(z)
    y = 2.0 * x - 1.0
    num = cmath.sin(mu) * cmath.cosh(mu * y) - cmath.cosh(mu) * cmath.sin(mu * y)
    den = 2.0 * mu * (cmath.cosh(mu) * cmath.cos(mu) - cmath.sinh(mu) * cmath.sin(mu))
    return num / den


def solve_beam_kappa(r: int) -> float:
    """Solve cos(kappa) + sech(kappa) = 0 for mode r >= 1 without overflow."""
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


def eval_psi_hat_sq(x: float, kap: float, r: int) -> float:
    """Cancellation-free normalized clamped-free mode psi_hat_r(x)^2 (clamped at x=1, free at x=0)."""
    u = 1.0 - x
    em = math.exp(-kap)
    em2 = em * em
    sk, ck = math.sin(kap), math.cos(kap)
    denom = 1.0 - em2 + 2.0 * em * sk
    # (1 - sigma_r)/2 * exp(k*u) written via exp(-k*(1-u)) with zero growing exponentials:
    grow_damped = ((sk - ck - em) / denom) * math.exp(-kap * (1.0 - u))
    half_one_minus_sig = ((sk - ck - em) * em) / denom
    decay = (1.0 - half_one_minus_sig) * math.exp(-kap * u)
    trig = -math.cos(kap * u) + (1.0 - 2.0 * half_one_minus_sig) * math.sin(kap * u)
    phi = grow_damped + decay + trig
    return phi * phi


def gauss_legendre_0_1(n: int = 40) -> tuple[list[float], list[float]]:
    """Compute n-point Gauss-Legendre nodes and weights on [0, 1]."""
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
    # 1. Exact Fraction verification of Theorem 1 & Theorem 2 for K = 0..8 (up to degree 33)
    for K in range(9):
        q_old = build_morning_Q_K_in_x(K)
        q_new = build_barycentric_Q_K_in_x(K)
        assert q_old == q_new, f"Theorem 1 Q_K mismatch at K={K}"

    for K in range(1, 9):
        b_old = build_morning_B_K_in_x(K)
        b_even, b_odd = build_barycentric_B_K_parts_in_x(K)
        assert poly_add(b_even, b_odd) == b_old, f"Theorem 1 B_K mismatch at K={K}"
        # Verify exact reflection parity: B_K^even(1 - x) == +B_K^even(x) and B_K^odd(1 - x) == -B_K^odd(x)
        assert poly_reflect(b_even) == b_even, f"B_K^even not reflection-even at K={K}"
        assert poly_reflect(b_odd) == poly_scale(b_odd, Fraction(-1)), f"B_K^odd not reflection-odd at K={K}"
        # Verify zero uniform integral of both parts
        assert poly_int_0_1(b_even) == 0, f"B_K^even uniform integral != 0 at K={K}"
        assert poly_int_0_1(b_odd) == 0, f"B_K^odd uniform integral != 0 at K={K}"

    # Verify Cloud Jee's P_{4K+1}(x) matches (-4)^K-free barycentric chord formula for K = 1..6
    y_poly = [Fraction(-1), Fraction(2)]
    wr, wi = [Fraction(0), Fraction(1)], [Fraction(1), Fraction(-1)]
    for K in range(1, 7):
        q_k = build_barycentric_Q_K_in_x(K)
        q_0 = build_barycentric_Q_K_in_x(0)
        p_cj = poly_scale(poly_add(q_k, poly_scale(q_0, Fraction(-1))), Fraction(1, (4 * K + 1) * (2 ** (4 * K - 1))))
        assert poly_eval_frac(p_cj, Fraction(0)) == 0 and poly_eval_frac(p_cj, Fraction(1)) == 0
        pr, pi = cpoly_pow(wr, wi, 4 * K + 1)
        # Im[(1+i)(w^(4K+1) - w)] = (pr + pi) - 1 since pr_1 + pi_1 = x + (1 - x) = 1!
        im_diff = poly_add(poly_add(pr, pi), [Fraction(-1)])
        num = poly_add(poly_add(poly_pow(y_poly, 4 * K + 1), poly_scale(y_poly, Fraction(-1))), poly_scale(im_diff, Fraction(1, 2)))
        p_bary = poly_scale(num, Fraction(1, (4 * K + 1) * (2 ** (4 * K - 1))))
        assert p_bary == p_cj, f"Barycentric P_{{4K+1}} mismatch at K={K}"

    # 2. Verify Theorem 3(a): Global finite-z Wick-Darboux Master Symmetry across complex (s, z),
    #    including z = 5.2 + 2.7j (|z| = 5.86 > kappa_1^2 = 3.516, outside the Volterra disk!)
    xs, ws = gauss_legendre_0_1(44)
    max_wick_master_err = 0.0
    for z in (0.0 + 0.0j, 0.7 - 0.4j, 1.25 + 0.9j, -1.8 + 0.6j, 5.2 + 2.7j):
        rho_vals = [eval_F_z_meromorphic(x, z) * eval_F_z_meromorphic(x, -z) for x in xs]
        norm_z = sum(w * rv for w, rv in zip(ws, rho_vals))
        for s in (0.6 + 0.3j, 1.4 - 0.8j, -0.9 + 1.1j):
            acc = 0.0 + 0.0j
            for x, w, rv in zip(xs, ws, rho_vals):
                wx = complex(x, 1.0 - x)
                w_bar = complex(x, -(1.0 - x))
                shadow_1 = ((1.0 + 1.0j) * E1_complex(s * wx) - (1.0 - 1.0j) * E1_complex(s * w_bar)) / (2.0j)
                ker = E1_complex(s * (2.0 * x - 1.0)) + 0.5 * shadow_1
                acc += w * ker * (rv / norm_z)
            max_wick_master_err = max(max_wick_master_err, abs(acc))
    assert max_wick_master_err < 1e-14, f"Master Wick-Darboux error too large: {max_wick_master_err}"

    # 3. Verify Theorem 2(c) & Theorem 3(b): Clamped-Free Beam Master Law & Parity Balance across r = 1..5
    max_beam_master_err = 0.0
    max_parity_balance_err = 0.0
    r1_B1_even_excess = 0.0
    r1_B1_odd_term = 0.0
    for r in range(1, 6):
        kap = solve_beam_kappa(r)
        psi2_vals = [eval_psi_hat_sq(x, kap, r) for x in xs]
        norm_psi = sum(w * pv for w, pv in zip(ws, psi2_vals))
        assert abs(norm_psi - 1.0) < 1e-13 and abs(eval_psi_hat_sq(0.0, kap, r) - 4.0) < 1e-12

        # Check parity balance at K = 1, 2, 3
        for K in (1, 2, 3, 4):
            ev_int = sum(w * (((2.0 * x - 1.0) ** (4 * K)) - 1.0 / (4 * K + 1)) * pv for x, w, pv in zip(xs, ws, psi2_vals))
            od_int = sum(w * (0.5 * (complex(x, 1.0 - x) ** (4 * K)).imag) * pv for x, w, pv in zip(xs, ws, psi2_vals))
            max_parity_balance_err = max(max_parity_balance_err, abs(ev_int + od_int))
            if r == 1 and K == 1:
                r1_B1_even_excess = ev_int
                r1_B1_odd_term = od_int

        # Check Master E_0 Integral Law for complex s in C
        for s in (0.5 + 0.0j, 1.3 - 0.7j, 2.1 + 0.9j):
            target = (cmath.sinh(s) + cmath.sin(s)) / (2.0 * s)
            lhs = 0.0 + 0.0j
            for x, w, pv in zip(xs, ws, psi2_vals):
                wx = complex(x, 1.0 - x)
                w_bar = complex(x, -(1.0 - x))
                shadow_0 = (E0_complex(s * wx) - E0_complex(s * w_bar)) / (2.0j)
                ker0 = E0_complex(s * (2.0 * x - 1.0)) + 0.5 * shadow_0
                lhs += w * ker0 * pv
            max_beam_master_err = max(max_beam_master_err, abs(lhs - target))

    assert max_parity_balance_err < 1e-14, f"Parity balance error too large: {max_parity_balance_err}"
    assert max_beam_master_err < 1e-14, f"Beam master E_0 law error too large: {max_beam_master_err}"

    return {
        "theorem_1_barycentric_cancellation_K_0_to_8": True,
        "theorem_2_reflection_parity_decomposition_K_1_to_8": True,
        "cloud_jee_P_4K_plus_1_barycentric_match_K_1_to_6": True,
        "r1_B1_even_excess": round(r1_B1_even_excess, 15),
        "r1_B1_odd_term": round(r1_B1_odd_term, 15),
        "r1_mirror_doubled_2x_even": round(2.0 * r1_B1_even_excess, 12),
        "max_wick_darboux_master_E1_error": float(f"{max_wick_master_err:.3e}"),
        "max_beam_master_E0_error": float(f"{max_beam_master_err:.3e}"),
        "max_parity_balance_error": float(f"{max_parity_balance_err:.3e}"),
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    res = verify_all()
    out_path = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out_path.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2))
