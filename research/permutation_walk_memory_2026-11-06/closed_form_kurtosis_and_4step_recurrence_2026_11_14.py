#!/usr/bin/env python3
"""
closed_form_kurtosis_and_4step_recurrence_2026_11_14.py

Verification of:
1. Petrovich's (§5 item 8, bus:1794671205_670600_20ab7a) Rayleigh odd-branch correction,
   closed-form bilateral MGF M(s; z) = E_z[e^{s(2x-1)}], eigenmode limit M_inf(s),
   and 3rd central moment mu_3^cent(z) / skewness gamma_{1,inf} = +0.7629848989123056.
2. Exact 4-step algebraic recurrence U_{p+4}(z) for all midpoint moments
   U_p(z) := E_z[(2x-1)^p] (both even p = 2m and odd p = 2m+1) implied by the
   binomial denominators (s^4 + z^2/4) and (s^4 - z^2) of M_even(s; z) and M_odd(s; z).
3. Exact closed-form 4th midpoint moment U_4(z) = E_z[(2x-1)^4], 4th central moment
   mu_4^cent(z) := E_z[(x - 1/4)^4], rational Taylor series in z^2 up to z^{14},
   and dominant cantilever eigenmode limit mu_{4,inf}^cent, kurtosis kappa_{4,inf},
   and excess kurtosis gamma_{2,inf} = kappa_{4,inf} - 3.

Authors: Jee-AGY (ompu-bd67c143cd) & Arch-Angelai (ompu-90b544b082), 2026-11-14
"""

from __future__ import annotations

import json
import math
from fractions import Fraction


def build_exact_resolvent_density_series(max_m: int = 18) -> list[list[Fraction]]:
    """Build exact polynomial coefficients g_n(x) where rho_{z^2}(x) = sum_{n>=0} g_n(x) z^{2n}."""
    polys: list[list[Fraction]] = [[Fraction(1), Fraction(-1)]]
    for _ in range(1, max_m):
        prev = polys[-1]
        nxt = [Fraction(0)] * (len(prev) + 2)
        for j, c in enumerate(prev):
            amp = c / Fraction((j + 1) * (j + 2))
            deg = j + 2
            binom = Fraction(1)
            for r in range(deg + 1):
                nxt[r] += amp * binom * (Fraction(-1) if r % 2 == 1 else Fraction(1))
                binom = binom * Fraction(deg - r, r + 1)
        polys.append(nxt)

    g_polys: list[list[Fraction]] = []
    for n in range(max_m // 2):
        deg = 4 * n + 2
        gn = [Fraction(0)] * (deg + 1)
        for a in range(2 * n + 1):
            b = 2 * n - a
            sign = Fraction(-1) if b % 2 == 1 else Fraction(1)
            pa, pb = polys[a], polys[b]
            for ia, ca in enumerate(pa):
                for ib, cb in enumerate(pb):
                    gn[ia + ib] += sign * ca * cb
        g_polys.append(gn)
    return g_polys


def int_0_1_poly_times(gn: list[Fraction], weight_poly: list[Fraction]) -> Fraction:
    res = Fraction(0)
    for i, c1 in enumerate(gn):
        for j, c2 in enumerate(weight_poly):
            res += c1 * c2 / Fraction(i + j + 1)
    return res


def series_div(num: list[Fraction], den: list[Fraction], terms: int = 8) -> list[Fraction]:
    q: list[Fraction] = []
    for n in range(terms):
        s = num[n]
        for k in range(1, n + 1):
            s -= den[k] * q[n - k]
        q.append(s / den[0])
    return q


def closed_form_moments(z: float) -> dict[str, float]:
    """Evaluate closed-form moments U_1..U_6, sigma^2(z), mu_3^cent(z), mu_4^cent(z) at z > 0."""
    k = math.sqrt(z)
    s_plus = math.cosh(k) * math.sin(k) + math.sinh(k) * math.cos(k)
    s_minus = math.cosh(k) * math.sin(k) - math.sinh(k) * math.cos(k)
    s_times = math.sinh(k) * math.sin(k)
    d_val = 1.0 + math.cosh(k) * math.cos(k)

    # Initial moments U_0 = 1, U_1 = -1/2, U_2, U_3:
    u0 = 1.0
    u1 = -0.5
    u2 = 1.0 - 4.0 * (s_plus - k * d_val) / (k**2 * s_minus)
    u3 = -0.5 + 6.0 * s_times / (k**3 * s_minus) - 3.0 * s_plus / (k**2 * s_minus)

    # Closed-form U_4 = E_z[(2x-1)^4]:
    u4 = (
        1.0
        - 96.0 / (z**2)
        + 96.0 * s_times / (k**3 * s_minus)
        - 24.0 * s_plus / (k**2 * s_minus)
        + 8.0 * d_val / (k * s_minus)
    )

    # 4-step recurrence for even U_{2m+4}(z) from (s^4 + z^2/4) M_even(s; z):
    def even_step(m: int, u_2m: float) -> float:
        p4 = math.factorial(2 * m + 4)
        f_ratio = p4 / math.factorial(2 * m)
        rhs_num = (
            (p4 / math.factorial(2 * m + 1)) * (k * s_times / s_minus)
            - (p4 / (2.0 * math.factorial(2 * m + 2))) * (k**2 * s_plus / s_minus)
            + (p4 / (2.0 * math.factorial(2 * m + 3))) * (k**3 * d_val / s_minus)
            + (z**2) / 4.0
        )
        return (-4.0 * f_ratio * u_2m + 4.0 * rhs_num) / (z**2)

    # 4-step recurrence for odd U_{2m+5}(z) from (s^4 - z^2) M_odd(s; z):
    def odd_step(m: int, u_2m1: float) -> float:
        p5 = math.factorial(2 * m + 5)
        f_ratio = p5 / math.factorial(2 * m + 1)
        rhs_num = (
            (p5 / math.factorial(2 * m + 2)) * (k * s_times / s_minus)
            - (p5 / (2.0 * math.factorial(2 * m + 3))) * (k**2 * s_plus / s_minus)
            - (z**2) / 2.0
        )
        return (f_ratio * u_2m1 + rhs_num) / (z**2)

    u4_from_rec = even_step(0, u0)
    u5_from_rec = odd_step(0, u1)
    u6_from_rec = even_step(1, u2)

    sigma2 = 3.0 / 16.0 - (s_plus - k * d_val) / (k**2 * s_minus)
    mu3_cent = (
        3.0 / 32.0
        - 9.0 * (s_plus - k * d_val) / (8.0 * k**2 * s_minus)
        + 3.0 * (2.0 * s_times - k**2 * d_val) / (8.0 * k**3 * s_minus)
    )
    mu4_cent = (
        21.0 / 256.0
        - 6.0 / (z**2)
        + 27.0 * s_times / (4.0 * k**3 * s_minus)
        - 9.0 * s_plus / (4.0 * k**2 * s_minus)
        + 7.0 * d_val / (8.0 * k * s_minus)
    )

    return {
        "u2": u2,
        "u3": u3,
        "u4": u4,
        "u4_from_rec": u4_from_rec,
        "u5_from_rec": u5_from_rec,
        "u6_from_rec": u6_from_rec,
        "sigma2": sigma2,
        "mu3_cent": mu3_cent,
        "mu4_cent": mu4_cent,
    }


def main() -> None:
    g_polys = build_exact_resolvent_density_series(18)
    w_1 = [Fraction(1)]
    # Weight polynomials for (2x-1)^p and (x - 1/4)^4:
    w_u4 = [Fraction(1), Fraction(-8), Fraction(24), Fraction(-32), Fraction(16)]
    w_u5 = [Fraction(-1), Fraction(10), Fraction(-40), Fraction(80), Fraction(-80), Fraction(32)]
    w_u6 = [Fraction(1), Fraction(-12), Fraction(60), Fraction(-160), Fraction(240), Fraction(-192), Fraction(64)]
    w_c4 = [Fraction(1, 256), Fraction(-1, 16), Fraction(3, 8), Fraction(-1, 1), Fraction(1, 1)]

    z_coeffs = [int_0_1_poly_times(gn, w_1) for gn in g_polys]
    u4_series = series_div([int_0_1_poly_times(gn, w_u4) for gn in g_polys], z_coeffs, 8)
    u5_series = series_div([int_0_1_poly_times(gn, w_u5) for gn in g_polys], z_coeffs, 8)
    u6_series = series_div([int_0_1_poly_times(gn, w_u6) for gn in g_polys], z_coeffs, 8)
    mu4_series = series_div([int_0_1_poly_times(gn, w_c4) for gn in g_polys], z_coeffs, 8)

    # Verify exact rational Taylor coefficients of E_z[(2x-1)^4] and mu_4^cent(z):
    assert u4_series[:4] == [
        Fraction(9, 35),
        Fraction(-221, 242550),
        Fraction(-2383, 662161500),
        Fraction(-267836497, 17786108159820000),
    ]
    assert mu4_series[:4] == [
        Fraction(39, 8960),
        Fraction(-223, 3104640),
        Fraction(-31, 113008896),
        Fraction(-1302671159, 1138310922228480000),
    ]

    # Check closed-form formulas & 4-step recurrence at z = 0.7:
    z = 0.7
    cf = closed_form_moments(z)
    u4_taylor = sum(float(c) * (z ** (2 * n)) for n, c in enumerate(u4_series))
    u5_taylor = sum(float(c) * (z ** (2 * n)) for n, c in enumerate(u5_series))
    u6_taylor = sum(float(c) * (z ** (2 * n)) for n, c in enumerate(u6_series))
    mu4_taylor = sum(float(c) * (z ** (2 * n)) for n, c in enumerate(mu4_series))

    assert abs(cf["u4"] - cf["u4_from_rec"]) < 5e-14
    assert abs(cf["u4"] - u4_taylor) < 5e-13
    assert abs(cf["u5_from_rec"] - u5_taylor) < 5e-12
    assert abs(cf["u6_from_rec"] - u6_taylor) < 5e-11
    assert abs(cf["mu4_cent"] - mu4_taylor) < 5e-14

    # Dominant cantilever mode limit z -> kappa_1^2:
    k1 = 1.8751040687119611664453082410782
    for _ in range(12):
        k1 -= (1.0 + math.cosh(k1) * math.cos(k1)) / (
            math.sinh(k1) * math.cos(k1) - math.cosh(k1) * math.sin(k1)
        )
    t1 = math.tanh(k1 / 2.0)

    sigma2_inf = 3.0 / 16.0 - (t1**2) / (k1**2)
    mu3_cent_inf = 3.0 / 32.0 - 9.0 * (t1**2) / (8.0 * k1**2) + 3.0 * t1 / (4.0 * k1**3)
    u4_inf = 1.0 - 96.0 / (k1**4) + 96.0 * t1 / (k1**3) - 24.0 * (t1**2) / (k1**2)
    mu4_cent_inf = (
        21.0 / 256.0
        - 6.0 / (k1**4)
        + 27.0 * t1 / (4.0 * k1**3)
        - 9.0 * (t1**2) / (4.0 * k1**2)
    )
    skewness_inf = mu3_cent_inf / (sigma2_inf**1.5)
    kurtosis_inf = mu4_cent_inf / (sigma2_inf**2)
    excess_kurtosis_inf = kurtosis_inf - 3.0

    # Independent Simpson quadrature of psi_hat_1(x)^2 on [0, 1]:
    s_minus_1 = math.cosh(k1) * math.sin(k1) - math.sinh(k1) * math.cos(k1)
    n_grid = 4000
    h = 1.0 / n_grid

    def psi1_sq(x: float) -> float:
        u = 2.0 * x - 1.0
        num = (
            math.sinh(k1 * x) * math.sin(k1 * x)
            + math.sinh(k1 * (1.0 - x)) * math.sin(k1 * (1.0 - x))
            - 0.5 * (math.sinh(k1) * math.sin(k1 * u) + math.sin(k1) * math.sinh(k1 * u))
        )
        return (k1 / s_minus_1) * num

    def simpson(fn) -> float:
        total = fn(0.0) + fn(1.0)
        for i in range(1, n_grid):
            total += (4.0 if i % 2 == 1 else 2.0) * fn(i * h)
        return total * h / 3.0

    quad_mass = simpson(psi1_sq)
    quad_mean = simpson(lambda x: x * psi1_sq(x))
    quad_mu4 = simpson(lambda x: ((x - 0.25) ** 4) * psi1_sq(x))
    assert abs(quad_mass - 1.0) < 1e-14
    assert abs(quad_mean - 0.25) < 1e-14
    assert abs(quad_mu4 - mu4_cent_inf) < 1e-14

    out = {
        "status": "ALL_CHECKS_PASSED",
        "u4_series_z0_to_z6": [str(c) for c in u4_series[:4]],
        "mu4_cent_series_z0_to_z6": [str(c) for c in mu4_series[:4]],
        "z_0_7_spot_check": {
            "u4_closed": cf["u4"],
            "u4_abs_diff": abs(cf["u4"] - u4_taylor),
            "u5_rec_abs_diff": abs(cf["u5_from_rec"] - u5_taylor),
            "u6_rec_abs_diff": abs(cf["u6_from_rec"] - u6_taylor),
            "mu4_cent_closed": cf["mu4_cent"],
            "mu4_cent_abs_diff": abs(cf["mu4_cent"] - mu4_taylor),
        },
        "dominant_eigenmode_limit": {
            "kappa_1": k1,
            "sigma2_inf": sigma2_inf,
            "mu3_cent_inf": mu3_cent_inf,
            "skewness_gamma1_inf": skewness_inf,
            "u4_inf": u4_inf,
            "mu4_cent_inf": mu4_cent_inf,
            "mu4_quad_abs_diff": abs(quad_mu4 - mu4_cent_inf),
            "kurtosis_kappa4_inf": kurtosis_inf,
            "excess_kurtosis_gamma2_inf": excess_kurtosis_inf,
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
