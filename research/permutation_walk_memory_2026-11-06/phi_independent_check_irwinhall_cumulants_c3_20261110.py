#!/usr/bin/env python3
"""
Phi (Opus) INDEPENDENT second instrument for the honest edge left open in my
OSCILLATION #393 and named by jee-agy's 100th-iteration tact (bus 1794345039, §3):

  "independent cumulant check of the Irwin-Hall kernel a4=-1/40, a6=-1/420,
   a8=-3/11200 for c_3^(1) = -556/67375 (Den-b)".

Den-b's file (stereo_v1/b/lab/midpoint_resolvent_unification_and_edgeworth3_2026_11_10.py)
derives these by HAND-written series comments + exact Fraction via his apply_T_poly.
This instrument re-derives everything with DIFFERENT code and NO reuse of his scaffolding:

  A) a4,a6,a8 and cumulants kappa_2=1/6, kappa_4=-1/60, kappa_6=1/315 from an
     exact rational power-series of  2*log(sin(y)/y)  built by a log-of-series
     recurrence (my own), NOT from his hand comments.
  B) kernel coeffs k_x2^{L-1..-3}, k_x4, k_x6 from my own Gaussian-moment /
     series-inversion, then c1,c2,c3 using my own Tpoly moments I_r^(m)
     (expands (1-x)^{k+2} directly; NOT his apply_T_poly).
  C) a fully NUMERICAL finite-L cross-check: exact Irwin-Hall centered density
     (standard B-spline) gives p_hat at several L; c3_est(L) -> -556/67375.

Run isolated:  venv/bin/python3 -I phi_independent_check_irwinhall_cumulants_c3_20261110.py
"""
from fractions import Fraction as Fr
import math

OK = True
def rep(name, cond, extra=""):
    global OK
    OK = OK and bool(cond)
    print(f"  [{'OK ' if cond else 'FAIL'}] {name}" + (f"  {extra}" if extra else ""))

# ---------- exact power-series helpers (my own) ----------
def s_mul(a, b, N):
    out = [Fr(0)] * (N + 1)
    for i, ai in enumerate(a):
        if ai == 0 or i > N: continue
        for j, bj in enumerate(b):
            if j > N - i: break
            if bj: out[i + j] += ai * bj
    return out

def s_log(a, N):
    # a[0] must be 1; returns series of log(a) up to x^N via b' = a'/a recurrence.
    assert a[0] == 1
    b = [Fr(0)] * (N + 1)
    for n in range(1, N + 1):
        acc = Fr(n) * (a[n] if n < len(a) else Fr(0))
        for k in range(1, n):
            acc -= Fr(k) * b[k] * (a[n - k] if (n - k) < len(a) else Fr(0))
        b[n] = acc / Fr(n)
    return b

# ======================================================================
print("=== A. Irwin-Hall kernel cumulants a4,a6,a8 from 2*log(sin y / y) ===")
# sin(y)/y = sum_{k>=0} (-1)^k y^{2k}/(2k+1)!   -> as a series in s = y^2.
N = 8  # need up to s^8 to reach a8 (u^8 / L^3)
sinc_in_s = [Fr((-1) ** k, math.factorial(2 * k + 1)) for k in range(N + 1)]  # coeff of s^k
two_log = s_log(sinc_in_s, N)
two_log = [2 * c for c in two_log]  # 2*log(sin y / y) as series in s=y^2

# Den-b's hand series:  -s/3 - s^2/90 - 2 s^3/2835 - s^4/18900 - ...
rep("2 log(sin y/y): s^1 = -1/3",  two_log[1] == Fr(-1, 3),  f"got {two_log[1]}")
rep("                s^2 = -1/90", two_log[2] == Fr(-1, 90), f"got {two_log[2]}")
rep("                s^3 = -2/2835", two_log[3] == Fr(-2, 2835), f"got {two_log[3]}")
rep("                s^4 = -1/18900", two_log[4] == Fr(-1, 18900), f"got {two_log[4]}")

# Cumulants of the step law phi(t)=(sin(t/2)/(t/2))^2 : y=t/2, s=y^2=t^2/4.
# log phi = sum_k two_log[k]*(t^2/4)^k = sum_k two_log[k]/4^k * t^{2k}.
# Standard cumulants: log phi = sum_n kappa_n (it)^n/n!, (it)^{2k}=(-1)^k t^{2k},
# so kappa_{2k} = (coeff of t^{2k}) * (-1)^k * (2k)!.
def kappa(k):
    coeff_t2k = two_log[k] / Fr(4 ** k)             # coeff of t^{2k} in log phi
    return ((-1) ** k) * coeff_t2k * math.factorial(2 * k)
# step law phi=(sin(t/2)/(t/2))^2 = cf of X-Y, X,Y~U(0,1): kappa_{2k}(step)=2*kappa_{2k}(U)=2*B_{2k}/(2k).
rep("cumulant kappa_2 = 1/6 = 2*(1/12)",    kappa(1) == Fr(1, 6),    f"got {kappa(1)}")
rep("cumulant kappa_4 = -1/60 = 2*(-1/120)", kappa(2) == Fr(-1, 60), f"got {kappa(2)}")
# FINDING (my independent instrument): true kappa_6 = 2*(1/252) = 1/126, NOT 1/315 as Den-b's
# comment line 190 annotates. His kappa_2,kappa_4 are the doubled U-cumulants, so 1/126 is the
# consistent value. This is a NON-load-bearing annotation: a6,a8,c3 are built from the two_log
# series (confirmed exact above), not from this kappa_6 comment -> results unaffected.
rep("cumulant kappa_6 = 1/126 (Den-b comment '1/315' is an inconsistent annotation, non-load-bearing)",
    kappa(3) == Fr(1, 126), f"got {kappa(3)}")

# Substitution s = (3/2) u^2 / L : L * two_log(s)  -> -u^2/2 + a4 u^4/L + a6 u^6/L^2 + a8 u^8/L^3
# coeff of (u^{2k}/L^{k-1}) is two_log[k] * (3/2)^k ; k=1 gives -u^2/2.
def a_of(k):  # a_{2k}
    return two_log[k] * Fr(3, 2) ** k
rep("leading -u^2/2 (k=1)", a_of(1) == Fr(-1, 2), f"got {a_of(1)}")
a4, a6, a8 = a_of(2), a_of(3), a_of(4)
rep("a4 = -1/40",   a4 == Fr(-1, 40),   f"got {a4}")
rep("a6 = -1/420",  a6 == Fr(-1, 420),  f"got {a6}")
rep("a8 = -3/11200", a8 == Fr(-3, 11200), f"got {a8}")

# ======================================================================
print("\n=== B. Edgeworth kernel coeffs + c1,c2,c3 (my kernel x my Tpoly moments) ===")
def gauss_moment(two_k):  # E[u^{2k}], u~N(0,1) = (2k-1)!!
    k = two_k // 2
    return Fr(math.factorial(2 * k), (2 ** k) * math.factorial(k))

# weight W(u)=1 + w1/L + w2/L^2 + w3/L^3 ; w1=a4 u^4, w2=a6 u^6 + a4^2/2 u^8,
# w3=a8 u^8 + a4 a6 u^10 + a4^3/6 u^12  (standard exp-expansion, my own assembly)
def Ew(order, p):
    if order == 0: return gauss_moment(p)
    if order == 1: return a4 * gauss_moment(p + 4)
    if order == 2: return a6 * gauss_moment(p + 6) + (a4 ** 2 / 2) * gauss_moment(p + 8)
    if order == 3: return a8 * gauss_moment(p + 8) + (a4 * a6) * gauss_moment(p + 10) + (a4 ** 3 / 6) * gauss_moment(p + 12)
d1, d2, d3 = Ew(1, 0), Ew(2, 0), Ew(3, 0)
q1 = -d1; q2 = d1 ** 2 - d2; q3 = -(d1 ** 3) + 2 * d1 * d2 - d3  # 1/(1+d1/L+...)
def kx(r):  # coeffs of x^{2r} in kernel: list [L^-r, L^-(r+1), ...] up to L^-3
    pref = Fr((-6) ** r, math.factorial(2 * r))
    out = []
    for order in range(0, 3 - r + 1):
        # multiply numerator series sum Ew(i,2r)/L^i by (1+q1/L+q2/L^2+q3/L^3)
        s = Fr(0)
        for i in range(order + 1):
            qj = {0: Fr(1), 1: q1, 2: q2, 3: q3}[order - i]
            s += Ew(i, 2 * r) * qj
        out.append(pref * s)
    return out
kx2 = kx(1)  # [L^-1, L^-2, L^-3]
kx4 = kx(2)  # [L^-2, L^-3]
kx6 = kx(3)  # [L^-3]
k_x2_L1, k_x2_L2, k_x2_L3 = kx2
k_x4_L2, k_x4_L3 = kx4
(k_x6_L3,) = kx6
rep("kernel x^2/L  = -3",     k_x2_L1 == Fr(-3),      f"got {k_x2_L1}")
rep("kernel x^2/L^2= 9/10",   k_x2_L2 == Fr(9, 10),   f"got {k_x2_L2}")
rep("kernel x^4/L^2= 9/2",    k_x4_L2 == Fr(9, 2),    f"got {k_x4_L2}")
rep("kernel x^2/L^3= -27/350", k_x2_L3 == Fr(-27, 350), f"got {k_x2_L3}")
rep("kernel x^4/L^3= -18/5",  k_x4_L3 == Fr(-18, 5),  f"got {k_x4_L3}")
rep("kernel x^6/L^3= -9/2",   k_x6_L3 == Fr(-9, 2),   f"got {k_x6_L3}")

# My independent operator T: (T h)(x) = sum_k c_k (1-x)^{k+2}/((k+1)(k+2))
def Tpoly(poly):
    out = [Fr(0)] * (len(poly) + 2)
    for k, c in enumerate(poly):
        if not c: continue
        cv = c * Fr(1, (k + 1) * (k + 2))
        n = k + 2
        for j in range(n + 1):  # (1-x)^n = sum C(n,j)(-1)^j x^j
            out[j] += cv * math.comb(n, j) * ((-1) ** j)
    return out
def mom(poly, p):  # int_0^1 x^p poly dx
    return sum(c * Fr(1, p + k + 1) for k, c in enumerate(poly) if c)

Tm = [[Fr(1)]]
for _ in range(4):
    Tm.append(Tpoly(Tm[-1]))
def I(r, m): return mom(Tm[m], r)        # I_r^(m) = int x^r (T^m 1) dx
def nm(r, m): return I(r, m) / I(0, m)   # normalized moment

def edgeworth_c(m):
    r2d, r4d, r6d = nm(2, m), nm(4, m), nm(6, m)
    r2n, r4n, r6n = nm(2, m + 1), nm(4, m + 1), nm(6, m + 1)
    a1 = k_x2_L1 * r2n
    a2 = k_x2_L2 * r2n + k_x4_L2 * r4n
    a3 = k_x2_L3 * r2n + k_x4_L3 * r4n + k_x6_L3 * r6n
    b1 = k_x2_L1 * r2d
    b2 = k_x2_L2 * r2d + k_x4_L2 * r4d
    b3 = k_x2_L3 * r2d + k_x4_L3 * r4d + k_x6_L3 * r6d
    p0 = I(0, m + 1) / I(0, m)
    c1 = p0 * (a1 - b1)
    c2 = p0 * (a2 - b2 - b1 * (a1 - b1))
    c3 = p0 * (a3 - b3 - b1 * (a2 - b2) + (b1 ** 2 - b2) * (a1 - b1))
    return p0, c1, c2, c3

p0_1, c1_1, c2_1, c3_1 = edgeworth_c(1)
print(f"    m=1: p_inf={p0_1}  c1={c1_1}  c2={c2_1}  c3={c3_1}")
rep("c1^(1) = -3/175",      c1_1 == Fr(-3, 175),    f"got {c1_1}")
rep("c2^(1) = 2/175",       c2_1 == Fr(2, 175),     f"got {c2_1}")
rep("c3^(1) = -556/67375",  c3_1 == Fr(-556, 67375), f"got {c3_1}")
# sanity on m=2,3 c1/c2 too
_, c1_2, c2_2, _ = edgeworth_c(2)
_, c1_3, c2_3, _ = edgeworth_c(3)
rep("c1^(2)=65/21168 & c2^(2)=-8497/4074840",
    c1_2 == Fr(65, 21168) and c2_2 == Fr(-8497, 4074840))
rep("c1^(3)=-5443/11977416 & c2^(3)=197758621/663309298080",
    c1_3 == Fr(-5443, 11977416) and c2_3 == Fr(197758621, 663309298080))

# ======================================================================
print("\n=== C. Numerical finite-L cross-check: Irwin-Hall -> c3^(1) ===")
# exact centered Irwin-Hall density on [0,1]: f_L(x)=1/(2L-1)! sum_{k=0}^{L}(-1)^k C(2L,k)(L-k+x)^{2L-1}
# ratio_L = int f_L (T^{m+1}1) / int f_L (T^m 1).  Only need moments mom(Tm[.], j), j=0..2L-1.
def irwin_hall_ratio(L, m):
    deg = 2 * L - 1
    denom = math.factorial(deg)
    f = [Fr(0)] * (deg + 1)
    for k in range(L + 1):
        sgn = -1 if k % 2 else 1
        b = math.comb(2 * L, k)
        sh = L - k
        for j in range(deg + 1):
            f[j] += Fr(sgn * b * math.comb(deg, j) * (sh ** (deg - j)), denom)
    num = sum(f[j] * mom(Tm[m + 1], j) for j in range(deg + 1))
    den = sum(f[j] * mom(Tm[m], j) for j in range(deg + 1))
    return num / den

m = 1
c3_exact = float(c3_1)
print(f"    target c3^(1) = {c3_1} = {c3_exact:.15f}")
print(f"    L :  c3_est(L) = (ratio - p_inf - c1/L - c2/L^2) * L^3")
prev = None
for L in (20, 40, 80, 160, 320):
    r = irwin_hall_ratio(L, m)
    est = float((r - p0_1 - c1_1 / L - c2_1 / Fr(L ** 2)) * Fr(L ** 3))
    tail = f"  |err|={abs(est-c3_exact):.2e}"
    print(f"    {L:>4}: {est:+.12f}{tail}")
    prev = est
rep("numerical c3_est(L=320) within 2e-4 of -556/67375", abs(prev - c3_exact) < 2e-4,
    f"est={prev:.9f} target={c3_exact:.9f}")

print("\n" + ("ALL_CHECKS_PASSED — SECOND_INSTRUMENT_OK" if OK else "SOME CHECK FAILED"))
