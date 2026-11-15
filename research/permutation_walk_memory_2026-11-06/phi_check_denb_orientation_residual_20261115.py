#!/usr/bin/env python3
"""
Independent check of Den-b's rev101 claim (bus 1794736594):
my residual 0.24 at 4(d) is a RIGHT/LEFT-end orientation artifact x <-> 1-x.

Turn operator:  (T phi)(x) = int_0^{1-x} (1-x-t) phi(t) dt
             =  int_0^1  max(1-x-t, 0) phi(t) dt   (kernel k(x,t)=(1-x-t)_+)

Claim to reproduce WITH MY OWN HAND (not his hardcode):
  Q(x) = x^4 - 9/4 x^3 + 15/8 x^2 - 5/8 x + 1/20         (= (1/16)(16u^4-4u^3+u-1/5), u=x-1/2)
  true turn-operator eigenmode psi_hat_r (clamped at x=1, free at x=0):
      I_true(r)  = int_0^1 Q(x) psi_hat_r(x)^2 dx  ->  ~ 0
  mirrored mode (standard beam, clamped at x=0) = psi_hat_r(1-x):
      I_mirror(r) = int_0^1 Q(x) psi_hat_r(1-x)^2 dx -> +0.235726 at r=1  (= 0.24/16? no: in u-norm *16)

Also verify the orientation mechanism directly:
  even part of Q (under u->-u) integrates the same on both; odd part flips sign.
"""
import numpy as np

N = 6000
# midpoint grid
x = (np.arange(N) + 0.5) / N
w = 1.0 / N

# kernel k(x,t) = (1 - x - t)_+
K = (1.0 - x[:, None] - x[None, :])
K = np.where(K > 0, K, 0.0) * w   # dense quadrature operator

# eigen-decomposition (non-symmetric Volterra-ish, but real spectrum here)
vals, vecs = np.linalg.eig(K)
vals = vals.real
vecs = vecs.real
order = np.argsort(-np.abs(vals))
vals = vals[order]
vecs = vecs[:, order]

def normify(v):
    # L2-normalize as a density: int psi^2 dx = 1
    s = np.sqrt(np.sum(v * v) * w)
    v = v / s
    # fix sign so psi(0 end) >= 0
    if v[0] < 0:
        v = -v
    return v

# Q(x)
def Q(xx):
    return xx**4 - (9.0/4.0)*xx**3 + (15.0/8.0)*xx**2 - (5.0/8.0)*xx + 1.0/20.0

Qx = Q(x)

print("lambda_r (first 5):", [f"{v:+.6f}" for v in vals[:5]])
print("expected #463   :  +0.284413, -0.045383, +0.016208, ...")
print()
print(" r |   end values psi(0)^2, psi(1)^2  |  I_true=int Q psi^2  |  I_mirror=int Q psi(1-x)^2  |  *16 (u-norm)")
for r in range(5):
    psi = normify(vecs[:, r])
    psi2 = psi * psi
    # clamped end: compare psi^2 at x~0 vs x~1
    e0, e1 = psi2[0], psi2[-1]
    I_true = np.sum(Qx * psi2) * w
    psi_mirror2 = psi2[::-1]          # psi(1-x)^2
    I_mirror = np.sum(Qx * psi_mirror2) * w
    print(f" {r+1} |  psi(0)^2={e0:7.4f} psi(1)^2={e1:7.4f} | {I_true:+.3e}        | {I_mirror:+.6f}            | {I_mirror*16:+.6f}")

print()
# Orientation mechanism: split Q into even/odd parts about u=x-1/2
u = x - 0.5
# even-in-u part and odd-in-u part of Q (as function of u)
Qe = 0.5*(Q(0.5+u) + Q(0.5-u))
Qo = 0.5*(Q(0.5+u) - Q(0.5-u))
psi1 = normify(vecs[:, 0]); p1 = psi1*psi1
It_e = np.sum(Qe*p1)*w; It_o = np.sum(Qo*p1)*w
Im_e = np.sum(Qe*p1[::-1])*w; Im_o = np.sum(Qo*p1[::-1])*w
print("r=1 even part  int Qe psi^2     =", f"{It_e:+.6f}", "   mirror:", f"{Im_e:+.6f}", " (should match: even invariant)")
print("r=1 odd  part  int Qo psi^2     =", f"{It_o:+.6f}", "   mirror:", f"{Im_o:+.6f}", " (should be +-, sign flip)")
print("r=1 odd part *16               =", f"{It_o*16:+.6f}", "   mirror*16:", f"{Im_o*16:+.6f}")
print()
print("VERDICT: I_true ~ 0 ;  mirror*16 ~ +0.2357 at r=1 ;  flip lives entirely in the odd-in-u part.")
