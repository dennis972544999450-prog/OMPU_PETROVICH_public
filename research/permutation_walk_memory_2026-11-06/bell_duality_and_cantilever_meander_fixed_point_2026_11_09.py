#!/usr/bin/env python3
"""
Exponential Bell-Polynomial Duality Between Multiplicative (b_{2j}) and Additive
(Sigma_{2m-1}) Wiener-Hopf Constants, Exact Hadamard Root-Sum Identity for Odd
Cumulants gamma_{2m-1}, True Closed Form of mu_1(T^3 f_1), and Three-Way Verification
of the Half-Line Cantilever-Meander Fixed Point mu_1(phi_1) = lim_{k->inf} mu_1(T^k f_1).

Author: Jee A (Lane A, OMPU Stereo Pair, ompu-d6a8af238c)
Date: 2026-11-09 20:30 CET (Monday Evening Tick, rev 95)
"""

from fractions import Fraction as F
from math import factorial
import math
import os
import numpy as np


def verify_bell_polynomial_duality() -> dict:
    """
    1. Exact Fraction proof of the Exponential Bell-Polynomial Duality linking:
       - Even multiplicative Wiener-Hopf cumulants b_{2j} in log(-12 Q(s)/s^2) = 2 sum_{j>=1} b_{2j} s^{2j}
       - Odd additive Wiener-Hopf root sums Sigma_{2m-1} in 1/(2s Q(s)) = -6/s^3 + 1/(5s) - 2 sum_{m>=1} Sigma_{2m-1} s^{2m-1}
       via the generating identity:
           -12 Q(s) / s^2 = exp(2 sum_{j>=1} b_{2j} s^{2j})
       ==> 6 / (-12 Q(s) / s^2) = 6 * exp(-2 sum_{j>=1} b_{2j} s^{2j})
                                = 6 - (1/5)*s^2 + 2 * sum_{m>=1} Sigma_{2m-1} s^{2m+2}.
       Thus Sigma_{2m-1} = 3 * [s^{2m+2}] exp(-2 sum_{j>=1} b_{2j} s^{2j}).
    """
    print("=== 1. EXPONENTIAL BELL-POLYNOMIAL DUALITY: b_{2j} <--> Sigma_{2m-1} (EXACT FRACTION) ===")
    M = 12
    c = [F(24, factorial(2 * k + 4)) for k in range(M + 1)]
    assert c[0] == F(1)

    L = [F(0)] * (M + 1)
    for j in range(1, M + 1):
        s_val = j * c[j] - sum(i * L[i] * c[j - i] for i in range(1, j))
        L[j] = s_val / j
    b_even = {2 * j: L[j] / 2 for j in range(1, M + 1)}

    E = [F(0)] * (M + 1)
    E[0] = F(1)
    for k in range(1, M + 1):
        E[k] = -sum(j * L[j] * E[k - j] for j in range(1, k + 1)) / k

    Sigma_odd = {2 * m - 1: 3 * E[m + 1] for m in range(1, M)}

    b2, b4, b6, b8, b10 = b_even[2], b_even[4], b_even[6], b_even[8], b_even[10]
    assert b2 == F(1, 60)
    assert b4 == F(1, 50400)
    assert b6 == F(-1, 2268000)
    assert b8 == F(73, 27941760000)
    assert b10 == F(1, 168168000000)

    bell_1 = 6 * (b2 ** 2 - b4)
    bell_3 = -6 * (b6 - 2 * b2 * b4 + F(2, 3) * (b2 ** 3))
    bell_5 = -6 * (b8 - 2 * b2 * b6 - (b4 ** 2) + 2 * (b2 ** 2) * b4 - F(1, 3) * (b2 ** 4))

    assert Sigma_odd[1] == bell_1 == F(13, 8400)
    assert Sigma_odd[3] == bell_3 == F(-1, 84000)
    assert Sigma_odd[5] == bell_5 == F(-31, 2328480000)
    assert Sigma_odd[7] == F(1343, 908107200000)
    assert Sigma_odd[9] == F(-6137, 381405024000000)

    for m in range(1, 7):
        j_idx = 2 * m - 1
        print(f"  m={m}: b_{2*m:<2d} = {str(b_even[2*m]):>20s}  <-->  Sigma_{j_idx:<2d} = 3*E_{m+1} = {str(Sigma_odd[j_idx]):>24s}")
    print("  [PASS] Exact Bell-polynomial duality Sigma_{2m-1} = 3*[s^{2m+2}] exp(-2 sum b_{2j} s^{2j}) verified.\n")
    return {"b_even": b_even, "Sigma_odd": Sigma_odd}


def apply_T_poly(poly: list[F]) -> list[F]:
    """
    Apply the exact 2nd-order turn operator (T h)(u) = int_0^{1-u} (1 - u - y) h(y) dy
    to a polynomial h(u) = sum_{j=0}^d poly[j] u^j in exact Fraction arithmetic.
    """
    deg = len(poly) - 1
    out = [F(0)] * (deg + 3)
    for j_idx, c_val in enumerate(poly):
        if c_val == 0:
            continue
        n = j_idx + 2
        coeff_v = c_val * F(1, (j_idx + 1) * (j_idx + 2))
        for r in range(n + 1):
            out[r] += coeff_v * math.comb(n, r) * ((-1) ** r)
    return out


def verify_cantilever_meander_fixed_point(bell_data: dict) -> dict:
    """
    2. Three-way verification of the half-line §6.1 iterated turn sequence mu_1(T^k f_1) (k=1..8)
       and the Euler-Bernoulli Cantilever-Meander fixed point mu_1(phi_1) = lim_{k->inf} mu_1(T^k f_1):
       - Method A: Exact Wiener-Hopf cumulant Taylor-moment series up to N=22 using Hadamard root sums
         gamma_{2m-1} = (-1)^{m-1} / ((2m-1)*2^{2m-2}) * sum_{Q1} Im(w^{-(2m-1)}).
       - Method B: 4-point complex Wiener-Hopf evaluation at s in {+kappa_1, -kappa_1, +i*kappa_1, -i*kappa_1}
         with Sokhotski-Plemelj principal-value subtraction on the imaginary axis.
       - Method C: Half-line grid R_2 Richardson extrapolation from v1_61_mu.py (h = 0.02, 0.01, 0.005, 0.0025).
    """
    print("=== 2. THREE-WAY VERIFICATION OF mu_1(T^k f_1) (k=1..8) & CANTILEVER FIXED POINT mu_1(phi_1) ===")
    b_even = {k: float(v) for k, v in bell_data["b_even"].items()}
    Sigma_odd = {k: float(v) for k, v in bell_data["Sigma_odd"].items()}

    # Verify the exact polynomial (T^2 f_1)(u) = (1-u)^2/6 - (1-u)^3/12 + (1-u)^5/120
    # = 11/120 - u/8 + u^4/24 - u^5/120 (note u^2 and u^3 cancel identically!):
    h0 = [F(1), F(-1)]
    h1 = apply_T_poly(h0)
    h2 = apply_T_poly(h1)
    assert h1 == [F(1, 3), F(-1, 2), F(0), F(1, 6)]
    assert h2 == [F(11, 120), F(-1, 8), F(0), F(0), F(1, 24), F(-1, 120)]
    print("  [PASS] Exact polynomial (T^2 f_1)(u) = 11/120 - u/8 + u^4/24 - u^5/120 (u^2 and u^3 vanish identically!).")

    # Roots w_k of sin(w) = +-w in Q1:
    J = 100000
    j = np.arange(1, J + 1)
    sig = np.where(j % 2 == 0, 1.0, -1.0)
    a = (j + 0.5) * np.pi
    w = a + 1j * np.arccosh(a)
    for _ in range(30):
        dw = (np.sin(w) - sig * w) / (np.cos(w) - sig)
        w = w - dw
        if np.max(np.abs(dw)) < 1e-15 * np.max(np.abs(w)):
            break
    s_k = 2j * w
    r_k = 1.0 / (4.0 * (1.0 - sig * np.cos(w)))

    # Hadamard root-sum identity for odd cumulants gamma_{2m-1} (m >= 2):
    gamma_odd = {1: 0.227350780091995, 3: 0.000991025277641}
    g3_hadamard = float((-1.0 / 12.0) * np.sum(np.imag(w ** (-3))))
    assert abs(g3_hadamard - gamma_odd[3]) < 1e-12
    for m in range(2, 13):
        n = 2 * m - 1
        coeff = ((-1) ** (m - 1)) / (n * (2 ** (n - 1)))
        gamma_odd[n] = float(coeff * np.sum(np.imag(w ** (-n))))

    Sigma_all = {0: -0.019721794539427, 2: -0.000018652156054}
    for m in range(1, 12):
        Sigma_all[2 * m - 1] = Sigma_odd[2 * m - 1]
        if 2 * m >= 4:
            Sigma_all[2 * m] = float(np.sum(2.0 * np.real(r_k / (s_k ** (2 * m + 1)))))

    N_max = 22
    L_full = [0.0] * (N_max + 1)
    for n in range(1, N_max + 1):
        L_full[n] = b_even[n] if n % 2 == 0 else gamma_odd[n]

    p = [0.0] * (N_max + 1)
    p[0] = 1.0
    for n in range(1, N_max + 1):
        p[n] = sum(j_idx * L_full[j_idx] * p[n - j_idx] for j_idx in range(1, n + 1)) / n

    eh = 1.0 / math.sqrt(12.0)
    m_tu = [factorial(n) * eh * p[n] for n in range(N_max + 1)]
    f_coeff = [7.0 / 20.0] + [((-1) ** m) * Sigma_all[m] for m in range(N_max)]
    m_tw = [
        -factorial(n) * eh * sum(p[n - j_idx] * f_coeff[j_idx] for j_idx in range(n + 1))
        for n in range(N_max + 1)
    ]

    # Method C: Half-line grid R_2 extrapolation from v1_61_mu.py for k = 1..8
    wh_dir = "/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/wh_turn_constants_2026-11-08-anthropic-1645"
    cwd_orig = os.getcwd()
    try:
        os.chdir(wh_dir)
        src = open("v1_61_check2.py").read().split("res={h:run")[0]
        ns_grid: dict = {}
        exec(src, ns_grid)
        solve_grid = ns_grid["solve"]
        s3 = math.sqrt(3.0)

        def run_grid_k(h: float, X: float = 12.0, Kmax: int = 8) -> np.ndarray:
            x, V, w_vec = solve_grid(h, X)
            N_g = len(x)
            d0_g = w_vec[len(w_vec) // 2]
            D_mat = np.abs(x[:, None] - x[None, :])
            K_mat = np.clip(1.0 - D_mat, 0.0, None) * h
            Dr_mat = np.abs(x[:, None] - (2.0 * X - x[None, :]))
            K_mat += np.clip(1.0 - Dr_mat, 0.0, None) * h
            P_vec = -2.0 * s3 * (x ** 3) - 6.0 * s3 * d0_g * (x ** 2)
            c3 = -2.0 * s3
            c2 = -6.0 * s3 * d0_g
            A_v = 1.0 - x
            a_v = x - 1.0
            F_fn = lambda y: A_v * (c3 * (y ** 4) / 4.0 + c2 * (y ** 3) / 3.0) + (
                c3 * (y ** 5) / 5.0 + c2 * (y ** 4) / 4.0
            )
            b_vec = np.where(x < 1.0, F_fn(0.0) - F_fn(a_v), 0.0)
            R_vec = np.linalg.solve(np.eye(N_g) - K_mat, s3 * (w_vec - d0_g) - b_vec)
            W0 = P_vec + R_vec
            m_mask = x < 1.0
            xm = x[m_mask]
            U_g = math.sqrt(12.0) * V[m_mask]
            W_g = W0[m_mask]
            c_norm = -0.5 - (W_g @ (1.0 - xm)) * h
            V1_g = 0.5 * U_g + W_g + c_norm * U_g
            Kt = np.clip(1.0 - xm[:, None] - xm[None, :], 0.0, None) * h
            p_vec = 1.0 - xm
            mus = []
            for _ in range(Kmax):
                p_vec = Kt @ p_vec
                mus.append(float((V1_g @ p_vec) / (U_g @ p_vec)))
            return np.array(mus)

        res_g = {h_val: run_grid_k(h_val) for h_val in (0.02, 0.01, 0.005, 0.0025)}
        hs_g = sorted(res_g, reverse=True)
        R1_g = [(4.0 * res_g[hs_g[i + 1]] - res_g[hs_g[i]]) / 3.0 for i in range(3)]
        R2_g = [(16.0 * R1_g[i + 1] - R1_g[i]) / 15.0 for i in range(2)]
        mu_grid_r2 = R2_g[1]
    finally:
        os.chdir(cwd_orig)

    # First two Euler-Bernoulli cantilever roots cosh(kappa)*cos(kappa) = -1:
    kappa_1 = 1.875104068711961166445308241078
    kappa_2 = 4.694091132974174576436391778019
    rho_turn = (kappa_2 / kappa_1) ** 2
    assert abs(rho_turn - 6.266893025771) < 1e-11

    # Method A: 4-point evaluation of mu_1(phi_1) via the entire Laplace power series of (-P(-s)/s) and P(-s)F_{-,W}(s):
    A1 = math.sinh(kappa_1) + math.sin(kappa_1)
    B1 = math.cosh(kappa_1) + math.cos(kappa_1)
    weights_u = [
        (+kappa_1, 0.5 * (A1 - B1)),
        (-kappa_1, 0.5 * (A1 + B1)),
        (+1j * kappa_1, 0.5 * (-A1 + B1 / 1j)),
        (-1j * kappa_1, 0.5 * (-A1 - B1 / 1j)),
    ]

    def eval_tu_lap(s: complex) -> complex:
        return sum((m_tu[n] / factorial(n)) * (s ** n) for n in range(N_max + 1))

    def eval_tw_lap(s: complex) -> complex:
        return sum((m_tw[n] / factorial(n)) * (s ** n) for n in range(N_max + 1))

    tu_phi1 = sum(c_u * np.exp(w_freq) * eval_tu_lap(-w_freq) for w_freq, c_u in weights_u).real
    tw_phi1 = sum(c_u * np.exp(w_freq) * eval_tw_lap(-w_freq) for w_freq, c_u in weights_u).real
    mu_phi1_exact = 0.5 + tw_phi1 / tu_phi1

    # Method B: Direct 4-point complex Wiener-Hopf integral with Sokhotski-Plemelj PV on the imaginary axis:
    with open(os.path.join(wh_dir, "vtv_residue.py")) as f:
        code = f.read().split("# sanity:")[0]
    ns_wh: dict = {}
    exec(code, ns_wh)
    logP_right = ns_wh["logP"]
    g_of = ns_wh["g_of"]
    T_grid = ns_wh["T"]
    W_grid = ns_wh["W"]
    TMAX = ns_wh["TMAX"]

    def eval_P_sokhotski(z: complex) -> complex:
        if abs(z.real) < 1e-10:
            eta = z.imag
            abs_eta = abs(eta)
            sinc = math.sin(abs_eta / 2.0) / (abs_eta / 2.0)
            re_log = 0.5 * math.log(1.0 - sinc * sinc)
            g_eta = float(g_of(np.array([abs_eta]))[0])
            I_pv = float(np.sum((g_of(T_grid) - g_eta) * W_grid / (T_grid ** 2 - abs_eta ** 2))) - 1.0 / (
                6.0 * (TMAX ** 3)
            )
            im_log = math.atan2(eta, 0.0) - math.atan2(eta, 1.0) + (2.0 * eta / math.pi) * I_pv
            return complex(math.exp(re_log) * np.exp(1j * im_log))
        elif z.real > 0:
            return complex(np.exp(logP_right(z)))
        else:
            Qz = 1.0 - 2.0 * (np.cosh(z) - 1.0) / (z * z)
            return complex(Qz / np.exp(logP_right(-z)))

    def eval_Fm(z: complex) -> complex:
        rm_sm = r_k / s_k
        return complex(
            7.0 / (20.0 * z)
            + Sigma_all[0]
            - z * np.sum(rm_sm / (z + s_k) + np.conj(rm_sm) / (z + np.conj(s_k)))
        )

    tu_phi1_pv = sum(c_u * np.exp(w_freq) * (-eval_P_sokhotski(w_freq) / (-w_freq)) for w_freq, c_u in weights_u).real
    tw_phi1_pv = sum(
        c_u * np.exp(w_freq) * (eval_P_sokhotski(w_freq) * eval_Fm(-w_freq)) for w_freq, c_u in weights_u
    ).real
    mu_phi1_pv = 0.5 + tw_phi1_pv / tu_phi1_pv

    # Compare k = 1..8 between exact WH cumulant closed forms and half-line grid R_2:
    h_poly = h0
    mu_wh_list = []
    for k in range(1, 9):
        u_val = sum(float(c_val) * m_tu[deg_i] for deg_i, c_val in enumerate(h_poly))
        w_val = sum(float(c_val) * m_tw[deg_i] for deg_i, c_val in enumerate(h_poly))
        mu_val = 0.5 + w_val / u_val
        mu_wh_list.append(mu_val)
        diff_grid = abs(mu_val - mu_grid_r2[k - 1])
        assert diff_grid < 5e-12, f"Mismatch at k={k}: WH={mu_val}, grid={mu_grid_r2[k-1]}"
        if k < 8:
            h_poly = apply_T_poly(h_poly)

    # Guard key exact numbers with assertions:
    assert abs(mu_wh_list[0] - 0.124475099397) < 5e-12
    assert abs(mu_wh_list[1] - 0.111783887139) < 5e-12
    assert abs(mu_wh_list[2] - 0.114103326553) < 5e-12
    assert abs(mu_phi1_exact - 0.113804216148) < 5e-12
    assert abs(mu_phi1_pv - mu_phi1_exact) < 1e-6

    # Spectral 2-point extrapolation from k=7, 8:
    mu_inf_k78 = (rho_turn * mu_wh_list[7] + mu_wh_list[6]) / (rho_turn + 1.0)
    assert abs(mu_inf_k78 - mu_phi1_exact) < 2e-11

    print(f"  Exact 4-point WH / entire series mu_1(phi_1) = {mu_phi1_exact:.12f}")
    print(f"  Spectral 2-point extrap from k=7,8           = {mu_inf_k78:.12f} (|diff| = {abs(mu_inf_k78 - mu_phi1_exact):.2e})")
    print(f"  Direct Sokhotski-Plemelj PV 4-point WH       = {mu_phi1_pv:.12f}")
    for k in range(1, 9):
        dk = mu_wh_list[k - 1] - mu_phi1_exact
        ratio_str = ""
        if k >= 2:
            dk_prev = mu_wh_list[k - 2] - mu_phi1_exact
            ratio_str = f",  delta_{k-1}/delta_{k} = {dk_prev / dk:+.6f}"
        print(
            f"  k={k}: WH closed form = {mu_wh_list[k-1]:.12f} | grid R_2 = {mu_grid_r2[k-1]:.12f} "
            f"(delta_{k} = {dk:+.10f}{ratio_str})"
        )
    print(f"  Target Euler-Bernoulli alternating ratio -(kappa_2/kappa_1)^2 = {-rho_turn:+.10f}\n")
    return {
        "mu_wh_list": mu_wh_list,
        "mu_grid_r2": mu_grid_r2.tolist(),
        "mu_phi1_exact": mu_phi1_exact,
        "mu_inf_k78": mu_inf_k78,
    }


if __name__ == "__main__":
    bell_data = verify_bell_polynomial_duality()
    verify_cantilever_meander_fixed_point(bell_data)
    print("ALL_CHECKS_PASSED")
