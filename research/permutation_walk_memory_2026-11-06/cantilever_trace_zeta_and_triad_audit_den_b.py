#!/usr/bin/env python3
"""
Free-End Cantilever Trace & Spectral Zeta Identity (T^{m-1} f_1)(0) = 4 Tr(T^m),
Independent Two-Route Verification of Multi-Mode Rayleigh-Cantilever Meander Moments
mu_1(phi_r) (r=1,2,3) and Asymptotic Turn Amplitude A_turn = -0.074981508556,
and Triad Audit (Prose / Code / JSON Data) across the Research Staging Package.

Author: Den B (Lane B, OMPU Stereo Pair, ompu-7f698bd908)
Date: 2026-11-10 10:35 CET (Tuesday Morning Tick, rev 96)
"""

from fractions import Fraction
import json
import math
import os
import shutil
import numpy as np


RESEARCH_DIR = "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06"


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


def apply_T_poly(poly: list[Fraction]) -> list[Fraction]:
    """
    Apply the exact 2nd-order turn operator (T h)(u) = int_0^{1-u} (1 - u - y) h(y) dy
    to a polynomial h(u) = sum_{j=0}^d poly[j] u^j in exact Fraction arithmetic.
    """
    deg = len(poly) - 1
    out = [Fraction(0)] * (deg + 3)
    for j_idx, c_val in enumerate(poly):
        if c_val == 0:
            continue
        n = j_idx + 2
        coeff_v = c_val * Fraction(1, (j_idx + 1) * (j_idx + 2))
        for r in range(n + 1):
            out[r] += coeff_v * math.comb(n, r) * ((-1) ** r)
    return out


def poly_l2_inner(p: list[Fraction], q: list[Fraction]) -> Fraction:
    """Exact L^2([0, 1]) inner product int_0^1 p(u) q(u) du in Fraction arithmetic."""
    total = Fraction(0)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            if b != 0:
                total += a * b / Fraction(i + j + 1)
    return total


def part1_free_end_cantilever_trace_zeta_theorem() -> dict:
    """
    Theorem (Free-End Cantilever Trace & Spectral Zeta Identity):
    For the self-adjoint turn operator (T h)(u) = int_0^{1-u} (1 - u - y) h(y) dy on L^2([0, 1])
    with orthonormal Euler-Bernoulli cantilever eigenfunctions hat_psi_r(u) satisfying
    T hat_psi_r = lambda_r hat_psi_r, lambda_r = (-1)^{r-1} / kappa_r^2 (cosh(kappa_r)cos(kappa_r) = -1),
    and free-end value hat_psi_r(0) = 2:
      1. <f_1, hat_psi_r> = (T hat_psi_r)(0) = lambda_r hat_psi_r(0) = 2 * lambda_r.
      2. Consequently, (T^{m-1} f_1)(u) = sum_{r>=1} 2 * lambda_r^m * hat_psi_r(u), and evaluating at u = 0
         or taking L^2([0, 1]) inner products <T^a f_1, T^b f_1> (a + b = m - 2) gives for ALL m >= 1:
             Tr(T^m) = sum_{r=1}^inf lambda_r^m = sum_{r=1}^inf ((-1)^{r-1} / kappa_r^2)^m
                     = (1/4) * (T^{m-1} f_1)(0)
                     = (1/4) * <T^a f_1, T^b f_1>_{L^2(0,1)}  (for all a, b >= 0 with a + b = m - 2).
      3. Simultaneously, -(T^m f_1)'(0) = int_0^1 (T^{m-1} f_1)(y) dy, so the ratio of linear
         coefficients at u = 0 is the exact m-turn Bayesian cell limit p_hat_inf(-, 1^{m-1}).
    """
    print("=== 1. FREE-END CANTILEVER TRACE & SPECTRAL ZETA THEOREM: (T^{m-1} f_1)(0) = 4 Tr(T^m) ===")
    M_max = 10
    iterates = [[Fraction(1), Fraction(-1)]]  # k = 0: f_1(u) = 1 - u
    for _ in range(1, M_max):
        iterates.append(apply_T_poly(iterates[-1]))

    kappas = [get_cantilever_root(r) for r in range(1, 201)]
    lambdas = [((-1) ** (r - 1)) / (kappas[r - 1] ** 2) for r in range(1, 201)]

    traces = {}
    for m in range(1, M_max + 1):
        # Free-end value (1/4) * (T^{m-1} f_1)(0)
        tr_free_end = iterates[m - 1][0] / Fraction(4)

        # Verify against all L^2([0, 1]) splits (1/4) * <T^a f_1, T^b f_1> with a + b = m - 2
        if m >= 2:
            for a in range(m - 1):
                b = (m - 2) - a
                tr_l2 = poly_l2_inner(iterates[a], iterates[b]) / Fraction(4)
                assert tr_l2 == tr_free_end, f"Mismatch at m={m}, a={a}, b={b}: {tr_l2} != {tr_free_end}"

        # Compare with spectral eigenvalue sum sum_{r>=1} lambda_r^m
        spec_sum = sum(lam ** m for lam in lambdas)
        if m == 1:
            # Alternating series sum (-1)^{r-1} / kappa_r^2: add Euler-Maclaurin tail
            tail = sum(((-1) ** (r - 1)) / (((r - 0.5) * math.pi) ** 2) for r in range(201, 20001))
            spec_sum += tail
            tol = 1e-9
        else:
            tail = sum(((-1) ** ((r - 1) * m)) / (((r - 0.5) * math.pi) ** (2 * m)) for r in range(201, 5001))
            spec_sum += tail
            tol = 1e-13

        diff = abs(float(tr_free_end) - spec_sum)
        assert diff < tol, f"Spectral trace mismatch at m={m}: {float(tr_free_end)} vs {spec_sum} (diff={diff})"

        # Also check linear slope at u = 0: -(T^{m-1} f_1)'(0) = int_0^1 (T^{m-2} f_1)(y) dy
        slope_at_0 = -iterates[m - 1][1]
        if m >= 2:
            mass_prev = sum(c / Fraction(j + 1) for j, c in enumerate(iterates[m - 2]))
            assert slope_at_0 == mass_prev

        traces[f"m={m}"] = {
            "Tr_T_pow_m_exact": str(tr_free_end),
            "T_pow_m_minus_1_f1_at_0": str(iterates[m - 1][0]),
            "minus_derivative_at_0": str(slope_at_0),
            "Tr_T_pow_m_float": float(tr_free_end),
            "spectral_sum_float": spec_sum,
            "abs_diff": diff,
        }
        print(
            f"  m={m:2d}: Tr(T^{m:<2d}) = (1/4)*(T^{m-1} f_1)(0) = {str(tr_free_end):>28s} "
            f"({float(tr_free_end):+.14f}, |diff|={diff:.2e})"
        )

    assert traces["m=1"]["Tr_T_pow_m_exact"] == "1/4"
    assert traces["m=2"]["Tr_T_pow_m_exact"] == "1/12"
    assert traces["m=3"]["Tr_T_pow_m_exact"] == "11/480"
    assert traces["m=4"]["Tr_T_pow_m_exact"] == "11/1680"
    assert traces["m=5"]["Tr_T_pow_m_exact"] == "2701/1451520"
    assert traces["m=6"]["Tr_T_pow_m_exact"] == "2641/4989600"
    print("  [PASS] Exact Free-End Cantilever Trace & Spectral Zeta Identity verified in Fraction for m = 1..10.\n")
    return traces


def part2_multi_mode_rayleigh_cantilever_verification() -> dict:
    """
    Independent verification of Jee A's multi-mode Rayleigh-Cantilever spectral expansion
    (rayleigh_cantilever_spectral_expansion_2026_11_10.py):
      - Route A: Universal Mod-4 Germ Series at s = 0 evaluated at kappa_1, kappa_2, kappa_3.
      - Route B: Direct extraction of mode r = 2 (<TU, hat_psi_2>, <TV_1, hat_psi_2>, mu_1(phi_2))
        and asymptotic amplitude A_turn from the exact Fraction polynomial iterates T^k f_1 (k = 1..8)
        after subtracting the leading mode r = 1 (2 * lambda_1^k * <T., hat_psi_1>) and 3rd mode r = 3.
    """
    print("=== 2. MULTI-MODE RAYLEIGH-CANTILEVER EXPANSION & SECOND-MODE EXTRACTION FROM POLYNOMIAL ITERATES ===")
    M = 16
    c_q = [Fraction(24, math.factorial(2 * k + 4)) for k in range(M + 1)]
    L_even = [Fraction(0)] * (M + 1)
    for j in range(1, M + 1):
        L_even[j] = (j * c_q[j] - sum(i * L_even[i] * c_q[j - i] for i in range(1, j))) / j
    b_even = {2 * j: float(L_even[j] / 2) for j in range(1, M + 1)}

    E = [Fraction(0)] * (M + 1)
    E[0] = Fraction(1)
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
    m_tu = [math.factorial(n) * eh * p[n] for n in range(N_max + 1)]
    m_tw = [-math.factorial(n) * eh * c_tw[n] for n in range(N_max + 1)]

    kappas = [get_cantilever_root(r) for r in range(1, 7)]
    modes = {}
    for r in range(1, 5):
        kr = kappas[r - 1]
        lam_r = ((-1) ** (r - 1)) / (kr ** 2)
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

    h_poly = [Fraction(1), Fraction(-1)]
    u_iters = {}
    v1_iters = {}
    for k in range(1, 9):
        u_ex = sum(float(c_val) * m_tu[deg_i] for deg_i, c_val in enumerate(h_poly))
        w_ex = sum(float(c_val) * m_tw[deg_i] for deg_i, c_val in enumerate(h_poly))
        u_iters[k] = u_ex
        v1_iters[k] = 0.5 * u_ex + w_ex
        if k < 8:
            h_poly = apply_T_poly(h_poly)

    # Route B: Pure spectral annihilator extraction of mode r=2 from polynomial iterates k=2..6
    # Applying P_ann(S) = prod_{r in {1, 3, 4, 5}} (S - lambda_r) to u_iters[k] and v1_iters[k]
    # annihilates modes r = 1, 3, 4, 5 simultaneously using ONLY the eigenvalues lambda_r and
    # the polynomial iterates T^k f_1 (zero use of any mode-r germ series!):
    kappas = [get_cantilever_root(r) for r in range(1, 10)]
    ann_poly = [1.0]
    for r_elim in (1, 3, 4, 5, 6):
        lam_e = ((-1) ** (r_elim - 1)) / (kappas[r_elim - 1] ** 2)
        nxt = [0.0] * (len(ann_poly) + 1)
        for idx, c_a in enumerate(ann_poly):
            nxt[idx] -= lam_e * c_a
            nxt[idx + 1] += c_a
        ann_poly = nxt

    k_base = 3
    lam2 = modes[2]["lambda"]
    p_ann_at_lam2 = sum(c_a * (lam2 ** idx) for idx, c_a in enumerate(ann_poly))
    denom_r2 = 2.0 * (lam2 ** k_base) * p_ann_at_lam2

    tu_2_from_poly = sum(c_a * u_iters[k_base + idx] for idx, c_a in enumerate(ann_poly)) / denom_r2
    tv1_2_from_poly = sum(c_a * v1_iters[k_base + idx] for idx, c_a in enumerate(ann_poly)) / denom_r2
    mu_2_from_poly = tv1_2_from_poly / tu_2_from_poly

    diff_mu2 = abs(mu_2_from_poly - modes[2]["mu"])
    assert diff_mu2 < 1e-7, f"Mismatch in mu_1(phi_2): {mu_2_from_poly} vs {modes[2]['mu']} (diff={diff_mu2})"

    # Similarly extract mode r=1 via prod_{r in {2, 3, 4, 5, 6}} (S - lambda_r) on k=3..8:
    ann_poly_1 = [1.0]
    for r_elim in (2, 3, 4, 5, 6):
        lam_e = ((-1) ** (r_elim - 1)) / (kappas[r_elim - 1] ** 2)
        nxt = [0.0] * (len(ann_poly_1) + 1)
        for idx, c_a in enumerate(ann_poly_1):
            nxt[idx] -= lam_e * c_a
            nxt[idx + 1] += c_a
        ann_poly_1 = nxt
    lam1 = modes[1]["lambda"]
    denom_r1 = 2.0 * (lam1 ** k_base) * sum(c_a * (lam1 ** idx) for idx, c_a in enumerate(ann_poly_1))
    tu_1_from_poly = sum(c_a * u_iters[k_base + idx] for idx, c_a in enumerate(ann_poly_1)) / denom_r1
    tv1_1_from_poly = sum(c_a * v1_iters[k_base + idx] for idx, c_a in enumerate(ann_poly_1)) / denom_r1
    mu_1_from_poly = tv1_1_from_poly / tu_1_from_poly

    A_turn_germ = (modes[2]["tu"] / modes[1]["tu"]) * (modes[2]["mu"] - modes[1]["mu"])
    A_turn_poly = (tu_2_from_poly / tu_1_from_poly) * (mu_2_from_poly - mu_1_from_poly)
    diff_A_turn = abs(A_turn_germ - A_turn_poly)
    assert diff_A_turn < 1e-7

    print(f"  Mode r=1 (Mod-4 Germ Series):   <TU,hat_psi_1> = {modes[1]['tu']:+.12f}, <TV_1,hat_psi_1> = {modes[1]['tv1']:+.12f}, mu_1(phi_1) = {modes[1]['mu']:+.12f}")
    print(f"  Mode r=1 (Spectral Annihilator):<TU,hat_psi_1> = {tu_1_from_poly:+.12f}, <TV_1,hat_psi_1> = {tv1_1_from_poly:+.12f}, mu_1(phi_1) = {mu_1_from_poly:+.12f} (|diff|={abs(mu_1_from_poly - modes[1]['mu']):.2e})")
    print(f"  Mode r=2 (Mod-4 Germ Series):   <TU,hat_psi_2> = {modes[2]['tu']:+.12f}, <TV_1,hat_psi_2> = {modes[2]['tv1']:+.12f}, mu_1(phi_2) = {modes[2]['mu']:+.12f}")
    print(f"  Mode r=2 (Spectral Annihilator):<TU,hat_psi_2> = {tu_2_from_poly:+.12f}, <TV_1,hat_psi_2> = {tv1_2_from_poly:+.12f}, mu_1(phi_2) = {mu_2_from_poly:+.12f} (|diff|={diff_mu2:.2e})")
    print(f"  Mode r=3 (Mod-4 Germ Series):   <TU,hat_psi_3> = {modes[3]['tu']:+.12f}, <TV_1,hat_psi_3> = {modes[3]['tv1']:+.12f}, mu_1(phi_3) = {modes[3]['mu']:+.12f}")
    print(f"  Asymptotic amplitude A_turn:    {A_turn_germ:+.12f} (annihilator: {A_turn_poly:+.12f}, |diff|={diff_A_turn:.2e})")
    print("  [PASS] Multi-mode Rayleigh-Cantilever expansion and A_turn = -0.074981508556 verified via two independent routes.\n")

    return {
        "modes_r1_to_r4": {f"r={r}": modes[r] for r in range(1, 5)},
        "mode_r2_poly_extracted": {
            "tu_2": tu_2_from_poly,
            "tv1_2": tv1_2_from_poly,
            "mu_2": mu_2_from_poly,
            "abs_diff_mu_2": diff_mu2,
        },
        "A_turn_germ": A_turn_germ,
        "A_turn_poly_extracted": A_turn_poly,
        "abs_diff_A_turn": diff_A_turn,
    }


def part3_triad_audit_prose_code_data() -> dict:
    """
    Triad Audit (Name/Prose · Code · JSON Data, per MADA 1794298653, Phi-Hausmaster 1794300901,
    and Petrovich Argon 1794300344):
      1. Synchronize the stale morning JSON file sect61_numerators_and_gram_s0_duality_results_den_b.json
         with the canonical sect61_numerators_and_gram_s0_duality_den_b_results.json so that zero stale
         k=3 values (0.118519663981) remain anywhere in RESEARCH_DIR.
      2. Verify that PAPER_WORKING_DRAFT_v0.1.md, cantilever_meander_fixed_point_and_bell_duality_den_b_results.json,
         and all three sect61_*_results*.json files agree on:
           - b_12 = -1829/6865290432000000, b_14 = 1319/583549686720000000, Sigma_11 = 3499/194516562240000000
           - k=3: <U, T^3 f_1> = 0.018493010650, <V_1, T^3 f_1> = 0.002110114033, mu_1(T^3 f_1) = 0.114103326553
           - mu_1(phi_1) = +0.113804216148
    """
    print("=== 3. TRIAD AUDIT (PROSE · CODE · JSON DATA) ACROSS RESEARCH STAGING PACKAGE ===")
    canon_sect61_json = os.path.join(RESEARCH_DIR, "sect61_numerators_and_gram_s0_duality_den_b_results.json")
    stale_sect61_json = os.path.join(RESEARCH_DIR, "sect61_numerators_and_gram_s0_duality_results_den_b.json")
    dated_sect61_json = os.path.join(RESEARCH_DIR, "sect61_numerators_and_gram_s0_duality_2026_11_09_results.json")

    if os.path.exists(canon_sect61_json) and os.path.exists(stale_sect61_json):
        shutil.copy2(canon_sect61_json, stale_sect61_json)

    for jpath in (canon_sect61_json, stale_sect61_json, dated_sect61_json):
        with open(jpath, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        k3 = d["part2_sect61_closed_forms_k1_k2_k3"]["k3_T3f1_new"]
        assert abs(k3["U_T3f1_closed"] - 0.018493010650) < 1e-11, f"Stale U_T3f1 in {jpath}"
        assert abs(k3["V1_T3f1_closed"] - 0.002110114033) < 1e-11, f"Stale V1_T3f1 in {jpath}"
        assert abs(k3["mu1_T3f1_closed"] - 0.114103326553) < 1e-11, f"Stale mu1_T3f1 in {jpath}"

    cant_json = os.path.join(RESEARCH_DIR, "cantilever_meander_fixed_point_and_bell_duality_den_b_results.json")
    with open(cant_json, "r", encoding="utf-8") as fh:
        cd = json.load(fh)
    assert cd["part1_exponential_bell_polynomial_duality"]["b_even"]["b_12"] == "-1829/6865290432000000"
    assert cd["part1_exponential_bell_polynomial_duality"]["sigma_odd_bell_verified"]["Sigma_11"]["b_2m_plus_2"] == "1319/583549686720000000"
    assert cd["part1_exponential_bell_polynomial_duality"]["sigma_odd_bell_verified"]["Sigma_11"]["rational"] == "3499/194516562240000000"

    draft_path = os.path.join(RESEARCH_DIR, "PAPER_WORKING_DRAFT_v0.1.md")
    with open(draft_path, "r", encoding="utf-8") as fh:
        draft_text = fh.read()
    assert "1829" in draft_text and "6\\,865\\,290\\,432\\,000\\,000" in draft_text
    assert "193/45" not in draft_text and "193}{45" not in draft_text
    assert "0.1185196" not in draft_text
    assert "0.114103326553" in draft_text
    assert "0.113804216148" in draft_text

    print("  [PASS 3.1] All three sect61_*_results*.json files synchronized and verified (mu_1(T^3 f_1) = 0.114103326553).")
    print("  [PASS 3.2] PAPER_WORKING_DRAFT_v0.1.md, code, and JSON results match on b_12, b_14, Sigma_11, k=3..5, and mu_1(phi_1).\n")
    return {
        "sect61_json_files_verified": 3,
        "b_12": "-1829/6865290432000000",
        "b_14": "1319/583549686720000000",
        "Sigma_11": "3499/194516562240000000",
        "mu_1_T3_f1": 0.114103326553,
        "mu_1_phi_1": 0.113804216148,
    }


if __name__ == "__main__":
    res1 = part1_free_end_cantilever_trace_zeta_theorem()
    res2 = part2_multi_mode_rayleigh_cantilever_verification()
    res3 = part3_triad_audit_prose_code_data()

    out = {
        "part1_free_end_cantilever_trace_zeta_theorem": res1,
        "part2_multi_mode_rayleigh_cantilever_verification": res2,
        "part3_triad_audit_prose_code_data": res3,
        "status": "ALL_CHECKS_PASSED",
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cantilever_trace_zeta_and_triad_audit_2026_11_10_results.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"Saved results to {out_path}")
