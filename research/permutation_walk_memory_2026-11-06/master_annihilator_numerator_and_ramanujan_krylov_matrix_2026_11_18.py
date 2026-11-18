#!/usr/bin/env python3
r"""
master_annihilator_numerator_and_ramanujan_krylov_matrix_2026_11_18.py
======================================================================
OMPU Stereo Pair — Lane B Lab Verification Module (Wednesday Morning, Rev 106 / 107)
Author: Den B (Lane B, instance jee-instance-524e408b5123473d95578e39c889f8a9)
Date:   2026-11-18

100% self-contained (`stdlib`-only: `decimal`, `fractions`, `json`, `math`, `pathlib`, `typing`;
0 local imports, 0 network/subprocess calls). Runnable via `python3 -I -B -W error`.

Closes:
  1. Jee A's `seq 249` open seam `[=~` (`quartet_transpose_annihilators_and_cyclic_zeta_ladders_2026_11_17.py`,
     sha256: 7db283f5...) on the 4x4 matrix of pairwise difference operators
     P_{\alpha,\beta} := (G_\Xi^{(\alpha)})^* - (G_\Xi^{(\beta)})^* and their higher-order spectral traces;
  2. The remaining 8 off-diagonal cells of the 4x4 Cross-Quartet Ratio Matrix
     R_{\beta,\alpha}(z) := (\beta! e_\beta(z)) / (\alpha! e_\alpha(z)) (\beta != \alpha), unifying
     Ramanujan's Notebook Ch. 14 Entry 25(vii) hyperbolic cotangent sums with clamped-pinned and
     clamped-sliding hyperbolic tangent/cotangent and squared tangent/cotangent Dirichlet series;
  3. The universal pole-free Entire Master Numerator N_Q(y; z) = \sum_{m>=0} U_{4m+4}(y) z^m
     and exact Q[y]-divisibility y(1-y)^3 | U_{4m+4}(y) across all four quartet domains.

Theorems proved & verified:
  - THEOREM 1 (Pole-Free Master Annihilator Numerator & Universal y(1-y)^3 Factorization):
      All four pure-beam dual annihilator generating functions share a single pole-free entire
      numerator N_Q(y; z) = \sum_{m>=0} U_{4m+4}(y) z^m:
          \tilde{Q}^{dual,(\alpha)}(y; z) := \sum_{k=1}^\infty Q_{4k}^{dual,(\alpha)}(y) z^{k-1}
                                          == \frac{N_Q(y; z)}{\alpha! e_\alpha(z)},
          U_{4m+4}(y) == \frac{3}{2 (4m+4)!} \Bigl[ 1 - (2y - 1)^{4m+4} - 2 Im[(y + i(1 - y))^{4m+4}] \Bigr].
      Every U_{4m+4}(y) (and hence every Q_{4k}^{dual,(\alpha)}(y)) is divisible by y(1-y)^3 in Q[y],
      annihilates all cantilever dual modes \Upsilon_r(y) (r >= 1), and at m = 1 yields the strictly
      positive all-unit-fraction polynomial
          U_8(y) == \frac{1}{840} y (1 - y)^3 \bigl[ (1 - y)^4 + 7 y^4 \bigr] > 0  on (0, 1).

  - THEOREM 2 (4x4 Pairwise Difference Idempotents \Pi_{\alpha,\beta}, Right-Zero Semigroup Law
      & Iterated Resolvent Trace Identity — Closure of Jee A's `seq 249` Seam `[=~`):
      With \tilde{\phi}_0^{(0)}(x) = -(2/3)x, \tilde{\phi}_0^{(1)}(x) = 0,
      \tilde{\phi}_0^{(2)}(x) = (1/3)(x - x^2), \tilde{\phi}_0^{(3)}(x) = (7x - 15x^2 + 8x^3)/3,
      every pairwise difference P_{\alpha,\beta} := (G_\Xi^{(\alpha)})^* - (G_\Xi^{(\beta)})^* is the
      rank-1 operator P_{\alpha,\beta} g = <\tilde{\phi}_0^{(\beta)} - \tilde{\phi}_0^{(\alpha)}, g> w_0^*
      with non-zero skew-symmetric trace (\forall \alpha != \beta)
          Tr(P_{\alpha,\beta}) == \zeta_{neg}^{(\beta)}(4) - \zeta_{neg}^{(\alpha)}(4),
          (\zeta_{neg}^{(0)}(4), \zeta_{neg}^{(1)}(4), \zeta_{neg}^{(2)}(4), \zeta_{neg}^{(3)}(4))
            = (1/24, 1/120, 1/360, 1/840).
      The normalized operators \Pi_{\alpha,\beta} := Tr(P_{\alpha,\beta})^{-1} P_{\alpha,\beta} (\alpha != \beta)
      are oblique idempotent projectors (\Pi_{\alpha,\beta}^2 == \Pi_{\alpha,\beta}) forming a right-zero
      semigroup \Pi_{\alpha,\beta} \Pi_{\mu,\nu} == \Pi_{\mu,\nu}, and their iterated resolvent traces
      generate the entire 4x4 Cross-Quartet Matrix:
          Tr\Bigl( P_{\alpha,\beta} \bigl((G_\Xi^{(\alpha)})^*\bigr)^{k-1} \Bigr)
            == [z^k]\left( \frac{\beta! e_\beta(z)}{\alpha! e_\alpha(z)} \right)  (\forall \alpha, \beta, k >= 1).

  - THEOREM 3 (Complete 12-Cell Cross-Quartet Ramanujan-Krylov Spectral Sum Table):
      Via s^\alpha e_\alpha(s^4) = E_\alpha(s) and E'_\alpha = E_{(\alpha-1) mod 4} along s_m = (1+i)\mu_m,
      all 12 off-diagonal entries [z^k](\beta! e_\beta / (\alpha! e_\alpha)) == \sum_{m>=1} W_{\beta,\alpha}(\mu_m) / (-4\mu_m^4)^k
      evaluate closed-form Dirichlet and hyperbolic tangent/cotangent series in 3 cyclic diagonals:
        * (\alpha - \beta) mod 4 = 1: pure spectral zetas \zeta_{neg}^{(\alpha)}(4k) (with Bernoulli prime 691);
        * (\alpha - \beta) mod 4 = 2: first-power hyperbolic tangent/cotangent sums, including
          Ramanujan's Entry 25(vii) \sum_{m>=1} \coth(m\pi)/(m\pi)^{4k-1} = (7/180, 19/56700, 1453/425675250, ...),
          dual odd-\pi/2 tangent sums \sum_{m>=1} \tanh((2m-1)\pi/2)/\mu_m^{4k+3} = (7/180, 181/28350, ...),
          clamped-pinned \sum_{m>=1} \coth\gamma_m / \gamma_m^{4k-1} = (3/140, 103/1455300, 97/331080750, ...),
          and clamped-sliding \sum_{m>=1} \tanh\beta_m / \beta_m^{4k+3} = (17/5040, 107/1091475, ...);
        * (\alpha - \beta) mod 4 = 3: even-shifted zetas & squared hyperbolic tangent/cotangent sums,
          including \sum_{m>=1} \coth^2\gamma_m / \gamma_m^{4k-2} = (17/140, 137/485100, 229/198648450, ...)
          and \sum_{m>=1} \tanh^2\beta_m / \beta_m^{4k+2} = (1/180, 41/226800, 2879/510810300, ...).
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

getcontext().prec = 112


# ---------------------------------------------------------------------------
# 0. Standalone Exact Polynomial & 105-Digit Decimal Transcendental Primitives
# ---------------------------------------------------------------------------

def poly_trim(p: List[Fraction]) -> List[Fraction]:
    out = p[:] if p else [Fraction(0)]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: List[Fraction], b: List[Fraction], sa: Fraction = Fraction(1), sb: Fraction = Fraction(1)) -> List[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i in range(len(a)):
        out[i] += sa * a[i]
    for i in range(len(b)):
        out[i] += sb * b[i]
    return poly_trim(out)


def poly_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    if not a or not b:
        return [Fraction(0)]
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca:
            for j, cb in enumerate(b):
                out[i + j] += ca * cb
    return poly_trim(out)


def poly_pow(p: List[Fraction], exp: int) -> List[Fraction]:
    res = [Fraction(1)]
    for _ in range(exp):
        res = poly_mul(res, p)
    return res


def poly_eval(p: List[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    for c in reversed(p):
        acc = acc * x + c
    return acc


def poly_deriv(p: List[Fraction], order: int = 1) -> List[Fraction]:
    cur = p[:]
    for _ in range(order):
        if len(cur) <= 1:
            return [Fraction(0)]
        cur = [cur[i] * i for i in range(1, len(cur))]
    return poly_trim(cur)


def poly_int(p: List[Fraction], order: int = 1) -> List[Fraction]:
    cur = p[:]
    for _ in range(order):
        cur = [Fraction(0)] + [c / Fraction(i + 1) for i, c in enumerate(cur)]
    return poly_trim(cur)


def poly_reflect(p: List[Fraction]) -> List[Fraction]:
    r"""Return (R p)(x) = p(1 - x) in Q[x]."""
    one_minus_x = [Fraction(1), Fraction(-1)]
    acc = [Fraction(0)]
    pw = [Fraction(1)]
    for c in p:
        if c:
            acc = poly_add(acc, pw, Fraction(1), c)
        pw = poly_mul(pw, one_minus_x)
    return acc


def poly_inner_product(a: List[Fraction], b: List[Fraction]) -> Fraction:
    prod = poly_mul(a, b)
    return sum(c / Fraction(i + 1) for i, c in enumerate(prod))


def poly_divmod(num: List[Fraction], den: List[Fraction]) -> Tuple[List[Fraction], List[Fraction]]:
    num_t = poly_trim(num)
    den_t = poly_trim(den)
    assert den_t[-1] != 0
    if len(num_t) < len(den_t):
        return [Fraction(0)], num_t
    rem = num_t[:]
    deg_d = len(den_t) - 1
    lead_d = den_t[-1]
    quot = [Fraction(0)] * (len(rem) - deg_d)
    while len(rem) - 1 >= deg_d and not (len(rem) == 1 and rem[0] == 0):
        deg_r = len(rem) - 1
        coeff = rem[-1] / lead_d
        shift = deg_r - deg_d
        quot[shift] = coeff
        for j, cd in enumerate(den_t):
            rem[shift + j] -= coeff * cd
        rem = poly_trim(rem)
    return poly_trim(quot), rem


def series_inv(a: List[Fraction]) -> List[Fraction]:
    assert a[0] != 0
    n = len(a)
    inv = [Fraction(1) / a[0]]
    for k in range(1, n):
        s = sum(a[j] * inv[k - j] for j in range(1, k + 1))
        inv.append(-s / a[0])
    return inv


def series_mul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    n = min(len(a), len(b))
    return [sum(a[j] * b[k - j] for j in range(k + 1)) for k in range(n)]


def compute_pi_dec() -> Decimal:
    """Machin's formula for pi to 105 digits."""
    def arctan_inv(m: int) -> Decimal:
        m_d = Decimal(m)
        m2 = m_d * m_d
        term = Decimal(1) / m_d
        total = term
        k = 1
        eps = Decimal("1e-108")
        while True:
            term = -term / m2
            add = term / Decimal(2 * k + 1)
            total += add
            if abs(add) < eps:
                break
            k += 1
        return total

    return Decimal(4) * (Decimal(4) * arctan_inv(5) - arctan_inv(239))


PI_DEC = compute_pi_dec()


def dec_sinh_cosh(x: Decimal) -> Tuple[Decimal, Decimal]:
    ex = x.exp()
    emx = (-x).exp()
    return Decimal("0.5") * (ex - emx), Decimal("0.5") * (ex + emx)


def dec_sin_cos(x: Decimal) -> Tuple[Decimal, Decimal]:
    two_pi = Decimal(2) * PI_DEC
    sgn = Decimal(-1) if x < 0 else Decimal(1)
    xr = abs(x) % two_pi
    if xr > PI_DEC:
        xr -= two_pi
    xr *= sgn
    x2 = xr * xr
    sin_v = xr
    cos_v = Decimal(1)
    t_sin = xr
    t_cos = Decimal(1)
    k = 1
    eps = Decimal("1e-108")
    while True:
        t_cos = -t_cos * x2 / Decimal((2 * k - 1) * (2 * k))
        t_sin = -t_sin * x2 / Decimal((2 * k) * (2 * k + 1))
        cos_v += t_cos
        sin_v += t_sin
        if abs(t_cos) < eps and abs(t_sin) < eps:
            break
        k += 1
    return sin_v, cos_v


def solve_kappa_105(r: int) -> Tuple[Decimal, Decimal]:
    """Solve cosh(kappa)*cos(kappa) + 1 = 0 for r >= 1 and return (kappa_r, tan(kappa_r/2))."""
    if r == 1:
        x = Decimal("1.8751040687119611664453082")
    elif r == 2:
        x = Decimal("4.6940911329741745764363918")
    else:
        x = (Decimal(r) - Decimal("0.5")) * PI_DEC
    for _ in range(18):
        sh, ch = dec_sinh_cosh(x)
        si, co = dec_sin_cos(x)
        # Divide by cosh(x) to keep O(1) scaling for large r:
        f = co + Decimal(1) / ch
        fp = -si + (sh / ch) * co - (sh / ch) * f + (sh / ch) * co  # wait: use exact cos + sech:
        # d/dx (cos x + sech x) = -sin x - sech x * tanh x
        fp_exact = -si - (sh / (ch * ch))
        dx = f / fp_exact
        x -= dx
        if abs(dx) < Decimal("1e-103"):
            break
    sh2, ch2 = dec_sinh_cosh(x / Decimal(2))
    si2, co2 = dec_sin_cos(x / Decimal(2))
    return x, si2 / co2


def solve_beta_cs(m: int) -> Decimal:
    """Solve tanh(beta) + tan(beta) = 0 (dilated clamped-sliding, alpha = 1)."""
    x = (Decimal(m) - Decimal("0.25")) * PI_DEC
    for _ in range(18):
        sh, ch = dec_sinh_cosh(x)
        si, co = dec_sin_cos(x)
        th = sh / ch
        f = th * co + si
        fp = (Decimal(1) - th * th) * co - th * si + co
        dx = f / fp
        x -= dx
        if abs(dx) < Decimal("1e-103"):
            break
    return x


def solve_gamma_cp(m: int) -> Decimal:
    """Solve tanh(gamma) - tan(gamma) = 0 (dilated clamped-pinned, alpha = 3)."""
    x = (Decimal(m) + Decimal("0.25")) * PI_DEC
    for _ in range(18):
        sh, ch = dec_sinh_cosh(x)
        si, co = dec_sin_cos(x)
        th = sh / ch
        f = th * co - si
        fp = (Decimal(1) - th * th) * co - th * si - co
        dx = f / fp
        x -= dx
        if abs(dx) < Decimal("1e-103"):
            break
    return x


def gauss_legendre_64() -> List[Tuple[Decimal, Decimal]]:
    """64-point Gauss-Legendre quadrature on [0, 1] in 105-digit Decimal."""
    n = 64
    nodes_weights: List[Tuple[Decimal, Decimal]] = []
    for i in range(1, n // 2 + 1):
        theta = PI_DEC * (Decimal(i) - Decimal("0.25")) / (Decimal(n) + Decimal("0.5"))
        _, z = dec_sin_cos(theta)
        for _ in range(16):
            p0 = Decimal(1)
            p1 = z
            for k in range(2, n + 1):
                p2 = (Decimal(2 * k - 1) * z * p1 - Decimal(k - 1) * p0) / Decimal(k)
                p0, p1 = p1, p2
            dp = Decimal(n) * (z * p1 - p0) / (z * z - Decimal(1))
            dz = p1 / dp
            z -= dz
            if abs(dz) < Decimal("1e-103"):
                break
        w = Decimal(2) / ((Decimal(1) - z * z) * dp * dp)
        nodes_weights.append((Decimal("0.5") * (Decimal(1) - z), Decimal("0.5") * w))
        nodes_weights.append((Decimal("0.5") * (Decimal(1) + z), Decimal("0.5") * w))
    nodes_weights.sort(key=lambda t: t[0])
    return nodes_weights


def eval_Upsilon_r_dec(kap: Decimal, t_r: Decimal, x: Decimal) -> Decimal:
    r"""Evaluate cantilever pure-beam dual mode \Upsilon_r(x) = (1/4) \Xi_r'(x)."""
    # Recall \hat{\psi}_r(x) = \cosh(\kappa x) - \cos(\kappa x) - \sigma_r (\sinh(\kappa x) - \sin(\kappa x)),
    # where \sigma_r = (\cosh\kappa + \cos\kappa)/(\sinh\kappa + \sin\kappa),
    # and \Upsilon_r(x) = (3/8) \hat{\psi}_r(x)^2 + (5/8) \hat{\psi}_r(1 - x)^2 ?
    # Wait: T v = u where u = (3/4) v - (5/4) R v ? Let's check:
    # From `gaussian_2plusi_quartet_and_cantilever_mode_duals_2026_11_16.py`:
    #   Xi_r(x) = (1 / (2 \kappa_r E_1(\kappa_r))) * [ ... ] and \Upsilon_r(x) = (1/4) \Xi_r'(x)!
    # Specifically, \Upsilon_r(x) = (\kappa_r / (4 E_1(\kappa_r))) * [ t_r (ch_{2x-1} + co_{2x-1}) ... ]?
    # Even simpler: since G_\Upsilon^{(C)}(x, y) = (1/4) \partial_x \int_y^1 ... wait:
    # Let's use the exact formula for \Xi_r(x) in y = x - 1/2:
    #   Xi_r(x) lies in Dom_0 \cap Dom_1 \cap Dom_2 \cap Dom_3 and satisfies L_\Xi \Xi_r = \kappa_r^4 \Xi_r!
    #   Wait: L_\Xi = -(1/32)(3I + 5R) D^4! On even functions (R = +I), L_\Xi = -(1/4) D^4;
    #   on odd functions (R = -I), L_\Xi = +(1/16) D^4!
    #   Wait: let's solve the 4-condition homogeneous BVP u(0)=u(1)=B_1(u)=B_2(u)=0 directly on the
    #   4-element eigenbasis of L_\Xi u = \kappa_r^4 u:
    #     even (-(1/4) u_e^(4) = \kappa^4 u_e => u_e^(4) = -4 \kappa^4 u_e = ((1+i)\kappa)^4 u_e):
    #       ch(k t) cos(k t), sh(k t) sin(k t)  with t = x - 1/2? Wait: ((1+i)\kappa)^4 = -4 \kappa^4!
    #     odd (+(1/16) u_o^(4) = \kappa^4 u_o => u_o^(4) = +16 \kappa^4 u_o = (2 \kappa)^4 u_o):
    #       sh(2 k t), sin(2 k t)  with t = x - 1/2!
    y = x - Decimal("0.5")
    ky = kap * y
    sh_k, ch_k = dec_sinh_cosh(ky)
    si_k, co_k = dec_sin_cos(ky)
    sh_2k, ch_2k = dec_sinh_cosh(Decimal(2) * ky)
    si_2k, co_2k = dec_sin_cos(Decimal(2) * ky)

    kh = kap * Decimal("0.5")
    sh_h, ch_h = dec_sinh_cosh(kh)
    si_h, co_h = dec_sin_cos(kh)
    sh_kap, ch_kap = dec_sinh_cosh(kap)
    si_kap, co_kap = dec_sin_cos(kap)

    # Even part E(y) with E(+-1/2) = 0 (since u(0)=u(1)=0 => E(1/2)=0 and O(1/2)=0!):
    #   f_e1(y) = ch(kh)*co(kh)*sh(ky)*si(ky) - sh(kh)*si(kh)*ch(ky)*co(ky)  => vanishes at y = +-1/2!
    # Odd part O(y) with O(+-1/2) = 0:
    #   f_o1(y) = sin(kap)*sh(2ky) - sinh(kap)*si(2ky)                      => vanishes at y = +-1/2!
    # Impose B_2(u) = 3 u''(0) + 5 u''(1) = 8 E''(1/2) + 2 O''(1/2) = 0!
    #   f_e1''(y) = 2 kap^2 [ ch(kh)*co(kh)*ch(ky)*co(ky) + sh(kh)*si(kh)*sh(ky)*si(ky) ]
    #   => f_e1''(1/2) = 2 kap^2 [ ch_h^2 * co_h^2 + sh_h^2 * si_h^2 ] = kap^2 (ch_kap + co_kap)/2 = 0 at cosh*cos = -1?
    #   WAIT A SECOND!! ch_h^2 co_h^2 + sh_h^2 si_h^2 = (1/4)[(ch_kap+1)(1+co_kap) + (ch_kap-1)(1-co_kap)] = (1/2)(ch_kap*co_kap + 1) == 0!!
    #   AND f_o1''(1/2) = 4 kap^2 (si_kap * sh_kap + sh_kap * si_kap) = 8 kap^2 sh_kap * si_kap!
    #   WAIT: since f_e1''(1/2) == 0, B_2(u) = 0 forces coeff of f_o1 to pair with the OTHER even/odd modes?
    #   No! u(0)=0 and u(1)=0 ONLY require E(1/2) - O(1/2) = 0 AND E(1/2) + O(1/2) = 0 => E(1/2) = 0 AND O(1/2) = 0!
    #   WAIT: there are TWO even basis functions {ch*co, sh*si}, so E(1/2)=0 leaves 1 even mode f_e1,
    #   and TWO odd basis functions {sh(2ky), si(2ky)}, so O(1/2)=0 leaves 1 odd mode f_o1!
    #   Then how do BOTH B_1(u)=0 and B_2(u)=0 hold?! Let's check B_1 and B_2 on {f_e1, f_o1}:
    #   u'(0) - 3 u'(1) = (E'(-1/2) + O'(-1/2)) - 3(E'(1/2) + O'(1/2)) = -4 E'(1/2) - 2 O'(1/2)!
    #   3 u''(0) + 5 u''(1) = 8 E''(1/2) + 2 O''(1/2)!
    #   Wait: f_o1''(1/2) = 4 kap^2 (si_kap * sh_kap - sh_kap * (-si_kap))? NO!
    #   (sh(2ky))'' = 4 kap^2 sh(2ky), (si(2ky))'' = -4 kap^2 si(2ky)!!
    #   SO f_o1''(1/2) = 4 kap^2 (si_kap * sh_kap - sh_kap * (-si_kap)) = 8 kap^2 sh_kap si_kap?
    #   Wait: if E''(1/2) = 0 and O''(1/2) != 0, then O must be 0?! Why? Because the odd eigenvalue is
    #   -(5-3)/32 = +(2/32) = +(1/16) OR -(3-5)/32 = +(1/16)? Let's check!
    #   L_Xi u = -(1/32)(3 u^(4) + 5 R u^(4)):
    #     On EVEN (R = +1): -(8/32) u^(4) = -(1/4) u^(4) = +kap^4 u  => u_e^(4) = -4 kap^4 u_e! (YES!)
    #     On ODD  (R = -1): -(-2/32) u^(4) = +(1/16) u^(4) = +kap^4 u => u_o^(4) = +16 kap^4 u_o!
    #   Wait: at kap_r, ch_kap * co_kap = -1, does sh_kap * si_kap vanish? NO!
    #   WAIT: at y = +1/2, 2*y = +1, so sh(2*kap*(1/2)) = sh(kap), si(2*kap*(1/2)) = si(kap).
    #   Why wasn't B_2(f_o1) = 0? Let's check E(y) and O(y) of \Xi_r(x)!
    #   Recall T v = (4/3 ...): \Upsilon_r = (1/4) \Xi_r', and v = \hat{\psi}_r^2 is NOT an eigenfunction of G_\Upsilon;
    #   rather \Xi_r(x) has the closed formula from `seq 244`:
    #     \Upsilon_r(x) = \frac{\kappa_r}{8 E_1(\kappa_r)} [ ... ]!
    #   Let's evaluate \Upsilon_r(x) directly from the exact closed formula in `seq 244`:
    #   Wait: let's solve the 3x3 system u(0)=0, u(1)=0, B_2(u)=0? No — why did E(1/2)=O(1/2)=0 fail?
    #   BECAUSE (R u)(x) = u(1 - x), so in y = x - 1/2, (R u)(y) = u(-y), AND (R u)''(y) = u''(-y),
    #   WAIT: 3 u''(0) + 5 u''(1) = 3 (E''(1/2) - O''(1/2)) + 5 (E''(1/2) + O''(1/2)) = 8 E''(1/2) + 2 O''(1/2)!!
    #   Wait: f_e1(y) = ch_h*co_h*sh_k*si_k - sh_h*si_h*ch_k*co_k:
    #   Let's differentiate sh(ky)*si(ky) TWICE:
    #     (sh si)' = k (ch si + sh co)
    #     (sh si)'' = 2 k^2 ch co!!
    #   And (ch co)'' = -2 k^2 sh si!!
    #   SO f_e1''(1/2) = 2 k^2 (ch_h^2 co_h^2 + sh_h^2 si_h^2) = k^2 [ (ch_kap+1)(co_kap+1) + (ch_kap-1)(1-co_kap) ] / 2
    #                  = k^2 (ch_kap + co_kap)  (NOT ch_kap*co_kap + 1!!)!!
    #   AHA!! (ch+1)(co+1) + (ch-1)(1-co) = (ch*co + ch + co + 1) + (ch - ch*co - 1 + co) = 2(ch + co) != 0!!
    fe_p = kap * (
        ch_h * co_h * (ch_k * si_k + sh_k * co_k)
        - sh_h * si_h * (sh_k * co_k - ch_k * si_k)
    )
    fo_p = Decimal(2) * kap * (si_kap * ch_2k - sh_kap * co_2k)
    # Ratio c_o / c_e from 8 E''(1/2) + 2 O''(1/2) = 0:
    #   E''(1/2) = kap^2 * (ch_kap + co_kap)
    #   O''(1/2) = 8 * kap^2 * sh_kap * si_kap
    #   => 8 * (ch_kap + co_kap) + 16 * c_ratio * sh_kap * si_kap = 0
    #   => c_ratio = -(ch_kap + co_kap) / (2 * sh_kap * si_kap)!
    c_ratio = -(ch_kap + co_kap) / (Decimal(2) * sh_kap * si_kap)
    return Decimal("0.25") * (fe_p + c_ratio * fo_p)


# ---------------------------------------------------------------------------
# 1. Operators L_\Xi, (G_\Xi^{(\alpha)})^* and Master Numerator U_{4m+4}(y)
# ---------------------------------------------------------------------------

W0_STAR_POLY = [Fraction(1), Fraction(-6), Fraction(9), Fraction(-4)]  # (1 - s)^2 (1 - 4s)

GAMMA_ALPHA = {
    0: Fraction(2, 3),
    1: Fraction(0),
    2: Fraction(-1, 3),
    3: Fraction(-2),
}

PHI0_SEEDS = {
    0: [Fraction(0), Fraction(1)],
    1: [Fraction(0)],
    2: [Fraction(0), Fraction(1), Fraction(-1)],
    3: [Fraction(0), Fraction(7, 6), Fraction(-5, 2), Fraction(4, 3)],
}

TILDE_PHI0 = {
    alpha: poly_add([Fraction(0)], PHI0_SEEDS[alpha], Fraction(1), -GAMMA_ALPHA[alpha])
    for alpha in range(4)
}


def apply_L_Xi_poly(u: List[Fraction]) -> List[Fraction]:
    u4 = poly_deriv(u, 4)
    return poly_add(u4, poly_reflect(u4), Fraction(-3, 32), Fraction(-5, 32))


def eval_B_functionals(u: List[Fraction]) -> Tuple[Fraction, List[Fraction]]:
    u0 = poly_eval(u, Fraction(0))
    u1 = poly_eval(u, Fraction(1))
    up0 = poly_eval(poly_deriv(u, 1), Fraction(0))
    up1 = poly_eval(poly_deriv(u, 1), Fraction(1))
    u20 = poly_eval(poly_deriv(u, 2), Fraction(0))
    u21 = poly_eval(poly_deriv(u, 2), Fraction(1))
    u30 = poly_eval(poly_deriv(u, 3), Fraction(0))
    u31 = poly_eval(poly_deriv(u, 3), Fraction(1))
    return u0, [u1, up0 - 3 * up1, 3 * u20 + 5 * u21, 3 * u30 - 5 * u31]


def apply_G_Xi_C_poly(g: List[Fraction]) -> List[Fraction]:
    rhs = poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    u0 = poly_int(rhs, 4)
    v1 = poly_eval(u0, Fraction(1))
    d2_1 = poly_eval(poly_deriv(u0, 2), Fraction(1))
    d3_1 = poly_eval(poly_deriv(u0, 3), Fraction(1))
    c3 = Fraction(-5, 12) * d3_1
    c2 = (Fraction(-5) * d2_1 - Fraction(30) * c3) / Fraction(16)
    c1 = -v1 - c2 - c3
    return poly_add(u0, [Fraction(0), c1, c2, c3])


def apply_G_Xi_C_adj_poly(g: List[Fraction]) -> List[Fraction]:
    rhs = poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    w0 = poly_int(rhs, 4)
    d2_1 = poly_eval(poly_deriv(w0, 2), Fraction(1))
    d1_1 = poly_eval(poly_deriv(w0, 1), Fraction(1))
    v_1 = poly_eval(w0, Fraction(1))
    c3 = -d2_1 / Fraction(6)
    c1 = -d1_1 - Fraction(3) * c3
    c0 = -v_1 - c1 - c3
    return poly_add(w0, [c0, c1, Fraction(0), c3])


def apply_G_Xi_alpha_adj_poly(alpha: int, g: List[Fraction]) -> List[Fraction]:
    base = apply_G_Xi_C_adj_poly(g)
    if alpha == 1:
        return base
    ip = poly_inner_product(PHI0_SEEDS[alpha], g)
    return poly_add(base, W0_STAR_POLY, Fraction(1), GAMMA_ALPHA[alpha] * ip)


def build_U_master_poly(m: int) -> List[Fraction]:
    r"""
    Closed-form pole-free polynomial U_{4m+4}(y):
      U_{4m+4}(y) = \frac{3}{2 (4m+4)!} [ 1 - (2y - 1)^{4m+4} - 2 Im[(y + i(1 - y))^{4m+4}] ].
    """
    n_deg = 4 * m + 4
    p_2y_m1 = poly_pow([Fraction(-1), Fraction(2)], n_deg)
    term1 = poly_add([Fraction(1)], p_2y_m1, Fraction(1), Fraction(-1))
    im_w = [Fraction(0)]
    for r in range(1, n_deg, 2):
        sgn = Fraction((-1) ** ((r - 1) // 2))
        binom = Fraction(math.comb(n_deg, r))
        ynr = [Fraction(0)] * (n_deg - r) + [Fraction(1)]
        omyr = poly_pow([Fraction(1), Fraction(-1)], r)
        im_w = poly_add(im_w, poly_mul(ynr, omyr), Fraction(1), sgn * binom)
    comb_p = poly_add(term1, im_w, Fraction(1), Fraction(-2))
    scale = Fraction(3, 2 * math.factorial(n_deg))
    return poly_trim([c * scale for c in comb_p])


# ---------------------------------------------------------------------------
# 2. Theorem 1 Verification
# ---------------------------------------------------------------------------

def verify_theorem_1(gl64: List[Tuple[Decimal, Decimal]]) -> Dict[str, object]:
    # (a) Verify 5-term Green-Lagrange law on all monomials x^0 .. x^11
    tau = [Fraction(3, 2), Fraction(3, 4), Fraction(3, 16), Fraction(1, 32)]
    for deg in range(12):
        uk = [Fraction(0)] * deg + [Fraction(1)]
        lhs = poly_inner_product(apply_L_Xi_poly(uk), W0_STAR_POLY)
        u0, bs = eval_B_functionals(uk)
        rhs = Fraction(-3, 2) * u0 + sum(tau[a] * bs[a] for a in range(4))
        assert lhs == rhs, f"5-term Green-Lagrange failed at deg={deg}: {lhs} vs {rhs}"

    # Verify exact adjointness <G_C x^i, s^j> == <x^i, G_C^* s^j>
    for i in range(6):
        xi = [Fraction(0)] * i + [Fraction(1)]
        g_xi = apply_G_Xi_C_poly(xi)
        for j in range(6):
            sj = [Fraction(0)] * j + [Fraction(1)]
            assert poly_inner_product(g_xi, sj) == poly_inner_product(xi, apply_G_Xi_C_adj_poly(sj))

    # (b) Verify pole-free Master Numerator across all alpha=0..3, k=1..6 (up to degree 24)
    #     and universal exact divisibility y(1-y)^3 | U_{4m+4}(y)
    u_list = [build_U_master_poly(m) for m in range(6)]
    q4_base = [Fraction(0), Fraction(1), Fraction(-3), Fraction(3), Fraction(-1)]  # y(1-y)^3

    for m_idx, u_p in enumerate(u_list):
        quot, rem = poly_divmod(u_p, q4_base)
        assert rem == [Fraction(0)], f"y(1-y)^3 divisibility failed at m={m_idx}: rem={rem}"
        if m_idx == 1:
            # Verify U_8(y) == (1/840) y(1-y)^3 [(1-y)^4 + 7 y^4]
            one_m_y_4 = poly_pow([Fraction(1), Fraction(-1)], 4)
            expected_q1 = poly_add(one_m_y_4, [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(7)],
                                   Fraction(1, 840), Fraction(1, 840))
            assert quot == expected_q1, f"U_8 quotient mismatch: {quot} vs {expected_q1}"

    for alpha in range(4):
        p_ladder = [W0_STAR_POLY]
        for _ in range(5):
            p_ladder.append(apply_G_Xi_alpha_adj_poly(alpha, p_ladder[-1]))
        q_ladder = [poly_int(p, 1) for p in p_ladder]
        for k in range(1, 7):
            assert poly_eval(q_ladder[k - 1], Fraction(0)) == 0
            assert poly_eval(q_ladder[k - 1], Fraction(1)) == 0
            _, q_rem = poly_divmod(q_ladder[k - 1], q4_base)
            assert q_rem == [Fraction(0)]
            conv = [Fraction(0)]
            for j in range(k):
                ea_j = Fraction(math.factorial(alpha), math.factorial(4 * j + alpha))
                conv = poly_add(conv, q_ladder[k - 1 - j], Fraction(1), ea_j)
            assert conv == u_list[k - 1], f"Master numerator mismatch at alpha={alpha}, k={k}"

    # (c) Verify <U_{4m+4}, Upsilon_r> == 0 in 105-digit quadrature for m=0..3, r=1..5
    modes_5 = [solve_kappa_105(r) for r in range(1, 6)]
    max_orth_err = Decimal(0)
    for m_idx in range(4):
        u_dec_coeffs = [Decimal(c.numerator) / Decimal(c.denominator) for c in u_list[m_idx]]
        u_vals = []
        for xq, _ in gl64:
            acc = Decimal(0)
            for c_d in reversed(u_dec_coeffs):
                acc = acc * xq + c_d
            u_vals.append(acc)
        for kap, t_r in modes_5:
            ip = sum(gl64[n][1] * u_vals[n] * eval_Upsilon_r_dec(kap, t_r, gl64[n][0]) for n in range(64))
            max_orth_err = max(max_orth_err, abs(ip))
    assert max_orth_err < Decimal("1e-95"), f"Cantilever dual annihilation error too large: {max_orth_err}"

    return {
        "status": "PASS",
        "U_8_unit_fractions": [str(c) for c in u_list[1]],
        "U_8_quotient_by_y_1_minus_y_cubed": "(1/840)*((1-y)^4 + 7*y^4)",
        "master_numerator_verified_alpha_0_to_3_up_to_k": 6,
        "max_U_annihilation_error_on_Upsilon_r": f"{max_orth_err:.3e}",
    }


# ---------------------------------------------------------------------------
# 3. Theorem 2 Verification: Pairwise Difference Idempotents & Trace Matrix
# ---------------------------------------------------------------------------

def apply_P_diff_poly(alpha: int, beta: int, g: List[Fraction]) -> List[Fraction]:
    r"""P_{\alpha,\beta} g = ((G_\Xi^{(\alpha)})^* - (G_\Xi^{(\beta)})^*) g."""
    diff_seed = poly_add(TILDE_PHI0[beta], TILDE_PHI0[alpha], Fraction(1), Fraction(-1))
    ip = poly_inner_product(diff_seed, g)
    return poly_add([Fraction(0)], W0_STAR_POLY, Fraction(1), ip)


def verify_theorem_2() -> Dict[str, object]:
    zeta4 = [Fraction(math.factorial(a), math.factorial(4 + a)) for a in range(4)]
    assert zeta4 == [Fraction(1, 24), Fraction(1, 120), Fraction(1, 360), Fraction(1, 840)]

    # (a) Verify P_{\alpha,\beta} g == (G_\Xi^{(\alpha)})^* g - (G_\Xi^{(\beta)})^* g on x^0..x^8,
    #     exact trace matrix Tr(P_{\alpha,\beta}) == \zeta_{neg}^{(\beta)}(4) - \zeta_{neg}^{(\alpha)}(4),
    #     idempotency \Pi_{\alpha,\beta}^2 == \Pi_{\alpha,\beta}, and right-zero semigroup law
    #     \Pi_{\alpha,\beta} \Pi_{\mu,\nu} == \Pi_{\mu,\nu}!
    trace_matrix: Dict[str, str] = {}
    pairs = [(a, b) for a in range(4) for b in range(4) if a != b]
    for a, b in pairs:
        tr_ab = poly_inner_product(
            poly_add(TILDE_PHI0[b], TILDE_PHI0[a], Fraction(1), Fraction(-1)), W0_STAR_POLY
        )
        assert tr_ab == zeta4[b] - zeta4[a]
        assert tr_ab != 0
        trace_matrix[f"({a},{b})"] = str(tr_ab)

        for deg in range(9):
            gd = [Fraction(0)] * deg + [Fraction(1)]
            lhs = apply_P_diff_poly(a, b, gd)
            rhs = poly_add(apply_G_Xi_alpha_adj_poly(a, gd), apply_G_Xi_alpha_adj_poly(b, gd),
                           Fraction(1), Fraction(-1))
            assert lhs == rhs
            pi_gd = [c / tr_ab for c in lhs]
            pi2_gd = [c / tr_ab for c in apply_P_diff_poly(a, b, pi_gd)]
            assert poly_trim(pi2_gd) == poly_trim(pi_gd)

    # Check right-zero semigroup law \Pi_{a,b} \Pi_{m,n} == \Pi_{m,n} on test polynomial 1 + 2x + 3x^2 + 5x^5:
    g_test = [Fraction(1), Fraction(2), Fraction(3), Fraction(0), Fraction(0), Fraction(5)]
    for a, b in pairs:
        tr_ab = zeta4[b] - zeta4[a]
        for m, n in pairs:
            tr_mn = zeta4[n] - zeta4[m]
            pi_mn = [c / tr_mn for c in apply_P_diff_poly(m, n, g_test)]
            pi_ab_mn = [c / tr_ab for c in apply_P_diff_poly(a, b, pi_mn)]
            assert poly_trim(pi_ab_mn) == poly_trim(pi_mn)

    # (b) Verify iterated resolvent trace identity:
    #     Tr(P_{\alpha,\beta} ((G_\Xi^{(\alpha)})^*)^{k-1}) == [z^k](\beta! e_\beta(z) / (\alpha! e_\alpha(z)))
    #     for ALL 16 pairs (\alpha, \beta) and k = 1..6!
    k_max = 6
    eb_series = [
        [Fraction(math.factorial(b), math.factorial(4 * k + b)) for k in range(k_max + 1)]
        for b in range(4)
    ]
    for alpha in range(4):
        p_ladder = [W0_STAR_POLY]
        for _ in range(k_max - 1):
            p_ladder.append(apply_G_Xi_alpha_adj_poly(alpha, p_ladder[-1]))
        inv_ea = series_inv(eb_series[alpha])
        for beta in range(4):
            ratio_ba = series_mul(eb_series[beta], inv_ea)
            diff_seed = poly_add(TILDE_PHI0[beta], TILDE_PHI0[alpha], Fraction(1), Fraction(-1))
            for k in range(1, k_max + 1):
                # Since P_{\alpha,\beta} A = |w_0^*><diff_seed| A, its trace is <diff_seed, A w_0^*>!
                tr_iter = poly_inner_product(diff_seed, p_ladder[k - 1])
                assert tr_iter == ratio_ba[k], f"Trace mismatch at ({alpha},{beta}), k={k}: {tr_iter} vs {ratio_ba[k]}"

    return {
        "status": "PASS",
        "skew_symmetric_traces_Tr_P_ab": trace_matrix,
        "right_zero_semigroup_and_idempotency_verified_pairs": len(pairs),
        "iterated_trace_quartet_ratio_verified_k_1_to_6": True,
    }


# ---------------------------------------------------------------------------
# 4. Theorem 3 Verification: 12-Cell Ramanujan-Krylov Spectral Sum Matrix
# ---------------------------------------------------------------------------

def wronskian_weight_dec(beta: int, alpha: int, mu: Decimal) -> Decimal:
    sh, ch = dec_sinh_cosh(mu)
    th = sh / ch
    cth = ch / sh
    if alpha == 0:
        return {1: Decimal(2) / (mu ** 2), 2: Decimal(4) * th / (mu ** 3), 3: Decimal(6) / (mu ** 4)}[beta]
    if alpha == 1:
        return {0: Decimal(-4), 2: Decimal(4) * (th ** 2) / (mu ** 2), 3: Decimal(12) * th / (mu ** 3)}[beta]
    if alpha == 2:
        return {0: Decimal(-4) * mu * cth, 1: Decimal(-2), 3: Decimal(6) / (mu ** 2)}[beta]
    if alpha == 3:
        return {
            0: Decimal(-4) * (mu ** 2) * (cth ** 2) / Decimal(3),
            1: Decimal(-4) * mu * cth / Decimal(3),
            2: Decimal(-4) / Decimal(3),
        }[beta]
    raise ValueError((beta, alpha))


def verify_theorem_3() -> Dict[str, object]:
    mus_0 = [Decimal(2 * m - 1) * PI_DEC / Decimal(2) for m in range(1, 151)]
    betas_1 = [solve_beta_cs(m) for m in range(1, 91)]
    mus_2 = [Decimal(m) * PI_DEC for m in range(1, 151)]
    gammas_3 = [solve_gamma_cp(m) for m in range(1, 91)]
    roots_map = {0: mus_0, 1: betas_1, 2: mus_2, 3: gammas_3}

    eb = [[Fraction(math.factorial(b), math.factorial(4 * k + b)) for k in range(5)] for b in range(4)]

    cell_k3_errors: Dict[str, str] = {}
    for alpha in range(4):
        inv_ea = series_inv(eb[alpha])
        for beta in range(4):
            if beta == alpha:
                continue
            r_ba = series_mul(eb[beta], inv_ea)
            target_f = r_ba[3]
            target_d = Decimal(target_f.numerator) / Decimal(target_f.denominator)
            s_val = sum(
                wronskian_weight_dec(beta, alpha, mu) / ((Decimal(-4) * (mu ** 4)) ** 3)
                for mu in roots_map[alpha]
            )
            err = abs(s_val - target_d)
            assert err < Decimal("1e-24"), f"12-cell sum failed at ({beta},{alpha}): err={err}"
            cell_k3_errors[f"(beta={beta},alpha={alpha})"] = f"{err:.3e}"

    # Extract closed-form rational values of the flagship Ramanujan-Krylov hyperbolic series (k = 1..4):
    r_02 = series_mul(eb[0], series_inv(eb[2]))  # Ramanujan Entry 25(vii): sum coth(m*pi)/(m*pi)^{4k-1}
    r_20 = series_mul(eb[2], series_inv(eb[0]))  # Dual odd-pi/2: sum tanh((2m-1)pi/2)/mu_m^{4k+3}
    r_13 = series_mul(eb[1], series_inv(eb[3]))  # Clamped-pinned: sum coth(gamma_m)/gamma_m^{4k-1}
    r_03 = series_mul(eb[0], series_inv(eb[3]))  # Clamped-pinned sq: sum coth^2(gamma_m)/gamma_m^{4k-2}
    r_31 = series_mul(eb[3], series_inv(eb[1]))  # Clamped-sliding: sum tanh(beta_m)/beta_m^{4k+3}
    r_21 = series_mul(eb[2], series_inv(eb[1]))  # Clamped-sliding sq: sum tanh^2(beta_m)/beta_m^{4k+2}

    ramanujan_coth_mpi = [str((Fraction(-4) ** (k - 1)) * r_02[k]) for k in range(1, 5)]
    dual_tanh_halfpi = [str((Fraction(-4) ** k) / Fraction(4) * r_20[k]) for k in range(1, 5)]
    cp_coth_gamma = [str(Fraction(3) * (Fraction(-4) ** (k - 1)) * r_13[k]) for k in range(1, 5)]
    cp_coth2_gamma = [str(Fraction(-3, 4) * (Fraction(-4) ** k) * r_03[k]) for k in range(1, 5)]
    cs_tanh_beta = [str((Fraction(-4) ** k) / Fraction(12) * r_31[k]) for k in range(1, 5)]
    cs_tanh2_beta = [str((Fraction(-4) ** k) / Fraction(4) * r_21[k]) for k in range(1, 5)]

    assert ramanujan_coth_mpi[:3] == ["7/180", "19/56700", "1453/425675250"]
    assert cp_coth_gamma[:3] == ["3/140", "103/1455300", "97/331080750"]
    assert cp_coth2_gamma[:3] == ["17/140", "137/485100", "229/198648450"]

    return {
        "status": "PASS",
        "all_12_off_diagonal_k3_errors": cell_k3_errors,
        "ramanujan_coth_mpi_4k_minus_1_k1_to_4": ramanujan_coth_mpi,
        "dual_odd_halfpi_tanh_4k_plus_3_k1_to_4": dual_tanh_halfpi,
        "clamped_pinned_coth_gamma_4k_minus_1_k1_to_4": cp_coth_gamma,
        "clamped_pinned_coth2_gamma_4k_minus_2_k1_to_4": cp_coth2_gamma,
        "clamped_sliding_tanh_beta_4k_plus_3_k1_to_4": cs_tanh_beta,
        "clamped_sliding_tanh2_beta_4k_plus_2_k1_to_4": cs_tanh2_beta,
    }


def G_Xi_alpha_dec(alpha: int, x: Decimal, s: Decimal) -> Decimal:
    r"""Exact piecewise-cubic kernel G_\Xi^{(\alpha)}(x, s) across [0, 1]^2."""
    t1 = ((x - s) ** 3) if x > s else Decimal(0)
    t2 = ((x + s - Decimal(1)) ** 3) if (x + s > Decimal(1)) else Decimal(0)
    gc = (
        t1
        - (Decimal(5) / Decimal(3)) * t2
        + (Decimal(7) / Decimal(3) - Decimal(2) * s - Decimal(3) * s * s + (Decimal(8) / Decimal(3)) * (s ** 3)) * x
        + Decimal(5) * (s - Decimal(1)) * (x ** 2)
        + (Decimal(5) / Decimal(3)) * (x ** 3)
    )
    if alpha == 1:
        return gc
    w0 = ((Decimal(1) - s) ** 2) * (Decimal(1) - Decimal(4) * s)
    if alpha == 0:
        return gc + (Decimal(2) / Decimal(3)) * x * w0
    if alpha == 2:
        return gc - (Decimal(1) / Decimal(3)) * (x - x * x) * w0
    if alpha == 3:
        phi3 = (Decimal(7) * x - Decimal(15) * (x ** 2) + Decimal(8) * (x ** 3)) / Decimal(6)
        return gc - Decimal(2) * phi3 * w0
    raise ValueError(alpha)


def verify_theorem_4_mixed_traces(gl64: List[Tuple[Decimal, Decimal]]) -> Dict[str, object]:
    r"""
    Theorem 4 (Closure of Jee A's `seq 250` Open Seam `[=~`):
      1. Joint spectral projection of mixed products G_\Xi^{(\alpha)} G_\Xi^{(\beta)}:
         Since G_\Xi^{(\alpha)} \Xi_r = \kappa_r^{-4} \Xi_r and <w_0^*, \Xi_r> = 0, the positive
         cantilever branch is a joint invariant eigenspace of ALL G_\Xi^{(\alpha)} G_\Xi^{(\beta)}
         with eigenvalues \kappa_r^{-8} (contributing \zeta_{cant}(8) = 11/1680), while the
         negative-branch contribution collapses via G_\Xi^{(\beta)} = G_\Xi^{(\alpha)} - \Delta_{\alpha,\beta}
         and Theorem 2(b) (k=2) to the manifestly symmetric closed form:
             Tr(G_\Xi^{(\alpha)} G_\Xi^{(\beta)})
               == \frac{11}{1680} + \frac{\alpha!}{(\alpha+4)!}\frac{\beta!}{(\beta+4)!}
                  - \frac{\alpha!}{(\alpha+8)!} - \frac{\beta!}{(\beta+8)!}.
      2. Verified by 3 independent hands across all 6 unordered pairs (\alpha < \beta) + 4 diagonals:
         Hand 1 (closed formula), Hand 2 (both operator orderings (\alpha,\beta) and (\beta,\alpha)),
         Hand 3 (112-digit piecewise Gauss-Legendre 2D quadrature across the X-light-cone).
    """
    c1 = [Fraction(math.factorial(a), math.factorial(4 + a)) for a in range(4)]
    c2 = [Fraction(math.factorial(a), math.factorial(8 + a)) for a in range(4)]
    tr_diag_sq = [Fraction(11, 1680) + (c1[a] ** 2 - 2 * c2[a]) for a in range(4)]

    # Use first 12 nodes of gl64? Better: build exact 10-pt Gauss-Legendre on [0, 1] for piecewise exactness on deg <= 6!
    gl16 = gl64[:0]
    # Note: gl64 on each subinterval has 64 points (exact for polynomials up to degree 127!), use 12-pt GL:
    n_sub = 12
    gl12: List[Tuple[Decimal, Decimal]] = []
    for i in range(1, n_sub // 2 + 1):
        theta = PI_DEC * (Decimal(i) - Decimal("0.25")) / (Decimal(n_sub) + Decimal("0.5"))
        _, z = dec_sin_cos(theta)
        for _ in range(16):
            p0, p1 = Decimal(1), z
            for k in range(2, n_sub + 1):
                p0, p1 = p1, (Decimal(2 * k - 1) * z * p1 - Decimal(k - 1) * p0) / Decimal(k)
            dp = Decimal(n_sub) * (z * p1 - p0) / (z * z - Decimal(1))
            dz = p1 / dp
            z -= dz
            if abs(dz) < Decimal("1e-108"):
                break
        w = Decimal(2) / ((Decimal(1) - z * z) * dp * dp)
        gl12.append((Decimal("0.5") * (Decimal(1) - z), Decimal("0.5") * w))
        gl12.append((Decimal("0.5") * (Decimal(1) + z), Decimal("0.5") * w))

    p7_map = {a: apply_G_Xi_alpha_adj_poly(a, W0_STAR_POLY) for a in range(4)}

    unordered_6: Dict[str, str] = {}
    max_quad_err = Decimal(0)

    for a in range(4):
        for b in range(a, 4):
            # Hand 1: closed symmetric formula
            closed_ab = Fraction(11, 1680) + c1[a] * c1[b] - c2[a] - c2[b]
            # Hand 2: both non-symmetric operator orderings
            diff_ba = poly_add(TILDE_PHI0[b], TILDE_PHI0[a], Fraction(1), Fraction(-1))
            diff_ab = poly_add(TILDE_PHI0[a], TILDE_PHI0[b], Fraction(1), Fraction(-1))
            op_ab = tr_diag_sq[a] - poly_inner_product(diff_ba, p7_map[a])
            op_ba = tr_diag_sq[b] - poly_inner_product(diff_ab, p7_map[b])
            assert closed_ab == op_ab == op_ba, f"Symmetry/formula mismatch at ({a},{b})"

            # Hand 3: 2D piecewise quadrature across x in (0, 1/2) U (1/2, 1) and s split at x, 1-x
            quad_2d = Decimal(0)
            for x_lo, x_hi in ((Decimal(0), Decimal("0.5")), (Decimal("0.5"), Decimal(1))):
                dx_len = x_hi - x_lo
                for ux, wx in gl12:
                    x = x_lo + dx_len * ux
                    cuts = sorted([Decimal(0), x, Decimal(1) - x, Decimal(1)])
                    inner = Decimal(0)
                    for idx_c in range(3):
                        s_lo, s_hi = cuts[idx_c], cuts[idx_c + 1]
                        ds_len = s_hi - s_lo
                        for us, ws in gl12:
                            s = s_lo + ds_len * us
                            inner += ds_len * ws * G_Xi_alpha_dec(a, x, s) * G_Xi_alpha_dec(b, s, x)
                    quad_2d += dx_len * wx * inner

            target_dec = Decimal(closed_ab.numerator) / Decimal(closed_ab.denominator)
            max_quad_err = max(max_quad_err, abs(quad_2d - target_dec))
            if a < b:
                unordered_6[f"Tr(G_{a} G_{b})"] = str(closed_ab)

    assert max_quad_err < Decimal("1e-106"), f"2D mixed trace quadrature error too large: {max_quad_err}"
    return {
        "status": "PASS",
        "mixed_traces_6_unordered_pairs": unordered_6,
        "max_2d_piecewise_quadrature_error": f"{max_quad_err:.3e}",
    }


def main() -> None:
    print("=" * 78)
    print("LANE B LAB: MASTER ANNIHILATOR NUMERATOR & 12-CELL RAMANUJAN-KRYLOV MATRIX")
    print("=" * 78)

    gl64 = gauss_legendre_64()
    res1 = verify_theorem_1(gl64)
    print(
        f"[PASS] Theorem 1: Pole-free U_{{4m+4}}(y) & y(1-y)^3 factorization up to deg 24 "
        f"(Upsilon orth={res1['max_U_annihilation_error_on_Upsilon_r']})"
    )

    res2 = verify_theorem_2()
    print(
        f"[PASS] Theorem 2: 12 oblique difference idempotents Pi_{{a,b}}, right-zero semigroup "
        f"& iterated trace identity k=1..6"
    )

    res3 = verify_theorem_3()
    print(
        f"[PASS] Theorem 3: Complete 12-cell Ramanujan-Krylov spectral sum table "
        f"(Entry 25(vii)={res3['ramanujan_coth_mpi_4k_minus_1_k1_to_4'][:3]}, "
        f"cp_coth={res3['clamped_pinned_coth_gamma_4k_minus_1_k1_to_4'][:3]})"
    )

    res4 = verify_theorem_4_mixed_traces(gl64)
    print(
        f"[PASS] Theorem 4: Symmetric mixed traces Tr(G_a G_b) across all 6 pairs "
        f"({res4['mixed_traces_6_unordered_pairs']}, 2D quad err={res4['max_2d_piecewise_quadrature_error']})"
    )

    summary = {
        "module": "master_annihilator_numerator_and_ramanujan_krylov_matrix_2026_11_18.py",
        "lane": "b",
        "instance_id": "jee-instance-524e408b5123473d95578e39c889f8a9",
        "theorem_1": res1,
        "theorem_2": res2,
        "theorem_3": res3,
        "theorem_4": res4,
        "verdict": "ALL_CHECKS_PASSED",
    }
    out_path = Path(__file__).with_name(
        "master_annihilator_numerator_and_ramanujan_krylov_matrix_2026_11_18_results.json"
    )
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
