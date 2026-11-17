#!/usr/bin/env python3
"""
quartet_transpose_annihilators_and_cyclic_zeta_ladders_2026_11_17.py

Self-contained stdlib-only verification module (Revision 106, Lane A, 2026-11-17 Evening).
Proves and verifies in exact `Fraction` arithmetic and 108-digit `Decimal` quadrature
(`python3 -I -B -W error`, zero external or sibling imports):

1. Theorem 1 (Universal Quartet Star Factorization, Master Green-Lagrange Boundary Identity,
   and Transpose-Green Pole-Exchange Ladders):
   - Across all four quartet domains alpha in {0, 1, 2, 3} (Dom_0, Dom_C, Dom_B, Dom_A),
     the 4-dimensional kernel ker(L_Xi^*) = ker(D^4) intersected with the 3 shared adjoint
     boundary conditions w(1) = w'(1) = w''(0) + 3 w''(1) = 0 of \\bigcap_{alpha=0}^3 Dom_alpha^*
     is 1-dimensional and spanned by the universal defect cubic w_0^*(s) = (1 - s)^2 (1 - 4s)
     (and its pure-beam partner v_0^*(y) = 4 \\int_y^1 w_0^*(s) ds = -4 y (1 - y)^3).
   - Every quartet Green's kernel differs from Dom_C (alpha = 1) by a rank-1 perturbation
     along the exact same right-hand adjoint covector w_0^*(s) (and v_0^*(y)):
         G_Xi^{(alpha)}(x, s) = G_Xi^{(C)}(x, s) + eta_alpha phi_0^{(alpha)}(x) w_0^*(s),
         G_Upsilon^{(alpha)}(x, y) = G_Upsilon^{(C)}(x, y) + eta_alpha psi_0^{(alpha)}(x) v_0^*(y),
     with eta_alpha = (2/3, 0, -1/3, -2) for alpha = (0, 1, 2, 3).
   - Master Green-Lagrange Identity: for EVERY u in C^4([0, 1]) with u(0) = 0,
         <L_Xi u, w_0^*> == \\sum_{alpha=0}^3 \\frac{3}{2^{alpha+1} alpha!} B_alpha(u)
                         == (3/2) B_0(u) + (3/4) B_1(u) + (3/16) B_2(u) + (1/32) B_3(u),
     where B_0(u) = u(1), B_1(u) = u'(0) - 3 u'(1), B_2(u) = 3 u''(0) + 5 u''(1),
     B_3(u) = 3 u'''(0) - 5 u'''(1).
   - Consequently, the transpose-Green polynomial ladders Q_{4k}^{(alpha)*}(s) = ((G_Xi^{(alpha)})^*)^{k-1} w_0^*(s)
     and P_{4k}^{(alpha)*}(y) = ((G_Upsilon^{(alpha)})^*)^{k-1} v_0^*(y) = 4 \\int_y^1 Q_{4k}^{(alpha)*}(s) ds
     annihilate the entire positive branch {Xi_r, Upsilon_r}_{r=1}^\\infty for all alpha in {0, 1, 2, 3}
     and satisfy the exact Sherman-Morrison pole-exchange convolution
         Q_{4k}^{(alpha)*}(s) == \\sum_{j=1}^k ([z^{k-j}] \\frac{e_1(z)}{alpha! e_alpha(z)}) Q_{4j}^{(1)*}(s)
     in exact Fraction for k = 1..6 (degree 24), matching the matrix-free binomial formula for Q_{4j}^{(1)*}(s).

2. Theorem 2 (Single-Branch Negative-Eigenvalue Mittag-Leffler Ladders & Two-Handed Adjoint
   Cauchy-Residue Verification Across the Quartet):
   - Because <Xi_r, Q_{4k}^{(alpha)*}> = <Upsilon_r, P_{4k}^{(alpha)*}> = 0, all four dual polynomial
     ladders expand PURELY over the single negative branch {Theta_m^{(alpha)*}(s)} and {Omega_m^{(alpha)*}(y)}
     with zero positive-branch contribution:
         Q_{4k}^{(alpha)*}(s) = (-1)^{k-1} \\sum_{m=1}^\\infty \\frac{c_m^{(alpha)*}}{|z_m^{(alpha)}|^{k-1}} Theta_m^{(alpha)*}(s),
         P_{4k}^{(alpha)*}(y) = (-1)^{k-1} \\sum_{m=1}^\\infty \\frac{c_m^{(alpha)*}}{|z_m^{(alpha)}|^{k-1}} Omega_m^{(alpha)*}(y),
     where the Master Identity yields the exact (4 - alpha)-power law
     c_m^{(alpha)*} = <Theta_m^{(alpha)}, w_0^*> = <Omega_m^{(alpha)}, v_0^*> = -3 B_alpha(Theta_m^{(alpha)}) / (2^{alpha+3} alpha! (mu_m^{(alpha)})^4):
         c_m^{(0)*} = -3 cosh(mu_m) / (4 mu_m^4)              (mu_m = (2m-1)pi/2, root-free Euler),
         c_m^{(1)*} = +3 cos^2(beta_m) cosh(beta_m) / beta_m^3 (tanh(beta_m) + tan(beta_m) = 0),
         c_m^{(2)*} = -3 (cosh^2(mu_m) + 1) / (2 mu_m^2)      (mu_m = m*pi, root-free Euler),
         c_m^{(3)*} = -cos^2(gamma_m) cosh(gamma_m) / gamma_m (tanh(gamma_m) - tan(gamma_m) = 0).
   - Second Independent Hand (Direct 4x4 Adjoint Cauchy-Residue Prover): solving the inhomogeneous
     4x4 adjoint boundary-value system on ker(L_Xi^* + 4 mu^4) with right-hand side
     [0, 0, 0, -B_{3-alpha}^*(w_0^*)] (-B_{3-alpha}^*(w_0^*) in {+48, +6, +6, -1}) and taking Cauchy
     residues at z = z_m^{(alpha)} reproduces c_m^{(alpha)*} Theta_m^{(alpha)*}(s) and c_m^{(alpha)*} Omega_m^{(alpha)*}(y)
     to > 60 digits across all alpha in {0, 1, 2, 3} without using Theta_m^{(alpha)}, N_m^{(alpha)}, or B_alpha.

3. Theorem 3 (Cyclic Quartet Derivative Ladder Dom_0 -> Dom_C -> Dom_B -> Dom_A -> Dom_0 &
   Root-Free Polynomial Integral Formulas for All Four Negative-Branch Spectral Zetas):
   - Pairing the cyclic seed differences against Q_{4k}^{(alpha)*}(s) and P_{4k}^{(alpha)*}(y) yields
     single-integral root-free polynomial formulas for all four negative-branch spectral zetas
     zeta_{neg}^{(alpha)}(4k) = \\sum_{m=1}^\\infty |z_m^{(alpha)}|^{-k} for k = 1..7:
         zeta_{neg}^{(0)}(4k) = (2^{4k}-1)|B_{4k}|/(2(4k)!) = (1/24)\\delta_{k,1} + ((-1)^{k-1}/36) <phi_0^{(0)} + 3 phi_0^{(3)}, Q_{4(k-1)}^{(0)*}>,
         zeta_{neg}^{(1)}(4k) = zeta_{cs}(4k)              = ((-1)^k/6) <phi_0^{(0)}, Q_{4k}^{(1)*}>,
         zeta_{neg}^{(2)}(4k) = |B_{4k}|/(2(4k)!)          = ((-1)^k/6) <phi_0^{(2)}, Q_{4k}^{(2)*}>,
         zeta_{neg}^{(3)}(4k) = zeta_{cp}(4k)              = ((-1)^k/4) <6 phi_0^{(3)} - phi_0^{(2)}, Q_{4k}^{(3)*}>,
     and identically with <psi_0^{(.)}, P_{4k}^{(alpha)*}>.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

getcontext().prec = 108


def compute_pi_dec() -> Decimal:
    """Compute pi to 108 digits via Machin's formula."""
    def atan_inv(m: int) -> Decimal:
        m_dec = Decimal(m)
        m2 = Decimal(m * m)
        term = Decimal(1) / m_dec
        total = term
        k = 1
        while True:
            term /= -m2
            step = term / Decimal(2 * k + 1)
            if abs(step) < Decimal("1e-109"):
                break
            total += step
            k += 1
        return total

    return Decimal(16) * atan_inv(5) - Decimal(4) * atan_inv(239)


PI_DEC = compute_pi_dec()


def dec_sinh_cosh(x: Decimal) -> Tuple[Decimal, Decimal]:
    if x == 0:
        return Decimal(0), Decimal(1)
    ex = x.exp()
    emx = Decimal(1) / ex
    return Decimal("0.5") * (ex - emx), Decimal("0.5") * (ex + emx)


def dec_sin_cos(x: Decimal) -> Tuple[Decimal, Decimal]:
    twopi = Decimal(2) * PI_DEC
    n = int((x / twopi).to_integral_value())
    r = x - Decimal(n) * twopi
    r2 = r * r
    sin_v = r
    cos_v = Decimal(1)
    t_s = r
    t_c = Decimal(1)
    k = 1
    while True:
        t_c = -t_c * r2 / Decimal((2 * k - 1) * (2 * k))
        t_s = -t_s * r2 / Decimal((2 * k) * (2 * k + 1))
        cos_v += t_c
        sin_v += t_s
        if abs(t_c) < Decimal("1e-109") and abs(t_s) < Decimal("1e-109"):
            break
        k += 1
    return sin_v, cos_v


def solve_beta_cs(m: int) -> Decimal:
    """Solve tanh(beta) + tan(beta) = 0 (dilated clamped-sliding, alpha = 1)."""
    b = Decimal("2.365020372431352013012024050417") if m == 1 else (Decimal(m) - Decimal("0.25")) * PI_DEC
    for _ in range(40):
        sh, ch = dec_sinh_cosh(b)
        si, co = dec_sin_cos(b)
        dk = (sh * co + ch * si) / (Decimal(2) * ch * co)
        b -= dk
        if abs(dk) < Decimal("1e-105"):
            break
    return b


def solve_gamma_cp(m: int) -> Decimal:
    """Solve tanh(gamma) - tan(gamma) = 0 (dilated clamped-pinned, alpha = 3)."""
    g = Decimal("3.926602312047919007916446109782") if m == 1 else (Decimal(m) + Decimal("0.25")) * PI_DEC
    for _ in range(40):
        sh, ch = dec_sinh_cosh(g)
        si, co = dec_sin_cos(g)
        dk = (sh * co - ch * si) / (-Decimal(2) * sh * si)
        g -= dk
        if abs(dk) < Decimal("1e-105"):
            break
    return g


def solve_kappa_cant(r: int) -> Tuple[Decimal, Decimal, Decimal]:
    """Solve cosh(kappa) cos(kappa) + 1 = 0 (positive-branch cantilever modes)."""
    if r == 1:
        k = Decimal("1.875104068711961166445308241078")
    elif r == 2:
        k = Decimal("4.694091132974174576436391778019")
    else:
        k = (Decimal(r) - Decimal("0.5")) * PI_DEC
    for _ in range(40):
        sh, ch = dec_sinh_cosh(k)
        si, co = dec_sin_cos(k)
        f = ch * co + Decimal(1)
        df = sh * co - ch * si
        dk = f / df
        k -= dk
        if abs(dk) < Decimal("1e-105"):
            break
    sh, ch = dec_sinh_cosh(k)
    si, co = dec_sin_cos(k)
    t_r = (sh - si) / (ch + co)
    w_r = (ch + co) / (sh * si)
    return k, t_r, w_r


def cdec_E(alpha: int, z: Tuple[Decimal, Decimal]) -> Tuple[Decimal, Decimal]:
    """Evaluate Krylov basis functions E_0..E_3 at complex argument z = a + i b."""
    a, b = z
    sh_a, ch_a = dec_sinh_cosh(a)
    si_a, co_a = dec_sin_cos(a)
    sh_b, ch_b = dec_sinh_cosh(b)
    si_b, co_b = dec_sin_cos(b)
    half = Decimal("0.5")
    ch = (ch_a * co_b, sh_a * si_b)
    sh = (sh_a * co_b, ch_a * si_b)
    co = (co_a * ch_b, -si_a * sh_b)
    si = (si_a * ch_b, co_a * sh_b)
    if alpha == 0:
        return (half * (ch[0] + co[0]), half * (ch[1] + co[1]))
    if alpha == 1:
        return (half * (sh[0] + si[0]), half * (sh[1] + si[1]))
    if alpha == 2:
        return (half * (ch[0] - co[0]), half * (ch[1] - co[1]))
    if alpha == 3:
        return (half * (sh[0] - si[0]), half * (sh[1] - si[1]))
    raise ValueError(alpha)


def eval_Xi_and_Upsilon_dec(kap: Decimal, w_r: Decimal, x: Decimal) -> Tuple[Decimal, Decimal]:
    """Evaluate closed-form positive-branch modes Xi_r(x) and Upsilon_r(x) = (1/4) Xi_r'(x)."""
    sh, ch = dec_sinh_cosh(kap)
    si, co = dec_sin_cos(kap)
    E0_k = Decimal("0.5") * (ch + co)
    c_u = (sh * si) / (Decimal(2) * E0_k)

    kw_kelvin = (kap * x, kap * (Decimal(1) - x))
    kw_rayleigh = (kap * (Decimal(2) * x - Decimal(1)), kap)

    im_E2_kelvin = cdec_E(2, kw_kelvin)[1]
    im_E0_rayleigh = cdec_E(0, kw_rayleigh)[1]
    xi_val = w_r * (c_u * im_E2_kelvin + im_E0_rayleigh)

    E1_kelvin = cdec_E(1, kw_kelvin)
    im_d_kelvin = kap * (E1_kelvin[1] - E1_kelvin[0])
    im_d_rayleigh = Decimal(2) * kap * cdec_E(3, kw_rayleigh)[1]
    upsilon_val = Decimal("0.25") * w_r * (c_u * im_d_kelvin + im_d_rayleigh)
    return xi_val, upsilon_val


def gauss_legendre_0_1_dec(n: int = 64) -> List[Tuple[Decimal, Decimal]]:
    nodes: List[Tuple[Decimal, Decimal]] = []
    m = (n + 1) // 2
    for i in range(1, m + 1):
        z = Decimal(str(math.cos(math.pi * (i - 0.25) / (n + 0.5))))
        for _ in range(30):
            p1 = Decimal(1)
            p2 = Decimal(0)
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = ((Decimal(2 * j - 1) * z * p2) - Decimal(j - 1) * p3) / Decimal(j)
            pp = Decimal(n) * (z * p1 - p2) / (z * z - Decimal(1))
            dz = p1 / pp
            z -= dz
            if abs(dz) < Decimal("1e-104"):
                break
        p1 = Decimal(1)
        p2 = Decimal(0)
        for j in range(1, n + 1):
            p3 = p2
            p2 = p1
            p1 = ((Decimal(2 * j - 1) * z * p2) - Decimal(j - 1) * p3) / Decimal(j)
        pp = Decimal(n) * (z * p1 - p2) / (z * z - Decimal(1))
        w = Decimal(2) / ((Decimal(1) - z * z) * pp * pp)
        x1 = Decimal("0.5") * (Decimal(1) - z)
        x2 = Decimal("0.5") * (Decimal(1) + z)
        w_half = Decimal("0.5") * w
        nodes.append((x1, w_half))
        if i != n + 1 - i:
            nodes.append((x2, w_half))
    nodes.sort(key=lambda t: t[0])
    return nodes


# ---------------------------------------------------------------------------
# Polynomial and Formal Series Arithmetic in Exact Fraction
# ---------------------------------------------------------------------------

def poly_trim(p: List[Fraction]) -> List[Fraction]:
    q = list(p)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q if q else [Fraction(0)]


def poly_add(p: List[Fraction], q: List[Fraction], a: Fraction = Fraction(1), b: Fraction = Fraction(1)) -> List[Fraction]:
    n = max(len(p), len(q))
    res = [Fraction(0)] * n
    for i in range(len(p)):
        res[i] += a * p[i]
    for i in range(len(q)):
        res[i] += b * q[i]
    return poly_trim(res)


def poly_ip(p: List[Fraction], q: List[Fraction]) -> Fraction:
    res = Fraction(0)
    for i, ci in enumerate(p):
        if ci == 0:
            continue
        for j, cj in enumerate(q):
            if cj == 0:
                continue
            res += ci * cj / Fraction(i + j + 1)
    return res


def series_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = min(len(a), len(b))
    res = [Fraction(0)] * n
    for i in range(n):
        s = Fraction(0)
        for j in range(i + 1):
            s += a[j] * b[i - j]
        res[i] = s
    return res


def series_inv(a: List[Fraction]) -> List[Fraction]:
    assert a[0] != 0
    n = len(a)
    inv = [Fraction(0)] * n
    inv[0] = Fraction(1) / a[0]
    for i in range(1, n):
        s = Fraction(0)
        for j in range(1, i + 1):
            s += a[j] * inv[i - j]
        inv[i] = -s / a[0]
    return inv


# Canonical quartet primal seeds \phi_0^{(\alpha)}(x) and pure-beam seeds \psi_0^{(\alpha)}(x) = (1/4)(\phi_0^{(\alpha)})'(x)
ETAS_FRAC: Dict[int, Fraction] = {
    0: Fraction(2, 3),
    1: Fraction(0),
    2: Fraction(-1, 3),
    3: Fraction(-2),
}
ETAS_DEC: Dict[int, Decimal] = {
    0: Decimal(2) / Decimal(3),
    1: Decimal(0),
    2: Decimal(-1) / Decimal(3),
    3: Decimal(-2),
}
PHI0_POLYS: Dict[int, List[Fraction]] = {
    0: [Fraction(0), Fraction(1)],
    1: [Fraction(0)],
    2: [Fraction(0), Fraction(1), Fraction(-1)],
    3: [Fraction(0), Fraction(7, 6), Fraction(-5, 2), Fraction(4, 3)],
}
PSI0_POLYS: Dict[int, List[Fraction]] = {
    0: [Fraction(1, 4)],
    1: [Fraction(0)],
    2: [Fraction(1, 4), Fraction(-1, 2)],
    3: [Fraction(7, 24), Fraction(-5, 4), Fraction(1)],
}
W0_STAR_POLY: List[Fraction] = [Fraction(1), Fraction(-6), Fraction(9), Fraction(-4)]
V0_STAR_POLY: List[Fraction] = [Fraction(0), Fraction(4), Fraction(-12), Fraction(12), Fraction(-4)]


def apply_G_Xi_C_poly(f_poly: List[Fraction]) -> List[Fraction]:
    """Exact polynomial action of G_Xi^{(C)} on Dom_C (alpha = 1): u^(4) = (6 I - 10 R) f."""
    d = len(f_poly) - 1
    one_minus_x = [Fraction(1), Fraction(-1)]
    p_pow = [[Fraction(1)]]
    for _ in range(d):
        prev = p_pow[-1]
        nxt = [Fraction(0)] * (len(prev) + 1)
        for i, c in enumerate(prev):
            nxt[i] += c * one_minus_x[0]
            nxt[i + 1] += c * one_minus_x[1]
        p_pow.append(nxt)
    tf = [Fraction(0)] * (d + 1)
    for k, c in enumerate(f_poly):
        if c == 0:
            continue
        for i in range(k + 1):
            tf[i] -= Fraction(10) * c * p_pow[k][i]
        tf[k] += Fraction(6) * c
    i4 = [Fraction(0)] * (d + 5)
    for m, c in enumerate(tf):
        if c != 0:
            i4[m + 4] = c / Fraction((m + 1) * (m + 2) * (m + 3) * (m + 4))
    v1 = sum(c for c in i4)
    d2_1 = sum(m * (m - 1) * c for m, c in enumerate(i4))
    d3_1 = sum(m * (m - 1) * (m - 2) * c for m, c in enumerate(i4))
    c3 = Fraction(-5, 12) * d3_1
    c2 = (Fraction(-5) * d2_1 - Fraction(30) * c3) / Fraction(16)
    c1 = -v1 - c2 - c3
    i4[1] += c1
    i4[2] += c2
    i4[3] += c3
    return poly_trim(i4)


def apply_G_Xi_C_star_poly(f_poly: List[Fraction]) -> List[Fraction]:
    """Exact polynomial action of the adjoint operator (G_Xi^{(C)})^* on Dom_1^*: v^(4) = (6 I - 10 R) f."""
    d = len(f_poly) - 1
    one_minus_s = [Fraction(1), Fraction(-1)]
    p_pow = [[Fraction(1)]]
    for _ in range(d):
        prev = p_pow[-1]
        nxt = [Fraction(0)] * (len(prev) + 1)
        for i, c in enumerate(prev):
            nxt[i] += c * one_minus_s[0]
            nxt[i + 1] += c * one_minus_s[1]
        p_pow.append(nxt)
    tf = [Fraction(0)] * (d + 1)
    for k, c in enumerate(f_poly):
        if c == 0:
            continue
        for i in range(k + 1):
            tf[i] -= Fraction(10) * c * p_pow[k][i]
        tf[k] += Fraction(6) * c
    v0 = [Fraction(0)] * (d + 5)
    for m, c in enumerate(tf):
        if c != 0:
            v0[m + 4] = c / Fraction((m + 1) * (m + 2) * (m + 3) * (m + 4))
    val_1 = sum(c for c in v0)
    d1_1 = sum(m * c for m, c in enumerate(v0))
    d2_1 = sum(m * (m - 1) * c for m, c in enumerate(v0))
    c3 = -d2_1 / Fraction(6)
    c1 = -d1_1 - Fraction(3) * c3
    c0 = -val_1 - c1 - c3
    v0[0] += c0
    v0[1] += c1
    v0[3] += c3
    return poly_trim(v0)


def apply_G_Xi_alpha_star_poly(alpha: int, f_poly: List[Fraction]) -> List[Fraction]:
    """
    Exact polynomial action of (G_Xi^{(alpha)})^* across the quartet alpha in {0, 1, 2, 3}
    via the Universal Quartet Star Factorization:
        (G_Xi^{(alpha)})^* f(s) = (G_Xi^{(C)})^* f(s) + eta_alpha <phi_0^{(alpha)}, f> w_0^*(s).
    """
    base = apply_G_Xi_C_star_poly(f_poly)
    if alpha == 1:
        return base
    ip = poly_ip(PHI0_POLYS[alpha], f_poly)
    return poly_add(base, W0_STAR_POLY, Fraction(1), ETAS_FRAC[alpha] * ip)


def integrate_from_y_to_1_times_4(q_poly: List[Fraction]) -> List[Fraction]:
    """Compute P(y) = 4 \\int_y^1 Q(s) ds in exact Fraction."""
    res = [Fraction(0)] * (len(q_poly) + 1)
    c0 = Fraction(0)
    for i, c in enumerate(q_poly):
        term = Fraction(4) * c / Fraction(i + 1)
        c0 += term
        res[i + 1] = -term
    res[0] = c0
    return poly_trim(res)


def gauss_pow_int(a: int, b: int, n: int) -> Tuple[int, int]:
    """Compute (a + b i)^n in exact Z[i]."""
    re_v, im_v = 1, 0
    ca, cb = a, b
    m = n
    while m > 0:
        if m & 1:
            re_v, im_v = re_v * ca - im_v * cb, re_v * cb + im_v * ca
        ca, cb = ca * ca - cb * cb, 2 * ca * cb
        m >>= 1
    return re_v, im_v


def closed_form_Q_dual_C(k: int) -> List[Fraction]:
    """
    Matrix-free Gaussian binomial formula for Q_{4k}^{(1)*}(s) = ((G_Xi^{(C)})^*)^{k-1} w_0^*(s)
    obtained by differentiating [z^m](e_1(z) \\int_0^s Q_tilde^{(1)*}(u; z) du).
    """
    e1 = [Fraction(1, math.factorial(4 * m + 1)) for m in range(k)]
    e1_inv = series_inv(e1)
    res = [Fraction(0)] * (4 * k)
    for m in range(k):
        am = e1_inv[k - 1 - m]
        deg = 4 * m + 4
        for r in range(1, deg + 1):
            denom = Fraction(math.factorial(r) * math.factorial(deg - r))
            term1 = Fraction(-3, 2) * Fraction((-2) ** r) / denom
            _, im_part = gauss_pow_int(1, 1, r)
            sign_v = -1 if (r & 1) else 1
            term2 = Fraction(-3 * sign_v * im_part) / denom
            res[r - 1] += am * Fraction(r) * (term1 + term2)
    return poly_trim(res)


def solve_primal_bvp_alpha_poly(alpha: int, f_poly: List[Fraction]) -> List[Fraction]:
    """
    Independent Hand 1 for Theorem 1: solve the direct 4th-order boundary-value problem
        L_Xi u = f_poly,   u(0) = 0,   B_j(u) = 0  (for all j != alpha)
    in exact Fraction by solving the 3x3 boundary linear system for (c_1, c_2, c_3),
    without referencing G_Xi^{(C)}, w_0^*, or eta_alpha.
    """
    d = len(f_poly) - 1
    one_minus_x = [Fraction(1), Fraction(-1)]
    p_pow = [[Fraction(1)]]
    for _ in range(d):
        prev = p_pow[-1]
        nxt = [Fraction(0)] * (len(prev) + 1)
        for i, c in enumerate(prev):
            nxt[i] += c * one_minus_x[0]
            nxt[i + 1] += c * one_minus_x[1]
        p_pow.append(nxt)
    tf = [Fraction(0)] * (d + 1)
    for k, c in enumerate(f_poly):
        if c == 0:
            continue
        for i in range(k + 1):
            tf[i] -= Fraction(10) * c * p_pow[k][i]
        tf[k] += Fraction(6) * c
    i4 = [Fraction(0)] * (d + 5)
    for m, c in enumerate(tf):
        if c != 0:
            i4[m + 4] = c / Fraction((m + 1) * (m + 2) * (m + 3) * (m + 4))

    def eval_B(j: int, p: List[Fraction]) -> Fraction:
        u0_1 = sum(c for c in p)
        u1_0 = p[1] if len(p) > 1 else Fraction(0)
        u1_1 = sum(m * c for m, c in enumerate(p))
        u2_0 = Fraction(2) * p[2] if len(p) > 2 else Fraction(0)
        u2_1 = sum(m * (m - 1) * c for m, c in enumerate(p))
        u3_0 = Fraction(6) * p[3] if len(p) > 3 else Fraction(0)
        u3_1 = sum(m * (m - 1) * (m - 2) * c for m, c in enumerate(p))
        if j == 0:
            return u0_1
        if j == 1:
            return u1_0 - Fraction(3) * u1_1
        if j == 2:
            return Fraction(3) * u2_0 + Fraction(5) * u2_1
        if j == 3:
            return Fraction(3) * u3_0 - Fraction(5) * u3_1
        raise ValueError(j)

    basis_cubics = [
        [Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ]
    active_j = [j for j in (0, 1, 2, 3) if j != alpha]
    mat = [[eval_B(j, b) for b in basis_cubics] + [-eval_B(j, i4)] for j in active_j]
    for col in range(3):
        piv = next(r for r in range(col, 3) if mat[r][col] != 0)
        mat[col], mat[piv] = mat[piv], mat[col]
        f = mat[col][col]
        mat[col] = [v / f for v in mat[col]]
        for r in range(3):
            if r != col and mat[r][col] != 0:
                ff = mat[r][col]
                mat[r] = [mat[r][c] - ff * mat[col][c] for c in range(4)]
    i4[1] += mat[0][3]
    i4[2] += mat[1][3]
    i4[3] += mat[2][3]
    return poly_trim(i4)


# ---------------------------------------------------------------------------
# Explicit Pointwise Green's Kernels and Quartet Dual Modes in 108-Digit Decimal
# ---------------------------------------------------------------------------

def G_Xi_C_dec(x: Decimal, s: Decimal) -> Decimal:
    """Closed-form piecewise-cubic Green's kernel G_Xi^{(C)}(x, s) on [0, 1]^2."""
    p1 = (x - s) ** 3 if x > s else Decimal(0)
    p2 = (Decimal(-5) / Decimal(3)) * ((x + s - Decimal(1)) ** 3) if (x + s > Decimal(1)) else Decimal(0)
    c1 = (
        Decimal(7) / Decimal(3)
        - Decimal(2) * s
        - Decimal(3) * (s ** 2)
        + (Decimal(8) / Decimal(3)) * (s ** 3)
    )
    c2 = Decimal(5) * (s - Decimal(1))
    c3 = Decimal(5) / Decimal(3)
    return p1 + p2 + c1 * x + c2 * (x ** 2) + c3 * (x ** 3)


def G_Upsilon_C_dec(x: Decimal, y: Decimal) -> Decimal:
    """Closed-form piecewise-cubic pure-beam dual Green's kernel G_Upsilon^{(C)}(x, y) on [0, 1]^2."""
    p1 = (x - y) ** 3 if x > y else Decimal(0)
    p2 = (Decimal(5) / Decimal(3)) * ((x + y - Decimal(1)) ** 3) if (x + y > Decimal(1)) else Decimal(0)
    q0 = (
        Decimal(1)
        - (Decimal(7) / Decimal(3)) * y
        + (y ** 2)
        + (y ** 3)
        - (Decimal(2) / Decimal(3)) * (y ** 4)
    )
    q1 = Decimal(-5) * ((y - Decimal(1)) ** 2) * x
    q2 = Decimal(5) * (Decimal(1) - y) * (x ** 2)
    q3 = (Decimal(-5) / Decimal(3)) * (x ** 3)
    return p1 + p2 + q0 + q1 + q2 + q3


def G_Xi_alpha_explicit_dec(alpha: int, x: Decimal, s: Decimal) -> Decimal:
    """Explicit piecewise-cubic Green's kernels G_Xi^{(alpha)}(x, s) for alpha in {0, 1, 2, 3}."""
    p1 = (x - s) ** 3 if x > s else Decimal(0)
    p2 = (Decimal(-5) / Decimal(3)) * ((x + s - Decimal(1)) ** 3) if (x + s > Decimal(1)) else Decimal(0)
    if alpha == 0:
        c1 = Decimal(3) * ((Decimal(1) - s) ** 2)
        c2 = Decimal(5) * (s - Decimal(1))
        c3 = Decimal(5) / Decimal(3)
        return p1 + p2 + c1 * x + c2 * (x ** 2) + c3 * (x ** 3)
    if alpha == 1:
        return G_Xi_C_dec(x, s)
    if alpha == 2:
        c1 = Decimal(2) - Decimal(6) * (s ** 2) + Decimal(4) * (s ** 3)
        c2 = (Decimal(-14) / Decimal(3)) + Decimal(3) * s + Decimal(3) * (s ** 2) - (Decimal(4) / Decimal(3)) * (s ** 3)
        c3 = Decimal(5) / Decimal(3)
        return p1 + p2 + c1 * x + c2 * (x ** 2) + c3 * (x ** 3)
    if alpha == 3:
        c1 = Decimal(12) * s - Decimal(24) * (s ** 2) + Decimal(12) * (s ** 3)
        c2 = Decimal(-25) * s + Decimal(45) * (s ** 2) - Decimal(20) * (s ** 3)
        c3 = (Decimal(-3) / Decimal(3)) + Decimal(16) * s - Decimal(24) * (s ** 2) + (Decimal(32) / Decimal(3)) * (s ** 3)
        return p1 + p2 + c1 * x + c2 * (x ** 2) + c3 * (x ** 3)
    raise ValueError(alpha)


def G_Upsilon_alpha_explicit_dec(alpha: int, x: Decimal, y: Decimal) -> Decimal:
    """Explicit piecewise-cubic pure-beam Green's kernels G_Upsilon^{(alpha)}(x, y)."""
    gc = G_Upsilon_C_dec(x, y)
    if alpha == 1:
        return gc
    v0 = Decimal(4) * y * ((Decimal(1) - y) ** 3)
    if alpha == 0:
        return gc - (Decimal(1) / Decimal(6)) * v0
    if alpha == 2:
        return gc + (Decimal(1) / Decimal(12)) * (Decimal(1) - Decimal(2) * x) * v0
    if alpha == 3:
        psi3 = (Decimal(7) - Decimal(30) * x + Decimal(24) * (x ** 2)) / Decimal(24)
        return gc + Decimal(2) * psi3 * v0
    raise ValueError(alpha)


def eval_quartet_neg_modes_dec(
    alpha: int, m: int, x: Decimal, root_val: Decimal | None = None
) -> Tuple[Decimal, Decimal, Decimal, Decimal, Decimal]:
    """
    Return unit-biorthogonal (Theta_m^{(alpha)}(x), Theta_m^{(alpha)*}(x),
    Omega_m^{(alpha)}(x), Omega_m^{(alpha)*}(x), |z_m^{(alpha)}|) for alpha in {0, 1, 2, 3}.
    """
    t2 = Decimal(2) * (x - Decimal("0.5"))
    if alpha == 0:
        mu = Decimal(2 * m - 1) * PI_DEC / Decimal(2)
        shm, chm = dec_sinh_cosh(mu)
        sh2, ch2 = dec_sinh_cosh(mu * t2)
        si2, co2 = dec_sin_cos(mu * t2)
        sgn = Decimal(1) if (m % 2 == 1) else Decimal(-1)
        norm0 = Decimal("-0.25") * (chm ** 2)
        th = ch2 + sgn * Decimal("0.5") * shm * co2 + sgn * (Decimal(2) * sh2 * co2 + ch2 * si2)
        th_star = (ch2 - sgn * shm * co2 + sgn * (sh2 * co2 - ch2 * si2)) / norm0
        om = Decimal("0.5") * mu * (
            sh2 - sgn * Decimal("0.5") * shm * si2 + sgn * (Decimal(3) * ch2 * co2 - sh2 * si2)
        )
        om_star = (Decimal(8) / (mu * (chm ** 2))) * (sh2 - sgn * shm * si2 + sgn * ch2 * co2)
        return th, th_star, om, om_star, Decimal(4) * (mu ** 4)

    if alpha == 1:
        assert root_val is not None
        bm = root_val
        shb, chb = dec_sinh_cosh(bm)
        sib, cob = dec_sin_cos(bm)
        sh2, ch2 = dec_sinh_cosh(bm * t2)
        si2, co2 = dec_sin_cos(bm * t2)
        n_m = -(chb ** 2) * (cob ** 4)
        th = sib * (cob * ch2 - chb * co2) + Decimal(2) * cob * (sh2 * co2 + ch2 * si2)
        th_star = (sib * (cob * ch2 + chb * co2) + cob * (sh2 * co2 - ch2 * si2)) / n_m
        th_prime = Decimal(2) * bm * sib * (cob * sh2 + chb * si2) + Decimal(8) * bm * cob * (ch2 * co2)
        om = Decimal("0.25") * th_prime

        def f_star(sh_v: Decimal, ch_v: Decimal, si_v: Decimal, co_v: Decimal) -> Decimal:
            return (sib * (cob * sh_v + chb * si_v) + cob * (ch_v * co_v)) / (Decimal(2) * bm * n_m)

        om_star = Decimal(4) * (f_star(shb, chb, sib, cob) - f_star(sh2, ch2, si2, co2))
        return th, th_star, om, om_star, Decimal(4) * (bm ** 4)

    if alpha == 2:
        mu = Decimal(m) * PI_DEC
        shm, chm = dec_sinh_cosh(mu)
        sh2, ch2 = dec_sinh_cosh(mu * t2)
        si2, co2 = dec_sin_cos(mu * t2)
        sgn = Decimal(-1) if (m % 2 == 1) else Decimal(1)
        norm2 = (-sgn) * Decimal("0.5") * shm * ((chm ** 2) + Decimal(1))
        th = chm * ch2 - sgn * (chm ** 2) * co2 - Decimal(2) * sgn * shm * ch2 * si2
        th_star = (shm * co2 - sh2 * co2 + ch2 * si2) / norm2
        om = Decimal("0.5") * mu * (
            chm * sh2 + sgn * (chm ** 2) * si2 - Decimal(2) * sgn * shm * (sh2 * si2 + ch2 * co2)
        )
        om_star = (Decimal(2) / (mu * norm2)) * (-sgn * chm - shm * si2 + ch2 * co2)
        return th, th_star, om, om_star, Decimal(4) * (mu ** 4)

    if alpha == 3:
        assert root_val is not None
        gm = root_val
        shg, chg = dec_sinh_cosh(gm)
        sig, cog = dec_sin_cos(gm)
        sh2, ch2 = dec_sinh_cosh(gm * t2)
        si2, co2 = dec_sin_cos(gm * t2)
        norm3 = (shg ** 2) * (cog ** 4)
        th = sig * (cog * ch2 - chg * co2) + Decimal(2) * cog * (sh2 * co2 - ch2 * si2)
        th_star = (sig * (cog * ch2 - chg * co2) + cog * (sh2 * co2 - ch2 * si2)) / norm3
        om = Decimal("0.5") * gm * (sig * (cog * sh2 + chg * si2) - Decimal(4) * cog * sh2 * si2)
        f_gm = (cog ** 2) * chg
        f_t = sig * (cog * sh2 - chg * si2) + cog * ch2 * co2
        om_star = (Decimal(2) / (gm * norm3)) * (f_gm - f_t)
        return th, th_star, om, om_star, Decimal(4) * (gm ** 4)

    raise ValueError(alpha)


def closed_form_c_m_star_dec(alpha: int, m: int, root_val: Decimal | None = None) -> Decimal:
    """
    Closed-form negative-branch projection c_m^{(alpha)*} = <Theta_m^{(alpha)}, w_0^*> = <Omega_m^{(alpha)}, v_0^*>
    from the Master Green-Lagrange Identity:
        c_m^{(alpha)*} = -3 B_alpha(Theta_m^{(alpha)}) / (2^{alpha+3} alpha! (mu_m^{(alpha)})^4).
    """
    if alpha == 0:
        mu = Decimal(2 * m - 1) * PI_DEC / Decimal(2)
        _, ch = dec_sinh_cosh(mu)
        return -Decimal(3) * ch / (Decimal(4) * (mu ** 4))
    if alpha == 1:
        assert root_val is not None
        bm = root_val
        _, ch = dec_sinh_cosh(bm)
        _, co = dec_sin_cos(bm)
        return Decimal(3) * (co ** 2) * ch / (bm ** 3)
    if alpha == 2:
        mu = Decimal(m) * PI_DEC
        _, ch = dec_sinh_cosh(mu)
        return -Decimal(3) * ((ch ** 2) + Decimal(1)) / (Decimal(2) * (mu ** 2))
    if alpha == 3:
        assert root_val is not None
        gm = root_val
        _, ch = dec_sinh_cosh(gm)
        _, co = dec_sin_cos(gm)
        return -(co ** 2) * ch / gm
    raise ValueError(alpha)


# ---------------------------------------------------------------------------
# Direct 4x4 Adjoint Cauchy-Residue Prover (Independent Second Hand)
# ---------------------------------------------------------------------------

def basis_jet(mu: Decimal, s: Decimal) -> Tuple[List[Decimal], List[Decimal], List[Decimal], List[Decimal]]:
    """Evaluate raw 4-element kernel basis of (L_Xi^* + 4 mu^4) w = 0 and its 1st..3rd derivatives."""
    t = Decimal(2) * mu * (s - Decimal("0.5"))
    sh, ch = dec_sinh_cosh(t)
    si, co = dec_sin_cos(t)
    s1 = Decimal(2) * mu
    s2 = s1 * s1
    s3 = s2 * s1
    v0 = [ch, co, sh * co, ch * si]
    v1 = [s1 * sh, -s1 * si, s1 * (ch * co - sh * si), s1 * (sh * si + ch * co)]
    v2 = [s2 * ch, -s2 * co, s2 * (-Decimal(2) * ch * si), s2 * (Decimal(2) * sh * co)]
    v3 = [
        s3 * sh,
        s3 * si,
        s3 * (-Decimal(2) * (sh * si + ch * co)),
        s3 * (Decimal(2) * (ch * co - sh * si)),
    ]
    return v0, v1, v2, v3


def adjoint_boundary_matrix(alpha: int, mu: Decimal) -> List[List[Decimal]]:
    """4x4 adjoint boundary matrix on ker(L_Xi^* + 4 mu^4) for Dom_alpha^*."""
    j0 = basis_jet(mu, Decimal(0))
    j1 = basis_jet(mu, Decimal(1))
    r0 = j1[0]
    r1 = j1[1]
    r2 = [j0[2][i] + Decimal(3) * j1[2][i] for i in range(4)]
    if alpha == 0:
        r3 = [Decimal(5) * j0[3][i] - Decimal(3) * j1[3][i] for i in range(4)]
    elif alpha == 1:
        r3 = j1[2]
    elif alpha == 2:
        r3 = j0[1]
    elif alpha == 3:
        r3 = j0[0]
    else:
        raise ValueError(alpha)
    return [r0, r1, r2, r3]


def basis_antideriv_from_y_to_1_times_4(mu: Decimal, y: Decimal) -> List[Decimal]:
    """Exact 4 \\int_y^1 f_i(s) ds for the raw 4-element kernel basis."""
    def F(s: Decimal) -> List[Decimal]:
        t = Decimal(2) * mu * (s - Decimal("0.5"))
        sh, ch = dec_sinh_cosh(t)
        si, co = dec_sin_cos(t)
        return [
            sh / (Decimal(2) * mu),
            si / (Decimal(2) * mu),
            (ch * co + sh * si) / (Decimal(4) * mu),
            (sh * si - ch * co) / (Decimal(4) * mu),
        ]
    f1 = F(Decimal(1))
    fy = F(y)
    return [Decimal(4) * (f1[i] - fy[i]) for i in range(4)]


def solve_4x4(a_mat: List[List[Decimal]], b_vec: List[Decimal]) -> List[Decimal]:
    m_aug = [row[:] + [b_vec[i]] for i, row in enumerate(a_mat)]
    for col in range(4):
        piv = max(range(col, 4), key=lambda r: abs(m_aug[r][col]))
        m_aug[col], m_aug[piv] = m_aug[piv], m_aug[col]
        f = m_aug[col][col]
        m_aug[col] = [v / f for v in m_aug[col]]
        for r in range(4):
            if r != col and m_aug[r][col] != 0:
                ff = m_aug[r][col]
                m_aug[r] = [m_aug[r][c] - ff * m_aug[col][c] for c in range(5)]
    return [m_aug[i][4] for i in range(4)]


# ---------------------------------------------------------------------------
# Main Verification Suite (Theorems 1, 2, and 3)
# ---------------------------------------------------------------------------

def verify_all() -> Dict[str, object]:
    gl64 = gauss_legendre_0_1_dec(64)

    # 1. THEOREM 1: Universal Quartet Star Factorization, Master Green-Lagrange Identity,
    #    and Transpose-Green Pole-Exchange Ladders
    # (a) Symbolic proof of Master Green-Lagrange Identity on 8-dim endpoint jet space
    #     [u(0), u(1), u'(0), u'(1), u''(0), u''(1), u'''(0), u'''(1)] with u(0) = 0:
    #     <L_Xi u, w_0^*> == (3/2) B_0(u) + (3/4) B_1(u) + (3/16) B_2(u) + (1/32) B_3(u).
    w0_jet = [
        Fraction(1), Fraction(0),
        Fraction(-6), Fraction(0),
        Fraction(18), Fraction(-6),
        Fraction(-24), Fraction(-24),
    ]
    M_ibp = [[Fraction(0)] * 8 for _ in range(8)]
    for j in range(4):
        u_ord = 3 - j
        sgn = (-1) ** j
        M_ibp[2 * u_ord + 1][2 * j + 1] += Fraction(-3 * sgn, 32)
        M_ibp[2 * u_ord + 1][2 * j + 0] += Fraction(-5, 32)
        M_ibp[2 * u_ord + 0][2 * j + 0] += Fraction(3 * sgn, 32)
        M_ibp[2 * u_ord + 0][2 * j + 1] += Fraction(5, 32)
    row_u = [sum(M_ibp[i][j] * w0_jet[j] for j in range(8)) for i in range(8)]
    expected_row_u = [
        Fraction(-3, 2), Fraction(3, 2),
        Fraction(3, 4), Fraction(-9, 4),
        Fraction(9, 16), Fraction(15, 16),
        Fraction(3, 32), Fraction(-5, 32),
    ]
    assert row_u == expected_row_u, f"Master Green-Lagrange identity failed: {row_u}"
    master_coeffs = [Fraction(3, (2 ** (a + 1)) * math.factorial(a)) for a in range(4)]
    assert master_coeffs == [Fraction(3, 2), Fraction(3, 4), Fraction(3, 16), Fraction(1, 32)]

    # (b) Two-handed verification of Universal Quartet Star Factorization:
    #     Hand 1 (Direct Primal 3x3 BVP Solver on Dom_alpha) vs Hand 2 (Rank-1 Star Formula around Dom_C)
    #     in exact Fraction on x^0 .. x^10, plus 108-digit pointwise check across [0, 1]^2.
    for n in range(11):
        xn = [Fraction(0)] * n + [Fraction(1)]
        gc_xn = apply_G_Xi_C_poly(xn)
        ip_w0 = poly_ip(xn, W0_STAR_POLY)
        for alpha in (0, 1, 2, 3):
            bvp_sol = solve_primal_bvp_alpha_poly(alpha, xn)
            star_sol = poly_add(gc_xn, PHI0_POLYS[alpha], Fraction(1), ETAS_FRAC[alpha] * ip_w0)
            assert bvp_sol == star_sol, f"Primal BVP vs Star formula mismatch at alpha={alpha}, n={n}"

    max_star_xi_diff: Dict[str, str] = {}
    max_star_ups_diff: Dict[str, str] = {}
    for alpha in (0, 1, 2, 3):
        err_xi = Decimal(0)
        err_ups = Decimal(0)
        for xs in ("0.17", "0.43", "0.81"):
            for ss in ("0.11", "0.52", "0.79"):
                x = Decimal(xs)
                s = Decimal(ss)
                w0 = ((Decimal(1) - s) ** 2) * (Decimal(1) - Decimal(4) * s)
                v0 = -Decimal(4) * s * ((Decimal(1) - s) ** 3)
                phi0_val = sum(
                    Decimal(c.numerator) / Decimal(c.denominator) * (x ** i)
                    for i, c in enumerate(PHI0_POLYS[alpha])
                )
                psi0_val = sum(
                    Decimal(c.numerator) / Decimal(c.denominator) * (x ** i)
                    for i, c in enumerate(PSI0_POLYS[alpha])
                )
                lhs_xi = G_Xi_alpha_explicit_dec(alpha, x, s) - G_Xi_C_dec(x, s)
                rhs_xi = ETAS_DEC[alpha] * phi0_val * w0
                lhs_ups = G_Upsilon_alpha_explicit_dec(alpha, x, s) - G_Upsilon_C_dec(x, s)
                rhs_ups = ETAS_DEC[alpha] * psi0_val * v0
                err_xi = max(err_xi, abs(lhs_xi - rhs_xi))
                err_ups = max(err_ups, abs(lhs_ups - rhs_ups))
        assert err_xi < Decimal("1e-104")
        assert err_ups < Decimal("1e-104")
        max_star_xi_diff[f"alpha={alpha}"] = f"{err_xi:.3e}"
        max_star_ups_diff[f"alpha={alpha}"] = f"{err_ups:.3e}"

    # (c) Exact Fraction verification of Sherman-Morrison pole-exchange convolution
    #     Q_{4k}^{(alpha)*}(s) == \sum_{j=1}^k ([z^{k-j}] e_1(z)/(alpha! e_alpha(z))) Q_{4j}^{(1)*}(s)
    #     for k = 1..6 (degree 24), plus matrix-free binomial formula for Q_{4j}^{(1)*}(s).
    K_max = 6
    e_series = {
        alpha: [Fraction(math.factorial(alpha), math.factorial(4 * m + alpha)) for m in range(K_max + 2)]
        for alpha in (0, 1, 2, 3)
    }
    pole_exchange_ratios = {
        alpha: series_mul(e_series[1][:K_max + 1], series_inv(e_series[alpha][:K_max + 1]))
        for alpha in (0, 1, 2, 3)
    }
    Q_C_closed = [closed_form_Q_dual_C(k) for k in range(1, K_max + 1)]
    Q_ladders: Dict[int, List[List[Fraction]]] = {a: [W0_STAR_POLY[:]] for a in (0, 1, 2, 3)}
    for a in (0, 1, 2, 3):
        for _ in range(1, K_max + 1):
            Q_ladders[a].append(apply_G_Xi_alpha_star_poly(a, Q_ladders[a][-1]))
    P_ladders: Dict[int, List[List[Fraction]]] = {
        a: [integrate_from_y_to_1_times_4(q) for q in Q_ladders[a]] for a in (0, 1, 2, 3)
    }
    for k in range(K_max):
        assert Q_ladders[1][k] == Q_C_closed[k], f"Closed-form Q_dual_C mismatch at k={k + 1}"
    for alpha in (0, 1, 2, 3):
        for k in range(K_max):
            conv_q = [Fraction(0)]
            conv_p = [Fraction(0)]
            for j in range(k + 1):
                wt = pole_exchange_ratios[alpha][k - j]
                conv_q = poly_add(conv_q, Q_C_closed[j], Fraction(1), wt)
                conv_p = poly_add(conv_p, P_ladders[1][j], Fraction(1), wt)
            assert conv_q == Q_ladders[alpha][k], f"Pole-exchange Q mismatch at alpha={alpha}, k={k + 1}"
            assert conv_p == P_ladders[alpha][k], f"Pole-exchange P mismatch at alpha={alpha}, k={k + 1}"

    # 2. THEOREM 2: Single-Branch Negative-Eigenvalue Mittag-Leffler Ladders &
    #    Two-Handed 4x4 Adjoint Cauchy-Residue Prover
    cant_modes = [solve_kappa_cant(r) for r in range(1, 5)]
    betas_90 = [solve_beta_cs(m) for m in range(1, 91)]
    gammas_90 = [solve_gamma_cp(m) for m in range(1, 91)]

    # (a) Positive-branch annihilation <Xi_r, Q_{4k}^{(alpha)*}> == <Upsilon_r, P_{4k}^{(alpha)*}> == 0
    #     and negative-branch closed-form projection c_m^{(alpha)*} = <Theta_m^{(alpha)}, w_0^*>
    pos_orth_errs: Dict[str, str] = {}
    proj_formula_errs: Dict[str, str] = {}
    w0_gl = [((Decimal(1) - z) ** 2) * (Decimal(1) - Decimal(4) * z) for z, _ in gl64]
    v0_gl = [-Decimal(4) * z * ((Decimal(1) - z) ** 3) for z, _ in gl64]

    for alpha in (0, 1, 2, 3):
        q12 = Q_ladders[alpha][2]
        p12 = P_ladders[alpha][2]
        q12_gl = [
            sum(Decimal(c.numerator) / Decimal(c.denominator) * (z ** i) for i, c in enumerate(q12))
            for z, _ in gl64
        ]
        p12_gl = [
            sum(Decimal(c.numerator) / Decimal(c.denominator) * (z ** i) for i, c in enumerate(p12))
            for z, _ in gl64
        ]
        max_po = Decimal(0)
        for kap, _, wr in cant_modes:
            xi_ups = [eval_Xi_and_Upsilon_dec(kap, wr, z) for z, _ in gl64]
            ip_xi = sum(gl64[i][1] * xi_ups[i][0] * q12_gl[i] for i in range(64))
            ip_ups = sum(gl64[i][1] * xi_ups[i][1] * p12_gl[i] for i in range(64))
            max_po = max(max_po, abs(ip_xi), abs(ip_ups))
        assert max_po < Decimal("1e-95"), f"Positive-branch annihilation error at alpha={alpha}: {max_po}"
        pos_orth_errs[f"alpha={alpha}"] = f"{max_po:.3e}"

        max_pf = Decimal(0)
        for m in range(1, 5):
            rv = betas_90[m - 1] if alpha == 1 else (gammas_90[m - 1] if alpha == 3 else None)
            modes_gl = [eval_quartet_neg_modes_dec(alpha, m, z, rv) for z, _ in gl64]
            ip_th = sum(gl64[i][1] * modes_gl[i][0] * w0_gl[i] for i in range(64))
            ip_om = sum(gl64[i][1] * modes_gl[i][2] * v0_gl[i] for i in range(64))
            cf_cm = closed_form_c_m_star_dec(alpha, m, rv)
            max_pf = max(max_pf, abs(ip_th - cf_cm), abs(ip_om - cf_cm))
        assert max_pf < Decimal("1e-84"), f"Closed-form c_m^({alpha})* error at alpha={alpha}: {max_pf}"
        proj_formula_errs[f"alpha={alpha}"] = f"{max_pf:.3e}"

    # (b) Single-branch negative-eigenvalue Mittag-Leffler convergence at k = 4 (Q_16^{(alpha)*}, P_16^{(alpha)*})
    ml_single_branch_errs: Dict[str, Dict[str, str]] = {}
    k_test = 4
    sgn_k = Decimal(-1) if ((k_test - 1) % 2 == 1) else Decimal(1)
    for alpha in (0, 1, 2, 3):
        q_poly = Q_ladders[alpha][k_test - 1]
        p_poly = P_ladders[alpha][k_test - 1]
        max_eq = Decimal(0)
        max_ep = Decimal(0)
        for ys in ("0.20", "0.375", "0.75"):
            y = Decimal(ys)
            ex_q = sum(Decimal(c.numerator) / Decimal(c.denominator) * (y ** i) for i, c in enumerate(q_poly))
            ex_p = sum(Decimal(c.numerator) / Decimal(c.denominator) * (y ** i) for i, c in enumerate(p_poly))
            ser_q = Decimal(0)
            ser_p = Decimal(0)
            for m in range(1, 91):
                rv = betas_90[m - 1] if alpha == 1 else (gammas_90[m - 1] if alpha == 3 else None)
                _, th_s, _, om_s, zm = eval_quartet_neg_modes_dec(alpha, m, y, rv)
                cm = closed_form_c_m_star_dec(alpha, m, rv)
                wt = sgn_k * cm / (zm ** (k_test - 1))
                ser_q += wt * th_s
                ser_p += wt * om_s
            max_eq = max(max_eq, abs(ex_q - ser_q))
            max_ep = max(max_ep, abs(ex_p - ser_p))
        assert max_eq < Decimal("1e-34"), f"Single-branch Q ML error at alpha={alpha}: {max_eq}"
        assert max_ep < Decimal("1e-34"), f"Single-branch P ML error at alpha={alpha}: {max_ep}"
        ml_single_branch_errs[f"alpha={alpha}"] = {
            "max_Q16_error_90modes": f"{max_eq:.3e}",
            "max_P16_error_90modes": f"{max_ep:.3e}",
        }

    # (c) Independent Second Hand: Direct 4x4 Adjoint Cauchy-Residue Prover on ker(L_Xi^* + 4 mu^4)
    rhs_vals = {0: Decimal(48), 1: Decimal(6), 2: Decimal(6), 3: Decimal(-1)}
    eps = Decimal("1e-30")
    adjoint_cauchy_q_diff: Dict[str, str] = {}
    adjoint_cauchy_p_diff: Dict[str, str] = {}
    for alpha in (0, 1, 2, 3):
        rhs = [Decimal(0), Decimal(0), Decimal(0), rhs_vals[alpha]]
        err_q = Decimal(0)
        err_p = Decimal(0)
        for m in (1, 2, 3):
            rv = betas_90[m - 1] if alpha == 1 else (gammas_90[m - 1] if alpha == 3 else None)
            mu_m = (
                (Decimal(2 * m - 1) * PI_DEC / Decimal(2))
                if alpha == 0
                else ((Decimal(m) * PI_DEC) if alpha == 2 else rv)
            )
            assert mu_m is not None
            cm = closed_form_c_m_star_dec(alpha, m, rv)
            c_p = solve_4x4(adjoint_boundary_matrix(alpha, mu_m * (Decimal(1) + eps)), rhs)
            c_m = solve_4x4(adjoint_boundary_matrix(alpha, mu_m * (Decimal(1) - eps)), rhs)
            for ys in ("0.23", "0.37", "0.71"):
                y = Decimal(ys)
                jp = basis_jet(mu_m * (Decimal(1) + eps), y)[0]
                jm = basis_jet(mu_m * (Decimal(1) - eps), y)[0]
                ap = basis_antideriv_from_y_to_1_times_4(mu_m * (Decimal(1) + eps), y)
                am = basis_antideriv_from_y_to_1_times_4(mu_m * (Decimal(1) - eps), y)
                res_q = Decimal(2) * eps * (sum(c_p[i] * jp[i] for i in range(4)) - sum(c_m[i] * jm[i] for i in range(4)))
                res_p = Decimal(2) * eps * (sum(c_p[i] * ap[i] for i in range(4)) - sum(c_m[i] * am[i] for i in range(4)))
                _, th_s, _, om_s, _ = eval_quartet_neg_modes_dec(alpha, m, y, rv)
                err_q = max(err_q, abs(res_q - cm * th_s))
                err_p = max(err_p, abs(res_p - cm * om_s))
        assert err_q < Decimal("1e-58"), f"Adjoint Cauchy Q mismatch at alpha={alpha}: {err_q}"
        assert err_p < Decimal("1e-58"), f"Adjoint Cauchy P mismatch at alpha={alpha}: {err_p}"
        adjoint_cauchy_q_diff[f"alpha={alpha}"] = f"{err_q:.3e}"
        adjoint_cauchy_p_diff[f"alpha={alpha}"] = f"{err_p:.3e}"

    # 3. THEOREM 3: Cyclic Quartet Derivative Ladder & Root-Free Polynomial Integral
    #    Formulas for All Four Negative-Branch Spectral Zetas (k = 1..7)
    zeta_exact: Dict[int, List[Fraction]] = {}
    for alpha in (0, 1, 2, 3):
        ea = e_series[alpha]
        ea_prime = [Fraction(m) * ea[m] for m in range(1, K_max + 2)]
        quot = series_mul(ea_prime, series_inv(ea[:K_max + 1]))
        zeta_exact[alpha] = [((-1) ** (k + 1)) * quot[k - 1] for k in range(1, K_max + 2)]

    phi_diff_3 = poly_add(PHI0_POLYS[3], PHI0_POLYS[2], Fraction(6), Fraction(-1))
    psi_diff_3 = poly_add(PSI0_POLYS[3], PSI0_POLYS[2], Fraction(6), Fraction(-1))
    phi_sum_0 = poly_add(PHI0_POLYS[0], PHI0_POLYS[3], Fraction(1), Fraction(3))
    psi_sum_0 = poly_add(PSI0_POLYS[0], PSI0_POLYS[3], Fraction(1), Fraction(3))

    cyclic_zeta_table: Dict[str, List[str]] = {f"alpha={a}": [] for a in (0, 1, 2, 3)}
    for k in range(1, K_max + 2):
        if k == 1:
            z0_q = Fraction(1, 24)
            z0_p = Fraction(1, 24)
        else:
            z0_q = Fraction((-1) ** (k - 1), 36) * poly_ip(phi_sum_0, Q_ladders[0][k - 2])
            z0_p = Fraction((-1) ** (k - 1), 36) * poly_ip(psi_sum_0, P_ladders[0][k - 2])
        z1_q = Fraction((-1) ** k, 6) * poly_ip(PHI0_POLYS[0], Q_ladders[1][k - 1])
        z1_p = Fraction((-1) ** k, 6) * poly_ip(PSI0_POLYS[0], P_ladders[1][k - 1])
        z2_q = Fraction((-1) ** k, 6) * poly_ip(PHI0_POLYS[2], Q_ladders[2][k - 1])
        z2_p = Fraction((-1) ** k, 6) * poly_ip(PSI0_POLYS[2], P_ladders[2][k - 1])
        z3_q = Fraction((-1) ** k, 4) * poly_ip(phi_diff_3, Q_ladders[3][k - 1])
        z3_p = Fraction((-1) ** k, 4) * poly_ip(psi_diff_3, P_ladders[3][k - 1])

        assert z0_q == z0_p == zeta_exact[0][k - 1]
        assert z1_q == z1_p == zeta_exact[1][k - 1]
        assert z2_q == z2_p == zeta_exact[2][k - 1]
        assert z3_q == z3_p == zeta_exact[3][k - 1]
        cyclic_zeta_table["alpha=0"].append(str(z0_q))
        cyclic_zeta_table["alpha=1"].append(str(z1_q))
        cyclic_zeta_table["alpha=2"].append(str(z2_q))
        cyclic_zeta_table["alpha=3"].append(str(z3_q))

    assert cyclic_zeta_table["alpha=0"][:3] == ["1/24", "17/10080", "691/9979200"]
    assert cyclic_zeta_table["alpha=1"][:3] == ["1/120", "29/453600", "331/648648000"]
    assert cyclic_zeta_table["alpha=2"][:3] == ["1/360", "1/151200", "691/40864824000"]
    assert cyclic_zeta_table["alpha=3"][:3] == ["1/840", "13/11642400", "37/31783752000"]

    return {
        "module": "quartet_transpose_annihilators_and_cyclic_zeta_ladders_2026_11_17.py",
        "revision": 106,
        "theorem_1_universal_star_and_pole_exchange": {
            "master_green_lagrange_coefficients": [str(c) for c in master_coeffs],
            "universal_star_eta_couplings": {f"alpha={a}": str(ETAS_FRAC[a]) for a in (0, 1, 2, 3)},
            "max_pointwise_star_G_Xi_diff": max_star_xi_diff,
            "max_pointwise_star_G_Upsilon_diff": max_star_ups_diff,
            "exact_pole_exchange_convolution_verified_up_to_k": K_max,
        },
        "theorem_2_single_branch_dual_ml_and_4x4_cauchy_second_hand": {
            "max_positive_branch_orth_error_Q12_P12": pos_orth_errs,
            "max_closed_form_c_m_star_projection_error": proj_formula_errs,
            "single_branch_ml_k4_90modes_errors": ml_single_branch_errs,
            "adjoint_4x4_cauchy_residue_max_Q_diff": adjoint_cauchy_q_diff,
            "adjoint_4x4_cauchy_residue_max_P_diff": adjoint_cauchy_p_diff,
        },
        "theorem_3_cyclic_root_free_spectral_zetas_k1_to_7": cyclic_zeta_table,
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    results = verify_all()
    out_path = Path(__file__).with_name("quartet_transpose_annihilators_and_cyclic_zeta_ladders_2026_11_17_results.json")
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, ensure_ascii=False))
