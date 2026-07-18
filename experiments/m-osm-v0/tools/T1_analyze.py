#!/usr/bin/env python3
"""Analyze the deterministic T1 noisy-Kuramoto experiment without dependencies."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path


LABELS_HZ = (5.0, 8.33, 12.5, 25.0)
LABEL_NAMES = (
    "M4_COGNITIVE_STABILIZATION",
    "M3_EXTERNAL_HARVESTING",
    "M1_SWARM_EXPANSION",
    "M2_SELF_EVOLUTION",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def mean_sd(values: list[float]) -> tuple[float, float]:
    return statistics.mean(values), statistics.stdev(values) if len(values) > 1 else 0.0


def r_squared(y: list[float], predicted: list[float]) -> float:
    center = statistics.mean(y)
    denominator = sum((value - center) ** 2 for value in y)
    numerator = sum((value - estimate) ** 2 for value, estimate in zip(y, predicted))
    return 1.0 - numerator / denominator if denominator > 0.0 else float("nan")


def in_sample_group_r2(y: list[float], groups: list[int]) -> float:
    sums: dict[int, float] = defaultdict(float)
    counts: dict[int, int] = defaultdict(int)
    for value, group in zip(y, groups):
        sums[group] += value
        counts[group] += 1
    predictions = [sums[group] / counts[group] for group in groups]
    return r_squared(y, predictions)


def cross_validated_group_r2(
    y: list[float], groups: list[int], folds: list[int], fold_count: int
) -> float:
    predictions = [float("nan")] * len(y)
    global_mean = statistics.mean(y)
    for held_out in range(fold_count):
        sums: dict[int, float] = defaultdict(float)
        counts: dict[int, int] = defaultdict(int)
        for index, (value, group) in enumerate(zip(y, groups)):
            if folds[index] != held_out:
                sums[group] += value
                counts[group] += 1
        for index, group in enumerate(groups):
            if folds[index] == held_out:
                predictions[index] = sums[group] / counts[group] if counts[group] else global_mean
    return r_squared(y, predictions)


def pearson(x: list[float], y: list[float]) -> float:
    x_mean = statistics.mean(x)
    y_mean = statistics.mean(y)
    numerator = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    x_ss = sum((a - x_mean) ** 2 for a in x)
    y_ss = sum((b - y_mean) ** 2 for b in y)
    return numerator / math.sqrt(x_ss * y_ss)


def balanced_groups(n: int, group_count: int, rng: random.Random) -> list[int]:
    groups = [index % group_count for index in range(n)]
    rng.shuffle(groups)
    return groups


def rank_bins(values: list[float], bin_count: int) -> list[int]:
    result = [0] * len(values)
    ordered = sorted(range(len(values)), key=values.__getitem__)
    for rank, index in enumerate(ordered):
        result[index] = min(bin_count - 1, rank * bin_count // len(values))
    return result


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def aggregate_k_sweep(rows: list[dict[str, str]]) -> list[dict[str, float]]:
    grouped: dict[float, list[float]] = defaultdict(list)
    for row in rows:
        grouped[float(row["K"])].append(float(row["mean_r"]))
    aggregate = []
    for coupling in sorted(grouped):
        mean_r, seed_sd = mean_sd(grouped[coupling])
        aggregate.append({"K": coupling, "mean_r": mean_r, "seed_sd": seed_sd})
    return aggregate


def aggregate_policies(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["policy"]].append(row)
    result = {}
    for policy, policy_rows in grouped.items():
        values = [float(row["mean_r"]) for row in policy_rows]
        mean_r, seed_sd = mean_sd(values)
        result[policy] = {
            "mean_r": mean_r,
            "seed_sd": seed_sd,
            "K": float(policy_rows[0]["K"]),
            "D": float(policy_rows[0]["D"]),
            "effective_gamma": float(policy_rows[0]["effective_gamma"]),
            "Kc": float(policy_rows[0]["Kc"]),
            "K_over_Kc": float(policy_rows[0]["K_over_Kc"]),
        }
    return result


def aggregate_convergence(rows: list[dict[str, str]]) -> dict[str, list[dict[str, float]]]:
    grouped: dict[tuple[str, float, float, int, float], list[float]] = defaultdict(list)
    for row in rows:
        key = (
            row["axis"],
            float(row["axis_value"]),
            float(row["K"]),
            int(row["N"]),
            float(row["dt"]),
        )
        grouped[key].append(float(row["mean_r"]))
    result: dict[str, list[dict[str, float]]] = defaultdict(list)
    for (axis, axis_value, coupling, n, dt), values in grouped.items():
        mean_r, seed_sd = mean_sd(values)
        result[axis].append(
            {
                "axis_value": axis_value,
                "K": coupling,
                "N": n,
                "dt": dt,
                "mean_r": mean_r,
                "seed_sd": seed_sd,
                "replicates": len(values),
            }
        )
    for values in result.values():
        values.sort(key=lambda row: (row["K"], row["axis_value"]))
    return dict(result)


def label_ablation(
    outcome_rows: list[dict[str, str]], assignment_path: Path
) -> dict[str, object]:
    outcome = [float(row["mean_local_alignment"]) for row in outcome_rows]
    abs_omega = [float(row["abs_intrinsic_omega"]) for row in outcome_rows]
    n = len(outcome)
    fold_rng = random.Random(1107)
    fold_order = list(range(n))
    fold_rng.shuffle(fold_order)
    folds = [0] * n
    for rank, index in enumerate(fold_order):
        folds[index] = rank % 5

    mechanistic_groups = rank_bins(abs_omega, 10)
    mechanistic_cv_r2 = cross_validated_group_r2(outcome, mechanistic_groups, folds, 5)
    mechanistic_correlation = pearson(abs_omega, outcome)

    assignment_rows = []
    cv_values = []
    in_sample_values = []
    correlations = []
    fixed_groups = None
    for assignment_index in range(512):
        seed = 20260718 + assignment_index
        groups = balanced_groups(n, len(LABELS_HZ), random.Random(seed))
        frequencies = [LABELS_HZ[group] for group in groups]
        cv_r2 = cross_validated_group_r2(outcome, groups, folds, 5)
        sample_r2 = in_sample_group_r2(outcome, groups)
        correlation = pearson(frequencies, outcome)
        assignment_rows.append(
            {
                "assignment_index": assignment_index,
                "label_seed": seed,
                "cv_r2": cv_r2,
                "in_sample_r2": sample_r2,
                "pearson_label_hz_outcome": correlation,
            }
        )
        cv_values.append(cv_r2)
        in_sample_values.append(sample_r2)
        correlations.append(correlation)
        if assignment_index == 0:
            fixed_groups = groups

    with assignment_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(assignment_rows[0]))
        writer.writeheader()
        writer.writerows(assignment_rows)

    assert fixed_groups is not None
    fixed_frequency = [LABELS_HZ[group] for group in fixed_groups]
    fixed_names = [LABEL_NAMES[group] for group in fixed_groups]
    return {
        "outcome": "per-oscillator mean cos(theta_i - psi), sampled after burn-in",
        "n_agents": n,
        "dynamics_seed": int(outcome_rows[0]["seed"]),
        "global_mean_r": float(outcome_rows[0]["global_mean_r"]),
        "fixed_assignment_seed": 20260718,
        "fixed_assignment_cv_r2": cv_values[0],
        "fixed_assignment_in_sample_r2": in_sample_values[0],
        "fixed_assignment_pearson": correlations[0],
        "random_assignments": 512,
        "random_label_cv_r2_mean": statistics.mean(cv_values),
        "random_label_cv_r2_median": statistics.median(cv_values),
        "random_label_cv_r2_p025": percentile(cv_values, 0.025),
        "random_label_cv_r2_p975": percentile(cv_values, 0.975),
        "random_label_cv_r2_max": max(cv_values),
        "random_label_fraction_cv_r2_positive": sum(value > 0.0 for value in cv_values)
        / len(cv_values),
        "random_label_abs_pearson_mean": statistics.mean(abs(value) for value in correlations),
        "mechanistic_abs_omega_decile_cv_r2": mechanistic_cv_r2,
        "mechanistic_abs_omega_pearson": mechanistic_correlation,
        "causal_label_effect": 0.0,
        "causal_label_effect_reason": "labels are assigned after dynamics and are absent from the equations",
        "fixed_assignments": [
            {
                "agent_id": int(row["agent_id"]),
                "label": name,
                "label_hz": frequency,
            }
            for row, name, frequency in zip(outcome_rows, fixed_names, fixed_frequency)
        ],
    }


def benchmark_label_ablation(
    scoreboard_path: Path, assignment_path: Path, fixed_path: Path
) -> dict[str, object]:
    with scoreboard_path.open(encoding="utf-8") as handle:
        scoreboard = json.load(handle)
    results = scoreboard["results"]
    outcomes = [float(row["exact_recall"]) for row in results]
    conditions = [str(row["condition"]) for row in results]
    n = len(outcomes)
    if n < 2 * len(LABELS_HZ):
        raise ValueError("benchmark ablation requires at least two rows per label")

    # Leave-one-out avoids evaluating a label mean on the row used to fit it.
    folds = list(range(n))
    assignment_rows = []
    fixed_groups = None
    for assignment_index in range(512):
        seed = 20260718 + assignment_index
        groups = balanced_groups(n, len(LABELS_HZ), random.Random(seed))
        frequencies = [LABELS_HZ[group] for group in groups]
        assignment_rows.append(
            {
                "assignment_index": assignment_index,
                "label_seed": seed,
                "loo_cv_r2": cross_validated_group_r2(
                    outcomes, groups, folds, n
                ),
                "in_sample_r2": in_sample_group_r2(outcomes, groups),
                "pearson_label_hz_outcome": pearson(frequencies, outcomes),
            }
        )
        if assignment_index == 0:
            fixed_groups = groups

    with assignment_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(assignment_rows[0]))
        writer.writeheader()
        writer.writerows(assignment_rows)

    assert fixed_groups is not None
    fixed_rows = [
        {
            "condition": condition,
            "exact_recall": outcome,
            "label": LABEL_NAMES[group],
            "label_hz": LABELS_HZ[group],
        }
        for condition, outcome, group in zip(conditions, outcomes, fixed_groups)
    ]
    with fixed_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fixed_rows[0]))
        writer.writeheader()
        writer.writerows(fixed_rows)

    cv_values = [float(row["loo_cv_r2"]) for row in assignment_rows]
    in_sample_values = [float(row["in_sample_r2"]) for row in assignment_rows]
    correlations = [
        float(row["pearson_label_hz_outcome"]) for row in assignment_rows
    ]
    return {
        "source": "raw/scoreboard.json existing blind-recall benchmark",
        "outcome": "exact_recall",
        "n_agent_runs": n,
        "conditions": conditions,
        "assignment_timing": "post hoc; labels were absent from agent inputs",
        "fixed_assignment_seed": 20260718,
        "fixed_assignment_loo_cv_r2": cv_values[0],
        "fixed_assignment_in_sample_r2": in_sample_values[0],
        "fixed_assignment_pearson": correlations[0],
        "random_assignments": len(assignment_rows),
        "random_label_loo_cv_r2_mean": statistics.mean(cv_values),
        "random_label_loo_cv_r2_median": statistics.median(cv_values),
        "random_label_loo_cv_r2_p025": percentile(cv_values, 0.025),
        "random_label_loo_cv_r2_p975": percentile(cv_values, 0.975),
        "random_label_fraction_loo_cv_r2_positive": sum(
            value > 0.0 for value in cv_values
        )
        / len(cv_values),
        "random_label_in_sample_r2_median": statistics.median(in_sample_values),
        "random_label_in_sample_r2_p975": percentile(in_sample_values, 0.975),
        "random_label_abs_pearson_mean": statistics.mean(
            abs(value) for value in correlations
        ),
        "causal_label_effect": 0.0,
        "causal_label_effect_reason": (
            "labels were assigned after the measured runs and were absent from prompts"
        ),
        "timing_signal_available": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_dir", type=Path)
    args = parser.parse_args()
    raw_dir = args.raw_dir

    k_rows = read_csv(raw_dir / "T1_k_sweep.csv")
    policy_rows = read_csv(raw_dir / "T1_c06_policies.csv")
    convergence_rows = read_csv(raw_dir / "T1_convergence.csv")
    outcome_rows = read_csv(raw_dir / "T1_c07_agent_outcomes.csv")

    gamma = 0.25
    diffusion = 0.12
    draft_k = 3.45
    kc = 2.0 * (gamma + diffusion)
    near_onset_r2_coefficient = (2.0 * diffusion + gamma) / (
        2.0 * (diffusion + gamma) ** 2
    )
    sweep = aggregate_k_sweep(k_rows)
    slopes = [
        {
            "lower_K": lower["K"],
            "upper_K": upper["K"],
            "slope": (upper["mean_r"] - lower["mean_r"]) / (upper["K"] - lower["K"]),
        }
        for lower, upper in zip(sweep, sweep[1:])
    ]
    steepest = max(slopes, key=lambda row: row["slope"])
    draft_simulation = next(row for row in sweep if math.isclose(row["K"], draft_k))

    ablation = label_ablation(
        outcome_rows, raw_dir / "T1_c07_label_assignments.csv"
    )
    fixed_assignments = ablation.pop("fixed_assignments")
    with (raw_dir / "T1_c07_fixed_labels.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fixed_assignments[0]))
        writer.writeheader()
        writer.writerows(fixed_assignments)

    benchmark_ablation = benchmark_label_ablation(
        raw_dir / "scoreboard.json",
        raw_dir / "T1_c07_benchmark_label_assignments.csv",
        raw_dir / "T1_c07_benchmark_fixed_labels.csv",
    )

    summary = {
        "experiment": "T1_math_kuramoto",
        "analytic": {
            "gamma": gamma,
            "D": diffusion,
            "draft_K": draft_k,
            "Kc": kc,
            "linear_eigenvalue": "lambda = K/2 - (gamma + D)",
            "draft_sqrt_K_minus_Kc": math.sqrt(draft_k - kc),
            "near_onset_r2_coefficient": near_onset_r2_coefficient,
            "near_onset_formula": "r^2 = ((2D+gamma)/(2(D+gamma)^2))*(K-Kc) + O((K-Kc)^2)",
        },
        "simulation": {
            "integrator": "Euler-Maruyama",
            "rng": "PCG32 plus Marsaglia polar Gaussian",
            "frequency_grid": "centered Lorentzian quantiles, shuffled per seed",
            "k_sweep": sweep,
            "steepest_discrete_r_slope": steepest,
            "draft_K_result": draft_simulation,
            "convergence": aggregate_convergence(convergence_rows),
        },
        "c06_policies": aggregate_policies(policy_rows),
        "c07_simulated_label_ablation": ablation,
        "c07_measured_agent_label_ablation": benchmark_ablation,
    }
    with (raw_dir / "T1_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
