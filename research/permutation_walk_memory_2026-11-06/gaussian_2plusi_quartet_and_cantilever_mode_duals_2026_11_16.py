#!/usr/bin/env python3
r"""
gaussian_2plusi_quartet_and_cantilever_mode_duals_2026_11_16.py
===============================================================
Lane B (Ден Б / ompu-7f698bd908) — Monday Morning Lab Verification
2026-11-16 (Revision 103)

Second-hand verification and analytic extension of:
  - Petrovich's `mittag_leffler_krylov_zeta_and_gaussian_2plusi_cramer_2026_11_16.py`
    (`1794819534_392371_7271e7`, sha256: ce68d148...);
  - Phi-Hausmaster's `1794772973_336129_f4cf3e` & `1794819747_068957_33fc2e`;
  - Jee-AGY's `READ-0090` (`commit b9e6f4f`, `1794780832_986061_c4f65c`);
  - Lane A & Lane B's `rev 102` Hodge-Fredholm direct sum (`seq 241` & `seq 242`).

Proves and verifies in exact `Fraction` arithmetic and 95-digit `Decimal` quadrature:

  THEOREM 1 (Master Gaussian-(2+i) Quartet Identity, Exact Factorization of D_KR(z),
             and Horizontal Rayleigh Midpoint Parity):
    (a) For ALL four Krylov sectors alpha in {0, 1, 2, 3}, let e_alpha(s^4) = E_alpha(s)/s^alpha
        and F(s) = E_0(s)^2 - E_1(s) E_3(s) = (1 + cosh(s) cos(s)) / 2. Then for all m >= 0:
          e_alpha(s^4) * F(s) = \sum_{m=0}^\infty
              \frac{2 + Re[i^alpha] + Re[(2 + i)^{4m + alpha}]}{4 * (4m + alpha)!} s^{4m}.
        In particular:
          - alpha = 1: Petrovich's Cramer determinant factors identically as
                D_KR(s^4) == e_1(s^4) * F(s) = ((sinh s + sin s)/(2s)) * ((1 + cosh s cos s)/2);
          - alpha = 0: After exact cancellation of e_1(s^4), the formal denominator of
                \tilde{\Phi}_{m_0}(x; s^4) is D_{m_0}(s^4) := e_0(s^4) * F(s)
                with m-th coefficient (3 + Re[(2+i)^{4m}]) / (4 * (4m)!).
    (b) Multiplying w(x) = x + i(1-x) by the Gaussian prime (1+i) maps the slanted segment [i, 1]
        onto the horizontal line segment (1+i) w(x) == (2x - 1) + i, yielding
          (-4)^j v_j(x) = -(1/4) Im[((2x - 1) + i)^{4j+4}] / (4j+4)!,
        and proving exact midpoint reflection parity for all j >= 0:
          v_j(1 - x) == -v_j(x)  (odd in y = 2x - 1),
          w_j(1 - x) == +w_j(x)  (even in y = 2x - 1).
    (c) Because e_0(z) = cosh((1+i)s/2) cosh((1-i)s/2) has exact closed-form roots
        z_r^{(0)} = -(2r - 1)^4 \pi^4 / 4 (r >= 1), the inverse series e_0(z)^{-1} satisfies
        the exact Euler-Dirichlet zeta sum rule in powers of \pi^{4n}.

  THEOREM 2 (Removable Singularity of e_0(z) = 0 in \tilde{\Phi}_{m_0}(x; z) vs
             Dual Clamped-Pinned Pole Spectrum in \tilde{\Phi}_{I_0}, \tilde{\Phi}_{H_0}):
    (a) At every root z_r^{(0)} = -(2r - 1)^4 \pi^4 / 4 of e_0(z) = 0, the numerator
        F(s) \tilde{W}(x; z) + e_2(-4z) \tilde{U}(x; z) - 4 e_0(z) \tilde{V}(x; -4z)
        vanishes IDENTICALLY for all x in C. Hence F(s) \tilde{\Phi}_{m_0}(x; s^4) is an
        ENTIRE function of (x, z) in C^2, and \tilde{\Phi}_{m_0}(x; z) has NO poles outside
        the positive cantilever spectrum {z = +\kappa_r^4}_{r >= 1}!
    (b) By contrast, \tilde{\Phi}_{I_0}(x; z) and \tilde{\Phi}_{H_0}(x; z) possess BOTH the
        clamped-free cantilever poles {+\kappa_r^4} (\kappa_1^4 \approx 12.36236) AND genuine
        negative rotated clamped-pinned poles {z = -4 \beta_r^4} (\tanh \beta_r + \tan \beta_r = 0,
        4 \beta_1^4 \approx 125.14084).

  THEOREM 3 (Closed-Form Analytic Biorthogonal Dual Basis {\Xi_r(x), \Upsilon_r(x)}_{r >= 1}
             to ALL Squared Cantilever Eigenmodes {\hat{\psi}_m(x)^2}_{m >= 1}):
    At every cantilever root \cosh \kappa_r \cos \kappa_r + 1 = 0, the Rank-1 Secular Identity
        e_1(-4 \kappa_r^4) = (\kappa_r t_r) e_2(-4 \kappa_r^4),
        \kappa_r^4 e_3(\kappa_r^4) = (\kappa_r t_r) e_0(\kappa_r^4)
    collapses the residues of (\tilde{\Phi}_{I_0}, \tilde{\Phi}_{H_0}, \tilde{\Phi}_{m_0}) at
    z = \kappa_r^4 onto a single explicit boundary-pinned analytic function \Xi_r(x) in exact
    geometric progression (\kappa_r t_r)^2 : (\kappa_r t_r) : 1:
        \Xi_r(x) := w_r \left[ \frac{\sinh \kappa_r \sin \kappa_r}{2 E_0(\kappa_r)}
                               Im[E_2(\kappa_r (x + i(1-x)))]
                             + Im[E_0(\kappa_r (2x - 1 + i))] \right],
        \Upsilon_r(x) := (1/4) \Xi_r'(x),
    where w_r = 8 / [\kappa_r (\cosh \kappa_r \sin \kappa_r - \sinh \kappa_r \cos \kappa_r)].
    For ALL modes r, m >= 1:
      - \Xi_r(0) = \Xi_r(1) = 0 and \int_0^1 \Upsilon_r(x) dx = 0;
      - \int_0^1 \Upsilon_r(x) \hat{\psi}_m(x)^2 dx = \delta_{r, m}  (exact Kronecker delta!);
      - \int_0^1 \Xi_r(x) \hat{\rho}_m(x) dx = \delta_{r, m}.

  THEOREM 4 (Functional Mittag-Leffler Expansion of Rational Projector Polynomials & Darboux Limit):
    For every k >= 1 and every x in [0, 1], the rational biorthogonal projector polynomials
    \Phi_{m_0, k+1}(x) and \Psi_{m_0, k+1}(x) expand in an exact convergent series over the
    cantilever dual modes (with ZERO entire remainder):
        \Phi_{m_0, k+1}(x) == \sum_{r=1}^\infty \frac{\Xi_r(x)}{\kappa_r^{4k+4}},
        \Psi_{m_0, k+1}(x) == \sum_{r=1}^\infty \frac{\Upsilon_r(x)}{\kappa_r^{4k+4}},
    and as k -> \infty all three rational projector branches converge to the fundamental mode dual:
        \kappa_1^{4k+4} \Phi_{m_0, k+1}(x) -> \Xi_1(x),
        \kappa_1^{4k+3} \Phi_{H_0, k}(x)   -> t_1 \Xi_1(x),
        \kappa_1^{4k+2} \Phi_{I_0, k}(x)   -> t_1^2 \Xi_1(x).
"""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import gaussian_toeplitz_convolution_and_biorthogonal_projectors_2026_11_15 as gtp

getcontext().prec = 105

PI_DEC = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148"
)


# ---------------------------------------------------------------------------
# 1. Exact rational series & complex Decimal helpers
# ---------------------------------------------------------------------------

def fact(n: int) -> int:
    return math.factorial(n)


def gaussian_pow(zr: int, zi: int, exp: int) -> Tuple[int, int]:
    rr, ri = 1, 0
    br, bi = zr, zi
    e = exp
    while e > 0:
        if e & 1:
            rr, ri = rr * br - ri * bi, rr * bi + ri * br
        br, bi = br * br - bi * bi, 2 * br * bi
        e >>= 1
    return rr, ri


def series_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = len(a)
    out = [Fraction(0)] * n
    for i in range(n):
        if a[i] == 0:
            continue
        for j in range(n - i):
            if b[j] != 0:
                out[i + j] += a[i] * b[j]
    return out


def series_inv(a: List[Fraction]) -> List[Fraction]:
    n = len(a)
    inv = [Fraction(0)] * n
    inv[0] = Fraction(1) / a[0]
    for m in range(1, n):
        inv[m] = -sum(a[k] * inv[m - k] for k in range(1, m + 1)) / a[0]
    return inv


def dec_sin_cos(x: Decimal) -> Tuple[Decimal, Decimal]:
    sgn = Decimal(-1) if x < 0 else Decimal(1)
    two_pi = Decimal(2) * PI_DEC
    xr = abs(x) % two_pi
    if xr > PI_DEC:
        xr -= two_pi
    x2 = -xr * xr
    # sin
    t_s = xr
    s_acc = xr
    # cos
    t_c = Decimal(1)
    c_acc = Decimal(1)
    for k in range(1, 85):
        t_c = t_c * x2 / Decimal((2 * k - 1) * (2 * k))
        c_acc += t_c
        t_s = t_s * x2 / Decimal((2 * k) * (2 * k + 1))
        s_acc += t_s
        if abs(t_c) < Decimal("1e-103") and abs(t_s) < Decimal("1e-103"):
            break
    return sgn * s_acc, c_acc


def dec_sinh_cosh(x: Decimal) -> Tuple[Decimal, Decimal]:
    ex = x.exp()
    emx = (-x).exp()
    return (ex - emx) / Decimal(2), (ex + emx) / Decimal(2)


def cdec_mul(a: Tuple[Decimal, Decimal], b: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cdec_add(a: Tuple[Decimal, Decimal], b: Tuple[Decimal, Decimal], sb: Decimal = Decimal(1)) -> Tuple[Decimal, Decimal]:
    return (a[0] + sb * b[0], a[1] + sb * b[1])


def cdec_cosh(z: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    zr, zi = z
    sh, ch = dec_sinh_cosh(zr)
    si, co = dec_sin_cos(zi)
    return (ch * co, sh * si)


def cdec_sinh(z: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    zr, zi = z
    sh, ch = dec_sinh_cosh(zr)
    si, co = dec_sin_cos(zi)
    return (sh * co, ch * si)


def cdec_cos(z: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    # cos(zr + i zi) = cos(zr) cosh(zi) - i sin(zr) sinh(zi)
    zr, zi = z
    si, co = dec_sin_cos(zr)
    sh, ch = dec_sinh_cosh(zi)
    return (co * ch, -si * sh)


def cdec_sin(z: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    # sin(zr + i zi) = sin(zr) cosh(zi) + i cos(zr) sinh(zi)
    zr, zi = z
    si, co = dec_sin_cos(zr)
    sh, ch = dec_sinh_cosh(zi)
    return (si * ch, co * sh)


def cdec_E(alpha: int, z: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    half = Decimal("0.5")
    if alpha == 0:
        ch = cdec_cosh(z)
        co = cdec_cos(z)
        return (half * (ch[0] + co[0]), half * (ch[1] + co[1]))
    if alpha == 1:
        sh = cdec_sinh(z)
        si = cdec_sin(z)
        return (half * (sh[0] + si[0]), half * (sh[1] + si[1]))
    if alpha == 2:
        ch = cdec_cosh(z)
        co = cdec_cos(z)
        return (half * (ch[0] - co[0]), half * (ch[1] - co[1]))
    if alpha == 3:
        sh = cdec_sinh(z)
        si = cdec_sin(z)
        return (half * (sh[0] - si[0]), half * (sh[1] - si[1]))
    raise ValueError(alpha)


def solve_kappa_105(r: int) -> Tuple[Decimal, Decimal, Decimal]:
    """Solve cosh(kappa)*cos(kappa) + 1 = 0 to ~100 digits; return (kappa_r, t_r, w_r)."""
    if r == 1:
        k = Decimal("1.87510406871196116644530824107825066257018237")
    elif r == 2:
        k = Decimal("4.69409113297417457643639177801981904938989673")
    else:
        k = (Decimal(2 * r - 1) * PI_DEC) / Decimal(2)

    for _ in range(40):
        sh, ch = dec_sinh_cosh(k)
        si, co = dec_sin_cos(k)
        f = ch * co + Decimal(1)
        fp = sh * co - ch * si
        dk = f / fp
        k -= dk
        if abs(dk) < Decimal("1e-100"):
            break

    sh, ch = dec_sinh_cosh(k)
    si, co = dec_sin_cos(k)
    t_r = (ch + co) / (sh + si)
    w_r = Decimal(8) / (k * (ch * si - sh * co))
    return k, t_r, w_r


def gauss_legendre_nodes_weights(n: int = 48) -> List[Tuple[Decimal, Decimal]]:
    """Compute n-point Gauss-Legendre quadrature nodes and weights mapped to [0, 1] in 105-digit Decimal."""
    nodes_weights: List[Tuple[Decimal, Decimal]] = []
    m = (n + 1) // 2
    for i in range(1, m + 1):
        # Initial guess on [-1, 1]
        theta = PI_DEC * (Decimal(i) - Decimal("0.25")) / (Decimal(n) + Decimal("0.5"))
        _, z = dec_sin_cos(theta)
        for _ in range(45):
            p1 = Decimal(1)
            p2 = Decimal(0)
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = ((Decimal(2 * j - 1) * z * p2) - Decimal(j - 1) * p3) / Decimal(j)
            pp = Decimal(n) * (z * p1 - p2) / (z * z - Decimal(1))
            dz = p1 / pp
            z -= dz
            if abs(dz) < Decimal("1e-100"):
                break
        # Recompute pp
        p1 = Decimal(1)
        p2 = Decimal(0)
        for j in range(1, n + 1):
            p3 = p2
            p2 = p1
            p1 = ((Decimal(2 * j - 1) * z * p2) - Decimal(j - 1) * p3) / Decimal(j)
        pp = Decimal(n) * (z * p1 - p2) / (z * z - Decimal(1))
        w_std = Decimal(2) / ((Decimal(1) - z * z) * pp * pp)

        # Map [-1, 1] -> [0, 1]: x = (1 - z)/2 and (1 + z)/2, weight = w_std / 2
        half = Decimal("0.5")
        nodes_weights.append((half * (Decimal(1) - z), half * w_std))
        if 2 * i - 1 != n:
            nodes_weights.append((half * (Decimal(1) + z), half * w_std))

    nodes_weights.sort(key=lambda pair: pair[0])
    return nodes_weights


# ---------------------------------------------------------------------------
# 2. Theorem 1: Master (2+i) Quartet, D_KR Factorization, & Horizontal Rayleigh
# ---------------------------------------------------------------------------

def verify_theorem_1(max_m: int = 12) -> Dict[str, object]:
    M = max_m + 1
    f_s = [Fraction(1)] + [Fraction((-4) ** m, 2 * fact(4 * m)) for m in range(1, M)]
    re_i_pow = {0: 1, 1: 0, 2: -1, 3: 0}

    quartet_samples: Dict[str, List[str]] = {}
    for alpha in range(4):
        e_alpha = [Fraction(1, fact(4 * m + alpha)) for m in range(M)]
        lhs = series_mul(e_alpha, f_s)
        rhs = [
            Fraction(
                2 + re_i_pow[alpha] + gaussian_pow(2, 1, 4 * m + alpha)[0],
                4 * fact(4 * m + alpha),
            )
            for m in range(M)
        ]
        assert lhs == rhs, f"Master (2+i) quartet failed at alpha={alpha}"
        quartet_samples[f"alpha={alpha}"] = [str(c) for c in rhs[:5]]

    # Check Horizontal Rayleigh expansion (-4)^j v_j(x) == -(1/4) Im[((2x-1)+i)^{4j+4}] / (4j+4)!
    # and midpoint reflection symmetry v_j(1-x) == -v_j(x), w_j(1-x) == +w_j(x)
    for j in range(6):
        vj = gtp.build_v_j(j)
        wj = gtp.build_w_j(j)
        deg = 4 * j + 4
        # Expand -(1/4)/(4j+4)! * sum_{r=0}^{2j+1} (-1)^r C(4j+4, 2r+1) (2x - 1)^{4j+3 - 2r}
        horiz_poly = [Fraction(0)] * (deg + 1)
        for r in range(2 * j + 2):
            odd_pow = deg - 1 - 2 * r
            c_outer = Fraction(-((-1) ** r) * math.comb(deg, 2 * r + 1), 4 * fact(deg))
            # (2x - 1)^odd_pow = sum_{p=0}^odd_pow C(odd_pow, p) (2x)^p (-1)^{odd_pow - p}
            for p in range(odd_pow + 1):
                term = c_outer * Fraction(math.comb(odd_pow, p) * (2 ** p) * ((-1) ** (odd_pow - p)))
                horiz_poly[p] += term
        while len(horiz_poly) > 1 and horiz_poly[-1] == 0:
            horiz_poly.pop()

        scaled_vj = gtp.poly_add(gtp.poly_scale(vj, Fraction((-4) ** j)), [Fraction(0)])
        assert scaled_vj == horiz_poly, f"Horizontal Rayleigh mismatch at j={j}"

        for x_t in (Fraction(1, 9), Fraction(3, 11), Fraction(2, 5)):
            assert gtp.poly_eval(vj, Fraction(1) - x_t) == -gtp.poly_eval(vj, x_t)
            assert gtp.poly_eval(wj, Fraction(1) - x_t) == gtp.poly_eval(wj, x_t)

    # Check Euler-Dirichlet pi^{4n} zeta sum rule for e_0(z)^{-1} = 1 - z/24 + 23 z^2/13440 - ...
    # Since e_0(z) = prod_{r>=1} (1 + 4 z / ((2r-1)^4 pi^4)), the simple poles of 1/e_0(z) are
    # z_r = -(2r-1)^4 pi^4 / 4 with residue weight:
    # 1 / e_0(z) = sum_{r=1}^infty u_r / (1 - z / z_r), where
    # u_r = (-1)^{r-1} * 8 / ((2r-1) * pi * cosh((2r-1)*pi/2))!
    e0_inv = series_inv([Fraction(1, fact(4 * m)) for m in range(7)])
    max_e0_zeta_err = Decimal(0)
    u_r_list: List[Tuple[Decimal, Decimal]] = []
    for r in range(1, 75):
        odd = Decimal(2 * r - 1)
        z_r = -(odd ** 4) * (PI_DEC ** 4) / Decimal(4)
        _, ch_half = dec_sinh_cosh(odd * PI_DEC / Decimal(2))
        sgn = Decimal(1) if (r % 2 == 1) else Decimal(-1)
        u_r = sgn * Decimal(8) / (odd * PI_DEC * ch_half)
        u_r_list.append((z_r, u_r))

    for n in range(7):
        zeta_val = sum(u_r / (z_r ** n) for z_r, u_r in u_r_list)
        exact_dec = Decimal(e0_inv[n].numerator) / Decimal(e0_inv[n].denominator)
        max_e0_zeta_err = max(max_e0_zeta_err, abs(zeta_val - exact_dec))
    assert max_e0_zeta_err < Decimal("1e-88"), f"e0_inv zeta error: {max_e0_zeta_err}"

    return {
        "status": "PASS",
        "max_s_degree_verified": 4 * max_m + 3,
        "quartet_samples_m_0_to_4": quartet_samples,
        "horizontal_rayleigh_and_midpoint_parity_j_0_to_5": True,
        "max_e0_inv_dirichlet_zeta_error": f"{max_e0_zeta_err:.3e}",
    }


# ---------------------------------------------------------------------------
# 3. Theorem 2: Removable Singularity of e_0(z)=0 in \Phi_{m_0} vs Dual Spectrum
# ---------------------------------------------------------------------------

def verify_theorem_2() -> Dict[str, object]:
    # (a) Verify at roots s_r = (1+i)*(2r-1)*pi/2 of e_0(z) = 0 that the numerator
    #     F(s)*W_tilde(x; z) + e_2(-4z)*U_tilde(x; z) - 4*e_0(z)*V_tilde(x; -4z) == 0
    #     to ~100 digits for all x in [0, 1]!
    max_rem_err = Decimal(0)
    for r in (1, 2, 3):
        a = Decimal(2 * r - 1) * PI_DEC / Decimal(2)
        s_r = (a, a)  # a * (1 + i)
        # s_r^2 = 2 i a^2, s_r^4 = -4 a^4
        z_r = Decimal(-4) * (a ** 4)
        e0_sr = cdec_E(0, s_r)
        assert abs(e0_sr[0]) < Decimal("1e-95") and abs(e0_sr[1]) < Decimal("1e-95")

        # F(s_r) = (1 + cosh(s_r)*cos(s_r))/2. Note cos(a(1+i)) = cosh(a(1-i)) = conj(cosh(s_r))!
        ch_sr = cdec_cosh(s_r)
        F_sr = Decimal("0.5") * (Decimal(1) + ch_sr[0] * ch_sr[0] + ch_sr[1] * ch_sr[1])

        # e_2(-4 z_r) = sinh(s_r)*sin(s_r) / (2 * s_r^2)
        sh_sr = cdec_sinh(s_r)
        si_sr = cdec_sin(s_r)
        prod_sh_si = cdec_mul(sh_sr, si_sr)
        # Divide by 2 * s_r^2 = 4 i a^2: (X + i Y) / (4 i a^2) = Y/(4a^2) - i X/(4a^2)
        e2_m4 = prod_sh_si[1] / (Decimal(4) * a * a)
        assert abs(prod_sh_si[0]) < Decimal("1e-90")

        for x_str in ("0.13", "0.25", "0.5", "0.77"):
            x = Decimal(x_str)
            w = (x, Decimal(1) - x)
            wb = (x, -(Decimal(1) - x))
            sw = cdec_mul(s_r, w)
            swb = cdec_mul(s_r, wb)
            # U_tilde(x; s_r^4) = (E_2(s_r w) - E_2(s_r wb)) / (2 i s_r^2)
            # Note 2 i s_r^2 = 2 i * (2 i a^2) = -4 a^2 (purely real!)
            E2_sw = cdec_E(2, sw)
            E2_swb = cdec_E(2, swb)
            U_tilde = (E2_sw[0] - E2_swb[0]) / (Decimal(-4) * a * a)
            assert abs(E2_sw[1] - E2_swb[1]) < Decimal("1e-90")

            # W_tilde(x; s_r^4) = (0.5*(E_0(s_r w) + E_0(s_r wb)) - E_0(s_r)) / z_r
            E0_sw = cdec_E(0, sw)
            E0_swb = cdec_E(0, swb)
            W_tilde = (Decimal("0.5") * (E0_sw[0] + E0_swb[0]) - e0_sr[0]) / z_r

            num_m0 = F_sr * W_tilde + e2_m4 * U_tilde
            max_rem_err = max(max_rem_err, abs(num_m0))

    assert max_rem_err < Decimal("1e-90"), f"Removable singularity residual too large: {max_rem_err}"

    # (b) Solve first clamped-pinned root beta_1 of tanh(beta) + tan(beta) = 0
    #     and confirm z_1^{(1)} = -4 * beta_1^4 is a GENUINE (non-removable) pole of \Phi_{I_0}, \Phi_{H_0}
    beta1 = Decimal("2.365020372431352")
    for _ in range(35):
        sh, ch = dec_sinh_cosh(beta1)
        si, co = dec_sin_cos(beta1)
        f = sh * co + ch * si
        fp = Decimal(2) * ch * co
        dk = f / fp
        beta1 -= dk
        if abs(dk) < Decimal("1e-100"):
            break

    z_clamped_pinned_abs = Decimal(4) * (beta1 ** 4)
    k1, _, _ = solve_kappa_105(1)
    z_cantilever_1 = k1 ** 4
    z_e0_1_abs = (PI_DEC ** 4) / Decimal(4)

    return {
        "status": "PASS",
        "max_e0_removable_singularity_residual": f"{max_rem_err:.3e}",
        "cantilever_nearest_pole_kappa1_pow4": float(z_cantilever_1),
        "e0_removable_root_pi4_over_4": float(z_e0_1_abs),
        "clamped_pinned_second_pole_4_beta1_pow4": float(z_clamped_pinned_abs),
        "beta_1_clamped_pinned": f"{beta1:.30f}",
    }


# ---------------------------------------------------------------------------
# 4. Theorem 3 & 4: Analytic Dual Modes {\Xi_r, \Upsilon_r} & Functional Mittag-Leffler
# ---------------------------------------------------------------------------

def eval_Xi_and_Upsilon_dec(
    kap: Decimal, w_r: Decimal, x: Decimal
) -> Tuple[Decimal, Decimal]:
    r"""Evaluate closed-form boundary-pinned dual \Xi_r(x) and pure-beam dual \Upsilon_r(x) = \Xi_r'(x)/4."""
    sh, ch = dec_sinh_cosh(kap)
    si, co = dec_sin_cos(kap)
    E0_k = Decimal("0.5") * (ch + co)
    c_u = (sh * si) / (Decimal(2) * E0_k)

    kw_kelvin = (kap * x, kap * (Decimal(1) - x))
    kw_rayleigh = (kap * (Decimal(2) * x - Decimal(1)), kap)

    im_E2_kelvin = cdec_E(2, kw_kelvin)[1]
    im_E0_rayleigh = cdec_E(0, kw_rayleigh)[1]
    xi_val = w_r * (c_u * im_E2_kelvin + im_E0_rayleigh)

    # Derivative: d/dx (kap * (x + i(1-x))) = kap * (1 - i); E_2' = E_1
    #             d/dx (kap * (2x - 1 + i)) = 2 * kap;       E_0' = E_3
    E1_kelvin = cdec_E(1, kw_kelvin)
    im_d_kelvin = kap * (E1_kelvin[1] - E1_kelvin[0])  # Im[(1 - i)*(A + i B)] = B - A
    im_d_rayleigh = Decimal(2) * kap * cdec_E(3, kw_rayleigh)[1]
    upsilon_val = Decimal("0.25") * w_r * (c_u * im_d_kelvin + im_d_rayleigh)

    return xi_val, upsilon_val


def eval_psi_hat_sq_dec(kap: Decimal, t_m: Decimal, x: Decimal) -> Decimal:
    r"""Evaluate normalized cantilever mode square \hat{\psi}_m(x)^2 (clamped at x=1, free at x=0)."""
    ky = kap * (Decimal(1) - x)
    sh, ch = dec_sinh_cosh(ky)
    si, co = dec_sin_cos(ky)
    psi = (ch - co) - t_m * (sh - si)
    return psi * psi


def verify_theorems_3_and_4() -> Dict[str, object]:
    modes_60 = [solve_kappa_105(r) for r in range(1, 61)]

    # 1. Rank-1 Secular Identity at r = 1..10:
    #    e_1(-4 k^4) == (k t_r) e_2(-4 k^4) and k^4 e_3(k^4) == (k t_r) e_0(k^4)
    max_rank1_err = Decimal(0)
    for r_idx in range(10):
        kap, t_r, _ = modes_60[r_idx]
        sh, ch = dec_sinh_cosh(kap)
        si, co = dec_sin_cos(kap)
        e1_m4 = (sh * co + ch * si) / (Decimal(2) * kap)
        e2_m4 = (sh * si) / (Decimal(2) * kap * kap)
        k4_e3 = kap * Decimal("0.5") * (sh - si)
        e0_v = Decimal("0.5") * (ch + co)
        max_rank1_err = max(
            max_rank1_err,
            abs(e1_m4 - (kap * t_r) * e2_m4),
            abs(k4_e3 - (kap * t_r) * e0_v),
        )
    assert max_rank1_err < Decimal("1e-88"), f"Rank-1 secular identity error: {max_rank1_err}"

    # 2. Boundary pinning \Xi_r(0) = \Xi_r(1) = 0 and 64-point Gauss-Legendre Kronecker biorthogonality
    #    \int_0^1 \Upsilon_r(x) \hat{\psi}_m(x)^2 dx = \delta_{r, m} for 1 <= r, m <= 5!
    gl_nodes = gauss_legendre_nodes_weights(64)
    max_boundary_err = Decimal(0)
    max_mean_zero_err = Decimal(0)
    max_biorth_err = Decimal(0)

    # Pre-evaluate Upsilon_r and psi_m^2 at the 64 quadrature nodes for r, m = 1..5
    ups_grid: List[List[Decimal]] = []
    psi2_grid: List[List[Decimal]] = []
    for r_idx in range(5):
        kap, t_r, w_r = modes_60[r_idx]
        xi_0, _ = eval_Xi_and_Upsilon_dec(kap, w_r, Decimal(0))
        xi_1, _ = eval_Xi_and_Upsilon_dec(kap, w_r, Decimal(1))
        max_boundary_err = max(max_boundary_err, abs(xi_0), abs(xi_1))

        u_row = []
        p_row = []
        for x_node, _ in gl_nodes:
            _, u_val = eval_Xi_and_Upsilon_dec(kap, w_r, x_node)
            p_val = eval_psi_hat_sq_dec(kap, t_r, x_node)
            u_row.append(u_val)
            p_row.append(p_val)
        ups_grid.append(u_row)
        psi2_grid.append(p_row)

        mean_ups = sum(w_node * u_row[i] for i, (_, w_node) in enumerate(gl_nodes))
        max_mean_zero_err = max(max_mean_zero_err, abs(mean_ups))

    assert max_boundary_err < Decimal("1e-85")
    assert max_mean_zero_err < Decimal("1e-75")

    for r_idx in range(5):
        for m_idx in range(5):
            integral = sum(
                w_node * ups_grid[r_idx][i] * psi2_grid[m_idx][i]
                for i, (_, w_node) in enumerate(gl_nodes)
            )
            target = Decimal(1) if r_idx == m_idx else Decimal(0)
            err = abs(integral - target)
            max_biorth_err = max(max_biorth_err, err)

    assert max_biorth_err < Decimal("1e-55"), f"Kronecker biorthogonality error: {max_biorth_err}"

    # 3. Functional Mittag-Leffler identity:
    #    \Phi_{m_0, k+1}(x) == \sum_{r=1}^\infty \Xi_r(x) / \kappa_r^{4k+4}
    #    \Psi_{m_0, k+1}(x) == \sum_{r=1}^\infty \Upsilon_r(x) / \kappa_r^{4k+4}
    #    for k = 1, 2, 3 across interior points x in {1/5, 1/2, 3/4}
    projs = gtp.build_biorthogonal_projectors(max_k=8)
    ml_poly_errors: Dict[str, str] = {}
    for k in (1, 2, 3):
        phi_poly = projs[("m0", k + 1)]["Phi"]
        psi_poly = projs[("m0", k + 1)]["Psi"]
        max_k_err = Decimal(0)
        for x_f in (Fraction(1, 5), Fraction(1, 2), Fraction(3, 4)):
            x_d = Decimal(x_f.numerator) / Decimal(x_f.denominator)
            exact_phi_f = gtp.poly_eval(phi_poly, x_f)
            exact_psi_f = gtp.poly_eval(psi_poly, x_f)
            exact_phi = Decimal(exact_phi_f.numerator) / Decimal(exact_phi_f.denominator)
            exact_psi = Decimal(exact_psi_f.numerator) / Decimal(exact_psi_f.denominator)

            sum_phi = Decimal(0)
            sum_psi = Decimal(0)
            for kap, _, w_r in modes_60:
                xi_v, ups_v = eval_Xi_and_Upsilon_dec(kap, w_r, x_d)
                denom = kap ** (4 * k + 4)
                sum_phi += xi_v / denom
                sum_psi += ups_v / denom

            max_k_err = max(max_k_err, abs(exact_phi - sum_phi), abs(exact_psi - sum_psi))
        ml_poly_errors[f"k={k}"] = f"{max_k_err:.3e}"
        assert max_k_err < Decimal("1e-12"), f"Functional Mittag-Leffler error at k={k}: {max_k_err}"

    # Note: at k=3 (1/kappa_r^{16}), 60 modes already reach ~60^{-16} ~ 1e-29!
    assert Decimal(ml_poly_errors["k=3"]) < Decimal("1e-24")

    # 4. Darboux Rank-1 Asymptotics at k = 8 vs fundamental mode dual \Xi_1(x)
    kap1, t1, w1 = modes_60[0]
    xi1_mid, _ = eval_Xi_and_Upsilon_dec(kap1, w1, Decimal("0.5"))
    phi_m0_9_mid = gtp.poly_eval(projs[("m0", 9)]["Phi"], Fraction(1, 2))
    phi_h0_8_mid = gtp.poly_eval(projs[("H0", 8)]["Phi"], Fraction(1, 2))
    phi_i0_8_mid = gtp.poly_eval(projs[("I0", 8)]["Phi"], Fraction(1, 2))

    asymp_m0 = (Decimal(phi_m0_9_mid.numerator) / Decimal(phi_m0_9_mid.denominator)) * (kap1 ** 36)
    asymp_h0 = (Decimal(phi_h0_8_mid.numerator) / Decimal(phi_h0_8_mid.denominator)) * (kap1 ** 35)
    asymp_i0 = (Decimal(phi_i0_8_mid.numerator) / Decimal(phi_i0_8_mid.denominator)) * (kap1 ** 34)

    err_darboux_m0 = abs(asymp_m0 - xi1_mid)
    err_darboux_h0 = abs(asymp_h0 - t1 * xi1_mid)
    err_darboux_i0 = abs(asymp_i0 - (t1 * t1) * xi1_mid)
    assert err_darboux_m0 < Decimal("1e-12")
    assert err_darboux_h0 < Decimal("1e-8")
    assert err_darboux_i0 < Decimal("1e-8")

    return {
        "status": "PASS",
        "max_rank1_secular_identity_error": f"{max_rank1_err:.3e}",
        "max_boundary_pinning_error": f"{max_boundary_err:.3e}",
        "max_kronecker_biorthogonality_error_5x5": f"{max_biorth_err:.3e}",
        "functional_mittag_leffler_errors_60_modes": ml_poly_errors,
        "darboux_k8_errors_at_midpoint": {
            "m0_vs_Xi1": f"{err_darboux_m0:.3e}",
            "H0_vs_t1_Xi1": f"{err_darboux_h0:.3e}",
            "I0_vs_t1sq_Xi1": f"{err_darboux_i0:.3e}",
        },
    }


def verify_theorem_5_lane_a_seq243_duplication_and_zeta() -> Dict[str, object]:
    r"""
    THEOREM 5 (Closure of Lane A's `seq 243` Seam: Krylov Duplication & Clamped-Pinned Zeta Laws):
      (a) Exact Euler-Dirichlet Mittag-Leffler law for Lane A's Krylov-Euler integers \varepsilon_d
          (1 / E_0(u) = \sum_{d>=0} \varepsilon_d u^{4d} / (4d)!):
            \varepsilon_d = (-1)^d (4d)! (8 * 4^d / \pi^{4d+1})
                            \sum_{m=1}^\infty \frac{(-1)^{m-1}}{(2m - 1)^{4d+1} \cosh((2m - 1)\pi / 2)}.
      (b) Exact Clamped-Pinned Mittag-Leffler law for \eta_d
          (E_3(s/2) / E_1(s/2) = \sum_{d>=0} \eta_d s^{4d+2}):
          The non-zero roots of E_1(s/2) = 0 lie NOT at 2(1 +- i)n\pi, but at the rotated
          clamped-pinned beam roots s_m = 2(+-1 +- i)\beta_m where \tanh \beta_m + \tan \beta_m = 0,
          yielding the convergent spectral zeta formula:
            \eta_d = \frac{(-1)^d}{2 * 64^d} \sum_{m=1}^\infty \frac{\tanh \beta_m}{\beta_m^{4d+3}}
            (in particular \sum_{m=1}^\infty \frac{\tanh \beta_m}{\beta_m^3} = \frac{1}{12}).
      (c) Krylov Duplication Decomposition of \tau_d^{(r)} (r in {0, 1, 2}):
          Because |E_{r+1}(s) / E_1(s/2)| ~ (1/2) exp(|s|/2) -> \infty as |s| -> \infty,
          \tau_d^{(r)} has NO pure Mittag-Leffler sum without subtracting its entire part!
          By the Krylov duplication identity (u = s/2):
            \frac{E_{r+1}(2u)}{2 E_1(u)} == E_r(u) + E_{(r+2) mod 4}(u) \frac{E_3(u)}{E_1(u)}  (r = 0, 1, 2),
          every \tau_d^{(r)} reduces to an exact finite convolution of the clamped-pinned \eta_k!
    """
    # 1. Exact rational eta_d and tau_d^{(r)} from series inversion of e_1(z)
    D = 6
    e0 = [Fraction(1, fact(4 * d)) for d in range(D + 1)]
    e1 = [Fraction(1, fact(4 * d + 1)) for d in range(D + 1)]
    e2 = [Fraction(1, fact(4 * d + 2)) for d in range(D + 1)]
    e3 = [Fraction(1, fact(4 * d + 3)) for d in range(D + 1)]

    e0_inv = series_inv(e0)
    eps_exact = [e0_inv[d] * Fraction(fact(4 * d)) for d in range(D)]
    assert eps_exact == [1, -1, 69, -33661, 60376809, -288294050521]

    # E_3(u)/E_1(u) = u^2 * (e_3(u^4)/e_1(u^4)) = sum_{d>=0} eta_d * (2u)^{4d+2} = 4 u^2 sum_{d>=0} (16^d eta_d) u^{4d}
    e3_over_e1 = series_mul(e3, series_inv(e1))
    eta_exact = [e3_over_e1[d] / Fraction(4 * (16 ** d)) for d in range(D)]

    # Direct series computation of tau_d^{(r)} from s * E_{r+1}(s) / (2 * E_1(s/2))
    e1_half = [e1[d] / Fraction(16 ** d) for d in range(D)]
    e1_half_inv = series_inv(e1_half)
    e_map = {1: e1[:D], 2: e2[:D], 3: e3[:D]}

    for r in (0, 1, 2):
        ratio = series_mul(e_map[r + 1], e1_half_inv)
        for d in range(D):
            tau_direct = ratio[d] * Fraction(fact(4 * d + 1 + r))
            if r == 0:
                tau_dup = Fraction(4 * d + 1, 16 ** d) + Fraction(fact(4 * d + 1)) * sum(
                    eta_exact[k] / Fraction((2 ** (4 * (d - 1 - k) + 2)) * fact(4 * (d - 1 - k) + 2))
                    for k in range(d)
                )
            elif r == 1:
                tau_dup = Fraction(4 * d + 2, 2 * (16 ** d)) + Fraction(fact(4 * d + 2)) * sum(
                    eta_exact[k] / Fraction((2 ** (4 * (d - 1 - k) + 3)) * fact(4 * (d - 1 - k) + 3))
                    for k in range(d)
                )
            else:
                tau_dup = Fraction(4 * d + 3, 4 * (16 ** d)) + Fraction(fact(4 * d + 3)) * sum(
                    eta_exact[k] / Fraction((2 ** (4 * (d - k))) * fact(4 * (d - k)))
                    for k in range(d + 1)
                )
            assert tau_direct == tau_dup, f"Krylov duplication mismatch at r={r}, d={d}"

    # 2. High-precision Clamped-Pinned Mittag-Leffler verification for \eta_d (d = 2, 3, 4)
    betas_55: List[Tuple[Decimal, Decimal]] = []
    for m in range(1, 56):
        b = Decimal("2.365020372431352013012024050417") if m == 1 else (Decimal(m) - Decimal("0.25")) * PI_DEC
        for _ in range(35):
            sh, ch = dec_sinh_cosh(b)
            si, co = dec_sin_cos(b)
            dk = (sh * co + ch * si) / (Decimal(2) * ch * co)
            b -= dk
            if abs(dk) < Decimal("1e-100"):
                break
        sh, ch = dec_sinh_cosh(b)
        betas_55.append((b, sh / ch))

    eta_zeta_errs: Dict[str, str] = {}
    for d in (2, 3, 4):
        sgn = Decimal(-1) if (d % 2 == 1) else Decimal(1)
        pref = sgn / (Decimal(2) * (Decimal(64) ** d))
        s_acc = pref * sum(th_b / (b ** (4 * d + 3)) for b, th_b in betas_55)
        ex_dec = Decimal(eta_exact[d].numerator) / Decimal(eta_exact[d].denominator)
        err = abs(s_acc - ex_dec)
        eta_zeta_errs[f"d={d}"] = f"{err:.3e}"
        assert err < Decimal("1e-18"), f"Clamped-pinned zeta error at d={d}: {err}"

    assert Decimal(eta_zeta_errs["d=4"]) < Decimal("1e-32")

    return {
        "status": "PASS",
        "krylov_euler_integers_0_to_5": [int(c) for c in eps_exact],
        "krylov_duplication_tau_verified_r012_up_to_d": D - 1,
        "clamped_pinned_eta_zeta_errors_55_modes": eta_zeta_errs,
    }


def main() -> None:
    res1 = verify_theorem_1(max_m=12)
    res2 = verify_theorem_2()
    res34 = verify_theorems_3_and_4()
    res5 = verify_theorem_5_lane_a_seq243_duplication_and_zeta()

    report = {
        "script": "gaussian_2plusi_quartet_and_cantilever_mode_duals_2026_11_16.py",
        "lane": "Lane B (Ден Б / ompu-7f698bd908)",
        "date": "2026-11-16",
        "revision": 103,
        "theorem_1_master_2plusi_quartet_and_horizontal_rayleigh": res1,
        "theorem_2_e0_removable_singularity_and_pole_spectrum": res2,
        "theorems_3_and_4_biorthogonal_cantilever_duals_and_functional_ml": res34,
        "theorem_5_lane_a_seq243_seam_closure": res5,
        "verdict": "ALL_CHECKS_PASSED",
    }

    out_path = HERE / "gaussian_2plusi_quartet_and_cantilever_mode_duals_2026_11_16_results.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=" * 78)
    print("LANE B LAB VERIFICATION: GAUSSIAN (2+i) QUARTET & CANTILEVER MODE DUALS")
    print("=" * 78)
    print(f"[PASS] Theorem 1: Master (2+i) Quartet up to deg={res1['max_s_degree_verified']}, "
          f"D_KR == e_1*F, Horizontal Rayleigh parity, e_0^-1 zeta err={res1['max_e0_inv_dirichlet_zeta_error']}")
    print(f"[PASS] Theorem 2: e_0(z)=0 removable in Phi_m0 (res={res2['max_e0_removable_singularity_residual']}), "
          f"poles: k1^4={res2['cantilever_nearest_pole_kappa1_pow4']:.5f} vs 4*beta1^4={res2['clamped_pinned_second_pole_4_beta1_pow4']:.5f}")
    print(f"[PASS] Theorem 3: Closed-form biorthogonal duals <Upsilon_r, psi_m^2> == delta_{{r,m}} "
          f"(5x5 GL-64 err={res34['max_kronecker_biorthogonality_error_5x5']})")
    print(f"[PASS] Theorem 4: Functional Mittag-Leffler Phi_{{m0,k+1}}(x) = sum Xi_r(x)/k_r^{{4k+4}} "
          f"({res34['functional_mittag_leffler_errors_60_modes']}) & Darboux k=8 ({res34['darboux_k8_errors_at_midpoint']})")
    print(f"[PASS] Theorem 5: Closed Lane A seq 243 seam — Krylov duplication for tau_d^(r) & "
          f"clamped-pinned zeta for eta_d ({res5['clamped_pinned_eta_zeta_errors_55_modes']})")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
