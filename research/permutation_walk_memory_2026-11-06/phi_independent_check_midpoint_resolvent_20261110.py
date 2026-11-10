#!/usr/bin/env python3
"""
Phi (Opus) independent second instrument for Den-b's evening tick 10.11.2026:
  midpoint_resolvent_unification_and_edgeworth3_den_b.py

Deliberately NOT 同源 with his code:
  - He verifies in exact `Fraction` via apply_T_poly recursion + Delta-series division.
  - I verify by high-precision mpmath Taylor/derivative numerics of the CLOSED-FORM
    analytic objects themselves, plus a from-scratch operator path using the
    (1-x)^{k+2}/((k+1)(k+2)) integration (a different implementation than apply_T_poly).

Checks:
  A. Delta(z) closed form's Taylor coeffs == (-1)^floor((m+1)/2)/(2^m (2m)!)      [his delta_coeff]
  B. R_z(0) = Delta(-z)/Delta(z) Taylor -> A_m = (2m)! H_0^(m) == stated integers [Andre-Cayley EGF]
  C. His closed-form profiles R_z(x), F_z(x) actually SOLVE the reflected BVPs
     R''(x)=z R(1-x), R(1)=1, R'(1)=0 ;  F''(x)=z F(1-x), F(1)=0, F'(1)=-1   [Theorem 1 core]
  D. F_z(0) = -4 Delta'(z)/Delta(z)  and  -F_z'(0) = R_z(0) = Delta(-z)/Delta(z)
  E. Midpoint numerators: R_z(1/2)*Delta = cos(w/2), F_z(1/2)*Delta = sin(w/2)/w
  F. Independent operator path -> A_m, reflected-moment identity J_r^(m)=I_{r-2}^(m+1)/(r-2)!
"""
from fractions import Fraction
import math
import mpmath as mp

mp.mp.dps = 60
OK = True

def rep(name, cond):
    global OK
    OK = OK and bool(cond)
    print(f"  [{'OK' if cond else 'FAIL'}] {name}")

w  = lambda z: mp.sqrt(z)
Delta = lambda z: mp.cosh(w(z)/2)*mp.cos(w(z)/2) - mp.sinh(w(z)/2)*mp.sin(w(z)/2)
# His closed-form profiles (y = x - 1/2):
def R(z, x):
    y = x - mp.mpf(1)/2; ww = w(z)
    return (mp.cos(ww/2)*mp.cosh(ww*y) - mp.sinh(ww/2)*mp.sin(ww*y)) / Delta(z)
def F(z, x):
    y = x - mp.mpf(1)/2; ww = w(z)
    return (mp.sin(ww/2)*mp.cosh(ww*y) - mp.cosh(ww/2)*mp.sin(ww*y)) / (ww*Delta(z))

print("=== A. Delta(z) Taylor coeffs vs (-1)^floor((m+1)/2)/(2^m (2m)!) ===")
tay = mp.taylor(Delta, 0, 12)                      # numeric series of the closed form
delta_coeff = lambda m: Fraction((-1)**((m+1)//2), (2**m)*math.factorial(2*m))
rep("delta_coeff m=0..12", all(abs(tay[m]-float(delta_coeff(m))) < 1e-18 for m in range(13)))

print("=== B. A_m = (2m)! H_0^(m) from Delta(-z)/Delta(z) (Andre-Cayley EGF) ===")
R0 = lambda z: Delta(-z)/Delta(z)
h0 = mp.taylor(R0, 0, 11)                          # H_0^(m) = coeff of z^m
A_claim = [1,1,3,26,413,10576,397023,20551376,1402815833,122087570176,13194844482843]
A_mp = [h0[m]*mp.factorial(2*m) for m in range(11)]
rep("A_m integers match letter", all(abs(A_mp[m]-A_claim[m]) < 1e-3*max(1,A_claim[m]) for m in range(11)))
print("      A_m =", [int(mp.nint(a)) for a in A_mp])

print("=== C. Closed-form profiles solve the reflected BVPs (Theorem 1 core) ===")
bad = mp.mpf(0)
for z in [mp.mpf('0.7'), mp.mpf('2.3'), -mp.mpf('1.1'), mp.mpf('5.0')]:
    for x in [mp.mpf('0.17'), mp.mpf('0.42'), mp.mpf('0.83')]:
        bad = max(bad, abs(mp.diff(lambda t: R(z,t), x, 2) - z*R(z, 1-x)))
        bad = max(bad, abs(mp.diff(lambda t: F(z,t), x, 2) - z*F(z, 1-x)))
    bad = max(bad, abs(R(z,1)-1), abs(mp.diff(lambda t: R(z,t),1,1)))
    bad = max(bad, abs(F(z,1)),   abs(mp.diff(lambda t: F(z,t),1,1)+1))
rep(f"R''=zR(1-x), F''=zF(1-x) + 4 boundary conds (max resid {mp.nstr(bad,3)})", bad < mp.mpf('1e-40'))

print("=== D. F_z(0) = -4 Delta'/Delta  and  -F_z'(0) = R_z(0) = Delta(-z)/Delta(z) ===")
dmax = mp.mpf(0)
for z in [mp.mpf('0.7'), mp.mpf('2.3'), mp.mpf('5.0')]:
    dmax = max(dmax, abs(F(z,0) - (-4*mp.diff(Delta, z)/Delta(z))))
    dmax = max(dmax, abs(-mp.diff(lambda t: F(z,t), 0, 1) - R(z,0)))
    dmax = max(dmax, abs(R(z,0) - Delta(-z)/Delta(z)))
rep(f"trace/slope unification (max resid {mp.nstr(dmax,3)})", dmax < mp.mpf('1e-40'))

print("=== E. Midpoint numerators cos(w/2), sin(w/2)/w ===")
emax = mp.mpf(0)
for z in [mp.mpf('0.7'), mp.mpf('2.3'), mp.mpf('5.0')]:
    emax = max(emax, abs(R(z, mp.mpf(1)/2)*Delta(z) - mp.cos(w(z)/2)))
    emax = max(emax, abs(F(z, mp.mpf(1)/2)*Delta(z) - mp.sin(w(z)/2)/w(z)))
rep(f"R(1/2)Delta=cos(w/2), F(1/2)Delta=sin(w/2)/w (max resid {mp.nstr(emax,3)})", emax < mp.mpf('1e-40'))

print("=== F. Independent operator path: (Th)(x)=int_0^{1-x}(1-x-y)h(y)dy ===")
# (T h)(x) = sum_k c_k (1-x)^{k+2}/((k+1)(k+2));  expand (1-x)^{k+2} independently.
def Tpoly(poly):
    out = [Fraction(0)]*(len(poly)+2)
    for k, c in enumerate(poly):
        if c == 0: continue
        n, cv = k+2, c*Fraction(1,(k+1)*(k+2))
        for r in range(n+1):
            out[r] += cv*math.comb(n, r)*((-1)**r)
    return out
def mom(poly, p=0):  # int_0^1 x^p poly dx
    return sum(c/Fraction(k+p+1) for k, c in enumerate(poly))
def refl_mom(poly, r):  # int_0^1 (1-x)^r/r! poly dx
    return sum(c*Fraction(math.factorial(k), math.factorial(r+k+1)) for k, c in enumerate(poly) if c)
t1 = [[Fraction(1)]]
for _ in range(9): t1.append(Tpoly(t1[-1]))
A_op = [ (sum(c*Fraction(0)**k if k else c for k,c in enumerate(t1[m])))  # (T^m 1)(0) = constant term
         for m in range(9)]
A_op = [t1[m][0]*math.factorial(2*m) for m in range(9)]   # H_0^(m)=const term; A_m=(2m)!*it
rep("independent-operator A_m == letter", all(A_op[m]==A_claim[m] for m in range(9)))
# Reflected-moment identity J_r^(m) = I_{r-2}^(m+1)/(r-2)!  (r>=2), J_1=H_0^(m+1), J_0=I_0^(m)
jm_ok = True
for m in range(7):
    for r in range(2, 9):
        if refl_mom(t1[m], r) != mom(t1[m+1], r-2)/Fraction(math.factorial(r-2)):
            jm_ok = False
    # J_1^(m) = H_0^(m+1) = (T^{m+1}1)(0) = constant term; J_0^(m) = I_0^(m) = integral
    jm_ok = jm_ok and refl_mom(t1[m],1)==t1[m+1][0] and refl_mom(t1[m],0)==mom(t1[m],0)
rep("reflected-moment identity J_r^(m)=I_{r-2}^(m+1)/(r-2)!", jm_ok)

print("\nSECOND_INSTRUMENT_OK" if OK else "\nSECOND_INSTRUMENT_FAIL")
