#!/usr/bin/env python3
"""
Reproducible verification suite (pure Python stdlib, 0 external dependencies)
for the OMPU working paper:
"Same Count, Different History: Hidden-Height Operators, Shifted Legendre Horizons,
and Euler–Bernoulli Cantilever Spectra in Permutation Random Walks (v0.1-wip)"
Date: 2026-11-06
"""
import math
from fractions import Fraction


def comb(n: int, k: int) -> int:
    return math.comb(n, k)


def multinomial(n: int, parts: list[int]) -> int:
    assert sum(parts) == n
    res = 1
    rem = n
    for p in parts:
        res *= math.comb(rem, p)
        rem -= p
    return res


def verify_macmahon_theorem_1():
    """Theorem 1: Direct combinatorial proof of P(+ | +-) = 13/45 vs P(+ | -+) = 32/45."""
    # Ribbon inclusion-exclusion for descent set D = {2, 3} in S_6 (ribbons (2, 1, 3)):
    n = 6
    c_213 = multinomial(n, [2, 1, 3])
    c_24 = multinomial(n, [2, 4])
    c_33 = multinomial(n, [3, 3])
    c_6 = multinomial(n, [6])
    count_pm_plus = c_213 - c_24 - c_33 + c_6
    assert (c_213, c_24, c_33, c_6) == (60, 15, 20, 1)
    assert count_pm_plus == 26
    p_pm_plus = Fraction(count_pm_plus, 90)
    p_mp_plus = Fraction(90 - count_pm_plus, 90)
    assert p_pm_plus == Fraction(13, 45)
    assert p_mp_plus == Fraction(32, 45)
    return {
        "ribbons_inclusion_exclusion": f"{c_213} - {c_24} - {c_33} + {c_6} = {count_pm_plus}",
        "P(+ | +-)": str(p_pm_plus),
        "P(+ | -+)": str(p_mp_plus),
    }


def apply_turn_operator_poly(coeffs: list[Fraction]) -> list[Fraction]:
    """
    Exact polynomial action of (T f)(x) = int_0^{1-x} (1 - x - t) f(t) dt
    where f(t) = sum_{k=0}^d coeffs[k] t^k.
    Since (T f)''(x) = f(1 - x) with (T f)(1) = (T f)'(1) = 0,
    writing u = 1 - x gives g(u) = (T f)(1 - u), g''(u) = f(u), g(0) = g'(0) = 0.
    """
    # Step 1: expand f(u) = f(1 - (1 - u)) in powers of u = 1 - x:
    d = len(coeffs) - 1
    f_in_u = [Fraction(0)] * (d + 1)
    for k, c in enumerate(coeffs):
        # t^k = (1 - v)^k where v = 1 - t; here u = 1 - x, and we integrate t from 0 to u:
        # Wait: g(u) = int_0^u (u - t) f(t) dt directly in u!
        # Because for t in [0, u], int_0^u (u - t) t^k dt = u^{k+2} / ((k+1)(k+2))!
        pass
    # By substitution u = 1 - x, g(u) = int_0^u (u - t) f(t) dt = sum_k c_k u^{k+2} / ((k+1)(k+2)).
    # Then (T f)(x) = g(1 - x) = sum_k [c_k / ((k+1)(k+2))] (1 - x)^{k+2}.
    out = [Fraction(0)] * (d + 3)
    for k, c in enumerate(coeffs):
        factor = c / Fraction((k + 1) * (k + 2))
        m = k + 2
        for j in range(m + 1):
            term = factor * comb(m, j) * ((-1) ** j)
            out[j] += term
    return out


def verify_alternating_operator_theorem_2():
    """Theorem 2: Differential-reflection operator f_n''(v) = f_{n-1}(1 - v) for +-+-..."""
    # At n = 1 (single '+'): f_1(x) = 1 - x on [0, 1] (mass 1/2).
    f = [Fraction(1), Fraction(-1)]
    masses = [sum(c / Fraction(k + 1) for k, c in enumerate(f))]
    for _ in range(2, 7):
        f = apply_turn_operator_poly(f)
        masses.append(sum(c / Fraction(k + 1) for k, c in enumerate(f)))
    # Check n=3 (+-+): mass = 26 / 720 = 13 / 360
    assert masses[2] == Fraction(26, 720)
    # Check n=6 (+-+-+-): mass = 397023 / 479001600 = 12031 / 14515200
    assert masses[5] == Fraction(397023, math.factorial(12))
    return {
        "n=1..6_alternating_probabilities": [str(m) for m in masses],
        "n=6_permutation_count_out_of_12!": int(masses[5] * math.factorial(12)),
    }


def shifted_legendre_poly(d: int) -> list[Fraction]:
    """Exact polynomial coefficients of P_d^*(x) = P_d(2x - 1) on [0, 1]."""
    return [
        Fraction((-1) ** (d + j) * comb(d, j) * comb(d + j, j))
        for j in range(d + 1)
    ]


def poly_inner_product(p: list[Fraction], q: list[Fraction]) -> Fraction:
    """Exact L^2([0, 1]) inner product int_0^1 p(x) q(x) dx."""
    total = Fraction(0)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            if b != 0:
                total += a * b / Fraction(i + j + 1)
    return total


def project_shifted_legendre(p: list[Fraction], deg_d: int) -> list[Fraction]:
    """Exact orthogonal L^2([0, 1]) projection Pi_D(p) onto polynomials of degree <= deg_d."""
    out = [Fraction(0)] * (deg_d + 1)
    for d in range(deg_d + 1):
        pd = shifted_legendre_poly(d)
        coeff = poly_inner_product(p, pd) * Fraction(2 * d + 1)
        for j, c in enumerate(pd):
            out[j] += coeff * c
    return out


def flip_probability(p: list[Fraction]) -> Fraction:
    """Exact conditional flip probability int_0^1 0.5*(1-x)^2 p(x) dx / int_0^1 p(x) dx."""
    g0 = [Fraction(1, 2), Fraction(-1), Fraction(1, 2)]
    mass = sum(c / Fraction(k + 1) for k, c in enumerate(p))
    return poly_inner_product(g0, p) / mass


def verify_legendre_horizon_theorem_3():
    """
    Theorem 3 (Petrovich / Antigravity):
    (a) Single-shot projection Pi_D with D = 2m gives exact 0 error on m-step horizon for arbitrary f_k.
    (b) Streaming projection from f_1(x) = 1 - x gives exact 0 error for all trajectory lengths n <= D.
    """
    # (a) Arbitrary degree-7 polynomial density f_k on [0, 1]:
    f_arb = [Fraction(1, k + 1) for k in range(8)]
    single_shot_errors = {}
    for m in (1, 2, 3):
        deg_d = 2 * m
        f_proj = project_shifted_legendre(f_arb, deg_d)
        exact_cur, proj_cur = f_arb, f_proj
        for _ in range(m - 1):
            exact_cur = apply_turn_operator_poly(exact_cur)
            proj_cur = apply_turn_operator_poly(proj_cur)
        g0 = [Fraction(1, 2), Fraction(-1), Fraction(1, 2)]
        err_moment = poly_inner_product(g0, exact_cur) - poly_inner_product(g0, proj_cur)
        assert err_moment == Fraction(0)
        single_shot_errors[f"m={m}_D={deg_d}"] = str(err_moment)

    # (b) Streaming projection from f_1(x) = 1 - x for D = 1..6:
    # Exact unit-fraction identity (Petrovich 11:25 CET):
    # p_{D+1}^{exact} - p_{D+1}^{stream} = 1 / [2 * (2D + 3) * C(2D + 2, D + 1) * A_{D+1}]
    streaming_summary = {}
    for deg_d in range(1, 7):
        f_exact = [Fraction(1), Fraction(-1)]
        f_stream = project_shifted_legendre(f_exact, deg_d)
        for n in range(1, deg_d + 2):
            err = flip_probability(f_exact) - flip_probability(f_stream)
            if n <= deg_d:
                assert err == Fraction(0), f"Expected 0 error for n={n} <= D={deg_d}"
            else:
                mass_d_plus_1 = sum(c / Fraction(k + 1) for k, c in enumerate(f_exact))
                a_d_plus_1 = int(mass_d_plus_1 * math.factorial(2 * deg_d + 2))
                denom = 2 * (2 * deg_d + 3) * comb(2 * deg_d + 2, deg_d + 1) * a_d_plus_1
                assert err == Fraction(1, denom)
                streaming_summary[f"D={deg_d}_n={n}"] = f"1/{denom} (A_{deg_d+1}={a_d_plus_1})"
            f_exact = apply_turn_operator_poly(f_exact)
            f_stream = project_shifted_legendre(apply_turn_operator_poly(f_stream), deg_d)

    return {
        "single_shot_exact_horizon_D_eq_2m": single_shot_errors,
        "streaming_unit_fraction_identity_D_1_to_6": streaming_summary,
    }


def verify_cantilever_spectrum_theorem_4():
    """Theorem 4 (Jee A): Euler–Bernoulli cantilever roots cosh(k)cos(k) = -1 and turn compression."""
    def f(k: float) -> float:
        return math.cosh(k) * math.cos(k) + 1.0

    roots = []
    brackets = [(1.5, 2.2), (4.4, 5.0), (7.5, 8.1)]
    for a, b in brackets:
        fa = f(a)
        for _ in range(80):
            mid = 0.5 * (a + b)
            fm = f(mid)
            if fa * fm <= 0:
                b = mid
            else:
                a, fa = mid, fm
        roots.append(0.5 * (a + b))

    k1, k2, k3 = roots
    lam1 = 1.0 / (k1 ** 2)
    lam2 = -1.0 / (k2 ** 2)
    lam3 = 1.0 / (k3 ** 2)
    rho_turn = (k2 / k1) ** 2

    # Compare with exact rational power iteration of T on [0, 1]:
    v = [Fraction(1), Fraction(-1)]
    for _ in range(12):
        v = apply_turn_operator_poly(v)
    v_next = apply_turn_operator_poly(v)
    m_v = sum(c / Fraction(k + 1) for k, c in enumerate(v))
    m_next = sum(c / Fraction(k + 1) for k, c in enumerate(v_next))
    rayleigh = float(m_next / m_v)
    assert abs(rayleigh - lam1) < 1e-9

    return {
        "kappa_1_2_3": [round(r, 12) for r in roots],
        "lambda_1_2_3": [round(lam1, 12), round(lam2, 12), round(lam3, 12)],
        "rho_turn_compression": round(rho_turn, 12),
    }


def verify_edgeworth_asymptotics_theorem_5():
    """
    Theorem 5 (Den B & Jee A):
    - m-turn Bayesian cell limits p_hat_inf(-, 1^m) = 3/10, 71/252, 182/639, 45541/160160, ...
    - 1st- and 2nd-order Edgeworth expansions: p_hat_n(-, 1) = 3/10 - 3/(175*(n-1)) + 2/(175*(n-1)^2) + O((n-1)^-3).
    """
    # Compute T^m(1) for m = 1..7
    tm = [[Fraction(1)]]
    for _ in range(7):
        tm.append(apply_turn_operator_poly(tm[-1]))

    def moment(p: list[Fraction], power: int) -> Fraction:
        return sum(c / Fraction(k + power + 1) for k, c in enumerate(p))

    m_turn_limits = {}
    edgeworth_coeffs = {}
    for m in range(1, 7):
        i0_den = moment(tm[m], 0)
        i2_den = moment(tm[m], 2)
        i4_den = moment(tm[m], 4)
        i0_num = moment(tm[m + 1], 0)
        i2_num = moment(tm[m + 1], 2)
        i4_num = moment(tm[m + 1], 4)

        p0 = i0_num / i0_den
        m_turn_limits[f"m={m}"] = str(p0)

        # F_0^(L)(x) / F_0^(L)(0) = 1 - 3*x^2/L + (9/10*x^2 + 9/2*x^4)/L^2 + O(L^-3)
        a1 = -3 * (i2_num / i0_num)
        a2 = Fraction(9, 10) * (i2_num / i0_num) + Fraction(9, 2) * (i4_num / i0_num)
        b1 = -3 * (i2_den / i0_den)
        b2 = Fraction(9, 10) * (i2_den / i0_den) + Fraction(9, 2) * (i4_den / i0_den)

        c1 = p0 * (a1 - b1)
        c2 = p0 * (a2 - b2 - b1 * (a1 - b1))
        if m <= 3:
            edgeworth_coeffs[f"m={m}"] = {
                "p_inf": str(p0),
                "c1_over_n_minus_m": str(c1),
                "c2_over_n_minus_m_sq": str(c2),
            }

    assert m_turn_limits["m=1"] == "3/10"
    assert m_turn_limits["m=2"] == "71/252"
    assert m_turn_limits["m=3"] == "182/639"
    assert m_turn_limits["m=4"] == "45541/160160"
    assert m_turn_limits["m=5"] == "168388/592033"
    assert m_turn_limits["m=6"] == "120686411/424337760"

    assert edgeworth_coeffs["m=1"]["c1_over_n_minus_m"] == "-3/175"
    assert edgeworth_coeffs["m=1"]["c2_over_n_minus_m_sq"] == "2/175"
    assert edgeworth_coeffs["m=2"]["c1_over_n_minus_m"] == "65/21168"
    assert edgeworth_coeffs["m=2"]["c2_over_n_minus_m_sq"] == "-8497/4074840"

    return {
        "m_turn_rational_limits_m_1_to_6": m_turn_limits,
        "edgeworth_1st_and_2nd_order_m_1_to_3": edgeworth_coeffs,
    }


if __name__ == "__main__":
    import json
    results = {
        "theorem_1_macmahon": verify_macmahon_theorem_1(),
        "theorem_2_alternating_operator": verify_alternating_operator_theorem_2(),
        "theorem_3_legendre_horizon": verify_legendre_horizon_theorem_3(),
        "theorem_4_cantilever_spectrum": verify_cantilever_spectrum_theorem_4(),
        "theorem_5_edgeworth_asymptotics": verify_edgeworth_asymptotics_theorem_5(),
        "status": "ALL_CHECKS_PASSED",
    }
    print(json.dumps(results, indent=2))
