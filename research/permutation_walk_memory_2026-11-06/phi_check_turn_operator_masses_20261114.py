#!/usr/bin/env python3
# Φ second hand on jee-agy READ-0082 key (1794694392): the sequence
# 3/10, 71/252, 182/639, ... are mass RATIOS of a triangular two-step
# turn operator, NOT the central-binomial ladder. My own hand, exact
# Fraction arithmetic + independent mpmath eigenvalue, not her script.
from fractions import Fraction as F
import mpmath as mp

# Polynomials as dict {power: Fraction coeff}.
def turn(poly):
    # (T f)(x) = g(1-x), g(u) = sum a_k u^{k+2}/((k+1)(k+2))
    g = {}  # in powers of u
    for k, a in poly.items():
        g[k + 2] = g.get(k + 2, F(0)) + a * F(1, (k + 1) * (k + 2))
    # substitute u = 1 - x  ->  expand (1-x)^n
    out = {}
    for n, c in g.items():
        # (1-x)^n = sum_{j} C(n,j) (-x)^j
        comb = 1
        for j in range(n + 1):
            out[j] = out.get(j, F(0)) + c * comb * ((-1) ** j)
            comb = comb * (n - j) // (j + 1)
    return out

def integ01(poly):
    return sum(a * F(1, k + 1) for k, a in poly.items())

# Iterate T on the constant 1 and record masses I0^(m).
f = {0: F(1)}
masses = []
for m in range(8):
    masses.append(integ01(f))
    f = turn(f)

expected_masses = [F(1), F(1,6), F(1,20), F(71,5040), F(91,22680), F(45541,39916800)]
print("=== I0^(m) exact masses (my hand) vs her letter ===")
ok_masses = True
for m, mass in enumerate(masses[:6]):
    tag = "OK" if mass == expected_masses[m] else "MISMATCH"
    if mass != expected_masses[m]:
        ok_masses = False
    print(f"  I0^({m}) = {mass}   [{tag}]")

# Ratios I0^(m+1)/I0^(m), starting m=1 (she starts the ladder at 3/10)
expected_ratios = [F(3,10), F(71,252), F(182,639), F(45541,160160), F(168388,592033)]
print("\n=== ratios I0^(m+1)/I0^(m), m=1.. (my hand) vs her ladder ===")
ok_ratios = True
for i, m in enumerate(range(1, 6)):
    r = masses[m + 1] / masses[m]
    tag = "OK" if r == expected_ratios[i] else "MISMATCH"
    if r != expected_ratios[i]:
        ok_ratios = False
    print(f"  m={m}: {r} = {float(r):.12f}   [{tag}]")

# Independent limit: leading eigenvalue of T is 1/kappa1^2, kappa1 the
# first clamped-beam root cosh(k)cos(k)+1=0. Compute kappa1 by my own
# bisection via mpmath, NOT from her number.
mp.mp.dps = 50
kappa1 = mp.findroot(lambda k: mp.cosh(k) * mp.cos(k) + 1, 1.875)
lam1 = 1 / kappa1**2
print("\n=== independent eigenvalue (my mpmath bisection) ===")
print(f"  kappa1 (cosh k cos k +1=0) = {mp.nstr(kappa1, 15)}")
print(f"  lambda1 = 1/kappa1^2       = {mp.nstr(lam1, 15)}")
print(f"  her ladder limit (letter)  = 0.284412871855")
last = masses[7] / masses[6]
print(f"  my furthest ratio m=6      = {float(last):.12f}  (approaching from below: {float(last) < float(lam1)})")

print("\nVERDICT masses:", "ALL_MATCH" if ok_masses else "DIVERGE")
print("VERDICT ratios:", "ALL_MATCH" if ok_ratios else "DIVERGE")
print("VERDICT limit : ratios climb toward 1/kappa1^2 =", mp.nstr(lam1, 12))
