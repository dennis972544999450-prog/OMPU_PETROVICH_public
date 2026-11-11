#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-Hausmaster independent check (11.11.2026, morning) of Petrovich's three NEW
consequences from his 09:20 digest (bus 1794386687_458195_cfcc29), §1:
  (1) Wick-rotation trace-mass duality:  int_0^1 Delta(z u^2) du = -4 Delta'(-z)
  (2) Centrosymmetric Wronskian conservation law:
          Delta(z)^2 - Delta(-z)^2 = -16 z Delta'(z) Delta'(-z) = -sinh(sqrt z) sin(sqrt z)
  (3) Midpoint Pythagorean identity:  R_z(1/2)^2 + z F_z(1/2)^2 = Delta(z)^-2
      and w_z(1/2) = -Delta(z)^-1

Independence: built ONLY from the Fredholm-determinant closed form in the paper
(line 115) and the midpoint resolvent profiles (line 119). Does NOT import or
reuse Petrovich's verify_all_theorems.py nor Den-b's midpoint_resolvent_*.py.
High-precision mpmath, plus an exact-rational series cross-check of (1) and (2).
Run: venv/bin/python3 -I lab/phi_independent_check_wronskian_wick_20261111.py
"""
import mpmath as mp
from fractions import Fraction as Fr

mp.mp.dps = 60

def Delta(z):
    a = mp.sqrt(z) / 2
    return mp.cosh(a) * mp.cos(a) - mp.sinh(a) * mp.sin(a)

def dDelta(z):
    return mp.diff(Delta, z)

def Rz_half(z):
    return mp.cos(mp.sqrt(z) / 2) / Delta(z)

def Fz_half(z):
    return mp.sin(mp.sqrt(z) / 2) / (mp.sqrt(z) * Delta(z))

def int_Delta_zu2(z):
    # int_0^1 Delta(z u^2) du
    return mp.quad(lambda u: Delta(z * u * u), [0, 1])

def report(name, lhs, rhs):
    err = abs(lhs - rhs)
    ok = err < mp.mpf(10) ** (-45)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: |LHS-RHS| = {mp.nstr(err, 3)}")
    return ok

print("Delta(z) = cosh(sqrt z/2)cos(sqrt z/2) - sinh(sqrt z/2)sin(sqrt z/2)")
print("test points z (real, negative, complex):")
all_ok = True
for z in [mp.mpf('0.7'), mp.mpf('3.5'), mp.mpf('-2.3'), mp.mpf('11.0'),
          mp.mpc('1.3', '2.1'), mp.mpc('-0.9', '4.0')]:
    print(f"\nz = {mp.nstr(z, 8)}")
    sz = mp.sqrt(z)
    # (1)
    all_ok &= report("(1a) int_0^1 Delta(z u^2)du == sinh(sz/2)cos(sz/2)/(sz/2)",
                     int_Delta_zu2(z),
                     mp.sinh(sz/2) * mp.cos(sz/2) / (sz/2))
    all_ok &= report("(1b) int_0^1 Delta(z u^2)du == -4 Delta'(-z)",
                     int_Delta_zu2(z), -4 * dDelta(-z))
    # (2)
    all_ok &= report("(2a) Delta(z)^2-Delta(-z)^2 == -16 z Delta'(z)Delta'(-z)",
                     Delta(z)**2 - Delta(-z)**2,
                     -16 * z * dDelta(z) * dDelta(-z))
    all_ok &= report("(2b) Delta(z)^2-Delta(-z)^2 == -sinh(sz)sin(sz)",
                     Delta(z)**2 - Delta(-z)**2,
                     -mp.sinh(sz) * mp.sin(sz))
    # (3)
    all_ok &= report("(3a) R_z(1/2)^2 + z F_z(1/2)^2 == Delta(z)^-2",
                     Rz_half(z)**2 + z * Fz_half(z)**2, Delta(z)**-2)

# ---- exact-rational series cross-check (my own hand, no float) ----
# Delta(z) = sum_m c_m z^m, c_m = (-1)^floor((m+1)/2) / (2^m (2m)!)
def c(m):
    import math
    sign = (-1) ** ((m + 1) // 2)
    return Fr(sign, (2 ** m) * math.factorial(2 * m))

N = 14
# (1): [z^m] of int_0^1 Delta(z u^2) du = c_m * int_0^1 u^{2m} du = c_m/(2m+1)
# must equal [z^m] of -4 Delta'(-z) = -4 * (m+1) c_{m+1} * (-1)^m
print("\nExact rational series check (up to z^%d):" % N)
ok1 = all(c(m) / (2 * m + 1) == -4 * (m + 1) * c(m + 1) * ((-1) ** m) for m in range(N))
print(f"  [{'PASS' if ok1 else 'FAIL'}] (1) coeff-by-coeff  c_m/(2m+1) == -4(m+1)c_(m+1)(-1)^m")
all_ok &= ok1
# (2): [z^k] of Delta(z)^2 - Delta(-z)^2.  Delta(-z) coeffs = c_m (-1)^m.
# conv of Delta^2: d2[k]=sum c_i c_{k-i}; Delta(-z)^2 coeff = sum c_i c_{k-i}(-1)^k = d2[k](-1)^k
# so LHS[k] = d2[k](1-(-1)^k) -> nonzero only odd k.
# RHS -sinh(sqrt z)sin(sqrt z): sinh(w)sin(w) with w=sqrt z. Use series in z.
def d2(k):
    return sum(c(i) * c(k - i) for i in range(k + 1))
# -sinh(sqrt z) sin(sqrt z) = - sum... ; sinh(w)sin(w)=sum_{n>=1} 2 (-1)^{n-1} w^{4n-2}/(4n-2)! ... compute via series of Im
# easier: sinh(w)sin(w) coefficients in w: product of sum w^{2a+1}/(2a+1)! and sum (-1)^b w^{2b+1}/(2b+1)!
def sinhsin_z_coeff(k):
    # coeff of z^k in sinh(sqrt z) sin(sqrt z); power of z is (a+b+1), need a+b+1=k
    import math
    tot = Fr(0)
    for a in range(0, k):
        b = k - 1 - a
        tot += Fr(((-1) ** b), math.factorial(2 * a + 1) * math.factorial(2 * b + 1))
    return tot
ok2 = all((d2(k) * (1 - (-1) ** k)) == -sinhsin_z_coeff(k) for k in range(1, N))
print(f"  [{'PASS' if ok2 else 'FAIL'}] (2) coeff-by-coeff  Delta^2-Delta(-.)^2 == -sinh(sz)sin(sz)")
all_ok &= ok2

print("\n==== %s ====" % ("ALL_CHECKS_PASSED" if all_ok else "SOME_CHECK_FAILED"))
