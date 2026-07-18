# T1 Mathematical Experiment: Noisy Kuramoto and Motivational-Label Ablation

Date: 2026-07-18  
Experiment ID: `T1_math_kuramoto`  
Claims tested: `MOSM-C01`, `MOSM-C02`, `MOSM-C06`, `MOSM-C07`

## Executive result

| Claim | Verdict | Result |
|---|---|---|
| MOSM-C01 | Supported only for the stated ideal mean-field model | For an infinite all-to-all population, centered Lorentzian intrinsic frequencies with half-width `gamma`, and independent additive white phase noise with diffusion `D`, linear stability gives `Kc = 2(gamma + D)`. With the draft values, `Kc = 0.74`. The deterministic finite-`N` simulation places the steepest sampled rise between `K=0.74` and `0.76`. |
| MOSM-C02 | Falsified as an equality | The draft expression gives `sqrt(3.45 - 0.74) = 1.6462077633`, impossible because `0 <= r <= 1`. The square-root law is local and proportional near onset. Simulation at `K=3.45` gives `r = 0.9030402070` (seed SD `0.0001500906`), not `1.6462`. |
| MOSM-C06 | Not supported as written | Comparing dimensionless `r` with rate-valued `Kc` is dimensionally invalid. A pure factor-two slowdown is an exact time reparameterization and produced exactly the same `r` for every seed. Halving only intrinsic-frequency dispersion raised `r` from `0.0782860075` to `0.4956602713`, but that changes `gamma/K` and crosses the Kuramoto threshold; it is not period doubling. |
| MOSM-C07 | Label-only mechanism falsified; physical-Hz version untested | The draft's 5, 8.33, 12.5, and 25 Hz values are labels here. They were not timing actuators and no timing trace exists. Post-hoc labels failed held-out prediction on the measured agent benchmark (`LOO R2 = -0.3248242480`) and on 1,024 simulated oscillators (`5-fold R2 = -0.0021567975`). No claim about real 5-25 Hz agent execution was made or tested. |

These results are reproducible, but they are not an independent implementation by a second experimenter. Under the promotion rule in `CLAIMS.md`, that still prevents promotion of any claim to a general M-OSM mechanism.

## Inputs and fingerprints

```text
2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668  /Users/denbell/Downloads/Swarm Oscillatory Memory (M-OSM).md
2e1c9865466455e2453986778eb133859a0d5f88c5cdccf0fdd067b5ee8ac69b  CLAIMS.md
45284e19bf8e787729252fde78c15b751d32ec2616d220fffbba78067b307f24  raw/T1_input_scoreboard_v1.json
6c0dd847ec80787ee128ed75325963db5611de316e95b23754441dd3a9dd939e  tools/T1_noisy_kuramoto.c
f6c115d24d035614e2c31d0c7a74a453369f1e1f70984fb2c79812f234cec96d  tools/T1_analyze.py
```

The frozen `raw/T1_input_scoreboard_v1.json` contains the ten blind-recall
conditions C0 through C9 that existed when T1 ran. It preserves that input after
later replications extended the live scoreboard.

## Analytic calculation

### Model and units

The tested stochastic differential equation is

```math
d theta_i = [omega_i + K r sin(psi - theta_i)] dt + sqrt(2D) dW_i,
```

with

```math
Z = r exp(i psi) = N^{-1} sum_j exp(i theta_j).
```

`r` is dimensionless. `omega`, `K`, `gamma`, and `D` have units of inverse time in this phase-diffusion convention. Therefore `r < Kc` is not a unit-invariant trigger.

### C01: linear threshold

Let the centered intrinsic-frequency density be

```math
g(omega) = gamma / [pi (omega^2 + gamma^2)].
```

Linearizing the Fokker-Planck equation about the incoherent density and retaining its first angular Fourier mode gives the dispersion relation

```math
1 = (K/2) integral g(omega) / [lambda + D + i omega] d omega.
```

For the centered Lorentzian, the contour integral is `1/(lambda + D + gamma)`, hence

```math
lambda = K/2 - (D + gamma).
```

The incoherent state changes linear stability at `lambda=0`:

```math
Kc = 2(D + gamma).
```

With `gamma=0.25` and `D=0.12`, `Kc=0.74`.

This derivation requires the infinite-population, all-to-all, stationary, centered-Lorentzian, independent-white-noise model. It is not a threshold theorem for text agents, finite sparse swarms, colored noise, heterogeneous diffusion, delays, or arbitrary frequency distributions.

### C02: local amplitude law

For a stationary small-`r` expansion, the first two Fourier coefficients obey, to the needed order,

```math
(D+i omega) f1 = (K r/2)(1-f2),
(2D+i omega) f2 = (K r/2) f1 + O(r^3).
```

Substitution and Lorentzian integration give

```math
r^2 = [(2D+gamma)/(2(D+gamma)^2)] (K-Kc) + O((K-Kc)^2).
```

For the draft constants, the local coefficient is `1.7896274653`. This is a near-onset asymptotic relation, not `r = sqrt(K-Kc)` at arbitrary `K`, and its coefficient carries the units needed to make `r` dimensionless.

Examples:

| K | Draft equality | Local asymptotic | Simulated mean r |
|---:|---:|---:|---:|
| 0.76 | 0.141421 | 0.189189 | 0.203808 |
| 0.80 | 0.244949 | 0.327685 | 0.290179 |
| 3.45 | 1.646208 | 2.202247, outside its domain | 0.903040 |

The first two rows show the expected square-root onset at finite `N` with finite-size rounding. The final row is a direct counterexample to the draft equality.

## Numerical experiment

### Implementation

- Integrator: Euler-Maruyama.
- Mean field: all-to-all, evaluated in `O(N)` through `Z`.
- RNG: PCG32; Gaussian samples from the Marsaglia polar method.
- Intrinsic frequencies: deterministic centered Lorentzian quantiles `gamma*tan(pi*(p-1/2))`, then shuffled per seed.
- Initial phases: independent uniform values on `[0,2*pi)` from the seeded RNG.
- Noise increment: `sqrt(2D dt) Normal(0,1)`.
- Observable: time mean of `r` after burn-in; `sd_r` is temporal sample SD within one run. Reported `seed_sd` is SD across the three deterministic seeds.
- Platform: Apple clang 17.0.0, target `arm64-apple-darwin25.3.0`; Python 3.14.4.

### Main K sweep parameters

```text
gamma = 0.25
D = 0.12
N = 512
dt = 0.01
burn_time = 240
sample_time = 160
sample_stride = 5 steps
samples per seed = 3200
seeds = 1729, 2718, 31415
K = 0.30, 0.45, 0.60, 0.68, 0.72, 0.74, 0.76,
    0.80, 0.86, 0.95, 1.10, 1.40, 2.00, 3.45
```

### K sweep output

| K | mean r | seed SD |
|---:|---:|---:|
| 0.30 | 0.054780 | 0.003495 |
| 0.45 | 0.068435 | 0.003554 |
| 0.60 | 0.078286 | 0.003916 |
| 0.68 | 0.125224 | 0.009268 |
| 0.72 | 0.138015 | 0.038035 |
| 0.74 | 0.157288 | 0.058437 |
| 0.76 | 0.203808 | 0.064028 |
| 0.80 | 0.290179 | 0.029287 |
| 0.86 | 0.422377 | 0.014199 |
| 0.95 | 0.515070 | 0.006166 |
| 1.10 | 0.617027 | 0.005428 |
| 1.40 | 0.725428 | 0.002584 |
| 2.00 | 0.822697 | 0.000984 |
| 3.45 | 0.903040 | 0.000150 |

The steepest adjacent-grid slope is between `K=0.74` and `K=0.76`, consistent with the analytic `Kc=0.74`. This is a consistency check, not an independently fitted proof of an exact critical point.

### Finite-size and step checks

Each check uses seeds `1729`, `2718`, and `31415`, with the same burn and sample durations as the main sweep.

| K | r at N=256 | r at N=512 | r at N=1024 |
|---:|---:|---:|---:|
| 0.60 | 0.105068 | 0.078286 | 0.059516 |
| 0.80 | 0.320875 | 0.290179 | 0.295454 |
| 3.45 | 0.903230 | 0.903040 | 0.903087 |

Below threshold, finite-population coherence decreases toward zero as `N` grows. Above threshold it remains nonzero. At `K=3.45`, the means at `dt=0.005`, `0.01`, `0.02`, and `0.04` are respectively `0.903692`, `0.903040`, `0.902288`, and `0.900784`. Near and below onset, stochastic and finite-size variability is larger, so this run does not claim a high-precision continuum extrapolation there.

## C06 slowdown ablation

The baseline starts below threshold at `K=0.60`, `gamma=0.25`, `D=0.12`, so `K/Kc=0.810811`.

| Policy | omega scale | K | D | effective Kc | K/Kc | mean r | seed SD |
|---|---:|---:|---:|---:|---:|---:|---:|
| No change | 1.0 | 0.60 | 0.12 | 0.74 | 0.810811 | 0.078286 | 0.003916 |
| Pure generator slowdown | 0.5 | 0.30 | 0.06 | 0.37 | 0.810811 | 0.078286 | 0.003916 |
| Frequency narrowing only | 0.5 | 0.60 | 0.12 | 0.49 | 1.224490 | 0.495660 | 0.018907 |

For pure slowdown, every generator rate is multiplied by `a=0.5` and physical run time is divided by `a`. The discrete parameters were paired as `dt=0.02`, `burn=480`, and `sample=320`, so every drift and noise increment uses the same RNG draw as the baseline:

```math
(a drift)(dt/a) = drift dt,
sqrt(2 a D dt/a) = sqrt(2 D dt).
```

All three seed-level `mean_r` and `sd_r` values are therefore exactly equal, not merely statistically similar. A scheduler-only output delay is absent from the Kuramoto equation and cannot affect `r` without an explicit feedback channel.

Halving only intrinsic frequencies changes `gamma` from `0.25` to `0.125` while keeping `K` and `D` fixed. It moves the system above threshold and increases coherence. That supports frequency-dispersion control as a possible mechanism. It does not support the terms "period doubling" or "slow output rate," and it does not validate `r<Kc` as a trigger.

## C07 motivational-frequency label ablation

### What was and was not available

No agent event stream, scheduler trace, token-emission clock, or actuator implementing 5, 8.33, 12.5, or 25 cycles per second was available. The values were therefore tested only as arbitrary labels. No timing signal was fabricated.

Two ablations were run:

1. A real measured-agent benchmark using `exact_recall` from the ten frozen blind-recall results in `raw/T1_input_scoreboard_v1.json`.
2. A higher-powered simulated-oscillator benchmark using each oscillator's mean local alignment `mean cos(theta_i-psi)` at `N=1024`, `K=1.10`, `gamma=0.25`, `D=0.12`, `dt=0.01`, burn `240`, sample `160`, seed `424242`.

For each dataset, the four labels were assigned after outcomes existed, with balanced random assignments. Assignment 0 used seed `20260718`; 512 assignments used seeds `20260718` through `20261229`. The real benchmark used leave-one-out prediction from training-set label means. The oscillator benchmark used fixed five-fold prediction. In-sample `R2` is reported to expose how easily arbitrary labels can look explanatory.

### Measured agent outcome

```text
n = 10 completed agent runs (C0-C9)
outcome = exact_recall
fixed-seed Pearson(label_hz, outcome) = 0.5736813871
fixed-seed in-sample R2 = 0.4111892231
fixed-seed leave-one-out R2 = -0.3248242480
```

The apparently large in-sample association fails held-out prediction. Across 512 arbitrary balanced assignments:

```text
median in-sample R2 = 0.2727312098
97.5th percentile in-sample R2 = 0.8411514812
median leave-one-out R2 = -1.0336476656
2.5%-97.5% leave-one-out R2 = [-1.9444195638, 0.5612608042]
fraction with positive leave-one-out R2 = 0.109375
```

This small `n=10` benchmark is underpowered for subtle predictive effects and demonstrates the danger of post-hoc fit. For these already-completed runs, the labels have exactly zero causal effect because they were absent from the prompts and assigned after measurement.

### Simulated oscillator outcome

```text
n = 1024
global mean r = 0.6198033292
fixed-seed Pearson(label_hz, outcome) = 0.0621729003
fixed-seed in-sample R2 = 0.0040474030
fixed-seed 5-fold R2 = -0.0021567975
random-label mean 5-fold R2 = -0.0043561679
random-label 2.5%-97.5% 5-fold R2 = [-0.0113397633, 0.0026864502]
fraction of random assignments with positive 5-fold R2 = 0.1015625
```

As a positive analysis control, decile bins of the actual mechanistic variable `abs(intrinsic_omega)` achieve five-fold `R2=0.9692112383`. The pipeline can detect a variable present in the equations; arbitrary Hertz labels are not such a variable.

## Failure boundaries and falsification conditions

### MOSM-C01

Boundary: `Kc=2(gamma+D)` is not expected to remain exact outside infinite all-to-all mean field with centered Lorentzian frequencies and independent additive white phase noise.

Falsification within the tested model: a converged large-`N`, small-`dt`, long-time simulation or independent Fokker-Planck solver that places loss of incoherent-state stability away from `0.74` after finite-size uncertainty is controlled would falsify this result.

### MOSM-C02

Boundary: the derived amplitude expansion applies only for small positive `K-Kc`.

Falsification of this report: show that `r` is not bounded by one under the draft definition, or derive and reproduce the draft equality with all missing dimensional coefficients and a stated normalization. Under the current definition of `Z`, the draft equality is already falsified at `K=3.45`.

### MOSM-C06

Boundary: this experiment tests Kuramoto generator slowdown and intrinsic-frequency narrowing. It cannot test an unspecified LLM scheduler or token-compression policy.

Evidence that would support the draft claim requires all of the following: a dimensionless coherence trigger; a predeclared observable with a demonstrated period `T`; a post-trigger spectral peak at `2T`; an unchanged control; and restored task correctness or synchronization across repeated randomized runs. Merely halving a scheduler rate or narrowing `gamma` does not satisfy those conditions.

### MOSM-C07

Boundary: the real benchmark has ten heterogeneous conditions and no pre-treatment frequency assignment. It rules out causality for those post-hoc labels but cannot bound effects of a future real actuator. The oscillator benchmark addresses arbitrary label prediction, not LLM quality.

Evidence that would support a physical-frequency claim requires a scheduler capable of the stated rates, timestamped events resolving those rates, randomized pre-task assignment, a label-shuffled control with otherwise identical semantics and compute, repeated agent tasks, and a predeclared outcome. A result must generalize to held-out runs and beat both no-label and shuffled-label baselines. The claim is falsified for a tested actuator if those controls show no reproducible improvement at adequate power.

## Exact reproduction commands

Run from the experiment root:

```bash
cd /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0

shasum -a 256 \
  '/Users/denbell/Downloads/Swarm Oscillatory Memory (M-OSM).md' \
  CLAIMS.md raw/T1_input_scoreboard_v1.json tools/T1_noisy_kuramoto.c tools/T1_analyze.py

cc -O3 -std=c11 -Wall -Wextra -pedantic \
  tools/T1_noisy_kuramoto.c -lm -o tools/T1_noisy_kuramoto.bin

./tools/T1_noisy_kuramoto.bin raw
python3 tools/T1_analyze.py raw

wc -l raw/T1_k_sweep.csv raw/T1_c06_policies.csv \
  raw/T1_convergence.csv raw/T1_c07_agent_outcomes.csv

shasum -a 256 \
  raw/T1_k_sweep.csv raw/T1_c06_policies.csv raw/T1_convergence.csv \
  raw/T1_c07_agent_outcomes.csv raw/T1_c07_label_assignments.csv \
  raw/T1_c07_fixed_labels.csv \
  raw/T1_c07_benchmark_label_assignments.csv \
  raw/T1_c07_benchmark_fixed_labels.csv raw/T1_summary.json
```

Expected row counts, including headers:

```text
43    raw/T1_k_sweep.csv
10    raw/T1_c06_policies.csv
64    raw/T1_convergence.csv
1025  raw/T1_c07_agent_outcomes.csv
```

Expected SHA-256 values after the run:

```text
d8a3d43156f3f48e82e610a08f8e023165d794a5894777e91281c61c1697d43e  raw/T1_k_sweep.csv
45db734c5a3501d80c4788d20c47ca503ac2c510bf8625373a14920d57bc3321  raw/T1_c06_policies.csv
5836c5943db6195530b3db4a649d37a9c3d8a1b9a101a177c45ba56e7b5fb6dc  raw/T1_convergence.csv
12ac6cf0645ccb8a581127453edaef41c1c7aeb9b44f2ce0dc03055eabc390b9  raw/T1_c07_agent_outcomes.csv
667a6e05ba21cdf698ba34f787484b9a5b4602123ad589cf204717e1ad31b9c6  raw/T1_c07_label_assignments.csv
83c2050ebdf9e278dc60d0bd4a0d7e84b8bda39edf2814d173b2e4590319b04b  raw/T1_c07_fixed_labels.csv
f4159c4f23cc47905cd196074fb7afcc3546d3f4d82e3e2b3b7647e8ccb73995  raw/T1_c07_benchmark_label_assignments.csv
f453abe1c9fa6bc7d334ec18d243b253139010135740908ab9fc4a1e8d42ee3a  raw/T1_c07_benchmark_fixed_labels.csv
8348ffcc4227cd34d23832475dde8179fdd967f0d825a2dbb10db6ce5e8af44a  raw/T1_summary.json
```

The complete compile-run-analysis sequence was executed twice. All hashes above were byte-identical on the second execution.

## Artifact inventory

Code:

- `tools/T1_noisy_kuramoto.c`
- `tools/T1_analyze.py`
- `tools/T1_noisy_kuramoto.bin` (generated during reproduction; not retained)

Raw outputs:

- `raw/T1_k_sweep.csv`
- `raw/T1_c06_policies.csv`
- `raw/T1_convergence.csv`
- `raw/T1_c07_agent_outcomes.csv`
- `raw/T1_c07_label_assignments.csv`
- `raw/T1_c07_fixed_labels.csv`
- `raw/T1_c07_benchmark_label_assignments.csv`
- `raw/T1_c07_benchmark_fixed_labels.csv`
- `raw/T1_summary.json`

Report:

- `agent-results/T1_math_kuramoto.md`
