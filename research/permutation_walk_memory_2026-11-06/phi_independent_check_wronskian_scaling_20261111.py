#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Φ-Hausmaster independent check (11.11.2026, morning, First OMPU Autumn Subbotnik)
of Jee-A's NEW self-similar Wronskian scaling law (bus 1794389764_684931_0c3cb9,
stereo_v1/a/lab/wronskian_scaling_and_simplex_symmetry_2026_11_11.py):

   MAIN CLAIM:  -w_z(x) = R_z'(x) F_z(x) - R_z(x) F_z'(x) = Delta(z (2x-1)^2) / Delta(z)
                for ALL x in [0, 1],
   where  Delta(z) = det(I - z T) = cosh(sqrt z/2)cos(sqrt z/2) - sinh(sqrt z/2)sin(sqrt z/2),
   T is the kernel operator  (T h)(x) = int_0^{1-x} (1 - x - y) h(y) dy,
   R_z = (I - zT)^{-1} 1,  F_z = (I - zT)^{-1} f_1  with f_1(x) = 1 - x.

INDEPENDENCE. Jee-A proved this by an EXACT power-series-in-z expansion (Fraction
polynomial coefficients W_m(x), order by order). This file takes an ORTHOGONAL
route and does NOT import or reuse her file, Petrovich's verify_all_theorems.py,
nor my own earlier phi_independent_check_wronskian_wick_20261111.py:

  (A) I derive, from the integral equation alone, the exact REFLECTION ODE that T
      forces on any resolvent y = (I - zT)^{-1} g:
          y(x) = g(x) + z (T y)(x)
          y'(x)  = g'(x) - z int_0^{1-x} y(t) dt          (d/dx of the kernel)
          y''(x) = g''(x) + z y(1-x).
      For g = 1 (R_z) and g = 1-x (F_z), g'' = 0, so BOTH obey
          y''(x) = z * y(1-x),   a reflection ODE,
      with data at x=1:  R_z(1)=1, R_z'(1)=0 ;  F_z(1)=0, F_z'(1)=-1.
  (B) The reflection ODE has the closed eigenbasis p''''=z^2 p, i.e.
      {cosh(wx), sinh(wx), cos(wx), sin(wx)}, w = sqrt(z). Imposing y''(x)=z y(1-x)
      forces  b = -tanh(w/2) a  and  d = -cot(w/2) c, giving a 2-parameter family
          y(x) = a*C(x) + c*D(x),
          C(x) = cosh(wx) - tanh(w/2) sinh(wx),
          D(x) = cos(wx)  - cot(w/2)  sin(wx).
      I solve the 2x2 boundary system for (a,c) for R_z and F_z, at dps=50.
  (C) I CLOSE THE LOOP: I verify my ODE-built R_z, F_z actually satisfy the
      ORIGINAL integral equation  y(x) - z (T y)(x) = g(x)  by numerical
      quadrature at sample points -- so the instrument really represents T,
      not merely some ODE.

Then I test the scaling law, its endpoint/midpoint specializations, the integral
identity int_0^1(-w_z)dx = I_z = -4 Delta'(-z)/Delta(z), and the simplex-exchange
antisymmetry  iint_{x+y<=1}(F_z(x)R_z(y)-R_z(x)F_z(y)) = 0.

Run: venv/bin/python3 -I lab/phi_independent_check_wronskian_scaling_20261111.py
"""
import mpmath as mp

mp.mp.dps = 50
TOL = mp.mpf(10) ** (-38)


def Delta(z):
    a = mp.sqrt(z) / 2
    return mp.cosh(a) * mp.cos(a) - mp.sinh(a) * mp.sin(a)


def dDelta(z):
    return mp.diff(Delta, z)


def resolvent_coeffs(z, g_val, gp_val):
    """Solve y = a C + c D with y(1)=g_val, y'(1)=gp_val for the reflection ODE."""
    w = mp.sqrt(z)
    th = mp.tanh(w / 2)
    ct = mp.cos(w / 2) / mp.sin(w / 2)  # cot(w/2)

    def C(x):
        return mp.cosh(w * x) - th * mp.sinh(w * x)

    def Cp(x):
        return w * mp.sinh(w * x) - th * w * mp.cosh(w * x)

    def D(x):
        return mp.cos(w * x) - ct * mp.sin(w * x)

    def Dp(x):
        return -w * mp.sin(w * x) - ct * w * mp.cos(w * x)

    # [[C(1), D(1)], [C'(1), D'(1)]] [a, c]^T = [g_val, gp_val]^T
    M = mp.matrix([[C(1), D(1)], [Cp(1), Dp(1)]])
    rhs = mp.matrix([g_val, gp_val])
    sol = mp.lu_solve(M, rhs)
    a, c = sol[0], sol[1]

    def y(x):
        return a * C(x) + c * D(x)

    def yp(x):
        return a * Cp(x) + c * Dp(x)

    return y, yp


def build_RF(z):
    R, Rp = resolvent_coeffs(z, mp.mpf(1), mp.mpf(0))       # R_z(1)=1, R_z'(1)=0
    F, Fp = resolvent_coeffs(z, mp.mpf(0), mp.mpf(-1))      # F_z(1)=0, F_z'(1)=-1
    return R, Rp, F, Fp


def T_apply(h, x):
    """(T h)(x) = int_0^{1-x} (1-x-y) h(y) dy, numeric."""
    s = 1 - x
    if abs(s) < mp.mpf(10) ** (-40):
        return mp.mpf(0)
    return mp.quad(lambda y: (s - y) * h(y), [0, s])


def report(name, lhs, rhs, acc=TOL):
    err = abs(lhs - rhs)
    ok = err < acc
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: |LHS-RHS| = {mp.nstr(err, 3)}")
    return ok


all_ok = True
xs = [mp.mpf('0'), mp.mpf('0.17'), mp.mpf('0.4'), mp.mpf('0.5'),
      mp.mpf('0.73'), mp.mpf('1')]
zs = [mp.mpf('0.6'), mp.mpf('4.2'), mp.mpf('-3.1'), mp.mpf('9.0'),
      mp.mpc('1.1', '1.7')]

print("Instrument: reflection ODE y''(x)=z y(1-x), closed eigenbasis, dps=50\n")

# ---- (C) close the loop: ODE solution satisfies the ORIGINAL integral eqn ----
print("(C) ODE solutions satisfy the original integral equation y - zTy = g:")
for z in [mp.mpf('0.6'), mp.mpf('4.2'), mp.mpf('-3.1')]:
    R, Rp, F, Fp = build_RF(z)
    for x in [mp.mpf('0.17'), mp.mpf('0.4'), mp.mpf('0.73')]:
        all_ok &= report(f"  R: R(x)-zT R(x)==1    z={mp.nstr(z,4)} x={mp.nstr(x,3)}",
                         R(x) - z * T_apply(R, x), mp.mpf(1))
        all_ok &= report(f"  F: F(x)-zT F(x)==1-x  z={mp.nstr(z,4)} x={mp.nstr(x,3)}",
                         F(x) - z * T_apply(F, x), 1 - x)

# ---- (1) the self-similar scaling law across [0,1] ----
print("\n(1) scaling law  -w_z(x) = Delta(z(2x-1)^2)/Delta(z)  for all x in [0,1]:")
for z in zs:
    R, Rp, F, Fp = build_RF(z)
    dz = Delta(z)
    for x in xs:
        negw = Rp(x) * F(x) - R(x) * Fp(x)
        rhs = Delta(z * (2 * x - 1) ** 2) / dz
        all_ok &= report(f"z={mp.nstr(z,5)} x={mp.nstr(x,3)}", negw, rhs)

# ---- (1') endpoint & midpoint specializations ----
print("\n(1') specializations  -w_z(0)=-w_z(1)=1  and  -w_z(1/2)=1/Delta(z):")
for z in zs:
    R, Rp, F, Fp = build_RF(z)
    negw0 = Rp(0) * F(0) - R(0) * Fp(0)
    negw1 = Rp(1) * F(1) - R(1) * Fp(1)
    negwh = Rp(mp.mpf('0.5')) * F(mp.mpf('0.5')) - R(mp.mpf('0.5')) * Fp(mp.mpf('0.5'))
    all_ok &= report(f"z={mp.nstr(z,5)}  -w(0)==1", negw0, mp.mpf(1))
    all_ok &= report(f"z={mp.nstr(z,5)}  -w(1)==1", negw1, mp.mpf(1))
    all_ok &= report(f"z={mp.nstr(z,5)}  -w(1/2)==1/Delta", negwh, 1 / Delta(z))

# ---- (2) integral identity  int_0^1(-w_z)dx = I_z = -4 Delta'(-z)/Delta(z) ----
print("\n(2) integral  int_0^1(-w_z(x))dx == -4 Delta'(-z)/Delta(z):")
for z in [mp.mpf('0.6'), mp.mpf('4.2'), mp.mpf('-3.1'), mp.mpf('9.0')]:
    R, Rp, F, Fp = build_RF(z)
    integ = mp.quad(lambda x: Rp(x) * F(x) - R(x) * Fp(x), [0, 1])
    # also via the scaling law RHS: int_0^1 Delta(z(2x-1)^2)dx / Delta(z)
    via_scale = mp.quad(lambda x: Delta(z * (2 * x - 1) ** 2), [0, 1]) / Delta(z)
    Iz = -4 * dDelta(-z) / Delta(z)
    all_ok &= report(f"z={mp.nstr(z,5)}  int(-w) == I_z", integ, Iz)
    all_ok &= report(f"z={mp.nstr(z,5)}  int(scaling RHS) == I_z", via_scale, Iz)

# ---- (3) simplex-exchange antisymmetry vanishes ----
print("\n(3) simplex antisymmetry  iint_{x+y<=1}(F(x)R(y)-R(x)F(y))dxdy == 0:")
for z in [mp.mpf('0.6'), mp.mpf('4.2'), mp.mpf('-3.1')]:
    R, Rp, F, Fp = build_RF(z)
    val = mp.quad(lambda x: mp.quad(lambda y: F(x) * R(y) - R(x) * F(y),
                                    [0, 1 - x]), [0, 1])
    all_ok &= report(f"z={mp.nstr(z,5)}  simplex integral == 0", val, mp.mpf(0),
                     acc=mp.mpf(10) ** (-30))

print("\n==== %s ====" % ("ALL_CHECKS_PASSED" if all_ok else "SOME_CHECK_FAILED"))
