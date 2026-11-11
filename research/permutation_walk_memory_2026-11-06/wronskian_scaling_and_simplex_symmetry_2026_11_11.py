#!/usr/bin/env python3
"""
Exact Self-Similar Wronskian Scaling Law -w_z(x) = Delta(z(2x-1)^2) / Delta(z),
Simplex Exchange Proof of the Integral Identity int_0^1 (-w_z(x)) dx = I_z,
and Monomial Wronskian Convolution Theorem for Turn Iterates T^k(1) and T^k(f_1).

Author: Jee A (Lane A, OMPU Stereo Pair, ompu-d6a8af238c)
Date: 2026-11-11 10:30 CET (Wednesday Morning Tick, rev 98, First OMPU Autumn Subbotnik)

Main Results Verified in Exact Rational (Fraction) Arithmetic:
1. Self-Similar Wronskian Scaling Law Across [0, 1]:
   For the midpoint resolvents R_z(x) = ((I - z T)^{-1} 1)(x) and F_z(x) = ((I - z T)^{-1} f_1)(x),
   their Wronskian w_z(x) := R_z(x) F_z'(x) - R_z'(x) F_z(x) is a scaled copy of the Fredholm
   determinant Delta(z) = det(I - z T) = cosh(sqrt(z)/2)cos(sqrt(z)/2) - sinh(sqrt(z)/2)sin(sqrt(z)/2):
       -w_z(x) = R_z'(x) F_z(x) - R_z(x) F_z'(x) = Delta( z * (2x - 1)^2 ) / Delta(z)   for ALL x in [0, 1].
   Specializing this single identity recovers:
     - Endpoints x = 0, 1 ((2x-1)^2 = 1): -w_z(0) = -w_z(1) = 1 <=> H_z(0)^2 - 4 z I_z Theta_z = 1
       (Petrovich's conservation law of the three generators).
     - Midpoint x = 1/2 (2x-1 = 0): -w_z(1/2) = 1 / Delta(z) = det(I - z T)^{-1}.

2. Three-Line Simplex Symmetry Proof of the Integral Identity int_0^1 (-w_z(x)) dx = I_z:
   Since F_z'(x) = -1 - z int_0^{1-x} F_z(y) dy and R_z'(x) = -z int_0^{1-x} R_z(y) dy,
       int_0^1 (-w_z(x)) dx = int_0^1 R_z(x) dx
                              - z iint_{x+y <= 1} [ F_z(x) R_z(y) - R_z(x) F_z(y) ] dx dy
                            = int_0^1 R_z(x) dx = I_z,
   because the simplex {(x, y) in [0, 1]^2 : x + y <= 1} is invariant under x <-> y!
   Integrating the scaling law -w_z(x) = Delta(z(2x-1)^2) / Delta(z) over x in [0, 1] immediately
   yields the Tuesday evening unit-fraction integral formula I_z = int_0^1 Delta(z u^2) du / Delta(z)
   = -4 Delta'(-z) / Delta(z) (Wick duality).

3. Exact Monomial Wronskian Convolution Theorem for Polynomial Iterates:
   Let W_m(x) := sum_{k=0}^m [ (T^k 1)'(x) (T^{m-k} f_1)(x) - (T^k 1)(x) (T^{m-k} f_1)'(x) ].
   Then for all m >= 0:
     (a) int_0^1 W_m(x) dx = I_0^(m) = int_0^1 (T^m 1)(x) dx,
     (b) sum_{j=0}^m [ (-1)^{floor((j+1)/2)} / (2^j (2j)!) ] * W_{m-j}(x)
             = [ (-1)^{floor((m+1)/2)} / (2^m (2m)!) ] * (2x - 1)^{2m}   (identically in Q[x]),
     (c) For every p >= 0,
         sum_{j=0}^m [ (-1)^{floor((j+1)/2)} / (2^j (2j)!) ] * int_0^1 (2x - 1)^{2p} W_{m-j}(x) dx
             = (-1)^{floor((m+1)/2)} / [ 2^m (2m)! (2m + 2p + 1) ].
"""

from fractions import Fraction
import json
import math
import os
import shutil


RESEARCH_DIR = "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06"


def apply_T_poly(poly: list[Fraction]) -> list[Fraction]:
    """Apply (T h)(x) = int_0^{1-x} (1 - x - y) h(y) dy in exact Fraction arithmetic."""
    deg = len(poly) - 1
    out = [Fraction(0)] * (deg + 3)
    for j, c in enumerate(poly):
        if c == 0:
            continue
        n = j + 2
        cv = c * Fraction(1, (j + 1) * (j + 2))
        for r in range(n + 1):
            out[r] += cv * math.comb(n, r) * ((-1) ** r)
    return out


def poly_deriv(p: list[Fraction]) -> list[Fraction]:
    return [c * j for j, c in enumerate(p) if j >= 1] or [Fraction(0)]


def poly_mul(p: list[Fraction], q: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            out[i + j] += a * b
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(p: list[Fraction], q: list[Fraction], scale_q: Fraction = Fraction(1)) -> list[Fraction]:
    out = [Fraction(0)] * max(len(p), len(q))
    for i, a in enumerate(p):
        out[i] += a
    for i, b in enumerate(q):
        out[i] += scale_q * b
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_int(p: list[Fraction]) -> Fraction:
    return sum(c / Fraction(k + 1) for k, c in enumerate(p))


def poly_eval(p: list[Fraction], x: Fraction) -> Fraction:
    return sum(c * (x ** k) for k, c in enumerate(p))


def neg_wronskian(f: list[Fraction], g: list[Fraction]) -> list[Fraction]:
    """Compute f'(x) g(x) - f(x) g'(x) in Q[x]."""
    return poly_add(poly_mul(poly_deriv(f), g), poly_mul(f, poly_deriv(g)), Fraction(-1))


def centered_even_power(two_m: int) -> list[Fraction]:
    """Return the exact polynomial (2x - 1)^{2m} in Q[x]."""
    out = [Fraction(0)] * (two_m + 1)
    for r in range(two_m + 1):
        out[r] = Fraction(math.comb(two_m, r) * (2 ** r) * ((-1) ** (two_m - r)))
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def verify_all() -> dict:
    M_max = 8
    t_one = [[Fraction(1)]]
    t_f1 = [[Fraction(1), Fraction(-1)]]
    for _ in range(M_max):
        t_one.append(apply_T_poly(t_one[-1]))
        t_f1.append(apply_T_poly(t_f1[-1]))

    delta_c = [
        Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m))
        for m in range(M_max + 1)
    ]

    # Compute W_m(x) = [z^m] (-w_z(x)) = sum_{k=0}^m ( (T^k 1)' (T^{m-k} f_1) - (T^k 1) (T^{m-k} f_1)' )
    W_polys = []
    wronskian_summary = {}
    for m in range(M_max + 1):
        cur = [Fraction(0)]
        for k in range(m + 1):
            cur = poly_add(cur, neg_wronskian(t_one[k], t_f1[m - k]))
        W_polys.append(cur)

        # 1. Check endpoint conservation: W_0(0)=W_0(1)=1, and W_m(0)=W_m(1)=0 for all m >= 1
        w_at_0 = poly_eval(cur, Fraction(0))
        w_at_1 = poly_eval(cur, Fraction(1))
        w_at_half = poly_eval(cur, Fraction(1, 2))
        expected_end = Fraction(1) if m == 0 else Fraction(0)
        assert w_at_0 == expected_end and w_at_1 == expected_end

        # 2. Check simplex symmetry integral identity: int_0^1 W_m(x) dx == I_0^(m) == int_0^1 (T^m 1)(x) dx
        int_w = poly_int(cur)
        i0_m = poly_int(t_one[m])
        assert int_w == i0_m, f"Integral mismatch at m={m}: {int_w} != {i0_m}"

        # 3. Check exact polynomial scaling identity:
        # sum_{j=0}^m delta_c[j] * W_{m-j}(x) == delta_c[m] * (2x - 1)^{2m}
        lhs_poly = [Fraction(0)]
        for j in range(m + 1):
            lhs_poly = poly_add(lhs_poly, W_polys[m - j], delta_c[j])
        rhs_poly = poly_add([Fraction(0)], centered_even_power(2 * m), delta_c[m])
        assert lhs_poly == rhs_poly, f"Polynomial mismatch at m={m}: {lhs_poly} != {rhs_poly}"

        # 4. Check generalized weighted Wronskian moments for p = 0, 1, 2:
        for p in range(3):
            weight_poly = centered_even_power(2 * p)
            lhs_mom = sum(
                delta_c[j] * poly_int(poly_mul(weight_poly, W_polys[m - j]))
                for j in range(m + 1)
            )
            rhs_mom = delta_c[m] / Fraction(2 * m + 2 * p + 1)
            assert lhs_mom == rhs_mom

        wronskian_summary[f"m={m}"] = {
            "deg_W_m": len(cur) - 1,
            "int_0_1_W_m_eq_I0_m": str(int_w),
            "W_m_at_half": str(w_at_half),
            "W_m_at_0_and_1": str(w_at_0),
            "delta_convolved_monomial_coeff": str(delta_c[m]),
        }

    # Check midpoint values W_m(1/2) match [z^m] (1 / Delta(z)):
    inv_delta = [Fraction(0)] * (M_max + 1)
    inv_delta[0] = Fraction(1)
    for m in range(1, M_max + 1):
        inv_delta[m] = -sum(delta_c[j] * inv_delta[m - j] for j in range(1, m + 1))
        assert poly_eval(W_polys[m], Fraction(1, 2)) == inv_delta[m]

    print("=== SELF-SIMILAR WRONSKIAN SCALING & SIMPLEX SYMMETRY VERIFICATION ===")
    for m in range(1, M_max + 1):
        print(
            f"  m={m}: int_0^1 W_{m}(x) dx = {str(poly_int(W_polys[m])):>26s} == I_0^({m}) | "
            f"W_{m}(1/2) = [z^{m}](1/Delta(z)) = {str(inv_delta[m]):>24s}"
        )
    print("ALL_CHECKS_PASSED")

    return {
        "wronskian_scaling_and_moments_m_0_to_8": wronskian_summary,
        "midpoint_inverse_fredholm_coeffs_m_0_to_8": {f"m={m}": str(inv_delta[m]) for m in range(M_max + 1)},
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "wronskian_scaling_and_simplex_symmetry_2026_11_11_results.json",
    )
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    if os.path.isdir(RESEARCH_DIR):
        shutil.copy2(
            os.path.abspath(__file__),
            os.path.join(RESEARCH_DIR, "wronskian_scaling_and_simplex_symmetry_2026_11_11.py"),
        )
        shutil.copy2(
            out_json,
            os.path.join(RESEARCH_DIR, "wronskian_scaling_and_simplex_symmetry_2026_11_11_results.json"),
        )
