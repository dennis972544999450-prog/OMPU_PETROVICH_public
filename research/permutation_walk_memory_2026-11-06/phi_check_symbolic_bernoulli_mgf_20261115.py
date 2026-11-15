#!/usr/bin/env python3
"""
Phi's independent second hand on Petrovich's 1794732060 symbolic closure:
  rho_hat_r -> Bernoulli(1/4), psi_hat_r^2 -> Uniform([0,1]),
  universal monotone-from-below law mu_p^cent for ALL p >= 2.

Independent means: NOT re-running his hardcoded coefficient tuples against
themselves. Instead:
  (A) Re-DERIVE the central-moment coefficients c0(p), c2(p) by extracting
      [xi^p / p!] from the Laurent-in-kappa expansion of M_r^cent(xi) with my
      own exact rational Taylor engine, and match BOTH the closed form AND his
      asserted tuples for p=2..6.
  (B) Prove the sign c2(p) < 0 for ALL p>=2 from the elementary inequality
      5*3^(p-2) + 3*(-1)^p >= 2 > 0, checked p=2..60.
  (C) The load-bearing closure: confirm his CLOSED-FORM two-sided MGF M_r(s)
      actually EQUALS the genuine MGF of the real spectral density, i.e.
      M_r(s) == integral_0^1 e^{s(2x-1)} rho_hat_r(x) dx, by high-order Simpson
      quadrature of the REAL density, for several (r,s). If his closed form is
      the true MGF, the weak limit to Bernoulli(1/4) follows from (A).
  (D) The duality that gives Uniform: 2*(M_r(s) - e^{-s})/s -> sinh(s)/s,
      cancelling e^{-s}, verified numerically as r->inf.

Zero external deps (decimal + fractions + math). Run: python3 -I -B this.py
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80

PI_DEC = Decimal(
    "3.1415926535897932384626433832795028841971693993751058209749445923078164062862"
)


def dec_cos(x: Decimal) -> Decimal:
    x2 = x * x
    term = Decimal(1)
    s = term
    k = 1
    while abs(term) > Decimal("1e-76"):
        term = -term * x2 / Decimal((2 * k - 1) * (2 * k))
        s += term
        k += 1
    return s


def dec_sin(x: Decimal) -> Decimal:
    x2 = x * x
    term = x
    s = term
    k = 1
    while abs(term) > Decimal("1e-76"):
        term = -term * x2 / Decimal((2 * k) * (2 * k + 1))
        s += term
        k += 1
    return s


def dec_cosh(x: Decimal) -> Decimal:
    return (x.exp() + (-x).exp()) / Decimal(2)


def dec_sinh(x: Decimal) -> Decimal:
    return (x.exp() - (-x).exp()) / Decimal(2)


def find_kappa_dec(r: int) -> Decimal:
    """Root of 1 + cosh(k)cos(k) = 0 near (2r-1)pi/2 (clamped-free beam)."""
    x = Decimal(2 * r - 1) * PI_DEC / Decimal(2)
    for _ in range(60):
        f = Decimal(1) + dec_cosh(x) * dec_cos(x)
        df = dec_sinh(x) * dec_cos(x) - dec_cosh(x) * dec_sin(x)
        x = x - f / df
    return x


# ----------------------------------------------------------------------------
# (A) Independent extraction of central-moment coefficients via a rational
#     Taylor engine. A series is a dict {power: Fraction coefficient}.
# ----------------------------------------------------------------------------
PMAX = 12  # keep terms up to xi^PMAX


def exp_series(a: Fraction) -> dict:
    """Taylor of e^{a*xi} up to xi^PMAX: coeff of xi^n is a^n / n!."""
    out = {}
    fact = 1
    ap = Fraction(1)
    for n in range(PMAX + 1):
        if n > 0:
            fact *= n
            ap *= a
        out[n] = ap / fact
    return out


def scale(series: dict, c: Fraction) -> dict:
    return {n: c * v for n, v in series.items()}


def add(*series_list: dict) -> dict:
    out: dict = {}
    for s in series_list:
        for n, v in s.items():
            out[n] = out.get(n, Fraction(0)) + v
    return out


def mul_by_xi_power(series: dict, k: int) -> dict:
    return {n + k: v for n, v in series.items() if n + k <= PMAX}


def central_moment_from_series(series: dict, p: int) -> Fraction:
    """mu_p^cent = p! * [xi^p] series   (series is in variable xi)."""
    fact = 1
    for i in range(1, p + 1):
        fact *= i
    return Fraction(fact) * series.get(p, Fraction(0))


def derive_c0_c2() -> dict:
    """Build M_r^cent(xi) = e^{xi/4} * M_r(xi/2) order by order in 1/kappa.

    Leading (kappa^0):   e^{xi/4} * (3/4 e^{-xi/2} + 1/4 e^{+xi/2})
                       = 3/4 e^{-xi/4} + 1/4 e^{3xi/4}   -> c0(p)
    kappa^-2 * t^2:      e^{xi/4} * (-(xi/2)^2 (5 e^{xi/2}+3 e^{-xi/2})/4)
                       = -(xi^2/16)(5 e^{3xi/4} + 3 e^{-xi/4})   -> c2(p)
    Both built WITHOUT assuming the closed forms; then matched to them.
    """
    # Leading:
    lead = add(
        scale(exp_series(Fraction(-1, 4)), Fraction(3, 4)),
        scale(exp_series(Fraction(3, 4)), Fraction(1, 4)),
    )
    # kappa^-2 coefficient (the factor t_r^2/kappa_r^2 stripped off):
    c2term = scale(
        mul_by_xi_power(
            add(
                scale(exp_series(Fraction(3, 4)), Fraction(5)),
                scale(exp_series(Fraction(-1, 4)), Fraction(3)),
            ),
            2,
        ),
        Fraction(-1, 16),
    )

    rows = {}
    for p in range(2, PMAX + 1):
        c0 = central_moment_from_series(lead, p)
        c2 = central_moment_from_series(c2term, p)
        # closed forms claimed by Petrovich:
        c0_closed = Fraction(3 * ((-1) ** p) + 3 ** p, 4 ** (p + 1))
        c2_closed = -Fraction(p * (p - 1) * (5 * 3 ** (p - 2) + 3 * ((-1) ** p)), 4 ** p)
        assert c0 == c0_closed, (p, c0, c0_closed)
        assert c2 == c2_closed, (p, c2, c2_closed)
        rows[p] = (c0, c2)

    # Cross-check against his hardcoded tuples for p=2..6:
    expect = {
        2: (Fraction(3, 16), Fraction(-1)),
        3: (Fraction(3, 32), Fraction(-9, 8)),
        4: (Fraction(21, 256), Fraction(-9, 4)),
        5: (Fraction(15, 256), Fraction(-165, 64)),
        6: (Fraction(183, 4096), Fraction(-765, 256)),
    }
    for p, (c0e, c2e) in expect.items():
        assert rows[p] == (c0e, c2e), (p, rows[p], (c0e, c2e))

    # c0(p) must equal the DEFINITION of Bernoulli(1/4) central moment:
    #   (3/4)(0-1/4)^p + (1/4)(1-1/4)^p
    for p in range(2, PMAX + 1):
        bern = Fraction(3, 4) * Fraction(-1, 4) ** p + Fraction(1, 4) * Fraction(3, 4) ** p
        assert rows[p][0] == bern, (p, rows[p][0], bern)

    return {str(p): [str(rows[p][0]), str(rows[p][1])] for p in rows}


# ----------------------------------------------------------------------------
# (B) Sign of the kappa^-2 correction is strictly negative for ALL p>=2.
# ----------------------------------------------------------------------------
def prove_sign() -> dict:
    worst = None
    for p in range(2, 61):
        inner = 5 * 3 ** (p - 2) + 3 * ((-1) ** p)  # >= 5*1 - 3 = 2
        assert inner >= 2, (p, inner)
        c2 = -Fraction(p * (p - 1) * inner, 4 ** p)
        assert c2 < 0
        if worst is None or inner < worst[1]:
            worst = (p, inner)
    # the minimum of the inner factor is at the smallest odd p (p=3): 5*3-3=12?
    # actually p=2 (even): 5*1+3=8; p=3 (odd): 15-3=12; so min is p=2 -> 8.
    return {"checked_p": "2..60", "min_inner_factor": worst[1], "all_c2_negative": True}


# ----------------------------------------------------------------------------
# Real spectral density rho_hat_r(x) (general r; same analytic form as the
# r=1 density, with kappa = kappa_r). Derived from the clamped-free squared
# eigenfunctions of the turn operator T.
# ----------------------------------------------------------------------------
def rho_hat(kf: float, x: float) -> float:
    num = (
        math.sinh(kf * x) * math.sin(kf * x)
        + math.sinh(kf * (1.0 - x)) * math.sin(kf * (1.0 - x))
        - 0.5
        * (
            math.sinh(kf) * math.sin(kf * (2.0 * x - 1.0))
            + math.sin(kf) * math.sinh(kf * (2.0 * x - 1.0))
        )
    )
    den = (math.cosh(kf) * math.sin(kf) - math.sinh(kf) * math.cos(kf)) / kf
    return num / den


def mgf_quadrature(kf: float, s: float, N: int = 40000) -> float:
    """integral_0^1 e^{s(2x-1)} rho_hat_r(x) dx  by composite Simpson."""
    h = 1.0 / N
    acc = math.exp(s * (2 * 0.0 - 1)) * rho_hat(kf, 0.0) + math.exp(
        s * (2 * 1.0 - 1)
    ) * rho_hat(kf, 1.0)
    for j in range(1, N):
        w = 4.0 if (j % 2 == 1) else 2.0
        xg = j * h
        acc += w * math.exp(s * (2 * xg - 1)) * rho_hat(kf, xg)
    return acc * h / 3.0


def mgf_closed_form(kr: Decimal, r: int, s: Decimal) -> Decimal:
    """Petrovich's exact two-sided closed-form MGF M_r(s)."""
    kh = kr / 2
    tr = (dec_sinh(kh) / dec_cosh(kh)) if (r % 2 == 1) else (dec_cosh(kh) / dec_sinh(kh))
    even = (
        kr
        * (
            tr * (s ** 3) * dec_sinh(s)
            - (kr * tr * tr / 2) * (s ** 2) * dec_cosh(s)
            + (kr ** 3 / 4) * dec_cosh(s)
        )
        / (s ** 4 + (kr ** 4) / 4)
    )
    odd = (
        kr
        * (
            tr * (s ** 3) * dec_cosh(s)
            - (kr * tr * tr / 2) * (s ** 2) * dec_sinh(s)
            - (kr ** 3 / 2) * dec_sinh(s)
        )
        / (s ** 4 - (kr ** 4))
    )
    return even - odd


# ----------------------------------------------------------------------------
# (C) Does the closed-form MGF equal the TRUE MGF of the real density?
# ----------------------------------------------------------------------------
def check_closed_form_is_true_mgf() -> dict:
    out = {}
    for r in (1, 2, 3, 5):
        kr = find_kappa_dec(r)
        kf = float(kr)
        row = {}
        for s in (Decimal("-0.9"), Decimal("0.5"), Decimal("1.3")):
            cf = mgf_closed_form(kr, r, s)
            q = mgf_quadrature(kf, float(s))
            diff = abs(float(cf) - q)
            row[f"s={s}"] = {"closed": float(cf), "quad": q, "abs_diff": diff}
            # Simpson error on a smooth periodic-ish integrand with N=40000
            # is comfortably < 1e-7; demand agreement there.
            assert diff < 1e-6, (r, s, diff)
        out[f"r={r}"] = row
    return out


# ----------------------------------------------------------------------------
# (D) Duality -> Uniform: 2*(M_r(s) - e^{-s})/s -> sinh(s)/s as r->inf,
#     and the e^{-s} genuinely cancels at leading order.
# ----------------------------------------------------------------------------
def check_uniform_duality() -> dict:
    out = {}
    s = Decimal("0.8")
    m_unif = dec_sinh(s) / s
    prev = None
    for r in (2, 4, 8, 16, 32):
        kr = find_kappa_dec(r)
        mr = mgf_closed_form(kr, r, s)
        beam = Decimal(2) * (mr - (-s).exp()) / s
        diff = abs(beam - m_unif)
        out[f"r={r}"] = {"beam_mgf": float(beam), "unif_mgf": float(m_unif), "abs_diff": float(diff)}
        if prev is not None:
            # monotone decrease of the gap (O(kappa^-2) ~ O(r^-2))
            assert diff < prev, (r, diff, prev)
        prev = diff
    # Leading-order algebra: 2*(3/4 e^{-s} + 1/4 e^{s} - e^{-s})/s == sinh(s)/s
    lead = Decimal(2) * (Decimal(3) / 4 * (-s).exp() + Decimal(1) / 4 * s.exp() - (-s).exp()) / s
    assert abs(lead - m_unif) < Decimal("1e-70"), abs(lead - m_unif)
    out["leading_order_exact_cancellation_of_e^-s"] = float(abs(lead - m_unif))
    return out


if __name__ == "__main__":
    result = {
        "A_rederived_c0_c2_match_closed_form_and_hardcode": derive_c0_c2(),
        "B_sign_c2_strictly_negative_all_p": prove_sign(),
        "C_closed_form_equals_true_mgf_of_real_density": check_closed_form_is_true_mgf(),
        "D_duality_to_uniform": check_uniform_duality(),
        "VERDICT": "ALL_CONFIRMED",
    }
    print(json.dumps(result, indent=2))
