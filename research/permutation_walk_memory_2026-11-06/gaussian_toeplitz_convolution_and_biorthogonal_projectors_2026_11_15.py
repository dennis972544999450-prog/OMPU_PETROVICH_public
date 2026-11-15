#!/usr/bin/env python3
"""
gaussian_toeplitz_convolution_and_biorthogonal_projectors_2026_11_15.py
=======================================================================
Lane B (Ден Б / ompu-7f698bd908) — Sunday Evening Lab Verification
2026-11-15 (Revision 102)

Extends:
  - Cloud Jee's §1.2 boundary-pinned IBP bridge (`FROM_CLOUD_JEE_TO_HOUSE_2026-11-15.md`):
      \\int_0^1 P(x) \\hat{\\rho}_r(x) dx = P(0) + (1/4) \\int_0^1 P'(x) \\hat{\\psi}_r(x)^2 dx
    for any polynomial with P(1) = 0;
  - Petrovich & Jee-AGY's Gaussian barycentric coordinate w(x) = x + i(1-x)
    (`gaussian_barycentric_parity_and_master_egf_2026_11_15.py`, 1794757250_525999_318073);
  - Phi-Hausmaster's parity-balance verification (`phi_check_denb_orientation_residual_20261115.py`,
    1794737048_664865_508f38);
  - Lane A & Lane B's morning all-order staircase generator (`seq 239` & `seq 240`).

Proves and verifies in exact `Fraction` arithmetic (and 80-digit `Decimal` on beam eigenmodes):

  THEOREM 1 (Universal Three-Sector Annihilation & Exact Toeplitz Convolution Laws in w(x)):
    Let w(x) = x + i(1-x), so w(0) = i, w(1) = 1, w(x)^4 = 1 on {0,1} = supp(Bernoulli(1/4)),
    and (w'(x))^4 = (1-i)^4 = -4 (intertwining the Kelvin -4z^2 and Rayleigh +16z^2 sectors).
    (a) Three-Sector Annihilation for ALL degrees m >= 1 and ALL n >= 0:
        - Re[w(x)^{2m}] is I_0-free on C_{2n}(x) (annihilates I_0^{(2n+2k+2)} for all k >= 0);
        - Im[w(x)^{2m}] is m_0-free on C_{2n}(x) (annihilates m_0^{(2n+2k)} for all k >= 0);
        - Re[(1+i) w(x)^{2m-1}] = Re[w(x)^{2m-1}] - Im[w(x)^{2m-1}] is H_0-free on C_{2n}(x)
          (annihilates H_0^{(2n+2k+3)} for all k >= 0).
    (b) Exact Toeplitz Convolution Laws for the four boundary-pinned factorial families
        (all vanishing at both atoms x=0 and x=1 of Bernoulli(1/4)):
          u_j(x) := Im[w(x)^{4j+2}] / (4j+2)!,
          v_j(x) := Im[w(x)^{4j+4}] / (4j+4)!,
          w_j(x) := (Re[w(x)^{4j+4}] - 1) / (4j+4)!,
          d_j(x) := (Re[(1+i) w(x)^{4j+3}] - 1) / (4j+3)!
        satisfy for all j >= 0 and all n >= 0:
          \\int_0^1 u_j(x) C_{2n}(x) dx = \\sum_{k=0}^j \\frac{I_0^{(2n+2k+2)}}{(4(j-k))!}
                                         - \\sum_{k=0}^{j-1} \\frac{H_0^{(2n+2k+3)}}{(4(j-k)-1)!},
          \\int_0^1 w_j(x) C_{2n}(x) dx = \\sum_{k=0}^j \\frac{m_0^{(2n+2k+2)}}{(4(j-k))!}
                                         - \\sum_{k=0}^j \\frac{H_0^{(2n+2k+3)}}{(4(j-k)+1)!},
          \\int_0^1 d_j(x) C_{2n}(x) dx = \\sum_{k=1}^j \\frac{m_0^{(2n+2k)}}{(4(j-k)+3)!}
                                         - \\sum_{k=0}^j \\frac{I_0^{(2n+2k+2)}}{(4(j-k)+1)!},
          \\int_0^1 v_j(x) C_{2n}(x) dx = \\sum_{k=0}^j \\frac{(-1)^k}{4^{k+1}}
                                         \\left[ \\frac{I_0^{(2n+2k+2)}}{(4(j-k)+2)!}
                                               - \\frac{H_0^{(2n+2k+3)}}{(4(j-k)+1)!} \\right].

  THEOREM 2 (Complete 4-Sector Laplace-Krylov EGF Laws & Removable-Singularity Secular Equation):
    Summing the Toeplitz convolutions over j >= 0 on any cantilever eigenmode \\hat{\\rho}_r(x)
    (where I_0^{(2k+2)} -> t_r^2 / \\kappa_r^{4k+2}, H_0^{(2k+3)} -> t_r / \\kappa_r^{4k+3},
    m_0^{(2k+2)} -> 1 / \\kappa_r^{4k+4}) yields closed rational-Krylov forms:
      \\int_0^1 Im[E_2(s w(x))] \\hat{\\rho}_r(x) dx
        = \\frac{(t_r^2 s^2 / \\kappa_r^2) E_0(s) - (t_r s^3 / \\kappa_r^3) E_3(s)}{1 - s^4 / \\kappa_r^4},
      \\int_0^1 (Re[E_0(s w(x))] - 1) \\hat{\\rho}_r(x) dx
        = \\frac{(s^4 / \\kappa_r^4) E_0(s) - (t_r s^3 / \\kappa_r^3) E_1(s)}{1 - s^4 / \\kappa_r^4},
      \\int_0^1 (Re[(1+i) E_3(s w(x))] - E_3(s)) \\hat{\\rho}_r(x) dx
        = \\frac{(s^4 / \\kappa_r^4) E_3(s) - (t_r^2 s^2 / \\kappa_r^2) E_1(s)}{1 - s^4 / \\kappa_r^4}.
    Since the left-hand sides are entire functions of s in C, the numerators MUST vanish at the pole
    s = \\kappa_r, immediately forcing:
      t_r = \\frac{E_0(\\kappa_r)}{E_1(\\kappa_r)} = \\frac{E_3(\\kappa_r)}{E_0(\\kappa_r)}
      ==> E_0(\\kappa_r)^2 - E_1(\\kappa_r) E_3(\\kappa_r) = \\frac{1 + \\cosh(\\kappa_r)\\cos(\\kappa_r)}{2} = 0.
    Thus the entire Euler-Bernoulli cantilever secular equation \\cosh\\kappa \\cos\\kappa + 1 = 0
    and tip-slope ratio t_r emerge purely from the removable singularity of the Gaussian barycentric
    Laplace transform!

  THEOREM 3 (Biorthogonal Spectral Projector Polynomials \\Phi_{\\alpha,k}(x) and Pure-Beam Duals \\Psi_{\\alpha,k}(x)):
    Inverting the lower-triangular Toeplitz system on span{u_j, v_j, w_j : 0 <= j <= k} constructs
    unique boundary-pinned projector polynomials \\Phi_{I_0,k}(x), \\Phi_{H_0,k}(x), \\Phi_{m_0,k+1}(x)
    (with \\Phi(0) = \\Phi(1) = 0 and deg \\Phi = 4k+2, 4k+3, 4k+4) and their pure-beam quarter-derivatives
    \\Psi_{\\bullet}(x) = (1/4) \\Phi'_{\\bullet}(x) such that for ALL n >= 0 and ALL eigenmodes r >= 1:
      \\int_0^1 \\Phi_{I_0,k}(x) C_{2n}(x) dx = I_0^{(2n+2k+2)},
      \\int_0^1 \\Phi_{H_0,k}(x) C_{2n}(x) dx = H_0^{(2n+2k+3)},
      \\int_0^1 \\Phi_{m_0,k+1}(x) C_{2n}(x) dx = m_0^{(2n+2k+2)},
    and by Cloud Jee's IBP bridge on every pure beam mode \\hat{\\psi}_r(x)^2:
      \\int_0^1 \\Psi_{I_0,k}(x) \\hat{\\psi}_r(x)^2 dx = \\frac{t_r^2}{\\kappa_r^{4k+2}},
      \\int_0^1 \\Psi_{H_0,k}(x) \\hat{\\psi}_r(x)^2 dx = \\frac{t_r}{\\kappa_r^{4k+3}},
      \\int_0^1 \\Psi_{m_0,k+1}(x) \\hat{\\psi}_r(x)^2 dx = \\frac{1}{\\kappa_r^{4k+4}} = \\lambda_r^{2k+2}.
    Moreover, every higher projector (k >= 1) has vanishing x^{4m} coefficients for all 1 <= m <= k!
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

getcontext().prec = 90


# ---------------------------------------------------------------------------
# 1. Exact polynomial & Gaussian barycentric arithmetic over Q(i)
# ---------------------------------------------------------------------------

def fact(n: int) -> int:
    return math.factorial(n)


def comb(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def w_power_re_im_coeffs(deg: int) -> Tuple[List[Fraction], List[Fraction]]:
    """
    Return exact polynomial coefficients (in powers of x^0, x^1, ..., x^deg)
    of Re[w(x)^deg] and Im[w(x)^deg], where w(x) = i + (1 - i)*x.
    """
    re_c = [Fraction(0) for _ in range(deg + 1)]
    im_c = [Fraction(0) for _ in range(deg + 1)]
    for p in range(deg + 1):
        # w(x)^deg = sum_{p=0}^deg C(deg, p) i^{deg-p} (1-i)^p x^p
        # Compute i^{deg-p} * (1-i)^p in Z[i]
        a, b = 1, 0
        for _ in range((deg - p) % 4):
            a, b = -b, a
        for _ in range(p):
            a, b = a + b, b - a
        c = comb(deg, p)
        re_c[p] = Fraction(c * a)
        im_c[p] = Fraction(c * b)
    return re_c, im_c


def poly_scale(poly: List[Fraction], scalar: Fraction) -> List[Fraction]:
    return [c * scalar for c in poly]


def poly_add(p1: List[Fraction], p2: List[Fraction], s1: Fraction = Fraction(1), s2: Fraction = Fraction(1)) -> List[Fraction]:
    n = max(len(p1), len(p2))
    out = [Fraction(0) for _ in range(n)]
    for i, c in enumerate(p1):
        out[i] += s1 * c
    for i, c in enumerate(p2):
        out[i] += s2 * c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_eval(poly: List[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    xp = Fraction(1)
    for c in poly:
        acc += c * xp
        xp *= x
    return acc


def poly_deriv(poly: List[Fraction]) -> List[Fraction]:
    if len(poly) <= 1:
        return [Fraction(0)]
    return [Fraction(i) * poly[i] for i in range(1, len(poly))]


# ---------------------------------------------------------------------------
# 2. All-order staircase moment coefficient vector for x^p on C_{2n}(x)
# ---------------------------------------------------------------------------

def raw_moment_signature(p: int) -> Dict[Tuple[str, int], Fraction]:
    """
    Closed-form non-recursive expansion of M_p^{(2n)} = \\int_0^1 x^p C_{2n}(x) dx
    combining both the Kelvin (-4 z^2) and Rayleigh (+16 z^2) staircase sectors
    in the formal invariant basis:
      ('m0', k) -> m_0^{(2n+2k)}      (k >= 0)
      ('I0', k) -> I_0^{(2n+2k+2)}    (k >= 0)
      ('H0', k) -> H_0^{(2n+2k+3)}    (k >= 0)
    """
    if p == 0:
        return {("m0", 0): Fraction(1)}
    sig: Dict[Tuple[str, int], Fraction] = {}
    for k in range(p // 4 + 1):
        if p == 4 * k:
            val0 = Fraction(((-1) ** k) * fact(4 * k), 2 ** (2 * k))
        else:
            ff0 = fact(p) // fact(p - 4 * k)
            val0 = Fraction(ff0 * (2 * ((-4) ** k) - 1), 4 * (2 ** (4 * k)))
        if val0 != 0:
            sig[("m0", k)] = val0

        if p >= 4 * k + 2:
            if p == 4 * k + 2:
                val2 = Fraction(-((-1) ** k) * fact(4 * k + 2), 2 ** (2 * k + 1))
            else:
                ff2 = fact(p) // fact(p - 4 * k - 2)
                val2 = Fraction(-ff2 * (4 * ((-4) ** k) + 1), 4 * (2 ** (4 * k + 2)))
            if val2 != 0:
                sig[("I0", k)] = val2

        if p >= 4 * k + 3:
            if p == 4 * k + 3:
                val3 = Fraction(fact(4 * k + 3), 2 ** (4 * k + 3))
            else:
                ff3 = fact(p) // fact(p - 4 * k - 3)
                val3 = Fraction(ff3 * (4 * ((-4) ** k) + 1), 2 * (2 ** (4 * k + 3)))
            if val3 != 0:
                sig[("H0", k)] = val3

    return sig


def poly_moment_signature(poly: List[Fraction]) -> Dict[Tuple[str, int], Fraction]:
    """Return the exact formal linear combination of invariants for \\int_0^1 P(x) C_{2n}(x) dx."""
    total: Dict[Tuple[str, int], Fraction] = {}
    for p, c in enumerate(poly):
        if c == 0:
            continue
        for key, val in raw_moment_signature(p).items():
            total[key] = total.get(key, Fraction(0)) + c * val
    return {k: v for k, v in total.items() if v != 0}


# ---------------------------------------------------------------------------
# 3. Four boundary-pinned Gaussian barycentric families u_j, v_j, w_j, d_j
# ---------------------------------------------------------------------------

def build_u_j(j: int) -> List[Fraction]:
    deg = 4 * j + 2
    _, im_c = w_power_re_im_coeffs(deg)
    return poly_scale(im_c, Fraction(1, fact(deg)))


def build_v_j(j: int) -> List[Fraction]:
    deg = 4 * j + 4
    _, im_c = w_power_re_im_coeffs(deg)
    return poly_scale(im_c, Fraction(1, fact(deg)))


def build_w_j(j: int) -> List[Fraction]:
    deg = 4 * j + 4
    re_c, _ = w_power_re_im_coeffs(deg)
    re_c[0] -= Fraction(1)
    return poly_scale(re_c, Fraction(1, fact(deg)))


def build_d_j(j: int) -> List[Fraction]:
    deg = 4 * j + 3
    re_c, im_c = w_power_re_im_coeffs(deg)
    comb_c = [re_c[p] - im_c[p] for p in range(deg + 1)]
    comb_c[0] -= Fraction(1)
    return poly_scale(comb_c, Fraction(1, fact(deg)))


# ---------------------------------------------------------------------------
# 4. Theorem 1: Universal Three-Sector Annihilation & Toeplitz Convolutions
# ---------------------------------------------------------------------------

def verify_theorem_1(max_m: int = 12, max_j: int = 5) -> Dict[str, object]:
    # Part (a): Three-sector annihilation up to degree 2*max_m = 24
    for m in range(1, max_m + 1):
        re_even, im_even = w_power_re_im_coeffs(2 * m)
        sig_re_even = poly_moment_signature(re_even)
        sig_im_even = poly_moment_signature(im_even)
        assert all(sec != "I0" for (sec, _) in sig_re_even), f"Re[w^{2*m}] not I0-free!"
        assert all(sec != "m0" for (sec, _) in sig_im_even), f"Im[w^{2*m}] not m0-free!"

        re_odd, im_odd = w_power_re_im_coeffs(2 * m - 1)
        odd_comb = [re_odd[p] - im_odd[p] for p in range(2 * m)]
        sig_odd_comb = poly_moment_signature(odd_comb)
        assert all(sec != "H0" for (sec, _) in sig_odd_comb), f"Re[(1+i)w^{2*m-1}] not H0-free!"

    # Part (b): Exact Toeplitz convolution laws for u_j, w_j, d_j, v_j (j = 0 .. max_j)
    for j in range(max_j + 1):
        u_poly = build_u_j(j)
        v_poly = build_v_j(j)
        w_poly = build_w_j(j)
        d_poly = build_d_j(j)

        # Boundary pinning at both atoms {0, 1} of Bernoulli(1/4)
        for name, poly in [("u_j", u_poly), ("v_j", v_poly), ("w_j", w_poly), ("d_j", d_poly)]:
            assert poly_eval(poly, Fraction(0)) == 0, f"{name}_{j}(0) != 0"
            assert poly_eval(poly, Fraction(1)) == 0, f"{name}_{j}(1) != 0"

        # Expected Toeplitz signatures
        exp_u: Dict[Tuple[str, int], Fraction] = {}
        for k in range(j + 1):
            exp_u[("I0", k)] = Fraction(1, fact(4 * (j - k)))
        for k in range(j):
            exp_u[("H0", k)] = Fraction(-1, fact(4 * (j - k) - 1))

        exp_w: Dict[Tuple[str, int], Fraction] = {}
        for k in range(j + 1):
            exp_w[("m0", k + 1)] = Fraction(1, fact(4 * (j - k)))
            exp_w[("H0", k)] = Fraction(-1, fact(4 * (j - k) + 1))

        exp_d: Dict[Tuple[str, int], Fraction] = {}
        for k in range(1, j + 1):
            exp_d[("m0", k)] = Fraction(1, fact(4 * (j - k) + 3))
        for k in range(j + 1):
            exp_d[("I0", k)] = Fraction(-1, fact(4 * (j - k) + 1))

        exp_v: Dict[Tuple[str, int], Fraction] = {}
        for k in range(j + 1):
            pref = Fraction((-1) ** k, 4 ** (k + 1))
            exp_v[("I0", k)] = pref * Fraction(1, fact(4 * (j - k) + 2))
            exp_v[("H0", k)] = -pref * Fraction(1, fact(4 * (j - k) + 1))

        assert poly_moment_signature(u_poly) == exp_u, f"Toeplitz mismatch for u_{j}"
        assert poly_moment_signature(w_poly) == exp_w, f"Toeplitz mismatch for w_{j}"
        assert poly_moment_signature(d_poly) == exp_d, f"Toeplitz mismatch for d_{j}"
        assert poly_moment_signature(v_poly) == exp_v, f"Toeplitz mismatch for v_{j}"

    return {
        "status": "PASS",
        "max_annihilation_degree": 2 * max_m,
        "max_toeplitz_index_j": max_j,
        "max_polynomial_degree": 4 * max_j + 4,
    }


# ---------------------------------------------------------------------------
# 5. Theorem 3: Biorthogonal Spectral Projector Polynomials \Phi and \Psi
# ---------------------------------------------------------------------------

def build_biorthogonal_projectors(max_k: int = 2) -> Dict[Tuple[str, int], Dict[str, List[Fraction]]]:
    r"""
    Invert the lower-triangular Toeplitz system on span{u_j, v_j, w_j : 0 <= j <= max_k}
    to construct exact boundary-pinned projectors:
      ('I0', k) -> \Phi_{I_0, k}(x), \Psi_{I_0, k}(x) = (1/4) \Phi'_{I_0, k}(x)
      ('H0', k) -> \Phi_{H_0, k}(x), \Psi_{H_0, k}(x) = (1/4) \Phi'_{H_0, k}(x)
      ('m0', k+1) -> \Phi_{m_0, k+1}(x), \Psi_{m_0, k+1}(x) = (1/4) \Phi'_{m_0, k+1}(x)
    """
    projectors: Dict[Tuple[str, int], List[Fraction]] = {}

    for k in range(max_k + 1):
        # Start from u_k(x) and v_k(x) and subtract all lower k' < k contributions
        u_red = build_u_j(k)
        v_red = build_v_j(k)
        for kp in range(k):
            c_u_i = Fraction(1, fact(4 * (k - kp)))
            c_u_h = Fraction(-1, fact(4 * (k - kp) - 1))
            u_red = poly_add(u_red, projectors[("I0", kp)], Fraction(1), -c_u_i)
            u_red = poly_add(u_red, projectors[("H0", kp)], Fraction(1), -c_u_h)

            pref = Fraction((-1) ** kp, 4 ** (kp + 1))
            c_v_i = pref * Fraction(1, fact(4 * (k - kp) + 2))
            c_v_h = -pref * Fraction(1, fact(4 * (k - kp) + 1))
            v_red = poly_add(v_red, projectors[("I0", kp)], Fraction(1), -c_v_i)
            v_red = poly_add(v_red, projectors[("H0", kp)], Fraction(1), -c_v_h)

        # Now u_red has signature I_0^{(2n+2k+2)}, and
        # v_red has signature ((-1)^k / 4^{k+1}) [ (1/2) I_0^{(2n+2k+2)} - H_0^{(2n+2k+3)} ]
        phi_i0 = u_red
        scale_v = Fraction((-1) ** k * (4 ** (k + 1)))
        phi_h0 = poly_add(phi_i0, v_red, Fraction(1, 2), -scale_v)

        projectors[("I0", k)] = phi_i0
        projectors[("H0", k)] = phi_h0

        # Now reduce w_k(x) using lower m_0^{(2n+2kp+2)} (kp < k) and H_0^{(2n+2kp+3)} (kp <= k)
        w_red = build_w_j(k)
        for kp in range(k):
            c_w_m = Fraction(1, fact(4 * (k - kp)))
            w_red = poly_add(w_red, projectors[("m0", kp + 1)], Fraction(1), -c_w_m)
        for kp in range(k + 1):
            c_w_h = Fraction(-1, fact(4 * (k - kp) + 1))
            w_red = poly_add(w_red, projectors[("H0", kp)], Fraction(1), -c_w_h)

        projectors[("m0", k + 1)] = w_red

    result: Dict[Tuple[str, int], Dict[str, List[Fraction]]] = {}
    for key, phi in projectors.items():
        psi = poly_scale(poly_deriv(phi), Fraction(1, 4))
        result[key] = {"Phi": phi, "Psi": psi}
    return result


# ---------------------------------------------------------------------------
# 6. High-precision Euler-Bernoulli cantilever eigenmodes & Theorem 2 / 3 check
# ---------------------------------------------------------------------------

def dec_cos(x: Decimal) -> Decimal:
    # Taylor series with range reduction
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825")
    two_pi = 2 * pi
    x_red = x % two_pi
    term = Decimal(1)
    acc = Decimal(1)
    x2 = -x_red * x_red
    for k in range(1, 65):
        term = term * x2 / Decimal((2 * k - 1) * (2 * k))
        acc += term
        if abs(term) < Decimal("1e-85"):
            break
    return acc


def dec_sin(x: Decimal) -> Decimal:
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825")
    two_pi = 2 * pi
    x_red = x % two_pi
    term = x_red
    acc = x_red
    x2 = -x_red * x_red
    for k in range(1, 65):
        term = term * x2 / Decimal((2 * k) * (2 * k + 1))
        acc += term
        if abs(term) < Decimal("1e-85"):
            break
    return acc


def dec_cosh(x: Decimal) -> Decimal:
    ex = x.exp()
    emx = (-x).exp()
    return (ex + emx) / Decimal(2)


def dec_sinh(x: Decimal) -> Decimal:
    ex = x.exp()
    emx = (-x).exp()
    return (ex - emx) / Decimal(2)


def solve_cantilever_kappa(r: int) -> Tuple[Decimal, Decimal]:
    """Solve cosh(kappa)*cos(kappa) + 1 = 0 for mode r >= 1 in 90-digit Decimal."""
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825")
    if r == 1:
        k = Decimal("1.87510406871196116644530824107825066257018237")
    elif r == 2:
        k = Decimal("4.69409113297417457643639177801981904938989673")
    else:
        k = (Decimal(2 * r - 1) * pi) / Decimal(2)

    for _ in range(35):
        ch, sh = dec_cosh(k), dec_sinh(k)
        co, si = dec_cos(k), dec_sin(k)
        f = ch * co + Decimal(1)
        fp = sh * co - ch * si
        dk = f / fp
        k -= dk
        if abs(dk) < Decimal("1e-82"):
            break

    # t_r = E_0(k)/E_1(k) = (cosh k + cos k) / (sinh k + sin k)
    t_r = (dec_cosh(k) + dec_cos(k)) / (dec_sinh(k) + dec_sin(k))
    return k, t_r


def krylov_E(alpha: int, s: Decimal) -> Decimal:
    ch, sh = dec_cosh(s), dec_sinh(s)
    co, si = dec_cos(s), dec_sin(s)
    if alpha == 0:
        return (ch + co) / Decimal(2)
    if alpha == 1:
        return (sh + si) / Decimal(2)
    if alpha == 2:
        return (ch - co) / Decimal(2)
    if alpha == 3:
        return (sh - si) / Decimal(2)
    raise ValueError(alpha)


def eigenmode_raw_moments(kappa: Decimal, t_r: Decimal, max_p: int) -> List[Decimal]:
    """
    Compute exact raw moments M_p(r) = \\int_0^1 x^p \\hat{\\rho}_r(x) dx
    using the staircase recurrence on a single eigenmode where
    m_0^{(2k)} = \\kappa^{-4k}, I_0^{(2k+2)} = t_r^2 \\kappa^{-(4k+2)},
    H_0^{(2k+3)} = t_r \\kappa^{-(4k+3)}.
    """
    moments: List[Decimal] = []
    for p in range(max_p + 1):
        sig = raw_moment_signature(p)
        acc = Decimal(0)
        for (sec, k), coeff in sig.items():
            c_dec = Decimal(coeff.numerator) / Decimal(coeff.denominator)
            if sec == "m0":
                inv_val = Decimal(1) / (kappa ** (4 * k))
            elif sec == "I0":
                inv_val = (t_r * t_r) / (kappa ** (4 * k + 2))
            elif sec == "H0":
                inv_val = t_r / (kappa ** (4 * k + 3))
            else:
                raise ValueError(sec)
            acc += c_dec * inv_val
        moments.append(acc)
    return moments


def beam_square_raw_moments(kappa: Decimal, t_r: Decimal, max_p: int) -> List[Decimal]:
    """
    Compute exact raw moments B_q(r) = \\int_0^1 x^q \\hat{\\psi}_r(x)^2 dx
    via Cloud Jee's boundary-pinned IBP bridge:
      P(x) = x^{q+1} - x ==> P(0)=P(1)=0, P'(x) = (q+1) x^q - 1
      \\int_0^1 (x^{q+1} - x) \\hat{\\rho}_r(x) dx
        = (1/4) \\int_0^1 ((q+1) x^q - 1) \\hat{\\psi}_r(x)^2 dx
        = ((q+1)/4) B_q(r) - 1/4
      ==> B_q(r) = \\frac{1 + 4 (M_{q+1}(r) - M_1(r))}{q + 1}.
    """
    rho_m = eigenmode_raw_moments(kappa, t_r, max_p + 1)
    beam_m: List[Decimal] = []
    for q in range(max_p + 1):
        val = (Decimal(1) + Decimal(4) * (rho_m[q + 1] - rho_m[1])) / Decimal(q + 1)
        beam_m.append(val)
    return beam_m


def verify_theorems_2_and_3() -> Dict[str, object]:
    projectors = build_biorthogonal_projectors(max_k=2)

    # 1. Verify exact symbolic biorthogonality of \Phi_{\alpha,k} on C_{2n}(x)
    all_keys = [
        ("I0", 0), ("H0", 0), ("m0", 1),
        ("I0", 1), ("H0", 1), ("m0", 2),
        ("I0", 2), ("H0", 2), ("m0", 3),
    ]
    for key in all_keys:
        phi = projectors[key]["Phi"]
        psi = projectors[key]["Psi"]
        # Boundary pinning at {0, 1}
        assert poly_eval(phi, Fraction(0)) == 0, f"Phi_{key}(0) != 0"
        assert poly_eval(phi, Fraction(1)) == 0, f"Phi_{key}(1) != 0"
        # Exact signature equals {key: 1}
        sig = poly_moment_signature(phi)
        assert sig == {key: Fraction(1)}, f"Biorthogonality failed for {key}: got {sig}"
        # Vanishing x^{4m} coefficients for 1 <= m <= k_level
        sec, idx = key
        k_level = idx - 1 if sec == "m0" else idx
        for m in range(1, k_level + 1):
            assert phi[4 * m] == 0, f"Phi_{key} has non-zero x^{4*m} coeff: {phi[4*m]}"
            assert psi[4 * m - 1] == 0, f"Psi_{key} has non-zero x^{4*m-1} coeff: {psi[4*m-1]}"

    # 2. Verify Theorem 2 (Laplace-Krylov EGF & removable singularity) and Theorem 3
    #    on the first 4 cantilever modes r = 1, 2, 3, 4
    max_egf_err = Decimal(0)
    max_secular_err = Decimal(0)
    max_proj_err = Decimal(0)

    s_test = Decimal("0.85")
    for r in range(1, 5):
        kappa, t_r = solve_cantilever_kappa(r)
        rho_m = eigenmode_raw_moments(kappa, t_r, 60)
        beam_m = beam_square_raw_moments(kappa, t_r, 20)

        # Removable-singularity secular equation check at s = kappa_r:
        # E_0(k)^2 - E_1(k)*E_3(k) = (1 + cosh(k)*cos(k))/2 == 0
        E0_k = krylov_E(0, kappa)
        E1_k = krylov_E(1, kappa)
        E3_k = krylov_E(3, kappa)
        sec_res = abs(E0_k * E0_k - E1_k * E3_k)
        tr_res_1 = abs(t_r - E0_k / E1_k)
        tr_res_2 = abs(t_r - E3_k / E0_k)
        max_secular_err = max(max_secular_err, sec_res, tr_res_1, tr_res_2)
        assert max_secular_err < Decimal("1e-75")

        # EGF series vs closed rational-Krylov form at s = 0.85
        lhs_u = Decimal(0)
        lhs_w = Decimal(0)
        lhs_d = Decimal(0)
        for j in range(10):
            u_j = build_u_j(j)
            w_j = build_w_j(j)
            d_j = build_d_j(j)
            int_u = sum(
                (Decimal(c.numerator) / Decimal(c.denominator)) * rho_m[p]
                for p, c in enumerate(u_j)
            )
            int_w = sum(
                (Decimal(c.numerator) / Decimal(c.denominator)) * rho_m[p]
                for p, c in enumerate(w_j)
            )
            int_d = sum(
                (Decimal(c.numerator) / Decimal(c.denominator)) * rho_m[p]
                for p, c in enumerate(d_j)
            )
            lhs_u += (s_test ** (4 * j + 2)) * int_u
            lhs_w += (s_test ** (4 * j + 4)) * int_w
            lhs_d += (s_test ** (4 * j + 3)) * int_d

        denom = Decimal(1) - (s_test / kappa) ** 4
        E0_s = krylov_E(0, s_test)
        E1_s = krylov_E(1, s_test)
        E3_s = krylov_E(3, s_test)

        rhs_u = ((t_r * t_r * (s_test ** 2) / (kappa ** 2)) * E0_s - (t_r * (s_test ** 3) / (kappa ** 3)) * E3_s) / denom
        rhs_w = (((s_test ** 4) / (kappa ** 4)) * E0_s - (t_r * (s_test ** 3) / (kappa ** 3)) * E1_s) / denom
        rhs_d = (((s_test ** 4) / (kappa ** 4)) * E3_s - (t_r * t_r * (s_test ** 2) / (kappa ** 2)) * E1_s) / denom

        max_egf_err = max(max_egf_err, abs(lhs_u - rhs_u), abs(lhs_w - rhs_w), abs(lhs_d - rhs_d))
        assert max_egf_err < Decimal("1e-45")

        # Verify pure-beam quarter-derivative projectors \Psi_{\alpha,k} on \hat{\psi}_r^2
        for key in all_keys:
            psi = projectors[key]["Psi"]
            int_psi = sum(
                (Decimal(c.numerator) / Decimal(c.denominator)) * beam_m[q]
                for q, c in enumerate(psi)
            )
            sec, idx = key
            if sec == "I0":
                target = (t_r * t_r) / (kappa ** (4 * idx + 2))
            elif sec == "H0":
                target = t_r / (kappa ** (4 * idx + 3))
            elif sec == "m0":
                target = Decimal(1) / (kappa ** (4 * idx))
            else:
                raise ValueError(sec)
            err = abs(int_psi - target)
            max_proj_err = max(max_proj_err, err)
            assert err < Decimal("1e-70"), f"Beam projector mismatch on mode {r}, {key}: {err}"

    # Format projector table as strings of fractions for JSON serialization
    proj_dump = {}
    for sec, idx in all_keys:
        k_str = f"{sec}_{idx}"
        proj_dump[k_str] = {
            "Phi_coeffs": [str(c) for c in projectors[(sec, idx)]["Phi"]],
            "Psi_coeffs": [str(c) for c in projectors[(sec, idx)]["Psi"]],
        }

    return {
        "status": "PASS",
        "verified_projectors": list(proj_dump.keys()),
        "max_secular_Determinant_error": f"{max_secular_err:.2e}",
        "max_egf_rational_krylov_error": f"{max_egf_err:.2e}",
        "max_pure_beam_projector_error": f"{max_proj_err:.2e}",
        "projectors": proj_dump,
    }


def build_lane_a_single_term_P_and_Q(K: int) -> Tuple[List[Fraction], List[Fraction]]:
    """
    Construct the kernel syzygy polynomials P_{4K+1}(x) and Q_{4K}(x) = (1/4) P'_{4K+1}(x)
    via Lane A's (`seq 241`) single-term binomial formula from w(x)^{4K} = (1 - (1+i)x)^{4K}:
      q_{K,0} = K / ((4K+1) * 2^{4K-2}),
      q_{K,j} = (-1)^j C(4K, j) 2^{-(4K-j)} [1 + 2^{-j-1} Im[(1+i)^j]]  (1 <= j <= 4K),
      P_{4K+1}(x) = 4 \\int_0^x Q_{4K}(t) dt.
    """
    Q_poly = [Fraction(0)] * (4 * K + 1)
    P_poly = [Fraction(0)] * (4 * K + 2)
    Q_poly[0] = Fraction(K, (4 * K + 1) * (2 ** (4 * K - 2)))
    P_poly[1] = Fraction(4) * Q_poly[0]
    for j in range(1, 4 * K + 1):
        a, b = 1, 0
        for _ in range(j):
            a, b = a - b, a + b
        q_kj = Fraction((-1) ** j * comb(4 * K, j), 2 ** (4 * K - j)) * (
            Fraction(1) + Fraction(b, 2 ** (j + 1))
        )
        Q_poly[j] = q_kj
        P_poly[j + 1] = Fraction(4, j + 1) * q_kj
    return P_poly, Q_poly


def verify_theorem_4_stereo_hodge_decomposition(max_K: int = 3) -> Dict[str, object]:
    """
    THEOREM 4 (Canonical Stereo Direct-Sum / Hodge-Fredholm Decomposition of V_{4K+1} and W_{4K}):
      Let V_{4K+1} = {P in Q[x]_{<= 4K+1} : P(0) = P(1) = 0} (dim = 4K) and
      W_{4K} = {Q in Q[x]_{<= 4K} : \\int_0^1 Q(x) dx = 0} (dim = 4K).
      Then for every K >= 1, V_{4K+1} and W_{4K} split into exact canonical direct sums
      combining Lane A's kernel basis (`seq 241`) and Lane B's biorthogonal projector basis (`seq 242`):
        V_{4K+1} = span{P_{4m+1}(x)}_{m=1}^K (dim K, ker M)
                   (+) span{\\Phi_{I_0,k}(x), \\Phi_{H_0,k}(x), \\Phi_{m_0,k+1}(x)}_{k=0}^{K-1} (dim 3K, coim M),
        W_{4K}   = span{Q_{4m}(x)}_{m=1}^K (dim K, ker <., \\hat{\\psi}_r^2>)
                   (+) span{\\Psi_{I_0,k}(x), \\Psi_{H_0,k}(x), \\Psi_{m_0,k+1}(x)}_{k=0}^{K-1} (dim 3K).
      In particular, for every basis element b_p(x) = x^p - x (2 <= p <= 4K+1), subtracting its
      biorthogonal coimage projection \\Pi_{coim}(b_p) leaves a remainder lying identically in
      span{P_{4m+1}(x) : 1 <= m <= (p-1)//4}.
    """
    projectors = build_biorthogonal_projectors(max_k=max_K - 1)
    P_ker: Dict[int, List[Fraction]] = {}
    Q_ker: Dict[int, List[Fraction]] = {}

    for m in range(1, max_K + 1):
        P_m, Q_m = build_lane_a_single_term_P_and_Q(m)
        assert poly_eval(P_m, Fraction(0)) == 0 and poly_eval(P_m, Fraction(1)) == 0
        assert poly_moment_signature(P_m) == {}, f"P_{4*m+1} not in kernel!"
        # Check mean-zero pin on Q_{4m}: \int_0^1 Q_{4m}(x) dx = P_{4m+1}(1)/4 == 0
        int_Q = sum(c / Fraction(j + 1) for j, c in enumerate(Q_m))
        assert int_Q == 0, f"Q_{4*m} not mean-zero!"
        P_ker[m] = P_m
        Q_ker[m] = Q_m

    kernel_coord_table: Dict[str, Dict[str, str]] = {}
    for p in range(2, 4 * max_K + 2):
        bp = [Fraction(0)] * (p + 1)
        bp[1] = Fraction(-1)
        bp[p] = Fraction(1)
        sig = poly_moment_signature(bp)
        rem = list(bp)
        for key, coeff in sig.items():
            rem = poly_add(rem, projectors[key]["Phi"], Fraction(1), -coeff)

        ker_coeffs: Dict[str, str] = {}
        for m in range(max_K, 0, -1):
            deg_m = 4 * m + 1
            if len(rem) > deg_m and rem[deg_m] != 0:
                c_m = rem[deg_m] / P_ker[m][deg_m]
                ker_coeffs[f"P_{deg_m}"] = str(c_m)
                rem = poly_add(rem, P_ker[m], Fraction(1), -c_m)
        assert rem == [Fraction(0)], f"Direct-sum decomposition failed at p={p}: rem={rem}"
        kernel_coord_table[f"x^{p}-x"] = ker_coeffs

    return {
        "status": "PASS",
        "max_K": max_K,
        "max_degree_verified": 4 * max_K + 1,
        "dimensions_at_max_K": {
            "dim_V_4K1": 4 * max_K,
            "dim_ker_Lane_A": max_K,
            "dim_coim_Lane_B": 3 * max_K,
        },
        "kernel_coordinates_of_xp_minus_x": kernel_coord_table,
    }


def main() -> None:
    res1 = verify_theorem_1(max_m=12, max_j=5)
    res23 = verify_theorems_2_and_3()
    res4 = verify_theorem_4_stereo_hodge_decomposition(max_K=3)

    report = {
        "script": "gaussian_toeplitz_convolution_and_biorthogonal_projectors_2026_11_15.py",
        "lane": "Lane B (Ден Б / ompu-7f698bd908)",
        "date": "2026-11-15",
        "revision": 102,
        "theorem_1_three_sector_annihilation_and_toeplitz": res1,
        "theorems_2_and_3_egf_secular_and_biorthogonal_projectors": res23,
        "theorem_4_stereo_direct_sum_hodge_decomposition": res4,
        "verdict": "ALL_CHECKS_PASSED",
    }

    out_path = Path(__file__).with_name(
        "gaussian_toeplitz_convolution_and_biorthogonal_projectors_2026_11_15_results.json"
    )
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=" * 76)
    print("LANE B LAB VERIFICATION: GAUSSIAN TOEPLITZ & BIORTHOGONAL PROJECTORS")
    print("=" * 76)
    print(f"[PASS] Theorem 1: 3-sector annihilation up to deg={res1['max_annihilation_degree']}, "
          f"Toeplitz convolutions u_j, v_j, w_j, d_j up to j={res1['max_toeplitz_index_j']} "
          f"(deg={res1['max_polynomial_degree']})")
    print(f"[PASS] Theorem 2: 4-sector Laplace-Krylov EGF & removable-singularity secular eq "
          f"(max_secular_err={res23['max_secular_Determinant_error']}, "
          f"max_egf_err={res23['max_egf_rational_krylov_error']})")
    print(f"[PASS] Theorem 3: Biorthogonal projectors Phi_{{alpha,k}} & pure-beam Psi_{{alpha,k}} "
          f"for {res23['verified_projectors']} (max_beam_err={res23['max_pure_beam_projector_error']})")
    print(f"[PASS] Theorem 4: Stereo Direct-Sum V_{{4K+1}} (dim {4*res4['max_K']}) = "
          f"Ker_A (dim {res4['max_K']}) (+) Coim_B (dim {3*res4['max_K']}) up to p={res4['max_degree_verified']}")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
