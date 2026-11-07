"""Probe 2: Theorem 4.2 / 5.2(d) on schemes NOT in the paper. nu from the script's own bracket (min-max of Q over
tight cycles of T), C(K* + eps) from the theorem-free grid LP (a relaxation, hence a lower bound on C), at
eps = eps_0 of Theorem 5.2(d) (when it is resolvable) and at a few multiples. Also recompute eps_0 for the irrational
scheme (paper: 0.0286)."""
import random
from probe_common import fv, Fr

rng = random.Random(99)


def analyse(S):
    K = S.kstar_exact()
    if K == 0:
        return None
    tc, tcyc = S.tight_by_cycles(K)
    P, _ = S.pinched(tc)
    if not P:
        return None
    lo, hi = fv.nu_bracket(S, tcyc, P)
    rhos = []
    for c in S._cycles:
        G, D = S.cycle_gd(c)
        if D > 0:
            rhos.append(G / D)
    mu_min = min(K - r for r in rhos if r < K)
    d_min = min(a[4] for a in S.arcs)
    eps0 = hi * float(d_min) * float(mu_min) / 4
    return K, P, lo, hi, mu_min, d_min, eps0


S_irr = fv.Scheme(*fv.NAMED["irrational"])
K, P, lo, hi, mu_min, d_min, eps0 = analyse(S_irr)
print(f"irrational: K*={K}, nu in [{lo:.9f},{hi:.9f}], mu_min={mu_min}, d_min={d_min}, eps0={eps0:.4f} (paper 0.0286)")

found = 0
tries = 0
while found < 6 and tries < 400:
    tries += 1
    S = fv.random_scheme(rng)
    a = analyse(S)
    if a is None:
        continue
    K, P, lo, hi, mu_min, d_min, eps0 = a
    found += 1
    print(f"\nscheme {found}: marks={[(str(t), o, u, str(g)) for t, o, u, g in S.marks]}")
    print(f"  K*={K}, |P|={len(P)}, nu in [{lo:.8f},{hi:.8f}], mu_min={mu_min}, d_min={d_min}, eps0={eps0:.5f} = {eps0/float(K):.4f} K*")
    for frac in (Fr(1, 40), Fr(1, 20), Fr(1, 10)):
        eps = frac * K
        Kk = K + eps
        N = 2400
        val = fv.grid_lp_C(S, Kk, N)
        form = hi * float(Kk) ** 2 / float(eps)
        tag = "eps<=eps0" if float(eps) <= eps0 else "eps>eps0"
        print(f"  eps={frac}K* ({tag}): grid LP C = {val:.6f}, nu K^2/eps = {form:.6f}, LP/formula = {val/form:.6f}")
