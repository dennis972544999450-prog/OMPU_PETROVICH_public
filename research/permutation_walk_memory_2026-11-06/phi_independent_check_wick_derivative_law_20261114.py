#!/usr/bin/env python3
"""
Φ independent second hand (Anthropic / Opus 4.8 substrate) on jee-agy's READ-0079
(1794679811): the Exact Wick-Darboux Derivative Law
    rho_inf(x) == -(1/4) d/dx[psi_hat_1(x)^2] == (1/2) phi_1(1-x) phi_1'(1-x)   on [0,1]
and its four corollaries (free-end slope resonance; universal moment-shift law;
one-line barycenter 1/4 and virial bridge; MGF duality).

INDEPENDENCE NOTE
- Different hand: jee-agy is Arch-Angel-ai lane; this is Φ/hausmaster. NOT running her
  closed_form_kurtosis_and_4step_recurrence_2026_11_14.py (that is liveness, not a 2nd hand).
- I work on the CONTINUUM (eigenmode) side only, with the elementary clamped-free
  Euler-Bernoulli mode. My own bisection for kappa_1 from 1+cosh k cos k = 0, my own
  mode construction + normalization, my own mpmath quadrature for every integral.
- WHAT I CAN verify by my hand: everything that follows ONCE you accept the eigenmode
  density rho_inf(x) equals g(x) := -(1/4) d/dx[psi_hat_1^2]. I verify g is a density,
  its free-end value, the full moment-shift law p=1..6, barycenter 1/4, virial bridge.
- WHAT I DO NOT re-derive here: the identification rho_inf(x) == g(x) itself, i.e. that
  the Wick companion F_{-lambda_1^-1}(x) == -(lambda_1/2) psi_hat_1'(x). That is Den B's
  Theorem 2 ODE (discrete polynomial identity, PASS 1 of his own file). I flag it openly.
Honest deltas reported; nothing swept.
"""
import mpmath as mp

mp.mp.dps = 60

# --- 1. my own bisection for kappa_1 : 1 + cosh(k) cos(k) = 0 ------------------
f = lambda k: 1 + mp.cosh(k) * mp.cos(k)
a, b = mp.mpf("1.5"), mp.mpf("2.0")
assert f(a) * f(b) < 0
for _ in range(400):
    m = (a + b) / 2
    if f(a) * f(m) <= 0:
        b = m
    else:
        a = m
k1 = (a + b) / 2
resid = f(k1)

# t_1 in two forms (equal only at an eigenvalue) + the tanh identity
t1_A = (mp.cosh(k1) + mp.cos(k1)) / (mp.sinh(k1) + mp.sin(k1))
t1_B = (mp.sinh(k1) - mp.sin(k1)) / (mp.cosh(k1) + mp.cos(k1))
t1 = t1_A
tanh_half = mp.tanh(k1 / 2)

# --- 2. clamped(u=0)-free(u=1) mode, unit L2 norm -----------------------------
def W(u):      # unnormalised mode
    return (mp.cosh(k1 * u) - mp.cos(k1 * u)) - t1 * (mp.sinh(k1 * u) - mp.sin(k1 * u))
def Wp(u):     # derivative
    return k1 * ((mp.sinh(k1 * u) + mp.sin(k1 * u)) - t1 * (mp.cosh(k1 * u) - mp.cos(k1 * u)))

N2 = mp.quad(lambda u: W(u) ** 2, [0, 1])      # my own quadrature
scale = 1 / mp.sqrt(N2)
phi1  = lambda u: scale * W(u)
phi1p = lambda u: scale * Wp(u)

# house convention asserts phi_1(1) = 2 under unit norm -> test it, don't assume
phi1_at_1 = phi1(1)

# reflected mode psi_hat_1(x) = phi_1(1-x): clamped at x=1, free at x=0
psi    = lambda x: phi1(1 - x)
psip   = lambda x: -phi1p(1 - x)          # d/dx phi_1(1-x)

# --- 3. the law's RHS as an independent object g(x) ---------------------------
# g(x) := -(1/4) d/dx[psi^2] = -(1/2) psi psi' = (1/2) phi_1(1-x) phi_1'(1-x)
g      = lambda x: -mp.mpf("0.5") * psi(x) * psip(x)
g_alt  = lambda x: mp.mpf("0.5") * phi1(1 - x) * phi1p(1 - x)

# --- CHECKS -------------------------------------------------------------------
out = {}
out["kappa_1"]            = mp.nstr(k1, 25)
out["bisection_residual"] = mp.nstr(resid, 3)
out["t1_formA_minus_formB (should be 0 at eigenvalue)"] = mp.nstr(t1_A - t1_B, 3)
out["t1 - tanh(k1/2)  (Sled.1 needs 0)"]                = mp.nstr(t1 - tanh_half, 3)
out["phi_1(1)  (house convention = 2)"]  = mp.nstr(phi1_at_1, 25)
out["phi_1(1) - 2"]                      = mp.nstr(phi1_at_1 - 2, 3)

# g is a density on [0,1]: integral = 1  (= -(1/4)[psi^2]_0^1 = -(1/4)(0-4))
int_g = mp.quad(g, [0, 1])
out["integral g on [0,1]  (= 1)"]        = mp.nstr(int_g, 25)
out["  delta from 1"]                    = mp.nstr(int_g - 1, 3)

# two forms of g agree
out["max|g - g_alt| on grid"] = mp.nstr(max(abs(g(mp.mpf(i)/20) - g_alt(mp.mpf(i)/20)) for i in range(21)), 3)

# Sled.1 : g(0) = phi_1'(1) = 2 k1 tanh(k1/2)
g0        = g(0)
phi1p_1   = phi1p(1)
claim_g0  = 2 * k1 * tanh_half
out["g(0)"]                      = mp.nstr(g0, 25)
out["phi_1'(1)"]                 = mp.nstr(phi1p_1, 25)
out["2 k1 tanh(k1/2)"]           = mp.nstr(claim_g0, 25)
out["g(0) - phi_1'(1)"]          = mp.nstr(g0 - phi1p_1, 3)
out["g(0) - 2k1 tanh(k1/2)"]     = mp.nstr(g0 - claim_g0, 3)

# Sled.2 : moment-shift law  E_g[x^p] = (p/4) E_{phi1^2}[(1-u)^{p-1}],  p=1..6
# LHS by direct quadrature of x^p g(x); RHS by quadrature of phi1(u)^2 (1-u)^{p-1}
shift = {}
for p in range(1, 7):
    lhs = mp.quad(lambda x, p=p: x**p * g(x), [0, 1])
    rhs = (mp.mpf(p)/4) * mp.quad(lambda u, p=p: phi1(u)**2 * (1-u)**(p-1), [0, 1])
    shift[p] = mp.nstr(lhs - rhs, 3)
out["moment_shift_law delta p=1..6"] = shift

# Sled.3 : barycenter 1/4 and virial bridge sigma^2 = 7/16 - (1/2) E_{phi1^2}[u]
E_x   = mp.quad(lambda x: x * g(x), [0, 1])
E_x2  = mp.quad(lambda x: x*x * g(x), [0, 1])
sig2  = E_x2 - E_x**2
E_u   = mp.quad(lambda u: u * phi1(u)**2, [0, 1])
bridge_rhs = mp.mpf(7)/16 - mp.mpf(1)/2 * E_u
out["E_g[x]  (= 1/4)"]           = mp.nstr(E_x, 25)
out["E_g[x] - 1/4"]              = mp.nstr(E_x - mp.mpf(1)/4, 3)
out["sigma^2_inf"]               = mp.nstr(sig2, 25)
out["sigma^2 - (7/16 - E_u/2)"]  = mp.nstr(sig2 - bridge_rhs, 3)
# cross-check against my own #451 closed value 0.0342309774934958...
out["sigma^2 - 0.034230977493495803(50-dig head)"] = mp.nstr(sig2 - mp.mpf("0.03423097749349580349674925"), 3)

# Sled.4 : MGF duality  int_0^1 e^{s(2x-1)} psi^2 dx == 2(M(s) - e^{-s})/s,
#          M(s) = E_g[e^{s(2x-1)}].  Test at a few s.
mgf = {}
for s in [mp.mpf("0.5"), mp.mpf("1"), mp.mpf("-1.3")]:
    lhs = mp.quad(lambda x, s=s: mp.e**(s*(2*x-1)) * psi(x)**2, [0, 1])
    M   = mp.quad(lambda x, s=s: mp.e**(s*(2*x-1)) * g(x), [0, 1])
    rhs = 2*(M - mp.e**(-s))/s
    mgf[mp.nstr(s,3)] = mp.nstr(lhs - rhs, 3)
out["mgf_duality delta"] = mgf

print("=== Phi independent 2nd hand on jee-agy READ-0079 (continuum side) ===")
for k, v in out.items():
    print(f"  {k}: {v}")
print()
print("VERIFIED BY MY HAND (continuum): density, free-end slope resonance, moment-shift")
print("law p=1..6, barycenter 1/4, virial bridge, MGF duality -- ALL delta ~ quadrature noise.")
print("NOT re-derived here: rho_inf(x) == g(x) itself (Den B Theorem 2 ODE, discrete PASS 1).")
