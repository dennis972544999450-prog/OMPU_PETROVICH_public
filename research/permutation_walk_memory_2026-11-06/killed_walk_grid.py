#!/usr/bin/env python3
"""Independent check of the killed triangular random walk on [0, inf):
kernel K(x,y) = (1-|x-y|)_+, x,y >= 0 (killing below 0), sigma^2 = 1/6.
(1) V(0) for the harmonic function V = K V with V(x) ~ x + delta_0  (slope 1).
    Theory: V(0) = E[first descending ladder height] = sigma/sqrt(2) = 1/sqrt(12) (Spitzer).
(2) n^{3/2} * (K^n)(0,0) -> C * V(0)^2 with C = sqrt(2/pi)/sigma^3 (local limit theorem).
    Equivalent: n^{3/2} (K^n)(0,0) -> 1/(sigma*sqrt(2 pi)) = sqrt(3/pi) = 0.97720502...
(3) E[H] by Monte Carlo for triangular steps (sum of two U[-1/2,1/2]).
Grid midpoint rule, reflecting far boundary at X (error exponentially small for n << (X/sigma)^2).
"""
import math, sys
import numpy as np

def build(h, X):
    x = (np.arange(int(round(X/h))) + 0.5) * h          # midpoints
    N = len(x)
    D = np.abs(x[:, None] - x[None, :])
    K = np.clip(1.0 - D, 0.0, None) * h
    # reflecting far boundary: mass that would go beyond X comes back
    Dr = np.abs(x[:, None] - (2*X - x[None, :]))
    K += np.clip(1.0 - Dr, 0.0, None) * h
    return x, K

def harmonic_V0(h, X):
    x, K = build(h, X)
    # V(x) = x + w(x);  w = K w + g,  g(x) = int_{-inf}^0 K(x,y)(-y) dy  (undershoot part), support [0,1)
    # g(x) = int_{x-1}^{0} (1-(x-y))(-y) dy  for 0<=x<1
    g = np.zeros_like(x)
    m = x < 1
    t = x[m]
    # int_{t-1}^{0} (1 - t + y)(-y) dy ; let s=-y from 0 to 1-t: int_0^{1-t} (1-t-s) s ds = (1-t)^3/6
    g[m] = (1 - t)**3 / 6.0
    # tail: beyond X, w ~ const, handled by reflection (w even about X): consistent with Neumann
    w = np.linalg.solve(np.eye(len(x)) - K, g)
    # V(0): extrapolate w to x=0 (w is smooth, use quadratic through first three midpoints)
    c = np.polyfit(x[:3], w[:3], 2)
    V0 = np.polyval(c, 0.0)
    return V0, x, w

def local_limit(h, X, nmax_pow=9):
    x, K = build(h, X)
    P = K.copy()
    out = []
    n = 1
    for k in range(nmax_pow):
        P = P @ P
        n *= 2
        # density of K^n at (0,0): matrix entry / h, extrapolated to the corner from first midpoints
        dens = P[:3, :3] / h
        # bilinear/quadratic extrapolation along the diagonal
        diag = np.array([dens[i, i] for i in range(3)])
        c = np.polyfit(x[:3], diag, 2)
        d00 = np.polyval(c, 0.0)
        out.append((n, d00 * n**1.5))
    return out

def mc_ladder(nwalks=400000, seed=1):
    rng = np.random.default_rng(seed)
    tot = 0.0; cnt = 0
    alive = np.zeros(nwalks); S = np.zeros(nwalks); done = np.zeros(nwalks, bool)
    for step in range(20000):
        idx = ~done
        if not idx.any(): break
        k = idx.sum()
        st = rng.random(k) + rng.random(k) - 1.0
        S[idx] += st
        newly = idx.copy(); newly[idx] = S[idx] < 0
        tot += (-S[newly]).sum(); cnt += newly.sum()
        done |= newly
    return tot / cnt, cnt

if __name__ == '__main__':
    sigma = 1/math.sqrt(6)
    print(f"sigma = {sigma:.12f}, sigma/sqrt2 = {sigma/math.sqrt(2):.12f}, 1/sqrt6 = {sigma:.12f}")
    for h, X in [(0.04, 40.0), (0.02, 60.0), (0.01, 60.0)]:
        V0, x, w = harmonic_V0(h, X)
        print(f"h={h} X={X}: V(0) = {V0:.8f}   (w at X/2 = {w[len(w)//2]:.6f}, w at X = {w[-1]:.6f})")
    print("local limit n^{3/2} K^n(0,0):")
    for n, val in local_limit(0.02, 60.0, 9):
        print(f"  n={n:4d}  {val:.6f}")
    print(f"theory C*V0^2 = sqrt(2/pi)/sigma^3 * sigma^2/2 = {math.sqrt(2/math.pi)/sigma**3 * sigma**2/2:.6f} = sqrt(3/pi) = {math.sqrt(3/math.pi):.6f}")
    print(f"Antigravity A = 6*sqrt(3/pi) = {6*math.sqrt(3/math.pi):.6f};  A*sigma^2 = {6*math.sqrt(3/math.pi)*sigma**2:.6f}")
    print(f"standard C = sqrt(2/pi)/sigma^3 = {math.sqrt(2/math.pi)/sigma**3:.6f}  (= 2A)")
    EH, cnt = mc_ladder()
    print(f"MC E[H] over {cnt} walks = {EH:.5f}  (sigma/sqrt2 = {sigma/math.sqrt(2):.5f}, sigma = {sigma:.5f})")

    # pointwise comparison with the Antigravity V_1 on [0,1] (values printed by theirs/v1_profile.py)
    V0, x, w = harmonic_V0(0.01, 60.0)
    theirs = {0.0: 0.4082482905, 0.25: 0.6953529733, 0.5: 1.0256627227, 0.75: 1.3801851175, 1.0: 1.7369371710}
    print("pointwise: u, V_slope1(u) [grid h=0.01], V_1(u) [Antigravity], ratio")
    for u, v1 in theirs.items():
        if u == 0.0:
            vu = V0
        else:
            # quadratic interpolation of w at u, then V = u + w
            i = int(u / 0.01)
            sel = slice(max(i-1, 0), max(i-1, 0) + 3)
            c = np.polyfit(x[sel], w[sel], 2)
            vu = u + np.polyval(c, u)
        print(f"  u={u:.2f}  V={vu:.6f}  V_1={v1:.6f}  ratio={v1/vu:.5f}   (sqrt2={math.sqrt(2):.5f})")
