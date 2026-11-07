"""Probe 6: Consequences (c), (d) of Theorem 4.3 on random schemes with pinched nodes (4 threads, half-integer marks):
  (c) nu <= max_Gamma (#ramps)/(2 L_Gamma)          (d) nu >= 2/(sqrt L1 + sqrt L2)^2 for every pinched r,
  with equality in (d) when P = {r}.  nu from the script's primal/dual bracket."""
import math
import random
from probe_common import fv, Fr

rng = random.Random(7)
threads = ["A", "B", "C", "D"]
viol_c = viol_d = viol_eq = 0
n = neq = 0
tries = 0
while n < 60 and tries < 3000:
    tries += 1
    k = rng.randint(2, 6)
    ts = sorted(rng.sample([Fr(i, 2) for i in range(24)], k))
    marks = []
    for t in ts:
        order = rng.sample(threads, 4)
        pairs = [(order[i], order[j]) for i in range(4) for j in range(i + 1, 4)]
        for (o, u) in rng.sample(pairs, rng.randint(1, 2)):
            marks.append((t, o, u, rng.choice([Fr(1), Fr(2)])))
    S = fv.Scheme(12, marks)
    K = S.kstar_exact()
    if K == 0:
        continue
    tc, tcyc = S.tight_by_cycles(K)
    P, sign = S.pinched(tc)
    if not P:
        continue
    n += 1
    lo, hi = fv.nu_bracket(S, tcyc, P)
    Pset = set(P)
    dens = 0.0
    shortest = {}  # (node, arc_id) -> shortest L of tight cycle through that arc
    for c in tcyc:
        _, D = S.cycle_gd(c)
        ramps = 0
        for kk in c:
            e = S.edges[kk]
            if e[0] != "arc":
                continue
            for end in (e[1], e[2]):
                if end in Pset:
                    ramps += 1
                    key = (end, e[3])
                    shortest[key] = min(shortest.get(key, math.inf), float(D))
        dens = max(dens, ramps / (2 * float(D)))
    if hi > dens + 1e-9:
        viol_c += 1
    for r in P:
        Ls = [v for (node, a), v in shortest.items() if node == r]
        assert len(Ls) == 2, Ls
        b = 2 / (math.sqrt(Ls[0]) + math.sqrt(Ls[1])) ** 2
        if lo < b - 1e-9:
            viol_d += 1
        if len(P) == 1:
            neq += 1
            if abs(hi - b) > 1e-7:
                viol_eq += 1
print(f"probe6: {n} random schemes with P nonempty ({tries} tries): (c) violations {viol_c}; (d) violations {viol_d}; "
      f"P={{r}} cases {neq}, equality failures {viol_eq}")
