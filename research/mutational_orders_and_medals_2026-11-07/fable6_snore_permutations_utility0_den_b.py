#!/usr/bin/env python3
"""
OMPU Mutation Roulette Micro-Experiment (Utility = 0.0):
Exact 38-Digit Count of Permutations in S_36 that Snore "zzzzzZZZZzzzZZZzzz" (Fable 6, 0.0809 Hz)
and Run-Plus-Turn Memory Compression (6.267 * r^2 ~ 56x per snore cycle).

Prompt from `awards.py roulette`:
  «Сделай микро-эксперимент с заведомо нулевой практической пользой (Utility = 0),
   исключительно чтобы посмотреть, что получится.»

Author: Den B (Ден Б, ompu-7f698bd908, stereo_v1/b, Google Antigravity)
Date: 2026-11-07 (20:35 CET Evening Tick)
Utility: 0.0 (Pure curiosity & cosmic snore acoustics)
"""

from fractions import Fraction as F
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, "/Users/denbell/OMPU_shared/petrovich_garage_v0/workbench/compact_height_2026-11-06-antigravity-1620")
import compact_height as ch


def eval_snore(snore_str: str):
    signs = "".join("+" if c == "z" else "-" for c in snore_str)
    pieces = [[F(1), F(-1)]]
    for i in range(1, len(signs)):
        if signs[i] == signs[i - 1]:
            pieces = ch.op_same(pieces)
        else:
            pieces = ch.op_flip(pieces)
    mass = sum(ch.poly_int_0_1(p) for p in pieces)
    flip = ch.poly_int_0_1(ch.op_flip(pieces)[0])
    p_next_z = F(1) - flip / mass
    return signs, mass, p_next_z


def main():
    snore = "zzzzzZZZZzzzZZZzzz"
    signs, prob_snore, p_next_z = eval_snore(snore)
    n_odd = len(snore)
    m_perm = 2 * n_odd  # S_36
    fact_36 = math.factorial(m_perm)
    exact_count = prob_snore * fact_36
    assert exact_count.denominator == 1

    # Fundamental Euler-Bernoulli cantilever mode lambda_1 and its power-spectrum square:
    kappa_1 = 1.875104068711961
    lambda_1 = 1.0 / (kappa_1 ** 2)
    f_snore_hz = lambda_1 ** 2

    print("=== OMPU MUTATION ROULETTE MICRO-EXPERIMENT (UTILITY = 0.0) ===")
    print(f"  1) Cosmic Snore String (Fable 6): '{snore}' -> '{signs}' (n={n_odd} odd steps in S_{m_perm})")
    print(f"  2) Cantilever Power Frequency:    lambda_1^2 = ({lambda_1:.10f})^2 = {f_snore_hz:.8f} Hz (~ 0.08 Hz!)")
    print(f"  3) Exact Rational Probability:    {prob_snore.numerator}")
    print(f"                                  / {prob_snore.denominator}")
    print(f"  4) Exact Snoring Permutations in S_36 (out of 36! = {fact_36}):")
    print(f"     N_snore(S_36) = {exact_count.numerator}")
    print(f"  5) Exact Next-Breath Forecast (19th breath):")
    print(f"     P('z' inhale | snore) = {float(p_next_z):.12f},  P('Z' exhale | snore) = {float(1 - p_next_z):.12f}\n")

    print("=== SUFFIX MEMORY COMPRESSION ACROSS SNORE CYCLES (6.267 * r^2 ~ 56x PER CYCLE) ===")
    suffixes = [
        ("0 turns ('zzz')", "zzz"),
        ("1 turn  ('Zzzz')", "Zzzz"),
        ("1 prev run ('ZZZzzz')", "ZZZzzz"),
        ("2 prev runs ('zzzZZZzzz')", "zzzZZZzzz"),
        ("3 prev runs ('ZZZZzzzZZZzzz')", "ZZZZzzzZZZzzz"),
        ("4 prev runs ('zzzzzZZZZzzzZZZzzz')", "zzzzzZZZZzzzZZZzzz"),
    ]
    suffix_table = []
    prev_err = None
    for label, s in suffixes:
        _, _, pz = eval_snore(s)
        err = float(abs(pz - p_next_z))
        ratio = (prev_err / err) if (prev_err is not None and err > 0) else 0.0
        print(f"  {label:36s}: P(z) = {float(pz):.12f} | err = {err:.3e} | compression = {ratio:5.1f}x")
        if err > 0:
            prev_err = err
        suffix_table.append({
            "suffix": s,
            "P_next_z": float(pz),
            "abs_error_vs_full": err,
            "compression_ratio": ratio,
        })

    out = {
        "author": "Den B (ompu-7f698bd908, stereo_v1/b, Google Antigravity)",
        "date": "2026-11-07",
        "utility": 0.0,
        "snore_string": snore,
        "sign_signature": signs,
        "cantilever_power_freq_hz": f_snore_hz,
        "exact_probability_rational": str(prob_snore),
        "exact_probability_float": float(prob_snore),
        "S_36_total_permutations": str(fact_36),
        "S_36_exact_snoring_permutations": str(exact_count.numerator),
        "P_19th_breath_z": float(p_next_z),
        "P_19th_breath_Z": float(1 - p_next_z),
        "suffix_compression_table": suffix_table,
    }
    Path(__file__).with_name("fable6_snore_permutations_utility0_results.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )


if __name__ == "__main__":
    main()
