"""Probe 7: Sec. 4 says, for the irrational scheme, 'balance is impossible there, which is why nu is a square-root
number'. Counter-check: find a scheme with an UNBALANCED optimum (x_r != 0) and RATIONAL nu.
With P = {r}, nu = 2/(sqrt L1 + sqrt L2)^2 and x_r = +-(sqrt L2 - sqrt L1)/(sqrt L1 + sqrt L2): rational whenever
L1/L2 is a rational square, e.g. L1 = 4, L2 = 16."""
import math
import random
from probe_common import fv, Fr

rng = random.Random(3)
threads = ["A", "B", "C", "D"]
found = None
for _ in range(20000):
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
    P, _ = S.pinched(tc)
    if len(P) != 1:
        continue
    r = P[0]
    Ls = {}
    for c in tcyc:
        _, D = S.cycle_gd(c)
        for kk in c:
            e = S.edges[kk]
            if e[0] == "arc" and r in (e[1], e[2]):
                Ls[e[3]] = min(Ls.get(e[3], math.inf), D)
    L1, L2 = sorted(Ls.values())
    q = Fr(L1) / Fr(L2)
    rt = (math.isqrt(q.numerator) ** 2 == q.numerator) and (math.isqrt(q.denominator) ** 2 == q.denominator)
    if rt and L1 != L2:
        lo, hi = fv.nu_bracket(S, tcyc, P)
        found = (S, L1, L2, lo, hi)
        break
if found:
    S, L1, L2, lo, hi = found
    s1, s2 = math.sqrt(L1), math.sqrt(L2)
    print(f"probe7: marks={[(str(t), o, u, str(g)) for t, o, u, g in S.marks]}")
    print(f"  P = {{{S.nodes[S.pinched(S.tight_by_cycles(S.kstar_exact())[0])[0][0]]}}}, shortest tight cycles through"
          f" its arcs L1={L1}, L2={L2}; nu bracket [{lo:.10f},{hi:.10f}] vs 2/(sqrt L1+sqrt L2)^2 = {2/(s1+s2)**2:.10f}"
          f" (= 2/27)"
          f"; optimal |x_r| = {(s2-s1)/(s1+s2):.6f} (unbalanced, rational nu)")
else:
    print("probe7: no example found")
