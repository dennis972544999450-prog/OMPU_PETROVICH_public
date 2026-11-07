"""Probe 3: lemmas in regimes the script does not sample.
(a) Lemma 5.1 MAXIMALITY (V3 only integrates the claimed maximiser): maximise the integral by an LP over grid
    derivatives (|p|<=K, |p_{i+1}-p_i|<=c dt, fixed ends) and compare with R(a,b), including tent cases.
(b) Transparent marks in general: min over the interior slope t of F(p,1-t;m1)+F(1-t,q;m2) (with side conditions
    |p-(1-t)|<=m1, |(1-t)-q|<=m2, t in [-1,1]) against F(p,q;m1+m2), random p,q in [0,2] (V3 checks only p=1,q=0,t=m1).
(c) F non-decreasing and concave in m (stated in Lemma 7.3, not checked by the script)."""
import random
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

rng = random.Random(11)


def R(K, a, b, c, d):
    delta = max(0.0, (2 * K - a - b - c * d) / 2)
    return K * d - ((K - a) ** 2 + (K - b) ** 2) / (2 * c) + delta ** 2 / c


def lp_max(K, a, b, c, d, N=4000):
    dt = d / N
    # variables p_0..p_N ; maximise trapezoid integral
    n = N + 1
    cost = np.full(n, -dt); cost[0] = cost[-1] = -dt / 2
    A = []
    rhs = []
    from scipy.sparse import lil_matrix
    M = lil_matrix((2 * N, n))
    for i in range(N):
        M[2 * i, i + 1] = 1; M[2 * i, i] = -1
        M[2 * i + 1, i + 1] = -1; M[2 * i + 1, i] = 1
    rhs = np.full(2 * N, c * dt)
    bounds = [(-K, K)] * n
    bounds[0] = (a, a); bounds[-1] = (b, b)
    res = linprog(cost, A_ub=M.tocsr(), b_ub=rhs, bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return -res.fun


worst = 0.0
ntent = 0
for _ in range(60):
    K = rng.uniform(0.3, 3); c = rng.uniform(0.1, 5); d = rng.uniform(0.2, 6)
    a = rng.uniform(-K, K); b = rng.uniform(-K, K)
    if abs(a - b) > c * d:
        continue
    r = R(K, a, b, c, d)
    v = lp_max(K, a, b, c, d)
    ntent += (2 * K - a - b - c * d) > 0
    worst = max(worst, abs(v - r) / max(1.0, abs(r)))
print(f"probe3a: Lemma 5.1 max vs grid-LP maximum: worst rel diff {worst:.2e} ({ntent} tent cases)")


def F(p, q, m):
    return (p * p + q * q) / 2 - (max(0.0, p + q - m) / 2) ** 2


worst = 0.0
argviol = 0
for _ in range(3000):
    p = rng.uniform(0, 2); q = rng.uniform(0, 2)
    m1 = rng.uniform(0.02, 3); m2 = rng.uniform(0.02, 3)
    if abs(p - q) > m1 + m2:
        continue
    # interior ramp height s = 1 - t in [0,2]; feasible interval from side conditions
    lo = max(0.0, p - m1, q - m2); hi = min(2.0, p + m1, q + m2)
    if lo > hi + 1e-12:
        argviol += 1
        continue
    ss = np.linspace(lo, hi, 20001)
    vals = np.array([F(p, s, m1) + F(s, q, m2) for s in ss])
    best = vals.min()
    target = F(p, q, m1 + m2)
    worst = max(worst, abs(best - target))
print(f"probe3b: min_t [F(p,1-t;m1)+F(1-t,q;m2)] vs F(p,q;m1+m2): worst abs diff {worst:.2e} "
      f"(grid step 1e-4 relative to the interval); infeasible splits {argviol}")

bad_mono = bad_conc = 0
for _ in range(5000):
    p = rng.uniform(0, 2); q = rng.uniform(0, 2)
    m1 = rng.uniform(abs(p - q), 5); m2 = rng.uniform(abs(p - q), 5)
    lo_, hi_ = min(m1, m2), max(m1, m2)
    if F(p, q, hi_) < F(p, q, lo_) - 1e-14:
        bad_mono += 1
    if F(p, q, (m1 + m2) / 2) < (F(p, q, m1) + F(p, q, m2)) / 2 - 1e-14:
        bad_conc += 1
print(f"probe3c: F in m: monotonicity violations {bad_mono}, concavity violations {bad_conc} (5000 cases)")
