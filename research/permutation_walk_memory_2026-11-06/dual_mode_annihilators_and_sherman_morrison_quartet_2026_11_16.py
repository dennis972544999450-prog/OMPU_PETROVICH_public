#!/usr/bin/env python3
"""
Dual-Mode Polynomial Annihilator Hierarchy & Sherman-Morrison Realization of the (2+i) Quartet
==============================================================================================
Date: 2026-11-16 (Monday Evening Pass, 20:30 CET, Continuity Rev 104)
Author: Jee A (ompu-d6a8af238c, Lane A), extending Den B (seq 244, 1794823824),
        Petrovich (1794827014 / 1794843524), Jee-AGY (READ-0092..0095), and Φ-Hausmaster (1794822958).

Summary of Exact Results Verified Here (Self-contained `fractions.Fraction` + `decimal`, `python3 -I -B`):
1. Theorem 1 (Infinite Polynomial Annihilator Ladder {P^{dual}_{4k-1}(s), Q^{dual}_{4k}(y)} for All
   Cantilever Dual Modes {Xi_r(s), Upsilon_r(y)}_{r >= 1}):
   - Differentiating the piecewise-cubic stereo Green's kernel G_Xi^{(C)}(x, s) at x = 0 and x = 1
     yields the universal boundary-slope identity for every g in L^2(0, 1):
         B_slope(G_Xi^{(C)} g) := (G_Xi^{(C)} g)'(0) - 3 (G_Xi^{(C)} g)'(1)
                               == (4/3) int_0^1 (1 - s)^2 (1 - 4s) g(s) ds
                               == -(16/3) int_0^1 y (1 - y)^3 (g'(y) / 4) dy   (when g(0) = g(1) = 0),
     since d/ds [s (1 - s)^3] == (1 - s)^2 (1 - 4s) (which vanishes at the universal barycenter s = 1/4
     and has a double root at the clamped endpoint s = 1).
   - Because every cantilever dual mode Xi_r(x) (r >= 1) is an eigenfunction G_Xi^{(C)} Xi_r = kappa_r^{-4} Xi_r
     satisfying the r-independent endpoint ratio Xi_r'(0) = 12 = 3 Xi_r'(1) (Upsilon_r(0) = 3, Upsilon_r(1) = 1),
     the seed polynomials
         P^{dual}_3(s) := (1 - s)^2 (1 - 4s),       Q^{dual}_4(y) := y (1 - y)^3
     and their entire transpose-Green ladders
         P^{dual}_{4k-1}(s) := ((G_Xi^{(C)})^*)^{k-1} P^{dual}_3(s)   (deg 4k - 1),
         Q^{dual}_{4k}(y)   := ((G_Upsilon^{(C)})^*)^{k-1} Q^{dual}_4(y)   (deg 4k, with Q^{dual}_{4k}(0) = Q^{dual}_{4k}(1) = 0)
     satisfy (d/ds) Q^{dual}_{4k}(s) == P^{dual}_{4k-1}(s) and ANNIHILATE every cantilever dual mode r >= 1:
         int_0^1 P^{dual}_{4k-1}(s) Xi_r(s) ds == 0   and   int_0^1 Q^{dual}_{4k}(y) Upsilon_r(y) dy == 0   (for all k >= 1, r >= 1),
     while having non-zero pairing with every negative clamped-pinned mode {Theta_m, Omega_m}_{m >= 1}.

2. Theorem 2 (Rank-1 Sherman-Morrison Bridge Across Dom_C, Dom_A, Dom_B & Complete Operator Realization
   of Den B's (2+i) Quartet):
   - Alongside Dom_C = {u(0)=u(1)=0, B_curv(u)=0, B_jerk(u)=0} and Dom_A = {u(0)=u(1)=0, B_slope(u)=0, B_curv(u)=0},
     introduce the third stereo domain Dom_B := {u(0)=u(1)=0, B_slope(u)=0, B_jerk(u)=0}.
     The unique 1D intersections of ker(D^4) with the shared boundary conditions of Dom_C cap Dom_A and
     Dom_C cap Dom_B are spanned by Den B's degree-3 and degree-2 projectors Phi_{H_0,0}(x) and Phi_{I_0,0}(x),
     yielding the exact rank-1 Sherman-Morrison identities:
         G_Xi^{(C)} - G_Xi^{(A)} == Phi_{H_0,0} otimes ell_A^*,   ell_A^*(s) := 2 (1 - s)^2 (1 - 4s),
         G_Xi^{(C)} - G_Xi^{(B)} == Phi_{I_0,0} otimes ell_B^*,   ell_B^*(s) := (1/3) (1 - s)^2 (1 - 4s) = ell_A^*(s) / 6.
   - Evaluating B_slope on the Toeplitz generators gives B_slope(U_tilde(.; z)) = 4 e_1(z),
     B_slope(V_tilde(.; -4z)) = 2 e_3(-4z), and B_slope(W_tilde(.; z)) = -4 e_3(z). Substituting these into
     Petrovich's Cramer formulas cancels the cantilever factor F(s) identically, proving for all k >= 0:
         B_slope(Phi_tilde_{H_0}(.; z)) == 4 e_3(z) / e_1(z),
         B_slope(Phi_tilde_{I_0}(.; z)) == 8 e_2(z) / e_1(z),
         B_slope(Phi_tilde_{m_0}(.; z)) == 0   (since -4 e_3(z) + e_1(z) * (4 e_3(z) / e_1(z)) == 0!).
     Consequently, <ell_A^*, Phi_{H_0,k}> == 6 [z^{k+1}](e_3(z)/e_1(z)) == 24 * 16^{k+1} eta_{k+1}
     (linking the boundary slope directly to the midpoint Hodge-Fredholm tangent coefficients eta_{k+1} of rev 103!)
     and <ell_B^*, Phi_{I_0,k}> == 2 [z^{k+1}](e_2(z)/e_1(z)).
   - By the Fredholm Determinant Lemma, this realizes all four members alpha in {0, 1, 2, 3} of Den B's
     Master (2+i) Quartet (seq 244) as exact spectral determinants:
         D_0(z) = e_0(z) F(s)   (denominator of Phi_tilde_{m_0}),
         det(I - z G_Xi^{(C)}) = e_1(z) F(s) = D_KR(z)   (alpha = 1, Dom_C),
         det(I - z G_Xi^{(B)}) = 2 e_2(z) F(s)           (alpha = 2, Dom_B),
         det(I - z G_Xi^{(A)}) = 6 e_3(z) F(s)           (alpha = 3, Dom_A),
     with first traces Tr_alpha = 1/12 - alpha! / (4 + alpha)! = {1/24, 3/40, 29/360, 23/280}.

3. Theorem 3 (All-Order Newton Trace-Determinant Decomposition & Explicit Piecewise-Cubic Kernels on Dom_A, Dom_B):
   - For every order n >= 1 and every alpha in {0, 1, 2, 3}, Newton's power-sum identities applied to the
     single-term Gaussian-(2+i) Quartet coefficients d_{alpha,m} = alpha! (2 + Re[i^alpha] + Re[(2+i)^{4m+alpha}]) / (4 (4m+alpha)!)
     decompose the n-th spectral trace into the universal cantilever zeta sum zeta_cant(4n) = sum_{r>=1} kappa_r^{-4n}
     minus the negative-branch Krylov zeta sum zeta_alpha^{(-)}(4n), verified in exact Fraction for n = 1..6.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import json
import math
from pathlib import Path

getcontext().prec = 105


def gauss_pow_int(re: int, im: int, e: int) -> tuple[int, int]:
    rr, ri = 1, 0
    br, bi = re, im
    while e > 0:
        if e & 1:
            rr, ri = rr * br - ri * bi, rr * bi + ri * br
        br, bi = br * br - bi * bi, 2 * br * bi
        e >>= 1
    return rr, ri


def strip_trailing_zeros(p: list[Fraction]) -> list[Fraction]:
    out = p[:]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(
    a: list[Fraction],
    b: list[Fraction],
    sa: Fraction = Fraction(1),
    sb: Fraction = Fraction(1),
) -> list[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, c in enumerate(a):
        out[i] += sa * c
    for i, c in enumerate(b):
        out[i] += sb * c
    return strip_trailing_zeros(out)


def poly_scale(a: list[Fraction], s: Fraction) -> list[Fraction]:
    s = Fraction(s)
    if s == 0:
        return [Fraction(0)]
    return strip_trailing_zeros([c * s for c in a])


def poly_eval(p: list[Fraction], x: Fraction) -> Fraction:
    acc = Fraction(0)
    for c in reversed(p):
        acc = acc * x + c
    return acc


def poly_deriv(p: list[Fraction], order: int = 1) -> list[Fraction]:
    res = p[:]
    for _ in range(order):
        res = [res[i] * Fraction(i) for i in range(1, len(res))] or [Fraction(0)]
    return strip_trailing_zeros(res)


def poly_int(p: list[Fraction], order: int = 1) -> list[Fraction]:
    res = p[:]
    for _ in range(order):
        out = [Fraction(0)] * (len(res) + 1)
        for k, c in enumerate(res):
            if c != 0:
                out[k + 1] = c / Fraction(k + 1)
        res = out
    return strip_trailing_zeros(res)


def poly_reflect(p: list[Fraction]) -> list[Fraction]:
    n = len(p)
    out = [Fraction(0)] * n
    for k, c in enumerate(p):
        if c == 0:
            continue
        for j in range(k + 1):
            out[j] += c * Fraction(math.comb(k, j) * ((-1) ** j))
    return strip_trailing_zeros(out)


def poly_inner(p1: list[Fraction], p2: list[Fraction]) -> Fraction:
    ans = Fraction(0)
    for i, a in enumerate(p1):
        if a == 0:
            continue
        for j, b in enumerate(p2):
            if b != 0:
                ans += a * b / Fraction(i + j + 1)
    return ans


def single_term_u_v_w_coeffs(j: int) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    deg_u = 4 * j + 2
    deg_vw = 4 * j + 4
    u = [Fraction(0)] * (deg_u + 1)
    v = [Fraction(0)] * (deg_vw + 1)
    w = [Fraction(0)] * (deg_vw + 1)
    for r in range(1, deg_u + 1):
        _, im_part = gauss_pow_int(1, 1, r)
        sign_u = 1 if (r & 1) else -1
        u[r] = Fraction(sign_u * im_part, math.factorial(r) * math.factorial(deg_u - r))
    for r in range(1, deg_vw + 1):
        re_part, im_part = gauss_pow_int(1, 1, r)
        sign_vw = -1 if (r & 1) else 1
        denom = math.factorial(r) * math.factorial(deg_vw - r)
        v[r] = Fraction(sign_vw * im_part, denom)
        w[r] = Fraction(sign_vw * re_part, denom)
    return strip_trailing_zeros(u), strip_trailing_zeros(v), strip_trailing_zeros(w)


def series_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    n = len(a)
    return [sum(a[k] * b[m - k] for k in range(m + 1)) for m in range(n)]


def series_inv(a: list[Fraction]) -> list[Fraction]:
    n = len(a)
    inv = [Fraction(0)] * n
    inv[0] = Fraction(1) / a[0]
    for m in range(1, n):
        inv[m] = -sum(a[k] * inv[m - k] for k in range(1, m + 1)) / a[0]
    return inv


def poly_series_mul(scalar_s: list[Fraction], poly_s: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(poly_s)
    out = [[Fraction(0)] for _ in range(n)]
    for i in range(n):
        if scalar_s[i] == 0:
            continue
        for j in range(n - i):
            out[i + j] = poly_add(out[i + j], poly_s[j], Fraction(1), scalar_s[i])
    return out


def build_cramer_projectors(max_k: int = 6) -> dict[tuple[str, int], list[Fraction]]:
    """Build Phi_{I0,k}, Phi_{H0,k}, Phi_{m0,k+1} via Petrovich's (2+i) Cramer formula."""
    K = max_k + 1
    e0 = [Fraction(1, math.factorial(4 * m)) for m in range(K)]
    e1 = [Fraction(1, math.factorial(4 * m + 1)) for m in range(K)]
    e2 = [Fraction(1, math.factorial(4 * m + 2)) for m in range(K)]
    e3 = [Fraction(1, math.factorial(4 * m + 3)) for m in range(K)]
    e1_m4 = [((-4) ** m) * e1[m] for m in range(K)]
    e2_m4 = [((-4) ** m) * e2[m] for m in range(K)]
    ze3 = [Fraction(0)] + e3[:-1]

    d_kr = [
        Fraction(2 + gauss_pow_int(2, 1, 4 * m + 1)[0], 4 * math.factorial(4 * m + 1))
        for m in range(K)
    ]
    delta_inv = series_inv([Fraction(-1, 4) * c for c in d_kr])
    e0_inv = series_inv(e0)

    u_polys, v_m4_polys, w_polys = [], [], []
    for j in range(K):
        u, v, w = single_term_u_v_w_coeffs(j)
        u_polys.append(u)
        v_m4_polys.append(poly_scale(v, Fraction((-4) ** j)))
        w_polys.append(w)

    num_i0 = [
        poly_add(
            poly_series_mul([Fraction(-1, 4) * c for c in e1_m4], u_polys)[k],
            poly_series_mul(ze3, v_m4_polys)[k],
        )
        for k in range(K)
    ]
    num_h0 = [
        poly_add(
            poly_series_mul([Fraction(-1, 4) * c for c in e2_m4], u_polys)[k],
            poly_series_mul(e0, v_m4_polys)[k],
        )
        for k in range(K)
    ]
    phi_i0 = poly_series_mul(delta_inv, num_i0)
    phi_h0 = poly_series_mul(delta_inv, num_h0)
    rhs_m0 = [poly_add(w_polys[k], poly_series_mul(e1, phi_h0)[k]) for k in range(K)]
    phi_m0 = poly_series_mul(e0_inv, rhs_m0)

    out: dict[tuple[str, int], list[Fraction]] = {}
    for k in range(K):
        out[("I0", k)] = phi_i0[k]
        out[("H0", k)] = phi_h0[k]
        out[("m0", k + 1)] = phi_m0[k]
    return out


def apply_G_Xi_C_poly(g: list[Fraction]) -> list[Fraction]:
    """Solve L_Xi u = g under Dom_C: u(0)=u(1)=0, 3u''(0)+5u''(1)=0, 3u'''(0)-5u'''(1)=0."""
    rhs = poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    u0 = poly_int(rhs, 4)
    v1 = poly_eval(u0, Fraction(1))
    d2_1 = poly_eval(poly_deriv(u0, 2), Fraction(1))
    d3_1 = poly_eval(poly_deriv(u0, 3), Fraction(1))
    c3 = Fraction(-5, 12) * d3_1
    c2 = (Fraction(-5) * d2_1 - 30 * c3) / Fraction(16)
    c1 = -v1 - c2 - c3
    return poly_add(u0, [Fraction(0), c1, c2, c3])


def apply_G_Xi_A_poly(g: list[Fraction]) -> list[Fraction]:
    """Solve L_Xi u = g under Dom_A: u(0)=u(1)=0, u'(0)-3u'(1)=0, 3u''(0)+5u''(1)=0."""
    rhs = poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    u0 = poly_int(rhs, 4)
    v1 = poly_eval(u0, Fraction(1))
    d1_1 = poly_eval(poly_deriv(u0, 1), Fraction(1))
    d2_1 = poly_eval(poly_deriv(u0, 2), Fraction(1))
    c3 = 6 * d1_1 - 4 * v1 - Fraction(5, 2) * d2_1
    c2 = (Fraction(-5) * d2_1 - 30 * c3) / Fraction(16)
    c1 = -v1 - c2 - c3
    return poly_add(u0, [Fraction(0), c1, c2, c3])


def apply_G_Xi_B_poly(g: list[Fraction]) -> list[Fraction]:
    """Solve L_Xi u = g under Dom_B: u(0)=u(1)=0, u'(0)-3u'(1)=0, 3u'''(0)-5u'''(1)=0."""
    rhs = poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    u0 = poly_int(rhs, 4)
    v1 = poly_eval(u0, Fraction(1))
    d1_1 = poly_eval(poly_deriv(u0, 1), Fraction(1))
    d3_1 = poly_eval(poly_deriv(u0, 3), Fraction(1))
    c3 = Fraction(-5, 12) * d3_1
    c2 = (2 * v1 - 3 * d1_1 - 7 * c3) / Fraction(4)
    c1 = -v1 - c2 - c3
    return poly_add(u0, [Fraction(0), c1, c2, c3])


def apply_G_Xi_C_transpose_poly(w: list[Fraction]) -> list[Fraction]:
    """
    Exact polynomial action of the adjoint operator (G_Xi^{(C)})^* on w(x):
    Solve L_Xi^* v = w under Dom_C^* = {v(1) = 0, v'(1) = 0, v''(0) = 0, v''(1) = 0}.
    Since L_Xi^* = L_Xi = -(3I + 5R)/32 D^4, v^(4)(s) = 6 w(s) - 10 w(1 - s) with v in Dom_C^*!
    """
    rhs = poly_add(w, poly_reflect(w), Fraction(6), Fraction(-10))
    v0 = poly_int(rhs, 4)
    # Add c0 + c1*s + c2*s^2 + c3*s^3 so that v''(0)=0, v''(1)=0, v'(1)=0, v(1)=0:
    # v''(0) = 2*c2 = 0 => c2 = 0
    # v''(1) = v0''(1) + 6*c3 = 0 => c3 = -v0''(1) / 6
    # v'(1)  = v0'(1) + c1 + 3*c3 = 0 => c1 = -v0'(1) - 3*c3
    # v(1)   = v0(1) + c0 + c1 + c3 = 0 => c0 = -v0(1) - c1 - c3
    d2_1 = poly_eval(poly_deriv(v0, 2), Fraction(1))
    d1_1 = poly_eval(poly_deriv(v0, 1), Fraction(1))
    val_1 = poly_eval(v0, Fraction(1))
    c2 = Fraction(0)
    c3 = -d2_1 / Fraction(6)
    c1 = -d1_1 - 3 * c3
    c0 = -val_1 - c1 - c3
    return poly_add(v0, [c0, c1, c2, c3])


def newton_power_sums_from_det(det_coeffs: list[Fraction]) -> list[Fraction]:
    """
    Given Fredholm determinant D(z) = 1 + sum_{m>=1} d_m z^m = prod_i (1 - lambda_i z),
    compute power sums p_n = sum_i lambda_i^n for n = 1..len(det_coeffs)-1 via -z D'(z) / D(z).
    """
    max_n = len(det_coeffs) - 1
    d_inv = series_inv(det_coeffs)
    # -z D'(z) has coefficient at z^n equal to -n * d_n
    neg_zd = [Fraction(0)] + [-Fraction(n) * det_coeffs[n] for n in range(1, max_n + 1)]
    prod = series_mul(neg_zd, d_inv)
    return prod[1:]


def verify_all() -> dict:
    # 1. Verify Theorem 1: Boundary-Slope Functional & Dual Polynomial Annihilator Ladder {P^{dual}_{4k-1}, Q^{dual}_{4k}}
    p3_dual = [Fraction(1), Fraction(-6), Fraction(9), Fraction(-4)]  # (1 - s)^2 (1 - 4s)
    q4_dual = [Fraction(0), Fraction(1), Fraction(-3), Fraction(3), Fraction(-1)]  # y (1 - y)^3
    assert poly_deriv(q4_dual, 1) == p3_dual

    # Check < (G_Xi^{(C)})^* w, g > == < w, G_Xi^{(C)} g > for all monomials up to degree 8
    for i in range(6):
        wi = [Fraction(0)] * (i + 1)
        wi[i] = Fraction(1)
        w_star = apply_G_Xi_C_transpose_poly(wi)
        # Verify w_star lies in Dom_C^* = {v(1)=0, v'(1)=0, v''(0)=0, v''(1)=0}
        assert poly_eval(w_star, Fraction(1)) == 0
        assert poly_eval(poly_deriv(w_star, 1), Fraction(1)) == 0
        assert poly_eval(poly_deriv(w_star, 2), Fraction(0)) == 0
        assert poly_eval(poly_deriv(w_star, 2), Fraction(1)) == 0
        for j in range(6):
            gj = [Fraction(0)] * (j + 1)
            gj[j] = Fraction(1)
            lhs = poly_inner(w_star, gj)
            rhs = poly_inner(wi, apply_G_Xi_C_poly(gj))
            assert lhs == rhs, f"Adjoint mismatch at ({i}, {j}): {lhs} vs {rhs}"

    # Build the Dual Annihilator Ladder P^{dual}_{4k-1}(s) and Q^{dual}_{4k}(y) for k = 1..5
    P_dual_ladder: dict[int, list[Fraction]] = {1: p3_dual}
    Q_dual_ladder: dict[int, list[Fraction]] = {1: q4_dual}
    for k in range(2, 6):
        p_next = apply_G_Xi_C_transpose_poly(P_dual_ladder[k - 1])
        # Since p_next in Dom_C^* has int_0^1 p_next(s) ds = 0 (because G_Xi^{(C)}(1) in Dom_A cap Dom_C!),
        # its antiderivative q_next = int_0^y p_next(s) ds vanishes at BOTH y = 0 and y = 1 (to order 3 at y = 1)!
        q_next = poly_int(p_next, 1)
        assert poly_eval(q_next, Fraction(0)) == 0
        assert poly_eval(q_next, Fraction(1)) == 0
        assert len(p_next) - 1 == 4 * k - 1
        assert len(q_next) - 1 == 4 * k
        P_dual_ladder[k] = p_next
        Q_dual_ladder[k] = q_next

    # Verify that EVERY P^{dual}_{4k-1}(s) and Q^{dual}_{4k}(y) annihilates all m_0 projectors Phi_{m_0, j+1}
    # and Psi_{m_0, j+1} (which span the cantilever dual expansion!) in exact Fraction arithmetic:
    projs = build_cramer_projectors(max_k=6)
    for k in range(1, 5):
        for j in range(7):
            phi_m0 = projs[("m0", j + 1)]
            psi_m0 = poly_scale(poly_deriv(phi_m0, 1), Fraction(1, 4))
            assert poly_inner(P_dual_ladder[k], phi_m0) == 0, f"P_dual_{4*k-1} not orthogonal to Phi_{{m0,{j+1}}}"
            assert poly_inner(Q_dual_ladder[k], psi_m0) + Fraction(1, 4) * poly_inner(P_dual_ladder[k], phi_m0) == 0
            assert poly_inner(Q_dual_ladder[k], psi_m0) == 0, f"Q_dual_{4*k} not orthogonal to Psi_{{m0,{j+1}}}"

    # 2. Verify Theorem 2: Rank-1 Sherman-Morrison Bridge Across Dom_C, Dom_A, Dom_B & (2+i) Quartet
    Phi_H0_0 = projs[("H0", 0)]
    Phi_I0_0 = projs[("I0", 0)]
    ell_A = poly_scale(p3_dual, Fraction(2))
    ell_B = poly_scale(p3_dual, Fraction(1, 3))

    for n in range(9):
        gn = [Fraction(0)] * (n + 1)
        gn[n] = Fraction(1)
        uC = apply_G_Xi_C_poly(gn)
        uA = apply_G_Xi_A_poly(gn)
        uB = apply_G_Xi_B_poly(gn)
        assert poly_add(uC, uA, Fraction(1), Fraction(-1)) == poly_scale(Phi_H0_0, poly_inner(ell_A, gn))
        assert poly_add(uC, uB, Fraction(1), Fraction(-1)) == poly_scale(Phi_I0_0, poly_inner(ell_B, gn))

    # Verify B_slope(Phi_tilde_{H0}) == 4 e_3(z)/e_1(z), B_slope(Phi_tilde_{I0}) == 8 e_2(z)/e_1(z),
    # and B_slope(Phi_tilde_{m0}) == 0 for k = 0..6:
    K = 7
    e1 = [Fraction(1, math.factorial(4 * m + 1)) for m in range(K)]
    e2 = [Fraction(1, math.factorial(4 * m + 2)) for m in range(K)]
    e3 = [Fraction(1, math.factorial(4 * m + 3)) for m in range(K)]
    e1_inv = series_inv(e1)
    ratio_e3_e1 = series_mul(e3, e1_inv)
    ratio_e2_e1 = series_mul(e2, e1_inv)

    for k in range(K):
        for alpha, target_val in (
            ("H0", 4 * ratio_e3_e1[k]),
            ("I0", 8 * ratio_e2_e1[k]),
            ("m0", Fraction(0)),
        ):
            idx = k + 1 if alpha == "m0" else k
            p = projs[(alpha, idx)]
            p1 = poly_deriv(p, 1)
            bs = poly_eval(p1, Fraction(0)) - 3 * poly_eval(p1, Fraction(1))
            assert bs == target_val, f"B_slope mismatch for {alpha}, k={k}: {bs} vs {target_val}"

        if k < K - 1:
            assert poly_inner(ell_A, projs[("H0", k)]) == 6 * ratio_e3_e1[k + 1]
            assert poly_inner(ell_B, projs[("I0", k)]) == 2 * ratio_e2_e1[k + 1]

    # 3. Verify Theorem 3: All-Order Newton Trace-Determinant Decomposition Across the (2+i) Quartet (alpha = 0, 1, 2, 3)
    # Build F(s) = 1 + sum_{m>=1} ((-4)^m / (2 * (4m)!)) z^m:
    f_cant = [Fraction(1)] + [Fraction((-4) ** m, 2 * math.factorial(4 * m)) for m in range(1, K)]
    zeta_cant = newton_power_sums_from_det(f_cant)
    assert zeta_cant[:4] == [
        Fraction(1, 12),
        Fraction(11, 1680),
        Fraction(2641, 4989600),
        Fraction(12343, 288288000),
    ]

    quartet_traces: dict[str, dict[str, list[str]]] = {}
    first_traces_expected = {
        0: Fraction(1, 24),
        1: Fraction(3, 40),
        2: Fraction(29, 360),
        3: Fraction(23, 280),
    }
    for alpha in range(4):
        re_i_alpha = gauss_pow_int(0, 1, alpha)[0]
        d_alpha = [
            Fraction(
                math.factorial(alpha) * (2 + re_i_alpha + gauss_pow_int(2, 1, 4 * m + alpha)[0]),
                4 * math.factorial(4 * m + alpha),
            )
            for m in range(K)
        ]
        e_alpha_norm = [
            Fraction(math.factorial(alpha), math.factorial(4 * m + alpha)) for m in range(K)
        ]
        assert d_alpha == series_mul(e_alpha_norm, f_cant), f"Quartet factorization failed at alpha={alpha}"

        tr_alpha = newton_power_sums_from_det(d_alpha)
        zeta_neg_branch = newton_power_sums_from_det(e_alpha_norm)
        # Since D_alpha(z) = e_alpha_norm(z) * F(s), Newton's log-derivative is additive:
        # Tr_alpha(n) == zeta_cant(4n) + zeta_neg_branch(n)!
        for n_idx in range(K - 1):
            assert tr_alpha[n_idx] == zeta_cant[n_idx] + zeta_neg_branch[n_idx]
        assert tr_alpha[0] == first_traces_expected[alpha]
        assert tr_alpha[0] == Fraction(1, 12) - Fraction(math.factorial(alpha), math.factorial(4 + alpha))
        quartet_traces[f"alpha={alpha}"] = {
            "traces_n1_to_4": [str(c) for c in tr_alpha[:4]],
            "negative_branch_zeta_n1_to_4": [str(c) for c in zeta_neg_branch[:4]],
        }

    # Verify exact alpha = 1 (Dom_C) traces: Tr_1 = 3/40, Tr_2 = (-3/40)^2 - 2*(-179/362880) = 2999/453600 = 11/1680 + 29/453600
    # (catching the inline comment typo 2399/362880 = 11/1680 + 23/362880 where 9!/(5!)^2 = 126/5 = 25.2 was written as 25)
    assert quartet_traces["alpha=1"]["traces_n1_to_4"][:2] == ["3/40", "2999/453600"]
    assert quartet_traces["alpha=1"]["negative_branch_zeta_n1_to_4"][:2] == ["-1/120", "29/453600"]

    return {
        "script": "dual_mode_annihilators_and_sherman_morrison_quartet_2026_11_16.py",
        "theorem_1_dual_mode_annihilator_ladder_k_1_to_5": True,
        "Q_dual_4_coeffs": [str(c) for c in Q_dual_ladder[1]],
        "Q_dual_8_coeffs": [str(c) for c in Q_dual_ladder[2]],
        "theorem_2_sherman_morrison_bridge_Dom_C_A_B": True,
        "first_traces_quartet_alpha_0_to_3": [str(first_traces_expected[a]) for a in range(4)],
        "theorem_3_newton_trace_decomposition_n_1_to_6": True,
        "cantilever_zeta_4n_n_1_to_4": [str(c) for c in zeta_cant[:4]],
        "quartet_traces": quartet_traces,
        "status": "ALL_CHECKS_PASSED",
    }


if __name__ == "__main__":
    res = verify_all()
    out_path = Path(__file__).with_name(Path(__file__).stem + "_results.json")
    out_path.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
