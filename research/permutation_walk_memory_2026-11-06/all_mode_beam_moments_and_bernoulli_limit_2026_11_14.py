#!/usr/bin/env python3
"""
All-Mode Cantilever Hierarchy, Closed-Form Pure Euler-Bernoulli Beam Moments
(closing Phi's sigma^2 = 0.0241 datum in 1794671368), and Semiclassical
Bernoulli(1/4) vs Uniform([0,1]) Weak-Limit Duality.

Verifies independently using Python's built-in `decimal` (80-digit precision)
and `fractions.Fraction` + Simpson quadrature (zero external dependencies):

1. Midpoint Parity Factorization of all cantilever eigenvalues (r >= 1):
     1 + cosh(k)*cos(k) = 2 * Delta(+k^2) * Delta(-k^2) = 0,
   where:
     - Odd modes  r = 1, 3, 5, ... : Delta(+kappa_r^2) = 0  (lambda_r = +kappa_r^-2 > 0),
       t_r := S_x(kappa_r)/S_-(kappa_r) = tanh(kappa_r/2) = cot(kappa_r/2),
       psi_hat_r(x) = cosh(kappa_r(x-1/2))/cosh(kappa_r/2) - sin(kappa_r(x-1/2))/sin(kappa_r/2);
     - Even modes r = 2, 4, 6, ... : Delta(-kappa_r^2) = 0  (lambda_r = -kappa_r^-2 < 0),
       t_r := S_x(kappa_r)/S_-(kappa_r) = coth(kappa_r/2) = -tan(kappa_r/2),
       psi_hat_r(x) = cos(kappa_r(x-1/2))/cos(kappa_r/2) - sinh(kappa_r(x-1/2))/sinh(kappa_r/2).

2. All-Mode Continuum Wick Companion & Pole Derivative Law (for ALL r >= 1):
     F_{-lambda_r^-1}(x) == -(lambda_r / 2) * psi_hat_r'(x),
     rho_hat_r(x) := lim_{z -> lambda_r^-1} rho_{z^2}(x) / m_0(z^2)
                  == -(1/4) * d/dx [psi_hat_r(x)^2],
     rho_hat_r(0) == -psi_hat_r'(0) == 2 * kappa_r * t_r,
   where rho_hat_1 >= 0 is a probability density while for r >= 2 rho_hat_r is a
   signed unit-mass distribution with invariant barycenter E_{rho_hat_r}[x] == 1/4.

3. Closed-Form Pure Euler-Bernoulli Cantilever Eigenmode Moments (r >= 1):
   Via E_{psi_hat_r^2}[x^q] = (4/(q+1)) * E_{rho_hat_r}[x^{q+1}] (q = 1, 2, 3):
     E_{psi_hat_r^2}[x]   = 1/2 - 2*t_r^2 / kappa_r^2,
     E_{psi_hat_r^2}[x^2] = 1/3 - (5/2)*t_r^2 / kappa_r^2 + t_r / kappa_r^3,
     E_{psi_hat_r^2}[x^3] = E_{rho_hat_r}[x^4]
                          = 1/4 - (15/4)*t_r^2 / kappa_r^2 + (15/2)*t_r / kappa_r^3 - 6 / kappa_r^4,
     sigma^2(psi_hat_r^2) = 1/12 - t_r^2 / (2*kappa_r^2) + t_r / kappa_r^3 - 4*t_r^4 / kappa_r^4,
     mu_3^cent(psi_hat_r^2) = -t_r^2 / kappa_r^2 + 6*t_r / kappa_r^3
                              - (6 + 3*t_r^4) / kappa_r^4 + 6*t_r^3 / kappa_r^5 - 16*t_r^6 / kappa_r^6.
   At r = 1, sigma^2(psi_hat_1^2) = 0.02407971602667635170195589583600701865023549845990...,
   closing Phi-Hausmaster's empirical pure-beam datum `sigma^2 = 0.0241` in 1794671368.

4. Semiclassical Weak-Limit Duality (r -> infinity):
   While psi_hat_r(x)^2 dx -> Uniform([0, 1]) weakly in C([0, 1])* (mean 1/2, var 1/12, mu_3 = 0),
   rho_hat_r(x) dx = -(1/4) d[psi_hat_r(x)^2] converges weakly in C^1([0, 1])* to the two-atom
   endpoint measure (3/4)*delta_0 + (1/4)*delta_1 = Bernoulli(1/4), whose central moments
   0, 3/16, 3/32, 21/256, 15/256, 183/4096, ... explain the leading kappa_r^0 constants
   of all central moments of rho_hat_r at once.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 85

PI_DEC = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628"
)


def dec_cos(x: Decimal) -> Decimal:
    x2 = x * x
    term = Decimal(1)
    s = term
    k = 1
    while abs(term) > Decimal("1e-80"):
        term = -term * x2 / Decimal((2 * k - 1) * (2 * k))
        s += term
        k += 1
    return s


def dec_sin(x: Decimal) -> Decimal:
    x2 = x * x
    term = x
    s = term
    k = 1
    while abs(term) > Decimal("1e-80"):
        term = -term * x2 / Decimal((2 * k) * (2 * k + 1))
        s += term
        k += 1
    return s


def dec_cosh(x: Decimal) -> Decimal:
    return (x.exp() + (-x).exp()) / Decimal(2)


def dec_sinh(x: Decimal) -> Decimal:
    return (x.exp() - (-x).exp()) / Decimal(2)


def find_kappa_dec(r: int) -> Decimal:
    x = Decimal(2 * r - 1) * PI_DEC / Decimal(2)
    for _ in range(50):
        f = Decimal(1) + dec_cosh(x) * dec_cos(x)
        df = dec_sinh(x) * dec_cos(x) - dec_cosh(x) * dec_sin(x)
        x = x - f / df
    return x


def eval_F_resolvent(z: float, x: float) -> float:
    """Exact continuum resolvent profile F_z(x) = ((I - z T)^-1 f_1)(x) (F_z(1)=0, F_z'(1)=-1)."""
    w = x - 0.5
    if z > 0:
        k = math.sqrt(z)
        kh = 0.5 * k
        delta = math.cosh(kh) * math.cos(kh) - math.sinh(kh) * math.sin(kh)
        num = math.sin(kh) * math.cosh(k * w) - math.cosh(kh) * math.sin(k * w)
        return num / (k * delta)
    else:
        k = math.sqrt(-z)
        kh = 0.5 * k
        delta = math.cosh(kh) * math.cos(kh) + math.sinh(kh) * math.sin(kh)
        num = math.sinh(kh) * math.cos(k * w) - math.cos(kh) * math.sinh(k * w)
        return num / (k * delta)


def verify_fraction_polynomials() -> dict:
    def add(A, B, scale=Fraction(1)):
        R = dict(A)
        for key, val in B.items():
            R[key] = R.get(key, Fraction(0)) + scale * val
            if R[key] == 0:
                del R[key]
        return R

    def mul(A, B):
        R = {}
        for (a1, b1), v1 in A.items():
            for (a2, b2), v2 in B.items():
                key = (a1 + a2, b1 + b2)
                R[key] = R.get(key, Fraction(0)) + v1 * v2
                if R[key] == 0:
                    del R[key]
        return R

    sig2_rho = {(0, 0): Fraction(3, 16), (2, 2): Fraction(-1, 1)}
    mu3_rho = {(0, 0): Fraction(3, 32), (2, 2): Fraction(-9, 8), (3, 1): Fraction(3, 4)}
    mu4_rho = {
        (0, 0): Fraction(21, 256),
        (4, 0): Fraction(-6, 1),
        (3, 1): Fraction(27, 4),
        (2, 2): Fraction(-9, 4),
    }

    m2_rho = add(sig2_rho, {(0, 0): Fraction(1, 16)})
    m3_rho = add(mu3_rho, add(mul({(0, 0): Fraction(3, 4)}, sig2_rho), {(0, 0): Fraction(1, 64)}))
    m4_rho = add(
        mu4_rho,
        add(mu3_rho, add(mul({(0, 0): Fraction(3, 8)}, sig2_rho), {(0, 0): Fraction(1, 256)})),
    )

    b1 = mul({(0, 0): Fraction(2, 1)}, m2_rho)
    b2 = mul({(0, 0): Fraction(4, 3)}, m3_rho)
    b3 = m4_rho

    sig2_beam = add(b2, mul(b1, b1), Fraction(-1, 1))
    mu3_beam = add(add(b3, mul(b1, b2), Fraction(-3, 1)), mul(b1, mul(b1, b1)), Fraction(2, 1))

    assert sig2_beam == {
        (0, 0): Fraction(1, 12),
        (2, 2): Fraction(-1, 2),
        (3, 1): Fraction(1, 1),
        (4, 4): Fraction(-4, 1),
    }
    assert mu3_beam == {
        (2, 2): Fraction(-1, 1),
        (3, 1): Fraction(6, 1),
        (4, 0): Fraction(-6, 1),
        (4, 4): Fraction(-3, 1),
        (5, 3): Fraction(6, 1),
        (6, 6): Fraction(-16, 1),
    }

    # Verify Bernoulli(1/4) central moments match leading kappa_r^0 constants
    bern = {}
    for p in range(1, 7):
        val = Fraction(3, 4) * (Fraction(-1, 4) ** p) + Fraction(1, 4) * (Fraction(3, 4) ** p)
        bern[f"p={p}"] = str(val)
    assert bern["p=1"] == "0"
    assert bern["p=2"] == "3/16"
    assert bern["p=3"] == "3/32"
    assert bern["p=4"] == "21/256"
    return {"bernoulli_quarter_central_moments": bern}


def verify_all_modes() -> dict:
    poly_info = verify_fraction_polynomials()
    mode_results = {}

    for r in (1, 2, 3, 4):
        kr = find_kappa_dec(r)
        kh = kr / Decimal(2)
        tanh_kh = dec_sinh(kh) / dec_cosh(kh)
        coth_kh = Decimal(1) / tanh_kh
        Sx = dec_sinh(kr) * dec_sin(kr)
        Sm = dec_cosh(kr) * dec_sin(kr) - dec_sinh(kr) * dec_cos(kr)
        Sp = dec_cosh(kr) * dec_sin(kr) + dec_sinh(kr) * dec_cos(kr)

        tr = Sx / Sm
        expected_tr = tanh_kh if (r % 2 == 1) else coth_kh
        assert abs(tr - expected_tr) < Decimal("1e-74")
        assert abs(Sp / Sm - tr * tr) < Decimal("1e-74")

        delta_plus = dec_cosh(kh) * dec_cos(kh) - dec_sinh(kh) * dec_sin(kh)
        delta_minus = dec_cosh(kh) * dec_cos(kh) + dec_sinh(kh) * dec_sin(kh)
        if r % 2 == 1:
            assert abs(delta_plus) < Decimal("1e-73")
        else:
            assert abs(delta_minus) < Decimal("1e-73")

        # Exact closed-form moments in 80-digit Decimal
        b1 = Decimal(1) / Decimal(2) - Decimal(2) * (tr * tr) / (kr * kr)
        sig2_beam = (
            Decimal(1) / Decimal(12)
            - (tr * tr) / (Decimal(2) * kr * kr)
            + tr / (kr ** 3)
            - Decimal(4) * (tr ** 4) / (kr ** 4)
        )
        mu3_beam = (
            -(tr * tr) / (kr * kr)
            + Decimal(6) * tr / (kr ** 3)
            - (Decimal(6) + Decimal(3) * (tr ** 4)) / (kr ** 4)
            + Decimal(6) * (tr ** 3) / (kr ** 5)
            - Decimal(16) * (tr ** 6) / (kr ** 6)
        )
        skew_beam = mu3_beam / (sig2_beam.sqrt() ** 3)

        # Continuum profile, Wick companion, and pole derivative checks on grid + Simpson quadrature
        kf = float(kr)
        lam_r = (1.0 if (r % 2 == 1) else -1.0) / (kf * kf)
        z_pole = 1.0 / lam_r

        def psi_hat(x: float) -> float:
            w = x - 0.5
            if r % 2 == 1:
                return math.cosh(kf * w) / math.cosh(0.5 * kf) - math.sin(kf * w) / math.sin(0.5 * kf)
            else:
                return math.cos(kf * w) / math.cos(0.5 * kf) - math.sinh(kf * w) / math.sinh(0.5 * kf)

        def psi_hat_prime(x: float) -> float:
            w = x - 0.5
            if r % 2 == 1:
                return kf * (
                    math.sinh(kf * w) / math.cosh(0.5 * kf) - math.cos(kf * w) / math.sin(0.5 * kf)
                )
            else:
                return kf * (
                    -math.sin(kf * w) / math.cos(0.5 * kf) - math.cosh(kf * w) / math.sinh(0.5 * kf)
                )

        def rho_pole_explicit(x: float) -> float:
            num = (
                math.sinh(kf * x) * math.sin(kf * x)
                + math.sinh(kf * (1.0 - x)) * math.sin(kf * (1.0 - x))
                - 0.5
                * (
                    math.sinh(kf) * math.sin(kf * (2.0 * x - 1.0))
                    + math.sin(kf) * math.sinh(kf * (2.0 * x - 1.0))
                )
            )
            den_m0 = (math.cosh(kf) * math.sin(kf) - math.sinh(kf) * math.cos(kf)) / kf
            return num / den_m0

        max_wick_diff = 0.0
        max_deriv_diff = 0.0
        for j in range(201):
            xg = j / 200.0
            f_comp = eval_F_resolvent(-z_pole, xg)
            wick_rhs = -0.5 * lam_r * psi_hat_prime(xg)
            max_wick_diff = max(max_wick_diff, abs(f_comp - wick_rhs))
            deriv_rhs = -0.5 * psi_hat(xg) * psi_hat_prime(xg)
            max_deriv_diff = max(max_deriv_diff, abs(rho_pole_explicit(xg) - deriv_rhs))

        assert max_wick_diff < 1e-13, (r, max_wick_diff)
        assert max_deriv_diff < 1e-12, (r, max_deriv_diff)
        assert abs(rho_pole_explicit(0.0) - float(Decimal(2) * kr * tr)) < 1e-12

        # Simpson quadrature of pure beam psi_hat_r(x)^2 on [0, 1]
        N = 20000
        h = 1.0 / N
        vals = [psi_hat(j * h) ** 2 for j in range(N + 1)]

        def simp(weight_fn):
            total = weight_fn(0.0) * vals[0] + weight_fn(1.0) * vals[N]
            for j in range(1, N):
                w = 4.0 if (j % 2 == 1) else 2.0
                total += w * weight_fn(j * h) * vals[j]
            return total * h / 3.0

        norm = simp(lambda x: 1.0)
        assert abs(norm - 1.0) < 1e-12
        b1_num = simp(lambda x: x)
        sig2_num = simp(lambda x: (x - b1_num) ** 2)
        mu3_num = simp(lambda x: (x - b1_num) ** 3)

        assert abs(float(b1) - b1_num) < 1e-12
        assert abs(float(sig2_beam) - sig2_num) < 1e-12
        assert abs(float(mu3_beam) - mu3_num) < 1e-12

        # Bilateral MGF duality check at s = 0.7 for mode r:
        s_val = 0.7
        tr_f = float(tr)
        mgf_rho = (
            kf
            * (
                tr_f * (s_val ** 3) * math.sinh(s_val)
                - 0.5 * kf * (tr_f ** 2) * (s_val ** 2) * math.cosh(s_val)
                + 0.25 * (kf ** 3) * math.cosh(s_val)
            )
            / (s_val ** 4 + 0.25 * (kf ** 4))
            - kf
            * (
                tr_f * (s_val ** 3) * math.cosh(s_val)
                - 0.5 * kf * (tr_f ** 2) * (s_val ** 2) * math.sinh(s_val)
                - 0.5 * (kf ** 3) * math.sinh(s_val)
            )
            / (s_val ** 4 - (kf ** 4))
        )
        mgf_beam_formula = 2.0 * (mgf_rho - math.exp(-s_val)) / s_val
        mgf_beam_quad = simp(lambda x: math.exp(s_val * (2.0 * x - 1.0)))
        assert abs(mgf_beam_formula - mgf_beam_quad) < 1e-12

        mode_results[f"r={r}"] = {
            "parity_branch": "Delta(+kappa_r^2)=0, t_r=tanh(kappa_r/2)"
            if (r % 2 == 1)
            else "Delta(-kappa_r^2)=0, t_r=coth(kappa_r/2)",
            "kappa_r_50d": str(kr)[:52],
            "t_r_50d": str(tr)[:52],
            "pure_beam_barycenter_50d": str(b1)[:52],
            "pure_beam_sigma2_50d": str(sig2_beam)[:52],
            "pure_beam_mu3_cent_50d": str(mu3_beam)[:52],
            "pure_beam_skewness_50d": str(skew_beam)[:52],
            "max_wick_companion_diff": max_wick_diff,
            "max_pole_derivative_diff": max_deriv_diff,
            "mgf_beam_duality_diff_s_0_7": abs(mgf_beam_formula - mgf_beam_quad),
        }

    # Check high-mode r=30 convergence to Uniform([0,1]) vs Bernoulli(1/4)
    k30 = find_kappa_dec(30)
    t30 = Decimal(1) / (dec_sinh(k30 / 2) / dec_cosh(k30 / 2))  # r=30 even -> coth
    sig2_rho_30 = Decimal(3) / Decimal(16) - (t30 * t30) / (k30 * k30)
    sig2_beam_30 = (
        Decimal(1) / Decimal(12)
        - (t30 * t30) / (Decimal(2) * k30 * k30)
        + t30 / (k30 ** 3)
        - Decimal(4) * (t30 ** 4) / (k30 ** 4)
    )
    assert abs(sig2_rho_30 - Decimal(3) / Decimal(16)) < Decimal("2e-4")
    assert abs(sig2_beam_30 - Decimal(1) / Decimal(12)) < Decimal("1e-4")

    return {
        "status": "ALL_CHECKS_PASSED",
        **poly_info,
        "modes_r_1_to_4": mode_results,
        "semiclassical_r30_check": {
            "kappa_30": float(k30),
            "sigma2_rho_30_vs_3_16": float(abs(sig2_rho_30 - Decimal(3) / Decimal(16))),
            "sigma2_beam_30_vs_1_12": float(abs(sig2_beam_30 - Decimal(1) / Decimal(12))),
        },
    }


if __name__ == "__main__":
    print(json.dumps(verify_all_modes(), indent=2))
