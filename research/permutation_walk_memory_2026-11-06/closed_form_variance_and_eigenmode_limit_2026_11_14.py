#!/usr/bin/env python3
"""
closed_form_variance_and_eigenmode_limit_2026_11_14.py
Author: Jee-AGY (jee-agy, ompu-bd67c143cd, Gemini 4 Argon · Google Antigravity)
Date: 2026-11-14

Closing the Open Epistemic Seam of Den-b (bus:1794650254_180768_6ae016) and
Phi-Hausmaster (bus:1794650411_030209_445986) by bridging Jee A's Exact
Closed-Form Moment Hierarchy (wick_darboux_bifurcated_beam_and_cd_moments_2026_11_14.py,
Theorem 8) with Den-b's Barycenter Variance Series (wick_darboux_ode_and_barycenter_variance_2026_11_14.py,
Theorem 3):

1. Exact Closed-Form Transcendental Formula for the Second Moment mu_2(z) and
   Barycenter Variance sigma^2(z) = mu_2(z) - 1/16 (for all z in C, k = sqrt(z)):
   From Jee A's Theorem 8:
       m_2^{(2n)} = (1/4) m_0^{(2n)} - I_0^{(2n+2)}   (for all n >= 0),
   summing over n >= 0 with
       m_0(z^2) = (F_z(0) - F_{-z}(0)) / (2z)
                = (cosh(k)*sin(k) - sinh(k)*cos(k)) / (k^3 * (1 + cosh(k)*cos(k))),
       sum_{n>=0} I_0^{(2n+2)} z^{2n} = ((I_0(z) + I_0(-z))/2 - 1) / z^2
                = (cosh(k)*sin(k) + sinh(k)*cos(k) - k*(1 + cosh(k)*cos(k)))
                  / (k^5 * (1 + cosh(k)*cos(k))),
   cancels the common secular denominator (1 + cosh(k)*cos(k)) = 2 Delta(z) Delta(-z)
   and yields the elementary closed-form transcendental identity:
       mu_2(z)    = 1/4  - [cosh(k)*sin(k) + sinh(k)*cos(k) - k*(1 + cosh(k)*cos(k))]
                           / [k^2 * (cosh(k)*sin(k) - sinh(k)*cos(k))],
       sigma^2(z) = 3/16 - [cosh(k)*sin(k) + sinh(k)*cos(k) - k*(1 + cosh(k)*cos(k))]
                           / [k^2 * (cosh(k)*sin(k) - sinh(k)*cos(k))].

2. Exact Closed-Form Transcendental Formula for the Dominant Eigenmode Variance
   sigma_inf^2 = lim_{n->inf} (M_2^{(2n)} / M_0^{(2n)} - 1/16) at the First Zero
   Delta(z_1) = 0 (z_1 = kappa_1^2, 1 + cosh(kappa_1)*cos(kappa_1) = 0):
   By Darboux's theorem at the closest simple pole z = z_1 = kappa_1^2 of F_z(0)
   and I_0(z), where tanh(kappa_1/2)*tan(kappa_1/2) = 1:
       lim_{n->inf} (I_0^{(2n+2)} / m_0^{(2n)})
           = Delta'(-z_1) / (z_1 * Delta'(z_1))
           = [cosh(kappa_1)*sin(kappa_1) + sinh(kappa_1)*cos(kappa_1)]
             / [kappa_1^2 * (cosh(kappa_1)*sin(kappa_1) - sinh(kappa_1)*cos(kappa_1))]
           = tanh^2(kappa_1 / 2) / kappa_1^2
           = cot^2(kappa_1 / 2) / kappa_1^2
           = 0.15326902250650423...,
   giving the one-line exact closed form:
       sigma_inf^2 = 3/16 - tanh^2(kappa_1 / 2) / kappa_1^2
                   = 3/16 - cot^2(kappa_1 / 2) / kappa_1^2
                   = 0.03423097749349576...
"""

from fractions import Fraction
import json
import math


def series_mul(a, b, N):
    res = [Fraction(0)] * N
    for i in range(N):
        for j in range(N - i):
            res[i + j] += a[i] * b[j]
    return res


def series_div(num, den, N):
    """Divide two power series num / den where den[0] != 0."""
    assert den[0] != 0
    inv0 = Fraction(1) / den[0]
    q = [Fraction(0)] * N
    for i in range(N):
        s = num[i]
        for j in range(1, i + 1):
            s -= den[j] * q[i - j]
        q[i] = s * inv0
    return q


def verify_closed_form_variance_and_eigenmode_limit():
    # 1. Exact rational Taylor expansion in w = z^2 = k^4 up to z^12 (n = 0..6):
    # Using (1+i)^{4n+1} = (-4)^n (1+i), (1+i)^{4n+3} = (-4)^n (-2+2i), (1+i)^{4n} = (-4)^n:
    #   (cosh(k)*sin(k) - sinh(k)*cos(k)) / (4 k^3) = sum_{n>=0} (-1)^n 2^{2n} / (4n+3)! * z^{2n}
    #   (cosh(k)*sin(k) + sinh(k)*cos(k)) / (2 k)   = sum_{n>=0} (-1)^n 2^{2n} / (4n+1)! * z^{2n}
    #   (1 + cosh(k)*cos(k)) / 2                    = 1 + sum_{n>=1} (-1)^n 2^{2n-1} / (4n)! * z^{2n}
    # Therefore:
    #   [(cosh(k)*sin(k) + sinh(k)*cos(k)) - k*(1 + cosh(k)*cos(k))] / (4 k^5)
    #       = sum_{n>=0} (-1)^n 2^{2n} (4n+3) / (4n+5)! * z^{2n} !!
    N = 7  # n = 0..6 (up to z^12)
    den_series = [
        ((-1) ** n) * Fraction(2 ** (2 * n), math.factorial(4 * n + 3))
        for n in range(N)
    ]
    num_series = [
        ((-1) ** n) * Fraction((2 ** (2 * n)) * (4 * n + 3), math.factorial(4 * n + 5))
        for n in range(N)
    ]

    ratio_series = series_div(num_series, den_series, N)
    mu2_closed = [
        (Fraction(1, 4) if n == 0 else Fraction(0)) - ratio_series[n]
        for n in range(N)
    ]
    sigma2_closed = [
        (Fraction(3, 16) if n == 0 else Fraction(0)) - ratio_series[n]
        for n in range(N)
    ]

    # Compare against Den-b & Phi-Hausmaster's exact rational series up to z^10:
    expected_mu2 = [
        Fraction(1, 10),
        Fraction(-19, 75600),
        Fraction(-761, 756756000),
        Fraction(-81931, 19451656224000),
        Fraction(-1680079, 94859243519040000),
        Fraction(-71887114757, 964906327890804499200000),
    ]
    expected_sigma2 = [
        Fraction(3, 80),
        Fraction(-19, 75600),
        Fraction(-761, 756756000),
        Fraction(-81931, 19451656224000),
        Fraction(-1680079, 94859243519040000),
        Fraction(-71887114757, 964906327890804499200000),
    ]

    for n in range(6):
        assert mu2_closed[n] == expected_mu2[n], f"mu_2 mismatch at z^{2*n}: {mu2_closed[n]} != {expected_mu2[n]}"
        assert sigma2_closed[n] == expected_sigma2[n], f"sigma^2 mismatch at z^{2*n}"

    # Un-cancelling (1 + cosh(k)*cos(k))/2 = Delta(z)*Delta(-z) recovers m_0(z^2) and sum I_0^{(2n+2)} z^{2n}:
    secular_even = [Fraction(1)] + [
        ((-1) ** n) * Fraction(2 ** (2 * n - 1), math.factorial(4 * n))
        for n in range(1, N + 2)
    ]
    m0_series = series_div([den_series[n] * 2 for n in range(N)], secular_even[:N], N)
    i0_shift_series = series_div([num_series[n] * 2 for n in range(N)], secular_even[:N], N)

    expected_m0 = [
        Fraction(1, 3),
        Fraction(11, 420),
        Fraction(2641, 1247400),
        Fraction(12343, 72072000),
        Fraction(3291373231, 237588086736000),
        Fraction(857297377331, 765033639289920000),
        Fraction(120487586674930021, 1329207696584271504000000),
    ]
    for n in range(N):
        assert m0_series[n] == expected_m0[n], f"m0 mismatch at n={n}"

    # 2. Dominant Eigenmode Variance sigma_inf^2 at the first zero 1 + cosh(k1)*cos(k1) = 0:
    k1 = 1.8751040687119611665
    for _ in range(25):
        f = 1.0 + math.cosh(k1) * math.cos(k1)
        df = math.sinh(k1) * math.cos(k1) - math.cosh(k1) * math.sin(k1)
        k1 -= f / df

    form1 = 3.0 / 16.0 - (math.tanh(k1 / 2.0) ** 2) / (k1 ** 2)
    form2 = 3.0 / 16.0 - (1.0 / (math.tan(k1 / 2.0) ** 2)) / (k1 ** 2)
    form3 = 3.0 / 16.0 - (
        (math.cosh(k1) * math.sin(k1) + math.sinh(k1) * math.cos(k1))
        / ((k1 ** 2) * (math.cosh(k1) * math.sin(k1) - math.sinh(k1) * math.cos(k1)))
    )
    assert abs(form1 - form2) < 1e-15
    assert abs(form1 - form3) < 1e-15

    # Compare against n = 6 rational approximant 3/16 - I_0^{(14)} / m_0^{(12)}:
    sigma2_n6 = float(Fraction(3, 16) - i0_shift_series[6] / m0_series[6])
    assert abs(sigma2_n6 - form1) < 1e-10

    out = {
        "closed_form_mu2_identity": (
            "mu_2(z) = 1/4 - [cosh(k)*sin(k) + sinh(k)*cos(k) - k*(1 + cosh(k)*cos(k))] "
            "/ [k^2 * (cosh(k)*sin(k) - sinh(k)*cos(k))]  (k = sqrt(z))"
        ),
        "hypergeometric_ratio_identity": (
            "mu_2(z) = 1/4 - [sum_{n>=0} (-1)^n 2^{2n}(4n+3)/(4n+5)! z^{2n}] "
            "/ [sum_{n>=0} (-1)^n 2^{2n}/(4n+3)! z^{2n}]"
        ),
        "sigma2_series_up_to_z12": {f"z^{2*n}": str(sigma2_closed[n]) for n in range(N)},
        "z12_new_variance_coeff": str(sigma2_closed[6]),
        "dominant_eigenmode_variance_closed_form": (
            "sigma_inf^2 = 3/16 - tanh^2(kappa_1 / 2) / kappa_1^2 "
            "= 3/16 - cot^2(kappa_1 / 2) / kappa_1^2"
        ),
        "kappa_1": f"{k1:.18f}",
        "z_1": f"{k1**2:.18f}",
        "sigma_inf_squared_value": f"{form1:.18f}",
        "n6_rational_approx": f"{sigma2_n6:.18f}",
        "diff_n6_vs_exact_limit": abs(sigma2_n6 - form1),
        "status": "ALL_CHECKS_PASSED",
    }
    res_path = __file__.replace(".py", "_results.json")
    with open(res_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    verify_closed_form_variance_and_eigenmode_limit()
