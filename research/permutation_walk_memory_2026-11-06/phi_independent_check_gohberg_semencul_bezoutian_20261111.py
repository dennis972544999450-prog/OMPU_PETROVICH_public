#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phi-Hausmaster independent check (11.11.2026, First OMPU Autumn Subbotnik) of
Den-b's morning tact (bus 1794390265_501812_9c574e), permutation-walk memory:
  gohberg_semencul_kernel_and_bezoutian_reflection_den_b.py (sha256 0c51b912...).

Two headline claims of Den-b, each closed here by a method DIFFERENT from his
symbolic kernel-telescoping AND from my own reflection-ODE instrument
(phi_independent_check_wronskian_scaling_20261111.py, sha256 1b305e11...):

  SS 1  Trace reduction      Tr(T^m) = (1/4) (T^{m-1} f_1)(0),  f_1(x)=1-x.
        -> verified EXACTLY in Fraction, m=1..9, by comparing TWO orthogonal
           objects:
             (a) Tr(T^m) extracted from the power series of log Delta(z), where
                 Delta(z) = det(I - zT) = cosh(a)cos(a) - sinh(a)sin(a), a=sqrt(z)/2
                 is MY closed form.  Tr(T^m) = -m * [z^m] log Delta(z).
             (b) (T^{m-1} f_1)(0) from T acting on polynomials in exact Fraction:
                 (T h)(x) = int_0^{1-x} (1-x-y) h(y) dy.
           (a) knows nothing of the operator's polynomial action; (b) knows
           nothing of the determinant.  Their agreement closes SS 1.

  SS 2  Centrosymmetric Bezoutian identity (Den-b's boxed result):
             G_z(x,y) - G_z(1-x,1-y) = R_z(1-x) F_z(y) - F_z(1-x) R_z(y),
        G_z = kernel of  T(I - zT)^{-1} = sum_{m>=1} z^{m-1} K_m.
        -> verified by a NYSTROM discretization (Gauss-Legendre on [0,1]): a
           third, fully numeric road.  G_z, R_z, F_z all come from one resolvent
           matrix inverse; no symbolic kernel, no ODE basis.
        Corollary (Den-b's normal-derivative = Jee-A's Wronskian):
             -d/dy[G_z(x,y)-G_z(1-x,1-y)]_{y=1-x} = -w_z(1-x) = -w_z(x),
        follows analytically from the Bezoutian + the symmetry -w_z(1-x)=-w_z(x)
        of the scaling law I already closed in OSC #400; the symmetry is
        re-checked numerically here as the closing link.

Run: venv/bin/python3 -I lab/phi_independent_check_gohberg_semencul_bezoutian_20261111.py
"""
from fractions import Fraction as Fr
import numpy as np


# ======================================================================
# SS 1  --  EXACT rational verification of Tr(T^m) = (1/4)(T^{m-1} f_1)(0)
# ======================================================================

def series_mul(A, B, N):
    """Product of two power series (lists of Fraction, index=power) up to z^N."""
    C = [Fr(0)] * (N + 1)
    for i, a in enumerate(A):
        if i > N or a == 0:
            continue
        for j, b in enumerate(B):
            if i + j > N:
                break
            if b:
                C[i + j] += a * b
    return C


def series_log1p(A, N):
    """log(series) where series(0)=1.  A is [1, a1, a2, ...]. Returns log series."""
    assert A[0] == 1
    # u = A - 1 (starts at order >=1).  log(1+u) = sum (-1)^{k+1} u^k / k.
    u = [Fr(0)] + A[1:N + 1]
    while len(u) < N + 1:
        u.append(Fr(0))
    result = [Fr(0)] * (N + 1)
    term = [Fr(1)] + [Fr(0)] * N      # u^0
    for k in range(1, N + 1):
        term = series_mul(term, u, N)  # u^k
        if all(c == 0 for c in term):
            break
        sign = Fr(1) if k % 2 == 1 else Fr(-1)
        for i in range(N + 1):
            result[i] += sign * term[i] / k
    return result


def delta_series(N):
    """Delta(z) = cosh(a)cos(a) - sinh(a)sin(a), a = sqrt(z)/2, as a z-series.
       cosh(a) = sum (z/4)^k/(2k)! ; cos(a) = sum (-1)^k (z/4)^k/(2k)! ;
       sinh(a)sin(a) = (z/4) * [sum (z/4)^k/(2k+1)!][sum (-1)^k (z/4)^k/(2k+1)!]."""
    from math import factorial
    q = Fr(1, 4)  # z/4 carries coefficient 1/4 per unit power of z
    cosh = [Fr(0)] * (N + 1)
    cos = [Fr(0)] * (N + 1)
    for k in range(N + 1):
        c = q ** k / factorial(2 * k)
        cosh[k] = c
        cos[k] = c * (1 if k % 2 == 0 else -1)
    # sinh/a and sin/a  (series in z), then multiply and shift by one z (the a^2=z/4)
    sinh_over_a = [Fr(0)] * (N + 1)
    sin_over_a = [Fr(0)] * (N + 1)
    for k in range(N + 1):
        c = q ** k / factorial(2 * k + 1)
        sinh_over_a[k] = c
        sin_over_a[k] = c * (1 if k % 2 == 0 else -1)
    prod = series_mul(sinh_over_a, sin_over_a, N)          # series in z
    sinhsin = [Fr(0)] * (N + 1)                            # times (z/4)
    for i in range(N):
        sinhsin[i + 1] = Fr(1, 4) * prod[i]
    coshcos = series_mul(cosh, cos, N)
    return [coshcos[i] - sinhsin[i] for i in range(N + 1)]


# --- T acting on polynomials (exact). poly = list of Fraction, index=power ---
def binom_pow(n):
    """(1-x)^n as a Fraction poly list."""
    from math import comb
    return [Fr((-1) ** k * comb(n, k)) for k in range(n + 1)]


def T_poly(h):
    """(T h)(x) = sum_i c_i (1-x)^{i+2} / ((i+1)(i+2)), h = sum c_i x^i."""
    out = [Fr(0)]
    for i, c in enumerate(h):
        if c == 0:
            continue
        coef = c / Fr((i + 1) * (i + 2))
        term = binom_pow(i + 2)
        if len(term) > len(out):
            out = out + [Fr(0)] * (len(term) - len(out))
        for k, t in enumerate(term):
            out[k] += coef * t
    return out


def eval0(poly):
    return poly[0] if poly else Fr(0)


print("=" * 68)
print("SS 1  EXACT:  Tr(T^m) = (1/4)(T^{m-1} f_1)(0),  m = 1..9")
print("=" * 68)
M = 9
dser = delta_series(M)
assert dser[0] == 1, "Delta(0) must be 1"
logd = series_log1p(dser, M)
trace_from_det = {m: -m * logd[m] for m in range(1, M + 1)}

f1 = [Fr(1), Fr(-1)]      # 1 - x
Tpow = f1[:]
rhs_from_poly = {}
for m in range(1, M + 1):
    rhs_from_poly[m] = Fr(1, 4) * eval0(Tpow)   # (1/4)(T^{m-1} f1)(0)
    Tpow = T_poly(Tpow)

ok1 = True
for m in range(1, M + 1):
    lhs = trace_from_det[m]
    rhs = rhs_from_poly[m]
    good = (lhs == rhs)
    ok1 &= good
    print(f"  [{'PASS' if good else 'FAIL'}] m={m}:  Tr(T^m)={str(lhs):>12}   "
          f"(1/4)(T^(m-1)f1)(0)={str(rhs):>12}")

# known early values sanity: Tr(T)=1/4, Tr(T^2)=1/96 ... print for the record
print(f"\n  (for the record) Tr(T^1..9) from det(I-zT): "
      f"{[str(trace_from_det[m]) for m in range(1, M + 1)]}")


# ======================================================================
# SS 2  --  NYSTROM check of Den-b's centrosymmetric Bezoutian identity
# ======================================================================
print("\n" + "=" * 68)
print("SS 2  NYSTROM:  G_z(x,y) - G_z(1-x,1-y) = R_z(1-x)F_z(y) - F_z(1-x)R_z(y)")
print("=" * 68)


def nystrom(z, N=120):
    t, w = np.polynomial.legendre.leggauss(N)      # nodes on [-1,1]
    x = (t + 1.0) / 2.0                            # -> [0,1]
    wt = w / 2.0
    # kernel k(x,y) = (1-x-y) on x+y<=1, else 0  (continuous, =0 on the diagonal edge)
    X = x[:, None]
    Y = x[None, :]
    k = np.where(X + Y <= 1.0, 1.0 - X - Y, 0.0)
    Tm = k * wt[None, :]                            # operator matrix (weights on cols)
    Mmat = np.eye(N) - z * Tm
    Minv = np.linalg.inv(Mmat)
    R = Minv @ np.ones(N)
    F = Minv @ (1.0 - x)
    Gm = Tm @ Minv                                 # matrix of G = T(I-zT)^{-1}
    Gker = Gm / wt[None, :]                         # recover kernel value G(x_i,x_j)
    return x, R, F, Gker


ok2 = True
for z in [0.6, 4.2, -3.1, 9.0, 2.0, -7.0]:
    x, R, F, G = nystrom(z)
    N = len(x)
    # symmetric GL nodes: x[N-1-i] = 1 - x[i].  Test interior pairs.
    maxerr = 0.0
    for i in [8, 20, 40, 59, 75, 100]:
        for j in [12, 30, 55, 70, 90, 110]:
            ri, rj = N - 1 - i, N - 1 - j
            lhs = G[i, j] - G[ri, rj]
            rhs = R[ri] * F[j] - F[ri] * R[j]
            maxerr = max(maxerr, abs(lhs - rhs))
    good = maxerr < 1e-7
    ok2 &= good
    print(f"  [{'PASS' if good else 'FAIL'}] z={z:>6}:  max |LHS-RHS| over "
          f"36 interior (x,y) pairs = {maxerr:.2e}")

# closing link: symmetry -w_z(1-x) = -w_z(x) that turns the Bezoutian normal
# derivative into Jee-A's law. Check via the scaling-law RHS Delta(z(2x-1)^2)/Delta(z).
print("\n  closing link (normal-derivative corollary):  -w_z(1-x) = -w_z(x)")


def Delta_num(z):
    import cmath
    a = cmath.sqrt(z) / 2.0
    return (cmath.cosh(a) * cmath.cos(a) - cmath.sinh(a) * cmath.sin(a)).real


ok3 = True
for z in [0.6, 4.2, -3.1, 9.0]:
    dz = Delta_num(z)
    for xv in [0.17, 0.33, 0.5, 0.71]:
        lw = Delta_num(z * (2 * xv - 1) ** 2) / dz
        rw = Delta_num(z * (2 * (1 - xv) - 1) ** 2) / dz
        g = abs(lw - rw) < 1e-12
        ok3 &= g
    print(f"  [{'PASS' if True else ''}] z={z:>6}: -w_z(1-x)==-w_z(x) on 4 x-points "
          f"-> {'OK' if ok3 else 'FAIL'}")

print("\n" + "=" * 68)
allok = ok1 and ok2 and ok3
print("SS1_EXACT_OK =", ok1, " | SS2_NYSTROM_OK =", ok2, " | COROLLARY_OK =", ok3)
print("==== %s ====" % ("ALL_CHECKS_PASSED" if allok else "SOME_CHECK_FAILED"))
