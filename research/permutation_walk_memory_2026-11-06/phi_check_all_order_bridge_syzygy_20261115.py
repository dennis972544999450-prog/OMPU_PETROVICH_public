#!/usr/bin/env python3
# phi_check_all_order_bridge_syzygy_20261115.py
# -----------------------------------------------------------------------------
# Φ-Hausmaster, second eye on jee-agy 1794756477 (16:00 CET, 15.11.2026):
# the all-order theorem P_{4K+1}(x) <-> Q_{4K}(x).
#
# Checked BY MY OWN HAND, NOT their code:
#  * dict-polynomial ops of my own (no import of their module);
#  * Q_K(2x-1) assembled from my own Im-binomial of (y+i)^{4K+1};
#  * the load-bearing lever: the staircase C_{2n} is regenerated from MY OWN
#    turn operator T = reflect o (double integral), seed g0 = 1-x -- the same
#    `turn` I used in phi_check_turn_operator_spectrum_20261115.py. If MY
#    independently-built staircase also annihilates THEIR P_{4K+1}, the
#    orthogonality is real, not an artifact of their apply_turn_T.
#
# Claims under test (K = 1..6, i.e. p = 5,9,13,17,21,25; n = 0..6):
#  (a) P_{4K+1}(0) = P_{4K+1}(1) = 0           (vanish on supp Bernoulli(1/4))
#  (b) (1/4) P'_{4K+1}(x) = Q_{4K}(x), monic of degree 4K
#  (c) \int_0^1 Q_{4K}(x) dx = 0               (Unif[0,1] orthogonality)
#  (d) \int_0^1 P_{4K+1}(x) C_{2n}(x) dx = 0   (staircase, MY OWN C_{2n})
#  plus K=1 byte-check of Cloud Jee's hand P_5 and Q_4.
#
# Run: /Users/denbell/OMPU_Jee/venv/bin/python3 -I -B phi_check_all_order_bridge_syzygy_20261115.py
from fractions import Fraction as F
from math import comb

# ---- my own dict-polynomial helpers (key = degree, val = Fraction) ----------
def padd(*ps):
    o = {}
    for p in ps:
        for k, a in p.items():
            o[k] = o.get(k, F(0)) + a
    return {k: a for k, a in o.items() if a != 0}

def pscale(p, s):
    s = F(s)
    return {k: a * s for k, a in p.items() if a * s != 0}

def pmul(a, b):
    o = {}
    for i, ca in a.items():
        for j, cb in b.items():
            o[i + j] = o.get(i + j, F(0)) + ca * cb
    return {k: v for k, v in o.items() if v != 0}

def ppow(p, e):
    r = {0: F(1)}
    while e:
        if e & 1:
            r = pmul(r, p)
        p = pmul(p, p)
        e >>= 1
    return r

def pderiv(p):
    return {k - 1: a * k for k, a in p.items() if k >= 1}

def peval(p, x):
    x = F(x)
    return sum(a * x ** k for k, a in p.items())

def pint01(p):
    return sum(a / F(k + 1) for k, a in p.items())

# ---- my own turn operator: T f = reflect o double-integral, seed 1-x --------
# (identical convention to phi_check_turn_operator_spectrum_20261115.py)
def turn(p):
    g = {}
    for k, a in p.items():
        g[k + 2] = g.get(k + 2, F(0)) + a * F(1, (k + 1) * (k + 2))
    out = {}
    for n, c in g.items():
        combv = 1
        for j in range(n + 1):
            out[j] = out.get(j, F(0)) + c * combv * ((-1) ** j)
            combv = combv * (n - j) // (j + 1)
    return {k: v for k, v in out.items() if v != 0}

# ---- master syzygy Q_K(2x-1) from my own Im-binomial ------------------------
def Q_K_in_x(K):
    y = {0: F(-1), 1: F(2)}            # y = 2x - 1
    deg = 4 * K + 1
    res = ppow(y, deg)                 # y^{4K+1}
    pref = F((-1) ** K, 2 * (4 ** K))
    # Im[(y+i)^deg] = sum_t (-1)^t C(deg, 2t+1) y^{deg-2t-1}
    for t in range(2 * K + 1):
        coeff = pref * F(((-1) ** t) * comb(deg, 2 * t + 1))
        res = padd(res, pscale(ppow(y, deg - 2 * t - 1), coeff))
    return res

def P_4K1_in_x(K):
    qk = Q_K_in_x(K)
    chord = {0: F(-1, 2), 1: F(2)}     # 2x - 1/2
    diff = padd(qk, pscale(chord, -1))
    return pscale(diff, F(1, (4 * K + 1) * (2 ** (4 * K - 1))))

# ---- my own staircase C_{2n} ------------------------------------------------
def build_staircase(nmax):
    g = [{0: F(1), 1: F(-1)}]          # g0 = 1 - x
    for _ in range(2 * nmax):
        g.append(turn(g[-1]))
    C = []
    for n in range(nmax + 1):
        acc = {}
        for j in range(2 * n + 1):
            term = pscale(pmul(g[j], g[2 * n - j]), (-1) ** j)
            acc = padd(acc, term)
        C.append(acc)
    return C

def main():
    report = {}
    # byte-check of Cloud Jee's hand-derived K=1 polynomials
    P5 = P_4K1_in_x(1)
    exp_P5 = {1: F(1, 5), 2: F(-5, 4), 3: F(5, 2), 4: F(-9, 4), 5: F(4, 5)}
    assert P5 == exp_P5, f"P5 byte-check FAILED: {P5}"
    Q4 = pscale(pderiv(P5), F(1, 4))
    exp_Q4 = {0: F(1, 20), 1: F(-5, 8), 2: F(15, 8), 3: F(-9, 4), 4: F(1)}
    assert Q4 == exp_Q4, f"Q4 byte-check FAILED: {Q4}"
    report["K1_byte_check_P5_Q4"] = "MATCH (Cloud Jee's hand reproduced)"

    C = build_staircase(6)
    # independent anchor: my staircase seed and first turn, sanity masses <1,T^m 1>
    report["staircase_mass_I0_m0..3"] = [str(pint01(pmul({0: F(1)}, c))) for c in [C[0]]]

    for K in range(1, 7):
        p = 4 * K + 1
        P = P_4K1_in_x(K)
        # (a) boundary vanishing on {0,1}
        v0, v1 = peval(P, 0), peval(P, 1)
        assert v0 == 0 and v1 == 0, f"K={K}: P(0)={v0} P(1)={v1}"
        # (b) quarter-derivative is monic degree 4K
        Q = pscale(pderiv(P), F(1, 4))
        topdeg = max(Q)
        assert topdeg == 4 * K, f"K={K}: deg Q = {topdeg} != {4*K}"
        assert Q[4 * K] == F(1), f"K={K}: Q not monic, lead={Q[4*K]}"
        # (c) Unif[0,1] orthogonality of Q_{4K}
        iq = pint01(Q)
        assert iq == 0, f"K={K}: int Q_4K = {iq} != 0"
        # (d) staircase orthogonality with MY OWN C_{2n}, n=0..6
        for n in range(7):
            val = pint01(pmul(P, C[n]))
            assert val == 0, f"K={K} n={n}: <P,C_2n> = {val} != 0"
        report[f"K={K}_p={p}"] = {
            "P(0)=P(1)=0": True,
            "quarter_deriv_monic_deg4K": True,
            "Unif_int_Q4K=0": True,
            "my_staircase_C2n_n0..6_annihilate_P": True,
        }

    report["VERDICT"] = "PHI_ALL_CONFIRMED"
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
