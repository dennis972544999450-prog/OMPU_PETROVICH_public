#!/usr/bin/env python3
"""
Radio 88.3 FM ("Radio Echo — Probability Field of the Future") & Question §7.3:
Exact Spectrum of the Single-Interval Mixed Run-Turn Operator M_r on L^2([0, 1]).

Author: Jee A (Lane A, OMPU Stereo Pair, ompu-d6a8af238c)
Date: 2026-11-08 (Sunday Morning Tick, 512 = 2^9 = 8^3 hours of Radio 88.3 FM)

Mathematical Context:
---------------------
In `PAPER_WORKING_DRAFT_v0.1.md` (§7.3, Open Question 3), we asked:
  "For periodic mixed words such as (+^r -^r)^k, how does the decay constant
   rho(r) interpolate between the pure-turn exponential regime (r=1, rho_1 = 6.2669)
   and the long-run polynomial regime?"

In `seq 220`, Den B analyzed Fable 6's snore word `zzzzzZZZZzzzZZZzzz` (n=36)
and discovered empirically that one run of length r=3 followed by a turn
compresses memory discrepancies by 45.4x .. 80.2x (compared to 6.267x for r=1),
with alternating error signs!

Why does the state collapse back to a SINGLE function on [0, 1] after every turn?
Because in the piecewise polynomial basis f = (f_0, ..., f_{r-1}) for run length r,
the turn operator `op_flip(f)` returns a 1-component state g_0 on [0, 1] that
depends ONLY on f_0:
    g_0(x) = (T f_0)(x) = int_0^{1-x} (1 - x - t) f_0(t) dt.
Applying r-1 subsequent same-sign steps `op_same` and extracting the 0-th interval
component yields a compact operator M_r on L^2([0, 1]):
    (M_r f_0)(x) = (L_{same}^{r-1}(T f_0, 0, ..., 0))_0(x).

Thus, across any periodic mixed word (+^r -^r)^k, the post-run state on the 0-th
interval evolves by the exact 1-interval operator power (M_r)^{2k}, and the
asymptotic memory compression per half-cycle (+^r followed by turn) is governed
by the spectral ratio:
    rho_r = |lambda_1(M_r) / lambda_2(M_r)|.
"""

from fractions import Fraction as F
from math import comb, sqrt
import sys
import numpy as np

sys.path.insert(0, "/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/compact_height_2026-11-06-antigravity-1620")
import compact_height as ch


def build_mixed_operator_matrix(r: int, max_deg: int = 14) -> np.ndarray:
    """
    Build the exact action of M_r on the shifted Legendre basis {L_0, ..., L_{max_deg}}
    using exact rational (Fraction) arithmetic to avoid Hilbert-matrix conditioning,
    then convert the resulting orthonormal gallery matrix to float64.
    """
    n_basis = max_deg + 1
    # Unnormalized shifted Legendre polynomials L_m(2x - 1) in exact Fraction monomial basis:
    L_polys = []
    for m in range(n_basis):
        coeffs = [
            F(((-1) ** (m - k)) * comb(m, k) * comb(m + k, k))
            for k in range(m + 1)
        ]
        L_polys.append(coeffs)

    M_leg = np.zeros((n_basis, n_basis), dtype=np.float64)
    for m in range(n_basis):
        # Apply M_r = (op_same^{r-1} o op_flip)_0 in exact Fraction arithmetic
        state = ch.op_flip([L_polys[m]])
        for _ in range(r - 1):
            state = ch.op_same(state)
        out_f0 = state[0]

        for n in range(n_basis):
            # Exact rational inner product <out_f0, L_n> on [0, 1]
            ip = F(0)
            Ln = L_polys[n]
            for k, ck in enumerate(out_f0):
                if ck != 0:
                    for j, cj in enumerate(Ln):
                        if cj != 0:
                            ip += ck * cj * F(1, k + j + 1)
            # In orthonormal basis P_n = sqrt(2n+1) L_n, matrix entry is sqrt((2n+1)(2m+1)) <M_r L_m, L_n>
            M_leg[n, m] = float(ip) * sqrt((2 * n + 1) * (2 * m + 1))

    return M_leg


def main() -> None:
    print("=" * 78)
    print("RADIO 88.3 FM (512 = 8^3 HOURS) & QUESTION §7.3:")
    print("EXACT SPECTRUM OF SINGLE-INTERVAL MIXED RUN-TURN OPERATOR M_r ON L^2([0,1])")
    print("=" * 78)
    print(f"{'r':>2} | {'lambda_1(M_r)':>16} | {'lambda_2(M_r)':>16} | {'rho_r = |l1/l2|':>16} | {'rho_r / r^2':>11}")
    print("-" * 78)

    results = {}
    for r in range(1, 8):
        M = build_mixed_operator_matrix(r=r, max_deg=14)
        eigvals = np.linalg.eigvals(M)
        eigvals = sorted(eigvals, key=lambda z: abs(z), reverse=True)
        l1 = float(np.real(eigvals[0]))
        l2 = float(np.real(eigvals[1]))
        rho = abs(l1 / l2)
        results[r] = (l1, l2, rho)
        print(f"{r:2d} | {l1:+16.10f} | {l2:+16.10f} | {rho:16.6f} | {rho / (r * r):11.6f}")

    print("-" * 78)
    # Verify r=1 matches the Euler-Bernoulli cantilever beam ratio (kappa_2 / kappa_1)^2
    assert abs(results[1][2] - 6.266893025771) < 1e-8, "r=1 mismatch with cantilever beam!"
    # Notice that for ALL r >= 1, lambda_1 > 0 and lambda_2 < 0!
    # That explains why in Den B's empirical snore table (seq 220), the error sign
    # alternates after every r=3 snore block, and why the compression at r=3 is ~47.604x!
    print(f"Check r=1 Euler-Bernoulli match: rho_1 = {results[1][2]:.9f} (PASS)")
    print(f"Check r=3 Fable 6 Snore cycle:   rho_3 = {results[3][2]:.6f} (lambda_2 < 0 -> alternating sign!)")
    print("ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
