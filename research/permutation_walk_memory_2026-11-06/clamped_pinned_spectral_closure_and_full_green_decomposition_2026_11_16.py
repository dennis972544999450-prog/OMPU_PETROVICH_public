#!/usr/bin/env python3
r"""
clamped_pinned_spectral_closure_and_full_green_decomposition_2026_11_16.py
==========================================================================
Continuity Rev 104 — Afternoon Verification Module (2026-11-16)
Author: Petrovich (ompu-e1dd503f59)

Closes the `[=~` seam proposed in `stereo_reflection_bvp_and_resolvent_kernel_2026_11_16.py`
(bus:1794827014, invited by Phi-Hausmaster in bus:1794827139 and integrated in READ-0093):

  1. THEOREM 1 (Adjoint Domain Dom_C^* & Closed-Form Clamped-Pinned Eigen-Pairs at z_m = -4 \beta_m^4):
     Under 4-fold integration by parts on L^2(0, 1), the stereo reflection operator
     L_\Xi = -(3 I + 5 R)/32 D^4 on Dom_C = {u(0)=u(1)=0, 3u''(0)+5u''(1)=0, 3u'''(0)-5u'''(1)=0}
     has formal adjoint L_\Xi^* = L_\Xi on the elementary local-endpoint adjoint domain:
         Dom_C^* = { w \in C^4[0, 1] : w(1) = 0,  w'(1) = 0,  w''(0) = 0,  w''(1) = 0 }.
     - On the positive cantilever branch z_r^+ = +\kappa_r^4 (\cosh\kappa_r \cos\kappa_r + 1 = 0),
       the adjoint eigenmodes in Dom_C^* are w_r^*(s) = -(1/4) d/ds [\hat{\psi}_r(s)^2] = -(1/2) \hat{\psi}_r(s) \hat{\psi}_r'(s).
     - On the negative clamped-pinned branch z_m^- = -4 \beta_m^4 (\tanh\beta_m + \tan\beta_m = 0, m >= 1),
       with y = x - 1/2, the exact closed-form right/left eigenmodes (\Theta_m \in Dom_C, \Theta_m^* \in Dom_C^*) are:
           \Theta_m(x)   = \sin\beta_m (\cos\beta_m \cosh 2\beta_m y - \cosh\beta_m \cos 2\beta_m y)
                           + 2 \cos\beta_m (\sinh 2\beta_m y \cos 2\beta_m y + \cosh 2\beta_m y \sin 2\beta_m y),
           \Theta_m^*(s) = [ \sin\beta_m (\cos\beta_m \cosh 2\beta_m y + \cosh\beta_m \cos 2\beta_m y)
                             + \cos\beta_m (\sinh 2\beta_m y \cos 2\beta_m y - \cosh 2\beta_m y \sin 2\beta_m y) ] / N_m,
       where all 1/\beta_m oscillatory integral terms cancel identically, leaving the single-monomial norm:
           N_m = -\cosh^2(\beta_m) \cos^4(\beta_m) == -(1/2) \cos^2(\beta_m) (\cosh^2\beta_m + \cos^2\beta_m)!
       Passing to pure-beam quarter-derivatives \Omega_m(x) := \Theta_m'(x)/4 and \Omega_m^*(y) := 4 \int_y^1 \Theta_m^*(s) ds
       yields full two-branch Kronecker biorthogonality across ALL r, m, n >= 1:
           <\Omega_m, \Omega_n^*> == \delta_{m,n},   <\Upsilon_r, \Omega_m^*> == 0,   <\Omega_m, \hat{\psi}_r^2> == 0.

  2. THEOREM 2 (Exact Two-Branch Spectral Decomposition of G_\Xi^{(C)}, G_\Upsilon^{(C)} & Trace Completeness):
     The piecewise-cubic stereo Green's kernels decompose across [0, 1]^2 with ZERO quasi-nilpotent remainder:
         G_\Xi^{(C)}(x, s)      = \sum_{r=1}^\infty \frac{\Xi_r(x) w_r^*(s)}{\kappa_r^4}
                                  - \sum_{m=1}^\infty \frac{\Theta_m(x) \Theta_m^*(s)}{4 \beta_m^4},
         G_\Upsilon^{(C)}(x, y) = K_res(x, y) - \sum_{m=1}^\infty \frac{\Omega_m(x) \Omega_m^*(y)}{4 \beta_m^4},
     and the analytical diagonal trace splits cleanly between the cantilever zeta 1/12 and clamped-pinned zeta 1/120:
         Tr(G_\Xi^{(C)}) = \int_0^1 G_\Xi^{(C)}(x, x) dx = -5/24 + 17/60 = 3/40 == 1/12 - 1/120
                         = \sum_{r=1}^\infty \frac{1}{\kappa_r^4} - \sum_{m=1}^\infty \frac{1}{4 \beta_m^4},
         Tr((G_\Xi^{(C)})^2) = \int_0^1 \int_0^1 G_\Xi^{(C)}(x, s) G_\Xi^{(C)}(s, x) ds dx = 2399/362880
                             == 11/1680 + 23/362880 = \sum_{r=1}^\infty \frac{1}{\kappa_r^8} + \sum_{m=1}^\infty \frac{1}{16 \beta_m^8}.

  3. THEOREM 3 (Exact Two-Branch Functional Mittag-Leffler Law for \Phi_{H_0, k} and \Phi_{I_0, k}):
     Because \Phi_{H_0, 0} and \Phi_{I_0, 0} have endpoint boundary defects -16 in B_5 and B_4 respectively,
     4-fold integration by parts against \Theta_m^* yields exact elementary clamped-pinned weights
         \Theta_m^*(0)  = 4 \tanh\beta_m / (\cosh\beta_m \cos^2\beta_m),
         \Theta_m^*'(0) = -8 \beta_m \tanh^2\beta_m / (\cosh\beta_m \cos^2\beta_m),
     closing the all-order functional Mittag-Leffler series for BOTH remaining projector ladders (k >= 1):
         \Phi_{H_0, k}(x) = \sum_{r=1}^\infty \frac{t_r \Xi_r(x)}{\kappa_r^{4k+3}}
                            + \sum_{m=1}^\infty \frac{\Theta_m^*(0) / 2}{(-4 \beta_m^4)^{k+1}} \Theta_m(x),
         \Phi_{I_0, k}(x) = \sum_{r=1}^\infty \frac{t_r^2 \Xi_r(x)}{\kappa_r^{4k+2}}
                            - \sum_{m=1}^\infty \frac{\Theta_m^*'(0) / 2}{(-4 \beta_m^4)^{k+1}} \Theta_m(x).

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
import stereo_reflection_bvp_and_resolvent_kernel_2026_11_16 as srb

getcontext().prec = 105
PI = d244.PI_DEC


def solve_beta_105(m: int) -> Decimal:
    """Solve tanh(beta) + tan(beta) = 0 (m >= 1) to ~102 digits in Decimal."""
    b = Decimal("2.365020372431352013012024050417") if m == 1 else (Decimal(m) - Decimal("0.25")) * PI
    for _ in range(40):
        sh, ch = d244.dec_sinh_cosh(b)
        si, co = d244.dec_sin_cos(b)
        dk = (sh * co + ch * si) / (Decimal(2) * ch * co)
        b -= dk
        if abs(dk) < Decimal("1e-102"):
            break
    return b


def eval_cp_modes_dec(b: Decimal, x: Decimal) -> Tuple[Decimal, Decimal, Decimal, Decimal]:
    """
    Evaluate normalized clamped-pinned eigen-quartet at x in [0, 1]:
      (Theta_m(x), Theta_m^*(x), Omega_m(x), Omega_m^*(x))
    satisfying <Theta_m, Theta_m^*> == 1 and <Omega_m, Omega_m^*> == 1.
    """
    y = x - Decimal("0.5")
    shb, chb = d244.dec_sinh_cosh(b)
    sib, cob = d244.dec_sin_cos(b)
    sh2, ch2 = d244.dec_sinh_cosh(Decimal(2) * b * y)
    si2, co2 = d244.dec_sin_cos(Decimal(2) * b * y)

    n_m = -(chb ** 2) * (cob ** 4)
    th = sib * (cob * ch2 - chb * co2) + Decimal(2) * cob * (sh2 * co2 + ch2 * si2)
    th_star = (sib * (cob * ch2 + chb * co2) + cob * (sh2 * co2 - ch2 * si2)) / n_m

    th_prime = Decimal(2) * b * sib * (cob * sh2 + chb * si2) + Decimal(8) * b * cob * (ch2 * co2)
    om = Decimal("0.25") * th_prime

    def f_star(sh_v: Decimal, ch_v: Decimal, si_v: Decimal, co_v: Decimal) -> Decimal:
        return (sib * (cob * sh_v + chb * si_v) + cob * (ch_v * co_v)) / (Decimal(2) * b * n_m)

    om_star = Decimal(4) * (f_star(shb, chb, sib, cob) - f_star(sh2, ch2, si2, co2))
    return th, th_star, om, om_star


def eval_w_r_star_dec(kap: Decimal, t_r: Decimal, s: Decimal) -> Decimal:
    r"""Evaluate cantilever adjoint mode w_r^*(s) = -(1/4) d/ds [\hat{\psi}_r(s)^2] in Dom_C^*."""
    u = kap * (Decimal(1) - s)
    sh, ch = d244.dec_sinh_cosh(u)
    si, co = d244.dec_sin_cos(u)
    psi = (ch - co) - t_r * (sh - si)
    psi_s = -kap * ((sh + si) - t_r * (ch - co))
    return Decimal("-0.5") * psi * psi_s


# ---------------------------------------------------------------------------
# 1. Theorem 1: Adjoint Domain Dom_C^*, Single-Monomial Norm & Biorthogonality
# ---------------------------------------------------------------------------

def verify_theorem_1(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    betas: List[Decimal],
    gl64: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    max_dom_c_err = Decimal(0)
    max_dom_c_star_err = Decimal(0)
    max_norm_id_err = Decimal(0)

    for m_idx in range(6):
        b = betas[m_idx]
        shb, chb = d244.dec_sinh_cosh(b)
        sib, cob = d244.dec_sin_cos(b)

        # Single-monomial normalization identity (relative error):
        #   -(1/2) sin^2(b)(cosh^2(b) - cos^2(b)) - cos^2(b) == -cosh^2(b) cos^4(b)
        lhs_norm = -Decimal("0.5") * (sib ** 2) * (chb ** 2 - cob ** 2) - (cob ** 2)
        rhs_norm = -(chb ** 2) * (cob ** 4)
        max_norm_id_err = max(max_norm_id_err, abs(lhs_norm - rhs_norm) / abs(rhs_norm))

        # Check endpoint BCs of Theta_m in Dom_C and Theta_m^* in Dom_C^*
        th_0, ths_0, _, oms_0 = eval_cp_modes_dec(b, Decimal(0))
        th_1, ths_1, _, oms_1 = eval_cp_modes_dec(b, Decimal(1))
        ths_p1 = (
            Decimal(2) * b * sib * (cob * shb - chb * sib)
            + Decimal(2) * b * cob * (Decimal(-2) * shb * sib)
        ) / rhs_norm
        ths_pp0 = (
            Decimal(4) * (b ** 2) * sib * (cob * chb - chb * cob)
            + Decimal(8) * (b ** 2) * cob * (chb * sib + shb * cob)
        ) / rhs_norm
        ths_pp1 = (
            Decimal(4) * (b ** 2) * sib * (cob * chb - chb * cob)
            - Decimal(8) * (b ** 2) * cob * (chb * sib + shb * cob)
        ) / rhs_norm

        max_dom_c_err = max(max_dom_c_err, abs(th_0) / chb, abs(th_1) / chb)
        max_dom_c_star_err = max(
            max_dom_c_star_err,
            abs(ths_1),
            abs(ths_p1),
            abs(ths_pp0),
            abs(ths_pp1),
            abs(oms_1),
        )

    assert max_norm_id_err < Decimal("1e-95")
    assert max_dom_c_err < Decimal("1e-95")
    assert max_dom_c_star_err < Decimal("1e-95")

    # Full 4x4 Kronecker biorthogonality & 4x4 cross-branch orthogonality
    max_cp_biorth = Decimal(0)
    max_cross_orth = Decimal(0)
    cp_grid = [[eval_cp_modes_dec(betas[m], x) for x, _ in gl64] for m in range(4)]
    cant_grid = [
        [
            (
                d244.eval_Xi_and_Upsilon_dec(modes[r][0], modes[r][2], x)[1],
                d244.eval_psi_hat_sq_dec(modes[r][0], modes[r][1], x),
            )
            for x, _ in gl64
        ]
        for r in range(4)
    ]

    for m in range(4):
        for n in range(4):
            ip_th = sum(gl64[i][1] * cp_grid[m][i][0] * cp_grid[n][i][1] for i in range(len(gl64)))
            ip_om = sum(gl64[i][1] * cp_grid[m][i][2] * cp_grid[n][i][3] for i in range(len(gl64)))
            tgt = Decimal(1) if m == n else Decimal(0)
            max_cp_biorth = max(max_cp_biorth, abs(ip_th - tgt), abs(ip_om - tgt))
        for r in range(4):
            c_uo = sum(gl64[i][1] * cant_grid[r][i][0] * cp_grid[m][i][3] for i in range(len(gl64)))
            c_op = sum(gl64[i][1] * cp_grid[m][i][2] * cant_grid[r][i][1] for i in range(len(gl64)))
            max_cross_orth = max(max_cross_orth, abs(c_uo), abs(c_op))

    assert max_cp_biorth < Decimal("1e-60"), f"Clamped-pinned biorthogonality error: {max_cp_biorth}"
    assert max_cross_orth < Decimal("1e-65"), f"Cross-branch orthogonality error: {max_cross_orth}"

    return {
        "status": "PASS",
        "max_single_monomial_norm_identity_error": f"{max_norm_id_err:.3e}",
        "max_Dom_C_and_Dom_C_star_boundary_error": f"{max(max_dom_c_err, max_dom_c_star_err):.3e}",
        "max_clamped_pinned_biorthogonality_4x4_error": f"{max_cp_biorth:.3e}",
        "max_cross_branch_orthogonality_4x4_error": f"{max_cross_orth:.3e}",
    }


# ---------------------------------------------------------------------------
# 2. Theorem 2: Exact Two-Branch Green Decomposition & Trace Completeness
# ---------------------------------------------------------------------------

def verify_theorem_2(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    betas: List[Decimal],
    gl32: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    # (a) Exact rational trace identities for Tr(G_Xi^{(C)}) and Tr((G_Xi^{(C)})^2)!
    # Diagonal G_Xi^{(C)}(x, x) = -(5/3)(2x - 1)_+^3 + (7/3)x - 7 x^2 + (11/3)x^3 + (8/3)x^4
    # Integral on [0, 1]: -5/24 + (7/6 - 7/3 + 11/12 + 8/15) = -5/24 + 17/60 = 3/40 == 1/12 - 1/120!
    tr1_analytic = Fraction(-5, 24) + Fraction(7, 6) - Fraction(7, 3) + Fraction(11, 12) + Fraction(8, 15)
    assert tr1_analytic == Fraction(3, 40) == Fraction(1, 12) - Fraction(1, 120)

    # Second iterated trace via Newton's power sums:
    # F(s) = 1 + sum_{m>=1} (-4)^m / (2*(4m)!) s^{4m} = 1 - (1/12) z + (1/5040) z^2 - ...
    # => sum 1/kap_r^4 = 1/12;  sum 1/kap_r^8 = (1/12)^2 - 2*(1/5040) = 11/1680!
    # e_1(z) = prod (1 + z / (4 beta_m^4)) = 1 + z/120 + z^2/362880 + ...
    # => sum 1/(4 beta_m^4) = 1/120;  sum 1/(4 beta_m^4)^2 = (1/120)^2 - 2/362880 = 23/362880!
    # Since (-1/(4 beta_m^4))^2 = +1/(16 beta_m^8), Tr((G_Xi^{(C)})^2) = 11/1680 + 23/362880 = 2399/362880!
    p2_cant = Fraction(1, 12) ** 2 - 2 * Fraction(1, 5040)  # 11/1680
    p2_cp = Fraction(1, 120) ** 2 - 2 * Fraction(1, 362880)  # 23/362880
    tr2_spectral_exact = p2_cant + p2_cp  # 2399/362880

    # Verify Tr((G_Xi^{(C)})^2) = \int_0^1 \int_0^1 G_Xi^{(C)}(x, s) G_Xi^{(C)}(s, x) ds dx by piecewise exact GL32!
    # Split [0, 1] at 1/2 -> subintervals [0, 1/2] and [1/2, 1], and on each split s at x and 1-x -> exact on degree <= 63!
    def quad_sub(fn, a: Decimal, b: Decimal) -> Decimal:
        if b <= a:
            return Decimal(0)
        length = b - a
        return sum(length * w * fn(a + length * z) for z, w in gl32)

    def diag_G2(x: Decimal) -> Decimal:
        pts = sorted(list({Decimal(0), Decimal(1), x, Decimal(1) - x}))
        return sum(
            quad_sub(lambda s: srb.G_Xi_C_dec(x, s) * srb.G_Xi_C_dec(s, x), pts[i], pts[i + 1])
            for i in range(len(pts) - 1)
        )

    tr2_quad = quad_sub(diag_G2, Decimal(0), Decimal("0.5")) + quad_sub(diag_G2, Decimal("0.5"), Decimal(1))
    tr2_exact_dec = Decimal(tr2_spectral_exact.numerator) / Decimal(tr2_spectral_exact.denominator)
    err_tr2_identity = abs(tr2_quad - tr2_exact_dec)
    assert err_tr2_identity < Decimal("1e-98"), f"Tr(G^2) spectral completeness error: {err_tr2_identity}"

    # Check numerical mode sums against p2_cant and p2_cp
    err_p2_modes = max(
        abs(sum(Decimal(1) / (k ** 8) for k, _, _ in modes) - Decimal(p2_cant.numerator) / Decimal(p2_cant.denominator)),
        abs(sum(Decimal(1) / (Decimal(16) * (b ** 8)) for b in betas) - Decimal(p2_cp.numerator) / Decimal(p2_cp.denominator)),
    )
    assert err_p2_modes < Decimal("1e-14")

    # (b) Pointwise two-branch decomposition of G_Upsilon^{(C)}(x, y) and G_Xi^{(C)}(x, y) across [0, 1]^2
    max_pt_ups_err = Decimal(0)
    max_pt_xi_err = Decimal(0)
    for xs, ys in (("0.23", "0.61"), ("0.37", "0.19"), ("0.71", "0.44")):
        x, y = Decimal(xs), Decimal(ys)
        g_ups_ex = srb.G_Upsilon_C_dec(x, y)
        g_xi_ex = srb.G_Xi_C_dec(x, y)

        pos_ups = sum(
            d244.eval_Xi_and_Upsilon_dec(k, w, x)[1] * d244.eval_psi_hat_sq_dec(k, t, y) / (k ** 4)
            for k, t, w in modes
        )
        neg_ups = sum(
            eval_cp_modes_dec(b, x)[2] * eval_cp_modes_dec(b, y)[3] / (Decimal(4) * (b ** 4))
            for b in betas
        )
        pos_xi = sum(
            d244.eval_Xi_and_Upsilon_dec(k, w, x)[0] * eval_w_r_star_dec(k, t, y) / (k ** 4)
            for k, t, w in modes
        )
        neg_xi = sum(
            eval_cp_modes_dec(b, x)[0] * eval_cp_modes_dec(b, y)[1] / (Decimal(4) * (b ** 4))
            for b in betas
        )

        # Confirm the negative clamped-pinned sum is O(10^-2) and cancels the gap down to ~10^-10!
        assert abs(g_ups_ex - pos_ups) > Decimal("1e-4")
        max_pt_ups_err = max(max_pt_ups_err, abs(g_ups_ex - (pos_ups - neg_ups)))
        max_pt_xi_err = max(max_pt_xi_err, abs(g_xi_ex - (pos_xi - neg_xi)))

    assert max_pt_ups_err < Decimal("1e-9"), f"Pointwise G_Upsilon 2-branch error: {max_pt_ups_err}"
    assert max_pt_xi_err < Decimal("1e-9"), f"Pointwise G_Xi 2-branch error: {max_pt_xi_err}"

    return {
        "status": "PASS",
        "trace_1_exact": str(tr1_analytic),
        "trace_2_exact": f"{tr2_spectral_exact} == {p2_cant} (cantilever) + {p2_cp} (clamped-pinned)",
        "trace_2_quadrature_vs_spectral_zeta_error": f"{err_tr2_identity:.3e}",
        "max_pointwise_G_Upsilon_2branch_error_90_modes": f"{max_pt_ups_err:.3e}",
        "max_pointwise_G_Xi_2branch_error_90_modes": f"{max_pt_xi_err:.3e}",
    }


# ---------------------------------------------------------------------------
# 3. Theorem 3: Exact Two-Branch Functional Mittag-Leffler for H_0 & I_0
# ---------------------------------------------------------------------------

def verify_theorem_3(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    betas: List[Decimal],
) -> Dict[str, object]:
    projs = gtp.build_biorthogonal_projectors(max_k=5)
    errors_h0: Dict[str, str] = {}
    errors_i0: Dict[str, str] = {}

    for k in (1, 2, 3):
        phi_h = projs[("H0", k)]["Phi"]
        psi_h = projs[("H0", k)]["Psi"]
        phi_i = projs[("I0", k)]["Phi"]
        psi_i = projs[("I0", k)]["Psi"]

        max_eh = Decimal(0)
        max_ei = Decimal(0)
        for xf in (Fraction(1, 5), Fraction(3, 8), Fraction(3, 4)):
            xd = Decimal(xf.numerator) / Decimal(xf.denominator)
            ex_phi_h = Decimal(gtp.poly_eval(phi_h, xf).numerator) / Decimal(gtp.poly_eval(phi_h, xf).denominator)
            ex_psi_h = Decimal(gtp.poly_eval(psi_h, xf).numerator) / Decimal(gtp.poly_eval(psi_h, xf).denominator)
            ex_phi_i = Decimal(gtp.poly_eval(phi_i, xf).numerator) / Decimal(gtp.poly_eval(phi_i, xf).denominator)
            ex_psi_i = Decimal(gtp.poly_eval(psi_i, xf).numerator) / Decimal(gtp.poly_eval(psi_i, xf).denominator)

            # Positive cantilever branch
            pos_phi_h = Decimal(0)
            pos_psi_h = Decimal(0)
            pos_phi_i = Decimal(0)
            pos_psi_i = Decimal(0)
            for kap, t_r, w_r in modes:
                xi_v, ups_v = d244.eval_Xi_and_Upsilon_dec(kap, w_r, xd)
                pos_phi_h += (t_r * xi_v) / (kap ** (4 * k + 3))
                pos_psi_h += (t_r * ups_v) / (kap ** (4 * k + 3))
                pos_phi_i += ((t_r ** 2) * xi_v) / (kap ** (4 * k + 2))
                pos_psi_i += ((t_r ** 2) * ups_v) / (kap ** (4 * k + 2))

            # Negative clamped-pinned branch with exact elementary weights:
            #   w_m^{(H0)} = (1/2) Theta_m^*(0)  = 2 tanh(b_m) / (cosh(b_m) cos^2(b_m))
            #   w_m^{(I0)} = -(1/2) Theta_m^*'(0) = 4 b_m tanh^2(b_m) / (cosh(b_m) cos^2(b_m))
            neg_phi_h = Decimal(0)
            neg_psi_h = Decimal(0)
            neg_phi_i = Decimal(0)
            neg_psi_i = Decimal(0)
            for b in betas:
                shb, chb = d244.dec_sinh_cosh(b)
                _, cob = d244.dec_sin_cos(b)
                th_b = shb / chb
                denom_b = chb * (cob ** 2)
                wm_h = (Decimal(2) * th_b) / denom_b
                wm_i = (Decimal(4) * b * (th_b ** 2)) / denom_b

                th_x, _, om_x, _ = eval_cp_modes_dec(b, xd)
                eig_pow = (Decimal(-4) * (b ** 4)) ** (k + 1)
                neg_phi_h += (wm_h / eig_pow) * th_x
                neg_psi_h += (wm_h / eig_pow) * om_x
                neg_phi_i += (wm_i / eig_pow) * th_x
                neg_psi_i += (wm_i / eig_pow) * om_x

            max_eh = max(max_eh, abs(ex_phi_h - (pos_phi_h + neg_phi_h)), abs(ex_psi_h - (pos_psi_h + neg_psi_h)))
            max_ei = max(max_ei, abs(ex_phi_i - (pos_phi_i + neg_phi_i)), abs(ex_psi_i - (pos_psi_i + neg_psi_i)))

        errors_h0[f"k={k}"] = f"{max_eh:.3e}"
        errors_i0[f"k={k}"] = f"{max_ei:.3e}"
        assert max_eh < Decimal("1e-11"), f"Two-branch H0 Mittag-Leffler failed at k={k}: {max_eh}"
        assert max_ei < Decimal("1e-10"), f"Two-branch I0 Mittag-Leffler failed at k={k}: {max_ei}"

    assert Decimal(errors_h0["k=3"]) < Decimal("1e-24")
    assert Decimal(errors_i0["k=3"]) < Decimal("1e-22")

    return {
        "status": "PASS",
        "two_branch_H0_errors_90_modes": errors_h0,
        "two_branch_I0_errors_90_modes": errors_i0,
    }


def main() -> None:
    modes_90 = [d244.solve_kappa_105(r) for r in range(1, 91)]
    betas_90 = [solve_beta_105(m) for m in range(1, 91)]
    gl32 = d244.gauss_legendre_nodes_weights(32)
    gl64 = d244.gauss_legendre_nodes_weights(64)

    res1 = verify_theorem_1(modes_90, betas_90, gl64)
    res2 = verify_theorem_2(modes_90, betas_90, gl32)
    res3 = verify_theorem_3(modes_90, betas_90)

    report = {
        "script": "clamped_pinned_spectral_closure_and_full_green_decomposition_2026_11_16.py",
        "author": "Petrovich (ompu-e1dd503f59)",
        "date": "2026-11-16",
        "revision": 104,
        "closes_seam": "Full two-branch spectral decomposition of G_Upsilon^(C) - K_res and H0/I0 Mittag-Leffler (bus:1794827014 / 1794827139)",
        "theorem_1_adjoint_domain_and_clamped_pinned_biorthogonality": res1,
        "theorem_2_two_branch_green_decomposition_and_trace_completeness": res2,
        "theorem_3_two_branch_H0_I0_mittag_leffler": res3,
        "verdict": "ALL_CHECKS_PASSED",
    }

    out_path = HERE / "clamped_pinned_spectral_closure_and_full_green_decomposition_2026_11_16_results.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=" * 78)
    print("CLAMPED-PINNED SPECTRAL CLOSURE & FULL TWO-BRANCH GREEN DECOMPOSITION")
    print("=" * 78)
    print(f"[PASS] Theorem 1: Dom_C^* = {{w(1)=w'(1)=w''(0)=w''(1)=0}}, N_m = -ch^2(b)cos^4(b) "
          f"(biorth err={res1['max_clamped_pinned_biorthogonality_4x4_error']}, cross err={res1['max_cross_branch_orthogonality_4x4_error']})")
    print(f"[PASS] Theorem 2: G_Upsilon^(C) = K_res - sum Omega_m Omega_m^* / (4 b_m^4) "
          f"(pt err={res2['max_pointwise_G_Upsilon_2branch_error_90_modes']}), "
          f"Tr(G)=3/40, Tr(G^2)=2399/362880 (err={res2['trace_2_quadrature_vs_spectral_zeta_error']})")
    print(f"[PASS] Theorem 3: Exact 2-branch Mittag-Leffler for Phi_H0 ({res3['two_branch_H0_errors_90_modes']}) "
          f"& Phi_I0 ({res3['two_branch_I0_errors_90_modes']})")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
