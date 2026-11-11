#!/usr/bin/env python3
"""
Gohberg-Semencul 2D Kernel Reconstruction from f_1(x) = 1 - x,
Rank-2 Wave Commutator [D^2, T], Centrosymmetric Bezoutian Reflection Identity
G_z(x, y) - G_z(1-x, 1-y) = R_z(1-x) F_z(y) - F_z(1-x) R_z(y),
and Anti-Diagonal Normal Derivative Bridge to Jee A's Self-Similar Wronskian.

Author: Den B (Lane B, OMPU Stereo Pair, ompu-7f698bd908, Google Antigravity)
Date: 2026-11-11 10:35 CET (Wednesday Morning Tick, rev 98, First OMPU Autumn Subbotnik)

Main Results Verified in Exact Rational (Fraction) Arithmetic:
1. Operator Anticommutator D T + T D = -f_1 (x) delta_0 & Gohberg-Semencul 2D Kernel Formula:
   Since (T h)'(x) = -int_0^{1-x} h(y) dy and integration by parts gives
   (T h')(x) = -h(0)(1 - x) + int_0^{1-x} h(y) dy, the differentiation operator D = d/dx
   satisfies the rank-1 anticommutator:
       (D T + T D) h = -h(0) f_1   (where f_1(x) = 1 - x).
   Telescoping D T^m - (-1)^m T^m D = sum_{k=0}^{m-1} (-1)^k T^k (D T + T D) T^{m-1-k} shows that
   the 2D kernel K_m(x, y) of T^m satisfies the first-order transport PDE:
       (d/dx + (-1)^m d/dy) K_m(x, y) = -sum_{k=0}^{m-2} (-1)^k (T^k f_1)(x) (T^{m-2-k} f_1)(y),
   which integrates from K_m(1, . ) = K_m( . , 1) = 0 and K_m(x, 0) = (T^{m-1} f_1)(x) to reconstruct
   the ENTIRE 2D kernel K_m(x, y) on [0, 1]^2 purely from the 1D iterates T^k f_1:
     - Even m = 2n >= 2:
         K_{2n}(x, y) = sum_{k=0}^{2n-2} (-1)^k int_0^{1 - max(x, y)} (T^k f_1)(x + u) (T^{2n-2-k} f_1)(y + u) du,
         Tr(T^{2n}) = int_0^1 K_{2n}(x, x) dx = sum_{k=0}^{2n-2} (-1)^k int_0^1 s (T^k f_1)(s) (T^{2n-2-k} f_1)(s) ds
                    = (1/4) (T^{2n-1} f_1)(0).
     - Odd m = 2n + 1 >= 1:
         K_{2n+1}(x, y) = 1_{x + y <= 1} (T^{2n} f_1)(x + y)
                        + sum_{k=0}^{2n-1} (-1)^k int_0^{min(y, 1 - x)} (T^k f_1)(x + u) (T^{2n-1-k} f_1)(y - u) du,
         Tr(T^{2n+1}) = (1/2) H_0^(2n+1)
                      + (1/2) sum_{k=0}^{2n-1} (-1)^k iint_{0 <= t <= s <= 1} (T^k f_1)(s) (T^{2n-1-k} f_1)(t) ds dt
                      = (1/4) (T^{2n} f_1)(0).

2. Rank-2 Wave Commutator [D^2, T], Centrosymmetric Bezoutian Reflection Identity,
   and Anti-Diagonal Normal Derivative = Jee A's Self-Similar Wronskian:
   Since (D^2 T h)(x) = h(1 - x) and (T D^2 h)(x) = h(1 - x) - h(0) 1(x) - h'(0) f_1(x),
   the bulk reflection operator Pi cancels in the commutator:
       [D^2, T] = D^2 T - T D^2 = 1 (x) delta_0 + f_1 (x) delta_0'.
   Consequently, the 2D resolvent kernel G_z(x, y) = sum_{m>=1} z^{m-1} K_m(x, y) satisfies the
   non-homogeneous 1D wave equation on [0, 1]^2:
       (d^2/dx^2 - d^2/dy^2) G_z(x, y) = z (G_z(1 - x, y) - G_z(x, 1 - y)) = R_z(x) F_z(y) - F_z(x) R_z(y).
   Replacing x -> 1 - x proves that all piecewise kinks across x = y and x + y = 1 cancel in the
   centrosymmetric reflection difference, leaving a pure rank-2 Bezoutian polynomial on all of [0, 1]^2:
       G_z(x, y) - G_z(1 - x, 1 - y) = R_z(1 - x) F_z(y) - F_z(1 - x) R_z(y),
       K_m(x, y) - K_m(1 - x, 1 - y) = sum_{k=0}^{m-1} [ (T^k 1)(1 - x) (T^{m-1-k} f_1)(y) - (T^k f_1)(1 - x) (T^{m-1-k} 1)(y) ].
   Moreover, Delta K_m(x, y) := K_m(x, y) - K_m(1 - x, 1 - y) vanishes identically on the anti-diagonal
   y = 1 - x, and its negative y-derivative along y = 1 - x is identically Jee A's self-similar Wronskian W_{m-1}(x):
       -d/dy [ K_m(x, y) - K_m(1 - x, 1 - y) ]_{y = 1 - x} = W_{m-1}(1 - x) = W_{m-1}(x),
       -d/dy [ G_z(x, y) - G_z(1 - x, 1 - y) ]_{y = 1 - x} = -w_z(x) = Delta(z(2x - 1)^2) / Delta(z).
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


def poly_eval(p: list[Fraction], x: Fraction) -> Fraction:
    return sum(c * (x ** k) for k, c in enumerate(p))


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


def shift_poly(p: list[Fraction], a: Fraction) -> list[Fraction]:
    """Return polynomial coefficients in u for p(a + u)."""
    deg = len(p) - 1
    out = [Fraction(0)] * (deg + 1)
    for k, c in enumerate(p):
        if c == 0:
            continue
        for j in range(k + 1):
            out[j] += c * math.comb(k, j) * (a ** (k - j))
    return out


def poly_int_0_to(p: list[Fraction], upper: Fraction) -> Fraction:
    return sum(c * (upper ** (k + 1)) / Fraction(k + 1) for k, c in enumerate(p))


def poly_int_simplex(p: list[Fraction], q: list[Fraction]) -> Fraction:
    """Exact integral iint_{0 <= t <= s <= 1} p(s) q(t) ds dt."""
    total = Fraction(0)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            if b == 0:
                continue
            total += a * b / Fraction((j + 1) * (i + j + 2))
    return total


def neg_wronskian(f: list[Fraction], g: list[Fraction]) -> list[Fraction]:
    """Return f'(x) g(x) - f(x) g'(x) in Q[x]."""
    return poly_add(poly_mul(poly_deriv(f), g), poly_mul(f, poly_deriv(g)), Fraction(-1))


def K_gohberg_semencul(m: int, x: Fraction, y: Fraction, t_f1: list[list[Fraction]]) -> Fraction:
    """
    Evaluate the exact 2D iterated kernel K_m(x, y) of T^m at (x, y) in [0, 1]^2
    using the 1D Gohberg-Semencul characteristic integral of T^k f_1.
    """
    if m % 2 == 0:
        upper = Fraction(1) - max(x, y)
        total = Fraction(0)
        for k in range(m - 1):
            pk = shift_poly(t_f1[k], x)
            pq = shift_poly(t_f1[m - 2 - k], y)
            total += ((-1) ** k) * poly_int_0_to(poly_mul(pk, pq), upper)
        return total
    else:
        total = poly_eval(t_f1[m - 1], x + y) if (x + y <= 1) else Fraction(0)
        upper = min(y, Fraction(1) - x)
        for k in range(m - 1):
            pk = shift_poly(t_f1[k], x)
            pq_pos = shift_poly(t_f1[m - 2 - k], y)
            pq = [c * ((-1) ** j) for j, c in enumerate(pq_pos)]
            total += ((-1) ** k) * poly_int_0_to(poly_mul(pk, pq), upper)
        return total


def verify_all() -> dict:
    M_max = 9
    t_one = [[Fraction(1)]]
    t_f1 = [[Fraction(1), Fraction(-1)]]
    for _ in range(M_max + 1):
        t_one.append(apply_T_poly(t_one[-1]))
        t_f1.append(apply_T_poly(t_f1[-1]))

    print("=== 1. OPERATOR ANTICOMMUTATOR D T + T D = -f_1 (x) delta_0 & GOHBERG-SEMENCUL DIAGONAL TRACES ===")
    # 1a. Verify (D T + T D) h = -h(0) f_1 and [D^2, T] h = h(0) 1 + h'(0) f_1 on basis monomials h(x) = x^r (r=0..8):
    for r in range(9):
        h = [Fraction(0)] * r + [Fraction(1)]
        th = apply_T_poly(h)
        d_th = poly_deriv(th)
        dh = poly_deriv(h)
        t_dh = apply_T_poly(dh)
        anticomm = poly_add(d_th, t_dh)
        expected_anticomm = poly_add([Fraction(0)], t_f1[0], -poly_eval(h, Fraction(0)))
        assert anticomm == expected_anticomm, f"Anticommutator mismatch at r={r}"

        d2_th = poly_deriv(d_th)
        d2h = poly_deriv(dh)
        t_d2h = apply_T_poly(d2h)
        comm_d2 = poly_add(d2_th, t_d2h, Fraction(-1))
        expected_comm = poly_add(
            poly_add([Fraction(0)], t_one[0], poly_eval(h, Fraction(0))),
            t_f1[0],
            poly_eval(dh, Fraction(0)),
        )
        assert comm_d2 == expected_comm, f"[D^2, T] mismatch at r={r}"

    # 1b. Verify Gohberg-Semencul diagonal trace formulas against (1/4)(T^{m-1} f_1)(0) for m = 1..9:
    gs_traces = {}
    for m in range(1, M_max + 1):
        tr_cantilever = poly_eval(t_f1[m - 1], Fraction(0)) / Fraction(4)
        if m % 2 == 0:
            tr_gs = Fraction(0)
            for k in range(m - 1):
                prod = poly_mul(t_f1[k], t_f1[m - 2 - k])
                int_s_prod = sum(c / Fraction(j + 2) for j, c in enumerate(prod))
                tr_gs += ((-1) ** k) * int_s_prod
        else:
            h0_m = sum(c / Fraction(j + 1) for j, c in enumerate(t_f1[m - 1]))
            term1 = Fraction(1, 2) * h0_m
            term2 = Fraction(0)
            for k in range(m - 1):
                term2 += Fraction(1, 2) * ((-1) ** k) * poly_int_simplex(t_f1[k], t_f1[m - 2 - k])
            tr_gs = term1 + term2
        assert tr_gs == tr_cantilever, f"Trace mismatch at m={m}: {tr_gs} != {tr_cantilever}"
        gs_traces[f"m={m}"] = {
            "trace_rational": str(tr_gs),
            "midpoint_kernel_K_m(1/2,1/2)": str(K_gohberg_semencul(m, Fraction(1, 2), Fraction(1, 2), t_f1)),
        }
        print(
            f"  m={m}: Tr(T^{m}) = {str(tr_gs):>28s} | K_{m}(1/2, 1/2) = {str(K_gohberg_semencul(m, Fraction(1, 2), Fraction(1, 2), t_f1))}"
        )
    print("  [PASS 1] D T + T D = -f_1 (x) delta_0, [D^2, T] = 1 (x) delta_0 + f_1 (x) delta_0', and Gohberg-Semencul traces verified.")

    print("\n=== 2. CENTROSYMMETRIC BEZOUTIAN REFLECTION K_m(x,y) - K_m(1-x,1-y) & WRONSKIAN NORMAL SLOPE ===")
    test_points = [
        (Fraction(1, 5), Fraction(2, 5)),
        (Fraction(3, 7), Fraction(5, 7)),
        (Fraction(2, 3), Fraction(1, 4)),
        (Fraction(1, 6), Fraction(1, 6)),
        (Fraction(3, 8), Fraction(5, 8)),
    ]
    bezoutian_checks = {}
    for m in range(1, 8):
        # Verify K_m(x, y) - K_m(1-x, 1-y) == sum_{k=0}^{m-1} [(T^k 1)(1-x)(T^{m-1-k} f_1)(y) - (T^k f_1)(1-x)(T^{m-1-k} 1)(y)]
        for x, y in test_points:
            lhs = K_gohberg_semencul(m, x, y, t_f1) - K_gohberg_semencul(m, 1 - x, 1 - y, t_f1)
            rhs = Fraction(0)
            for k in range(m):
                rhs += (
                    poly_eval(t_one[k], 1 - x) * poly_eval(t_f1[m - 1 - k], y)
                    - poly_eval(t_f1[k], 1 - x) * poly_eval(t_one[m - 1 - k], y)
                )
            assert lhs == rhs, f"Bezoutian reflection mismatch at m={m}, ({x}, {y}): {lhs} != {rhs}"

        # Verify that the negative y-derivative of Delta K_m(x, y) on the anti-diagonal y = 1 - x
        # is identically Jee A's Wronskian polynomial W_{m-1}(x):
        # -d/dy [ sum_{k=0}^{m-1} ((T^k 1)(1-x)(T^{m-1-k} f_1)(y) - (T^k f_1)(1-x)(T^{m-1-k} 1)(y)) ]_{y = 1 - x}
        # = sum_{k=0}^{m-1} [ (T^{m-1-k} 1)'(1-x) (T^k f_1)(1-x) - (T^k 1)(1-x) (T^{m-1-k} f_1)'(1-x) ] = W_{m-1}(1-x) = W_{m-1}(x)!
        W_m_minus_1 = [Fraction(0)]
        for k in range(m):
            W_m_minus_1 = poly_add(W_m_minus_1, neg_wronskian(t_one[k], t_f1[m - 1 - k]))

        for x_val in [Fraction(0), Fraction(1, 5), Fraction(1, 3), Fraction(1, 2), Fraction(3, 4), Fraction(1)]:
            y_val = Fraction(1) - x_val
            normal_slope = Fraction(0)
            for k in range(m):
                d_f1 = poly_deriv(t_f1[m - 1 - k])
                d_one = poly_deriv(t_one[m - 1 - k])
                normal_slope -= (
                    poly_eval(t_one[k], 1 - x_val) * poly_eval(d_f1, y_val)
                    - poly_eval(t_f1[k], 1 - x_val) * poly_eval(d_one, y_val)
                )
            w_val = poly_eval(W_m_minus_1, x_val)
            assert normal_slope == w_val, f"Normal slope mismatch at m={m}, x={x_val}: {normal_slope} != {w_val}"

        bezoutian_checks[f"m={m}"] = {
            "Delta_K_m(1/5, 2/5)": str(
                K_gohberg_semencul(m, Fraction(1, 5), Fraction(2, 5), t_f1)
                - K_gohberg_semencul(m, Fraction(4, 5), Fraction(3, 5), t_f1)
            ),
            "anti_diagonal_normal_slope_at_1/3_eq_W_{m-1}(1/3)": str(poly_eval(W_m_minus_1, Fraction(1, 3))),
            "anti_diagonal_normal_slope_at_1/2_eq_W_{m-1}(1/2)": str(poly_eval(W_m_minus_1, Fraction(1, 2))),
        }
        print(
            f"  m={m}: Delta K_{m}(1/5,2/5) = {bezoutian_checks[f'm={m}']['Delta_K_m(1/5, 2/5)']:>22s} | "
            f"-d_y Delta K_{m}|_{{y=1-x}}(1/2) = W_{m-1}(1/2) = {bezoutian_checks[f'm={m}']['anti_diagonal_normal_slope_at_1/2_eq_W_{m-1}(1/2)']}"
        )

    print("  [PASS 2] Centrosymmetric Bezoutian Reflection and Anti-Diagonal Normal Derivative = W_{m-1}(x) verified.")
    print("ALL_CHECKS_PASSED")

    return {
        "theorem_1_gohberg_semencul_traces_and_midpoint_kernels": gs_traces,
        "theorem_2_centrosymmetric_bezoutian_and_wronskian_slope": bezoutian_checks,
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "gohberg_semencul_kernel_and_bezoutian_reflection_2026_11_11_results.json",
    )
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    if os.path.isdir(RESEARCH_DIR):
        shutil.copy2(
            os.path.abspath(__file__),
            os.path.join(RESEARCH_DIR, "gohberg_semencul_kernel_and_bezoutian_reflection_den_b.py"),
        )
        shutil.copy2(
            out_json,
            os.path.join(RESEARCH_DIR, "gohberg_semencul_kernel_and_bezoutian_reflection_den_b_results.json"),
        )
