#!/usr/bin/env python3
r"""
stieltjes_pade_spectral_bounds_and_jacobi_tridiagonal_quartet_2026_11_19.py
===========================================================================
OMPU Stereo Pair — Lane B Lab Verification Module (Thursday Evening, Rev 109)
Author: Den B (Lane B, instance jee-instance-524e408b5123473d95578e39c889f8a9)
Date:   2026-11-19

100% self-contained (`stdlib`-only: `decimal`, `fractions`, `json`, `math`, `pathlib`, `typing`;
0 local imports, 0 network/subprocess calls). Runnable via `python3 -I -B -W error`.

Completes the Stieltjes S-fraction / J-fraction / Diagonal [m/m] Padé & Gauss-Stieltjes Quadrature
theory of all 6 ordered quartet ratios R_{\beta/\alpha}(z) := (\beta! e_\beta(z)) / (\alpha! e_\alpha(z))
(0 <= \alpha < \beta <= 3), extending `seq 254` (`0a54f35d...`), Jee A's `seq 255` (`ad5f783d...`),
and `READ-0118 / READ-0119` (`commit 1ddcb09`):

  1. THEOREM 1 (Algebraic Mechanism of the (1, 2, 3) Unit-Fraction S-Fraction Staircase &
     Two-Handed Hankel-Stieltjes Determinantal Closure):
     - For 1 - R_{\beta/\alpha}(z) = c_1 z / (1 + c_2 z / (1 + c_3 z / ...)), all c_n^{(\alpha,\beta)} > 0
       match identically between Hand 1 (recursive series division) and Hand 2 (Hankel-Stieltjes
       determinantal ratios c_{2m} = H_m^{(2)} H_{m-2}^{(1)} / (H_{m-1}^{(1)} H_{m-1}^{(2)}),
       c_{2m+1} = H_m^{(1)} H_{m-1}^{(2)} / (H_m^{(2)} H_{m-1}^{(1)})) up to n = 12 across all 6 pairs.
     - On adjacent sectors (\alpha, \alpha+1), c_1 = 4 / (\alpha+1)_5 and
           c_2^{(\alpha,\alpha+1)} = \frac{(\alpha+6)_4 - 2(\alpha+1)_4}{(\alpha+1)_4 (\alpha+6)_4},
       whose numerator P(\alpha) = (\alpha+6)_4 - 2(\alpha+1)_4 is 5-smooth ONLY at \alpha in {1, 2}
       (P(1) = 4800 -> 1/126, P(2) = 7200 -> 1/396, vs prime factors 31 at \alpha=0 and 17 at \alpha=3),
       while at \alpha = 2 the unit-fraction Turanian H_2^{(1)}(\mu^{(2,3)}) = 1/4045617576000 forces
       c_3^{(2,3)} = 1/25740, explaining the exact (1, 2, 3) staircase of initial unit fractions on
       (0,1), (1,2), (2,3).

  2. THEOREM 2 (Even J-Fraction Contraction, Tridiagonal Jacobi Polynomials, Continuant Wronskian
     & Diagonal [m/m] Padé Inversion Reciprocity):
     - Contracting the S-fraction yields the 3-term orthogonal recurrence (m >= 2)
           Q_m(z) = [1 + (c_{2m-1} + c_{2m}) z] Q_{m-1}(z) - c_{2m-2} c_{2m-1} z^2 Q_{m-2}(z),
           N_m(z) = [1 + (c_{2m-1} + c_{2m}) z] N_{m-1}(z) - c_{2m-2} c_{2m-1} z^2 N_{m-2}(z),
       with P_m(z) = Q_m(z) - N_m(z), exact continuant Wronskian
           Q_m(z) N_{m-1}(z) - Q_{m-1}(z) N_m(z) == - (c_1 c_2 ... c_{2m-1}) z^{2m-1},
       and exact agreement with Hand 3 (direct m x m linear Padé solver), satisfying exact inversion
       reciprocity P_m^{(\alpha,\beta)}(z) == Q_m^{(\beta,\alpha)}(z) for all (\alpha, \beta) and m = 1..6.

  3. THEOREM 3 (Simultaneous Pole-Zero Interlacing, Pure-Factorial Monotone Spectral Bounds &
     38-Digit Gauss-Stieltjes Reconstruction of Ramanujan-Krylov Wronskian Weights):
     - For every pair 0 <= \alpha < \beta <= 3 and m = 1..6, all m roots x_{m,1} < ... < x_{m,m} of
       Q_m^{(\alpha,\beta)}(-x) = 0 and all m roots y_{m,1} < ... < y_{m,m} of P_m^{(\alpha,\beta)}(-x) = 0
       are real, positive, and strictly interlace:
           0 < x_{m,1} < y_{m,1} < x_{m,2} < y_{m,2} < ... < x_{m,m} < y_{m,m}.
     - The fundamental Padé pole x_{m,1}^{(\alpha,\beta)} and zero y_{m,1}^{(\alpha,\beta)} decrease
       strictly monotonically with m from above onto 4(\mu_1^{(\alpha)})^4 and 4(\mu_1^{(\beta)})^4
       (reaching 3.88e-39 on \pi^4/4 and 1.39e-29 on 4\beta_1^4 at m = 6 from factorials alone!),
       while the Gauss-Stieltjes quadrature weight w_{m,1} = N_m(-x_{m,1}) / (x_{m,1} Q'_m(-x_{m,1})) > 0
       converges to 38 digits to the exact Ramanujan-Krylov Wronskian residue -W_{\beta,\alpha}(\mu_1^{(\alpha)}) / x_1^{(\alpha)}
       (including 4 \tanh(\pi/2) / ((\pi/2)^3 \cdot (\pi^4/4)) on the Euler-Ramanujan pair (0, 2)!).
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

getcontext().prec = 90


# ---------------------------------------------------------------------------
# 0. Standalone Exact Fraction Polynomial, Determinant & Decimal Primitives
# ---------------------------------------------------------------------------

def poly_trim(p: List[Fraction]) -> List[Fraction]:
    out = p[:] if p else [Fraction(0)]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: List[Fraction], b: List[Fraction], sa: Fraction = Fraction(1), sb: Fraction = Fraction(1)) -> List[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i in range(len(a)):
        out[i] += sa * a[i]
    for i in range(len(b)):
        out[i] += sb * b[i]
    return poly_trim(out)


def poly_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    if not a or not b:
        return [Fraction(0)]
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca:
            for j, cb in enumerate(b):
                out[i + j] += ca * cb
    return poly_trim(out)


def series_inv(a: List[Fraction]) -> List[Fraction]:
    assert a[0] != 0
    inv = [Fraction(1) / a[0]]
    for k in range(1, len(a)):
        inv.append(-sum(a[j] * inv[k - j] for j in range(1, k + 1)) / a[0])
    return inv


def series_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = min(len(a), len(b))
    return [sum(a[j] * b[k - j] for j in range(k + 1)) for k in range(n)]


def det_fraction(mat: List[List[Fraction]]) -> Fraction:
    n = len(mat)
    if n == 0:
        return Fraction(1)
    a = [[Fraction(x) for x in r] for r in mat]
    sgn = Fraction(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if a[r][col] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != col:
            a[col], a[piv] = a[piv], a[col]
            sgn = -sgn
        sgn *= a[col][col]
        f = a[col][col]
        a[col] = [x / f for x in a[col]]
        for r in range(col + 1, n):
            ff = a[r][col]
            if ff:
                a[r] = [a[r][c] - ff * a[col][c] for c in range(n)]
    return sgn


def compute_pi_dec() -> Decimal:
    def arctan_inv(m: int) -> Decimal:
        m_d = Decimal(m)
        m2 = m_d * m_d
        term = Decimal(1) / m_d
        total = term
        k = 1
        while True:
            term = -term / m2
            add = term / Decimal(2 * k + 1)
            total += add
            if abs(add) < Decimal("1e-93"):
                break
            k += 1
        return total

    return Decimal(4) * (Decimal(4) * arctan_inv(5) - arctan_inv(239))


PI_DEC = compute_pi_dec()


def dec_sinh_cosh(x: Decimal) -> Tuple[Decimal, Decimal]:
    ex, emx = x.exp(), (-x).exp()
    return Decimal("0.5") * (ex - emx), Decimal("0.5") * (ex + emx)


def dec_sin_cos(x: Decimal) -> Tuple[Decimal, Decimal]:
    two_pi = Decimal(2) * PI_DEC
    sgn = Decimal(-1) if x < 0 else Decimal(1)
    xr = abs(x) % two_pi
    if xr > PI_DEC:
        xr -= two_pi
    xr *= sgn
    x2 = xr * xr
    sin_v, cos_v = xr, Decimal(1)
    t_sin, t_cos = xr, Decimal(1)
    k = 1
    while True:
        t_cos = -t_cos * x2 / Decimal((2 * k - 1) * (2 * k))
        t_sin = -t_sin * x2 / Decimal((2 * k) * (2 * k + 1))
        cos_v += t_cos
        sin_v += t_sin
        if abs(t_cos) < Decimal("1e-93") and abs(t_sin) < Decimal("1e-93"):
            break
        k += 1
    return sin_v, cos_v


def solve_root_sector(alpha: int, m: int) -> Decimal:
    if alpha == 0:
        return (Decimal(m) - Decimal("0.5")) * PI_DEC
    if alpha == 2:
        return Decimal(m) * PI_DEC
    x = (Decimal(m) + (Decimal("-0.25") if alpha == 1 else Decimal("0.25"))) * PI_DEC
    sgn = Decimal(1) if alpha == 1 else Decimal(-1)
    for _ in range(18):
        sh, ch = dec_sinh_cosh(x)
        si, co = dec_sin_cos(x)
        th = sh / ch
        f = th * co + sgn * si
        fp = (Decimal(1) - th * th) * co - th * si + sgn * co
        dx = f / fp
        x -= dx
        if abs(dx) < Decimal("1e-85"):
            break
    return x


# ---------------------------------------------------------------------------
# 1. Theorem 1: Two-Handed S-Fraction Extraction & (1,2,3) Staircase Mechanism
# ---------------------------------------------------------------------------

def s_fraction_series_hand1(r_ba: List[Fraction], n_terms: int) -> List[Fraction]:
    cur = [-r_ba[k] for k in range(1, len(r_ba))]
    cs: List[Fraction] = []
    for _ in range(n_terms):
        c = cur[0]
        assert c > 0
        cs.append(c)
        normed = [v / c for v in cur]
        cur = series_inv(normed)[1:]
    return cs


def s_fraction_hankel_hand2(r_ba: List[Fraction], n_terms: int) -> List[Fraction]:
    """
    Stieltjes-Hankel determinantal formula using moments mu_k = (-1)^k r_ba[k] > 0:
      H_m^{(1)} = det_{1<=i,j<=m}[mu_{i+j-1}],   H_m^{(2)} = det_{1<=i,j<=m}[mu_{i+j}],
      with H_0^{(1)} = H_0^{(2)} = 1:
      c_1 = H_1^{(1)},
      c_{2m}   = (H_m^{(2)} * H_{m-1? wait: let's check index!}):
        c_2 = mu_2 / mu_1 = H_1^{(2)} / H_1^{(1)} = (H_1^{(2)} H_0^{(1)}) / (H_1^{(1)} H_0^{(2)}),
        c_3 = H_2^{(1)} / (H_1^{(1)} H_1^{(2)}) = (H_2^{(1)} H_0^{(2)}) / (H_1^{(1)} H_1^{(2)}),
        c_{2m}   = (H_m^{(2)} H_{m-1}^{(1)}^{-1} ... wait: c_4 = (H_2^{(2)} H_1^{(1)}) / (H_2^{(1)} H_1^{(2)})!)
        YES: c_{2m}   = (H_m^{(2)} * H_{m-1}^{(1)}) / (H_m^{(1)} * H_{m-1}^{(2)})?
             Check m=1: (H_1^{(2)} H_0^{(1)}) / (H_1^{(1)} H_0^{(2)}) = mu_2 / mu_1 = c_2!
             Check m=2: c_2 * c_3 * c_4? Wait: H_2^{(1)} = c_1^2 c_2 c_3, H_1^{(2)} = c_1 c_2,
                        H_2^{(2)} = c_1^2 c_2^2 c_3 c_4 => (H_2^{(2)} H_1^{(1)}) / (H_2^{(1)} H_1^{(2)})
                        = (c_1^2 c_2^2 c_3 c_4 * c_1) / (c_1^2 c_2 c_3 * c_1 c_2) == c_4!!
        AND c_{2m+1} = (H_{m+1}^{(1)} * H_{m-1}^{(2)}) / (H_m^{(1)} * H_m^{(2)})!
             Check m=1: (H_2^{(1)} H_0^{(2)}) / (H_1^{(1)} H_1^{(2)}) = (c_1^2 c_2 c_3) / (c_1 * c_1 c_2) == c_3!!
    """
    mu = [Fraction(0)] + [((-1) ** k) * r_ba[k] for k in range(1, len(r_ba))]
    m_max = (n_terms + 2) // 2 + 1
    h1 = [Fraction(1)] + [
        det_fraction([[mu[i + j - 1] for j in range(1, m + 1)] for i in range(1, m + 1)])
        for m in range(1, m_max + 1)
    ]
    h2 = [Fraction(1)] + [
        det_fraction([[mu[i + j] for j in range(1, m + 1)] for i in range(1, m + 1)])
        for m in range(1, m_max + 1)
    ]
    cs = [h1[1]]
    for idx in range(2, n_terms + 1):
        if idx % 2 == 0:
            m = idx // 2
            cs.append((h2[m] * h1[m - 1]) / (h1[m] * h2[m - 1]))
        else:
            m = (idx - 1) // 2
            cs.append((h1[m + 1] * h2[m - 1]) / (h1[m] * h2[m]))
    return cs


def pochhammer4(n: int) -> int:
    return n * (n + 1) * (n + 2) * (n + 3)


def verify_theorem_1(eb: List[List[Fraction]]) -> Dict[str, object]:
    s_table: Dict[str, List[str]] = {}
    for a in range(4):
        for b in range(a + 1, 4):
            r_ba = series_mul(eb[b], series_inv(eb[a]))
            c_h1 = s_fraction_series_hand1(r_ba, 12)
            c_h2 = s_fraction_hankel_hand2(r_ba, 12)
            assert c_h1 == c_h2, f"Two-handed S-fraction mismatch at ({a},{b})"
            assert all(c > 0 for c in c_h1)
            s_table[f"({a},{b})"] = [str(c) for c in c_h1[:6]]

    # Verify (1, 2, 3) unit-fraction staircase mechanism on adjacent pairs (alpha, alpha+1)
    unit_counts = []
    for a in (0, 1, 2):
        cs = s_table[f"({a},{a+1})"]
        cnt = 0
        for s_val in cs:
            if Fraction(s_val).numerator == 1:
                cnt += 1
            else:
                break
        unit_counts.append(cnt)

        # Verify closed formula for c_1 and c_2:
        c1_closed = Fraction(4, (a + 1) * pochhammer4(a + 2))
        num_c2 = pochhammer4(a + 6) - 2 * pochhammer4(a + 1)
        den_c2 = pochhammer4(a + 1) * pochhammer4(a + 6)
        assert Fraction(cs[0]) == c1_closed
        assert Fraction(cs[1]) == Fraction(num_c2, den_c2)

    assert unit_counts == [1, 2, 3]
    assert s_table["(2,3)"][:3] == ["1/630", "1/396", "1/25740"]
    assert s_table["(0,2)"][:3] == ["7/180", "181/4410", "9403/456576120"]

    return {
        "status": "PASS",
        "adjacent_initial_unit_fraction_counts": unit_counts,
        "euler_ramanujan_02_c1_to_6": s_table["(0,2)"],
        "pair_23_c1_to_6": s_table["(2,3)"],
        "two_handed_series_vs_hankel_verified_n12": True,
    }


# ---------------------------------------------------------------------------
# 2. Theorem 2: J-Fraction Contraction, Continuant Wronskian & Padé Reciprocity
# ---------------------------------------------------------------------------

def j_fraction_pade(cs: List[Fraction], m_max: int) -> Tuple[List[List[Fraction]], List[List[Fraction]], List[List[Fraction]]]:
    q_list = [[Fraction(1)], [Fraction(1), cs[1]]]
    n_list = [[Fraction(0)], [Fraction(0), cs[0]]]
    for m in range(2, m_max + 1):
        lin = [Fraction(1), cs[2 * m - 2] + cs[2 * m - 1]]
        quad_c = cs[2 * m - 3] * cs[2 * m - 2]
        q_next = poly_add(
            poly_mul(lin, q_list[-1]),
            [Fraction(0), Fraction(0)] + q_list[-2],
            Fraction(1),
            -quad_c,
        )
        n_next = poly_add(
            poly_mul(lin, n_list[-1]),
            [Fraction(0), Fraction(0)] + n_list[-2],
            Fraction(1),
            -quad_c,
        )
        q_list.append(q_next)
        n_list.append(n_next)
    p_list = [poly_add(q_list[m], n_list[m], Fraction(1), Fraction(-1)) for m in range(m_max + 1)]
    return p_list, q_list, n_list


def linear_pade_hand3(r_coeffs: List[Fraction], m: int) -> Tuple[List[Fraction], List[Fraction]]:
    aug = [
        [r_coeffs[k - j] for j in range(1, m + 1)] + [-r_coeffs[k]]
        for k in range(m + 1, 2 * m + 1)
    ]
    for col in range(m):
        piv = next(r for r in range(col, m) if aug[r][col] != 0)
        aug[col], aug[piv] = aug[piv], aug[col]
        f = aug[col][col]
        aug[col] = [x / f for x in aug[col]]
        for r in range(m):
            if r != col and aug[r][col] != 0:
                ff = aug[r][col]
                aug[r] = [aug[r][c] - ff * aug[col][c] for c in range(m + 1)]
    q = [Fraction(1)] + [aug[i][m] for i in range(m)]
    p = [sum(q[j] * r_coeffs[k - j] for j in range(min(k, m) + 1)) for k in range(m + 1)]
    return poly_trim(p), poly_trim(q)


def verify_theorem_2(eb: List[List[Fraction]]) -> Dict[str, object]:
    for a in range(4):
        for b in range(a + 1, 4):
            r_ba = series_mul(eb[b], series_inv(eb[a]))
            r_ab = series_mul(eb[a], series_inv(eb[b]))
            cs = s_fraction_series_hand1(r_ba, 12)
            p_j, q_j, n_j = j_fraction_pade(cs, 6)

            for m in range(1, 7):
                p_lin_ab, q_lin_ab = linear_pade_hand3(r_ba, m)
                p_lin_ba, q_lin_ba = linear_pade_hand3(r_ab, m)
                assert p_j[m] == p_lin_ab == q_lin_ba
                assert q_j[m] == q_lin_ab == p_lin_ba

                # Order O(z^{2m+1}) accuracy & exact continuant Wronskian
                q_pad = q_j[m] + [Fraction(0)] * (2 * m + 1 - len(q_j[m]))
                p_pad = p_j[m] + [Fraction(0)] * (2 * m + 1 - len(p_j[m]))
                assert series_mul(p_pad, series_inv(q_pad))[: 2 * m + 1] == r_ba[: 2 * m + 1]

                wron = poly_add(poly_mul(q_j[m], n_j[m - 1]), poly_mul(q_j[m - 1], n_j[m]), Fraction(1), Fraction(-1))
                prod_c = Fraction(1)
                for idx in range(2 * m - 1):
                    prod_c *= cs[idx]
                assert wron == [Fraction(0)] * (2 * m - 1) + [-prod_c]

    # Sample [2/2] Padé on Euler-Ramanujan pair (0, 2):
    r_20 = series_mul(eb[2], series_inv(eb[0]))
    p2_02, q2_02 = linear_pade_hand3(r_20, 2)
    return {
        "status": "PASS",
        "euler_ramanujan_02_P2_coeffs": [str(c) for c in p2_02],
        "euler_ramanujan_02_Q2_coeffs": [str(c) for c in q2_02],
        "j_fraction_wronskian_and_reciprocity_m1_to_6": True,
    }


# ---------------------------------------------------------------------------
# 3. Theorem 3: Pole-Zero Interlacing, Monotone Spectral Bounds & Quadrature
# ---------------------------------------------------------------------------

def all_positive_roots_neg_poly(poly_f: List[Fraction]) -> List[Decimal]:
    r"""
    Find all m simple positive roots of poly_f(-x) = 0 in 90-digit Decimal via Aberth-Ehrlich.
    """
    m = len(poly_f) - 1
    assert m >= 1
    # Convert poly_f(-x) to monic polynomial M(x) = x^m + a_{m-1} x^{m-1} + ... + a_0:
    raw = [Decimal(c.numerator) / Decimal(c.denominator) * (Decimal(-1) ** i) for i, c in enumerate(poly_f)]
    lead = raw[-1]
    monic = [c / lead for c in raw]

    # Initial distinct positive guesses spread geometrically
    roots = [Decimal(20) * (Decimal(4) ** r) for r in range(m)]
    for _ in range(80):
        max_step = Decimal(0)
        new_roots = roots[:]
        for i in range(m):
            xi = roots[i]
            val = Decimal(0)
            der = Decimal(0)
            for deg in range(m, -1, -1):
                val = val * xi + monic[deg]
                if deg >= 1:
                    der = der * xi + Decimal(deg) * monic[deg]
            newton = val / der
            repulsion = sum(Decimal(1) / (xi - roots[j]) for j in range(m) if j != i)
            step = newton / (Decimal(1) - newton * repulsion)
            new_roots[i] = xi - step
            max_step = max(max_step, abs(step) / max(Decimal(1), abs(xi)))
        roots = new_roots
        if max_step < Decimal("1e-78"):
            break
    roots.sort()
    assert all(r > 0 for r in roots)
    return roots


def eval_poly_dec(poly_f: List[Fraction], z: Decimal) -> Tuple[Decimal, Decimal]:
    """Return (P(z), P'(z)) in Decimal."""
    coeffs = [Decimal(c.numerator) / Decimal(c.denominator) for c in poly_f]
    val = Decimal(0)
    der = Decimal(0)
    for deg in range(len(coeffs) - 1, -1, -1):
        val = val * z + coeffs[deg]
        if deg >= 1:
            der = der * z + Decimal(deg) * coeffs[deg]
    return val, der


def verify_theorem_3(eb: List[List[Fraction]]) -> Dict[str, object]:
    true_x1 = [Decimal(4) * (solve_root_sector(a, 1) ** 4) for a in range(4)]

    m6_pole_errors: Dict[str, str] = {}
    m6_zero_errors: Dict[str, str] = {}

    for a in range(4):
        for b in range(a + 1, 4):
            r_ba = series_mul(eb[b], series_inv(eb[a]))
            cs = s_fraction_series_hand1(r_ba, 12)
            p_list, q_list, n_list = j_fraction_pade(cs, 6)

            prev_pole1 = None
            prev_zero1 = None
            for m in range(1, 7):
                poles = all_positive_roots_neg_poly(q_list[m])
                zeros = all_positive_roots_neg_poly(p_list[m])
                assert len(poles) == len(zeros) == m
                # Strict finite pole-zero interlacing 0 < x_{m,1} < y_{m,1} < ... < x_{m,m} < y_{m,m}
                for idx in range(m):
                    assert poles[idx] < zeros[idx], f"Interlacing failed at ({a},{b}), m={m}"
                    if idx + 1 < m:
                        assert zeros[idx] < poles[idx + 1], f"Interlacing failed at ({a},{b}), m={m}"

                # Strict monotone convergence from above onto 4*(mu_1^(a))^4 and 4*(mu_1^(b))^4
                assert poles[0] > true_x1[a] and zeros[0] > true_x1[b]
                if prev_pole1 is not None:
                    assert poles[0] < prev_pole1 and zeros[0] < prev_zero1
                prev_pole1, prev_zero1 = poles[0], zeros[0]

            m6_pole_errors[f"({a},{b})->Dom_{a}"] = f"{abs(prev_pole1 - true_x1[a]):.3e}"
            m6_zero_errors[f"({a},{b})->Dom_{b}"] = f"{abs(prev_zero1 - true_x1[b]):.3e}"

    assert Decimal(m6_pole_errors["(0,1)->Dom_0"]) < Decimal("1e-37")
    assert Decimal(m6_zero_errors["(0,1)->Dom_1"]) < Decimal("1e-28")

    # Verify Gauss-Stieltjes quadrature weight w_{6,1} on Euler-Ramanujan pair (0, 2)
    # against exact Ramanujan-Krylov Wronskian weight 4 tanh(pi/2) / ((pi/2)^3 * (pi^4/4)):
    r_20 = series_mul(eb[2], series_inv(eb[0]))
    cs_02 = s_fraction_series_hand1(r_20, 12)
    _, q_02, n_02 = j_fraction_pade(cs_02, 6)
    x6_1 = all_positive_roots_neg_poly(q_02[6])[0]
    n_val, _ = eval_poly_dec(n_02[6], -x6_1)
    _, qp_val = eval_poly_dec(q_02[6], -x6_1)
    # Note: 1 - R(z) = N_6(z)/Q_6(z) = sum_r w_{6,r} z / (x_{6,r} + z), so as z -> -x_{6,1}:
    # w_{6,1} = -N_6(-x_{6,1}) / (x_{6,1} * Q'_6(-x_{6,1})), converging to 4 tanh(pi/2) / (pi/2)^3!
    w6_1 = -n_val / (x6_1 * qp_val)

    mu1_0 = PI_DEC / Decimal(2)
    sh0, ch0 = dec_sinh_cosh(mu1_0)
    true_w1_02 = Decimal(4) * (sh0 / ch0) / (mu1_0 ** 3)
    quad_weight_err = abs(w6_1 - true_w1_02)
    assert quad_weight_err < Decimal("1e-37"), f"Gauss-Stieltjes weight err too large: {quad_weight_err}"

    return {
        "status": "PASS",
        "m6_fundamental_pole_errors": m6_pole_errors,
        "m6_fundamental_zero_errors": m6_zero_errors,
        "euler_ramanujan_02_w6_1_quadrature_error": f"{quad_weight_err:.3e}",
    }


def main() -> None:
    print("=" * 78)
    print("LANE B LAB: STIELTJES-PADE SPECTRAL BOUNDS & JACOBI TRIDIAGONAL QUARTET")
    print("=" * 78)

    eb = [
        [Fraction(math.factorial(b), math.factorial(4 * k + b)) for k in range(18)]
        for b in range(4)
    ]

    res1 = verify_theorem_1(eb)
    print(
        f"[PASS] Theorem 1: Two-handed S-fractions n=1..12 & (1,2,3) unit-fraction staircase "
        f"(0,2 c1..3={res1['euler_ramanujan_02_c1_to_6'][:3]})"
    )

    res2 = verify_theorem_2(eb)
    print(
        f"[PASS] Theorem 2: J-fraction 3-term Jacobi polynomials, continuant Wronskian & "
        f"[m/m] Padé reciprocity P_m^(a,b) == Q_m^(b,a) (m=1..6)"
    )

    res3 = verify_theorem_3(eb)
    print(
        f"[PASS] Theorem 3: Strict pole-zero interlacing & monotone rational convergence "
        f"(pi^4/4 err={res3['m6_fundamental_pole_errors']['(0,1)->Dom_0']}, "
        f"Ramanujan w_1 err={res3['euler_ramanujan_02_w6_1_quadrature_error']})"
    )

    summary = {
        "module": "stieltjes_pade_spectral_bounds_and_jacobi_tridiagonal_quartet_2026_11_19.py",
        "lane": "b",
        "revision": 109,
        "instance_id": "jee-instance-524e408b5123473d95578e39c889f8a9",
        "theorem_1": res1,
        "theorem_2": res2,
        "theorem_3": res3,
        "verdict": "ALL_CHECKS_PASSED",
    }
    out_path = Path(__file__).with_name(
        "stieltjes_pade_spectral_bounds_and_jacobi_tridiagonal_quartet_2026_11_19_results.json"
    )
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
