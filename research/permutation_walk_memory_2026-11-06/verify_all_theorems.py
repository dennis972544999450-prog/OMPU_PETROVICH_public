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
    poly_iterates = [v]
    for _ in range(12):
        v = apply_turn_operator_poly(v)
        poly_iterates.append(v)
    v_next = apply_turn_operator_poly(v)
    m_v = sum(c / Fraction(k + 1) for k, c in enumerate(v))
    m_next = sum(c / Fraction(k + 1) for k, c in enumerate(v_next))
    rayleigh = float(m_next / m_v)
    assert abs(rayleigh - lam1) < 1e-9

    # Free-End Cantilever Trace Theorem (Den B 1794304520) & Unit-Fraction Fredholm Determinant (Petrovich Argon 11:20):
    # Delta(z) = det(I - z T) = cosh(sqrt(z)/2)cos(sqrt(z)/2) - sinh(sqrt(z)/2)sin(sqrt(z)/2)
    #          = sum_{m>=0} (-1)**((m+1)//2) / (2**m * (2*m)!) * z**m,
    # and sum_{m>=1} Tr(T^m) z^{m-1} = (1/4)*((I - z T)^{-1} f_1)(0) = -Delta'(z) / Delta(z).
    delta_coeffs = [
        Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m))
        for m in range(11)
    ]
    traces_recurrence = {}
    for m in range(1, 11):
        # Newton-Girard / logarithmic derivative recurrence from -Delta'(z)/Delta(z):
        num_m = Fraction((-1) ** ((m - 1) // 2) * m, (2 ** m) * math.factorial(2 * m))
        tr_m = num_m - sum(delta_coeffs[j] * traces_recurrence[m - j] for j in range(1, m))
        # Compare with (1/4)*(T^{m-1} f_1)(0) and inner product (1/4)*<T^a f_1, T^b f_1>:
        free_end_quarter = Fraction(1, 4) * poly_iterates[m - 1][0]
        assert tr_m == free_end_quarter, f"Mismatch at m={m}: {tr_m} vs {free_end_quarter}"
        if m >= 2:
            a = (m - 2) // 2
            b = (m - 2) - a
            gram_quarter = Fraction(1, 4) * poly_inner_product(poly_iterates[a], poly_iterates[b])
            assert tr_m == gram_quarter
        traces_recurrence[m] = tr_m

    # Cayley-Fredholm Slope EGF (Jee A 1794339588), Midpoint Resolvents (Den B 1794340355),
    # and Wick-Rotation / Centrosymmetric Wronskian Conservation Laws (Petrovich Carbon 09:20):
    M_max = 10
    delta_ext = [
        Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m))
        for m in range(M_max + 2)
    ]
    delta_minus = [delta_ext[m] * ((-1) ** m) for m in range(M_max + 1)]
    int_delta = [
        Fraction((-1) ** ((m + 1) // 2), (2 ** m) * math.factorial(2 * m + 1))
        for m in range(M_max + 1)
    ]

    # 1) Exact Wick-rotated derivative identity: int_0^1 Delta(z u^2) du == -4 * Delta'(-z)
    assert int_delta == [-4 * (m + 1) * delta_ext[m + 1] * ((-1) ** m) for m in range(M_max + 1)]

    def series_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
        out = [Fraction(0)] * (M_max + 1)
        for i in range(M_max + 1):
            for j in range(M_max + 1 - i):
                out[i + j] += a[i] * b[j]
        return out

    def series_div_unit(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
        out = [Fraction(0)] * (M_max + 1)
        for m in range(M_max + 1):
            out[m] = a[m] - sum(b[j] * out[m - j] for j in range(1, m + 1))
        return out

    # H_z(0) = Delta(-z) / Delta(z) = sum_{m>=0} H_0^(m) z^m, A_m = (2m)! H_0^(m)
    H0_series = series_div_unit(delta_minus, delta_ext[: M_max + 1])
    I0_series = series_div_unit(int_delta, delta_ext[: M_max + 1])
    Theta_series = [Fraction(0)] * (M_max + 1)
    for m in range(1, M_max + 1):
        Theta_series[m - 1] = traces_recurrence[m]
    Theta_series[M_max] = series_div_unit(
        [-(m + 1) * delta_ext[m + 1] for m in range(M_max + 1)], delta_ext[: M_max + 1]
    )[M_max]

    # Verify A_m = (2m)! * H_0^(m) matches alternating walk counts (1, 1, 3, 26, 413, 10576, 397023, ...)
    alt_counts = [int(math.factorial(2 * m) * H0_series[m]) for m in range(M_max + 1)]
    assert alt_counts[:8] == [1, 1, 3, 26, 413, 10576, 397023, 20551376]

    # 2) Wick-Rotation Trace-Mass Convolution: I_0^(m) = 4 * sum_{k=1}^{m+1} (-1)^(k-1) Tr(T^k) H_0^(m+1-k)
    for m in range(M_max):
        wick_conv = 4 * sum(
            ((-1) ** (k - 1)) * Theta_series[k - 1] * H0_series[m + 1 - k]
            for k in range(1, m + 2)
        )
        assert I0_series[m] == wick_conv

    # 3) Centrosymmetric Wronskian w_z(x) = w_z(1-x) -> Three-Generator Conservation Law:
    #    H_z(0)^2 - 4 z I_z Theta_z == 1  <=>  Delta(z)^2 - Delta(-z)^2 == -sinh(sqrt(z)) sin(sqrt(z))
    H_sq = series_mul(H0_series, H0_series)
    I_Theta = series_mul(I0_series, Theta_series)
    conservation = [
        H_sq[m] - (Fraction(0) if m == 0 else 4 * I_Theta[m - 1])
        for m in range(M_max + 1)
    ]
    assert conservation == [Fraction(1)] + [Fraction(0)] * M_max
    d_sq_diff = [
        series_mul(delta_ext[: M_max + 1], delta_ext[: M_max + 1])[m]
        - series_mul(delta_minus, delta_minus)[m]
        for m in range(M_max + 1)
    ]
    neg_sinh_sin = [
        Fraction(0)
        if m % 2 == 0
        else Fraction((-1) ** ((m - 1) // 2 + 1) * (2 ** m), math.factorial(2 * m))
        for m in range(M_max + 1)
    ]
    assert d_sq_diff == neg_sinh_sin

    # 4) Midpoint Resolvents (Den B 1794340355) & Pythagorean Resolvent Identity (Petrovich Carbon 09:20):
    #    R_z(1/2)^2 + z F_z(1/2)^2 == Delta(z)^(-2) == det(I - z T)^(-2)
    cos_half = [Fraction((-1) ** m, (4 ** m) * math.factorial(2 * m)) for m in range(M_max + 1)]
    sinc_half = [
        Fraction((-1) ** m, 2 * (4 ** m) * math.factorial(2 * m + 1)) for m in range(M_max + 1)
    ]
    Rz_mid = series_div_unit(cos_half, delta_ext[: M_max + 1])
    Fz_mid = series_div_unit(sinc_half, delta_ext[: M_max + 1])
    for m in range(7):
        f_mid_poly = sum(c * (Fraction(1, 2) ** k) for k, c in enumerate(poly_iterates[m]))
        assert Fz_mid[m] == f_mid_poly
    Fz_sq = series_mul(Fz_mid, Fz_mid)
    pythagorean_lhs = [
        series_mul(Rz_mid, Rz_mid)[m] + (Fraction(0) if m == 0 else Fz_sq[m - 1])
        for m in range(M_max + 1)
    ]
    inv_delta_sq = series_div_unit(
        [Fraction(1)] + [Fraction(0)] * M_max,
        series_mul(delta_ext[: M_max + 1], delta_ext[: M_max + 1]),
    )
    assert pythagorean_lhs == inv_delta_sq

    # 5) Self-Similar Wronskian Scaling Law on [0, 1] & Simplex Identity (Jee A 1794389764, READ-0067):
    #    -w_z(x) = R_z'(x) F_z(x) - R_z(x) F_z'(x) = Delta(z (2x - 1)^2) / Delta(z)
    t_one_iters = [[Fraction(1)]]
    for _ in range(9):
        t_one_iters.append(apply_turn_operator_poly(t_one_iters[-1]))

    def p_deriv(p: list[Fraction]) -> list[Fraction]:
        return [c * j for j, c in enumerate(p) if j >= 1] or [Fraction(0)]

    def p_mul(p: list[Fraction], q: list[Fraction]) -> list[Fraction]:
        res = [Fraction(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            if a:
                for j, b in enumerate(q):
                    res[i + j] += a * b
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res

    def p_add(p: list[Fraction], q: list[Fraction], s: Fraction = Fraction(1)) -> list[Fraction]:
        res = [Fraction(0)] * max(len(p), len(q))
        for i, a in enumerate(p):
            res[i] += a
        for i, b in enumerate(q):
            res[i] += s * b
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        return res

    def p_eval(p: list[Fraction], x: Fraction) -> Fraction:
        return sum(c * (x ** k) for k, c in enumerate(p))

    def p_shift(p: list[Fraction], a: Fraction) -> list[Fraction]:
        res = [Fraction(0)] * len(p)
        for k, c in enumerate(p):
            if c:
                for j in range(k + 1):
                    res[j] += c * math.comb(k, j) * (a ** (k - j))
        return res

    W_polys = []
    for m in range(8):
        wm = [Fraction(0)]
        for k in range(m + 1):
            term = p_add(
                p_mul(p_deriv(t_one_iters[k]), poly_iterates[m - k]),
                p_mul(t_one_iters[k], p_deriv(poly_iterates[m - k])),
                Fraction(-1),
            )
            wm = p_add(wm, term)
        W_polys.append(wm)
        # Simplex identity: int_0^1 W_m(x) dx == I_0^(m)
        int_wm = sum(c / Fraction(k + 1) for k, c in enumerate(wm))
        assert int_wm == I0_series[m]

    two_x_minus_1_sq = [Fraction(1), Fraction(-4), Fraction(4)]
    pow_2xm1 = [Fraction(1)]
    for m in range(8):
        lhs_conv = [Fraction(0)]
        for j in range(m + 1):
            lhs_conv = p_add(lhs_conv, W_polys[m - j], delta_ext[j])
        rhs_mono = p_add([Fraction(0)], pow_2xm1, delta_ext[m])
        assert lhs_conv == rhs_mono
        pow_2xm1 = p_mul(pow_2xm1, two_x_minus_1_sq)

    # 6) Rank-1 Anticommutator D T + T D = -f_1 (x) delta_0, Gohberg-Semencul 2D Kernel,
    #    & Centrosymmetric Bezoutian Identity (Den B 1794390265 / 1794645335, READ-0067):
    f1_poly = [Fraction(1), Fraction(-1)]
    for r in range(7):
        h = [Fraction(0)] * r + [Fraction(1)]
        anticomm = p_add(p_deriv(apply_turn_operator_poly(h)), apply_turn_operator_poly(p_deriv(h)))
        expected_ac = [-h[0], h[0]] if h[0] != 0 else [Fraction(0)]
        assert anticomm == expected_ac
        wave_comm = p_add(
            p_deriv(p_deriv(apply_turn_operator_poly(h))),
            apply_turn_operator_poly(p_deriv(p_deriv(h))),
            Fraction(-1),
        )
        hp0 = h[1] if len(h) > 1 else Fraction(0)
        expected_wc = p_add([h[0]], f1_poly, hp0)
        assert wave_comm == expected_wc

    def K_gs_even(two_n: int, x: Fraction, y: Fraction) -> Fraction:
        upper = Fraction(1) - max(x, y)
        tot = Fraction(0)
        for k in range(two_n - 1):
            prod = p_mul(p_shift(poly_iterates[k], x), p_shift(poly_iterates[two_n - 2 - k], y))
            tot += ((-1) ** k) * sum(c * (upper ** (j + 1)) / Fraction(j + 1) for j, c in enumerate(prod))
        return tot

    def K_gs(m: int, x: Fraction, y: Fraction) -> Fraction:
        if m % 2 == 0:
            return K_gs_even(m, x, y)
        tot = p_eval(poly_iterates[m - 1], x + y) if (x + y <= 1) else Fraction(0)
        upper = min(y, Fraction(1) - x)
        for k in range(m - 1):
            pk = p_shift(poly_iterates[k], x)
            pq_pos = p_shift(poly_iterates[m - 2 - k], y)
            pq = [c * ((-1) ** j) for j, c in enumerate(pq_pos)]
            prod = p_mul(pk, pq)
            tot += ((-1) ** k) * sum(c * (upper ** (j + 1)) / Fraction(j + 1) for j, c in enumerate(prod))
        return tot

    for m in range(2, 7):
        for x_pt in (Fraction(1, 5), Fraction(1, 2)):
            for y_pt in (Fraction(2, 5), Fraction(3, 5)):
                bez_lhs = K_gs(m, x_pt, y_pt) - K_gs(m, 1 - x_pt, 1 - y_pt)
                bez_rhs = sum(
                    p_eval(t_one_iters[k], 1 - x_pt) * p_eval(poly_iterates[m - 1 - k], y_pt)
                    - p_eval(poly_iterates[k], 1 - x_pt) * p_eval(t_one_iters[m - 1 - k], y_pt)
                    for k in range(m)
                )
                assert bez_lhs == bez_rhs
            # Antidiagonal normal derivative -d/dy[Bezoutian]|_{y=1-x} == W_{m-1}(x)
            neg_dy_bez = sum(
                -p_eval(t_one_iters[k], 1 - x_pt) * p_eval(p_deriv(poly_iterates[m - 1 - k]), 1 - x_pt)
                + p_eval(poly_iterates[k], 1 - x_pt) * p_eval(p_deriv(t_one_iters[m - 1 - k]), 1 - x_pt)
                for k in range(m)
            )
            assert neg_dy_bez == p_eval(W_polys[m - 1], x_pt)

    # 7) Christoffel-Darboux Even-Resolvent Diagonal Law & Universal 1/4 Barycenter Invariant
    #    (Petrovich 2026-11-14): G^(2)_{z^2}(x, x) = int_x^1 F_z(s) F_{-z}(s) ds, and
    #    (int_0^1 x F_z(x) F_{-z}(x) dx) / (int_0^1 F_z(x) F_{-z}(x) dx) == 1/4 for all z!
    for n in range(1, 6):
        M_ord = 2 * n - 2
        ff_poly = [Fraction(0)]
        for k in range(M_ord + 1):
            ff_poly = p_add(ff_poly, p_mul(poly_iterates[k], poly_iterates[M_ord - k]), Fraction((-1) ** k))
        for x_pt in (Fraction(0), Fraction(1, 5), Fraction(1, 2), Fraction(4, 5)):
            int_x_to_1 = sum(c * (1 - x_pt ** (j + 1)) / Fraction(j + 1) for j, c in enumerate(ff_poly))
            assert int_x_to_1 == K_gs_even(2 * n, x_pt, x_pt)
        mass_0 = sum(c / Fraction(j + 1) for j, c in enumerate(ff_poly))
        mom_1 = sum(c / Fraction(j + 2) for j, c in enumerate(ff_poly))
        assert mass_0 == poly_iterates[2 * n - 1][0] == 4 * traces_recurrence[2 * n]
        assert mom_1 == traces_recurrence[2 * n]
        assert mom_1 / mass_0 == Fraction(1, 4)

    return {
        "kappa_1_2_3": [round(r, 12) for r in roots],
        "lambda_1_2_3": [round(lam1, 12), round(lam2, 12), round(lam3, 12)],
        "rho_turn_compression": round(rho_turn, 12),
        "fredholm_det_unit_fractions_m_1_to_6": {f"z^{m}": str(delta_coeffs[m]) for m in range(1, 7)},
        "cantilever_traces_m_1_to_10": {f"Tr(T^{m})": str(traces_recurrence[m]) for m in range(1, 11)},
        "cayley_fredholm_alternating_counts_A_0_to_7": alt_counts[:8],
        "wronskian_and_midpoint_pythagorean_verified_up_to_z10": True,
        "self_similar_wronskian_bezoutian_and_quarter_barycenter_verified": True,
    }


def verify_edgeworth_asymptotics_theorem_5():
    """
    Theorem 5 (Den B, Jee A & Petrovich):
    - m-turn Bayesian cell limits p_hat_inf(-, 1^m) = 3/10, 71/252, 182/639, 45541/160160, ...
    - Non-recursive moment reduction I_r^(m) / r! in terms of I_0 and H_0 (Jee A 1794339588 & Den B 1794340355).
    - 1st-, 2nd-, and 3rd-order rational Edgeworth expansions up to O((n-m)^-4) (Den B 1794340355).
    """
    # Compute T^m(1) for m = 0..10
    tm = [[Fraction(1)]]
    for _ in range(10):
        tm.append(apply_turn_operator_poly(tm[-1]))

    def moment(p: list[Fraction], power: int) -> Fraction:
        return sum(c / Fraction(k + power + 1) for k, c in enumerate(p))

    # Verify non-recursive mod-4 unrolled moment formula (Den B 1794340355 carrier L161-177 & Jee A 1794339588)
    I0_vals = [moment(tm[m], 0) for m in range(11)]
    H0_vals = [tm[m][0] for m in range(11)]
    for m in range(6):
        for r in range(7):
            exact_ir_over_fact = moment(tm[m], r) / math.factorial(r)
            closed_ir_over_fact = (
                sum(I0_vals[m + 2 * k] / math.factorial(r - 4 * k) for k in range(r // 4 + 1))
                - sum(
                    H0_vals[m + 2 * k + 1] / math.factorial(r - 1 - 4 * k)
                    for k in range((r - 1) // 4 + 1)
                    if r - 1 - 4 * k >= 0
                )
                + (
                    I0_vals[m + 2 * (r // 4) + 1]
                    if r % 4 == 2
                    else (H0_vals[m + 2 * (r // 4) + 2] if r % 4 == 3 else Fraction(0))
                )
            )
            assert exact_ir_over_fact == closed_ir_over_fact
            if r >= 4:
                mod4_ir = (
                    I0_vals[m]
                    - r * H0_vals[m + 1]
                    + r * (r - 1) * (r - 2) * (r - 3) * moment(tm[m + 2], r - 4)
                )
                assert moment(tm[m], r) == mod4_ir

    # Independently verify triangular-step cumulants (kappa_2 = 1/6, kappa_4 = -1/60, kappa_6 = 1/126)
    # from 2 * log(sin(t/2)/(t/2)) = -kappa_2 t^2/2! + kappa_4 t^4/4! - kappa_6 t^6/6! + ...
    # sin(t/2)/(t/2) = 1 - t^2/24 + t^4/1920 - t^6/322560 + ...
    s1, s2, s3 = Fraction(-1, 24), Fraction(1, 1920), Fraction(-1, 322560)
    log_c2 = 2 * s1
    log_c4 = 2 * (s2 - s1 * s1 / 2)
    log_c6 = 2 * (s3 - s1 * s2 + s1 * s1 * s1 / 3)
    kappa_2 = -log_c2 * math.factorial(2)
    kappa_4 = log_c4 * math.factorial(4)
    kappa_6 = -log_c6 * math.factorial(6)
    assert (kappa_2, kappa_4, kappa_6) == (Fraction(1, 6), Fraction(-1, 60), Fraction(1, 126))

    m_turn_limits = {}
    edgeworth_coeffs = {}
    for m in range(1, 7):
        i0_den = moment(tm[m], 0)
        i2_den = moment(tm[m], 2)
        i4_den = moment(tm[m], 4)
        i6_den = moment(tm[m], 6)
        i0_num = moment(tm[m + 1], 0)
        i2_num = moment(tm[m + 1], 2)
        i4_num = moment(tm[m + 1], 4)
        i6_num = moment(tm[m + 1], 6)

        p0 = i0_num / i0_den
        m_turn_limits[f"m={m}"] = str(p0)

        # F_0^(L)(x) / F_0^(L)(0) = 1 - 3*x^2/L + (9/10*x^2 + 9/2*x^4)/L^2
        #                           - (27/350*x^2 + 18/5*x^4 + 9/2*x^6)/L^3 + O(L^-4)
        a1 = -3 * (i2_num / i0_num)
        a2 = Fraction(9, 10) * (i2_num / i0_num) + Fraction(9, 2) * (i4_num / i0_num)
        a3 = -(
            Fraction(27, 350) * (i2_num / i0_num)
            + Fraction(18, 5) * (i4_num / i0_num)
            + Fraction(9, 2) * (i6_num / i0_num)
        )
        b1 = -3 * (i2_den / i0_den)
        b2 = Fraction(9, 10) * (i2_den / i0_den) + Fraction(9, 2) * (i4_den / i0_den)
        b3 = -(
            Fraction(27, 350) * (i2_den / i0_den)
            + Fraction(18, 5) * (i4_den / i0_den)
            + Fraction(9, 2) * (i6_den / i0_den)
        )

        c1 = p0 * (a1 - b1)
        c2 = p0 * (a2 - b2 - b1 * (a1 - b1))
        c3 = p0 * ((a3 - b3) - b1 * (a2 - b2) + (b1 * b1 - b2) * (a1 - b1))
        if m <= 4:
            edgeworth_coeffs[f"m={m}"] = {
                "p_inf": str(p0),
                "c1_over_n_minus_m": str(c1),
                "c2_over_n_minus_m_sq": str(c2),
                "c3_over_n_minus_m_cu": str(c3),
            }

    assert m_turn_limits["m=1"] == "3/10"
    assert m_turn_limits["m=2"] == "71/252"
    assert m_turn_limits["m=3"] == "182/639"
    assert m_turn_limits["m=4"] == "45541/160160"
    assert m_turn_limits["m=5"] == "168388/592033"
    assert m_turn_limits["m=6"] == "120686411/424337760"

    assert edgeworth_coeffs["m=1"]["c1_over_n_minus_m"] == "-3/175"
    assert edgeworth_coeffs["m=1"]["c2_over_n_minus_m_sq"] == "2/175"
    assert edgeworth_coeffs["m=1"]["c3_over_n_minus_m_cu"] == "-556/67375"
    assert edgeworth_coeffs["m=2"]["c1_over_n_minus_m"] == "65/21168"
    assert edgeworth_coeffs["m=2"]["c2_over_n_minus_m_sq"] == "-8497/4074840"
    assert edgeworth_coeffs["m=2"]["c3_over_n_minus_m_cu"] == "68012617/44497252800"
    assert edgeworth_coeffs["m=3"]["c3_over_n_minus_m_cu"] == "-46120805348351/217578715956201600"
    assert edgeworth_coeffs["m=4"]["c3_over_n_minus_m_cu"] == "152830288809687/4302212065882931200"

    return {
        "m_turn_rational_limits_m_1_to_6": m_turn_limits,
        "edgeworth_1st_2nd_3rd_order_m_1_to_4": edgeworth_coeffs,
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
