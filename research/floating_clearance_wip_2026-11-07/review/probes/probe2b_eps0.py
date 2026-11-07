"""Probe 2b: schemes 2 and 3 of probe 2 leave the formula upward at eps = K*/40. Is the sufficient threshold eps_0 of
Theorem 5.2(d) respected (grid LP = lower bound on C must not exceed nu K^2/eps for eps <= eps_0)? Where is the
first departure (crude bracket)? Fine grids, since ramps are short."""
from probe_common import fv, Fr

schemes = {
    "s2": [(1, 'A', 'C', 1), (3, 'C', 'B', 1), (5, 'C', 'A', 3), (10, 'B', 'C', 3)],
    "s3": [(0, 'C', 'B', 3), (2, 'A', 'B', 2), (3, 'A', 'C', 3), (7, 'B', 'A', 3), (11, 'A', 'B', 3)],
}
for name, marks in schemes.items():
    S = fv.Scheme(12, marks)
    K = S.kstar_exact()
    tc, tcyc = S.tight_by_cycles(K)
    P, _ = S.pinched(tc)
    lo, hi = fv.nu_bracket(S, tcyc, P)
    rhos = [G / D for G, D in (S.cycle_gd(c) for c in S._cycles) if D > 0]
    mu_min = min(K - r for r in rhos if r < K)
    d_min = min(a[4] for a in S.arcs)
    eps0 = hi * float(d_min) * float(mu_min) / 4
    print(f"{name}: K*={K}, nu={hi:.8f}, eps0={eps0:.6f} = {eps0/float(K):.5f} K*")
    for mult in (0.5, 1.0, 2.0, 4.0, 8.0):
        eps = Fr(eps0 * mult).limit_denominator(10**6)
        Kk = K + eps
        N = 4800
        val = fv.grid_lp_C(S, Kk, N)
        form = hi * float(Kk) ** 2 / float(eps)
        print(f"  eps = {mult} eps0: grid LP C = {val:.6f}, formula = {form:.6f}, LP/formula - 1 = {val/form - 1:+.2e}")
