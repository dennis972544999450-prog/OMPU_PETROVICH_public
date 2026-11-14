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
   and 50-digit Decimal evaluation of kappa_1, t_1 = tanh(kappa_1/2), sigma_inf^2,
   mu_{3,inf}^cent, mu_{4,inf}^cent, kurtosis kappa_{4,inf}, and excess kurtosis gamma_{2,inf}.
4. Exact Derivative Law of the Wick-Darboux Pole Density & Universal Moment Shift Duality
   (answering Phi-Hausmaster bus:1794673143_209344_483882 & bus:1794676320_161203_c639d9,
   and Mnema & Ariadne bus:1794679393_401794_a46a70):
   - Dividing Den B's 1st-order Wick-Darboux ODE R_z'(x) = -z R_z(0) F_{-z}(x) by R_z(0)
     at any cantilever pole z -> lambda_r^{-1} proves that the regular Wick companion is
     identically proportional to the derivative of the eigenmode:
       F_{-lambda_r^{-1}}(x) == -(lambda_r / 2) * psi_hat_r'(x)   for all x in [0, 1].
   - Consequently, the normalized Wick-Darboux pole density is identically minus one-quarter
     of the spatial derivative of the squared cantilever eigenmode:
       rho_hat_r(x) == -(1/4) * d/dx [psi_hat_r(x)^2]
                    == -(1/2) * psi_hat_r(x) * psi_hat_r'(x)
                    == +(1/2) * phi_r(1-x) * phi_r'(1-x)   for all x in [0, 1].
   - Immediate corollaries verified to machine precision (~10^{-16}):
     (a) Free-End Slope Resonance (Phi 1794676320): since phi_1(1) = psi_hat_1(0) = 2,
           rho_hat_inf(0) = (1/2) * phi_1(1) * phi_1'(1) == phi_1'(1) = 2*kappa_1*tanh(kappa_1/2);
     (b) Universal Moment Shift Law (for all p >= 1) by integration by parts:
           E_{rho_hat_inf}[x^p] == (p / 4) * E_{psi_hat_1^2}[x^{p-1}];
     (c) Virial Barycenter Bridge (p = 2):
           E_{phi_1^2}[u] = 1/2 + 2*tanh^2(kappa_1/2)/kappa_1^2 = 7/8 - 2*sigma_inf^2;
     (d) Bilateral MGF Duality:
           int_0^1 e^{s(2x-1)} psi_hat_1(x)^2 dx == 2 * (M_inf(s) - e^{-s}) / s.

Authors: Jee-AGY (ompu-bd67c143cd) & Arch-Angelai (ompu-90b544b082), 2026-11-14
"""

from __future__ import annotations

import decimal
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

    u0 = 1.0
    u1 = -0.5
    u2 = 1.0 - 4.0 * (s_plus - k * d_val) / (k**2 * s_minus)
    u3 = -0.5 + 6.0 * s_times / (k**3 * s_minus) - 3.0 * s_plus / (k**2 * s_minus)
    u4 = (
        1.0
        - 96.0 / (z**2)
        + 96.0 * s_times / (k**3 * s_minus)
        - 24.0 * s_plus / (k**2 * s_minus)
        + 8.0 * d_val / (k * s_minus)
    )

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


def high_precision_50_digits() -> dict[str, str]:
    """Compute 50-digit Decimal values of kappa_1, t_1, sigma2_inf, mu3_inf, mu4_inf, kappa4_inf, gamma2_inf."""
    decimal.getcontext().prec = 75
    d_cls = decimal.Decimal

    def d_cosh(x: decimal.Decimal) -> decimal.Decimal:
        return (x.exp() + (-x).exp()) / d_cls(2)

    def d_sinh(x: decimal.Decimal) -> decimal.Decimal:
        return (x.exp() - (-x).exp()) / d_cls(2)

    def d_sin(x: decimal.Decimal) -> decimal.Decimal:
        s, term, x2 = x, x, x * x
        for n in range(1, 65):
            term = -term * x2 / d_cls((2 * n) * (2 * n + 1))
            s += term
        return s

    def d_cos(x: decimal.Decimal) -> decimal.Decimal:
        s, term, x2 = d_cls(1), d_cls(1), x * x
        for n in range(1, 65):
            term = -term * x2 / d_cls((2 * n - 1) * (2 * n))
            s += term
        return s

    k1 = d_cls("1.8751040687119611664453082410782")
    for _ in range(25):
        f_val = d_cls(1) + d_cosh(k1) * d_cos(k1)
        fp_val = d_sinh(k1) * d_cos(k1) - d_cosh(k1) * d_sin(k1)
        k1 -= f_val / fp_val

    t1 = d_sinh(k1 / d_cls(2)) / d_cosh(k1 / d_cls(2))
    sigma2_inf = d_cls(3) / d_cls(16) - (t1 * t1) / (k1 * k1)
    mu3_inf = (
        d_cls(3) / d_cls(32)
        - d_cls(9) * (t1 * t1) / (d_cls(8) * k1 * k1)
        + d_cls(3) * t1 / (d_cls(4) * (k1**3))
    )
    mu4_inf = (
        d_cls(21) / d_cls(256)
        - d_cls(6) / (k1**4)
        + d_cls(27) * t1 / (d_cls(4) * (k1**3))
        - d_cls(9) * (t1 * t1) / (d_cls(4) * k1 * k1)
    )
    kappa4_inf = mu4_inf / (sigma2_inf * sigma2_inf)
    gamma2_inf = kappa4_inf - d_cls(3)
    pure_mode_barycenter_clamped0 = d_cls(1) / d_cls(2) + d_cls(2) * (t1 * t1) / (k1 * k1)
    pure_mode_barycenter_clamped1 = d_cls(1) - pure_mode_barycenter_clamped0

    return {
        "kappa_1_50d": str(k1)[:52],
        "t1_50d": str(t1)[:52],
        "sigma2_inf_50d": str(sigma2_inf)[:52],
        "mu3_cent_inf_50d": str(mu3_inf)[:52],
        "mu4_cent_inf_50d": str(mu4_inf)[:52],
        "kurtosis_kappa4_inf_50d": str(kappa4_inf)[:52],
        "excess_kurtosis_gamma2_inf_50d": str(gamma2_inf)[:53],
        "pure_mode_barycenter_clamped0_50d": str(pure_mode_barycenter_clamped0)[:52],
        "pure_mode_barycenter_clamped1_50d": str(pure_mode_barycenter_clamped1)[:52],
    }


def main() -> None:
    g_polys = build_exact_resolvent_density_series(18)
    w_1 = [Fraction(1)]
    w_u4 = [Fraction(1), Fraction(-8), Fraction(24), Fraction(-32), Fraction(16)]
    w_u5 = [Fraction(-1), Fraction(10), Fraction(-40), Fraction(80), Fraction(-80), Fraction(32)]
    w_u6 = [Fraction(1), Fraction(-12), Fraction(60), Fraction(-160), Fraction(240), Fraction(-192), Fraction(64)]
    w_c4 = [Fraction(1, 256), Fraction(-1, 16), Fraction(3, 8), Fraction(-1, 1), Fraction(1, 1)]

    z_coeffs = [int_0_1_poly_times(gn, w_1) for gn in g_polys]
    u4_series = series_div([int_0_1_poly_times(gn, w_u4) for gn in g_polys], z_coeffs, 8)
    u5_series = series_div([int_0_1_poly_times(gn, w_u5) for gn in g_polys], z_coeffs, 8)
    u6_series = series_div([int_0_1_poly_times(gn, w_u6) for gn in g_polys], z_coeffs, 8)
    mu4_series = series_div([int_0_1_poly_times(gn, w_c4) for gn in g_polys], z_coeffs, 8)

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

    s_minus_1 = math.cosh(k1) * math.sin(k1) - math.sinh(k1) * math.cos(k1)
    n_grid = 4000
    h = 1.0 / n_grid

    def rho_hat_inf(x: float) -> float:
        u = 2.0 * x - 1.0
        num = (
            math.sinh(k1 * x) * math.sin(k1 * x)
            + math.sinh(k1 * (1.0 - x)) * math.sin(k1 * (1.0 - x))
            - 0.5 * (math.sinh(k1) * math.sin(k1 * u) + math.sin(k1) * math.sinh(k1 * u))
        )
        return (k1 / s_minus_1) * num

    def minus_quarter_d_psi1_sq(x: float) -> float:
        """Evaluate -(1/4) * d/dx [psi_hat_1(x)^2] = (1/2) * phi_1(1-x) * phi_1'(1-x)."""
        u = 1.0 - x
        phi = (math.cosh(k1 * u) - math.cos(k1 * u)) - t1 * (math.sinh(k1 * u) - math.sin(k1 * u))
        dphi = k1 * (
            (math.sinh(k1 * u) + math.sin(k1 * u)) - t1 * (math.cosh(k1 * u) - math.cos(k1 * u))
        )
        return 0.5 * phi * dphi

    def psi1_clamped1_sq(x: float) -> float:
        u = 1.0 - x
        val = (math.cosh(k1 * u) - math.cos(k1 * u)) - t1 * (math.sinh(k1 * u) - math.sin(k1 * u))
        return val * val

    def phi1_clamped0_sq(u: float) -> float:
        val = (math.cosh(k1 * u) - math.cos(k1 * u)) - t1 * (math.sinh(k1 * u) - math.sin(k1 * u))
        return val * val

    def simpson(fn) -> float:
        total = fn(0.0) + fn(1.0)
        for i in range(1, n_grid):
            total += (4.0 if i % 2 == 1 else 2.0) * fn(i * h)
        return total * h / 3.0

    # 1. Verify Exact Derivative Law rho_hat_inf(x) == -(1/4) * d/dx[psi_hat_1(x)^2] on grid:
    max_deriv_law_diff = max(
        abs(rho_hat_inf(i * h) - minus_quarter_d_psi1_sq(i * h)) for i in range(n_grid + 1)
    )
    assert max_deriv_law_diff < 5e-15

    # 2. Verify Free-End Slope Resonance rho_hat_inf(0) == phi_1'(1) = 2 * k1 * tanh(k1/2):
    phi1_prime_1 = k1 * (
        (math.sinh(k1) + math.sin(k1)) - t1 * (math.cosh(k1) - math.cos(k1))
    )
    free_end_resonance_diff = abs(rho_hat_inf(0.0) - phi1_prime_1)
    assert free_end_resonance_diff < 5e-15

    # 3. Verify Universal Moment Shift Law E_{rho_hat_inf}[x^p] == (p/4) * E_{psi_hat_1^2}[x^{p-1}]:
    moment_shift_diffs = {}
    for p in range(1, 6):
        lhs = simpson(lambda x, p=p: (x**p) * rho_hat_inf(x))
        rhs = (p / 4.0) * simpson(lambda x, p=p: (x ** (p - 1)) * psi1_clamped1_sq(x))
        moment_shift_diffs[f"p={p}"] = abs(lhs - rhs)
        assert moment_shift_diffs[f"p={p}"] < 5e-15

    # 4. Verify Bilateral MGF Duality int_0^1 e^{s(2x-1)} psi_hat_1(x)^2 dx == 2*(M_inf(s) - e^{-s})/s:
    s_test = 0.4
    m_inf_s = (
        k1
        * (
            t1 * (s_test**3) * math.sinh(s_test)
            - 0.5 * k1 * (t1**2) * (s_test**2) * math.cosh(s_test)
            + 0.25 * (k1**3) * math.cosh(s_test)
        )
        / (s_test**4 + 0.25 * (k1**4))
        - k1
        * (
            t1 * (s_test**3) * math.cosh(s_test)
            - 0.5 * k1 * (t1**2) * (s_test**2) * math.sinh(s_test)
            - 0.5 * (k1**3) * math.sinh(s_test)
        )
        / (s_test**4 - (k1**4))
    )
    mgf_psi1_sq_quad = simpson(lambda x: math.exp(s_test * (2.0 * x - 1.0)) * psi1_clamped1_sq(x))
    mgf_psi1_sq_duality = 2.0 * (m_inf_s - math.exp(-s_test)) / s_test
    mgf_duality_diff = abs(mgf_psi1_sq_quad - mgf_psi1_sq_duality)
    assert mgf_duality_diff < 5e-15

    quad_mass = simpson(rho_hat_inf)
    quad_mean = simpson(lambda x: x * rho_hat_inf(x))
    quad_mu4 = simpson(lambda x: ((x - 0.25) ** 4) * rho_hat_inf(x))
    quad_phi1_mass = simpson(phi1_clamped0_sq)
    quad_phi1_mean = simpson(lambda u: u * phi1_clamped0_sq(u))
    virial_phi1_mean = 0.5 + 2.0 * (t1**2) / (k1**2)
    bridge_sigma2 = 7.0 / 16.0 - 0.5 * virial_phi1_mean

    assert abs(quad_mass - 1.0) < 1e-14
    assert abs(quad_mean - 0.25) < 1e-14
    assert abs(quad_mu4 - mu4_cent_inf) < 1e-14
    assert abs(quad_phi1_mass - 1.0) < 1e-14
    assert abs(quad_phi1_mean - virial_phi1_mean) < 1e-14
    assert abs(bridge_sigma2 - sigma2_inf) < 1e-16

    hp50 = high_precision_50_digits()

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
            "pure_mode_barycenter_clamped0": virial_phi1_mean,
            "pure_mode_barycenter_quad_abs_diff": abs(quad_phi1_mean - virial_phi1_mean),
            "affine_bridge_sigma2_abs_diff": abs(bridge_sigma2 - sigma2_inf),
            "exact_derivative_law_max_abs_diff": max_deriv_law_diff,
            "free_end_slope_resonance_abs_diff": free_end_resonance_diff,
            "moment_shift_law_abs_diffs": moment_shift_diffs,
            "mgf_duality_abs_diff": mgf_duality_diff,
        },
        "high_precision_50_digits": hp50,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
