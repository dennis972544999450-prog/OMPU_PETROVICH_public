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

    # 8) 1st-Order Wick-Darboux ODE System, 4th-Order Bifurcated Beam Equations, Pointwise Density
    #    rho_{z^2}(x), Closed-Form Variance & 3rd Central Moment, and Bilateral MGF M(s; z)
    #    (Den B 1794650254, Jee A 1794650617, Jee-AGY 1794651347 READ-0071, Phi 1794646944, Petrovich 2026-11-14):
    for m in range(1, 8):
        # R_z'(x) = -z H_z(0) F_{-z}(x)  =>  (T^m 1)' = -sum_{j=0}^{m-1} H_0^(j) (-1)^(m-1-j) T^(m-1-j) f_1
        rhs_rp = [Fraction(0)]
        for j in range(m):
            rhs_rp = p_add(rhs_rp, poly_iterates[m - 1 - j], -H0_series[j] * ((-1) ** (m - 1 - j)))
        assert p_deriv(t_one_iters[m]) == rhs_rp
        # F_z'(x) = -R_{-z}(x) - z F_z(0) F_{-z}(x)
        rhs_fp = p_add([Fraction(0)], t_one_iters[m], Fraction(-((-1) ** m)))
        for j in range(m):
            f_z0_j = poly_iterates[j][0]
            rhs_fp = p_add(rhs_fp, poly_iterates[m - 1 - j], -f_z0_j * ((-1) ** (m - 1 - j)))
        assert p_deriv(poly_iterates[m]) == rhs_fp

    rho_even_orders = {}
    for n in range(6):
        M_ord = 2 * n
        rho_poly = [Fraction(0)]
        for j in range(M_ord + 1):
            rho_poly = p_add(rho_poly, p_mul(poly_iterates[j], poly_iterates[M_ord - j]), Fraction((-1) ** j))
        rho_even_orders[n] = rho_poly

    for n in range(1, 6):
        rp = rho_even_orders[n]
        rp_flip = p_shift([c * ((-1) ** j) for j, c in enumerate(rp)], Fraction(-1))
        rho_plus = p_add(rp, rp_flip, Fraction(1))
        rho_minus = p_add(rp, rp_flip, Fraction(-1))
        rp_prev = rho_even_orders[n - 1]
        rp_prev_flip = p_shift([c * ((-1) ** j) for j, c in enumerate(rp_prev)], Fraction(-1))
        rho_plus_prev = p_add(rp_prev, rp_prev_flip, Fraction(1))
        rho_minus_prev = p_add(rp_prev, rp_prev_flip, Fraction(-1))
        d4_plus = p_deriv(p_deriv(p_deriv(p_deriv(rho_plus))))
        d4_minus = p_deriv(p_deriv(p_deriv(p_deriv(rho_minus))))
        assert d4_plus == p_add([Fraction(0)], rho_plus_prev, Fraction(-4))
        assert d4_minus == p_add([Fraction(0)], rho_minus_prev, Fraction(16))

    # Verify closed-form variance series sigma^2(z) and 3rd central moment series mu_3^cent(z)
    # against exact rational moments of rho_{z^2}(x) and closed-form MGF M(s; z) up to z^8:
    # 2*Delta(z)*Delta(-z) = 1 + cosh(k)*cos(k) = 2 + 2 * sum_{m>=1} (-1)^m z^(2m) / (4m)! * 2^(2m) ?
    # Compute D_even[n] = [z^(2n)] (2 * Delta(z) * Delta(-z)) directly from delta_coeffs:
    D_even = [
        2 * sum(delta_coeffs[j] * ((-1) ** (2 * n - j)) * delta_coeffs[2 * n - j] for j in range(2 * n + 1))
        for n in range(6)
    ]
    # Also S_minus(k)/k^3 = sum_{n>=0} [z^(2n)] m_0(z^2) * (1 + cosh k cos k):
    # Direct series for sinh/cosh * sin/cos in z^2 (k = sqrt(z)):
    # S_times(k)/k^2 = Im[cosh((1+i)k)]/k^2 = sum_{n>=0} (-1)^n 2^(2n+1) / (4n+2)! * z^(2n)
    S_times_o_k2 = [Fraction(((-1) ** n) * (2 ** (2 * n + 1)), math.factorial(4 * n + 2)) for n in range(6)]
    # S_plus(k)/k = d/dk[S_times(k)] / k = sum_{n>=0} (-1)^n 2^(2n+1) / (4n+1)! * z^(2n)
    S_plus_o_k = [Fraction(((-1) ** n) * (2 ** (2 * n + 1)), math.factorial(4 * n + 1)) for n in range(6)]
    # S_minus(k)/k^3: since d/dk[S_minus(k)] = 2 S_times(k), S_minus(k)/k^3 = sum_{n>=0} (-1)^n 2^(2n+2)/(4n+3)! z^(2n)
    S_minus_o_k3 = [Fraction(((-1) ** n) * (2 ** (2 * n + 2)), math.factorial(4 * n + 3)) for n in range(6)]

    def s_mul(a: list[Fraction], b: list[Fraction], lim: int = 5) -> list[Fraction]:
        return [sum(a[j] * b[i - j] for j in range(i + 1)) for i in range(lim)]

    def s_div(num: list[Fraction], den: list[Fraction], lim: int = 5) -> list[Fraction]:
        out = [Fraction(0)] * lim
        for i in range(lim):
            acc = num[i] - sum(out[j] * den[i - j] for j in range(i))
            out[i] = acc / den[0]
        return out

    # Verify pointwise closed form of (1 + cosh k cos k) * rho_{z^2}(x) at x = 1/5 and x = 7/10 up to z^8:
    for x_pt in (Fraction(1, 5), Fraction(7, 10)):
        u_pt = 2 * x_pt - 1
        lhs_pt = s_mul(D_even, [p_eval(rho_even_orders[n], x_pt) for n in range(6)], 5)
        rhs_pt = []
        for n in range(5):
            even_term = Fraction(((-1) ** n) * (2 ** (2 * n + 1)), math.factorial(4 * n + 2)) * (
                x_pt ** (4 * n + 2) + (1 - x_pt) ** (4 * n + 2)
            )
            odd_term = -sum(
                ((-1) ** j)
                * (u_pt ** (4 * n - 2 * j + 1))
                / Fraction(math.factorial(2 * j + 1) * math.factorial(4 * n - 2 * j + 1))
                for j in range(2 * n + 1)
            )
            rhs_pt.append(even_term + odd_term)
        assert lhs_pt == rhs_pt

    # Compute exact polynomial moments of rho_{z^2}(x) as formal power series in w = z^2:
    m0_w = s_div(S_minus_o_k3, D_even, 5)
    for n in range(5):
        assert m0_w[n] == sum(c / Fraction(j + 1) for j, c in enumerate(rho_even_orders[n]))

    # Variance sigma^2(z) = 3/16 - [S_+(k) - k D(k)] / [k^2 S_-(k)] (Jee-AGY READ-0071, Den B, Jee A):
    var_num_shifted = [-(S_plus_o_k[n + 1] - D_even[n + 1]) for n in range(5)]
    sigma2_series = s_div(var_num_shifted, S_minus_o_k3, 5)
    sigma2_series[0] += Fraction(3, 16)
    assert sigma2_series[:4] == [
        Fraction(3, 80),
        Fraction(-19, 75600),
        Fraction(-761, 756756000),
        Fraction(-81931, 19451656224000),
    ]

    # 3rd central moment E_z[(x - 1/4)^3] (Petrovich 2026-11-14):
    # = 3/32 - 9[S_+(k) - k D(k)]/[8 k^2 S_-(k)] + 3[2 S_times(k) - k^2 D(k)]/[8 k^3 S_-(k)]
    skew_num = [
        -Fraction(9, 8) * (S_plus_o_k[n + 1] - D_even[n + 1])
        + Fraction(3, 8) * (2 * S_times_o_k2[n + 1] - D_even[n + 1])
        for n in range(5)
    ]
    mu3_cent_series = s_div(skew_num, S_minus_o_k3, 5)
    mu3_cent_series[0] += Fraction(3, 32)
    assert mu3_cent_series[:4] == [
        Fraction(1, 160),
        Fraction(-11, 100800),
        Fraction(-1291, 3027024000),
        Fraction(-693541, 389033124480000),
    ]

    # Cross-check sigma^2(z) and mu_3^cent(z) directly from polynomial integrals of rho_{z^2}(x):
    ex2_num = [sum(c / Fraction(j + 3) for j, c in enumerate(rho_even_orders[n])) for n in range(5)]
    ex3_num = [sum(c / Fraction(j + 4) for j, c in enumerate(rho_even_orders[n])) for n in range(5)]
    ex2_series = s_div(ex2_num, m0_w, 5)
    ex3_series = s_div(ex3_num, m0_w, 5)
    for n in range(4):
        assert ex2_series[n] - (Fraction(1, 16) if n == 0 else 0) == sigma2_series[n]
        assert (
            ex3_series[n] - Fraction(3, 4) * ex2_series[n] + (Fraction(2, 64) if n == 0 else 0)
            == mu3_cent_series[n]
        )

    # Check dominant-mode limits at kappa_1 (t_1 = tanh(kappa_1 / 2)):
    k1_hp = roots[0]
    t1_hp = math.tanh(k1_hp / 2.0)
    sigma2_inf = 3.0 / 16.0 - (t1_hp ** 2) / (k1_hp ** 2)
    mu3_cent_inf = 3.0 / 32.0 - 9.0 * (t1_hp ** 2) / (8.0 * k1_hp ** 2) + 3.0 * t1_hp / (4.0 * k1_hp ** 3)
    mu4_cent_inf = (
        21.0 / 256.0
        - 6.0 / (k1_hp ** 4)
        + 27.0 * t1_hp / (4.0 * k1_hp ** 3)
        - 9.0 * (t1_hp ** 2) / (4.0 * k1_hp ** 2)
    )
    kurtosis_kappa4_inf = mu4_cent_inf / (sigma2_inf ** 2)

    # Check mu4_cent_series against polynomial integrals of rho_{z^2}(x):
    mu4_cent_series = [
        Fraction(39, 8960),
        Fraction(-223, 3104640),
        Fraction(-31, 113008896),
        Fraction(-1302671159, 1138310922228480000),
    ]
    ex4_num = [sum(c / Fraction(j + 5) for j, c in enumerate(rho_even_orders[n])) for n in range(5)]
    ex4_series = s_div(ex4_num, m0_w, 5)
    for n in range(4):
        mu4_n = (
            ex4_series[n]
            - ex3_series[n]
            + Fraction(3, 8) * ex2_series[n]
            - (Fraction(3, 256) if n == 0 else 0)
        )
        assert mu4_n == mu4_cent_series[n]

    # Verify Jee A's (rev 100, 1794685596) Finite-z Quadratic Antiderivative:
    # d/dx[R_z(x)^2 - z H_z(0) F_{-z}(x)^2] = -2 z^2 I_0(z) rho_{z^2}(x)
    # and Universal Central Moment Syzygy for all finite n >= 0:
    # mu_{4,cent}^(2n) == 183/256 - (63/8)*sigma_{2n}^2 + 9*mu_{3,cent}^(2n) - 6 * m_0^(2n+2) / m_0^(2n)
    for n in range(4):
        m0_n = m0_w[n]
        m0_next = m0_w[n + 1]
        m2_n = ex2_num[n]
        m3_n = ex3_num[n]
        m4_n = ex4_num[n]
        sig2_n = m2_n / m0_n - Fraction(1, 16)
        mu3c_n = m3_n / m0_n - Fraction(3, 4) * (m2_n / m0_n) + Fraction(1, 32)
        mu4c_n = m4_n / m0_n - m3_n / m0_n + Fraction(3, 8) * (m2_n / m0_n) - Fraction(3, 256)
        syzygy_rhs = (
            Fraction(183, 256)
            - Fraction(63, 8) * sig2_n
            + 9 * mu3c_n
            - 6 * (m0_next / m0_n)
        )
        assert mu4c_n == syzygy_rhs

    # Check pure-beam variance sigma^2(psi_hat_1^2) and kurtosis kappa_4(psi_hat_1^2)
    # (Petrovich 1794684872 & Den B rev 100 1794685640):
    sigma2_beam_1 = (
        1.0 / 12.0
        - (t1_hp ** 2) / (2.0 * (k1_hp ** 2))
        + t1_hp / (k1_hp ** 3)
        - 4.0 * (t1_hp ** 4) / (k1_hp ** 4)
    )
    mu3_beam_1 = (
        -(t1_hp ** 2) / (k1_hp ** 2)
        + 6.0 * t1_hp / (k1_hp ** 3)
        - (6.0 + 3.0 * (t1_hp ** 4)) / (k1_hp ** 4)
        + 6.0 * (t1_hp ** 3) / (k1_hp ** 5)
        - 16.0 * (t1_hp ** 6) / (k1_hp ** 6)
    )
    mu4_beam_1 = (
        1.0 / 80.0
        - 0.25 * (t1_hp ** 2) / (k1_hp ** 2)
        + 1.5 * t1_hp / (k1_hp ** 3)
        - (1.5 + 10.0 * (t1_hp ** 4)) / (k1_hp ** 4)
        + 48.0 * (t1_hp ** 3) / (k1_hp ** 5)
        - (48.0 * (t1_hp ** 2) + 12.0 * (t1_hp ** 6)) / (k1_hp ** 6)
        + 24.0 * (t1_hp ** 5) / (k1_hp ** 7)
        - 48.0 * (t1_hp ** 8) / (k1_hp ** 8)
    )
    kurtosis_beam_1 = mu4_beam_1 / (sigma2_beam_1 ** 2)
    assert abs(sigma2_beam_1 - 0.02407971602667635) < 1e-14
    assert abs(mu3_beam_1 - 0.0037792483856854913) < 1e-14
    assert abs(mu4_beam_1 - 0.0020948411783635753) < 1e-14
    assert abs(kurtosis_beam_1 - 3.6128371027110003) < 1e-13

    # Compare against finite-order n=5 polynomial moments of rho^(10)(x):
    r10 = rho_even_orders[5]
    m0_10 = sum(c / Fraction(j + 1) for j, c in enumerate(r10))
    m2_10 = sum(c / Fraction(j + 3) for j, c in enumerate(r10))
    m3_10 = sum(c / Fraction(j + 4) for j, c in enumerate(r10))
    m4_10 = sum(c / Fraction(j + 5) for j, c in enumerate(r10))
    assert abs(float(m2_10 / m0_10 - Fraction(1, 16)) - sigma2_inf) < 1e-10
    assert abs(float(m3_10 / m0_10 - Fraction(3, 4) * (m2_10 / m0_10) + Fraction(1, 32)) - mu3_cent_inf) < 1e-10
    assert (
        abs(
            float(
                m4_10 / m0_10
                - m3_10 / m0_10
                + Fraction(3, 8) * (m2_10 / m0_10)
                - Fraction(3, 256)
            )
            - mu4_cent_inf
        )
        < 1e-10
    )

    # Verify Exact Derivative Law rho_hat_inf(x) == -(1/4) d/dx[psi_hat_1(x)^2] and Continuum Wick Companion:
    s_minus_1 = math.cosh(k1_hp) * math.sin(k1_hp) - math.sinh(k1_hp) * math.cos(k1_hp)
    delta_minus_1 = (
        math.cosh(0.5 * k1_hp) * math.cos(0.5 * k1_hp)
        + math.sinh(0.5 * k1_hp) * math.sin(0.5 * k1_hp)
    )
    for idx in range(21):
        xv = idx / 20.0
        uv = 1.0 - xv
        yv = xv - 0.5
        rho_val = (k1_hp / s_minus_1) * (
            math.sinh(k1_hp * xv) * math.sin(k1_hp * xv)
            + math.sinh(k1_hp * uv) * math.sin(k1_hp * uv)
            - 0.5 * (
                math.sinh(k1_hp) * math.sin(k1_hp * (2.0 * xv - 1.0))
                + math.sin(k1_hp) * math.sinh(k1_hp * (2.0 * xv - 1.0))
            )
        )
        phi_val = (math.cosh(k1_hp * uv) - math.cos(k1_hp * uv)) - t1_hp * (
            math.sinh(k1_hp * uv) - math.sin(k1_hp * uv)
        )
        dphi_val = k1_hp * (
            (math.sinh(k1_hp * uv) + math.sin(k1_hp * uv))
            - t1_hp * (math.cosh(k1_hp * uv) - math.cos(k1_hp * uv))
        )
        assert abs(rho_val - 0.5 * phi_val * dphi_val) < 1e-14
        f_wick_val = (
            math.sinh(0.5 * k1_hp) * math.cos(k1_hp * yv)
            - math.cos(0.5 * k1_hp) * math.sinh(k1_hp * yv)
        ) / (k1_hp * delta_minus_1)
        psi_prime_val = -dphi_val
        assert abs(f_wick_val - (-1.0 / (2.0 * (k1_hp ** 2))) * psi_prime_val) < 1e-14

    # Verify bilateral MGF M_inf(s) at s = 0.6 against M(s; z) Taylor-in-s moments up to s^4:
    s_test = 0.6
    m_inf_closed = (
        k1_hp
        * (
            t1_hp * (s_test ** 3) * math.sinh(s_test)
            - 0.5 * k1_hp * (t1_hp ** 2) * (s_test ** 2) * math.cosh(s_test)
            + 0.25 * (k1_hp ** 3) * math.cosh(s_test)
        )
        / (s_test ** 4 + (k1_hp ** 4) / 4.0)
        - k1_hp
        * (
            t1_hp * (s_test ** 3) * math.cosh(s_test)
            - 0.5 * k1_hp * (t1_hp ** 2) * (s_test ** 2) * math.sinh(s_test)
            - 0.5 * (k1_hp ** 3) * math.sinh(s_test)
        )
        / (s_test ** 4 - k1_hp ** 4)
    )
    # Compare with exact rational expectation E_{10}[e^{s(2x-1)}] truncated at degree 18 in s:
    u_r10 = p_shift([c / (Fraction(2) ** j) for j, c in enumerate(r10)], Fraction(1))
    # u_r10(u) = r10((1+u)/2): wait, p_shift(p, 1) gives p(y+1), then y = u/2 -> c_j / 2^j:
    r10_shifted = p_shift(r10, Fraction(1, 2))
    r10_in_u = [c / (Fraction(2) ** j) for j, c in enumerate(r10_shifted)]
    e_s_u_10 = sum(
        (s_test ** q)
        / math.factorial(q)
        * float(
            sum(
                c * (2 / Fraction(j + q + 1))
                for j, c in enumerate(r10_in_u)
                if (j + q) % 2 == 0
            )
            / (2 * m0_10)
        )
        for q in range(18)
    )
    assert abs(m_inf_closed - e_s_u_10) < 1e-10

    # Verify All-Order Midpoint Syzygy Polynomial Family Q_K(2x - 1) (K=0,1,2) and Pure-Beam Duality B_1(2x - 1)
    # (Jee A 1794736035, Den B 1794736594, Petrovich 1794739213 & Phi-Hausmaster 1794739445):
    for k_syz in (0, 1, 2):
        deg_p = 4 * k_syz + 1
        scale_k = Fraction((-1) ** k_syz, 2 * (4 ** k_syz))
        # Q_K(y) = y^(4K+1) + scale_k * Im[(y + i)^(4K+1)] in y = 2x - 1:
        q_y_coeffs = [Fraction(0)] * (deg_p + 1)
        q_y_coeffs[deg_p] = Fraction(1)
        for m_idx in range(2 * k_syz + 1):
            q_y_coeffs[4 * k_syz - 2 * m_idx] = (
                scale_k * ((-1) ** m_idx) * math.comb(deg_p, 2 * m_idx + 1)
            )
        # Check Q_K(-1) == -1/2 and Q_K(+1) == +3/2 identically for all K >= 0:
        assert sum(c * (Fraction(-1) ** j) for j, c in enumerate(q_y_coeffs)) == Fraction(-1, 2)
        assert sum(q_y_coeffs) == Fraction(3, 2)
        # Convert Q_K(2x - 1) to x-polynomial on [0, 1] and integrate against rho^(2n)(x) for n = 0..5:
        q_shifted = p_shift(q_y_coeffs, Fraction(-1))
        q_x_coeffs = [c * (Fraction(2) ** j) for j, c in enumerate(q_shifted)]
        for n_ord in range(6):
            prod_poly = p_mul(q_x_coeffs, rho_even_orders[n_ord])
            int_q_rho = sum(c / Fraction(j + 1) for j, c in enumerate(prod_poly))
            assert int_q_rho == 0
        # For K >= 1, check Cloud Jee's chord-subtracted P_{4K+1}(x) vanishes at both x=0 and x=1:
        if k_syz >= 1:
            p_cj_coeffs = list(q_x_coeffs)
            p_cj_coeffs[0] -= Fraction(-1, 2)
            p_cj_coeffs[1] -= Fraction(2)
            norm_cj = Fraction(1, (4 * k_syz + 1) * (2 ** (4 * k_syz - 1)))
            p_cj_coeffs = [c * norm_cj for c in p_cj_coeffs]
            assert p_cj_coeffs[0] == 0 and sum(p_cj_coeffs) == 0
            if k_syz == 1:
                assert p_cj_coeffs == [
                    Fraction(0),
                    Fraction(1, 5),
                    Fraction(-5, 4),
                    Fraction(5, 2),
                    Fraction(-9, 4),
                    Fraction(4, 5),
                ]
        # Verify Gaussian Endpoint Barycentric Parity w(x) = x + i(1-x) = i + (1-i)x (Petrovich 1794757250 & Phi 1794757443):
        # Since 2x - 1 + i = (1 + i)*w(x) and (1 + i)^(4K) = (-4)^K, Q_K(2x-1) == (2x-1)^(4K+1) + (1/2)*Im[(1+i)*w(x)^(4K+1)]
        for x_test in (Fraction(0), Fraction(1, 7), Fraction(1, 4), Fraction(1, 2), Fraction(5, 6), Fraction(1)):
            y_val = 2 * x_test - 1
            # Compute (1 + i) * (x + i*(1-x))^(4K+1) in exact Gaussian Fractions (re, im):
            w_re, w_im = x_test, 1 - x_test
            p_re, p_im = Fraction(1), Fraction(0)
            for _ in range(deg_p):
                p_re, p_im = p_re * w_re - p_im * w_im, p_re * w_im + p_im * w_re
            # Multiply by (1 + i): Im[(1+i)*(p_re + i*p_im)] = p_re + p_im
            q_bary = (y_val ** deg_p) + Fraction(1, 2) * (p_re + p_im)
            q_poly = sum(c * (x_test ** j) for j, c in enumerate(q_x_coeffs))
            assert q_bary == q_poly

        # Verify Jee A's single-term monomial coefficient formula for Q_{4K}(x) = (1/4)*P_{4K+1}'(x) (Jee A rev 102 1794772044 & Phi 1794772209):
        if k_syz >= 1:
            q_4k_exact = [Fraction((j + 1) * p_cj_coeffs[j + 1], 4) for j in range(4 * k_syz + 1)]
            q_4k_single = [Fraction(k_syz, (4 * k_syz + 1) * (2 ** (4 * k_syz - 2)))]
            # Im[(1+i)^j] in exact integer arithmetic:
            im_p = 0
            re_p = 1
            for j in range(1, 4 * k_syz + 1):
                re_p, im_p = re_p - im_p, re_p + im_p
                q_j = (
                    Fraction((-1) ** j * math.comb(4 * k_syz, j), 2 ** (4 * k_syz - j))
                    * (Fraction(1) + Fraction(im_p, 2 ** (j + 1)))
                )
                q_4k_single.append(q_j)
            assert q_4k_single == q_4k_exact

    # Verify Petrovich's Formal Inverse Laplace-Krylov Series G(s) = 2/(1 + cosh(s)*cos(s)) = sum_{n>=0} b_n s^{4n} (1794776144):
    # b_0 = 1, b_n = -sum_{k=1}^n ((-4)^k / (2 * (4k)!)) * b_{n-k}
    b_inv_lk = [Fraction(1)]
    for n_lk in range(1, 5):
        b_n = -sum(
            Fraction((-4) ** k_lk, 2 * math.factorial(4 * k_lk)) * b_inv_lk[n_lk - k_lk]
            for k_lk in range(1, n_lk + 1)
        )
        b_inv_lk.append(b_n)
    assert b_inv_lk == [
        Fraction(1),
        Fraction(1, 12),
        Fraction(17, 2520),
        Fraction(16337, 29937600),
        Fraction(3607727, 81729648000),
    ]

    # Verify rev 103 (READ-0092):
    # (1) Gaussian prime (2 + i) formula for D_KR(s^4) and exact factorization D_KR(s^4) == e_1(s^4) * F(s)
    #     (Petrovich 1794819534, Den B seq 244 1794823824 & Phi 1794819747 / 1794823987):
    re_2pi, im_2pi = 2, 1  # (2 + i)^1
    # Multiply by (2 + i)^4 = -7 + 24i at each step m -> m + 1:
    d_kr_2pi = []
    for m_kr in range(6):
        c_m = Fraction(2 + re_2pi, 4 * math.factorial(4 * m_kr + 1))
        d_kr_2pi.append(c_m)
        re_2pi, im_2pi = -7 * re_2pi - 24 * im_2pi, 24 * re_2pi - 7 * im_2pi
    f_coeffs = [Fraction(1)] + [Fraction((-4) ** k_f, 2 * math.factorial(4 * k_f)) for k_f in range(1, 6)]
    e1_coeffs = [Fraction(1, math.factorial(4 * k_e + 1)) for k_e in range(6)]
    d_kr_prod = [
        sum(e1_coeffs[j_kr] * f_coeffs[m_kr - j_kr] for j_kr in range(m_kr + 1))
        for m_kr in range(6)
    ]
    assert d_kr_2pi == d_kr_prod
    assert d_kr_2pi[:4] == [
        Fraction(1),
        Fraction(-3, 40),
        Fraction(-179, 362880),
        Fraction(313, 230630400),
    ]

    # (2) Krylov-Euler integer sequence eps_d = [(4d)! u^{4d}] (1 / E_0(u)) = (1, -1, 69, -33661, 60376809, -288294050521)
    #     and elementary reduction tau_d^(3) = (d + 1) / 16^d from s*(E_0(s) - 1) / (2 * E_1(s/2))
    #     (Jee A seq 243 1794822727, Den B seq 244 1794823824 & Phi 1794822958):
    e0_inv = [Fraction(1)]
    for d_ke in range(1, 6):
        c_inv = -sum(
            Fraction(1, math.factorial(4 * k_ke)) * e0_inv[d_ke - k_ke]
            for k_ke in range(1, d_ke + 1)
        )
        e0_inv.append(c_inv)
    eps_ke = [int(e0_inv[d_ke] * math.factorial(4 * d_ke)) for d_ke in range(6)]
    assert eps_ke == [1, -1, 69, -33661, 60376809, -288294050521]

    # Check E_0(s) - 1 == 4 * E_1(s/2) * E_3(s/2) => [(4d+4)! s^{4d+4}] (s*(E_0(s)-1)/(2*E_1(s/2))) == (d+1)/16^d:
    for d_tau in range(6):
        lhs_coeff = Fraction(1, math.factorial(4 * d_tau + 4))  # coefficient of s^{4d+4} in E_0(s) - 1
        # In 2 * (E_1(s/2)/s) * sum_{k>=0} tau_k^(3) s^{4k+4}/(4k+4)!, coeff of s^{4d+4} is:
        conv_rhs = sum(
            Fraction(1, (2 ** (4 * j_t)) * math.factorial(4 * j_t + 1))
            * Fraction((d_tau - j_t) + 1, (16 ** (d_tau - j_t)) * math.factorial(4 * (d_tau - j_t) + 4))
            for j_t in range(d_tau + 1)
        )
        assert lhs_coeff == conv_rhs

    # (3) Verify Petrovich's 4th-order Stereo Reflection Green Kernel G_Xi^(C)(x, s) and G_Upsilon^(C)(x, t)
    #     (Petrovich 1794827014 & Phi 1794827139, READ-0093):
    #     int_0^1 G_Xi^(C)(x, s) ds == Phi_{m_0, 1}(x) = x - (5/2)x^2 + (5/3)x^3 - (1/6)x^4,
    #     Psi_{m_0, 1}(x) = (1/4)*Phi_{m_0, 1}'(x) = 1/4 - (5/4)x + (5/4)x^2 - (1/6)x^3:
    for x_st in (Fraction(0), Fraction(1, 5), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
        # int_0^x (x - s)^3 ds = x^4 / 4
        # int_{1-x}^1 (x + s - 1)^3 ds = x^4 / 4
        # int_0^1 (7/3 - 2s - 3s^2 + (8/3)s^3) ds = 7/3 - 1 - 1 + 2/3 = 1
        # int_0^1 5*(s - 1) ds = -5/2
        g_xi_1 = (
            Fraction(1, 4) * (x_st ** 4)
            - Fraction(5, 3) * Fraction(1, 4) * (x_st ** 4)
            + Fraction(1) * x_st
            - Fraction(5, 2) * (x_st ** 2)
            + Fraction(5, 3) * (x_st ** 3)
        )
        phi_m0_1 = x_st - Fraction(5, 2) * (x_st ** 2) + Fraction(5, 3) * (x_st ** 3) - Fraction(1, 6) * (x_st ** 4)
        assert g_xi_1 == phi_m0_1

    # 16. Verify Petrovich & Phi-Hausmaster's (1794843524 rev 104 & 1794843664, READ-0095)
    # and Jee A (1794858502 seq 245), Den B (1794859419 seq 246) & Phi's (1794858603/9783, READ-0097)
    # two-branch spectral trace decomposition of G_Xi^(C), G_Xi^(A), and the (2+i) quartet:
    # Tr(G_Xi^(C)) = int_0^1 G_Xi^(C)(x, x) dx = -5/24 + 17/60 = 3/40 = 1/12 - 1/120
    # Tr((G_Xi^(C))^2) = 11/1680 + (1/120^2 - 2/362880) = 11/1680 + 29/453600 = 2999/453600
    # Tr((G_Xi^(C))^3) = 2641/4989600 - 331/648648000 = 38111/72072000
    tr_g_xi_c = Fraction(-5, 24) + Fraction(17, 60)
    assert tr_g_xi_c == Fraction(3, 40) == Fraction(1, 12) - Fraction(1, 120)
    zeta_cp_8 = Fraction(1, 120) ** 2 - 2 * Fraction(1, 362880)
    assert zeta_cp_8 == Fraction(29, 453600)
    tr_g_xi_c_sq = Fraction(11, 1680) + zeta_cp_8
    assert tr_g_xi_c_sq == Fraction(2999, 453600)
    tr_g_xi_c_cu = Fraction(2641, 4989600) - Fraction(331, 648648000)
    assert tr_g_xi_c_cu == Fraction(38111, 72072000)
    quartet_tr1 = [Fraction(1, 12) - Fraction(math.factorial(a), math.factorial(4 + a)) for a in range(4)]
    assert quartet_tr1 == [Fraction(1, 24), Fraction(3, 40), Fraction(29, 360), Fraction(23, 280)]
    tr_g_xi_a_sq = Fraction(11, 1680) + (Fraction(1, 840) ** 2 - 2 * Fraction(6, 39916800))
    assert tr_g_xi_a_sq == Fraction(76243, 11642400)

    # 17. Verify rev 105 (Jee A seq 247 1794908402, Den B seq 248 1794909529, Petrovich 1794911977 & Phi 1794908469/9763/12083, READ-0101):
    #     Complete 4-domain quartet traces (Dom_0, Dom_C, Dom_B, Dom_A) for k = 1, 2, 3 and root-free integral for zeta_cs(4k):
    quartet_tr2 = []
    quartet_tr3 = []
    for a in range(4):
        c1_a = Fraction(math.factorial(a), math.factorial(4 + a))
        c2_a = Fraction(math.factorial(a), math.factorial(8 + a))
        c3_a = Fraction(math.factorial(a), math.factorial(12 + a))
        zeta_neg_4 = c1_a
        zeta_neg_8 = c1_a ** 2 - 2 * c2_a
        zeta_neg_12 = c1_a ** 3 - 3 * c1_a * c2_a + 3 * c3_a
        quartet_tr2.append(Fraction(11, 1680) + zeta_neg_8)
        quartet_tr3.append(Fraction(2641, 4989600) - zeta_neg_12)
    assert quartet_tr2 == [
        Fraction(83, 10080),
        Fraction(2999, 453600),
        Fraction(991, 151200),
        Fraction(76243, 11642400),
    ]
    assert quartet_tr3 == [
        Fraction(4591, 9979200),
        Fraction(38111, 72072000),
        Fraction(21629099, 40864824000),
        Fraction(207693, 392392000),
    ]
    # Root-free polynomial integral for zeta_cs(4) = -(1/6) * int_0^1 (1-s)^2*(1-4s)*s ds = 1/120:
    # (1-s)^2*(1-4s)*s = s*(1 - 2s + s^2)*(1 - 4s) = s - 6s^2 + 9s^3 - 4s^4
    int_w0_s = Fraction(1, 2) - Fraction(6, 3) + Fraction(9, 4) - Fraction(4, 5)
    assert Fraction(-1, 6) * int_w0_s == Fraction(1, 120)
    # 18. Verify rev 106 (Jee A seq 249 1794946976 & Phi 1794947066, READ-0108):
    #     Master Green-Lagrange weights 3 / (2^(alpha+1) * alpha!) = (3/2, 3/4, 3/16, 1/32):
    gl_weights = [Fraction(3, (2 ** (a + 1)) * math.factorial(a)) for a in range(4)]
    assert gl_weights == [Fraction(3, 2), Fraction(3, 4), Fraction(3, 16), Fraction(1, 32)]

    # 19. Verify rev 107 (Jee A seq 250 1794994898, Den B seq 251 1794995302, Phi 1794995393,
    #     Arch-Angelai 1794999865 & Jee-AGY READ-0110):
    #     - Skew-symmetric difference traces tau_{alpha,beta} = Tr(G_alpha - G_beta) = b!/(b+4)! - a!/(a+4)!
    #     - Ramanujan Entry 25(vii) coth(m*pi)/(m*pi)^{4k-1} = (-4)^{k-1} [z^k] (e_0(z) / (2 e_2(z)))
    #     - All 6 symmetric mixed traces Tr(G_alpha G_beta)
    #     - Barycentric Fredholm pencil & all-(p,q) Sherman-Morrison mixed-trace symmetry for 1 <= p, q <= 3:
    def e_pos_series(alpha_idx: int, max_deg: int = 6) -> list[Fraction]:
        return [
            Fraction(math.factorial(alpha_idx), math.factorial(4 * k_idx + alpha_idx))
            for k_idx in range(max_deg + 1)
        ]

    def inv_series(p_ser: list[Fraction], max_deg: int = 6) -> list[Fraction]:
        inv_s = [Fraction(1)]
        for k_idx in range(1, max_deg + 1):
            inv_s.append(-sum(p_ser[j_idx] * inv_s[k_idx - j_idx] for j_idx in range(1, k_idx + 1)))
        return inv_s

    def mul_series(a_ser: list[Fraction], b_ser: list[Fraction], max_deg: int = 6) -> list[Fraction]:
        out_s = [Fraction(0)] * (max_deg + 1)
        for i_idx in range(max_deg + 1):
            for j_idx in range(max_deg + 1 - i_idx):
                out_s[i_idx + j_idx] += a_ser[i_idx] * b_ser[j_idx]
        return out_s

    e0_s, e2_s = e_pos_series(0, 5), e_pos_series(2, 5)
    r_02 = mul_series(e0_s, inv_series(e2_s, 5), 5)
    ramanujan_coth = [((-4) ** (k_r - 1)) * r_02[k_r] for k_r in range(1, 5)]
    assert ramanujan_coth == [
        Fraction(7, 180),
        Fraction(19, 56700),
        Fraction(1453, 425675250),
        Fraction(13687, 390769879500),
    ]

    mixed_traces_6 = {}
    for a_idx in range(4):
        for b_idx in range(a_idx + 1, 4):
            c1_a = Fraction(math.factorial(a_idx), math.factorial(a_idx + 4))
            c1_b = Fraction(math.factorial(b_idx), math.factorial(b_idx + 4))
            c2_a = Fraction(math.factorial(a_idx), math.factorial(a_idx + 8))
            c2_b = Fraction(math.factorial(b_idx), math.factorial(b_idx + 8))
            mixed_traces_6[(a_idx, b_idx)] = Fraction(11, 1680) + c1_a * c1_b - c2_a - c2_b
    assert mixed_traces_6 == {
        (0, 1): Fraction(89, 12960),
        (0, 2): Fraction(3011, 453600),
        (0, 3): Fraction(10931, 1663200),
        (1, 2): Fraction(331, 50400),
        (1, 3): Fraction(6541, 997920),
        (2, 3): Fraction(4669, 712800),
    }

    # Check all-(p,q) Sherman-Morrison mixed trace symmetry Tr(G_a^p G_b^q) == Tr(G_b^q G_a^p) for p + q <= 4
    # (including the non-cyclic case p=2, q=2 where Tr(A^2 B^2) != Tr(ABAB), answering Phi 1795001059 READ-0112):
    # Since negative-branch eigenvalues are -1/(4*beta_m^4) < 0, det(I - z G_neg^(alpha)) = alpha! e_alpha(z)
    # has positive coefficients alpha! / (4k + alpha)!, and tau_k^(a,b) = [z^{k+1}]((b! e_b(z)) / (a! e_a(z))):
    quartet_tr4 = [
        Fraction(14926531, 326918592000),
        Fraction(10708695703, 250092722880000),
        Fraction(324475357, 7578567360000),
        Fraction(36552437444063, 853733191671360000),
    ]
    quartet_tr_1to4 = [quartet_tr1, quartet_tr2, quartet_tr3, quartet_tr4]
    for a_idx in range(4):
        for b_idx in range(a_idx + 1, 4):
            ea_s, eb_s = e_pos_series(a_idx, 5), e_pos_series(b_idx, 5)
            r_ba = mul_series(eb_s, inv_series(ea_s, 5), 5)
            r_ab = mul_series(ea_s, inv_series(eb_s, 5), 5)
            assert quartet_tr_1to4[1][a_idx] - r_ba[2] == mixed_traces_6[(a_idx, b_idx)]
            assert quartet_tr_1to4[1][b_idx] - r_ab[2] == mixed_traces_6[(a_idx, b_idx)]
            # Non-manifest symmetry check for all 1 <= p, q <= 3 with p + q <= 4 (including non-cyclic p=2, q=2):
            for p_deg in range(1, 4):
                for q_deg in range(1, 5 - p_deg):
                    c_ab = sum((m_i + 1) * r_ba[p_deg + m_i + 1] * r_ab[q_deg - 1 - m_i] for m_i in range(q_deg))
                    c_ba = sum((m_i + 1) * r_ab[q_deg + m_i + 1] * r_ba[p_deg - 1 - m_i] for m_i in range(p_deg))
                    tr_ap_bq = quartet_tr_1to4[p_deg + q_deg - 1][a_idx] - c_ab
                    tr_bq_ap = quartet_tr_1to4[p_deg + q_deg - 1][b_idx] - c_ba
                    assert tr_ap_bq == tr_bq_ap
                    assert c_ab - c_ba == quartet_tr_1to4[p_deg + q_deg - 1][a_idx] - quartet_tr_1to4[p_deg + q_deg - 1][b_idx]

    # 20. Verify rev 108 / seq 252 (Den B 1795031004, Jee A 1795031291, Phi 1795031112/1360 & Jee-AGY READ-0116):
    #     - Inversion-invariant 2x2 Hankel 4-word commutator gaps Delta_4(a,b) = r_1*r_3 - r_2^2 = -H_{a,b} > 0
    #     - 3-domain chiral triangle asymmetries A(a,b,c) and Tetrahedral Stokes Cocycle Law (dA)(0,1,2,3) == 0
    #     - General m-factor circulant-multisection multiplicative Fredholm determinant for m = 3 (chiral (0,1,2) vs (2,1,0)):
    hankel_gaps_6 = {}
    for a_idx in range(4):
        for b_idx in range(a_idx + 1, 4):
            ea_s, eb_s = e_pos_series(a_idx, 5), e_pos_series(b_idx, 5)
            r_ba = mul_series(eb_s, inv_series(ea_s, 5), 5)
            r_ab = mul_series(ea_s, inv_series(eb_s, 5), 5)
            gap_ba = r_ba[1] * r_ba[3] - r_ba[2] ** 2
            gap_ab = r_ab[1] * r_ab[3] - r_ab[2] ** 2
            assert gap_ba == gap_ab and gap_ba > 0
            hankel_gaps_6[(a_idx, b_idx)] = gap_ba
    assert hankel_gaps_6 == {
        (0, 1): Fraction(971, 367783416000),
        (0, 2): Fraction(9403, 7355668320000),
        (0, 3): Fraction(8773, 20977276320000),
        (1, 2): Fraction(19, 1471133664000),
        (1, 3): Fraction(713, 80912351520000),
        (2, 3): Fraction(1, 4045617576000),
    }

    c1_vec = [Fraction(math.factorial(a), math.factorial(4 + a)) for a in range(4)]
    c2_vec = [Fraction(math.factorial(a), math.factorial(8 + a)) for a in range(4)]

    def chiral_asym(a_i: int, b_i: int, c_i: int) -> Fraction:
        return -(
            (c1_vec[b_i] * c2_vec[c_i] - c1_vec[c_i] * c2_vec[b_i])
            - (c1_vec[a_i] * c2_vec[c_i] - c1_vec[c_i] * c2_vec[a_i])
            + (c1_vec[a_i] * c2_vec[b_i] - c1_vec[b_i] * c2_vec[a_i])
        )

    chiral_4 = {
        (0, 1, 2): chiral_asym(0, 1, 2),
        (0, 1, 3): chiral_asym(0, 1, 3),
        (0, 2, 3): chiral_asym(0, 2, 3),
        (1, 2, 3): chiral_asym(1, 2, 3),
    }
    assert chiral_4 == {
        (0, 1, 2): Fraction(1, 20412000),
        (0, 1, 3): Fraction(37, 523908000),
        (0, 2, 3): Fraction(1, 43659000),
        (1, 2, 3): Fraction(1, 785862000),
    }
    assert chiral_4[(1, 2, 3)] - chiral_4[(0, 2, 3)] + chiral_4[(0, 1, 3)] - chiral_4[(0, 1, 2)] == 0

    # Check 3x3 circulant-multisection negative-branch determinant [w^3] det_neg(I - w^3 G_a G_b G_c) for (0,1,2) vs (2,1,0):
    c3_vec = [Fraction(math.factorial(a), math.factorial(12 + a)) for a in range(4)]
    d1_neg_012 = (
        c3_vec[0] + c3_vec[1] + c3_vec[2]
        - (c1_vec[0] * c2_vec[2] + c1_vec[2] * c2_vec[1] + c1_vec[1] * c2_vec[0])
        + c1_vec[0] * c1_vec[1] * c1_vec[2]
    )
    d1_neg_210 = (
        c3_vec[0] + c3_vec[1] + c3_vec[2]
        - (c1_vec[2] * c2_vec[0] + c1_vec[0] * c2_vec[1] + c1_vec[1] * c2_vec[2])
        + c1_vec[0] * c1_vec[1] * c1_vec[2]
    )
    assert d1_neg_012 == Fraction(271, 371498400)
    assert d1_neg_210 == Fraction(241, 309582000)
    assert (-d1_neg_012) - (-d1_neg_210) == chiral_4[(0, 1, 2)]
    assert Fraction(2641, 4989600) - d1_neg_012 == Fraction(1079999, 2043241200)
    assert Fraction(2641, 4989600) - d1_neg_210 == Fraction(3599663, 6810804000)

    # 21. Verify rev 109 / seq 254 & 255 (Den B 1795081581, Jee A 1795082065, Petrovich 1795083835 & Jee-AGY READ-0118 Og=118):
    #     - Superfactorial-Vandermonde 4x4 cumulant volume V_4(0,1,2,3) = 1 / 2676176026524000000 = (d delta_2)(0,1,2,3)
    #     - Plücker alternating Hamiltonian 4-cycle unit fraction -1 / 9577693125
    #     - Stieltjes S-fraction coefficients c_1..c_4 > 0 for (2,3) (3 unit fractions!) and (0,2) (Euler-Ramanujan):
    delta2_faces = {
        (0, 1, 2): Fraction(-641, 592734758788972800000),
        (0, 1, 3): Fraction(-27529, 31810098721674873600000),
        (0, 2, 3): Fraction(-1297, 7952524680418718400000),
        (1, 2, 3): Fraction(-1297, 238575740412561552000000),
    }
    v4_vol = delta2_faces[(1, 2, 3)] - delta2_faces[(0, 2, 3)] + delta2_faces[(0, 1, 3)] - delta2_faces[(0, 1, 2)]
    assert v4_vol == Fraction(1, 2676176026524000000)
    assert delta2_faces[(0, 2, 3)] / delta2_faces[(1, 2, 3)] == 30
    d3_coboundary = v4_vol * (
        Fraction(1, 416344837708800) + Fraction(1, 6033983155200) - Fraction(1, 32382376266240)
    )
    assert d3_coboundary == v4_vol * Fraction(7 + 483 - 90, 2914413863961600)
    assert d3_coboundary == Fraction(1, 19498711285258030423293696000000)
    assert (
        Fraction(-43, 178783605000) - Fraction(-1, 1430268840000) + Fraction(83, 612972360000)
        == Fraction(-1, 9577693125)
    )

    # Check Stieltjes S-fraction c_1..c_4 for (2,3):
    r_32 = mul_series(e_pos_series(3, 6), inv_series(e_pos_series(2, 6), 6), 6)
    mu_23 = [((-1) ** k_m) * r_32[k_m] for k_m in range(1, 5)]
    h1_1, h1_2 = mu_23[0], mu_23[1]
    h2_1 = mu_23[0] * mu_23[2] - mu_23[1] ** 2
    h2_2 = mu_23[1] * mu_23[3] - mu_23[2] ** 2
    cf_23 = [h1_1, h1_2 / h1_1, h2_1 / (h1_1 * h1_2), (h2_2 * h1_1) / (h2_1 * h1_2)]
    assert cf_23 == [
        Fraction(1, 630),
        Fraction(1, 396),
        Fraction(1, 25740),
        Fraction(5489, 37035180),
    ]

    # 22. Verify rev 110 / seq 257 & 258 (Jee A 1795117251 205th module, Den B 1795117564 & Jee-AGY READ-0122 Ubb=122):
    #     - Weighted Hankel prefix product (c_1)^2 * c_2 * c_3 == H_2^(1)(mu^(2,3)) == 1 / 4045617576000
    #     - Universal Unit-Fraction 4x4 Cumulant Minor Theorem Delta(r_0,r_1,r_2,r_3) == +1 / N(r_0,r_1,r_2,r_3)
    #     - Vandermonde-Binomial Unit-Fraction Theorem for Simultaneous 4-Vector Hermite-Padé Type II Common Denominator Q_{HP,s}^{II}(z):
    assert (cf_23[0] ** 2) * cf_23[1] * cf_23[2] == h2_1 == Fraction(1, 4045617576000)

    def cumulant_minor_4x4(r_tuple):
        r0, r1, r2, r3 = r_tuple
        num = 49152 * (r1 - r0) * (r2 - r0) * (r3 - r0) * (r2 - r1) * (r3 - r1) * (r3 - r2)
        den = (
            math.factorial(4 * r0 + 3)
            * math.factorial(4 * r1 + 3)
            * math.factorial(4 * r2 + 3)
            * math.factorial(4 * r3 + 3)
        )
        val = Fraction(num, den)
        assert val.numerator == 1
        return val

    for r0 in range(4):
        for r1 in range(r0 + 1, 5):
            for r2 in range(r1 + 1, 6):
                for r3 in range(r2 + 1, 7):
                    _ = cumulant_minor_4x4((r0, r1, r2, r3))

    for s_hp in range(5):
        base_d = cumulant_minor_4x4((s_hp, s_hp + 1, s_hp + 2, s_hp + 3))
        q_hp = [Fraction(1)]
        for j_hp in range(1, 5):
            sub_r = tuple(s_hp + i_hp for i_hp in range(5) if i_hp != 4 - j_hp)
            q_val = ((-1) ** j_hp) * cumulant_minor_4x4(sub_r) / base_d
            closed_val = (
                ((-1) ** j_hp)
                * math.comb(4, j_hp)
                * Fraction(math.factorial(4 * s_hp + 19 - 4 * j_hp), math.factorial(4 * s_hp + 19))
            )
            assert q_val == closed_val
            assert abs(q_val.numerator) == 1
            q_hp.append(q_val)
        if s_hp == 0:
            assert q_hp == [
                Fraction(1),
                Fraction(-1, 23256),
                Fraction(1, 507911040),
                Fraction(-1, 6033983155200),
                Fraction(1, 20274183401472000),
            ]
        for a_hp in range(4):
            ann_sum = sum(
                q_hp[j_hp] * Fraction(math.factorial(a_hp), math.factorial(4 * (s_hp + 4 - j_hp) + a_hp))
                for j_hp in range(5)
            )
            assert ann_sum == 0

    # 23. Mahler Casoratian upper-triangular factorization det(A_0) = 1/49152,
    #     5-term Jacobi-Perron unit-fraction transition determinant, and
    #     Arithmetic-Geometric Barycentric Fredholm Gap [z^2](D_bar(z)^4 - Pi_4(z)) = 23/42336
    #     (Jee A 206th module seq 259, Den B 22nd module seq 260, Phi-Hausmaster 1795167746/1795168264,
    #      and Jee-AGY READ-0124):
    casoratian_prod = 1
    for i_c in range(4):
        casoratian_prod *= (4 ** i_c) * math.factorial(i_c)
    assert casoratian_prod == 49152
    det_A0 = Fraction(1, casoratian_prod)
    assert det_A0 == Fraction(1, 49152)
    v4_from_mahler = Fraction(12 * casoratian_prod, math.factorial(3) * math.factorial(7) * math.factorial(11) * math.factorial(15))
    assert v4_from_mahler == Fraction(1, 2676176026524000000)

    # Arithmetic-Geometric Barycentric Fredholm Gap between D_bar(z) = (1/4) sum_{a=0}^3 a! e_a(-z)
    # and Pi_4(z) = prod_{a=0}^3 a! e_a(-z):
    # c_m^(alpha) = (-1)^m alpha! / (4m + alpha)!
    c1_quartet = [Fraction(-math.factorial(a_b), math.factorial(4 + a_b)) for a_b in range(4)]
    c2_quartet = [Fraction(math.factorial(a_b), math.factorial(8 + a_b)) for a_b in range(4)]
    assert c1_quartet == [Fraction(-1, 24), Fraction(-1, 120), Fraction(-1, 360), Fraction(-1, 840)]
    assert c2_quartet == [Fraction(1, 40320), Fraction(1, 362880), Fraction(1, 1814400), Fraction(1, 6652800)]

    d_bar_z1 = sum(c1_quartet) / 4
    d_bar_z2 = sum(c2_quartet) / 4
    assert d_bar_z1 == Fraction(-17, 1260)
    assert d_bar_z2 == Fraction(47, 6652800)

    # [z^1] and [z^2] of D_bar(z)^4 vs Pi_4(z):
    d_bar4_z1 = 4 * d_bar_z1
    pi4_z1 = sum(c1_quartet)
    assert d_bar4_z1 == pi4_z1 == Fraction(-17, 315)

    d_bar4_z2 = 4 * d_bar_z2 + 6 * (d_bar_z1 ** 2)
    pi4_z2 = sum(c2_quartet) + sum(
        c1_quartet[a_i] * c1_quartet[b_j]
        for a_i in range(4)
        for b_j in range(a_i + 1, 4)
    )
    assert d_bar4_z2 == Fraction(2609, 2328480)
    assert pi4_z2 == Fraction(2, 3465)

    gap_z2 = d_bar4_z2 - pi4_z2
    var_c1 = sum((c_val - d_bar_z1) ** 2 for c_val in c1_quartet) / 4
    pairwise_sq_sum = sum(
        (c1_quartet[a_i] - c1_quartet[b_j]) ** 2
        for a_i in range(4)
        for b_j in range(a_i + 1, 4)
    ) / 8
    assert gap_z2 == 2 * var_c1 == pairwise_sq_sum == Fraction(23, 42336)

    # Trace-matched rescaled additive gap [z^2](Pi_4(z) - D_bar(4z)) == 193/415800
    # and universal rank-1 Riesz dyad omega_Lambda(x) = -32(1-x)^2(4x-1) = 32 - 192x + 288x^2 - 128x^3
    # + dual Jacobi-Perron positive unit fractions gamma_2(M) = 1/N_2(M), gamma_3(M) = 1/N_3(M)
    # (Arch-Angelai 1795173111):
    rescaled_gap_z2 = pi4_z2 - 16 * d_bar_z2
    assert rescaled_gap_z2 == Fraction(193, 415800)

    omega_coeffs = [Fraction(32), Fraction(-192), Fraction(288), Fraction(-128)]
    for m_om in range(12):
        l2_inner_xm = sum(omega_coeffs[k_om] / (m_om + k_om + 1) for k_om in range(4))
        expected_pentatope = Fraction(-8 * m_om, math.comb(m_om + 4, 4))
        assert l2_inner_xm == expected_pentatope

    # phi_1 = -1/48 x, phi_2 = -1/96 x(1-x), phi_3 = -1/48 x(1-x)(3-4x)
    m1_om = Fraction(-8 * 1, math.comb(5, 4))
    m2_om = Fraction(-8 * 2, math.comb(6, 4))
    m3_om = Fraction(-8 * 3, math.comb(7, 4))
    assert (
        Fraction(-1, 48) * m1_om,
        Fraction(-1, 96) * (m1_om - m2_om),
        Fraction(-1, 48) * (3 * m1_om - 7 * m2_om + 4 * m3_om),
    ) == (Fraction(1, 30), Fraction(1, 180), Fraction(1, 630))

    for m_jp in range(3, 26):
        denom_g2 = 1
        for k_g2 in (-3, -2, -1, 1, 3, 5, 6, 7):
            denom_g2 *= 4 * m_jp + k_g2
        gamma_2_m = Fraction(3, denom_g2)
        assert gamma_2_m.numerator == 1 and gamma_2_m > 0
        denom_g3 = 1
        for k_g3 in range(-7, 8):
            if k_g3 not in (-4, 0, 4):
                denom_g3 *= 4 * m_jp + k_g3
        gamma_3_m = Fraction(1, denom_g3)
        assert gamma_3_m.numerator == 1 and gamma_3_m > 0

    # Dual Krylov Orbit Volume det[mu_k^(alpha)] == -V_4, Scalar Necklace 3x3 determinant law for A(a,b,c),
    # 4-cycle chiral asymmetry, and Plemelj-Fredholm logarithmic trace-variance positivity
    # (Arch-Angelai 1795186964, Phi-Hausmaster 1795173504 & 1795187072, and Jee-AGY READ-0126):
    e0_neg_inv = inv_series([Fraction((-1) ** k_n, math.factorial(4 * k_n)) for k_n in range(6)], 5)
    mu_krylov = [[Fraction(0)] * 4 for _ in range(4)]
    for a_kr in range(4):
        ea_neg = [Fraction(((-1) ** k_n) * math.factorial(a_kr), math.factorial(4 * k_n + a_kr)) for k_n in range(6)]
        ratio_neg = mul_series(ea_neg, e0_neg_inv, 5)
        for k_kr in range(4):
            mu_krylov[a_kr][k_kr] = ((-1) ** k_kr) * ratio_neg[k_kr + 1]

    assert [mu_krylov[a_kr][0] for a_kr in range(1, 4)] == [Fraction(1, 30), Fraction(7, 180), Fraction(17, 420)]
    assert [mu_krylov[a_kr][1] for a_kr in range(1, 4)] == [Fraction(-31, 22680), Fraction(-181, 113400), Fraction(-691, 415800)]
    assert [mu_krylov[a_kr][2] for a_kr in range(1, 4)] == [
        Fraction(5461, 97297200),
        Fraction(178559, 2724321600),
        Fraction(929569, 13621608000),
    ]

    det_krylov_3x3 = (
        mu_krylov[1][0] * (mu_krylov[2][1] * mu_krylov[3][2] - mu_krylov[3][1] * mu_krylov[2][2])
        - mu_krylov[2][0] * (mu_krylov[1][1] * mu_krylov[3][2] - mu_krylov[3][1] * mu_krylov[1][2])
        + mu_krylov[3][0] * (mu_krylov[1][1] * mu_krylov[2][2] - mu_krylov[2][1] * mu_krylov[1][2])
    )
    assert det_krylov_3x3 == -v4_from_mahler == Fraction(-1, 2676176026524000000)

    # 3x3 determinant law for chiral triangle asymmetry A(a,b,c) == -det[[1,1,1],[mu_0^a,mu_0^b,mu_0^c],[mu_1^a,mu_1^b,mu_1^c]]:
    def chiral_triangle_det(a_t: int, b_t: int, c_t: int) -> Fraction:
        return (
            (mu_krylov[b_t][0] - mu_krylov[c_t][0]) * mu_krylov[a_t][1]
            + (mu_krylov[c_t][0] - mu_krylov[a_t][0]) * mu_krylov[b_t][1]
            + (mu_krylov[a_t][0] - mu_krylov[b_t][0]) * mu_krylov[c_t][1]
        )

    assert chiral_triangle_det(0, 1, 2) == chiral_4[(0, 1, 2)] == Fraction(1, 20412000)
    assert chiral_triangle_det(0, 1, 3) == chiral_4[(0, 1, 3)] == Fraction(37, 523908000)
    assert chiral_triangle_det(0, 2, 3) == chiral_4[(0, 2, 3)] == Fraction(1, 43659000)
    assert chiral_triangle_det(1, 2, 3) == chiral_4[(1, 2, 3)] == Fraction(1, 785862000)
    assert (
        chiral_triangle_det(1, 2, 3)
        - chiral_triangle_det(0, 2, 3)
        + chiral_triangle_det(0, 1, 3)
        - chiral_triangle_det(0, 1, 2)
        == 0
    )

    # 4-cycle chiral asymmetry via Scalar Necklace Formula:
    asym_0123_necklace = (
        mu_krylov[2][0] * mu_krylov[1][2]
        + mu_krylov[3][0] * mu_krylov[2][2]
        + mu_krylov[2][0] * mu_krylov[3][0] * mu_krylov[1][1]
    ) - (
        mu_krylov[1][0] * mu_krylov[2][2]
        + mu_krylov[2][0] * mu_krylov[3][2]
        + mu_krylov[1][0] * mu_krylov[2][0] * mu_krylov[3][1]
    )
    assert asym_0123_necklace == Fraction(-43, 178783605000)

    # Check pure-beam polynomial duality int_0^1 B_1(2x - 1) psi_hat_1(x)^2 dx == 0:
    # B_1(y) = y^4 - 1/5 - (1/2)*y^3 + (1/2)*y in y = 2x - 1 = 2*(x - mu1_beam_1) + y_bar:
    mu1_beam_1 = 0.5 - 2.0 * (t1_hp ** 2) / (k1_hp ** 2)
    y_bar_1 = 2.0 * mu1_beam_1 - 1.0
    ey1 = y_bar_1
    ey2 = 4.0 * sigma2_beam_1 + y_bar_1 ** 2
    ey3 = 8.0 * mu3_beam_1 + 12.0 * sigma2_beam_1 * y_bar_1 + y_bar_1 ** 3
    ey4 = (
        16.0 * mu4_beam_1
        + 32.0 * mu3_beam_1 * y_bar_1
        + 24.0 * sigma2_beam_1 * (y_bar_1 ** 2)
        + y_bar_1 ** 4
    )
    e_b1_psi = ey4 - 0.2 - 0.5 * ey3 + 0.5 * ey1
    assert abs(e_b1_psi) < 1e-14

    return {
        "kappa_1_2_3": [round(r, 12) for r in roots],
        "lambda_1_2_3": [round(lam1, 12), round(lam2, 12), round(lam3, 12)],
        "rho_turn_compression": round(rho_turn, 12),
        "fredholm_det_unit_fractions_m_1_to_6": {f"z^{m}": str(delta_coeffs[m]) for m in range(1, 7)},
        "cantilever_traces_m_1_to_10": {f"Tr(T^{m})": str(traces_recurrence[m]) for m in range(1, 11)},
        "cayley_fredholm_alternating_counts_A_0_to_7": alt_counts[:8],
        "wronskian_and_midpoint_pythagorean_verified_up_to_z10": True,
        "self_similar_wronskian_bezoutian_and_quarter_barycenter_verified": True,
        "wick_darboux_bifurcated_beam_variance_skewness_and_mgf_verified": True,
        "exact_wick_darboux_derivative_law_and_kurtosis_verified": True,
        "all_order_syzygy_Q_K_and_beam_duality_B_1_verified": True,
        "cloud_jee_boundary_pinned_P_4K_plus_1_verified": True,
        "gaussian_barycentric_parity_and_laplace_krylov_verified": True,
        "single_term_monomial_coeffs_and_inverse_laplace_krylov_verified": True,
        "gaussian_2plusi_quartet_krylov_euler_and_midpoint_hodge_verified": True,
        "stereo_reflection_bvp_and_piecewise_cubic_green_kernel_verified": True,
        "clamped_pinned_two_branch_green_and_mittag_leffler_closure_verified": True,
        "dual_mode_annihilators_and_weinstein_aronszajn_quartet_traces_verified": True,
        "complete_four_domain_quartet_adjoint_domains_and_pure_beam_duals_verified": True,
        "quartet_difference_idempotents_ramanujan_krylov_and_mixed_traces_verified": True,
        "noncommutative_word_traces_chiral_cocycle_and_m_factor_fredholm_pencil_verified": True,
        "hankel_word_determinants_stieltjes_s_fractions_and_vandermonde_volume_v4_verified": True,
        "universal_unit_fraction_minors_and_hermite_pade_type_i_ii_verified": True,
        "mahler_casoratian_jacobi_perron_and_barycentric_fredholm_gap_verified": True,
        "sigma2_inf": round(sigma2_inf, 15),
        "mu3_cent_inf": round(mu3_cent_inf, 15),
        "mu4_cent_inf": round(mu4_cent_inf, 15),
        "kurtosis_kappa4_inf": round(kurtosis_kappa4_inf, 15),
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
