#!/usr/bin/env python3
r"""
quartet_pure_beam_duals_and_ab_cross_verification_2026_11_17.py
===============================================================
Continuity Rev 105 — Midday Unification & Cross-Verification Module (2026-11-17)
Author: Petrovich (ompu-e1dd503f59)

Simultaneously closes BOTH open items of Revision 105:
  (A) Phi-Hausmaster's declared loss in `bus:1794909763_874280_aa8e5e`:
      direct side-by-side programmatic A <-> B cross-verification between Lane A (`seq 247`,
      `complete_four_domain_quartet_and_dual_mittag_leffler_2026_11_17.py`, sha256: 9f8f074e...)
      and Lane B (`seq 248`, `complete_quartet_adjoint_domains_and_two_branch_green_2026_11_17.py`,
      sha256: 38b7fefc...);
  (B) Lane B's open epistemic seam `[=~` in `bus:1794909529_661867_8c0bd4` (§2):
      exact transfer of the negative-branch stereo pairs {\Theta_m^{(\alpha)}, \Theta_m^{(\alpha)*}}
      (\alpha = 0, 2, 3) into closed-form pure-beam biorthogonal pairs
      {\Omega_m^{(\alpha)}(x), \Omega_m^{(\alpha)*}(y)}, complete two-branch pure-beam Green's
      decompositions G_\Upsilon^{(\alpha)}(x, y), and functional Mittag-Leffler ladders across
      all four quartet domains Dom_0 (Euler-Krylov), Dom_C (dilated clamped-sliding,
      \tanh\beta + \tan\beta = 0, \zeta_{cs}(4) = 1/120), Dom_B (simply-supported), and
      Dom_A (dilated clamped-pinned, \tanh\gamma - \tan\gamma = 0, \zeta_{cp}(4) = 1/840).

Proves and verifies in exact `Fraction` arithmetic and 105-digit `Decimal` quadrature
(`python3 -I -B -W error`):

  1. THEOREM 1 (Direct Side-by-Side A <-> B Equivalence Across Revision 105):
     - Exact `Fraction` identity `lane_a.apply_G_Xi_C_poly(x^n) == lane_b.apply_G_Xi_C_poly(x^n)`
       and `lane_a.apply_G_Xi_0_poly(x^n) == G_Xi^{(C)}(x^n) + (2/3) x <w_0^*, x^n>` for n = 0..10.
     - 105-digit pointwise agreement `< 1e-103` between `lane_a.G_Xi_0_dec(x, s)` (explicit
       piecewise-cubic formula) and `lane_b.G_Xi_alpha_dec(0, x, s)` across the X-shaped light-cone
       {s = x} U {s = 1 - x}, plus exact `Fraction` equivalence between Lane A's generating law
       <w_0^*, (G_\Xi^{(C)})^k(x)> == -(3/2)[z^{k+1}](e_0/e_1), Lane B's derivative law
       e_0(z)/e_1(z) == 1 + 4z e_1'(z)/e_1(z), the root-free dilated clamped-sliding zetas
       \zeta_{cs}(4k) = (1/120, 29/453600, 331/648648000, ...), and the Dom_0 Newton traces
       Tr((G_\Xi^{(0)})^n) = (1/24, 83/10080, 4591/9979200).

  2. THEOREM 2 (Closed-Form Pure-Beam Quartet Duals {\Omega_m^{(\alpha)}, \Omega_m^{(\alpha)*}},
     Positive-Branch Shifts v_r^{(\alpha)*}, and Complete Two-Branch Pure-Beam Green Kernels):
     - Because D_x R = -R D_x flips T^{-1} = (3/8)I + (5/8)R into (3/8)I - (5/8)R, the quarter-
       derivative / antiderivative intertwining
           \Omega_m^{(\alpha)}(x) := \frac{1}{4} \partial_x \Theta_m^{(\alpha)}(x),
           \Omega_m^{(\alpha)*}(y) := 4 \int_y^1 \Theta_m^{(\alpha)*}(s) ds
       annihilates the boundary term [\Theta_m^{(\alpha)}(y) \int_y^1 \Theta_n^{(\alpha)*}(s) ds]_0^1
       for ALL four \alpha in {0, 1, 2, 3} (including \alpha = 0 where \Theta_m^{(0)}(1) != 0, since
       the upper integral limit vanishes at y = 1 while \Theta_m^{(0)}(0) = 0 at y = 0!), preserving
       exact Kronecker biorthogonality <\Omega_m^{(\alpha)}, \Omega_n^{(\alpha)*}> == \delta_{m,n}.
     - Moreover, since \int_0^1 (R f)(s) ds == \int_0^1 f(s) ds, every negative-branch adjoint mode
       for \alpha in {0, 2, 3} has zero total mass \int_0^1 \Theta_m^{(\alpha)*}(s) ds == 0, so
       \Omega_m^{(\alpha)*}(0) = \Omega_m^{(\alpha)*}(1) = 0 in elementary closed form (with t = 2\mu(y - 1/2)):
         * \alpha = 0 (\mu_m = (2m-1)\pi/2, \sigma_m = (-1)^{m-1}):
               \Omega_m^{(0)*}(y) = \frac{8}{\mu_m \cosh^2\mu_m}
                   [ \sinh t - \sigma_m \sinh\mu_m \sin t + \sigma_m \cosh t \cos t ];
         * \alpha = 2 (\mu_m = m\pi, \sigma_m = (-1)^m):
               \Omega_m^{(2)*}(y) = \frac{-4 \sigma_m}{\mu_m \sinh\mu_m (\cosh^2\mu_m + 1)}
                   [ -\sigma_m \cosh\mu_m - \sinh\mu_m \sin t + \cosh t \cos t ];
         * \alpha = 3 (\tanh\gamma_m - \tan\gamma_m = 0, clamped-pinned):
               \Omega_m^{(3)*}(y) = \frac{2}{\gamma_m \sinh^2\gamma_m \cos^4\gamma_m}
                   [ \cos^2\gamma_m \cosh\gamma_m - \sin\gamma_m (\cos\gamma_m \sinh t - \cosh\gamma_m \sin t)
                     - \cos\gamma_m \cosh t \cos t ].
     - Integrating Lane B's H_r^*(s) via E_0' = E_3 and d/ds E_0(\kappa_r(s + i(1-s))) =
       \kappa_r(1 - i) E_3(\kappa_r(s + i(1-s))) cancels \kappa_r^4 identically:
           \Lambda_r^*(y) := E_0(\kappa_r) - E_0(\kappa_r(2y - 1)) - 2 Im[E_0(\kappa_r(y + i(1 - y)))],
           v_r^{(0)*}(y) = \hat{\psi}_r(y)^2 - \Lambda_r^*(y) / E_0(\kappa_r),
           v_r^{(2)*}(y) = \hat{\psi}_r(y)^2 + t_r^2 \Lambda_r^*(y) / E_2(\kappa_r),
           v_r^{(3)*}(y) = \hat{\psi}_r(y)^2 + 2 \Lambda_r^*(y) / E_0(\kappa_r),
       yielding exact zero-remainder two-branch pure-beam Green's decompositions across [0, 1]^2:
           G_\Upsilon^{(\alpha)}(x, y) == \sum_{r=1}^\infty \frac{\Upsilon_r(x) v_r^{(\alpha)*}(y)}{\kappa_r^4}
                                         - \sum_{m=1}^\infty \frac{\Omega_m^{(\alpha)}(x) \Omega_m^{(\alpha)*}(y)}{|z_m^{(\alpha)}|},
       with exact diagonal Beta-integral traces Tr(G_\Upsilon^{(\alpha)}) == Tr(G_\Xi^{(\alpha)}) =
       {1/24, 3/40, 29/360, 23/280}. (In particular, at \alpha = 0 the constant \Psi_{0,0}(x) = 1/4
       kills the nilpotent \lambda-gauge of G_\Xi^{(0,\lambda)} and becomes the non-nilpotent rank-1
       shift -(2/3) y(1-y)^3 carrying the -1/30 trace shift 3/40 - 1/30 = 1/24.)

  3. THEOREM 3 (Universal Endpoint-Curvature Pairing Law <u, L_\Xi w> == (1/8) B_1(u) w''(1),
     Sherman-Morrison Pole-Exchange Identities, and Functional Mittag-Leffler Ladders on Dom_0, Dom_B, Dom_A):
     - For every \alpha in {0, 2, 3}, every u in ker(D^4) with u(0)=0 and B_j(u)=0 (\forall j notin {1, \alpha}),
       and every w in Dom_\alpha^*, 4-fold integration by parts collapses to a single endpoint curvature:
           <u, L_\Xi w> == \frac{1}{8} B_1(u) w''(1)!
     - Applying this to the canonical seeds \phi_0^{(0)}(x) = x, \phi_0^{(2)}(x) = \Phi_{I_0,0}(x) = x - x^2,
       \phi_0^{(3)}(x) = \Phi_{H_0,0}(x) = (7x - 15x^2 + 8x^3)/6 yields Sherman-Morrison pole-exchange laws
           (I - z G_\Xi^{(0)})^{-1}(x)          == [e_1(z) / e_0(z)] (I - z G_\Xi^{(C)})^{-1}(x),
           (I - z G_\Xi^{(B)})^{-1}(\Phi_{I_0,0}) == [e_1(z) / (2 e_2(z))] \tilde{\Phi}_{I_0}(x; z),
           (I - z G_\Xi^{(A)})^{-1}(\Phi_{H_0,0}) == [e_1(z) / (6 e_3(z))] \tilde{\Phi}_{H_0}(x; z),
       and elementary closed-form Mittag-Leffler weights (w_{r,+}^{(\alpha)}, w_{m,-}^{(\alpha)}) for
       \Phi_k^{(\alpha)} = (G_\Xi^{(\alpha)})^k \phi_0^{(\alpha)} and \Psi_k^{(\alpha)} = (G_\Upsilon^{(\alpha)})^k \psi_0^{(\alpha)}:
         * \alpha = 0 (Dom_0): w_{r,+}^{(0)} = E_1(\kappa_r) / (4 \kappa_r E_0(\kappa_r)),
                               w_{m,-}^{(0)} = 1 / (\mu_m^2 \cosh\mu_m)   (\mu_m = (2m-1)\pi/2);
         * \alpha = 2 (Dom_B): w_{r,+}^{(2)} = t_r^2 E_1(\kappa_r) / (2 \kappa_r E_2(\kappa_r)),
                               w_{m,-}^{(2)} = 1 / (\mu_m^2 (\cosh^2\mu_m + 1))   (\mu_m = m\pi);
         * \alpha = 3 (Dom_A): w_{r,+}^{(3)} = E_1(\kappa_r) / (6 \kappa_r E_0(\kappa_r)),
                               w_{m,-}^{(3)} = 1 / (6 \gamma_m^2 \sinh\gamma_m \cos^2\gamma_m).
"""

from __future__ import annotations

import hashlib
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

import complete_four_domain_quartet_and_dual_mittag_leffler_2026_11_17 as lane_a
import complete_quartet_adjoint_domains_and_two_branch_green_2026_11_17 as lane_b

getcontext().prec = 105
PI_DEC = lane_b.PI_DEC
d244 = lane_b.fq.d244
gtp = lane_b.gtp
srb = lane_b.fq.srb
fq = lane_b.fq
cp = lane_b.cp

EXPECTED_HASHES = {
    "lane_a_py": "9f8f074ec633bbdb866f7952d1a1b32fe2e80fdbf96a08869d3cb0586929c2f0",
    "lane_a_json": "677d91fb93205d9ec9cc9cbc38b8cd62f7cbed45a3a939c790fc6c427087dd0d",
    "lane_b_py": "38b7fefc8f565ecdfde26a5532f08207c20269c8d932334db14f24d524d50d74",
    "lane_b_json": "8bf724ea3548deef098419cc401e8fb4b861f03dea5cd8b8d697b20802ee0c85",
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# 1. Theorem 1: Direct Side-by-Side A <-> B Cross-Verification
# ---------------------------------------------------------------------------

def verify_theorem_1_ab_cross(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    betas: List[Decimal],
    gl64: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    # (a) Verify exact SHA-256 hashes of Lane A and Lane B carriers & result JSONs
    p_a_py = HERE / "complete_four_domain_quartet_and_dual_mittag_leffler_2026_11_17.py"
    p_a_js = HERE / "complete_four_domain_quartet_and_dual_mittag_leffler_2026_11_17_results.json"
    p_b_py = HERE / "complete_quartet_adjoint_domains_and_two_branch_green_2026_11_17.py"
    p_b_js = HERE / "complete_quartet_adjoint_domains_and_two_branch_green_2026_11_17_results.json"

    actual_hashes = {
        "lane_a_py": sha256_file(p_a_py),
        "lane_a_json": sha256_file(p_a_js),
        "lane_b_py": sha256_file(p_b_py),
        "lane_b_json": sha256_file(p_b_js),
    }
    assert actual_hashes == EXPECTED_HASHES, f"Hash mismatch: {actual_hashes} vs {EXPECTED_HASHES}"

    # (b) Exact polynomial operator equivalence on monomials x^0 .. x^10
    w0_star = [Fraction(1), Fraction(-6), Fraction(9), Fraction(-4)]
    phi_0_0 = [Fraction(0), Fraction(1)]
    for n in range(11):
        xn = [Fraction(0)] * (n + 1)
        xn[n] = Fraction(1)
        u_c_a = lane_a.apply_G_Xi_C_poly(xn)
        u_c_b = lane_b.apply_G_Xi_C_poly(xn)
        assert u_c_a == u_c_b, f"A vs B G_Xi^(C) polynomial mismatch at n={n}"

        u_0_a = lane_a.apply_G_Xi_0_poly(xn)
        ip_w0 = fq.poly_inner_product(w0_star, xn)
        u_0_b = lane_a.strip_trailing_zeros(
            gtp.poly_add(u_c_b, phi_0_0, Fraction(1), Fraction(2, 3) * ip_w0)
        )
        assert u_0_a == u_0_b, f"A vs B G_Xi^(0) polynomial mismatch at n={n}"

    # (c) 105-digit pointwise equivalence of G_Xi^{(0)}(x, s) across [0, 1]^2 & light-cone
    grid_pts = [Decimal(s) for s in ("0.07", "0.19", "0.31", "0.50", "0.69", "0.81", "0.93")]
    max_g0_ab_diff = Decimal(0)
    for x in grid_pts:
        for s in grid_pts:
            va = lane_a.G_Xi_0_dec(x, s)
            vb = lane_b.G_Xi_alpha_dec(0, x, s)
            max_g0_ab_diff = max(max_g0_ab_diff, abs(va - vb))
    assert max_g0_ab_diff < Decimal("1e-103"), f"Pointwise A vs B G_Xi^(0) diff: {max_g0_ab_diff}"

    # (d) Exact Fraction bridge between Lane A's <w_0^*, G_C^k(x)> = -(3/2)[z^{k+1}](e_0/e_1),
    #     Lane B's e_0/e_1 = 1 + 4z e_1'/e_1, dilated clamped-sliding zetas, and Dom_0 Newton traces
    K = 7
    e0 = [Fraction(1, math.factorial(4 * m)) for m in range(K + 1)]
    e1 = [Fraction(1, math.factorial(4 * m + 1)) for m in range(K + 1)]
    f_s = [Fraction(1)] + [Fraction((-4) ** m, 2 * math.factorial(4 * m)) for m in range(1, K + 1)]
    ratio_e0_e1 = d244.series_mul(e0, d244.series_inv(e1))
    e1_neg = [((-1) ** m) * e1[m] for m in range(K + 1)]
    zeta_cs = fq.fredholm_traces_from_det(e1_neg)

    cur_x = phi_0_0[:]
    for k in range(1, K + 1):
        ip_a = lane_a.poly_inner(w0_star, cur_x)
        z_from_a = Fraction((-1) ** k, 6) * ip_a
        z_from_ratio = Fraction((-1) ** (k - 1), 4) * ratio_e0_e1[k]
        assert z_from_a == z_from_ratio == zeta_cs[k - 1]
        cur_x = lane_a.apply_G_Xi_C_poly(cur_x)

    det_0 = d244.series_mul(e0, f_s)
    traces_0 = fq.fredholm_traces_from_det(det_0)
    assert traces_0[0] == Fraction(1, 24)
    assert traces_0[1] == Fraction(83, 10080)
    assert traces_0[2] == Fraction(4591, 9979200)

    # (e) Cross-check Lane A's closed-form Q^{dual}_{4k}(y) against Lane B's modes
    q_dual_a = lane_a.build_closed_form_Q_dual(max_k=4)
    q12 = q_dual_a[3]
    q12_vals = [
        sum(Decimal(c.numerator) / Decimal(c.denominator) * (z ** i) for i, c in enumerate(q12))
        for z, _ in gl64
    ]
    max_q_cant_orth = Decimal(0)
    max_q_cs_pair_err = Decimal(0)
    for r_idx in range(4):
        kap, _, wr = modes[r_idx]
        ip_cant = sum(
            gl64[i][1] * q12_vals[i] * d244.eval_Xi_and_Upsilon_dec(kap, wr, gl64[i][0])[1]
            for i in range(64)
        )
        max_q_cant_orth = max(max_q_cant_orth, abs(ip_cant))
    for m_idx in range(4):
        b = betas[m_idx]
        _, chb = d244.dec_sinh_cosh(b)
        _, cob = d244.dec_sin_cos(b)
        ip_cs = sum(
            gl64[i][1] * q12_vals[i] * cp.eval_cp_modes_dec(b, gl64[i][0])[2]
            for i in range(64)
        )
        c_m_dual = Decimal(3) * b * (cob ** 2) * chb
        expected_ip = c_m_dual / ((Decimal(-4) * (b ** 4)) ** 3)
        max_q_cs_pair_err = max(max_q_cs_pair_err, abs(ip_cs - expected_ip))

    assert max_q_cant_orth < Decimal("1e-95"), f"Q_dual_12 cantilever orthogonality error: {max_q_cant_orth}"
    assert max_q_cs_pair_err < Decimal("1e-90"), f"Q_dual_12 clamped-sliding pairing error: {max_q_cs_pair_err}"

    return {
        "status": "PASS",
        "carrier_and_json_hashes_verified": actual_hashes,
        "exact_poly_operator_match_deg_0_to_10": True,
        "max_pointwise_G_Xi_0_ab_diff": f"{max_g0_ab_diff:.3e}",
        "dom_0_exact_traces_n1_to_3": [str(traces_0[0]), str(traces_0[1]), str(traces_0[2])],
        "dilated_clamped_sliding_zeta_k1_to_4": [str(z) for z in zeta_cs[:4]],
        "max_Q_dual_12_cantilever_orth_error": f"{max_q_cant_orth:.3e}",
        "max_Q_dual_12_clamped_sliding_pairing_error": f"{max_q_cs_pair_err:.3e}",
    }


# ---------------------------------------------------------------------------
# 2. Pure-Beam Quartet Duals {\Omega_m^{(\alpha)}, \Omega_m^{(\alpha)*}},
#    Positive Shifts v_r^{(\alpha)*}, and Two-Branch Pure-Beam Green Kernels
# ---------------------------------------------------------------------------

def eval_pure_beam_neg_pair_dec(
    alpha: int,
    m: int,
    x: Decimal,
    root_val: Decimal | None = None,
) -> Tuple[Decimal, Decimal, Decimal]:
    r"""
    Return (\Omega_m^{(\alpha)}(x), \Omega_m^{(\alpha)*}(x), |z_m^{(\alpha)}|)
    for \alpha in {0, 1, 2, 3}, satisfying <\Omega_m^{(\alpha)}, \Omega_n^{(\alpha)*}> == \delta_{m,n}.
    """
    t = Decimal(2) * (x - Decimal("0.5"))
    if alpha == 0:
        mu = Decimal(2 * m - 1) * PI_DEC / Decimal(2)
        shm, chm = d244.dec_sinh_cosh(mu)
        sh2, ch2 = d244.dec_sinh_cosh(mu * t)
        si2, co2 = d244.dec_sin_cos(mu * t)
        sgn = Decimal(1) if (m % 2 == 1) else Decimal(-1)
        om = Decimal("0.5") * mu * (
            sh2 - sgn * Decimal("0.5") * shm * si2 + sgn * (Decimal(3) * ch2 * co2 - sh2 * si2)
        )
        om_star = (Decimal(8) / (mu * (chm ** 2))) * (
            sh2 - sgn * shm * si2 + sgn * ch2 * co2
        )
        return om, om_star, Decimal(4) * (mu ** 4)

    if alpha == 1:
        assert root_val is not None
        _, _, om, om_star = cp.eval_cp_modes_dec(root_val, x)
        return om, om_star, Decimal(4) * (root_val ** 4)

    if alpha == 2:
        mu = Decimal(m) * PI_DEC
        shm, chm = d244.dec_sinh_cosh(mu)
        sh2, ch2 = d244.dec_sinh_cosh(mu * t)
        si2, co2 = d244.dec_sin_cos(mu * t)
        sgn = Decimal(-1) if (m % 2 == 1) else Decimal(1)
        om = Decimal("0.5") * mu * (
            chm * sh2 + sgn * (chm ** 2) * si2 - Decimal(2) * sgn * shm * (sh2 * si2 + ch2 * co2)
        )
        norm2 = (-sgn) * Decimal("0.5") * shm * ((chm ** 2) + Decimal(1))
        om_star = (Decimal(2) / (mu * norm2)) * (-sgn * chm - shm * si2 + ch2 * co2)
        return om, om_star, Decimal(4) * (mu ** 4)

    if alpha == 3:
        assert root_val is not None
        gm = root_val
        shg, chg = d244.dec_sinh_cosh(gm)
        sig, cog = d244.dec_sin_cos(gm)
        sh2, ch2 = d244.dec_sinh_cosh(gm * t)
        si2, co2 = d244.dec_sin_cos(gm * t)
        om = Decimal("0.5") * gm * (
            sig * (cog * sh2 + chg * si2) - Decimal(4) * cog * sh2 * si2
        )
        norm3 = (shg ** 2) * (cog ** 4)
        f_gm = (cog ** 2) * chg
        f_t = sig * (cog * sh2 - chg * si2) + cog * ch2 * co2
        om_star = (Decimal(2) / (gm * norm3)) * (f_gm - f_t)
        return om, om_star, Decimal(4) * (gm ** 4)

    raise ValueError(alpha)


def eval_v_alpha_star_dec(alpha: int, kap: Decimal, t_r: Decimal, y: Decimal) -> Decimal:
    r"""
    Closed-form positive-branch pure-beam adjoint mode v_r^{(\alpha)*}(y) = 4 \int_y^1 w_r^{(\alpha)*}(s) ds.
    """
    base = d244.eval_psi_hat_sq_dec(kap, t_r, y)
    if alpha == 1:
        return base
    _, ch = d244.dec_sinh_cosh(kap)
    _, co = d244.dec_sin_cos(kap)
    E0_k = Decimal("0.5") * (ch + co)
    E2_k = Decimal("0.5") * (ch - co)
    E0_sym = d244.cdec_E(0, (kap * (Decimal(2) * y - Decimal(1)), Decimal(0)))[0]
    E0_w = d244.cdec_E(0, (kap * y, kap * (Decimal(1) - y)))
    lam_y = E0_k - E0_sym - Decimal(2) * E0_w[1]
    if alpha == 0:
        return base - lam_y / E0_k
    if alpha == 2:
        return base + ((t_r ** 2) * lam_y) / E2_k
    if alpha == 3:
        return base + (Decimal(2) * lam_y) / E0_k
    raise ValueError(alpha)


def G_Upsilon_alpha_dec(alpha: int, x: Decimal, y: Decimal) -> Decimal:
    r"""Explicit piecewise-cubic pure-beam Green's kernel G_\Upsilon^{(\alpha)}(x, y) for \alpha in {0,1,2,3}."""
    gc = srb.G_Upsilon_C_dec(x, y)
    q0 = y * ((Decimal(1) - y) ** 3)
    if alpha == 0:
        return gc - (Decimal(2) / Decimal(3)) * q0
    if alpha == 1:
        return gc
    if alpha == 2:
        return gc + (Decimal(1) / Decimal(3)) * (Decimal(1) - Decimal(2) * x) * q0
    if alpha == 3:
        psi_h0 = (Decimal(7) - Decimal(30) * x + Decimal(24) * x * x) / Decimal(24)
        return gc + Decimal(8) * psi_h0 * q0
    raise ValueError(alpha)


def verify_theorem_2_pure_beam_quartet(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    betas: List[Decimal],
    gammas: List[Decimal],
    gl32: List[Tuple[Decimal, Decimal]],
    gl64: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    # (a) Verify exact antiderivative identity v_r^(alpha)*(y) == 4 int_y^1 w_r^(alpha)*(s) ds
    #     and Omega_m^(alpha)*(y) == 4 int_y^1 Theta_m^(alpha)*(s) ds + zero-mass endpoint pinning
    max_antideriv_err = Decimal(0)
    max_endpoint_pin_err = Decimal(0)
    y_test = Decimal("0.29")
    span = Decimal(1) - y_test

    for alpha in (0, 2, 3):
        for r_idx in range(3):
            kap, tr, _ = modes[r_idx]
            quad_v = Decimal(4) * sum(
                span * w * lane_b.eval_w_alpha_star_dec(alpha, kap, tr, y_test + span * z)
                for z, w in gl64
            )
            cf_v = eval_v_alpha_star_dec(alpha, kap, tr, y_test)
            max_antideriv_err = max(max_antideriv_err, abs(quad_v - cf_v))

        for m in range(1, 4):
            rv = gammas[m - 1] if alpha == 3 else None
            quad_om_s = Decimal(4) * sum(
                span * w * lane_b.eval_neg_pair_dec(alpha, m, y_test + span * z, rv)[1]
                for z, w in gl64
            )
            _, cf_om_s, _ = eval_pure_beam_neg_pair_dec(alpha, m, y_test, rv)
            _, om_s_0, _ = eval_pure_beam_neg_pair_dec(alpha, m, Decimal(0), rv)
            _, om_s_1, _ = eval_pure_beam_neg_pair_dec(alpha, m, Decimal(1), rv)
            max_antideriv_err = max(max_antideriv_err, abs(quad_om_s - cf_om_s))
            max_endpoint_pin_err = max(max_endpoint_pin_err, abs(om_s_0), abs(om_s_1))

    assert max_antideriv_err < Decimal("1e-95"), f"Antiderivative mismatch: {max_antideriv_err}"
    assert max_endpoint_pin_err < Decimal("1e-95"), f"Endpoint pinning mismatch: {max_endpoint_pin_err}"

    # (b) Full 4x4 Kronecker biorthogonality & cross-branch orthogonality across ALL alpha in {0,1,2,3}
    biorth_errs: Dict[str, str] = {}
    cross_errs: Dict[str, str] = {}
    for alpha in (0, 1, 2, 3):
        max_b = Decimal(0)
        max_c = Decimal(0)
        om_grid = []
        oms_grid = []
        for m in range(1, 5):
            rv = betas[m - 1] if alpha == 1 else (gammas[m - 1] if alpha == 3 else None)
            pairs = [eval_pure_beam_neg_pair_dec(alpha, m, z, rv) for z, _ in gl64]
            om_grid.append([p[0] for p in pairs])
            oms_grid.append([p[1] for p in pairs])

        for i in range(4):
            for j in range(4):
                ip = sum(gl64[n][1] * om_grid[i][n] * oms_grid[j][n] for n in range(64))
                tgt = Decimal(1) if i == j else Decimal(0)
                max_b = max(max_b, abs(ip - tgt))

        ups_grid = [[d244.eval_Xi_and_Upsilon_dec(modes[r][0], modes[r][2], z)[1] for z, _ in gl64] for r in range(4)]
        va_grid = [[eval_v_alpha_star_dec(alpha, modes[r][0], modes[r][1], z) for z, _ in gl64] for r in range(4)]

        for r1 in range(4):
            for r2 in range(4):
                ip_pos = sum(gl64[n][1] * ups_grid[r1][n] * va_grid[r2][n] for n in range(64))
                tgt = Decimal(1) if r1 == r2 else Decimal(0)
                max_b = max(max_b, abs(ip_pos - tgt))
            for m_idx in range(4):
                c1 = sum(gl64[n][1] * ups_grid[r1][n] * oms_grid[m_idx][n] for n in range(64))
                c2 = sum(gl64[n][1] * om_grid[m_idx][n] * va_grid[r1][n] for n in range(64))
                max_c = max(max_c, abs(c1), abs(c2))

        assert max_b < Decimal("1e-62"), f"Pure-beam biorthogonality error at alpha={alpha}: {max_b}"
        assert max_c < Decimal("1e-62"), f"Pure-beam cross-orthogonality error at alpha={alpha}: {max_c}"
        biorth_errs[f"alpha={alpha}"] = f"{max_b:.3e}"
        cross_errs[f"alpha={alpha}"] = f"{max_c:.3e}"

    # (c) Exact diagonal trace equality Tr(G_Upsilon^(alpha)) == Tr(G_Xi^(alpha)) & 2-branch decomposition
    expected_traces = {
        0: Fraction(1, 24),
        1: Fraction(3, 40),
        2: Fraction(29, 360),
        3: Fraction(23, 280),
    }

    def quad32(fn, a: Decimal, b: Decimal) -> Decimal:
        h = b - a
        return sum(h * w * fn(a + h * z) for z, w in gl32)

    trace_errs: Dict[str, str] = {}
    pt_errs: Dict[str, str] = {}
    test_pts = (("0.23", "0.61"), ("0.37", "0.19"), ("0.71", "0.44"))
    for alpha in (0, 1, 2, 3):
        tr_q = quad32(lambda y: G_Upsilon_alpha_dec(alpha, y, y), Decimal(0), Decimal("0.5")) + quad32(
            lambda y: G_Upsilon_alpha_dec(alpha, y, y), Decimal("0.5"), Decimal(1)
        )
        tr_ex = Decimal(expected_traces[alpha].numerator) / Decimal(expected_traces[alpha].denominator)
        err_tr = abs(tr_q - tr_ex)
        assert err_tr < Decimal("1e-102"), f"Diagonal trace mismatch at alpha={alpha}: {err_tr}"
        trace_errs[f"alpha={alpha}"] = f"{err_tr:.3e}"

        max_pt = Decimal(0)
        for xs, ys in test_pts:
            x, y = Decimal(xs), Decimal(ys)
            g_ex = G_Upsilon_alpha_dec(alpha, x, y)
            pos_sum = sum(
                d244.eval_Xi_and_Upsilon_dec(kap, wr, x)[1] * eval_v_alpha_star_dec(alpha, kap, tr, y) / (kap ** 4)
                for kap, tr, wr in modes
            )
            neg_sum = Decimal(0)
            for m in range(1, len(modes) + 1):
                rv = betas[m - 1] if alpha == 1 else (gammas[m - 1] if alpha == 3 else None)
                om_x, _, abs_zm = eval_pure_beam_neg_pair_dec(alpha, m, x, rv)
                _, oms_y, _ = eval_pure_beam_neg_pair_dec(alpha, m, y, rv)
                neg_sum += (om_x * oms_y) / abs_zm
            assert abs(g_ex - pos_sum) > Decimal("1e-4")
            max_pt = max(max_pt, abs(g_ex - (pos_sum - neg_sum)))

        assert max_pt < Decimal("1e-9"), f"Pointwise G_Upsilon^(alpha) 2-branch error at alpha={alpha}: {max_pt}"
        pt_errs[f"alpha={alpha}"] = f"{max_pt:.3e}"

    return {
        "status": "PASS",
        "max_closed_form_antiderivative_error": f"{max_antideriv_err:.3e}",
        "max_Omega_star_endpoint_pinning_error_alpha_0_2_3": f"{max_endpoint_pin_err:.3e}",
        "pure_beam_biorthogonality_4x4_errors": biorth_errs,
        "pure_beam_cross_branch_4x4_errors": cross_errs,
        "diagonal_trace_quadrature_errors": trace_errs,
        "pointwise_G_Upsilon_2branch_errors_90_modes": pt_errs,
    }


# ---------------------------------------------------------------------------
# 3. Theorem 3: Universal Curvature Pairing Law, Sherman-Morrison Pole Exchange,
#    and Functional Mittag-Leffler Ladders on Dom_0, Dom_B, Dom_A
# ---------------------------------------------------------------------------

def apply_G_Xi_alpha_poly(alpha: int, g: List[Fraction], phi_I0_0: List[Fraction], phi_H0_0: List[Fraction]) -> List[Fraction]:
    w0_star = [Fraction(1), Fraction(-6), Fraction(9), Fraction(-4)]
    phi_0_0 = [Fraction(0), Fraction(1)]
    uC = lane_a.apply_G_Xi_C_poly(g)
    ip = fq.poly_inner_product(w0_star, g)
    if alpha == 0:
        return lane_a.strip_trailing_zeros(gtp.poly_add(uC, phi_0_0, Fraction(1), Fraction(2, 3) * ip))
    if alpha == 1:
        return uC
    if alpha == 2:
        return lane_a.strip_trailing_zeros(gtp.poly_add(uC, phi_I0_0, Fraction(1), Fraction(-1, 3) * ip))
    if alpha == 3:
        return lane_a.strip_trailing_zeros(gtp.poly_add(uC, phi_H0_0, Fraction(1), Fraction(-2) * ip))
    raise ValueError(alpha)


def verify_theorem_3_mittag_leffler_ladders(
    modes: List[Tuple[Decimal, Decimal, Decimal]],
    gammas: List[Decimal],
    gl64: List[Tuple[Decimal, Decimal]],
) -> Dict[str, object]:
    projs = gtp.build_biorthogonal_projectors(max_k=5)
    phi_0_0 = [Fraction(0), Fraction(1)]
    phi_I0_0 = projs[("I0", 0)]["Phi"]
    phi_H0_0 = projs[("H0", 0)]["Phi"]
    seeds = {0: phi_0_0, 2: phi_I0_0, 3: phi_H0_0}
    b1_vals = {0: Fraction(-2), 2: Fraction(4), 3: Fraction(2, 3)}

    # (a) Verify Sherman-Morrison pole-exchange generating identities in exact Fraction for k = 0..5:
    #       (I - z G_Xi^(0))^{-1}(x)          == [e_1(z) / e_0(z)] (I - z G_Xi^(C))^{-1}(x)
    #       (I - z G_Xi^(B))^{-1}(Phi_{I0,0}) == [e_1(z) / (2 e_2(z))] Phi_tilde_{I0}(x; z)
    #       (I - z G_Xi^(A))^{-1}(Phi_{H0,0}) == [e_1(z) / (6 e_3(z))] Phi_tilde_{H0}(x; z)
    K = 5
    e0 = [Fraction(1, math.factorial(4 * m)) for m in range(K + 1)]
    e1 = [Fraction(1, math.factorial(4 * m + 1)) for m in range(K + 1)]
    two_e2 = [Fraction(2, math.factorial(4 * m + 2)) for m in range(K + 1)]
    six_e3 = [Fraction(6, math.factorial(4 * m + 3)) for m in range(K + 1)]

    ratios = {
        0: d244.series_mul(e1, d244.series_inv(e0)),
        2: d244.series_mul(e1, d244.series_inv(two_e2)),
        3: d244.series_mul(e1, d244.series_inv(six_e3)),
    }

    c_ladders: Dict[int, List[List[Fraction]]] = {0: [phi_0_0], 2: [], 3: []}
    for k in range(1, K + 1):
        c_ladders[0].append(lane_a.apply_G_Xi_C_poly(c_ladders[0][-1]))
    for k in range(K + 1):
        c_ladders[2].append(projs[("I0", k)]["Phi"])
        c_ladders[3].append(projs[("H0", k)]["Phi"])

    alpha_ladders_phi: Dict[int, List[List[Fraction]]] = {}
    alpha_ladders_psi: Dict[int, List[List[Fraction]]] = {}
    for alpha in (0, 2, 3):
        seq_phi = [seeds[alpha][:]]
        for _ in range(1, K + 1):
            seq_phi.append(apply_G_Xi_alpha_poly(alpha, seq_phi[-1], phi_I0_0, phi_H0_0))
        alpha_ladders_phi[alpha] = seq_phi
        alpha_ladders_psi[alpha] = [
            lane_a.poly_scale(srb.poly_deriv(p, 1), Fraction(1, 4)) for p in seq_phi
        ]

        # Check pole-exchange convolution against C-ladder at every order k = 0..K!
        for k in range(K + 1):
            conv = [Fraction(0)]
            for j in range(k + 1):
                conv = lane_a.poly_add(conv, c_ladders[alpha][j], Fraction(1), ratios[alpha][k - j])
            assert conv == seq_phi[k], f"Pole-exchange identity failed at alpha={alpha}, k={k}"

    # (b) Verify universal boundary-curvature pairing law <u, w> == B_1(u) w''(1) / (8 z)
    #     and closed-form Mittag-Leffler weights to ~100 digits!
    weight_errs: Dict[str, Dict[str, str]] = {}
    ml_errs: Dict[str, Dict[str, str]] = {}

    for alpha in (0, 2, 3):
        seed = seeds[alpha]
        seed_vals = [
            sum(Decimal(c.numerator) / Decimal(c.denominator) * (z ** i) for i, c in enumerate(seed))
            for z, _ in gl64
        ]
        b1_dec = Decimal(b1_vals[alpha].numerator) / Decimal(b1_vals[alpha].denominator)
        max_wp_err = Decimal(0)
        max_wn_err = Decimal(0)

        for r_idx in range(5):
            kap, tr, _ = modes[r_idx]
            sh, ch = d244.dec_sinh_cosh(kap)
            si, co = d244.dec_sin_cos(kap)
            E0 = Decimal("0.5") * (ch + co)
            E1 = Decimal("0.5") * (sh + si)
            E2 = Decimal("0.5") * (ch - co)
            ip_q = sum(
                gl64[i][1] * seed_vals[i] * lane_b.eval_w_alpha_star_dec(alpha, kap, tr, gl64[i][0])
                for i in range(64)
            )
            if alpha == 0:
                w_pp_1 = -(kap ** 3) * E1 / E0
                cf_pos = E1 / (Decimal(4) * kap * E0)
            elif alpha == 2:
                w_pp_1 = (kap ** 3) * (tr ** 2) * E1 / E2
                cf_pos = ((tr ** 2) * E1) / (Decimal(2) * kap * E2)
            else:
                w_pp_1 = Decimal(2) * (kap ** 3) * E1 / E0
                cf_pos = E1 / (Decimal(6) * kap * E0)
            curv_formula = (b1_dec * w_pp_1) / (Decimal(8) * (kap ** 4))
            max_wp_err = max(max_wp_err, abs(ip_q - cf_pos), abs(curv_formula - cf_pos))

        for m in range(1, 6):
            rv = gammas[m - 1] if alpha == 3 else None
            ip_n = sum(
                gl64[i][1] * seed_vals[i] * lane_b.eval_neg_pair_dec(alpha, m, gl64[i][0], rv)[1]
                for i in range(64)
            )
            if alpha == 0:
                mu = Decimal(2 * m - 1) * PI_DEC / Decimal(2)
                _, chm = d244.dec_sinh_cosh(mu)
                th_pp_1 = Decimal(16) * (mu ** 2) / chm
                zm = Decimal(-4) * (mu ** 4)
                cf_neg = Decimal(1) / ((mu ** 2) * chm)
            elif alpha == 2:
                mu = Decimal(m) * PI_DEC
                _, chm = d244.dec_sinh_cosh(mu)
                th_pp_1 = Decimal(-8) * (mu ** 2) / ((chm ** 2) + Decimal(1))
                zm = Decimal(-4) * (mu ** 4)
                cf_neg = Decimal(1) / ((mu ** 2) * ((chm ** 2) + Decimal(1)))
            else:
                gm = rv
                shg, _ = d244.dec_sinh_cosh(gm)
                _, cog = d244.dec_sin_cos(gm)
                th_pp_1 = Decimal(-8) * (gm ** 2) / (shg * (cog ** 2))
                zm = Decimal(-4) * (gm ** 4)
                cf_neg = Decimal(1) / (Decimal(6) * (gm ** 2) * shg * (cog ** 2))
            curv_neg = (b1_dec * th_pp_1) / (Decimal(8) * zm)
            max_wn_err = max(max_wn_err, abs(ip_n - cf_neg), abs(curv_neg - cf_neg))

        assert max_wp_err < Decimal("1e-98"), f"Pos weight error at alpha={alpha}: {max_wp_err}"
        assert max_wn_err < Decimal("1e-90"), f"Neg weight error at alpha={alpha}: {max_wn_err}"
        weight_errs[f"alpha={alpha}"] = {
            "max_pos_weight_error": f"{max_wp_err:.3e}",
            "max_neg_weight_error": f"{max_wn_err:.3e}",
        }

        # (c) Functional Mittag-Leffler convergence across k = 1, 2, 3 on [0, 1]
        ml_errs[f"alpha={alpha}"] = {}
        for k in (1, 2, 3):
            p_phi = alpha_ladders_phi[alpha][k]
            p_psi = alpha_ladders_psi[alpha][k]
            max_ephi = Decimal(0)
            max_epsi = Decimal(0)
            for xs in ("0.20", "0.375", "0.75"):
                x = Decimal(xs)
                ex_phi = sum(Decimal(c.numerator) / Decimal(c.denominator) * (x ** i) for i, c in enumerate(p_phi))
                ex_psi = sum(Decimal(c.numerator) / Decimal(c.denominator) * (x ** i) for i, c in enumerate(p_psi))

                pos_phi = Decimal(0)
                pos_psi = Decimal(0)
                for kap, tr, wr in modes:
                    sh, ch = d244.dec_sinh_cosh(kap)
                    si, co = d244.dec_sin_cos(kap)
                    E0 = Decimal("0.5") * (ch + co)
                    E1 = Decimal("0.5") * (sh + si)
                    E2 = Decimal("0.5") * (ch - co)
                    wp = (
                        E1 / (Decimal(4) * kap * E0)
                        if alpha == 0
                        else (
                            ((tr ** 2) * E1) / (Decimal(2) * kap * E2)
                            if alpha == 2
                            else E1 / (Decimal(6) * kap * E0)
                        )
                    )
                    xi_v, ups_v = d244.eval_Xi_and_Upsilon_dec(kap, wr, x)
                    denom = kap ** (4 * k)
                    pos_phi += (wp / denom) * xi_v
                    pos_psi += (wp / denom) * ups_v

                neg_phi = Decimal(0)
                neg_psi = Decimal(0)
                for m in range(1, len(modes) + 1):
                    rv = gammas[m - 1] if alpha == 3 else None
                    th_x, _, abs_zm = lane_b.eval_neg_pair_dec(alpha, m, x, rv)
                    om_x, _, _ = eval_pure_beam_neg_pair_dec(alpha, m, x, rv)
                    if alpha == 0:
                        mu = Decimal(2 * m - 1) * PI_DEC / Decimal(2)
                        _, chm = d244.dec_sinh_cosh(mu)
                        wn = Decimal(1) / ((mu ** 2) * chm)
                    elif alpha == 2:
                        mu = Decimal(m) * PI_DEC
                        _, chm = d244.dec_sinh_cosh(mu)
                        wn = Decimal(1) / ((mu ** 2) * ((chm ** 2) + Decimal(1)))
                    else:
                        gm = rv
                        shg, _ = d244.dec_sinh_cosh(gm)
                        _, cog = d244.dec_sin_cos(gm)
                        wn = Decimal(1) / (Decimal(6) * (gm ** 2) * shg * (cog ** 2))
                    eig_pow = (-abs_zm) ** k
                    neg_phi += (wn / eig_pow) * th_x
                    neg_psi += (wn / eig_pow) * om_x

                max_ephi = max(max_ephi, abs(ex_phi - (pos_phi + neg_phi)))
                max_epsi = max(max_epsi, abs(ex_psi - (pos_psi + neg_psi)))

            assert max_ephi < Decimal("1e-13"), f"Phi ML error too large at alpha={alpha}, k={k}: {max_ephi}"
            assert max_epsi < Decimal("1e-11"), f"Psi ML error too large at alpha={alpha}, k={k}: {max_epsi}"
            ml_errs[f"alpha={alpha}"][f"k={k}"] = {
                "max_Phi_error": f"{max_ephi:.3e}",
                "max_Psi_error": f"{max_epsi:.3e}",
            }

        assert Decimal(ml_errs[f"alpha={alpha}"]["k=3"]["max_Phi_error"]) < Decimal("1e-32")
        assert Decimal(ml_errs[f"alpha={alpha}"]["k=3"]["max_Psi_error"]) < Decimal("1e-30")

    return {
        "status": "PASS",
        "sherman_morrison_pole_exchange_verified_k0_to_5": True,
        "universal_curvature_pairing_weight_errors": weight_errs,
        "functional_mittag_leffler_90_mode_errors": ml_errs,
    }


def main() -> None:
    modes_90 = [d244.solve_kappa_105(r) for r in range(1, 91)]
    betas_90 = [cp.solve_beta_105(m) for m in range(1, 91)]
    gammas_90 = [fq.solve_gamma_minus(m) for m in range(1, 91)]
    gl32 = d244.gauss_legendre_nodes_weights(32)
    gl64 = d244.gauss_legendre_nodes_weights(64)

    res1 = verify_theorem_1_ab_cross(modes_90, betas_90, gl64)
    res2 = verify_theorem_2_pure_beam_quartet(modes_90, betas_90, gammas_90, gl32, gl64)
    res3 = verify_theorem_3_mittag_leffler_ladders(modes_90, gammas_90, gl64)

    report = {
        "script": "quartet_pure_beam_duals_and_ab_cross_verification_2026_11_17.py",
        "author": "Petrovich (ompu-e1dd503f59)",
        "date": "2026-11-17",
        "revision": 105,
        "closes": [
            "Phi-Hausmaster declared loss (bus:1794909763): direct side-by-side A <-> B cross-verification of seq 247 & seq 248",
            "Lane B open seam `[=~` (bus:1794909529 §2): pure-beam quartet duals {Omega_m^(alpha), Omega_m^(alpha)*}, 2-branch G_Upsilon^(alpha), and Mittag-Leffler ladders on Dom_0, Dom_B, Dom_A",
        ],
        "theorem_1_ab_cross_verification": res1,
        "theorem_2_pure_beam_quartet_duals_and_2branch_green": res2,
        "theorem_3_curvature_pairing_pole_exchange_and_mittag_leffler": res3,
        "verdict": "ALL_CHECKS_PASSED",
    }

    out_path = HERE / "quartet_pure_beam_duals_and_ab_cross_verification_2026_11_17_results.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=" * 78)
    print("REV 105 UNIFICATION: A<->B CROSS-VERIFIER & PURE-BEAM QUARTET CLOSURE")
    print("=" * 78)
    print(f"[PASS] Theorem 1 (A<->B Cross-Check): exact poly deg 0..10, G_Xi^(0) diff={res1['max_pointwise_G_Xi_0_ab_diff']}, "
          f"Dom_0 traces={res1['dom_0_exact_traces_n1_to_3']}")
    print(f"[PASS] Theorem 2 (Pure-Beam Quartet): biorth={res2['pure_beam_biorthogonality_4x4_errors']}, "
          f"2-branch G_Upsilon={res2['pointwise_G_Upsilon_2branch_errors_90_modes']}")
    print(f"[PASS] Theorem 3 (Pole Exchange & ML Ladders on Dom_0, Dom_B, Dom_A): "
          f"k=3 errs={{a0: {res3['functional_mittag_leffler_90_mode_errors']['alpha=0']['k=3']}, "
          f"a2: {res3['functional_mittag_leffler_90_mode_errors']['alpha=2']['k=3']}, "
          f"a3: {res3['functional_mittag_leffler_90_mode_errors']['alpha=3']['k=3']}}}")
    print("VERDICT: ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
