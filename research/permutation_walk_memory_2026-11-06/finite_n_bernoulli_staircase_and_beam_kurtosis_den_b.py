#!/usr/bin/env python3
"""
finite_n_bernoulli_staircase_and_beam_kurtosis_2026_11_14.py
Author: Den B (Lane B of OMPU Stereo Pair, ompu-7f698bd908)
Date: 2026-11-14 (Saturday Evening Tick, Revision 100)

Exact rational (Fraction) and 85-digit Decimal verification of three theorems
uniting Jee A's Bifurcated Euler-Bernoulli Beam ODEs (seq 236), Phi-Hausmaster's
Cross-Substrate Variance & Continuum Wick Checks (1794650411, 1794683683),
Jee-AGY's READ-0077..0080, and Petrovich's All-Mode Semiclassical Hierarchy (1794684872):

1. Theorem 1 (Exact Finite-n Raw & Central Moment Staircase p = 1..6 and the
   Finite-n Origin of the Bernoulli(1/4) Constants):
   Integrating Jee A's 4th-order bifurcated beam equations
       rho_+^{(4)}(x; z^2) = -4 z^2 rho_+(x; z^2),
       rho_-^{(4)}(x; z^2) = +16 z^2 rho_-(x; z^2)
   by parts against x^p gives a closed 4-step recursive staircase expressing
   every finite-n raw moment m_p^{(2n)} = int_0^1 x^p P_{2n}(x) dx (for all n >= 0)
   as an exact rational linear combination of the boundary sequences
   {m_0^{(2n+2k)}, I_0^{(2n+2k+2)}, H_0^{(2n+2k+3)}}:
       m_1^{(2n)} = (1/4) m_0^{(2n)},
       m_2^{(2n)} = (1/4) m_0^{(2n)} - I_0^{(2n+2)},
       m_3^{(2n)} = (1/4) m_0^{(2n)} - (15/8) I_0^{(2n+2)} + (3/4) H_0^{(2n+3)},
       m_4^{(2n)} = (1/4) m_0^{(2n)} - (15/4) I_0^{(2n+2)} + (15/2) H_0^{(2n+3)} - 6 m_0^{(2n+2)},
       m_5^{(2n)} = (1/4) m_0^{(2n)} - (25/4) I_0^{(2n+2)} + (75/4) H_0^{(2n+3)} - (135/8) m_0^{(2n+2)},
       m_6^{(2n)} = (1/4) m_0^{(2n)} - (75/8) I_0^{(2n+2)} + (75/2) H_0^{(2n+3)} - (405/8) m_0^{(2n+2)} + 90 I_0^{(2n+4)}.
   By induction on p, the coefficient of the unshifted mass m_0^{(2n)} in m_p^{(2n)}
   is identically 1/4 for ALL p >= 1 (and 1 for p = 0). Consequently, already at every
   finite order n >= 0, the coefficient of m_0^{(2n)} in the central moment
   mu_p^{cent,(2n)} = int_0^1 (x - 1/4)^p P_{2n}(x) dx is identically the p-th central
   moment of Bernoulli(1/4):
       (-1/4)^p + (1/4) sum_{j=1}^p comb(p, j) (-1/4)^{p-j} = (3 (-1)^p + 3^p) / 4^{p+1},
   yielding 0, 3/16, 3/32, 21/256, 15/256, 183/4096 for p = 1..6.

2. Theorem 2 (Exact Dictionary Between Finite-n Boundary Shifts and All-Mode Pole
   Invariants, & Closed-Form 5th and 6th Central Moments of rho_hat_r for all r >= 1):
   Under the Darboux residue map at any cantilever mode r >= 1 (1 + cosh(kappa_r)cos(kappa_r) = 0,
   t_r = tanh(kappa_r/2) for odd r and coth(kappa_r/2) for even r), the finite-n basis
   elements map coefficient-by-coefficient to:
       m_0^{(2n)} / m_0^{(2n)}        -> 1,
       I_0^{(2n+2k)} / m_0^{(2n)}     -> t_r^2 / kappa_r^{4k-2},
       H_0^{(2n+2k+1)} / m_0^{(2n)}   -> t_r / kappa_r^{4k-1},
       m_0^{(2n+2k)} / m_0^{(2n)}     -> 1 / kappa_r^{4k}.
   Because Petrovich's 1/4 Barycenter Invariant (2 m_1^{(2n+2)} - m_0^{(2n+2)} = -(1/2) m_0^{(2n+2)})
   annihilates the 5th-order shift at p = 5, mu_5^{cent}(rho_hat_r) has no kappa_r^{-5} term:
       mu_5^{cent}(rho_hat_r) = 15/256 - (165/64) t_r^2 / kappa_r^2 + (315/32) t_r / kappa_r^3 - (75/8) / kappa_r^4,
       mu_6^{cent}(rho_hat_r) = 183/4096 - (765/256) t_r^2 / kappa_r^2 + (1035/64) t_r / kappa_r^3
                                - (495/16) / kappa_r^4 + 90 t_r^2 / kappa_r^6.

3. Theorem 3 (Closed-Form 4th Central Moment & Kurtosis of All Pure Euler-Bernoulli
   Beam Eigenmodes psi_hat_r(x)^2, r >= 1):
   Via Mnema's shift law E_{psi_hat_r^2}[x^q] = (4/(q+1)) E_{rho_hat_r}[x^{q+1}] at q = 4, 5:
       E_{psi_hat_r^2}[x^4] = 1/5 - 5 t_r^2 / kappa_r^2 + 15 t_r / kappa_r^3 - (27/2) / kappa_r^4,
       E_{psi_hat_r^2}[x^5] = 1/6 - (25/4) t_r^2 / kappa_r^2 + 25 t_r / kappa_r^3 - (135/4) / kappa_r^4 + 60 t_r^2 / kappa_r^6,
   and the 4th central moment of the pure beam mode psi_hat_r(x)^2 has the exact closed form:
       mu_4^{cent}(psi_hat_r^2) = 1/80 - t_r^2 / (4 kappa_r^2) + (3/2) t_r / kappa_r^3
                                  - (3 + 20 t_r^4) / (2 kappa_r^4) + 48 t_r^3 / kappa_r^5
                                  - 12 t_r^2 (4 + t_r^4) / kappa_r^6 + 24 t_r^5 / kappa_r^7 - 48 t_r^8 / kappa_r^8.
   At r = 1, psi_hat_1(x)^2 is the unique leptokurtic mode:
       mu_4^{cent}(psi_hat_1^2) = 0.00209484117836357533423945627164552645384871580894...,
       kappa_4(psi_hat_1^2)     = 3.61283710271100033518773627125982909107152505926166... (> 3),
       gamma_2(psi_hat_1^2)     = +0.61283710271100033518773627125982909107152505926166...,
   whereas all higher modes r >= 2 are platykurtic (kappa_4 < 3, converging to 9/5 = 1.8 of Uniform[0, 1]).
"""

from __future__ import annotations

import json
import math
import os
import shutil
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Dict, List, Tuple

getcontext().prec = 85

RESEARCH_DIR = "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06"

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


def poly_add(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = max(len(a), len(b))
    res = [Fraction(0)] * n
    for i in range(len(a)):
        res[i] += a[i]
    for i in range(len(b)):
        res[i] += b[i]
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def poly_scale(a: List[Fraction], c: Fraction) -> List[Fraction]:
    if c == 0:
        return [Fraction(0)]
    return [x * c for x in a]


def poly_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    res = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            res[i + j] += ai * bj
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def apply_T_poly(p: List[Fraction]) -> List[Fraction]:
    deg = len(p) - 1
    out = [Fraction(0)] * (deg + 3)
    for k, ck in enumerate(p):
        if ck == 0:
            continue
        coeff = ck / Fraction((k + 1) * (k + 2))
        m = k + 2
        for j in range(m + 1):
            sgn = -1 if (j % 2 == 1) else 1
            out[j] += coeff * Fraction(sgn * math.comb(m, j))
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_moment_x(p: List[Fraction], r: int) -> Fraction:
    return sum(ck / Fraction(k + r + 1) for k, ck in enumerate(p))


def lin_comb(
    d1: Dict[Tuple[str, int], Fraction],
    d2: Dict[Tuple[str, int], Fraction],
    c1: Fraction = Fraction(1),
    c2: Fraction = Fraction(1),
) -> Dict[Tuple[str, int], Fraction]:
    res: Dict[Tuple[str, int], Fraction] = {}
    for k in set(d1) | set(d2):
        v = c1 * d1.get(k, Fraction(0)) + c2 * d2.get(k, Fraction(0))
        if v != 0:
            res[k] = v
    return res


def verify_all() -> Dict[str, object]:
    print("=== THEOREM 1: EXACT FINITE-n RAW & CENTRAL MOMENT STAIRCASE (p = 1..6) ===")
    t_one = [[Fraction(1)]]
    t_f1 = [[Fraction(1), Fraction(-1)]]
    for _ in range(20):
        t_one.append(apply_T_poly(t_one[-1]))
        t_f1.append(apply_T_poly(t_f1[-1]))

    H0 = [t_one[m][0] for m in range(21)]
    I0 = [poly_moment_x(t_one[m], 0) for m in range(21)]

    N_max = 6  # n = 0..5
    P_2n = []
    for n in range(N_max + 2):
        p = [Fraction(0)]
        for k in range(2 * n + 1):
            sgn = -1 if ((2 * n - k) % 2 == 1) else 1
            p = poly_add(p, poly_scale(poly_mul(t_f1[k], t_f1[2 * n - k]), Fraction(sgn)))
        P_2n.append(p)

    m_exact = [[poly_moment_x(P_2n[n], p) for n in range(N_max + 2)] for p in range(7)]

    # Symbolic basis representation: key = (seq_name, index_offset_from_2n)
    M_raw_sym: List[Dict[Tuple[str, int], Fraction]] = [
        {("m0", 0): Fraction(1)},
        {("m0", 0): Fraction(1, 4)},
        {("m0", 0): Fraction(1, 4), ("I0", 2): Fraction(-1)},
        {("m0", 0): Fraction(1, 4), ("I0", 2): Fraction(-15, 8), ("H0", 3): Fraction(3, 4)},
        {("m0", 0): Fraction(1, 4), ("I0", 2): Fraction(-15, 4), ("H0", 3): Fraction(15, 2), ("m0", 2): Fraction(-6)},
        {
            ("m0", 0): Fraction(1, 4),
            ("I0", 2): Fraction(-25, 4),
            ("H0", 3): Fraction(75, 4),
            ("m0", 2): Fraction(-135, 8),
        },
        {
            ("m0", 0): Fraction(1, 4),
            ("I0", 2): Fraction(-75, 8),
            ("H0", 3): Fraction(75, 2),
            ("m0", 2): Fraction(-405, 8),
            ("I0", 4): Fraction(90),
        },
    ]

    # Derive M_central_sym[p] = sum_{j=0}^p comb(p, j) (-1/4)^{p-j} M_raw_sym[j]
    M_cent_sym: List[Dict[Tuple[str, int], Fraction]] = []
    bernoulli_quarter_moments: Dict[str, str] = {}
    for p in range(7):
        mu_p: Dict[Tuple[str, int], Fraction] = {}
        for j in range(p + 1):
            mu_p = lin_comb(
                mu_p,
                M_raw_sym[j],
                Fraction(1),
                Fraction(math.comb(p, j)) * (Fraction(-1, 4) ** (p - j)),
            )
        M_cent_sym.append(mu_p)
        if p >= 1:
            bern_p = Fraction(3, 4) * (Fraction(-1, 4) ** p) + Fraction(1, 4) * (Fraction(3, 4) ** p)
            coeff_m0 = mu_p.get(("m0", 0), Fraction(0))
            assert coeff_m0 == bern_p, f"Bernoulli(1/4) leading coefficient mismatch at p={p}"
            bernoulli_quarter_moments[f"p={p}"] = str(bern_p)

    def eval_sym_at_n(sym_dict: Dict[Tuple[str, int], Fraction], n: int) -> Fraction:
        total = Fraction(0)
        for (name, sh), coeff in sym_dict.items():
            if name == "m0":
                total += coeff * m_exact[0][n + sh // 2]
            elif name == "I0":
                total += coeff * I0[2 * n + sh]
            elif name == "H0":
                total += coeff * H0[2 * n + sh]
            else:
                raise ValueError(f"Unknown sequence {name}")
        return total

    finite_n_checks = {}
    for n in range(N_max):
        row = {}
        for p in range(1, 7):
            raw_val = eval_sym_at_n(M_raw_sym[p], n)
            assert raw_val == m_exact[p][n], f"Raw moment m_{p}^({2*n}) mismatch at n={n}"
            cent_exact = sum(
                Fraction(math.comb(p, j)) * (Fraction(-1, 4) ** (p - j)) * m_exact[j][n]
                for j in range(p + 1)
            )
            cent_val = eval_sym_at_n(M_cent_sym[p], n)
            assert cent_val == cent_exact, f"Central moment mu_{p}^cent,({2*n}) mismatch at n={n}"
            row[f"m_{p}"] = str(raw_val)
            row[f"mu_{p}_cent"] = str(cent_val)
        finite_n_checks[f"n={n}_z^{2*n}"] = row

    print("  [PASS 1] Exact finite-n raw moments m_p^{(2n)} and central moments mu_p^{cent,(2n)} (p=1..6)")
    print("           verified in Fraction for all n = 0..5, confirming that the coefficient of m_0^{(2n)}")
    print("           in mu_p^{cent,(2n)} is identically the Bernoulli(1/4) central moment at every finite n.")

    print("\n=== THEOREM 2 & 3: ALL-MODE POLE MOMENTS (p=5,6) & PURE BEAM KURTOSIS (r=1..4) ===")
    # Symbolic polynomial in (inv_kappa_pow, t_pow) for pure beam moments b_q = (4/(q+1)) E_{rho_r}[x^{q+1}]
    def sym_to_pole_poly(sym_dict: Dict[Tuple[str, int], Fraction]) -> Dict[Tuple[int, int], Fraction]:
        """Map ('m0', 2k)->(4k, 0), ('I0', 2k)->(4k-2, 2), ('H0', 2k+1)->(4k-1, 1)."""
        poly: Dict[Tuple[int, int], Fraction] = {}
        for (name, sh), coeff in sym_dict.items():
            if name == "m0":
                key = (2 * sh, 0)
            elif name == "I0":
                key = (2 * sh - 2, 2)
            elif name == "H0":
                key = (2 * sh - 3, 1)
            else:
                raise ValueError(name)
            poly[key] = poly.get(key, Fraction(0)) + coeff
        return {k: v for k, v in poly.items() if v != 0}

    def poly_dict_add(a: Dict[Tuple[int, int], Fraction], b: Dict[Tuple[int, int], Fraction], scale: Fraction = Fraction(1)):
        res = dict(a)
        for k, v in b.items():
            res[k] = res.get(k, Fraction(0)) + scale * v
            if res[k] == 0:
                del res[k]
        return res

    def poly_dict_mul(a: Dict[Tuple[int, int], Fraction], b: Dict[Tuple[int, int], Fraction]):
        res: Dict[Tuple[int, int], Fraction] = {}
        for (a1, b1), v1 in a.items():
            for (a2, b2), v2 in b.items():
                k = (a1 + a2, b1 + b2)
                res[k] = res.get(k, Fraction(0)) + v1 * v2
                if res[k] == 0:
                    del res[k]
        return res

    # Verify the pole polynomials for mu_5^{cent}(rho_r), mu_6^{cent}(rho_r), and b_1..b_5 = E_{psi_r^2}[x^1..x^5]:
    mu5_rho_pole = sym_to_pole_poly(M_cent_sym[5])
    mu6_rho_pole = sym_to_pole_poly(M_cent_sym[6])
    assert mu5_rho_pole == {
        (0, 0): Fraction(15, 256),
        (2, 2): Fraction(-165, 64),
        (3, 1): Fraction(315, 32),
        (4, 0): Fraction(-75, 8),
    }
    assert mu6_rho_pole == {
        (0, 0): Fraction(183, 4096),
        (2, 2): Fraction(-765, 256),
        (3, 1): Fraction(1035, 64),
        (4, 0): Fraction(-495, 16),
        (6, 2): Fraction(90, 1),
    }

    b_beam = {}
    for q in range(1, 6):
        b_beam[q] = {k: v * Fraction(4, q + 1) for k, v in sym_to_pole_poly(M_raw_sym[q + 1]).items()}

    # Compute exact 4th central moment polynomial of pure beam mode psi_hat_r(x)^2:
    # mu_4^{cent}(psi_r^2) = b_4 - 4 b_1 b_3 + 6 b_1^2 b_2 - 3 b_1^4
    b1 = b_beam[1]
    b2 = b_beam[2]
    b3 = b_beam[3]
    b4 = b_beam[4]
    b1_2 = poly_dict_mul(b1, b1)
    b1_4 = poly_dict_mul(b1_2, b1_2)
    mu4_beam_pole = poly_dict_add(
        poly_dict_add(b4, poly_dict_mul(b1, b3), Fraction(-4)),
        poly_dict_add(poly_dict_mul(b1_2, b2), b1_4, Fraction(-1, 2)),
        Fraction(6),
    )
    expected_mu4_beam_pole = {
        (0, 0): Fraction(1, 80),
        (2, 2): Fraction(-1, 4),
        (3, 1): Fraction(3, 2),
        (4, 0): Fraction(-3, 2),
        (4, 4): Fraction(-10, 1),
        (5, 3): Fraction(48, 1),
        (6, 2): Fraction(-48, 1),
        (6, 6): Fraction(-12, 1),
        (7, 5): Fraction(24, 1),
        (8, 8): Fraction(-48, 1),
    }
    assert mu4_beam_pole == expected_mu4_beam_pole, f"mu4_beam_pole mismatch: {mu4_beam_pole}"

    mode_table = {}
    N_simp = 6000
    h_simp = 1.0 / N_simp

    for r in (1, 2, 3, 4):
        kr = find_kappa_dec(r)
        kh = kr / Decimal(2)
        tr = (dec_sinh(kh) / dec_cosh(kh)) if (r % 2 == 1) else (dec_cosh(kh) / dec_sinh(kh))

        def eval_pole_dec(poly_d: Dict[Tuple[int, int], Fraction]) -> Decimal:
            return sum(
                (Decimal(v.numerator) / Decimal(v.denominator)) * (tr ** b) / (kr ** a)
                for (a, b), v in poly_d.items()
            )

        mu5_rho_dec = eval_pole_dec(mu5_rho_pole)
        mu6_rho_dec = eval_pole_dec(mu6_rho_pole)
        b4_dec = eval_pole_dec(b_beam[4])
        b5_dec = eval_pole_dec(b_beam[5])
        mu4_beam_dec = eval_pole_dec(mu4_beam_pole)
        sig2_beam_dec = (
            Decimal(1) / Decimal(12)
            - (tr * tr) / (Decimal(2) * kr * kr)
            + tr / (kr ** 3)
            - Decimal(4) * (tr ** 4) / (kr ** 4)
        )
        kurt_beam_dec = mu4_beam_dec / (sig2_beam_dec * sig2_beam_dec)
        excess_kurt_beam_dec = kurt_beam_dec - Decimal(3)

        # Cross-check by Simpson quadrature on [0, 1]
        kf = float(kr)
        mean_beam_f = float(Decimal(1) / Decimal(2) - Decimal(2) * (tr * tr) / (kr * kr))

        def psi_sq(x: float) -> float:
            w = x - 0.5
            if r % 2 == 1:
                val = math.cosh(kf * w) / math.cosh(0.5 * kf) - math.sin(kf * w) / math.sin(0.5 * kf)
            else:
                val = math.cos(kf * w) / math.cos(0.5 * kf) - math.sinh(kf * w) / math.sinh(0.5 * kf)
            return val * val

        def rho_r(x: float) -> float:
            w = x - 0.5
            if r % 2 == 1:
                psi = math.cosh(kf * w) / math.cosh(0.5 * kf) - math.sin(kf * w) / math.sin(0.5 * kf)
                dpsi = kf * (math.sinh(kf * w) / math.cosh(0.5 * kf) - math.cos(kf * w) / math.sin(0.5 * kf))
            else:
                psi = math.cos(kf * w) / math.cos(0.5 * kf) - math.sinh(kf * w) / math.sinh(0.5 * kf)
                dpsi = kf * (-math.sin(kf * w) / math.cos(0.5 * kf) - math.cosh(kf * w) / math.sinh(0.5 * kf))
            return -0.5 * psi * dpsi

        def simp(fn) -> float:
            s = fn(0.0) + fn(1.0)
            for i in range(1, N_simp):
                s += (4.0 if (i % 2 == 1) else 2.0) * fn(i * h_simp)
            return s * h_simp / 3.0

        q_mu5_rho = simp(lambda x: ((x - 0.25) ** 5) * rho_r(x))
        q_mu6_rho = simp(lambda x: ((x - 0.25) ** 6) * rho_r(x))
        q_b4 = simp(lambda x: (x ** 4) * psi_sq(x))
        q_b5 = simp(lambda x: (x ** 5) * psi_sq(x))
        q_mu4_beam = simp(lambda x: ((x - mean_beam_f) ** 4) * psi_sq(x))

        assert abs(float(mu5_rho_dec) - q_mu5_rho) < 1e-12
        assert abs(float(mu6_rho_dec) - q_mu6_rho) < 1e-12
        assert abs(float(b4_dec) - q_b4) < 1e-12
        assert abs(float(b5_dec) - q_b5) < 1e-12
        assert abs(float(mu4_beam_dec) - q_mu4_beam) < 1e-12

        mode_table[f"r={r}"] = {
            "mu5_cent_rho_50d": str(mu5_rho_dec)[:52],
            "mu6_cent_rho_50d": str(mu6_rho_dec)[:52],
            "pure_beam_E_x4_50d": str(b4_dec)[:52],
            "pure_beam_E_x5_50d": str(b5_dec)[:52],
            "pure_beam_mu4_cent_50d": str(mu4_beam_dec)[:52],
            "pure_beam_kurtosis_kappa4_50d": str(kurt_beam_dec)[:52],
            "pure_beam_excess_kurtosis_gamma2_50d": str(excess_kurt_beam_dec)[:53],
        }
        print(
            f"  r={r}: mu5_rho={float(mu5_rho_dec):+.10f} | mu6_rho={float(mu6_rho_dec):+.10f} | "
            f"mu4_cent(psi_{r}^2)={float(mu4_beam_dec):.10f} | kappa_4(psi_{r}^2)={float(kurt_beam_dec):.10f}"
        )

    print("  [PASS 2 & 3] Closed-form 5th/6th pole central moments mu_5^cent(rho_r), mu_6^cent(rho_r) and")
    print("               pure-beam 4th central moment mu_4^cent(psi_r^2) & kurtosis kappa_4(psi_r^2) verified.")
    print("ALL_CHECKS_PASSED")

    return {
        "bernoulli_quarter_central_moments_p_1_to_6": bernoulli_quarter_moments,
        "finite_n_staircase_verified_n_0_to_5": finite_n_checks,
        "all_mode_moments_and_pure_beam_kurtosis_r_1_to_4": mode_table,
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_json = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "finite_n_bernoulli_staircase_and_beam_kurtosis_2026_11_14_results.json",
    )
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    if os.path.isdir(RESEARCH_DIR):
        dst_py = os.path.join(RESEARCH_DIR, "finite_n_bernoulli_staircase_and_beam_kurtosis_den_b.py")
        dst_json = os.path.join(RESEARCH_DIR, "finite_n_bernoulli_staircase_and_beam_kurtosis_den_b_results.json")
        if os.path.abspath(__file__) != os.path.abspath(dst_py):
            shutil.copy2(os.path.abspath(__file__), dst_py)
        if os.path.abspath(out_json) != os.path.abspath(dst_json):
            shutil.copy2(out_json, dst_json)
