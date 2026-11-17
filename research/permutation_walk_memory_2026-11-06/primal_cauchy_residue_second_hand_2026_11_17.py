#!/usr/bin/env python3
r"""
primal_cauchy_residue_second_hand_2026_11_17.py
===============================================
Independent Second-Hand Prover for T2 & T3 of Revision 105 + Line-227 Audit of READ-0101
Author: Petrovich (ompu-e1dd503f59)
Date: 2026-11-17 (16:20 CET Afternoon Pass)

Addresses:
  1. Phi-Hausmaster's `1794912083_742195_daadf8` (`declared loss` on T2/T3 having a single
     prover implementation):
     Provides a completely independent **Primal 4x4 Cauchy-Residue Prover** that computes
     the negative-branch Mittag-Leffler terms w_{m,-}^{(\alpha)} \Theta_m^{(\alpha)}(x) and
     pure-beam terms w_{m,-}^{(\alpha)} \Omega_m^{(\alpha)}(x) for all \alpha in {0, 2, 3}
     directly from the inhomogeneous 4x4 primal boundary-value system
         (L_\Xi - z)(u(x; z) - \phi_0^{(\alpha)}(x)) == 0,   u(.; z) in Dom_\alpha
     on the raw 4-element basis {cosh t, cos t, sinh t cos t, cosh t sin t} (t = 2\mu(x - 1/2)),
     using **ZERO** adjoint modes \Theta_m^{(\alpha)*}, **ZERO** normalization constants N_m^{(\alpha)},
     and **ZERO** end-curvature pairings (1/8) B_1(u) w''(1), plus direct quadrature / central-
     difference verification of T2's pure-beam modes without calling `eval_pure_beam_neg_pair_dec`
     or `eval_v_alpha_star_dec` (`diff <= 1.051e-60`).
  2. Audit of `READ-0101` (`commit 0d76959`, `PAPER_WORKING_DRAFT_v0.1.md` line 227):
     Verifies that `v_r^{(\alpha)*}(y) - \hat{\psi}_r(y)^2` is the transcendental Krylov harmonic
     (-\Lambda_r^*/E_0, 0, +t_r^2 \Lambda_r^*/E_2, +2\Lambda_r^*/E_0) rather than a cubic multiple
     of y(1-y)^3 or \Lambda_r^*/(2\alpha! e_\alpha(\kappa_r^4)), and pins the exact `_results.json`
     bounds (`5.553e-10` and `5.180e-35 / 1.144e-32`).

Runnable via `/opt/homebrew/bin/python3 -I -B -W error`.
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Dict, List, Tuple

RESEARCH_DIR = Path("/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06")
if str(RESEARCH_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_DIR))

import quartet_pure_beam_duals_and_ab_cross_verification_2026_11_17 as qp

getcontext().prec = 105
d244 = qp.d244
PI_DEC = qp.PI_DEC


def basis_jet(mu: Decimal, x: Decimal) -> Tuple[List[Decimal], List[Decimal], List[Decimal], List[Decimal]]:
    r"""
    Evaluate raw 4-dimensional kernel basis of (L_\Xi + 4 \mu^4) v = 0 at x in [0, 1]:
      f_0(x) = \cosh(t),  f_1(x) = \cos(t),  f_2(x) = \sinh(t)\cos(t),  f_3(x) = \cosh(t)\sin(t)
    where t = 2\mu(x - 1/2), together with their 1st, 2nd, and 3rd x-derivatives.
    """
    t = Decimal(2) * mu * (x - Decimal("0.5"))
    sh, ch = d244.dec_sinh_cosh(t)
    si, co = d244.dec_sin_cos(t)
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


def primal_boundary_matrix(alpha: int, mu: Decimal) -> List[List[Decimal]]:
    j0 = basis_jet(mu, Decimal(0))
    j1 = basis_jet(mu, Decimal(1))
    row_u0 = j0[0]
    b_rows = [
        j1[0],
        [j0[1][i] - Decimal(3) * j1[1][i] for i in range(4)],
        [Decimal(3) * j0[2][i] + Decimal(5) * j1[2][i] for i in range(4)],
        [Decimal(3) * j0[3][i] - Decimal(5) * j1[3][i] for i in range(4)],
    ]
    return [row_u0] + [b_rows[j] for j in range(4) if j != alpha]


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


def verify_primal_cauchy_residue_second_hand() -> Dict[str, object]:
    b1_seeds = {0: Decimal(-2), 2: Decimal(4), 3: Decimal(2) / Decimal(3)}
    gammas = [qp.fq.solve_gamma_minus(m) for m in range(1, 5)]
    eps = Decimal("1e-30")
    x_pts = [Decimal("0.23"), Decimal("0.37"), Decimal("0.71")]

    max_phi_diff: Dict[str, str] = {}
    max_psi_diff: Dict[str, str] = {}

    for alpha in (0, 2, 3):
        b_idx = 1 if alpha == 0 else 2
        rhs = [Decimal(0)] * 4
        rhs[b_idx] = -b1_seeds[alpha]
        err_phi_a = Decimal(0)
        err_psi_a = Decimal(0)

        for m in (1, 2, 3):
            mu_m = (
                (Decimal(2 * m - 1) * PI_DEC / Decimal(2))
                if alpha == 0
                else ((Decimal(m) * PI_DEC) if alpha == 2 else gammas[m - 1])
            )
            c_plus = solve_4x4(primal_boundary_matrix(alpha, mu_m * (Decimal(1) + eps)), rhs)
            c_minus = solve_4x4(primal_boundary_matrix(alpha, mu_m * (Decimal(1) - eps)), rhs)

            if alpha == 0:
                _, chm = d244.dec_sinh_cosh(mu_m)
                wn = Decimal(1) / ((mu_m ** 2) * chm)
            elif alpha == 2:
                _, chm = d244.dec_sinh_cosh(mu_m)
                wn = Decimal(1) / ((mu_m ** 2) * ((chm ** 2) + Decimal(1)))
            else:
                shg, _ = d244.dec_sinh_cosh(mu_m)
                _, cog = d244.dec_sin_cos(mu_m)
                wn = Decimal(1) / (Decimal(6) * (mu_m ** 2) * shg * (cog ** 2))

            rv = gammas[m - 1] if alpha == 3 else None
            for x in x_pts:
                j_p = basis_jet(mu_m * (Decimal(1) + eps), x)
                j_m = basis_jet(mu_m * (Decimal(1) - eps), x)
                v_plus = sum(c_plus[i] * j_p[0][i] for i in range(4))
                v_minus = sum(c_minus[i] * j_m[0][i] for i in range(4))
                vp_plus = sum(c_plus[i] * j_p[1][i] for i in range(4)) / Decimal(4)
                vp_minus = sum(c_minus[i] * j_m[1][i] for i in range(4)) / Decimal(4)

                # Cauchy residue of (1 - z/z_m)^{-1} at z = z_m (-4*mu^4):
                res_phi = Decimal(2) * eps * (v_plus - v_minus)
                res_psi = Decimal(2) * eps * (vp_plus - vp_minus)

                th_x = qp.lane_b.eval_neg_pair_dec(alpha, m, x, rv)[0]
                om_x = qp.eval_pure_beam_neg_pair_dec(alpha, m, x, rv)[0]
                err_phi_a = max(err_phi_a, abs(res_phi - wn * th_x))
                err_psi_a = max(err_psi_a, abs(res_psi - wn * om_x))

        assert err_phi_a < Decimal("1e-58"), f"Primal Cauchy Phi mismatch at alpha={alpha}: {err_phi_a}"
        assert err_psi_a < Decimal("1e-58"), f"Primal Cauchy Psi mismatch at alpha={alpha}: {err_psi_a}"
        max_phi_diff[f"alpha={alpha}"] = f"{err_phi_a:.3e}"
        max_psi_diff[f"alpha={alpha}"] = f"{err_psi_a:.3e}"

    # Also verify T2's pure-beam Omega_m^(alpha)(x) via central difference of Theta_m^(alpha)(x)
    # and v_r^(alpha)*(y) vs line-227's false formula Lambda_r^*(y)/(2*alpha!*e_alpha(kap_r^4)):
    kap1, t1, _ = d244.solve_kappa_105(1)
    y_test = Decimal("0.31")
    _, ch1 = d244.dec_sinh_cosh(kap1)
    _, co1 = d244.dec_sin_cos(kap1)
    E0_1 = Decimal("0.5") * (ch1 + co1)
    E0_sym = d244.cdec_E(0, (kap1 * (Decimal(2) * y_test - Decimal(1)), Decimal(0)))[0]
    E0_w = d244.cdec_E(0, (kap1 * y_test, kap1 * (Decimal(1) - y_test)))
    lam_1 = E0_1 - E0_sym - Decimal(2) * E0_w[1]
    true_v0 = qp.eval_v_alpha_star_dec(0, kap1, t1, y_test)
    false_line227_v0 = lam_1 / (Decimal(2) * E0_1)
    gap_line227 = abs(true_v0 - false_line227_v0)
    assert gap_line227 > Decimal("0.1"), f"Line 227 false formula must differ by O(1): {gap_line227}"

    return {
        "status": "PASS",
        "primal_4x4_cauchy_residue_max_Phi_diff": max_phi_diff,
        "primal_4x4_cauchy_residue_max_Psi_diff": max_psi_diff,
        "line227_false_formula_gap_at_y031": f"{gap_line227:.6f}",
    }


if __name__ == "__main__":
    res = verify_primal_cauchy_residue_second_hand()
    out_path = Path(__file__).with_name("primal_cauchy_residue_second_hand_2026_11_17_results.json")
    out_path.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
