import os
"""Shared helpers for the review probes. Imports the frozen fc_verify.py read-only (no bytecode)."""
import sys
sys.dont_write_bytecode = True
SNAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "verify")  # package copy: the revised script (review ran on the v0.1 snapshot)
sys.path.insert(0, SNAP)
import fc_verify as fv  # noqa: E402  (main() is guarded by __name__)

import numpy as np  # noqa: E402
from fractions import Fraction as Fr  # noqa: E402
from scipy.optimize import linprog  # noqa: E402
from scipy.sparse import coo_matrix  # noqa: E402


def grid_lp_kstar(S, N):
    """min K over grid functions with |h_{i+1}-h_i| <= K dt and clearances at marks (no theorem inside)."""
    L = S.L
    dt = L / N
    threads = sorted({X for X, _ in S.nodes})
    ti = {X: j for j, X in enumerate(threads)}
    T = len(threads)
    nv = T * N + 1
    kc = T * N
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for X in threads:
        base = ti[X] * N
        for i in range(N):
            a, b = base + i, base + (i + 1) % N
            for s in (1, -1):
                rows += [r, r, r]; cols += [b, a, kc]; vals += [s, -s, -float(dt)]; rhs.append(0.0); r += 1
    for t, o, u, g in S.marks:
        k = t / dt
        assert k.denominator == 1
        k = int(k) % N
        rows += [r, r]; cols += [ti[u] * N + k, ti[o] * N + k]; vals += [1, -1]; rhs.append(-float(g)); r += 1
    A = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
    cost = np.zeros(nv); cost[kc] = 1.0
    res = linprog(cost, A_ub=A, b_ub=np.array(rhs), bounds=[(None, None)] * (T * N) + [(0, None)], method="highs")
    assert res.status == 0, res.message
    return res.x[kc]


def grid_lp_minK_at_c(S, c, N):
    """min K over grid functions with |d2h| <= c dt^2, |dh| <= K dt, clearances (relaxation => lower bound on K1(c))."""
    L = S.L
    dt = L / N
    threads = sorted({X for X, _ in S.nodes})
    ti = {X: j for j, X in enumerate(threads)}
    T = len(threads)
    nv = T * N + 1
    kc = T * N
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    dt2 = float(dt * dt)
    for X in threads:
        base = ti[X] * N
        for i in range(N):
            a, b, z = base + i, base + (i + 1) % N, base + (i - 1) % N
            for s in (1, -1):
                rows += [r, r, r]; cols += [b, a, kc]; vals += [s, -s, -float(dt)]; rhs.append(0.0); r += 1
            for s in (1, -1):
                rows += [r, r, r]; cols += [b, a, z]; vals += [s, -2 * s, s]; rhs.append(c * dt2); r += 1
    for t, o, u, g in S.marks:
        k = t / dt
        assert k.denominator == 1
        k = int(k) % N
        rows += [r, r]; cols += [ti[u] * N + k, ti[o] * N + k]; vals += [1, -1]; rhs.append(-float(g)); r += 1
    A = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
    cost = np.zeros(nv); cost[kc] = 1.0
    res = linprog(cost, A_ub=A, b_ub=np.array(rhs), bounds=[(None, None)] * (T * N) + [(0, None)], method="highs")
    if res.status != 0:
        return None
    return res.x[kc]
