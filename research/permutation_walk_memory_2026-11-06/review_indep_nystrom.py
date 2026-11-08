# Independent check: product-trapezoid (hat-function) Nystrom, nodes at x_i = i h (V(0) read at a node, no corner extrapolation),
# constant continuation beyond X instead of reflection.
import math, numpy as np, sys
def W_matrix(h, X):
    N = int(round(X/h)); x = np.arange(N+1)*h
    k = np.clip(1.0 - np.abs(x[:,None]-x[None,:]), 0, None)       # k(x_i, y_j)
    W = np.zeros_like(k)
    W += 4*k
    W[:,1:] += k[:,:-1]; W[:,:-1] += k[:,1:]
    W *= h/6.0
    # ends: node 0 has only a right interval, node N only a left one -> Simpson pieces (h/6)[k_j + 2 kmid_j] etc.
    W[:,0] = (h/6.0)*(k[:,0] + 2*0.5*(k[:,0]+k[:,1]))
    W[:,N] = (h/6.0)*(k[:,N] + 2*0.5*(k[:,N]+k[:,N-1]))
    # constant continuation beyond X: int_X^{x_i+1} (1-(y-x_i)) dy = (1-X+x_i)^2/2 for x_i > X-1
    tail = np.clip(1.0 - X + x, 0, None)**2/2
    W[:,N] += tail
    return x, W
def run(h, X, nmax=4096):
    x, W = W_matrix(h, X)
    g = np.where(x < 1, (1-x)**3/6, 0.0)
    w = np.linalg.solve(np.eye(len(x)) - W, g)
    V = x + w
    out = {"V0": V[0], "winf": w[-1]}
    for u in [0.25,0.5,0.75,1.0]:
        out[f"V{u}"] = V[int(round(u/h))]
    m = x <= 1.0 + 1e-12
    out["normV2_01"] = np.trapezoid(V[m]**2, x[m])
    # K^n(0,0) by repeated application to k_1(.,0) = (1-z)_+
    kn = np.clip(1-x, 0, None); n = 1; res = {}
    while n < nmax:
        kn = W @ kn; n += 1
        if n in (64,128,256,512,1024,2048,4096): res[n] = kn[0]*n**1.5
    out["Kn00"] = res
    return out
if __name__ == "__main__":
    s = 1/math.sqrt(6)
    theirs = {0.0: 0.4082482905, 0.25: 0.6953529733, 0.5: 1.0256627227, 0.75: 1.3801851175, 1.0: 1.7369371710}
    hs = [0.04, 0.02, 0.01]; results = {}
    for h in hs:
        X = 60.0 if h <= 0.02 else 40.0
        r = run(h, X); results[h] = r
        print(f"h={h} X={X}: V(0)={r['V0']:.9f}  w(inf)={r['winf']:.6f}  ||V||^2_[0,1]={r['normV2_01']:.7f}")
        print("   V(u):", {u: round(r[f'V{u}'],7) for u in [0.25,0.5,0.75,1.0]})
        print("   n^{3/2}K^n(0,0):", {n: round(v,6) for n,v in r['Kn00'].items()})
    # Richardson h^2 on V(0) and on K^n
    a,b,c = [results[h]['V0'] for h in hs]
    print(f"V(0) diffs {a-b:.3e} {b-c:.3e} ratio {(a-b)/(b-c):.3f}; Richardson(h^2) V(0) = {c-(b-c)/3:.9f}; exact sigma/sqrt2 = {s/math.sqrt(2):.9f}")
    for u in [0.0,0.25,0.5,0.75,1.0]:
        key = 'V0' if u==0 else f'V{u}'
        vb, vc = results[0.02][key], results[0.01][key]
        vr = vc - (vb-vc)/3
        print(f"  u={u}: V_h0.01={vc:.7f} Richardson={vr:.7f}  ratio V_1/V: raw {theirs[u]/vc:.6f}  Rich {theirs[u]/vr:.7f}  (sqrt2={math.sqrt(2):.7f})")
    for n in (512,1024,2048,4096):
        vb, vc = results[0.02]['Kn00'][n], results[0.01]['Kn00'][n]
        print(f"  n={n}: K h=0.02 {vb:.6f} h=0.01 {vc:.6f} Richardson(h^2) {vc-(vb-vc)/3:.6f}   target sqrt(3/pi)={math.sqrt(3/math.pi):.6f}")
