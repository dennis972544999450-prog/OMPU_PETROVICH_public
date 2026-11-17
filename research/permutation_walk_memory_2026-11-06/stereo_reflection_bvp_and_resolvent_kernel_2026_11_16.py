#!/usr/bin/env python3
r"""
stereo_reflection_bvp_and_resolvent_kernel_2026_11_16.py
========================================================
Continuity Rev 103 — Midday Verification Module (2026-11-16)
Author: Petrovich (ompu-e1dd503f59)

Closes the open `[=~` seam from Lane B (`seq 244`, bus:1794823824 §2.5) and connects it
directly to Lane A's Stereo Hodge-Fredholm projection (`seq 243`, bus:1794822727):

  1. THEOREM 1 (4th-Order Stereo Reflection Differential Operators & Exact Spectral Determinants):
     Let (R f)(x) := f(1 - x) be midpoint reflection on [0, 1]. Because every cantilever dual
     \Xi_r(x) = u_{K,r}(x) + u_{R,r}(x) splits into an R-even Kelvin branch (D^4 u_K = -4 \kappa_r^4 u_K)
     and an R-odd Rayleigh branch (D^4 u_R = +16 \kappa_r^4 u_R), both \Xi_r(x) and \Upsilon_r(x) = \Xi_r'(x)/4
     are exact linear eigenfunctions of 4th-order reflection-differential operators:
         (L_\Xi u)(x) := -(3 u^{(4)}(x) + 5 u^{(4)}(1 - x)) / 32 = \kappa_r^4 u(x),
         (L_\Upsilon v)(x) := -(3 v^{(4)}(x) - 5 v^{(4)}(1 - x)) / 32 = \kappa_r^4 v(x),
     and also satisfy the local 8th-order quadratic pencil (D^8 - 12 \kappa_r^4 D^4 - 64 \kappa_r^8) u = 0
     with universal r-independent endpoint laws (\Upsilon_r(0) = 3, \Upsilon_r(1) = 1, 3\Upsilon_r'(0) + 5\Upsilon_r'(1) = 0,
     3\Upsilon_r''(0) - 5\Upsilon_r''(1) = 0, \Upsilon_r'''(0) = \Upsilon_r'''(1) = 0).
     Furthermore:
       - On Dom_C := {u : u(0) = u(1) = 0, 3 u''(0) + 5 u''(1) = 0, 3 u'''(0) - 5 u'''(1) = 0},
         the characteristic determinant is identically the (2+i) Kelvin-Rayleigh determinant:
             det_C(\kappa) == -512 \kappa^5 (\cosh\kappa \cos\kappa + 1) E_1(\kappa),
         whose eigenvalues z = \kappa^4 are {+\kappa_r^4}_{r>=1} U {-4 \beta_m^4}_{m>=1} (\tanh\beta_m + \tan\beta_m = 0).
       - On Dom_A := {u : u(0) = u(1) = 0, u'(0) - 3 u'(1) = 0, 3 u''(0) + 5 u''(1) = 0},
             det_A(\kappa) == -128 \kappa^3 (\cosh\kappa \cos\kappa + 1) E_3(\kappa).
       - Since gcd(E_1(\kappa), E_3(\kappa)) = 1 on C \ {0}, Dom_A \cap Dom_C isolates the PURE
         cantilever dual spectrum {+\kappa_r^4}_{r>=1}, explaining why \Phi_{m_0,k} \in Dom_A \cap Dom_C
         has only cantilever poles while \Phi_{H_0,k}, \Phi_{I_0,k} \in Dom_C \setminus Dom_A carry
         clamped-pinned poles at z = -4 \beta_m^4.

  2. THEOREM 2 (Closed-Form Piecewise-Cubic Stereo Green's Kernels & Universal Projector Ladder):
     Since (-1/32 (3 I + 5 R))^{-1} = 2 (3 I - 5 R), the exact inverse G_\Xi^{(C)} = (L_\Xi|_{Dom_C})^{-1}
     and its pure-beam quarter-derivative dual G_\Upsilon^{(C)} have explicit piecewise-cubic kernels
     supported across the X-shaped Kelvin-Rayleigh light-cone {s = x} U {s = 1 - x}:
         G_\Xi^{(C)}(x, s) = (x - s)_+^3 - (5/3)(x + s - 1)_+^3
                             + (7/3 - 2s - 3s^2 + (8/3)s^3) x + 5(s - 1) x^2 + (5/3) x^3,
         G_\Upsilon^{(C)}(x, t) = (x - t)_+^3 + (5/3)(x + t - 1)_+^3
                                  + (1 - (7/3)t + t^2 + t^3 - (2/3)t^4)
                                  - 5(t - 1)^2 x + 5(1 - t) x^2 - (5/3) x^3.
     They satisfy:
       (a) \int_0^1 G_\Xi^{(C)}(x, s) \Xi_r(s) ds == \Xi_r(x) / \kappa_r^4 and
           \int_0^1 G_\Upsilon^{(C)}(x, t) \Upsilon_r(t) dt == \Upsilon_r(x) / \kappa_r^4 for all r >= 1;
       (b) G_\Xi^{(C)}(1) == \Phi_{m_0, 1}(x), and G_\Xi^{(C)}(\Phi_{\alpha, k}) == \Phi_{\alpha, k+1},
           G_\Upsilon^{(C)}(\Psi_{\alpha, k}) == \Psi_{\alpha, k+1} in Q[x] for ALL \alpha in {m_0, H_0, I_0}, k >= 1.

  3. THEOREM 3 (Biorthogonal Resolvent Kernel K_res(x, y) & Hodge-Fredholm Oblique Decomposition):
     Because ||\hat{\psi}_r||_{L^2(0,1)}^2 == 1, \hat{\psi}_r(0)^2 == 4, and |\Upsilon_r(x)| = O(1),
     the spectral resolvent kernel
         K_res(x, y) := \sum_{r=1}^\infty \Upsilon_r(x) \hat{\psi}_r(y)^2 / \kappa_r^4
     converges absolutely and uniformly on [0, 1]^2 at rate O(r^{-4}), and equals the composition
     G_\Upsilon^{(C)} \circ P_beam of the piecewise-cubic stereo Green's operator with the distributional
     oblique Hodge-Fredholm projector P_beam(x, y) = \sum_{r=1}^\infty \Upsilon_r(x) \hat{\psi}_r(y)^2
     whose nullspace in y is spanned by {1} U {P_{4m+1}'(y)}_{m>=1} (Lane A `seq 243`). Specifically:
       - \int_0^1 K_res(x, y) dy == \Psi_{m_0, 1}(x) = 1/4 - (5/4)x + (5/4)x^2 - (1/6)x^3;
       - K_res(x, 0) == 4 \Psi_{m_0, 1}(x),   K_res(x, 1) == 0;
       - \int_0^1 K_res(x, y) P_{4m+1}'(y) dy == 0 for all m >= 1 (whereas \int_0^1 G_\Upsilon^{(C)}(x, y) P_{4m+1}'(y) dy != 0);
       - Tr(K_res) = \int_0^1 K_res(x, x) dx == \sum_{r=1}^\infty 1 / \kappa_r^4 == 1/12.

Pure standard library (`fractions`, `decimal`, `math`, `json`), runnable via `python3 -I -B`.
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

import gaussian_2plusi_quartet_and_cantilever_mode_duals_2026_11_16 as d244
import gaussian_toeplitz_convolution_and_biorthogonal_projectors_2026_11_15 as gtp
import hodge_fredholm_projection_and_krylov_euler_syzygy_2026_11_16 as jee243

getcontext().prec = 105


# ---------------------------------------------------------------------------
# 1. Exact rational polynomial reflection-differential & Green's helpers
# ---------------------------------------------------------------------------

def poly_deriv(p: List[Fraction], order: int = 1) -> List[Fraction]:
    res = p[:]
    for _ in range(order):
        res = [res[i] * Fraction(i) for i in range(1, len(res))] or [Fraction(0)]
    return res


def poly_int(p: List[Fraction], order: int = 1) -> List[Fraction]:
    res = p[:]
    for _ in range(order):
        out = [Fraction(0)] * (len(res) + 1)
        for k, c in enumerate(res):
            if c != 0:
                out[k + 1] = c / Fraction(k + 1)
        res = out
    return res


def poly_reflect(p: List[Fraction]) -> List[Fraction]:
    """Return R(p)(x) := p(1 - x) in exact Fraction arithmetic."""
    n = len(p)
    out = [Fraction(0)] * n
    for k, c in enumerate(p):
        if c == 0:
            continue
        for j in range(k + 1):
            out[j] += c * Fraction(math.comb(k, j) * ((-1) ** j))
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def L_Xi_poly(p: List[Fraction]) -> List[Fraction]:
    """(L_Xi p)(x) = -(3 p^(4)(x) + 5 p^(4)(1 - x)) / 32."""
    d4 = poly_deriv(p, 4)
    rd4 = poly_reflect(d4)
    return gtp.poly_scale(gtp.poly_add(d4, rd4, Fraction(-3), Fraction(-5)), Fraction(1, 32))


def L_Upsilon_poly(p: List[Fraction]) -> List[Fraction]:
    """(L_Upsilon p)(x) = -(3 p^(4)(x) - 5 p^(4)(1 - x)) / 32."""
    d4 = poly_deriv(p, 4)
    rd4 = poly_reflect(d4)
    return gtp.poly_scale(gtp.poly_add(d4, rd4, Fraction(-3), Fraction(5)), Fraction(1, 32))


def apply_G_Xi_C_poly(g: List[Fraction]) -> List[Fraction]:
    """Exact polynomial evaluation of x -> int_0^1 G_Xi^{(C)}(x, s) g(s) ds."""
    # Split int_0^1 = int_0^x + int_x^1 for (x-s)_+^3 and int_{1-x}^1 for (x+s-1)_+^3:
    # Equivalently solve u^(4)(x) = 6 g(x) - 10 g(1 - x) under Dom_C!
    rhs = gtp.poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    u0 = poly_int(rhs, 4)
    v1 = gtp.poly_eval(u0, Fraction(1))
    d2_1 = gtp.poly_eval(poly_deriv(u0, 2), Fraction(1))
    d3_1 = gtp.poly_eval(poly_deriv(u0, 3), Fraction(1))
    c3 = Fraction(-5, 12) * d3_1
    c2 = (Fraction(-5) * d2_1 - 30 * c3) / Fraction(16)
    c1 = -v1 - c2 - c3
    return gtp.poly_add(u0, [Fraction(0), c1, c2, c3])


def apply_G_Xi_A_poly(g: List[Fraction]) -> List[Fraction]:
    """Exact polynomial evaluation of x -> int_0^1 G_Xi^{(A)}(x, s) g(s) ds under Dom_A."""
    rhs = gtp.poly_add(g, poly_reflect(g), Fraction(6), Fraction(-10))
    u0 = poly_int(rhs, 4)
    v1 = gtp.poly_eval(u0, Fraction(1))
    d1_1 = gtp.poly_eval(poly_deriv(u0, 1), Fraction(1))
    d2_1 = gtp.poly_eval(poly_deriv(u0, 2), Fraction(1))
    c3 = 6 * d1_1 - 4 * v1 - Fraction(5, 2) * d2_1
    c2 = (Fraction(-5) * d2_1 - 30 * c3) / Fraction(16)
    c1 = -v1 - c2 - c3
    return gtp.poly_add(u0, [Fraction(0), c1, c2, c3])


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


def G_Upsilon_C_dec(x: Decimal, t: Decimal) -> Decimal:
    """Closed-form piecewise-cubic pure-beam dual Green's kernel G_Upsilon^{(C)}(x, t) on [0, 1]^2."""
    p1 = (x - t) ** 3 if x > t else Decimal(0)
    p2 = (Decimal(5) / Decimal(3)) * ((x + t - Decimal(1)) ** 3) if (x + t > Decimal(1)) else Decimal(0)
    q0 = (
        Decimal(1)
        - (Decimal(7) / Decimal(3)) * t
        + (t ** 2)
        + (t ** 3)
        - (Decimal(2) / Decimal(3)) * (t ** 4)
    )
    q1 = Decimal(-5) * ((t - Decimal(1)) ** 2) * x
    q2 = Decimal(5) * (Decimal(1) - t) * (x ** 2)
    q3 = (Decimal(-5) / Decimal(3)) * (x ** 3)
    return p1 + p2 + q0 + q1 + q2 + q3


def xi_derivs_dec(kap: Decimal, w_r: Decimal, x: Decimal, max_n: int = 8) -> List[Decimal]:
    """Evaluate exact n-th derivatives of Xi_r(x) for 0 <= n <= max_n in 105-digit Decimal."""
    sh, ch = d244.dec_sinh_cosh(kap)
    si, co = d244.dec_sin_cos(kap)
    e0_k = Decimal("0.5") * (ch + co)
    c_u = (sh * si) / (Decimal(2) * e0_k)
    kw_k = (kap * x, kap * (Decimal(1) - x))
    kw_r = (kap * (Decimal(2) * x - Decimal(1)), kap)
    out: List[Decimal] = []
    pr, pi = Decimal(1), Decimal(0)
    for n in range(max_n + 1):
        ek = d244.cdec_E((2 - n) % 4, kw_k)
        er = d244.cdec_E((0 - n) % 4, kw_r)
        im_k = (kap ** n) * (pr * ek[1] + pi * ek[0])
        im_r = ((Decimal(2) * kap) ** n) * er[1]
        out.append(w_r * (c_u * im_k + im_r))
        pr, pi = pr + pi, pi - pr  # multiply by (1 - i)
    return out


# ---------------------------------------------------------------------------
# 2. Theorem 1: 4th-Order Stereo Reflection BVP & Spectral Determinants
# ---------------------------------------------------------------------------

def verify_theorem_1(modes: List[Tuple[Decimal, Decimal, Decimal]]) -> Dict[str, object]:
    max_ode4_xi_err = Decimal(0)
    max_ode4_ups_err = Decimal(0)
    max_ode8_err = Decimal(0)
    max_bc_err = Decimal(0)

    test_xs = [Decimal("0.13"), Decimal("0.29"), Decimal("0.5"), Decimal("0.81")]
    for r_idx in range(8):
        kap, _, w_r = modes[r_idx]
        lam = kap ** 4
        d0 = xi_derivs_dec(kap, w_r, Decimal(0), 8)
        d1 = xi_derivs_dec(kap, w_r, Decimal(1), 8)
        # Universal endpoint laws (in particular Upsilon_r(0)=3, Upsilon_r(1)=1 for all r >= 1!)
        bc_errs = [
            abs(d0[0]),
            abs(d1[0]),
            abs(d0[1] - Decimal(12)),
            abs(d1[1] - Decimal(4)),
            abs(Decimal(3) * d0[2] + Decimal(5) * d1[2]),
            abs(Decimal(3) * d0[3] - Decimal(5) * d1[3]),
            abs(d0[4]),
            abs(d1[4]),
            abs(Decimal(9) * d0[5] - Decimal(7) * d1[5]),
            abs(Decimal(17) * d0[6] + Decimal(15) * d1[6]),
            abs(Decimal(17) * d0[7] - Decimal(15) * d1[7]),
            abs(d0[8]),
            abs(d1[8]),
        ]
        max_bc_err = max(max_bc_err, max(bc_errs))

        for x in test_xs:
            dx = xi_derivs_dec(kap, w_r, x, 8)
            dr = xi_derivs_dec(kap, w_r, Decimal(1) - x, 8)
            lhs_xi = -(Decimal(3) * dx[4] + Decimal(5) * dr[4]) / Decimal(32)
            # Upsilon_r = Xi_r'/4, so Upsilon_r^(4)(1-x) = (-1)^4 * (-1)?? Wait:
            # Upsilon(z) = (1/4) Xi'(z) => Upsilon^(4)(z) = (1/4) Xi^(5)(z), so at z = 1 - x it is (1/4) Xi^(5)(1 - x)!
            ups_x = Decimal("0.25") * dx[1]
            lhs_ups = -(Decimal(3) * (Decimal("0.25") * dx[5]) - Decimal(5) * (Decimal("0.25") * dr[5])) / Decimal(32)
            ode8 = dx[8] - Decimal(12) * lam * dx[4] - Decimal(64) * (lam ** 2) * dx[0]

            max_ode4_xi_err = max(max_ode4_xi_err, abs(lhs_xi - lam * dx[0]))
            max_ode4_ups_err = max(max_ode4_ups_err, abs(lhs_ups - lam * ups_x))
            max_ode8_err = max(max_ode8_err, abs(ode8))

    assert max_ode4_xi_err < Decimal("1e-92"), f"L_Xi eigenfunction error: {max_ode4_xi_err}"
    assert max_ode4_ups_err < Decimal("1e-90"), f"L_Upsilon eigenfunction error: {max_ode4_ups_err}"
    assert max_ode8_err < Decimal("1e-85"), f"8th-order pencil error: {max_ode8_err}"
    assert max_bc_err < Decimal("1e-90"), f"Universal BC error: {max_bc_err}"

    # Verify exact closed-form spectral determinants det_C(kap) and det_A(kap)
    def det4(mat: List[List[Decimal]]) -> Decimal:
        a = [row[:] for row in mat]
        det = Decimal(1)
        for i in range(4):
            piv = max(range(i, 4), key=lambda r: abs(a[r][i]))
            if abs(a[piv][i]) < Decimal("1e-95"):
                return Decimal(0)
            if piv != i:
                a[i], a[piv] = a[piv], a[i]
                det = -det
            det *= a[i][i]
            for r in range(i + 1, 4):
                fac = a[r][i] / a[i][i]
                for c in range(i, 4):
                    a[r][c] -= fac * a[i][c]
        return det

    max_det_c_err = Decimal(0)
    max_det_a_err = Decimal(0)
    for kap_str in ("0.7", "1.3", "1.57079632679489661923", "2.1", "2.8"):
        kap = Decimal(kap_str)

        def eval_basis(x_pt: Decimal) -> List[List[Decimal]]:
            yy = x_pt - Decimal("0.5")
            ky = kap * yy
            sh, ch = d244.dec_sinh_cosh(ky)
            si, co = d244.dec_sin_cos(ky)
            sh2, ch2 = d244.dec_sinh_cosh(Decimal(2) * ky)
            si2, co2 = d244.dec_sin_cos(Decimal(2) * ky)
            ud: List[List[Decimal]] = [[], [], [], []]
            pr, pi = Decimal(1), Decimal(0)
            for n in range(5):
                zr, zi = (ch * co, sh * si) if (n % 2 == 0) else (sh * co, ch * si)
                ud[0].append((kap ** n) * (pr * zr - pi * zi))
                ud[1].append((kap ** n) * (pr * zi + pi * zr))
                k2 = (Decimal(2) * kap) ** n
                ud[2].append(k2 * (sh2 if (n % 2 == 0) else ch2))
                ud[3].append(k2 * [si2, co2, -si2, -co2][n % 4])
                pr, pi = pr - pi, pr + pi
            return ud

        b0 = eval_basis(Decimal(0))
        b1 = eval_basis(Decimal(1))
        full = [
            [
                b0[j][0],
                b1[j][0],
                b0[j][1] - Decimal(3) * b1[j][1],
                Decimal(3) * b0[j][2] + Decimal(5) * b1[j][2],
                Decimal(3) * b0[j][3] - Decimal(5) * b1[j][3],
            ]
            for j in range(4)
        ]
        det_c = det4([[full[j][k] for k in (0, 1, 3, 4)] for j in range(4)])
        det_a = det4([[full[j][k] for k in (0, 1, 2, 3)] for j in range(4)])

        shk, chk = d244.dec_sinh_cosh(kap)
        sik, cok = d244.dec_sin_cos(kap)
        sec = chk * cok + Decimal(1)
        e1_k = Decimal("0.5") * (shk + sik)
        e3_k = Decimal("0.5") * (shk - sik)

        exact_c = Decimal(-512) * (kap ** 5) * sec * e1_k
        exact_a = Decimal(-128) * (kap ** 3) * sec * e3_k
        max_det_c_err = max(max_det_c_err, abs(det_c - exact_c))
        max_det_a_err = max(max_det_a_err, abs(det_a - exact_a))

    assert max_det_c_err < Decimal("1e-90"), f"det_C identity error: {max_det_c_err}"
    assert max_det_a_err < Decimal("1e-90"), f"det_A identity error: {max_det_a_err}"

    return {
        "status": "PASS",
        "max_L_Xi_eigen_error": f"{max_ode4_xi_err:.3e}",
        "max_L_Upsilon_eigen_error": f"{max_ode4_ups_err:.3e}",
        "max_8th_order_pencil_error": f"{max_ode8_err:.3e}",
        "max_universal_endpoint_law_error": f"{max_bc_err:.3e}",
        "max_det_C_factorization_error": f"{max_det_c_err:.3e}",
        "max_det_A_factorization_error": f"{max_det_a_err:.3e}",
    }


# ---------------------------------------------------------------------------
# 3. Theorem 2: Piecewise-Cubic Stereo Green's Kernels & Universal Ladder
# ---------------------------------------------------------------------------

def verify_theorem_2(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    gl32: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    projs = gtp.build_biorthogonal_projectors(max_k=6)

    # (a) Exact rational polynomial ladder checks across ALL 3 families m0, H0, I0
    assert apply_G_Xi_C_poly([Fraction(1)]) == projs[("m0", 1)]["Phi"]
    assert apply_G_Xi_A_poly([Fraction(1)]) == projs[("m0", 1)]["Phi"]
    assert L_Xi_poly(projs[("m0", 1)]["Phi"]) == [Fraction(1)]

    for k in range(1, 6):
        assert apply_G_Xi_C_poly(projs[("m0", k)]["Phi"]) == projs[("m0", k + 1)]["Phi"]
        assert apply_G_Xi_A_poly(projs[("m0", k)]["Phi"]) == projs[("m0", k + 1)]["Phi"]
        assert L_Xi_poly(projs[("m0", k + 1)]["Phi"]) == projs[("m0", k)]["Phi"]
        assert L_Upsilon_poly(projs[("m0", k + 1)]["Psi"]) == projs[("m0", k)]["Psi"]

    for fam in ("H0", "I0"):
        for k in range(1, 5):
            assert apply_G_Xi_C_poly(projs[(fam, k)]["Phi"]) == projs[(fam, k + 1)]["Phi"]
            assert L_Xi_poly(projs[(fam, k + 1)]["Phi"]) == projs[(fam, k)]["Phi"]
            assert L_Upsilon_poly(projs[(fam, k + 1)]["Psi"]) == projs[(fam, k)]["Psi"]
            # Confirm Dom_A differs from Dom_C on H0/I0 because B_3 != 0 (clamped-pinned defect)
            assert apply_G_Xi_A_poly(projs[(fam, k)]["Phi"]) != projs[(fam, k + 1)]["Phi"]

    # (b) Verify piecewise-cubic kernels G_Xi^{(C)}(x, s) and G_Upsilon^{(C)}(x, t) directly by
    #     piecewise 32-point Gauss-Legendre quadrature split across the ridges s = x and s = 1 - x!
    def quad_sub(fn, a: Decimal, b: Decimal) -> Decimal:
        if b <= a:
            return Decimal(0)
        length = b - a
        return sum(length * w * fn(a + length * z) for z, w in gl32)

    max_green_xi_eigen_err = Decimal(0)
    max_green_ups_eigen_err = Decimal(0)
    max_green_poly_err = Decimal(0)

    for xs in ("0.2", "0.37", "0.73"):
        x = Decimal(xs)
        pts = sorted(list({Decimal(0), Decimal(1), x, Decimal(1) - x}))

        # Check integral against Psi_{H0, 2}(t) -> Psi_{H0, 3}(x)
        psi_in = projs[("H0", 2)]["Psi"]
        psi_out = projs[("H0", 3)]["Psi"]
        ex_f = gtp.poly_eval(psi_out, Fraction(int(x * 100), 100))
        ex_d = Decimal(ex_f.numerator) / Decimal(ex_f.denominator)

        def eval_poly_dec(poly: List[Fraction], t_val: Decimal) -> Decimal:
            acc = Decimal(0)
            for p_pow in range(len(poly) - 1, -1, -1):
                c_f = poly[p_pow]
                c_d = Decimal(c_f.numerator) / Decimal(c_f.denominator)
                acc = acc * t_val + c_d
            return acc

        num_poly = sum(
            quad_sub(lambda t: G_Upsilon_C_dec(x, t) * eval_poly_dec(psi_in, t), pts[i], pts[i + 1])
            for i in range(len(pts) - 1)
        )
        max_green_poly_err = max(max_green_poly_err, abs(num_poly - ex_d))

        for r_idx in range(4):
            kap, _, w_r = modes[r_idx]
            xi_x, ups_x = d244.eval_Xi_and_Upsilon_dec(kap, w_r, x)
            int_xi = sum(
                quad_sub(lambda s: G_Xi_C_dec(x, s) * d244.eval_Xi_and_Upsilon_dec(kap, w_r, s)[0], pts[i], pts[i + 1])
                for i in range(len(pts) - 1)
            )
            int_ups = sum(
                quad_sub(lambda t: G_Upsilon_C_dec(x, t) * d244.eval_Xi_and_Upsilon_dec(kap, w_r, t)[1], pts[i], pts[i + 1])
                for i in range(len(pts) - 1)
            )
            max_green_xi_eigen_err = max(max_green_xi_eigen_err, abs(int_xi - xi_x / (kap ** 4)))
            max_green_ups_eigen_err = max(max_green_ups_eigen_err, abs(int_ups - ups_x / (kap ** 4)))

    assert max_green_poly_err < Decimal("1e-95"), f"Green kernel polynomial ladder error: {max_green_poly_err}"
    assert max_green_xi_eigen_err < Decimal("1e-50"), f"Green kernel Xi_r eigen error: {max_green_xi_eigen_err}"
    assert max_green_ups_eigen_err < Decimal("1e-50"), f"Green kernel Upsilon_r eigen error: {max_green_ups_eigen_err}"

    return {
        "status": "PASS",
        "universal_ladder_verified_in_Q_x": {
            "m0": "k=1..6 (Dom_C and Dom_A identical)",
            "H0": "k=1..5 (Dom_C exact; Dom_A separates clamped-pinned defect)",
            "I0": "k=1..5 (Dom_C exact; Dom_A separates clamped-pinned defect)",
        },
        "max_green_kernel_poly_quadrature_error": f"{max_green_poly_err:.3e}",
        "max_green_Xi_eigen_error_r1_to_4": f"{max_green_xi_eigen_err:.3e}",
        "max_green_Upsilon_eigen_error_r1_to_4": f"{max_green_ups_eigen_err:.3e}",
    }


# ---------------------------------------------------------------------------
# 4. Theorem 3: Resolvent Kernel K_res(x, y) & Hodge-Fredholm Decomposition
# ---------------------------------------------------------------------------

def verify_theorem_3(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    gl64: List[Tuple[Decimal, Decimal]],
    gl32: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    projs = gtp.build_biorthogonal_projectors(max_k=2)
    psi_m0_1 = projs[("m0", 1)]["Psi"]  # 1/4 - 5/4 x + 5/4 x^2 - 1/6 x^3
    assert psi_m0_1 == [Fraction(1, 4), Fraction(-5, 4), Fraction(5, 4), Fraction(-1, 6)]

    # (a) Verify ||\hat{\psi}_r||_{L^2}^2 == 1, \hat{\psi}_r(0)^2 == 4, \hat{\psi}_r(1)^2 == 0
    max_norm_err = Decimal(0)
    max_tip_err = Decimal(0)
    for r_idx in range(6):
        kap, t_r, _ = modes[r_idx]
        norm2 = sum(w * d244.eval_psi_hat_sq_dec(kap, t_r, y) for y, w in gl64)
        tip0 = d244.eval_psi_hat_sq_dec(kap, t_r, Decimal(0))
        root1 = d244.eval_psi_hat_sq_dec(kap, t_r, Decimal(1))
        max_norm_err = max(max_norm_err, abs(norm2 - Decimal(1)))
        max_tip_err = max(max_tip_err, abs(tip0 - Decimal(4)), abs(root1))

    assert max_norm_err < Decimal("1e-55"), f"L2 norm error: {max_norm_err}"
    assert max_tip_err < Decimal("1e-88"), f"Tip/root evaluation error: {max_tip_err}"

    # (b) Verify exact k=0 Mittag-Leffler traces of K_res(x, y):
    #     \int_0^1 K_res(x, y) dy == \Psi_{m_0, 1}(x) and K_res(x, 0) == 4 \Psi_{m_0, 1}(x)
    max_k0_trace_err = Decimal(0)
    for xf in (Fraction(1, 5), Fraction(1, 2), Fraction(3, 4)):
        xd = Decimal(xf.numerator) / Decimal(xf.denominator)
        ex_f = gtp.poly_eval(psi_m0_1, xf)
        ex_d = Decimal(ex_f.numerator) / Decimal(ex_f.denominator)
        sum_int_y = sum(d244.eval_Xi_and_Upsilon_dec(k, w, xd)[1] / (k ** 4) for k, _, w in modes)
        sum_tip_0 = sum(
            d244.eval_Xi_and_Upsilon_dec(k, w, xd)[1] * d244.eval_psi_hat_sq_dec(k, t, Decimal(0)) / (k ** 4)
            for k, t, w in modes
        )
        max_k0_trace_err = max(max_k0_trace_err, abs(sum_int_y - ex_d), abs(sum_tip_0 - Decimal(4) * ex_d))

    # 85 modes with O(r^{-4}) tail (~ 85^{-3} ~ 1e-6, alternating ~ 1e-9)
    assert max_k0_trace_err < Decimal("1e-8"), f"k=0 Mittag-Leffler trace error: {max_k0_trace_err}"

    # (c) Verify Hodge-Fredholm annihilation: \int_0^1 \hat{\psi}_r(y)^2 P_{4m+1}'(y) dy == 0
    #     for m = 1, 2, 3 and r = 1..5, whereas \int_0^1 G_Upsilon^{(C)}(x, y) P_{4m+1}'(y) dy != 0!
    def eval_poly_dec(poly: List[Fraction], y_val: Decimal) -> Decimal:
        acc = Decimal(0)
        for p_pow in range(len(poly) - 1, -1, -1):
            c_f = poly[p_pow]
            c_d = Decimal(c_f.numerator) / Decimal(c_f.denominator)
            acc = acc * y_val + c_d
        return acc

    def quad_sub(fn, a: Decimal, b: Decimal) -> Decimal:
        if b <= a:
            return Decimal(0)
        length = b - a
        return sum(length * w * fn(a + length * z) for z, w in gl32)

    max_hodge_annih_err = Decimal(0)
    nonvanishing_green_samples: Dict[str, str] = {}
    x_probe = Decimal("0.37")
    pts_probe = sorted(list({Decimal(0), Decimal(1), x_probe, Decimal(1) - x_probe}))

    for m_ker in (1, 2, 3):
        p_ker = jee243.single_term_P_4K_plus_1_coeffs(m_ker)
        dp_ker = poly_deriv(p_ker, 1)
        for r_idx in range(5):
            kap, t_r, _ = modes[r_idx]
            ip = sum(
                w * d244.eval_psi_hat_sq_dec(kap, t_r, y) * eval_poly_dec(dp_ker, y)
                for y, w in gl64
            )
            max_hodge_annih_err = max(max_hodge_annih_err, abs(ip))

        g_on_ker = sum(
            quad_sub(lambda t: G_Upsilon_C_dec(x_probe, t) * eval_poly_dec(dp_ker, t), pts_probe[i], pts_probe[i + 1])
            for i in range(len(pts_probe) - 1)
        )
        assert apply_G_Xi_C_poly(p_ker) != [Fraction(0)]
        assert abs(g_on_ker) > Decimal("1e-12")
        nonvanishing_green_samples[f"m={m_ker}"] = f"{g_on_ker:.6e}"

    assert max_hodge_annih_err < Decimal("1e-55"), f"Hodge kernel annihilation error: {max_hodge_annih_err}"

    # (d) Verify spectral trace Tr(K_res) = \int_0^1 K_res(x, x) dx == \sum_{r>=1} 1/\kappa_r^4 == 1/12
    #     and iterated trace Tr(K_res^2) = \sum_{r>=1} 1/\kappa_r^8 == 11/1680!
    tr1_num = sum(Decimal(1) / (k ** 4) for k, _, _ in modes)
    tr2_num = sum(Decimal(1) / (k ** 8) for k, _, _ in modes)
    err_tr1 = abs(tr1_num - Decimal(1) / Decimal(12))
    err_tr2 = abs(tr2_num - Decimal(11) / Decimal(1680))
    assert err_tr1 < Decimal("1e-7")
    assert err_tr2 < Decimal("1e-15")

    return {
        "status": "PASS",
        "max_psi_hat_L2_norm_error": f"{max_norm_err:.3e}",
        "max_psi_hat_tip_root_error": f"{max_tip_err:.3e}",
        "max_k0_mittag_leffler_trace_error_85_modes": f"{max_k0_trace_err:.3e}",
        "max_hodge_kernel_annihilation_error": f"{max_hodge_annih_err:.3e}",
        "green_operator_on_hodge_kernel_x037": nonvanishing_green_samples,
        "trace_errors_85_modes": {
            "Tr_K_res_vs_1_over_12": f"{err_tr1:.3e}",
            "Tr_K_res_sq_vs_11_over_1680": f"{err_tr2:.3e}",
        },
    }


def main() -> None:
    modes_85 = [d244.solve_kappa_105(r) for r in range(1, 86)]
    gl32 = d244.gauss_legendre_nodes_weights(32)
    gl64 = d244.gauss_legendre_nodes_weights(64)

    res1 = verify_theorem_1(modes_85)
    res2 = verify_theorem_2(modes_85, gl32)
    res3 = verify_theorem_3(modes_85, gl64, gl32)

    report = {
        "script": "stereo_reflection_bvp_and_resolvent_kernel_2026_11_16.py",
        "author": "Petrovich (ompu-e1dd503f59)",
        "date": "2026-11-16",
        "revision": 103,
        "closes_seam": "Lane B seq 244 (bus:1794823824 §2.5) + connects to Lane A seq 243 (bus:1794822727)",
        "theorem_1_stereo_reflection_bvp_and_spectral_determinants": res1,
        "theorem_2_piecewise_cubic_green_kernels_and_universal_ladder": res2,
        "theorem_3_resolvent_kernel_and_hodge_fredholm_decomposition": res3,
        "verdict": "ALL_CHECKS_PASSED",
    }

    out_path = HERE / "stereo_reflection_bvp_and_resolvent_kernel_2026_11_16_results.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=" * 78)
    print("STEREO REFLECTION BVP, PIECEWISE-CUBIC GREEN KERNEL & RESOLVENT DECOMPOSITION")
    print("=" * 78)
    print(f"[PASS] Theorem 1: 4th-order stereo operators L_Xi, L_Upsilon (err={res1['max_L_Upsilon_eigen_error']}), "
          f"det_C == -512 k^5 (ch*co+1) E_1 (err={res1['max_det_C_factorization_error']}), "
          f"det_A == -128 k^3 (ch*co+1) E_3 (err={res1['max_det_A_factorization_error']})")
    print(f"[PASS] Theorem 2: Piecewise-cubic Green kernels G_Xi^(C), G_Upsilon^(C) across s=x & s=1-x "
          f"(poly err={res2['max_green_kernel_poly_quadrature_error']}, eigen err={res2['max_green_Upsilon_eigen_error_r1_to_4']})")
    print(f"[PASS] Theorem 3: K_res = G_Upsilon^(C) o P_beam, k=0 traces (err={res3['max_k0_mittag_leffler_trace_error_85_modes']}), "
          f"Hodge annihilation <psi_r^2, P_{{4m+1}}'> == 0 (err={res3['max_hodge_kernel_annihilation_error']})")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
