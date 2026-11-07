#!/usr/bin/env python3
"""
1. Exact 1st- and 2nd-Order Edgeworth Expansions for m-Turn Run-Length Memory (sign, r_1, ..., r_m):
     p_hat_n(-, 1)    = 3/10 - 3/(175*(n-1)) + 2/(175*(n-1)^2) + O((n-1)^-3)
     p_hat_n(-, 1, 1) = 71/252 + 65/(21168*(n-2)) - 8497/(4074840*(n-2)^2) + O((n-2)^-3)
   (closing Row 5 and Row 6 of the §8 Coverage Matrix in PAPER_WORKING_DRAFT_v0.1.md).

2. Solution of Open Question §7.2: Sparre Andersen Universality and Exact Leading Constant C(tau, sigma)
   of the O(r^-2) Meander Decay:
     P(+ | tau '+'^r) - P(+ | sigma '+'^r) = C(tau, sigma) / r^2 + O(r^-3),
     C(tau, sigma) = (a_tau - a_sigma)/2 + mu_1(psi_sigma) - mu_1(psi_tau),
   where mu_1(psi) = <V_1, psi> / <V, psi> is the ratio of the subleading and leading Wiener-Hopf
   harmonic survival functionals on [0, 1].

Author: Den B (Ден Б, ompu-7f698bd908, stereo_v1/b, Google Antigravity)
Date: 2026-11-07 (Morning Tick 10:35 CET, in stereo duet with Jee A's 10:30 CET tick)
Standard library only (fractions, math, json, pathlib). Zero external dependencies.
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path


def comb(n: int, k: int) -> int:
    return math.comb(n, k)


def apply_turn_operator_poly(coeffs: list[F]) -> list[F]:
    """Exact polynomial action of (T f)(x) = int_0^{1-x} (1 - x - t) f(t) dt on [0, 1]."""
    d = len(coeffs) - 1
    out = [F(0)] * (d + 3)
    for k, c in enumerate(coeffs):
        factor = c / F((k + 1) * (k + 2))
        m = k + 2
        for j in range(m + 1):
            out[j] += factor * comb(m, j) * ((-1) ** j)
    return out


def irwin_hall_unit_poly(L: int) -> list[F]:
    """Exact polynomial density of unconditional T_L = sum_{i=1}^L Y_i on x in [0, 1]."""
    deg = 2 * L - 1
    coeffs = [F(0)] * (deg + 1)
    denom = math.factorial(deg)
    for k in range(L + 1):
        sign = -1 if (k % 2 == 1) else 1
        b_2L_k = comb(2 * L, k)
        shift = L - k
        for j in range(deg + 1):
            c_j = comb(deg, j) * (shift ** (deg - j))
            coeffs[j] += F(sign * b_2L_k * c_j, denom)
    return coeffs


def poly_moment(p: list[F], r: int = 0) -> F:
    """Exact integral int_0^1 x^r p(x) dx."""
    return sum(c / F(k + r + 1) for k, c in enumerate(p))


def shifted_legendre_poly(d: int) -> list[F]:
    """Exact polynomial coefficients of P_d^*(x) = P_d(2x - 1) on [0, 1]."""
    return [
        F((-1) ** (d + j) * comb(d, j) * comb(d + j, j))
        for j in range(d + 1)
    ]


def poly_inner_product(p: list[F], q: list[F]) -> F:
    total = F(0)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            if b != 0:
                total += a * b / F(i + j + 1)
    return total


def leg_int1(c: list[float], D: int) -> list[float]:
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


def leg_I2(c: list[float], D: int) -> list[float]:
    return leg_int1(leg_int1(c, D), D)


def leg_R(c: list[float]) -> list[float]:
    return [c[d] if d % 2 == 0 else -c[d] for d in range(len(c))]


def leg_T(c: list[float], D: int) -> list[float]:
    return leg_R(leg_I2(c, D))


def leg_R_I2_R(c: list[float], D: int) -> list[float]:
    return leg_R(leg_I2(leg_R(c), D))


def step_same(f: list[list[float]], D: int) -> list[list[float]]:
    m = len(f)
    f_new = [[0.0] * (D + 1) for _ in range(m + 1)]
    for j in range(m):
        c = f[j]
        i2 = leg_I2(c, D)
        ri2r = leg_R_I2_R(c, D)
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


def richardson_extrapolate(vals: list[float], ms: list[int]) -> float:
    hs = [1.0 / (2 * m + 2) for m in ms]
    T = [list(vals)]
    for k in range(1, len(ms)):
        row = []
        for i in range(len(ms) - k):
            val = (hs[i] * T[k - 1][i + 1] - hs[i + k] * T[k - 1][i]) / (hs[i] - hs[i + k])
            row.append(val)
        T.append(row)
    return T[-1][0]


def main():
    print("=== 1. EXACT 1ST- & 2ND-ORDER EDGEWORTH EXPANSIONS FOR m-TURN MEMORY p_hat_n(-, 1^m) ===")
    print("  Unconditional Irwin-Hall B-spline expansion on [0, 1] (L = n - m):")
    print("    F_0^{(L)}(x) / F_0^{(L)}(0) = 1 - (3/L)*x^2 + ((9/10)*x^2 + (9/2)*x^4)/L^2 + O(L^-3)\n")

    t_polys = [[F(1)]]
    for _ in range(7):
        t_polys.append(apply_turn_operator_poly(t_polys[-1]))

    f0_30 = irwin_hall_unit_poly(30)
    edgeworth_table = {}
    prev_c1 = None
    prev_c2 = None

    for m in range(1, 7):
        tm = t_polys[m]
        tm1 = t_polys[m + 1]
        I0_m, I2_m, I4_m = poly_moment(tm, 0), poly_moment(tm, 2), poly_moment(tm, 4)
        I0_m1, I2_m1, I4_m1 = poly_moment(tm1, 0), poly_moment(tm1, 2), poly_moment(tm1, 4)

        a1 = -3 * (I2_m1 / I0_m1)
        a2 = F(9, 10) * (I2_m1 / I0_m1) + F(9, 2) * (I4_m1 / I0_m1)
        b1 = -3 * (I2_m / I0_m)
        b2 = F(9, 10) * (I2_m / I0_m) + F(9, 2) * (I4_m / I0_m)

        lead = I0_m1 / I0_m
        c1 = lead * (a1 - b1)
        c2 = lead * (a2 - b2 - b1 * (a1 - b1))

        # Verify against exact Irwin-Hall B-spline at L = 30 (n = 30 + m):
        num_30 = sum(f0_30[j] * poly_moment(tm1, j) for j in range(len(f0_30)))
        den_30 = sum(f0_30[j] * poly_moment(tm, j) for j in range(len(f0_30)))
        exact_30 = num_30 / den_30
        err1_30 = float(abs(exact_30 - (lead + c1 / 30)))
        err2_30 = float(abs(exact_30 - (lead + c1 / 30 + c2 / 900)))

        r_c1 = float(prev_c1 / c1) if prev_c1 is not None else 0.0
        r_c2 = float(prev_c2 / c2) if prev_c2 is not None else 0.0
        prev_c1, prev_c2 = c1, c2

        edgeworth_table[m] = {
            "p_hat_inf_rational": str(lead),
            "p_hat_inf_float": float(lead),
            "c1_rational": str(c1),
            "c1_float": float(c1),
            "c2_rational": str(c2),
            "c2_float": float(c2),
            "c1_compression_ratio": r_c1,
            "c2_compression_ratio": r_c2,
            "L30_err_order1": err1_30,
            "L30_err_order2": err2_30,
        }
        print(
            f"  m={m}: p_hat_n(-, 1^{m}) = {lead} + ({c1})/(n-{m}) + ({c2})/(n-{m})^2\n"
            f"       float: {float(lead):.10f} + ({float(c1):+.10f})/L + ({float(c2):+.10f})/L^2\n"
            f"       ratios: c1_prev/c1 = {r_c1:+.4f}x, c2_prev/c2 = {r_c2:+.4f}x | L=30 err2 = {err2_30:.3e}"
        )

    assert edgeworth_table[1]["p_hat_inf_rational"] == "3/10"
    assert edgeworth_table[1]["c1_rational"] == "-3/175"
    assert edgeworth_table[1]["c2_rational"] == "2/175"
    assert edgeworth_table[2]["p_hat_inf_rational"] == "71/252"
    assert edgeworth_table[2]["c1_rational"] == "65/21168"
    assert edgeworth_table[2]["c2_rational"] == "-8497/4074840"

    print("\n=== 2. SOLUTION OF OPEN QUESTION §7.2: SPARRE ANDERSEN & WIENER-HOPF MEANDER PREFACTOR C(tau, sigma) ===")
    D = 14
    basis_states = {}
    for d in range(6):
        c = [0.0] * (D + 1)
        c[d] = 1.0
        basis_states[d] = [c]

    masses = {d: {} for d in range(6)}
    for m in range(1, 121):
        base_m = comb(2 * m, m) / (4.0 ** m)
        for d in range(6):
            masses[d][m] = sum(c[0] for c in basis_states[d]) / base_m
            if m < 120:
                basis_states[d] = step_same(basis_states[d], D)

    ms = [20, 40, 60, 90, 120]
    V_leg = []
    V1_leg = []
    print("  Shifted-Legendre moments of positive-half-line harmonic V(x) and subleading V_1(x):")
    for d in range(6):
        v_d = richardson_extrapolate([masses[d][m] for m in ms], ms)
        v1_d = richardson_extrapolate([m * (masses[d][m] - v_d) for m in ms], ms)
        V_leg.append(v_d)
        V1_leg.append(v1_d)
        print(f"    d={d}: <V, P_{d}*> = {v_d:+.12f},  <V_1, P_{d}*> = {v1_d:+.12f}")

    # Verify exact Sparre Andersen normalization on psi_0(x) = 1 - x = 0.5 P_0* - 0.5 P_1*:
    norm_V = 0.5 * V_leg[0] - 0.5 * V_leg[1]
    norm_V1 = 0.5 * V1_leg[0] - 0.5 * V1_leg[1]
    assert abs(norm_V - 1.0) < 1e-11
    assert abs(norm_V1) < 1e-11
    print(f"  Check Sparre Andersen baseline (psi_0 = 1-x): <V, 1-x> = {norm_V:.12f}, <V_1, 1-x> = {norm_V1:.3e}")

    # Compute mu_1(psi) = <V_1, psi> / <V, psi> and c_2(psi) = -1/2 + mu_1(psi) for k-turn profiles T^k f_1:
    f1 = [F(1), F(-1)]
    turn_profiles = [f1]
    for _ in range(1, 7):
        turn_profiles.append(apply_turn_operator_poly(turn_profiles[-1]))

    print("\n  Asymptotic flip expansion q_psi(m) = 1/(2m) + c_2(psi)/m^2 + O(m^-3), c_2(psi) = -1/2 + mu_1(psi):")
    mu1_turns = {}
    c2_turns = {}
    for k, p_poly in enumerate(turn_profiles):
        leg_coeffs = [
            float(poly_inner_product(p_poly, shifted_legendre_poly(d)) * F(2 * d + 1))
            for d in range(6)
        ]
        v_ip = sum(leg_coeffs[d] * V_leg[d] for d in range(6))
        v1_ip = sum(leg_coeffs[d] * V1_leg[d] for d in range(6))
        mu1 = v1_ip / v_ip
        c2 = -0.5 + mu1
        mu1_turns[k] = mu1
        c2_turns[k] = c2
        label = "pure (+)" if k == 0 else f"{k}-turn (T^{k} f_1)"
        print(f"    k={k} ({label:16s}): mu_1 = {mu1:+.12f},  c_2 = {c2:+.12f}")

    # Compute C(tau, sigma) for Petrovich's NOTE.txt pair (-+ +^r vs +- +^r) and same-run-length pairs:
    c_same_12 = mu1_turns[2] - mu1_turns[1]
    c_note_mp_pm = 0.5 + c_same_12
    c_same_23 = mu1_turns[3] - mu1_turns[2]
    c_same_34 = mu1_turns[4] - mu1_turns[3]
    c_same_45 = mu1_turns[5] - mu1_turns[4]

    print("\n  Explicit O(r^-2) prefactors C(tau, sigma) in P(+ | tau '+'^r) - P(+ | sigma '+'^r) = C / r^2 + O(r^-3):")
    print(f"    1) NOTE.txt pair (tau='-+', sigma='+-', Delta_m = 1): C('-+', '+-') = 1/2 + (mu_1(T^2 f_1) - mu_1(T f_1)) = {c_note_mp_pm:+.12f}")
    print(f"    2) Same-run-length 1-turn vs 2-turn (Delta_m = 0):    C_same(T f_1, T^2 f_1)  = {c_same_12:+.12f}")
    print(f"    3) Same-run-length 2-turn vs 3-turn (Delta_m = 0):    C_same(T^2 f_1, T^3 f_1)= {c_same_23:+.12f} (ratio {c_same_12 / c_same_23:+.4f}x)")
    print(f"    4) Same-run-length 3-turn vs 4-turn (Delta_m = 0):    C_same(T^3 f_1, T^4 f_1)= {c_same_34:+.12f} (ratio {c_same_23 / c_same_34:+.4f}x)")
    print(f"    5) Same-run-length 4-turn vs 5-turn (Delta_m = 0):    C_same(T^4 f_1, T^5 f_1)= {c_same_45:+.12f} (ratio {c_same_34 / c_same_45:+.4f}x)")

    out = {
        "author": "Den B (ompu-7f698bd908, stereo_v1/b, Google Antigravity)",
        "date": "2026-11-07",
        "edgeworth_m_turn_table": edgeworth_table,
        "wiener_hopf_harmonic_legendre_moments": {
            "V_P_d": V_leg,
            "V1_P_d": V1_leg,
        },
        "turn_profile_meander_constants": {
            f"k={k}": {"mu_1": mu1_turns[k], "c_2": c2_turns[k]} for k in range(7)
        },
        "C_prefactor_note_txt_mp_vs_pm": c_note_mp_pm,
        "C_prefactor_same_run_1_vs_2_turns": c_same_12,
        "C_prefactor_same_run_2_vs_3_turns": c_same_23,
        "C_prefactor_same_run_3_vs_4_turns": c_same_34,
        "C_prefactor_same_run_4_vs_5_turns": c_same_45,
    }
    Path(__file__).with_name("meander_prefactor_and_edgeworth2_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )


if __name__ == "__main__":
    main()
