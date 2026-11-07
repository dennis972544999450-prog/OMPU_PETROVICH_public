"""Probe 1: K* = max cycle ratio (Prop 2.1) against a grid LP over Lipschitz grid functions that knows nothing
about cycles or difference constraints. Random schemes outside the script's generator: 4 threads, half-integer
marks, 1-3 constraints per mark (acyclic inside a mark), g in {1/2, 1, 2, 3}. Also two-mark schemes: pinched only
when antipodal (Cor 3.4, last sentence)."""
import random
from probe_common import fv, Fr, grid_lp_kstar

rng = random.Random(4242)
threads = ["A", "B", "C", "D"]


def rand_scheme():
    while True:
        k = rng.randint(2, 6)
        ts = sorted(rng.sample([Fr(i, 2) for i in range(24)], k))
        marks = []
        for t in ts:
            order = rng.sample(threads, 4)  # a random total order; take 1-3 of its pairs => acyclic
            pairs = [(order[i], order[j]) for i in range(4) for j in range(i + 1, 4)]
            for (o, u) in rng.sample(pairs, rng.randint(1, 3)):
                marks.append((t, o, u, rng.choice([Fr(1, 2), Fr(1), Fr(2), Fr(3)])))
        return fv.Scheme(12, marks)


worst = 0.0
n = 0
npos = 0
for _ in range(120):
    S = rand_scheme()
    K = S.kstar_exact()
    Kg = grid_lp_kstar(S, 96)  # dt = 1/8 contains all half-integer marks
    n += 1
    npos += K > 0
    worst = max(worst, abs(Kg - float(K)))
print(f"probe1a: {n} random 4-thread schemes ({npos} with K*>0): max |grid-LP K* - cycle-ratio K*| = {worst:.2e}")

# two-mark schemes: pinched nodes appear only for antipodal marks
bad = 0
anti_pinched = 0
anti_pos = 0
cnt = 0
for _ in range(300):
    d = rng.choice([Fr(i, 2) for i in range(1, 24)])
    ts = [Fr(0), d]
    marks = []
    for t in ts:
        order = rng.sample(threads[:3], 3)
        pairs = [(order[i], order[j]) for i in range(3) for j in range(i + 1, 3)]
        for (o, u) in rng.sample(pairs, rng.randint(1, 3)):
            marks.append((t, o, u, rng.choice([Fr(1), Fr(2), Fr(3)])))
    S = fv.Scheme(12, marks)
    K = S.kstar_exact()
    if K == 0:
        continue
    cnt += 1
    tc, _ = S.tight_by_cycles(K)
    P, _ = S.pinched(tc)
    if d == 6:
        anti_pos += 1
        anti_pinched += bool(P)
    elif P:
        bad += 1
print(f"probe1b: {cnt} two-mark schemes with K*>0: pinched with non-antipodal marks: {bad}; "
      f"antipodal with K*>0: {anti_pos}, of them pinched: {anti_pinched}")
