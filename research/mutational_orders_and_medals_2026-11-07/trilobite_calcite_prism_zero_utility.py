"""Micro-experiment with Utility = 0.0 for OMPU Mutation Roulette.

Connects:
1. Flament & Dhungana (Nature) / Phi-Hausmaster's monologue "Skeleton of the Erased"
   (billion years of Great Unconformity eroded into Cambrian calcium for trilobite shells).
2. Optical calcite (CaCO3) as the physical material of trilobite double-convex lenses.
3. 512 hours of Radio 88.3 FM (2^9 = 8^3) as monochromatic harmonic wavelength lambda = 512 nm.
4. Jee A's Euler-Bernoulli beam damping factor (kappa_2/kappa_1)^2 = 6.266893.
"""

import math

def run():
    n_o = 1.6584  # ordinary ray
    n_e = 1.4864  # extraordinary ray
    delta_n = n_e - n_o  # -0.1720

    hours = 512
    lambda_light_nm = 512.0  # cyan-green light harmonic

    theta_brewster = math.degrees(math.atan(n_o))
    kappa_ratio_sq = 6.26689303
    phi_cambrian = abs(delta_n) / kappa_ratio_sq

    return {
        "wavelength_nm": lambda_light_nm,
        "n_o": n_o,
        "n_e": n_e,
        "delta_n": delta_n,
        "brewster_deg": theta_brewster,
        "beam_damping": kappa_ratio_sq,
        "cambrian_euler_invariant": phi_cambrian,
        "utility": 0.0
    }

if __name__ == "__main__":
    res = run()
    for k, v in res.items():
        print(f"{k}: {v}")
