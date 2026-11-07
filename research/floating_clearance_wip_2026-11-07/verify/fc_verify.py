#!/usr/bin/env python3
"""Floating clearance: self-contained verification suite (research in progress, v0.1-wip).

Written 2026-11-07 as an independent re-implementation for the working paper
PAPER_WORKING_DRAFT_v0.1.md next to this folder. It does NOT import the dated
workbench code it summarizes; it recomputes a chosen set of claims from scratch:

  V1  K* = maximum cycle ratio (exact cycle enumeration) == LP optimum          [Prop. 2.1]
  V2  forced (tight) edges: Floyd-Warshall test == union of tight simple cycles   [Fact 3.2]
      pinched node => the scheme has >= 2 tight simple cycles (random schemes;
      a weak test: whole-scheme count, few pinched cases)                         [Cor. 3.4]
  V3  arc lemma: identity in exact fractions AND maximality by an LP over grid
      derivatives; its K = infinity form; the exact-deficit identity and midpoint
      convexity; transparent mark: run deficit == min over the interior slope      [Lemmas 5.1, 6.1, 7.3]
  V4  nu = min_x max_Gamma Q_Gamma(x): primal (SLSQP) / dual (separable) bracket,
      rigorous both ways, against the closed forms (P = {} rows are trivial)       [Thm 4.2, 4.3]
  V5  explicit C^{1,1} profiles in exact fractions (pair, two partners):
      continuity, |h'| <= K, |h''| <= c, periodicity, clearances: UPPER sides     [Prop. 4.4, Thm 7.2]
  V6  grid LP for C(K) with no theorem inside (min c, |dh| <= K dt,
      |d2h| <= c dt^2, clearances at marks). Marks lie on the grid, so the LP is
      a relaxation: a rigorous LOWER bound on C up to solver tolerance. Checked
      one-sidedly against closed forms / exact-solver values; two points just
      past predicted upward departures certify C > formula there               [Thm 4.2, Prop 4.4, 6.3, Thm 7.2; Sec. 7.3]

Run:  python3 -B fc_verify.py            (about 1-3 minutes; needs numpy, scipy)
      python3 -B fc_verify.py --quick    (skips the slower grid LPs)
Exit code 0 and the last line ALL_CHECKS_PASSED when every check holds.
"""
import itertools
import math
import random
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.sparse import coo_matrix

QUICK = "--quick" in sys.argv
RESULTS = []  # (id, ok, text)


def check(cid, ok, text):
    RESULTS.append((cid, bool(ok), text))
    print(f"[{'PASS' if ok else 'FAIL'}] {cid}: {text}", flush=True)


# --------------------------------------------------------------------------- model
class Scheme:
    """Threads on a circle of length L; marks (t, over, under, g): h_over(t) - h_under(t) >= g.

    Nodes are (thread, time) only where the thread takes part in a mark.  A thread's arcs join
    its consecutive nodes cyclically; a thread with two nodes has two distinct arcs between the
    same pair of nodes (kept apart by arc id), a thread with one node has none (held constant)."""

    def __init__(self, L, marks):
        self.L = Fr(L)
        self.marks = [(Fr(t), o, u, Fr(g)) for (t, o, u, g) in marks]
        times = {}
        for t, o, u, g in self.marks:
            times.setdefault(o, set()).add(t)
            times.setdefault(u, set()).add(t)
        self.nodes = sorted((X, t) for X in times for t in times[X])
        self.idx = {v: i for i, v in enumerate(self.nodes)}
        self.arcs = []  # (arc_id, thread, i_start, i_end, length) in time direction
        for X in sorted(times):
            ts = sorted(times[X])
            if len(ts) < 2:
                continue
            for j, t in enumerate(ts):
                t2 = ts[(j + 1) % len(ts)]
                d = (t2 - t) % self.L
                self.arcs.append((len(self.arcs), X, self.idx[(X, t)], self.idx[(X, t2)], d))
        # edges of the difference-constraint graph: H_v - H_u <= weight
        # kind 'arc': (u, v, arc_id, sigma, d)   weight K*d ; sigma=+1 along time, -1 against
        # kind 'tr' : (u, v, g)                  weight -g  (over -> under)
        self.edges = []
        for a, X, i, j, d in self.arcs:
            self.edges.append(("arc", i, j, a, +1, d))
            self.edges.append(("arc", j, i, a, -1, d))
        for t, o, u, g in self.marks:
            self.edges.append(("tr", self.idx[(o, t)], self.idx[(u, t)], g))

    # ---- cycles
    def simple_cycles(self):
        """All simple directed cycles as edge-index tuples (parallel edges give distinct cycles)."""
        n = len(self.nodes)
        out_e = [[] for _ in range(n)]
        for k, e in enumerate(self.edges):
            out_e[e[1]].append(k)
        cycles = []

        def dfs(s, u, path_nodes, path_edges):
            for k in out_e[u]:
                v = self.edges[k][2]
                if v == s:
                    cycles.append(tuple(path_edges + [k]))
                elif v > s and v not in path_nodes:
                    path_nodes.add(v)
                    dfs(s, v, path_nodes, path_edges + [k])
                    path_nodes.discard(v)

        for s in range(n):
            dfs(s, s, {s}, [])
        return cycles

    def cycle_gd(self, cyc):
        G = sum((self.edges[k][3] for k in cyc if self.edges[k][0] == "tr"), Fr(0))
        D = sum((self.edges[k][5] for k in cyc if self.edges[k][0] == "arc"), Fr(0))
        return G, D

    def kstar_exact(self):
        best = Fr(0)
        cyc = self.simple_cycles()
        for c in cyc:
            G, D = self.cycle_gd(c)
            if D == 0:
                assert G <= 0, "infeasible: positive clearance cycle inside one mark"
                continue
            best = max(best, G / D)
        self._cycles = cyc
        return best

    def kstar_lp(self):
        n = len(self.nodes)
        rows, rhs = [], []
        for e in self.edges:
            r = np.zeros(n + 1)
            if e[0] == "arc":
                _, u, v, a, s, d = e
                r[v] += 1; r[u] -= 1; r[n] = -float(d)
                rows.append(r); rhs.append(0.0)
            else:
                _, u, v, g = e
                r[v] += 1; r[u] -= 1
                rows.append(r); rhs.append(-float(g))
        c = np.zeros(n + 1); c[n] = 1.0
        res = linprog(c, A_ub=np.array(rows), b_ub=np.array(rhs),
                      bounds=[(None, None)] * n + [(0, None)], method="highs")
        assert res.status == 0, res.message
        return res.x[n]

    # ---- tight structure at K*
    def tight_by_cycles(self, K):
        tight, tcycles = set(), []
        for c in self._cycles:
            G, D = self.cycle_gd(c)
            if D > 0 and G == K * D:
                tight.update(c)
                tcycles.append(c)
        return tight, tcycles

    def tight_by_floyd(self, K):
        n = len(self.nodes)
        INF = None
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = Fr(0)
        w = []
        for e in self.edges:
            wt = K * e[5] if e[0] == "arc" else -e[3]
            w.append(wt)
            u, v = e[1], e[2]
            if dist[u][v] is None or wt < dist[u][v]:
                dist[u][v] = wt
        for k in range(n):
            dk = dist[k]
            for i in range(n):
                dik = dist[i][k]
                if dik is None:
                    continue
                di = dist[i]
                for j in range(n):
                    if dk[j] is None:
                        continue
                    s = dik + dk[j]
                    if di[j] is None or s < di[j]:
                        di[j] = s
        for i in range(n):
            assert dist[i][i] == 0, "negative cycle at K*"
        return {k for k, e in enumerate(self.edges) if dist[e[2]][e[1]] is not None and dist[e[2]][e[1]] == -w[k]}

    def pinched(self, tight):
        """Pinched node: the arcs ending and starting at it are both forced, with opposite slopes."""
        forced = {}  # arc_id -> slope sign
        for k in tight:
            e = self.edges[k]
            if e[0] == "arc":
                forced.setdefault(e[3], set()).add(e[4])
        for a in forced:
            assert len(forced[a]) == 1, "an arc forced both ways"
        sign = {a: next(iter(s)) for a, s in forced.items()}
        left, right = {}, {}
        for a, X, i, j, d in self.arcs:
            right[i] = a
            left[j] = a
        P = []
        for v in range(len(self.nodes)):
            if v in left and v in right and left[v] in sign and right[v] in sign:
                if sign[left[v]] == -sign[right[v]]:
                    P.append(v)
        return P, sign


# --------------------------------------------------------------------------- nu
def nu_bracket(S, tcycles, P, seed=0):
    """nu = min_{x in [-1,1]^P} max_Gamma Q_Gamma(x), Q = sum over ramps (1 - sigma x_r)^2 / (2 L_Gamma)."""
    if not P:
        return 0.0, 0.0
    pos = {v: i for i, v in enumerate(P)}
    data = []  # per cycle: (L_Gamma, [(r_index, sigma), ...])
    for c in tcycles:
        _, D = S.cycle_gd(c)
        ramps = []
        for k in c:
            e = S.edges[k]
            if e[0] != "arc":
                continue
            for end in (e[1], e[2]):
                if end in pos:
                    ramps.append((pos[end], e[4]))
        if ramps:
            data.append((float(D), ramps))
    m = len(P)

    def Q(x, Lg, ramps):
        return sum((1 - s * x[r]) ** 2 for r, s in ramps) / (2 * Lg)

    def qmax(x):
        return max(Q(x, Lg, rp) for Lg, rp in data)

    # primal, epigraph form
    rng = np.random.default_rng(seed)
    best_x, best = None, math.inf
    starts = [np.zeros(m)] + [rng.uniform(-1, 1, m) for _ in range(8)]
    for x0 in starts:
        z0 = np.append(x0, qmax(x0))
        cons = [{"type": "ineq", "fun": (lambda z, Lg=Lg, rp=rp: z[-1] - Q(z[:-1], Lg, rp))} for Lg, rp in data]
        res = minimize(lambda z: z[-1], z0, method="SLSQP", constraints=cons,
                       bounds=[(-1, 1)] * m + [(0, None)], options={"ftol": 1e-15, "maxiter": 500})
        val = qmax(np.clip(res.x[:-1], -1, 1))
        if val < best:
            best, best_x = val, np.clip(res.x[:-1], -1, 1)
    nu_U = best

    # dual: g(lam) = sum_r 4 A_r B_r / (A_r + B_r),  A_r, B_r = weights of ramps with sigma = +1 / -1
    nc = len(data)

    def g(lam):
        A = np.zeros(m); B = np.zeros(m)
        for l, (Lg, rp) in zip(lam, data):
            for r, s in rp:
                if s > 0:
                    A[r] += l / (2 * Lg)
                else:
                    B[r] += l / (2 * Lg)
        tot = A + B
        mask = tot > 1e-300
        return float(np.sum(4 * A[mask] * B[mask] / tot[mask]))

    best_l = -math.inf
    for trial in range(10):
        l0 = np.ones(nc) / nc if trial == 0 else rng.dirichlet(np.ones(nc))
        res = minimize(lambda l: -g(np.maximum(l, 0)), l0, method="SLSQP",
                       constraints=[{"type": "eq", "fun": lambda l: np.sum(l) - 1}],
                       bounds=[(0, 1)] * nc, options={"ftol": 1e-15, "maxiter": 500})
        lam = np.maximum(res.x, 0)
        lam = lam / lam.sum()
        best_l = max(best_l, g(lam))
    return best_l, nu_U


# --------------------------------------------------------------------------- exact profiles
class PWL:
    """Continuous piecewise-linear function given by exact breakpoints [(t, value)], t increasing."""

    def __init__(self, pts):
        self.pts = pts

    def integral(self, a, b):
        tot = Fr(0)
        for (t0, v0), (t1, v1) in zip(self.pts, self.pts[1:]):
            lo, hi = max(a, t0), min(b, t1)
            if hi <= lo:
                continue
            f = lambda t: v0 + (v1 - v0) * (t - t0) / (t1 - t0)
            tot += (f(lo) + f(hi)) * (hi - lo) / 2
        return tot

    def max_abs(self):
        return max(abs(v) for _, v in self.pts)

    def max_slope(self):
        return max(abs((v1 - v0) / (t1 - t0)) for (t0, v0), (t1, v1) in zip(self.pts, self.pts[1:]) if t1 > t0)



def shift_pwl(d, s, L):
    """The periodic PWL t -> d(t - s) on [0, L] (adds the breakpoint where the circle is cut)."""
    cut = L - s
    pts = list(d.pts)
    if all(t != cut for t, _ in pts):
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            if t0 < cut < t1:
                pts.append((cut, v0 + (v1 - v0) * (cut - t0) / (t1 - t0)))
                break
        pts.sort()
    tail = [(t - cut, v) for t, v in pts if t >= cut]
    head = [(t + s, v) for t, v in pts if t <= cut]
    return PWL(tail + head[1:])


def min3_profile(K, a, b, c, t0, t1, sign=1):
    """sign * min(K, a + c(t - t0), b + c(t1 - t)) on [t0, t1] as exact breakpoints (a, b in sign-frame)."""
    cand = {t0, t1}
    for t in (t0 + (K - a) / c, t1 - (K - b) / c, (b - a + c * (t0 + t1)) / (2 * c)):
        if t0 < t < t1:
            cand.add(t)
    pts = []
    for t in sorted(cand):
        v = min(K, a + c * (t - t0), b + c * (t1 - t))
        pts.append((t, sign * v))
    return pts


def join(*pieces):
    pts = []
    for p in pieces:
        if pts:
            assert pts[-1][0] == p[0][0]
            if pts[-1][1] != p[0][1]:
                return None  # derivative discontinuity
            pts.extend(p[1:])
        else:
            pts.extend(p)
    return PWL(pts)


def check_profile(name, K, c, ders, L, clearances, starts):
    """ders: thread -> PWL derivative on [0, L]; starts: thread -> h(0); clearances: (t, over, under, g)."""
    ok = True
    notes = []
    for X, d in ders.items():
        if d is None:
            return False, f"{name}: derivative of a thread is discontinuous"
        if d.pts[0][1] != d.pts[-1][1]:
            ok = False; notes.append(f"{X}: h' not periodic")
        if d.integral(Fr(0), L) != 0:
            ok = False; notes.append(f"{X}: h not periodic")
        if d.max_abs() > K:
            ok = False; notes.append(f"{X}: |h'| > K")
        if d.max_slope() > c:
            ok = False; notes.append(f"{X}: |h''| > c")
    h = lambda X, t: starts[X] + ders[X].integral(Fr(0), t)
    slack = []
    for t, o, u, g in clearances:
        s = h(o, Fr(t)) - h(u, Fr(t)) - g
        slack.append(s)
        if s < 0:
            ok = False; notes.append(f"clearance at {t} violated by {s}")
    return ok, f"{name}: K={K}, c={c}, slacks={[str(s) for s in slack]}" + ("" if ok else "; " + "; ".join(notes))


# --------------------------------------------------------------------------- grid LP
def grid_lp_C(S, K, N):
    """min c over grid functions: |h_{i+1}-h_i| <= K dt, |h_{i+1}-2h_i+h_{i-1}| <= c dt^2, clearances."""
    L = S.L
    dt = L / N
    threads = sorted({X for X, _ in S.nodes})
    T = len(threads)
    ti = {X: j for j, X in enumerate(threads)}
    nv = T * N + 1
    cidx = T * N
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    Kdt = float(K * dt)
    dt2 = float(dt * dt)
    for X in threads:
        base = ti[X] * N
        for i in range(N):
            a, b, z = base + i, base + (i + 1) % N, base + (i - 1) % N
            for s in (1, -1):  # s*(h_b - h_a) <= K dt
                rows += [r, r]; cols += [b, a]; vals += [s, -s]; rhs.append(Kdt); r += 1
            for s in (1, -1):  # s*(h_b - 2h_a + h_z) - c dt^2 <= 0
                rows += [r, r, r, r]; cols += [b, a, z, cidx]; vals += [s, -2 * s, s, -dt2]; rhs.append(0.0); r += 1
    for t, o, u, g in S.marks:
        k = t / dt
        assert k.denominator == 1, "mark not on grid"
        k = int(k) % N
        rows += [r, r]; cols += [ti[u] * N + k, ti[o] * N + k]; vals += [1, -1]; rhs.append(-float(g)); r += 1
    A = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
    cost = np.zeros(nv); cost[cidx] = 1.0
    bounds = [(None, None)] * (T * N) + [(0, None)]
    res = linprog(cost, A_ub=A, b_ub=np.array(rhs), bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return res.x[cidx]


# --------------------------------------------------------------------------- schemes
NAMED = {
    "pair": (12, [(0, "A", "B", 1), (6, "B", "A", 1)]),
    "two partners": (12, [(0, "A", "B", 1), (3, "B", "A", 1), (6, "A", "C", 1), (9, "C", "A", 1)]),
    "irrational": (12, [(0, "B", "A", 1), (2, "A", "B", 1), (4, "B", "A", 1), (6, "B", "A", 1), (8, "A", "B", 1), (10, "A", "B", 1)]),
    "connected T": (12, [(0, "A", "B", 6), (6, "B", "A", 6), (0, "X", "Y", 1), (1, "Y", "X", 1), (0, "X", "Z", 4), (8, "Z", "X", 4), (0, "A", "Y", 4), (1, "Y", "B", 2)]),
    "#1": (12, [(0, "B", "A", 1), (3, "A", "B", 1), (6, "B", "A", 1), (9, "A", "B", 1)]),
    "#3": (12, [(0, "D", "A", 1), (3, "C", "D", 1), (6, "B", "D", 1), (9, "D", "B", 1), (9, "A", "D", 1)]),
    "#5": (12, [(0, "D", "A", 1), (0, "C", "A", 1), (2, "B", "A", 1), (4, "A", "D", 1), (6, "C", "D", 1), (6, "A", "C", 1), (10, "C", "B", 1), (10, "C", "A", 1)]),
    "short arc 1/8": (12, [(0, "A", "B", 1), (6, "B", "A", 1), (3, "A", "C", 1), (Fr(25, 8), "C", "A", 1)]),
    "asym-1": (12, [(0, "A", "B", Fr(2, 3)), (2, "B", "A", Fr(2, 3)), (3, "A", "C", Fr(4, 3)), (7, "C", "A", Fr(4, 3))]),
    "asym-2": (12, [(0, "A", "B", Fr(1, 3)), (1, "B", "A", Fr(1, 3)), (4, "A", "C", Fr(5, 3)), (9, "C", "A", Fr(5, 3))]),
    "asym-3": (12, [(0, "A", "B", Fr(1, 3)), (1, "B", "A", Fr(1, 3)), (0, "A", "C", 1), (3, "C", "A", 1), (6, "A", "D", 1), (9, "D", "A", 1)]),
    # small examples of Sections 2-3
    "cyclic triple (Prosvet)": (12, [(0, "A", "B", 1), (4, "B", "C", 1), (8, "C", "A", 1)]),
    "triple 0,1,7.5 L=10": (10, [(0, "A", "B", 1), (1, "B", "C", 1), (Fr(15, 2), "C", "A", 1)]),
    "full order A>B>C / C>B>A": (12, [(0, "A", "B", 1), (0, "B", "C", 1), (3, "C", "B", 1), (3, "B", "A", 1)]),
    "GLM example L=2": (2, [(0, "A", "B", 1), (0, "A", "C", 1), (0, "B", "C", 100),
                            (1, "A", "C", 1), (1, "A", "B", 1), (1, "C", "B", 100)]),
}
S2, S5 = math.sqrt(2), math.sqrt(5)
KSTAR = {"pair": Fr(1, 6), "two partners": Fr(1, 3), "irrational": Fr(1, 2), "connected T": Fr(1), "#1": Fr(1, 3),
         "#3": Fr(1, 3), "#5": Fr(1, 4), "short arc 1/8": Fr(8), "asym-1": Fr(1, 3), "asym-2": Fr(1, 3), "asym-3": Fr(1, 3),
         "cyclic triple (Prosvet)": Fr(1, 4), "triple 0,1,7.5 L=10": Fr(3, 7), "full order A>B>C / C>B>A": Fr(2, 3),
         "GLM example L=2": Fr(100)}
NU = {"pair": 1 / 6, "two partners": 1 / 6, "irrational": 6 - 4 * S2, "connected T": 1 / 6, "#1": 1 / 3, "#3": 1 / 12,
      "#5": 1 / 6, "short arc 1/8": 0.0, "asym-1": 3 - 2 * S2, "asym-2": (3 - S5) / 4, "asym-3": 4 / (1 + S2 + math.sqrt(6)) ** 2,
      "cyclic triple (Prosvet)": 0.0, "triple 0,1,7.5 L=10": 0.0, "full order A>B>C / C>B>A": 0.0}
NU_TOL = {}  # asym-3 closed form 4/(1+sqrt2+sqrt6)^2 found 2026-11-07 (asym3_closed_form.py)


def random_scheme(rng):
    L = 12
    threads = ["A", "B", "C"]
    while True:
        k = rng.randint(2, 5)
        ts = sorted(rng.sample(range(12), k))
        marks = []
        for t in ts:
            for _ in range(rng.randint(1, 2)):
                o, u = rng.sample(threads, 2)
                marks.append((t, o, u, rng.choice([1, 2, 3])))
        # feasibility inside a mark: the 'over' relation at one time must be acyclic
        bad = False
        for t in ts:
            rel = {(o, u) for (tt, o, u, g) in marks if tt == t}
            if any((u, o) in rel for (o, u) in rel):
                bad = True
            for (o, u) in rel:
                for (u2, w) in rel:
                    if u2 == u and (w, o) in rel:
                        bad = True
        if not bad:
            return Scheme(L, marks)


# --------------------------------------------------------------------------- main
def main():
    t_start = time.time()
    print("Floating clearance verification suite v0.1-wip;", sys.version.split()[0],
          "numpy", np.__version__, flush=True)
    schemes = {name: Scheme(L, mk) for name, (L, mk) in NAMED.items()}

    # V1 + V2 on named schemes
    info = {}
    for name, S in schemes.items():
        K = S.kstar_exact()
        Klp = S.kstar_lp()
        check("V1.kstar." + name, K == KSTAR[name] and abs(Klp - float(K)) < 1e-9,
              f"K* exact {K} (expected {KSTAR[name]}), LP {Klp:.12f}")
        tc, tcyc = S.tight_by_cycles(K)
        tf = S.tight_by_floyd(K)
        P, sign = S.pinched(tc)
        check("V2.tight." + name, tc == tf,
              f"{len(tc)} tight edges by cycles == by Floyd; {len(tcyc)} tight simple cycles; pinched nodes "
              f"{[S.nodes[v][0] + '@' + str(S.nodes[v][1]) for v in P]}")
        info[name] = (S, K, tcyc, P)

    # V2b: random schemes, pinching needs at least two tight cycles; Floyd == cycles
    rng = random.Random(20261107)
    n_rand = 60 if QUICK else 200
    n_pinched, viol, mismatch = 0, 0, 0
    for _ in range(n_rand):
        S = random_scheme(rng)
        K = S.kstar_exact()
        if K == 0:
            continue
        tc, tcyc = S.tight_by_cycles(K)
        if tc != S.tight_by_floyd(K):
            mismatch += 1
        P, _ = S.pinched(tc)
        if P:
            n_pinched += 1
            if len(tcyc) < 2:
                viol += 1
    check("V2.random", viol == 0 and mismatch == 0,
          f"{n_rand} random schemes (seed 20261107): {n_pinched} with pinched nodes, all with >= 2 tight cycles; "
          f"Floyd/cycles mismatches {mismatch}")

    # V3 exact identities
    rr = random.Random(7)

    def rf(lo, hi, den=97):
        return Fr(rr.randint(int(lo * den), int(hi * den)), den)

    bad = 0
    n_ok = 0
    for _ in range(1500):
        K = rf(Fr(1, 4), 3); c = rf(Fr(1, 10), 5); d = rf(Fr(1, 10), 6)
        a = rf(-K, K); b = rf(-K, K)
        if abs(a - b) > c * d:
            continue
        n_ok += 1
        prof = PWL(min3_profile(K, a, b, c, Fr(0), d))
        delta = max(Fr(0), (2 * K - a - b - c * d) / 2)
        R = K * d - ((K - a) ** 2 + (K - b) ** 2) / (2 * c) + delta ** 2 / c
        if prof.integral(Fr(0), d) != R:
            bad += 1
    check("V3.arc_lemma", bad == 0, f"R(a,b) closed form == exact integral of min(K, a+ct, b+c(d-t)) on {n_ok} random rational cases")

    bad = 0
    for _ in range(1000):
        c = rf(Fr(1, 10), 5); d = rf(Fr(1, 10), 6)
        a = rf(-4, 4); b = a + rf(-1, 1) * c * d
        p_star = (a + b + c * d) / 2
        tent = (2 * p_star ** 2 - a * a - b * b) / (2 * c)
        m = (a + b) * d / 2
        W = c * d * d / 4 - (a - b) ** 2 / (4 * c)
        prof = PWL(min3_profile(abs(a) + abs(b) + c * d + 1, a, b, c, Fr(0), d))  # cap never active
        if not (tent == m + W == prof.integral(Fr(0), d)):
            bad += 1
    check("V3.arc_lemma_K_inf", bad == 0, "max integral without slope cap == m + W (tent), 1000 cases")

    def F1(p, q, m):
        return (p * p + q * q) / 2 - (max(Fr(0), p + q - m) / 2) ** 2

    def F2(p, q, m):
        return m * (p + q) / 2 - m * m / 4 + (p - q) ** 2 / 4 + max(Fr(0), m - p - q) ** 2 / 4

    bad = badc = 0
    for _ in range(3000):
        m = rf(Fr(1, 20), 5); p, q = rf(0, 2), rf(0, 2); p2, q2 = rf(0, 2), rf(0, 2)
        if F1(p, q, m) != F2(p, q, m):
            bad += 1
        if F1((p + p2) / 2, (q + q2) / 2, m) > (F1(p, q, m) + F1(p2, q2, m)) / 2:
            badc += 1
    check("V3.exact_deficit", bad == 0 and badc == 0,
          "F(p,q;m) = (p^2+q^2)/2 - ((p+q-m)_+/2)^2 equals the convex form; midpoint convexity holds (3000 cases)")
    bad = 0
    for _ in range(500):
        m1 = rf(Fr(1, 50), Fr(49, 50)); m2 = rf(1 - m1, 4)
        if F1(Fr(1), 1 - m1, m1) + F1(1 - m1, Fr(0), m2) != Fr(1, 2) or F1(Fr(1), Fr(0), m1 + m2) != Fr(1, 2):
            bad += 1
    check("V3.transparent_mark.special", bad == 0, "F(1,1-m1;m1) + F(1-m1,0;m2) = 1/2 = F(1,0;m1+m2) for m1 < 1 <= m1+m2 (500 cases)")

    # general transparent mark: F(p,q;m1+m2) == min over the interior ramp height r in [0,2] with
    # |p-r| <= m1, |r-q| <= m2 of F(p,r;m1) + F(r,q;m2)   (convex in r: golden-section search, floats)
    def Ff(p, q, m):
        return (p * p + q * q) / 2 - (max(0.0, p + q - m) / 2) ** 2

    rg = random.Random(11)
    worst, cnt = 0.0, 0
    while cnt < 3000:
        p_, q_ = rg.uniform(0, 2), rg.uniform(0, 2)
        m1, m2 = rg.uniform(0.02, 3), rg.uniform(0.02, 3)
        lo_r, hi_r = max(0.0, p_ - m1, q_ - m2), min(2.0, p_ + m1, q_ + m2)
        if lo_r > hi_r or abs(p_ - q_) > m1 + m2:
            continue
        cnt += 1
        f = lambda r: Ff(p_, r, m1) + Ff(r, q_, m2)
        a_, b_ = lo_r, hi_r
        gr = (math.sqrt(5) - 1) / 2
        for _ in range(200):
            c1, c2 = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
            if f(c1) <= f(c2):
                b_ = c2
            else:
                a_ = c1
        worst = max(worst, abs(f((a_ + b_) / 2) - Ff(p_, q_, m1 + m2)))
    check("V3.transparent_mark.general", worst < 1e-9,
          f"run deficit F(p,q;m1+m2) == min_r [F(p,r;m1) + F(r,q;m2)] on 3000 random feasible cases; max |diff| {worst:.1e}")

    # arc lemma maximality: LP over grid derivative values (|p| <= K, |dp| <= c h, ends fixed), trapezoid integral
    rl = random.Random(5)
    worst, cnt, tents = 0.0, 0, 0
    Ng = 400
    while cnt < (8 if QUICK else 30):
        K_ = rl.uniform(0.3, 2); c_ = rl.uniform(0.2, 4); d_ = rl.uniform(0.3, 4)
        a_, b_ = rl.uniform(-K_, K_), rl.uniform(-K_, K_)
        if abs(a_ - b_) > c_ * d_:
            continue
        cnt += 1
        h = d_ / Ng
        wts = np.full(Ng + 1, h); wts[0] = wts[-1] = h / 2
        rows, rhs = [], []
        for i in range(Ng):
            for sgn in (1, -1):
                r_ = np.zeros(Ng + 1); r_[i + 1] = sgn; r_[i] = -sgn
                rows.append(r_); rhs.append(c_ * h)
        bnds = [(-K_, K_)] * (Ng + 1); bnds[0] = (a_, a_); bnds[-1] = (b_, b_)
        res = linprog(-wts, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=bnds, method="highs")
        delta = max(0.0, (2 * K_ - a_ - b_ - c_ * d_) / 2)
        if delta > 0:
            tents += 1
        Rv = K_ * d_ - ((K_ - a_) ** 2 + (K_ - b_) ** 2) / (2 * c_) + delta ** 2 / c_
        worst = max(worst, abs(-res.fun - Rv) / max(1.0, abs(Rv)))
    check("V3.arc_lemma_maximal", worst < 5e-5,
          f"LP maximum of the integral over grid profiles (N={Ng}) == R(a,b) on {cnt} random cases ({tents} tents); max rel diff {worst:.1e}")

    # V4 nu
    for name, (S, K, tcyc, P) in info.items():
        if name not in NU:
            continue
        lo, hi = nu_bracket(S, tcyc, P)
        tol = NU_TOL.get(name, 1e-7)
        ok = (lo <= hi + 1e-12) and (hi - lo < 1e-6) and abs(hi - NU[name]) < tol and abs(lo - NU[name]) < tol
        triv = " (trivial: P is empty, nu = 0 by definition)" if not P else ""
        check("V4.nu." + name, ok, f"nu in [{lo:.10f}, {hi:.10f}], expected {NU[name]:.10f}; |P| = {len(P)}{triv}")

    # V5 exact profiles
    L = Fr(12)
    for kappa in (Fr(6, 5), Fr(3, 2), Fr(2)):  # pair, kappa <= 2: c = K^2/(6 eps)
        K = kappa / 6; eps = K - Fr(1, 6); c = K * K / (6 * eps)
        dA = join(min3_profile(K, Fr(0), Fr(0), c, Fr(0), Fr(6), -1), min3_profile(K, Fr(0), Fr(0), c, Fr(6), Fr(12), +1))
        dB = PWL([(t, -v) for t, v in dA.pts])
        ok, txt = check_profile(f"pair kappa={kappa}", K, c, {"A": dA, "B": dB}, L, NAMED["pair"][1],
                                {"A": Fr(1, 2), "B": Fr(-1, 2)})
        check(f"V5.pair.{kappa}", ok, txt + " (upper side: C <= (2/L)K^2/eps)")
    for kappa in (Fr(5, 2), Fr(4)):  # pair, kappa >= 2: c = 8K*/L = 1/9 (slope cap inactive)
        K = kappa / 6; c = Fr(1, 9)
        dA = join(min3_profile(K, Fr(0), Fr(0), c, Fr(0), Fr(6), -1), min3_profile(K, Fr(0), Fr(0), c, Fr(6), Fr(12), +1))
        dB = PWL([(t, -v) for t, v in dA.pts])
        ok, txt = check_profile(f"pair kappa={kappa}", K, c, {"A": dA, "B": dB}, L, NAMED["pair"][1],
                                {"A": Fr(1, 2), "B": Fr(-1, 2)})
        check(f"V5.pair.{kappa}", ok, txt + " (upper side: C <= 8K*/L)")
    for kappa in (Fr(4, 3), Fr(3, 2), Fr(9, 5), Fr(2)):  # two partners, 4/3 <= kappa <= 2
        K = kappa / 3; eps = K - Fr(1, 3); c = K * K / (6 * eps); a = 3 * c / 2
        tent = lambda t0, s: [(t0, Fr(0)), (t0 + Fr(3, 2), s * a), (t0 + 3, Fr(0))]
        dA = join(tent(Fr(0), -1), tent(Fr(3), 1), tent(Fr(6), -1), tent(Fr(9), 1))
        up = min3_profile(K, a, a, c, Fr(0), Fr(3), +1)
        down = min3_profile(K, -a, -a, c, Fr(3), Fr(12), -1)
        dB = join(up, down)
        dC = shift_pwl(dB, Fr(6), L)  # C is B moved by 6 on the circle
        starts = {"A": Fr(0), "B": Fr(-1)}
        hA6 = dA.integral(Fr(0), Fr(6))
        starts["C"] = hA6 - 1 - dC.integral(Fr(0), Fr(6))
        ok, txt = check_profile(f"two partners kappa={kappa}", K, c, {"A": dA, "B": dB, "C": dC}, L,
                                NAMED["two partners"][1], starts)
        check(f"V5.partners.{kappa}", ok, txt + " (upper side: C <= K^2/(6 eps))")

    # V6 grid LP
    if QUICK:
        print("(--quick: grid LP checks skipped)")
    else:
        N = 1200
        jobs = []
        for kappa in (1.2, 1.5, 2.0, 3.0):
            Ks = 1 / 6; K = kappa * Ks; eps = K - Ks
            exp = (2 / 12) * K * K / eps if kappa <= 2 else 8 * Ks / 12
            jobs.append(("pair", kappa, exp, "closed form 02.11"))
        for kappa in (1.2, 1.5, 1.8, 2.5):
            Ks = 1 / 3; K = kappa * Ks; eps = K - Ks
            exp = K * K / (6 * eps) if kappa <= 2 else 2 / 9
            jobs.append(("two partners", kappa, exp, "closed form 06.11"))
        jobs.append(("irrational", 1.3, None, "Theorem 4.2 formula (below kappa_A = 1.7071)"))
        jobs.append(("asym-1", 1.06, None, "Theorem 4.2 formula (downward departure at 1.093836)"))
        jobs.append(("asym-1", 1.15, ("normalized", 0.16172), "exact solver C*eps/K^2 = 0.16172, below formula (downward departure)"))
        jobs.append(("asym-2", 1.15, ("normalized", 0.195353), "exact solver C*eps/K^2 = 0.195353, above formula (upward departure)"))
        jobs.append(("#3", 1.1, None, "Theorem 4.2 formula (upward departure only at 8/7)"))
        jobs.append(("asym-2", 1.09, None, "Theorem 4.2 formula (upward departure at 2 - 2 sqrt5/5 = 1.10557)"))
        jobs.append(("#3", 1.16, "UP", "past the predicted upward departure 8/7 = 1.142857"))
        jobs.append(("asym-2", 1.12, "UP", "past the predicted upward departure 1.105573"))
        for name, kappa, exp, src in jobs:
            S, Kst, _, _ = info[name]
            K = Fr(kappa).limit_denominator(1000) * Kst
            eps = float(K - Kst)
            form = NU[name] * float(K) ** 2 / eps
            t0 = time.time()
            val = grid_lp_C(S, K, N)
            if exp == "UP":  # the LP is a lower bound on C: LP > formula certifies C > formula
                rel = val / form - 1
                check(f"V6.gridLP.{name}.{kappa}", rel > 1e-3,
                      f"grid LP N={N} (lower bound on C) = {val:.6f} > formula nu K^2/eps = {form:.6f} by {rel:+.2e} "
                      f"({src}): C departs upward; {time.time() - t0:.1f} s")
                continue
            if exp is None:
                exp = form
            elif isinstance(exp, tuple):  # workbench values are recorded as C*eps/K^2
                exp = exp[1] * float(K) ** 2 / eps
            rel = val / exp - 1
            side = "" if abs(val / form - 1) < 2.5e-3 else (" [below formula]" if val < form else " [above formula]")
            # one-sided: LP <= C (relaxation, solver tolerance 1e-8) and LP >= C (1 - 3e-4) (grid resolution)
            check(f"V6.gridLP.{name}.{kappa}", -3e-4 <= rel <= 1e-8,
                  f"grid LP N={N}: C = {val:.6f}, expected {exp:.6f} ({src}); rel {rel:+.2e}; formula nu K^2/eps = {form:.6f}"
                  f"{side}; {time.time() - t0:.1f} s")

    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{len(RESULTS)} checks, {n_fail} failed, {time.time() - t_start:.0f} s")
    if n_fail:
        for cid, ok, text in RESULTS:
            if not ok:
                print("FAILED:", cid, text)
        print("SOME_CHECKS_FAILED")
        sys.exit(1)
    print("ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
