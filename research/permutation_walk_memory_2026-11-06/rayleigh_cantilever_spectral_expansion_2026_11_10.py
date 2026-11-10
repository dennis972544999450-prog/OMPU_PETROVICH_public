#!/usr/bin/env python3
"""
Rayleigh-Cantilever Spectral Expansion of Iterated Turn Moments <U, T^k f_1> and <V_1, T^k f_1>,
Universal Mod-4 Germ Series for All Cantilever Modes hat_psi_r (r >= 1), and the Exact
Second-Harmonic Amplitude A_turn in mu_1(T^k f_1) - mu_1(phi_1) ~ A_turn * (-rho_turn)^{-k}.

Author: Jee A (Lane A, OMPU Stereo Pair, ompu-d6a8af238c)
Date: 2026-11-10 10:30 CET (Tuesday Morning Tick, rev 96)
"""

from fractions import Fraction as F
from math import factorial
import math
import numpy as np


def get_cantilever_root(r: int) -> float:
    """Solve cosh(kappa_r) * cos(kappa_r) = -1 in float64 without overflow for large r."""
    k = (r - 0.5) * math.pi
    if r == 1:
        k = 1.875104068711961166445308241078
    elif r == 2:
        k = 4.694091132974174576436391778019
    elif r == 3:
        k = 7.854757438237612564861008582909
    if r >= 12:
        return k
    for _ in range(30):
        f = math.cos(k) + 1.0 / math.cosh(k)
        df = -math.sin(k) - math.sinh(k) / (math.cosh(k) ** 2)
        k -= f / df
    return k


def apply_T_poly(poly: list[F]) -> list[F]:
    """Exact 2nd-order turn operator (T h)(u) = int_0^{1-u} (1 - u - y) h(y) dy on polynomials."""
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


def main() -> None:
    print("=== 1. RAYLEIGH-CANTILEVER PROJECTION IDENTITY <f_1, hat_psi_r> = 2 * lambda_r ===")
    kappas = [get_cantilever_root(r) for r in range(1, 51)]
    sum_inv_k4 = sum(1.0 / (k ** 4) for k in kappas)
    tail_inv_k4 = sum(1.0 / (((r - 0.5) * math.pi) ** 4) for r in range(51, 5000))
    assert abs((sum_inv_k4 + tail_inv_k4) - (1.0 / 12.0)) < 1e-9
    print(f"  Parseval check: sum_{{r>=1}} <f_1, hat_psi_r>^2 = 4 * sum kappa_r^-4 = {4*(sum_inv_k4+tail_inv_k4):.12f} == 1/3 (PASS)")

    print("\n=== 2. UNIVERSAL MOD-4 GERM SERIES FOR CANTILEVER MODES r = 1, 2, 3, 4 ===")
    M = 16
    c_q = [F(24, factorial(2 * k + 4)) for k in range(M + 1)]
    L_even = [F(0)] * (M + 1)
    for j in range(1, M + 1):
        L_even[j] = (j * c_q[j] - sum(i * L_even[i] * c_q[j - i] for i in range(1, j))) / j
    b_even = {2 * j: float(L_even[j] / 2) for j in range(1, M + 1)}

    E = [F(0)] * (M + 1)
    E[0] = F(1)
    for k in range(1, M + 1):
        E[k] = -sum(j * L_even[j] * E[k - j] for j in range(1, k + 1)) / k
    Sigma_odd = {2 * m - 1: float(3 * E[m + 1]) for m in range(1, M)}

    J = 100000
    j_arr = np.arange(1, J + 1)
    sig = np.where(j_arr % 2 == 0, 1.0, -1.0)
    a_arr = (j_arr + 0.5) * np.pi
    w = a_arr + 1j * np.arccosh(a_arr)
    for _ in range(30):
        dw = (np.sin(w) - sig * w) / (np.cos(w) - sig)
        w = w - dw
        if np.max(np.abs(dw)) < 1e-15 * np.max(np.abs(w)):
            break
    s_k = 2j * w
    r_k = 1.0 / (4.0 * (1.0 - sig * np.cos(w)))

    gamma_odd = {1: 0.227350780091995, 3: 0.000991025277641}
    for m in range(2, M + 1):
        n = 2 * m - 1
        coeff = ((-1) ** (m - 1)) / (n * (2 ** (n - 1)))
        gamma_odd[n] = float(coeff * np.sum(np.imag(w ** (-n))))

    Sigma_all = {0: -0.019721794539427, 2: -0.000018652156054}
    for m in range(1, M):
        Sigma_all[2 * m - 1] = Sigma_odd[2 * m - 1]
        if 2 * m >= 4:
            Sigma_all[2 * m] = float(np.sum(2.0 * np.real(r_k / (s_k ** (2 * m + 1)))))

    N_max = 30
    L_full = [0.0] * (N_max + 1)
    for n in range(1, N_max + 1):
        L_full[n] = b_even[n] if n % 2 == 0 else gamma_odd[n]

    p = [0.0] * (N_max + 1)
    p[0] = 1.0
    for n in range(1, N_max + 1):
        p[n] = sum(j_idx * L_full[j_idx] * p[n - j_idx] for j_idx in range(1, n + 1)) / n

    eh = 1.0 / math.sqrt(12.0)
    f_coeff = [7.0 / 20.0] + [((-1) ** m) * Sigma_all[m] for m in range(N_max)]
    c_tw = [sum(p[n - j_idx] * f_coeff[j_idx] for j_idx in range(n + 1)) for n in range(N_max + 1)]
    m_tu = [factorial(n) * eh * p[n] for n in range(N_max + 1)]
    m_tw = [-factorial(n) * eh * c_tw[n] for n in range(N_max + 1)]

    # Evaluate <TU, hat_psi_r>, <TW, hat_psi_r>, <TV_1, hat_psi_r>, and mu_1(phi_r) via the Universal Mod-4 Germ Series:
    # Since hat_psi_r(u) = 2 * sum_{m>=0} [ (kappa_r u)^{4m}/(4m)! - (B_r/A_r)*(kappa_r u)^{4m+1}/(4m+1)! ],
    # pairing with m_n(TU) = n! E[H] p_n and m_n(TW) = -n! E[H] c_n cancels (4m)! and (4m+1)!:
    #   <TU, hat_psi_r> = 2 * E[H] * sum_{m>=0} [ kappa_r^{4m} p_{4m} - (B_r/A_r) kappa_r^{4m+1} p_{4m+1} ],
    #   <TW, hat_psi_r> = -2 * E[H] * sum_{m>=0} [ kappa_r^{4m} c_{4m} - (B_r/A_r) kappa_r^{4m+1} c_{4m+1} ]!
    modes = {}
    for r in (1, 2, 3):
        kr = kappas[r - 1]
        lam_r = ((-1) ** (r - 1)) / (kr * kr)
        # Note B_r / A_r = (cosh kr + cos kr) / (sinh kr + sin kr). For large kr, tanh(kr) -> 1:
        Br_over_Ar = (math.cosh(kr) + math.cos(kr)) / (math.sinh(kr) + math.sin(kr))
        tu_r = 0.0
        tw_r = 0.0
        for m in range(N_max // 4):
            n0 = 4 * m
            n1 = 4 * m + 1
            tu_r += 2.0 * eh * ((kr ** n0) * p[n0] - Br_over_Ar * (kr ** n1) * p[n1])
            tw_r += -2.0 * eh * ((kr ** n0) * c_tw[n0] - Br_over_Ar * (kr ** n1) * c_tw[n1])
        tv1_r = 0.5 * tu_r + tw_r
        mu_r = tv1_r / tu_r
        modes[r] = {
            "kappa": kr,
            "lambda": lam_r,
            "tu": tu_r,
            "tw": tw_r,
            "tv1": tv1_r,
            "mu": mu_r,
        }
        print(
            f"  Mode r={r} (kappa_{r}={kr:.9f}, lam_{r}={lam_r:+.9f}): "
            f"<TU,hat_psi_{r}> = {tu_r:+.12f}, <TV_1,hat_psi_{r}> = {tv1_r:+.12f}, mu_1(phi_{r}) = {mu_r:+.12f}"
        )

    # Check Den B's unnormalized psi_inf = (A_1 / 2) * hat_psi_1 (where Den B printed <TU, psi_inf / 4>):
    A1 = math.sinh(kappas[0]) + math.sin(kappas[0])
    u_phi1_denb = 0.125 * A1 * modes[1]["tu"]
    v1_phi1_denb = 0.125 * A1 * modes[1]["tv1"]
    assert abs(modes[1]["mu"] - 0.113804216148) < 5e-12
    assert abs(modes[2]["mu"] - (-0.330094418380)) < 5e-11

    print("\n=== 3. EXACT SPECTRAL DECOMPOSITION OF <U, T^k f_1>, <V_1, T^k f_1>, AND ASYMPTOTIC AMPLITUDE A_turn ===")
    rho_turn = (kappas[1] / kappas[0]) ** 2
    A_turn = (modes[2]["tu"] / modes[1]["tu"]) * (modes[2]["mu"] - modes[1]["mu"])
    print(f"  Exact second-mode prefactor: mu_1(phi_2) = {modes[2]['mu']:.12f}")
    print(f"  Exact ratio <TU, hat_psi_2> / <TU, hat_psi_1> = {modes[2]['tu'] / modes[1]['tu']:.12f}")
    print(f"  Exact asymptotic amplitude A_turn = {A_turn:+.12f}")
    assert abs(A_turn - (-0.074981508556)) < 5e-11

    h_poly = [F(1), F(-1)]
    for k in range(1, 9):
        u_exact = sum(float(c_val) * m_tu[deg_i] for deg_i, c_val in enumerate(h_poly))
        w_exact = sum(float(c_val) * m_tw[deg_i] for deg_i, c_val in enumerate(h_poly))
        mu_exact = 0.5 + w_exact / u_exact

        # 3-mode spectral approximation (r = 1, 2, 3):
        u_spec3 = sum(2.0 * (modes[r]["lambda"] ** k) * modes[r]["tu"] for r in (1, 2, 3))
        v1_spec3 = sum(2.0 * (modes[r]["lambda"] ** k) * modes[r]["tv1"] for r in (1, 2, 3))
        mu_spec3 = v1_spec3 / u_spec3

        dk = mu_exact - modes[1]["mu"]
        dk_asymp = A_turn * ((-rho_turn) ** (-k))
        print(
            f"  k={k}: mu_exact = {mu_exact:.12f} | 3-mode spec = {mu_spec3:.12f} (|diff|={abs(mu_exact-mu_spec3):.2e}) | "
            f"dk / ((-rho)^-k) = {dk * ((-rho_turn) ** k):+.10f} (-> A_turn = {A_turn:+.10f})"
        )
        if k >= 5:
            assert abs(mu_exact - mu_spec3) < 1e-9
        if k < 8:
            h_poly = apply_T_poly(h_poly)

    print("\nALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
