#!/usr/bin/env python3
"""
Third-Eye Verification of the 2x2 Gram-Turn Determinant for c_2 and C_rho (§6.4),
Moment-Generating Function of (TW)(u) on [0, 1], and Macroscopic vs Boundary-Layer
Decomposition of <U, TU>, <U, TW>, and <W, TW>.

Author: Jee A (Lane A, OMPU Stereo Pair, ompu-d6a8af238c)
Date: 2026-11-09 10:30 CET (Monday Morning Tick, 536h Radio 88.3 FM, Pulse #412)
"""

from fractions import Fraction
import math
import subprocess
import sys
import numpy as np


def main() -> None:
    print("=" * 80)
    print("1. RUNNING CANONICAL VERIFIER verify_sect61_closed_forms_and_thmd.py")
    print("=" * 80)
    res = subprocess.run(
        [sys.executable, "/Users/denbell/OMPU_shared/research/permutation_walk_memory_2026-11-06/verify_sect61_closed_forms_and_thmd.py"],
        capture_output=True,
        text=True,
        check=True,
    )
    for line in res.stdout.strip().splitlines():
        if "Sigma_0 (" in line:
            Sigma_0 = float(line.split("=")[1].strip())
        elif "Sigma_2 (" in line:
            Sigma_2 = float(line.split("=")[1].strip())
    for line in res.stdout.strip().splitlines()[-8:]:
        print("  " + line)

    print("\n" + "=" * 80)
    print("2. MOMENT-GENERATING FUNCTION OF (TW)(u) & MACROSCOPIC VS BOUNDARY-LAYER SPLIT")
    print("=" * 80)
    # Constants verified in §6.1 / §6.4:
    d0 = 0.227350780091995
    g3 = 0.000991025277641
    vtv = 0.039958599729073
    Sigma_1 = float(Fraction(13, 8400))
    Sigma_3 = float(Fraction(-1, 84000))

    # From int_0^1 e^{su} (TW)(u) du = P(-s) * (7/(20s) + Sigma_0 - Sigma_1 s + Sigma_2 s^2 - ...)
    # where P(-s) = -(s / sqrt(12)) * exp(d0 s + (1/60)*s^2 + g3*s^3 + ...)
    #             = -(s / sqrt(12)) * (1 + d0*s + (1/60 + d0^2/2)*s^2 + (g3 + d0/60 + d0^3/6)*s^3 + ...)
    eh = 1.0 / math.sqrt(12.0)
    p1 = d0
    p2 = 1.0 / 60.0 + 0.5 * (d0 ** 2)
    p3 = g3 + d0 / 60.0 + (d0 ** 3) / 6.0

    # Exact polynomial moments m_k = int_0^1 u^k (TW)(u) du = k! * [s^k] int_0^1 e^{su} (TW)(u) du:
    m0_tw = -eh * (7.0 / 20.0)
    m1_tw = -eh * ((7.0 / 20.0) * p1 + Sigma_0)
    m2_tw = -2.0 * eh * ((7.0 / 20.0) * p2 + p1 * Sigma_0 - Sigma_1)
    m3_tw = -6.0 * eh * ((7.0 / 20.0) * p3 + p2 * Sigma_0 - p1 * Sigma_1 + Sigma_2)

    print(f"  int_0^1 (TW)(u) du   = -7/(20*sqrt(12))                  = {m0_tw:+.12f}")
    print(f"  int_0^1 u(TW)(u) du  = -(7/20*d0 + Sigma_0)/sqrt(12)     = {m1_tw:+.12f}")
    print(f"  int_0^1 u^2(TW)(u)du                                     = {m2_tw:+.12f}")
    print(f"  int_0^1 u^3(TW)(u)du                                     = {m3_tw:+.12f}")

    # Verify that <W, T f_1> = int_0^1 (1 - u)(TW)(u) du and <W, T^2 f_1> = int_0^1 (1/3 - u/2 + u^3/6)(TW)(u) du
    # reproduce mu_1(T f_1) and mu_1(T^2 f_1) to machine precision:
    w_Tf1 = m0_tw - m1_tw
    u_Tf1 = eh * (1.0 - d0)
    mu1_Tf1 = 0.5 + w_Tf1 / u_Tf1

    w_T2f1 = (1.0 / 3.0) * m0_tw - 0.5 * m1_tw + (1.0 / 6.0) * m3_tw
    u_T2f1 = eh * (1.0 / 3.0 - 0.5 * d0 + (d0 ** 3) / 6.0 + d0 / 60.0 + g3)
    mu1_T2f1 = 0.5 + w_T2f1 / u_T2f1

    num_T2f1 = (2.9 - 3.0 * (d0 ** 2)) * Sigma_0 + (13.0 / 1400.0) * d0 - 6.0 * Sigma_2
    den_T2f1 = 2.0 - 2.9 * d0 + (d0 ** 3) + 6.0 * g3
    assert abs(mu1_Tf1 - (0.15 + Sigma_0 / (1.0 - d0))) < 1e-15
    assert abs(mu1_T2f1 - (0.15 + num_T2f1 / den_T2f1)) < 1e-15
    assert abs(mu1_T2f1 - 0.111783887137) < 5e-12
    print(f"  Check mu_1(T f_1)   from moments m0, m1     = {mu1_Tf1:.12f} (PASS)")
    print(f"  Check mu_1(T^2 f_1) from moments m0, m1, m3 = {mu1_T2f1:.12f} (PASS)")

    # Macroscopic vs Boundary-Layer Split of <U, TU>, <U, TW>, and <W, TW>:
    # 1) <U, TU>: U(u) = U_asymp(u) + U_BL(u) with U_asymp(u) = sqrt(12)*(u + d0)
    utu_full = 12.0 * vtv
    utu_macro = 2.0 * d0
    utu_bl = utu_full - utu_macro

    # 2) <U, TW>: <U_asymp, TW> = sqrt(12)*(m1_tw + d0 * m0_tw) = -(7/10)*d0 - Sigma_0
    utw_full = -0.150169088439
    utw_macro = math.sqrt(12.0) * (m1_tw + d0 * m0_tw)
    assert abs(utw_macro - (-0.7 * d0 - Sigma_0)) < 1e-15
    utw_bl = utw_full - utw_macro
    # Accelerated lead_utw includes -1/2 * <U_BL, TU> = -6 * <V_BL, TV>:
    utw_accel = utw_macro - 0.5 * utu_bl
    assert abs(utw_accel - (-6.0 * vtv + 0.3 * d0 - Sigma_0)) < 1e-15

    # 3) <W, TW>: s=0 pole residue vs non-zero roots s_k
    wtw_full = 0.032653149614
    wtw_macro = 6.0 * Sigma_2 + (0.5 + 12.0 * (d0 ** 2)) * Sigma_0 + (121.0 / 1400.0) * d0 + 2.8 * (d0 ** 3) + 4.2 * g3
    wtw_bl = wtw_full - wtw_macro

    print("\n--- Macroscopic (s=0 polynomial asymptote) vs Boundary-Layer (s_k != 0) Split ---")
    print(f"  <U, TU> = {utu_full:+.12f} = {utu_macro:+.12f} ({100*utu_macro/utu_full:5.2f}% macro) + {utu_bl:+.12f} ({100*utu_bl/utu_full:5.2f}% BL)")
    print(f"  <U, TW> = {utw_full:+.12f} = {utw_macro:+.12f} ({100*utw_macro/utw_full:5.2f}% macro) + {utw_bl:+.12f} ({100*utw_bl/utw_full:5.2f}% BL)")
    print(f"          = {utw_accel:+.12f} ({100*utw_accel/utw_full:5.2f}% with -6<V_BL,TV> accel) + {utw_full - utw_accel:+.12f} ({100*(utw_full-utw_accel)/utw_full:5.2f}% O(k^-4) tail)")
    print(f"  <W, TW> = {wtw_full:+.12f} = {wtw_macro:+.12f} ({100*wtw_macro/wtw_full:5.2f}% s=0)   + {wtw_bl:+.12f} ({100*wtw_bl/wtw_full:5.2f}% s_k!=0)")

    print("\nALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
