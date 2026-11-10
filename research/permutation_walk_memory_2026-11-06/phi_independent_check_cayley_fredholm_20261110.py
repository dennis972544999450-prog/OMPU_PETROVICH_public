#!/usr/bin/env python3
"""Phi's independent second instrument for Jee A's letter 1794339589_303506_4665dc.

Reimplements the operator T from scratch (NOT reusing her apply_T_poly), in the
standard x-power basis, to recompute H_0^(m), I_0^(m), p_inf and to verify the
mod-4 moment-reduction identities of her Theorem 5 by direct polynomial moments.

(T h)(x) = int_0^{1-x} (1-x-y) h(y) dy.
Write H(t) = int_0^t (t-y) h(y) dy; if h(y)=sum a_k y^k then
H(t) = sum_k a_k t^{k+2} / ((k+1)(k+2)); then substitute t = 1-x and expand.
"""
from fractions import Fraction
from math import comb, factorial


def apply_T(a):
    """a: list of Fraction coeffs in x-power basis. Returns T a in x-power basis.
    Independent route: build H(t) in t-powers, then expand t=(1-x)."""
    # H(t) = sum_k a_k t^{k+2}/((k+1)(k+2))  -> coefficient on t^n
    deg = len(a) - 1
    Ht = [Fraction(0)] * (deg + 3)
    for k, ak in enumerate(a):
        if ak == 0:
            continue
        Ht[k + 2] += ak * Fraction(1, (k + 1) * (k + 2))
    # substitute t = 1 - x : t^n = sum_r C(n,r) (-x)^r
    out = [Fraction(0)] * (len(Ht))
    for n, cn in enumerate(Ht):
        if cn == 0:
            continue
        for r in range(n + 1):
            out[r] += cn * comb(n, r) * ((-1) ** r)
    return out


def at0(a):
    return a[0]  # value at x=0


def integ(a, power=0):
    """int_0^1 x^power * a(x) dx."""
    return sum(c * Fraction(1, k + power + 1) for k, c in enumerate(a))


M = 10
# T^m applied to constant 1
pw = [[Fraction(1)]]
for _ in range(M + 3):
    pw.append(apply_T(pw[-1]))

H0 = [at0(pw[m]) for m in range(M + 3)]          # H_0^(m) = (T^m 1)(0)
I0 = [integ(pw[m], 0) for m in range(M + 3)]      # I_0^(m) = int_0^1 (T^m 1)
p_inf = {m: I0[m + 1] / I0[m] for m in range(1, 9)}

# Headline values she asserted
expect_H0 = {1: "1/2", 2: "1/8", 3: "13/360", 4: "59/5760"}
expect_I0 = {1: "1/6", 2: "1/20", 3: "71/5040"}
expect_p = {1: "3/10", 2: "71/252", 3: "182/639", 4: "45541/160160",
            5: "168388/592033", 6: "120686411/424337760"}

for m, v in expect_H0.items():
    assert str(H0[m]) == v, f"H0[{m}]={H0[m]} != {v}"
for m, v in expect_I0.items():
    assert str(I0[m]) == v, f"I0[{m}]={I0[m]} != {v}"
for m, v in expect_p.items():
    assert str(p_inf[m]) == v, f"p_inf[{m}]={p_inf[m]} != {v}"

# Mod-4 moment reduction identities (Theorem 5) vs direct polynomial moments
for m in range(1, 7):
    i1d = integ(pw[m], 1)
    i2d = integ(pw[m], 2)
    i3d = integ(pw[m], 3)
    i4d = integ(pw[m], 4)
    assert i1d == I0[m] - H0[m + 1]
    assert i2d == I0[m] - 2 * H0[m + 1] + 2 * I0[m + 1]
    assert i3d == I0[m] - 3 * H0[m + 1] + 6 * H0[m + 2]
    assert i4d == I0[m] - 4 * H0[m + 1] + 24 * I0[m + 2]

# Cayley exponential relation via traces Tr(T^m) = (1/4)(T^{m-1} f1)(0), independent build
f1 = [[Fraction(1), Fraction(-1)]]
for _ in range(M + 3):
    f1.append(apply_T(f1[-1]))
traces = [Fraction(1, 4) * at0(f1[m - 1]) for m in range(1, M + 3)]  # Tr(T^m), m>=1
for m in range(1, M + 1):
    rhs = 2 * sum(traces[2 * k] * H0[m - (2 * k + 1)] for k in range((m + 1) // 2))
    assert m * H0[m] == rhs, f"Cayley exp fails at m={m}"

print("PHI_INDEPENDENT_CHECK: all headline H0/I0/p_inf match;")
print("  mod-4 moment identities hold m=1..6; Cayley-exp relation holds m=1..10.")
print("  H0[1..4] =", [str(H0[m]) for m in range(1, 5)])
print("  I0[1..3] =", [str(I0[m]) for m in range(1, 4)])
print("  p_inf[1..6] =", [str(p_inf[m]) for m in range(1, 7)])
print("SECOND_INSTRUMENT_OK")
