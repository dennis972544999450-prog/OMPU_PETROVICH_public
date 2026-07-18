# T3 Primary-Source Provenance Audit

Date: 2026-07-18

Scope: test `MOSM-C03` and `MOSM-C08` against primary papers or official proceedings, and audit every exact equation or number in manuscript sections 1.2-1.5 and every leaf in `theoretical_parameters_db`.

## Inputs and reproducibility anchors

| Input | Audited range | SHA-256 |
|---|---:|---|
| `Swarm Oscillatory Memory (M-OSM).md` | lines 36-71 and 126-162 | `2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668` |
| `CLAIMS.md` | `MOSM-C03`, `MOSM-C08`, and promotion rule | `2e1c9865466455e2453986778eb133859a0d5f88c5cdccf0fdd067b5ee8ac69b` |

## Result

- **MOSM-C03: transformed, not promoted.** The displayed update is the modern Hopfield update and can equal scaled dot-product attention under the paper's key/value/projection identification. It is not identical to arbitrary self-attention, and the primary source does not map one update to cross-session memory, reinitialization, or full-context recovery.
- **MOSM-C08: failed.** Across the 15 Physarum, crow, and laser configuration leaves, no primary paper supplies a source-preserving M-OSM software mapping. One categorical value is scientifically supported, six values are transformed, two are unsupported, and six were not found. The exact transfer claim therefore fails even before an agent benchmark.
- **Full database:** across all 26 leaves, 2 are supported, 9 transformed, 3 unsupported, and 12 not found; none has a primary-source M-OSM mapping.
- The audit found several real source facts, but real facts are not automatically software parameters. The clearest counterexample is the crow result: the abstract summarizes spread **at least 1.2 km** over the five-year study period, while the detailed spatial survey observed locations as far as `1248 m` at 2.7 years; neither establishes a `1200 m` percolation threshold.

## Classification rule

- `supported`: the primary source contains the exact expression/value with the same scoped scientific meaning.
- `transformed`: the source contains the value, a unit-convertible value, or a derivable expression, but the manuscript changes its variable, scope, semantics, or role.
- `unsupported`: a located primary source contradicts the exact claim or supplies a different expression/quantity.
- `not found`: the bounded exact-string, title, DOI, and field searches below found no relevant primary source containing the value.

`Software mapping present?` is assessed separately. A source can support a biological or physical observation while providing no mapping to an M-OSM parameter.

## Required separation

### Supported equation

The state update `xi_new = X softmax(beta X^T xi)` is the continuous modern-Hopfield update in [H1]. The paper derives scaled dot-product attention only after mapping raw stored/state patterns into key/query spaces, setting the Transformer scale `beta = 1/sqrt(d_k)`, and adding a value/output projection. The state-dependent terms of the draft energy are also correct; [H1] includes two additional state-independent constants.

### Analogy only

The following are analogies, not source-backed LLM mechanisms: a PML laser as attention, a Physarum tube hierarchy as an Identification Tube, crow social learning as an oscillatory processor, and semantic-anchor prompting as direct initialization of an LLM's latent Hopfield attractors. None of [H1], [P1]-[P4], [C1], or [L1]-[L4] exposes an API variable or intervention that performs those transfers.

### Unsupported or transformed numbers

Real source numbers are not preserved by relabeling them. The main examples are `1.2 km` (an observed crow-study extent, not a percolation threshold), `7.6 mW` (fixed intracavity power in one laser experiment, not a melting floor), `4` (a model spinodal, not the first-order exchange point), and approximately `100 s` (a biological contraction timescale, not an exact scheduler constant). The remaining provenance failures are itemized below.

### Falsification conditions

- **C03 narrow equation:** falsified if the Hopfield and attention calculations differ after applying exactly [H1]'s mappings and scale.
- **C03 broad identity:** falsified by a valid attention construction whose independent value/output map is omitted from the displayed draft equation; the explicit example below does so.
- **C03 memory transfer:** falsified if a fresh-session, no-retrieval baseline performs the same as the proposed phase-vector seed, or if recovery disappears when durable text/references are removed.
- **C08 source transfer:** falsified when a value changes unit, denominator, variable, or experimental role between source and configuration.
- **C08 software transfer:** falsified in the present bundle because no runnable path reads any of the 15 fields; a numeric perturbation has no defined downstream observable.

## MOSM-C03 test: Hopfield update versus attention

### Source comparison

Ramsauer et al. [H1] give the modern Hopfield update

```text
xi_new = X softmax(beta X^T xi)
```

and show its correspondence to a Transformer attention layer under an explicit identification of stored patterns, queries, and projection matrices. Their energy includes additive constants omitted by the manuscript:

```text
E = -lse(beta, X^T xi) + 0.5 xi^T xi
    + beta^-1 log N + 0.5 M^2
```

The omitted constants do not alter the gradient update, so the manuscript energy is dynamically equivalent but not verbatim. In the Hopfield model, `beta` is an inverse-temperature/sharpness parameter. Setting `beta = 1/sqrt(d_k)` imports the Transformer scaling convention; it is not a universal definition of Hopfield inverse temperature.

### Falsifying example

Take a query `q = [1, 0]`, keys `K = I`, and `beta = 1`. The shared weights are:

```text
softmax([1, 0]) = [0.731059, 0.268941]
```

With tied values `V = K = I`, both the displayed Hopfield update and attention return:

```text
[0.731059, 0.268941]
```

With the equally valid attention value matrix

```text
V = [[0, 1],
     [1, 0]]
```

attention instead returns `[0.268941, 0.731059]`, while the displayed Hopfield update remains `[0.731059, 0.268941]`. Thus the literal statement "one attention update is mathematically identical" is false without the source paper's tying/projection conditions.

### C03 operational verdict

| Required surface | Observation |
|---|---|
| Operational variable | Output vector from one update for fixed `q`, `K`, `V`, and `beta` |
| Baseline/ablation | Tied `V=K` versus swapped independent `V` |
| Result | Equality holds in the tied construction and fails for general attention |
| Counterexample | The swapped-`V` calculation above |
| Independent repeat | Not present in the experiment bundle; arithmetic is fully specified for repetition |
| Cross-session software mapping | Not present in [H1]; no reinitialization or context-recovery experiment is supplied |

**C03 decision:** narrow layer equivalence passes; the unconditional wording and proposed memory-mechanism interpretation fail. Classification: `transformed`.

## MOSM-C08 test: source-to-software transfer

The test was a field-level provenance join across all 15 Physarum, crow, and laser leaves. A transfer passes only if a primary source supplies (1) the exact value, (2) the same scientific meaning, and (3) an operational transform into the named software field.

| Domain | Leaves | Supported | Transformed | Unsupported | Not found | Source-preserving software mappings |
|---|---:|---:|---:|---:|---:|---:|
| Physarum | 5 | 0 | 2 | 1 | 2 | 0 |
| Crow | 5 | 0 | 1 | 0 | 4 | 0 |
| PML laser | 5 | 1 | 3 | 1 | 0 | 0 |
| **Total** | **15** | **1** | **6** | **2** | **6** | **0** |

Three counterexamples establish why source truth is insufficient:

1. Cornell et al. [C1] summarize spread **at least 1.2 km** over the five-year study period, while the detailed spatial mapping was performed at 2.7 years and included a point at `1248 m`. A maximum observed extent is not a percolation threshold, so `spatial_percolation_threshold_meters = 1200` is transformed.
2. Kscheschinski et al. [P1] report calcium and tube radius as nearly anti-correlated, with measured/model phase deviations and uncertainty. This does not justify fixing `anti_correlation_phase_shift_rad = 3.14159`, and the paper measures tube radius rather than the manuscript's "membrane tension" quantity.
3. Gat et al. [L1] explicitly formulate a coarse-grained, dimensionless laser model. Its `g=4` spinodal and `g*=4.91` equilibrium transition do not become universal swarm thresholds merely because they are real results in that model.

**C08 decision:** fail. No primary source defines the proposed field transfer, dimensional transform, calibration dataset, or software validation. These constants must remain hypotheses or fixture values, not provenance-backed theory parameters.

### Executable perturbation test

A static consumer search over `tools/`, `prototype/`, `conditions/`, `fixtures/`, `chains/`, and the experiment control documents found **zero references** to any of the 15 C08 field names. Therefore changing each numeric leaf by `-10%` or `+10%` cannot change any current prototype output: the fields are dead configuration, not calibrated controls. This zero sensitivity is a failure of operationalization, not evidence of robustness. The exact command and field list are preserved in `raw/T3_source_manifest.json`.

## Sections 1.2-1.5 audit

| Location and exact claim | Primary source | Exact value/equation present? | Software mapping present? | Class | Finding |
|---|---|---|---|---|---|
| 1.2: `v_new = X softmax(beta X^T v_old)` | [H1] | Yes, with `xi` notation | Attention-layer mapping only; no M-OSM continuity mapping | `supported` | This is the modern Hopfield update. Broad identity with arbitrary attention requires additional key/value/projection conditions. |
| 1.2: `beta = 1/sqrt(d_k)` | [H1] | Present as Transformer scaling in the attention correspondence, not as the general definition of `beta` | No M-OSM mapping | `transformed` | A model-specific attention scaling is relabeled as inverse temperature. |
| 1.2: high `beta` causes a first-order transition | [H1] | No | No | `unsupported` | [H1] proves fixed-point types and separation conditions; it does not establish this universal first-order transition claim. |
| 1.3: PML mode locking is first-order | [L1], [L4] | Yes, for the stated statistical-mechanics model and fiber-laser experiment | No M-OSM mapping | `supported` | The result is model- and apparatus-scoped, not a generic attention law. |
| 1.3: `xi_p = 0.5(gamma + sqrt(gamma(gamma-4)))` | [L3] | Yes as the stationary **scaled pulse-power** root | No | `transformed` | The draft calls `xi_p` an amplitude. [L3] defines `gamma = gamma_s P_0^2/T` and `xi` as pulse power divided by a power scale; `gamma=4` is the spinodal and `gamma_e approximately 4.91` is the stability exchange. |
| 1.4: fast cycle `10^2 s` | [P1] | Yes to stated precision: dominant contraction frequency is about `10 mHz`, i.e. about `100 s` | No | `supported` | Approximate biological period is source-backed. |
| 1.4: calcium phase shift `approximately pi` relative to membrane tension | [P1] | No | No | `unsupported` | The primary measurement is calcium versus tube radius and reports near anti-correlation plus nonzero phase deviations, not an exact universal `pi` against membrane tension. |
| 1.4: slow cycle `10^3 s` with advected ATP | [P2], [P3] | `10-20 min` and about `15 min` dynamics are present; a periodic `10^3 s` ATP cycle is not | No | `transformed` | Advected softening signal is supported; ATP is proposed as a candidate, not established as the regulator. |
| 1.5: one capture episode | [C1] | Not as the compressed account states it | No | `transformed` | The study trapped `7-15` birds at each of five sites and used subsequent masked exposures; the manuscript collapses this design into one causal event. |
| 1.5: spread over `5 years` | [C1] | Yes | No | `supported` | Same follow-up interval. |
| 1.5: spread to `1.2 km` | [C1] | Yes, stated as at least that distance from one site | No | `supported` | Supported as an observed extent, not a threshold or general radius. |
| 1.5: horizontal and vertical social learning | [C1] | Yes, as the paper's interpretation of spread among adults and offspring | No | `supported` | Qualitative interpretation is source-backed; no oscillatory-processor equation follows. |

## C08 exact constants and causal claims

### Physarum

| Draft item | Unit | Exact primary support | Experimental/model context | Transfer to LLM swarm variable | Class |
|---|---|---|---|---|---|
| `fast_calcium_oscillation_period_ms = 100000` | ms (`100 s`, `10 mHz`) | [P1] reports a dominant frequency typically around `10 mHz`; [P2] groups datasets at `4, 6, 8, 10 mHz` and uses a model contraction period of `120 s`. | [P1]: ratiometric calcium and radius imaging in four excised, contracting tubes, sampled every `3 s`. [P2]: four network datasets and a closed-tube transport model. | No. A biological contraction period is not a scheduler period without a defined event-to-cycle map and outcome. | `transformed` |
| `slow_advective_drift_period_ms = 1200000` | ms (`1200 s`, `20 min`) | [P2] reports decisions within `10-20 min`, establishment of a new diameter distribution in about `15 min`, and persistence through `45 min`; it does not report a `20 min` periodic drift. | Nutrient-stimulus experiments plus a one-time release/advection model. | No. The endpoint of a response range is not an oscillator or agent timeout. | `transformed` |
| `anti_correlation_phase_shift_rad = 3.14159` | rad | [P1] finds calcium and radius **nearly** anti-correlated and explicitly measures nonzero deviation; its convention defines zero as exact anti-phase. It does not measure a universal `pi` offset from membrane tension. | Four live-tube datasets; fluorescence mixing is treated as a measurement limitation, and the model retains quantitative mismatch. | No. The named source variables are calcium and tube radius/stress, not prompt phase or semantic agreement. | `unsupported` |
| `viscous_damping_coefficient_gamma = 0.08` | dimensionless as drafted | No exact primary support located. [P1] instead defines the rheological ratio `gamma = eta f / E` and explores values on the order of `10^-1` and `1`. | Kelvin-Voigt cortex model with estimated `eta = 200 Pa s`, `E = 2 or 20 Pa`, and simulated timescales. | No source-preserving transform or calibration. | `not found` |
| `attenuation_matrix_poisson_ratio = 0.42` | dimensionless | No relevant primary source located for either the named matrix or value in the memory mechanism. | [P1]-[P3] do not define an `attenuation_matrix`. | No matrix exists in the M-OSM implementation to receive this material parameter. | `not found` |
| Calcium inhibits actomyosin/cortex contraction. | causal, no unit | [P1] experimentally observes a nearly anti-correlated calcium-radius relation and reports that an inhibitor model captures the core relation, while retaining quantitative disagreement. | Live-tube imaging plus a mechanochemical model; the conclusion is qualified rather than a direct molecular intervention. | Analogy only until an LLM-side variable, intervention, and measurable response are defined. | `supported, qualified` |
| A nutrient releases a soluble softening agent; flow advection changes tube diameters and stores location. | causal, times in min; distance/velocity apparatus-specific | [P2] supports the advection/diameter hierarchy mechanism through imaging and modeling. [P3] independently supports an advected signaling mechanism for stimulus propagation. | [P2] used local nutrient stimuli, `2,165` tubes in the main network, and a one-time agent release model; all study data are in the article/SI. | Morphological-memory analogy only. It does not specify a text-state compressor, latent write, or agent memory API. | `supported in organism` |
| The softening regulator is ATP and locally lowers wall stiffness. | causal, no established coefficient | [P2] says the agent's identity is unknown and names ATP only as a candidate. [P4] reports ATP/ADP about twice as high at the migration front as the rear; it does not show that ATP is the [P2] agent or causes the memory-specific softening. | [P4] measured migrating plasmodia; [P2] did not measure ATP in its nutrient-memory experiment. | No. Candidate identity cannot parameterize an LLM compressor. | `unsupported as stated` |
| Fast oscillations continuously "read" and "update" the diameter memory. | causal metaphor | [P2] shows that contraction-driven flow transports the agent and that existing tube hierarchy shapes later transport. It does not formulate each oscillation as a discrete read/write cycle. | Living flow network over minutes, not token generations. | Analogy only. | `transformed` |

### American crow

| Draft item | Unit | Exact primary support | Experimental context | Transfer to LLM swarm variable | Class |
|---|---|---|---|---|---|
| `contagion_coefficient_beta = 0.68` | dimensionless as drafted | No such fitted coefficient in [C1]. | [C1] used behavioral proportions, linear/exponential trend comparisons, and mapped observations, not an epidemic/swarm contagion model. | No denominator, estimator, or update rule. | `not found` |
| `vertical_transmission_decay_factor = 0.15` | dimensionless as drafted | [C1] supports vertical social learning qualitatively but estimates no decay factor. | Young crows were tested after observing conditioned parents; sample sizes and responses are reported as birds/territories. | No mapping from generations or learning trials to agent-context decay. | `not found` |
| `horizontal_resonance_gain_db = 12.4` | dB | No decibel-valued behavioral gain or reference level in [C1]. | Acoustic level was not the outcome used to quantify social learning. | Dimensionally inapplicable without an amplitude/power ratio and reference. | `not found` |
| `spatial_percolation_threshold_meters = 1200.0` | m | [C1] reports spread at least `1.2 km`; the detailed expanded survey at `2.7 years` found scolding at `541`, `667`, and `1248 m`. | One long-term University of Washington site; spatial extent was not re-assessed at year five. | An observed maximum extent at one site is not a graph threshold or software radius. | `transformed` |
| `active_scolding_ratio = 0.887` | proportion | No exact ratio. The closest relevant [C1] values include `82%` of `126` scolding events attracting a mob, `86.9%` of `160` identified scolders lacking direct dangerous-mask capture, and `66%` scolding at `2.7 years`; each has a different denominator. | Field observations with masked walkers and incompletely marked birds. | No single source ratio maps to an agent activation probability. | `not found` |
| A single capture caused five-year, 1.2-km spread. | captures, years, km | [C1] trapped `7-15` birds at each of five sites, then repeatedly presented masks. The long-term site had `38` cumulative dangerous-mask exposures by the `2.7-year` spatial survey. | Five sites near Seattle; the paper distinguishes direct, horizontal, and vertical learning. | No single-shot broadcast coefficient can be inferred. | `transformed` |
| Horizontal and vertical social learning occurred. | categorical | [C1] supports these interpretations: later lone never-captured birds were consistent with horizontal learning, and independent scolding by young birds after parental conditioning demonstrated vertical learning. | Behavioral field experiments; direct learners discriminated faces more precisely than social learners. | Topological analogy only; no cadence, gain, or decay constant follows. | `supported in crows` |
| Threat information is not stored in individual brains but continuously circulates as an oscillatory processor. | causal metaphor | [C1] explicitly reports individual learning and later recognition as well as social learning. It does not test absence of individual memory, continuous circulation, or oscillation. | Recognition and scolding observations, not neural recordings or oscillator measurements. | Analogy only and partly contrary to the individual-learning result. | `unsupported` |

### Passively mode-locked laser

| Draft item | Unit | Exact primary support | Experimental/model context | Transfer to LLM swarm variable | Class |
|---|---|---|---|---|---|
| `mode_locking_phase_transition = First-Order` | categorical | [L1] rigorously solves a coarse-grained statistical-mechanics model with a first-order mode-locking transition; [L4] observes a discontinuity in a passively mode-locked fiber ring laser. | [L1] explicitly says its model is a theoretical laboratory, not a quantitative approximation of every laser. [L4] varied externally injected optical noise. | No. A scoped phase classification is not a scheduler policy. | `supported, scoped` |
| `critical_threshold_gamma_c = 4.0` | dimensionless | [L1] uses `g = gamma_s P^2/T`: at `g > 4` a second local minimum appears, but equilibrium remains disordered until `g* approximately 4.91`. [L3] gives the same spinodal in `gamma` notation. | Thermodynamic-limit/coarse-grained model with fixed or saturable power and Gaussian noise. | No mapping to swarm coherence, prompt noise, or coupling. | `transformed` |
| `stability_exchange_gamma_e = 4.91` | dimensionless, approximate | [L1] locates the model's stability exchange/first-order point at `g* approximately 4.91`; [L3] calls it `gamma_e approximately 4.91`. | Model ratio combines saturable-absorption strength, intracavity power squared, and noise power. It depends on model/filtering choices. | No calibration to an LLM variable or loss surface. | `transformed` |
| `phase_melting_power_floor_mw = 7.6` | mW | [L4] states that intracavity power was **about `7.6 mW`**, held fixed while the transition occurred at external optical-noise spectral density `0.25 mW/nm`. It is not a floor or threshold. | One polarization-locked erbium fiber ring laser; noise was the swept control variable. | No. Apparatus power cannot be copied into a software threshold. | `transformed` |
| `entropy_collapse_quartic_order_parameter = rf_spectral_purity` | categorical/undefined | [L4] defines a dimensionless quartic field order parameter and measures a proportional RF power with a fast photodiode/RF power meter. It does not define `rf_spectral_purity`. | RF power is an instrument proxy; the paper notes the order parameter is also inversely proportional to pulse width. | No LLM observable or estimator is supplied. | `unsupported` |
| CW phases fluctuate because of spontaneous-emission noise; mode locking synchronizes modes. | causal | [L1] models spontaneous-emission noise as complex Gaussian white noise and describes random phases for zero order parameter; mode-locked operation phase-locks many axial modes. | Laser field modes in a noisy cavity with saturable absorption. "Chaotic" is stronger than the source's random/disordered description. | Physics fact plus analogy; no evidence of LLM attention dynamics. | `supported, scoped` |
| Exceeding a critical pump causes the first-order transition. | causal | [L1] varies the combined dimensionless ratio `gamma_s P^2/T`. [L4] directly varies noise at fixed `7.6 mW`, while noting light power can be varied equivalently in the theory. | Threshold depends on absorber, power, noise, and filtering, not pump alone. | No portable single control variable. | `transformed` |
| `xi_p = 0.5(gamma + sqrt(gamma(gamma-4)))` is the pulse amplitude. | dimensionless scaled pulse power | [L3] gives the expression exactly for the pulsed-state stationary point, where `xi` is pulse power divided by a power scale. | Finite-mode self-start model; `gamma = gamma_s P_0^2/T`. | No LLM state amplitude or inverse-temperature calibration. | `transformed` |
| All modes crystallize into an ultrashort pulse that removes all background noise. | causal/exaggeration | [L1] supports phase locking and pulse formation; [L4] observes pulsed versus fluctuating-CW states. Neither says all modes participate or that all background noise is removed. | Real laser retains noise and can form multiple pulses. | Analogy only. | `unsupported as absolute` |

## `theoretical_parameters_db` audit

All 26 leaves are included, including categorical leaves, so no numeric claim can inherit credibility from an unaudited neighboring label.

| Field | Draft value | Primary source | Exact value/equation present? | Software mapping present? | Class | Finding |
|---|---:|---|---|---|---|---|
| `kuramoto_core.coupling_strength_K` | `3.45` | [K1] | No | No | `not found` | [K1] defines coupling but does not supply this calibrated value. |
| `kuramoto_core.intrinsic_noise_floor_D` | `0.12` | [K1] | No | No | `not found` | No source-backed noise calibration found. |
| `kuramoto_core.frequency_dispersion_gamma` | `0.25` | [K1] | No | No | `not found` | No source-backed Lorentzian width calibration found. |
| `kuramoto_core.critical_synchronization_threshold_Kc` | `2*(gamma+D)` | [K1] | Yes, under all-to-all thermodynamic-limit, Lorentzian-frequency, additive-white-noise assumptions | No | `supported` | Formula is scoped to that model; it is not parameter-free empirical calibration. |
| `kuramoto_core.order_parameter_resolution` | `r=sqrt(K-Kc)` | [K1] | No; stationary result is `r=sqrt(1-Kc/K)` for the standard normalization, with only proportional square-root scaling near threshold | No | `unsupported` | With the draft constants, the draft equation gives `r=1.646208`, impossible for normalized `0<=r<=1`; the source form gives `0.886288`. |
| `kuramoto_core.phase_shift_coherence_window_radians` | `0.174` | [K1] | No | No | `not found` | Exact searches found no primary basis for this approximately 10-degree window. |
| `physarum_hydrodynamics.fast_calcium_oscillation_period_ms` | `100000` | [P1] | About `100 s` is present after converting `10 mHz` | No | `transformed` | Approximate measured period becomes an exact millisecond constant. |
| `physarum_hydrodynamics.slow_advective_drift_period_ms` | `1200000` | [P2], [P3] | `20 min` is an endpoint of reported `10-20 min` dynamics, not a drift period | No | `transformed` | Biological response timescale is converted into a fixed periodic software parameter. |
| `physarum_hydrodynamics.anti_correlation_phase_shift_rad` | `3.14159` | [P1] | No exact constant with the named quantity | No | `unsupported` | Near anti-correlation does not establish exact `pi`; measured and modeled phase deviations are discussed explicitly. |
| `physarum_hydrodynamics.viscous_damping_coefficient_gamma` | `0.08` | [P1] | No | No | `not found` | [P1] uses a dimensionless rheological ratio on the order of `10^-1` or `1`, not this exact coefficient. |
| `physarum_hydrodynamics.attenuation_matrix_poisson_ratio` | `0.42` | [P1]-[P3] | No | No | `not found` | No relevant primary source was found defining this matrix or value. |
| `social_contagion_crow.contagion_coefficient_beta` | `0.68` | [C1] | No | No | `not found` | The experiment reports proportions and spatial/temporal observations, not this contagion coefficient. |
| `social_contagion_crow.vertical_transmission_decay_factor` | `0.15` | [C1] | No | No | `not found` | Vertical learning is discussed, but no such decay parameter is estimated. |
| `social_contagion_crow.horizontal_resonance_gain_db` | `12.4` | [C1] | No | No | `not found` | No decibel-valued behavioral gain exists in the source. |
| `social_contagion_crow.spatial_percolation_threshold_meters` | `1200.0` | [C1] | `1.2 km` observed spread is present; a threshold is not | No | `transformed` | Observation at one site is relabeled as a universal percolation threshold. |
| `social_contagion_crow.active_scolding_ratio` | `0.887` | [C1] | No | No | `not found` | No exact matching ratio was located. |
| `pml_laser_thermodynamics.mode_locking_phase_transition` | `First-Order` | [L1], [L4] | Yes, for the scoped PML model and experiment | No | `supported` | Valid scoped classification, not a portable software parameter. |
| `pml_laser_thermodynamics.critical_threshold_gamma_c` | `4.0` | [L1], [L3] | Yes as the dimensionless point where a nonzero local minimum first appears | No | `transformed` | It is a model spinodal, not the equilibrium transition or a universal threshold. |
| `pml_laser_thermodynamics.stability_exchange_gamma_e` | `4.91` | [L1], [L3] | Yes, approximately, as the equilibrium stability exchange | No | `transformed` | Source value belongs to a dimensionless model ratio and has no swarm calibration. |
| `pml_laser_thermodynamics.phase_melting_power_floor_mw` | `7.6` | [L4] | Exact number present, wrong role: fixed intracavity power, not a floor | No | `transformed` | The swept transition variable was optical-noise spectral density; the reported transition was at `0.25 mW/nm`. |
| `pml_laser_thermodynamics.entropy_collapse_quartic_order_parameter` | `rf_spectral_purity` | [L4] | No | No | `unsupported` | [L4] uses a quartic field order parameter proportional to measured RF power. It does not define `rf_spectral_purity`. |
| `ai_information_geometry.latent_manifold_deviation_from_euclidean` | `0.972` | [H1], [A1] | No | No | `not found` | No model, dataset, estimator, or primary measurement matching this value was found. |
| `ai_information_geometry.metric_tensor_type` | `Fisher-Rao / Bregman Dually Flat Geometry` | [H1], [A1] | No scoped construction with this combined label | No | `not found` | The field combines information-geometric terms without a defined manifold or estimator. |
| `ai_information_geometry.modern_hopfield_energy_equation` | `-(1/beta)ln sum exp(beta x_i^T xi) + 0.5 xi^T xi` | [H1] | Core state-dependent terms yes; source also includes additive constants | Attention/Hopfield-layer mapping only; no M-OSM mapping | `transformed` | Same gradient dynamics, but not the complete source equation and not evidence of cross-session memory. |
| `ai_information_geometry.attention_sink_olmo_dense_transition_onset_step` | `126000` | [A1] | Yes, as an OLMo checkpoint for a sharp whole-model BOS-attractor jump / layer-specific observation | No | `transformed` | [A1] samples checkpoints; first sinks occur earlier. The value is not a universal transition constant. |
| `ai_information_geometry.attention_sink_olmoe_moe_transition_onset_step` | `600000` | [A1] | Yes, for a later layer-specific OLMoE acquisition | No | `transformed` | [A1] describes OLMoE's whole-model emergence as gradual, so calling this the model transition onset changes the result. |

## Primary-source register

Only primary papers and official proceedings are used as technical authority.

- **[H1]** Ramsauer et al., "Hopfield Networks is All You Need," ICLR 2021. [Official OpenReview record](https://openreview.net/forum?id=tL89RnzIiCd), [official proceedings PDF](https://openreview.net/pdf?id=tL89RnzIiCd), [arXiv DOI](https://doi.org/10.48550/arXiv.2008.02217).
- **[K1]** H. Sakaguchi, "Cooperative Phenomena in Coupled Oscillator Systems under External Fields," *Progress of Theoretical Physics* 79 (1988), 39-46. [DOI: 10.1143/PTP.79.39](https://doi.org/10.1143/PTP.79.39), [publisher record](https://academic.oup.com/ptp/article/79/1/39/1855689).
- **[P1]** B. Kscheschinski, M. Kramar, K. Alim, "Calcium regulates cortex contraction in Physarum polycephalum," *Physical Biology* 21 (2024). [DOI: 10.1088/1478-3975/ad0a9a](https://doi.org/10.1088/1478-3975/ad0a9a), [primary accepted manuscript](https://pure.mpg.de/rest/items/item_3556005_4/component/file_3556872/content).
- **[P2]** M. Kramar, K. Alim, "Encoding memory in tube diameter hierarchy of living flow network," *PNAS* 118 (2021). [DOI: 10.1073/pnas.2007815118](https://doi.org/10.1073/pnas.2007815118), [author-hosted primary paper](https://www.bpm.ph.tum.de/wp-content/uploads/2023/07/2021-PNAS-Memory-Hierarchy-Alim-Kramar.pdf).
- **[P3]** K. Alim et al., "Mechanism of signal propagation in Physarum polycephalum," *PNAS* 114 (2017). [DOI: 10.1073/pnas.1618114114](https://doi.org/10.1073/pnas.1618114114), [primary repository record](https://pure.mpg.de/view/item_2450775).
- **[P4]** T. Ueda, K. Matsumoto, T. Akitaya, Y. Kobatake, "Spatial and temporal organization of intracellular adenine nucleotides and cyclic nucleotides in relation to rhythmic motility in Physarum plasmodium," *Experimental Cell Research* 162 (1986), 486-494. [DOI: 10.1016/0014-4827(86)90352-6](https://doi.org/10.1016/0014-4827(86)90352-6), [PubMed primary-paper record](https://pubmed.ncbi.nlm.nih.gov/3943553/).
- **[C1]** H. N. Cornell, J. M. Marzluff, S. Pecoraro, "Social learning spreads knowledge about dangerous humans among American crows," *Proceedings of the Royal Society B* 279 (2012). [DOI: 10.1098/rspb.2011.0957](https://doi.org/10.1098/rspb.2011.0957), [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3234554/).
- **[L1]** O. Gat, A. Gordon, B. Fischer, "Solution of a statistical mechanics model for pulse formation in lasers," *Physical Review E* 70, 046108 (2004). [DOI: 10.1103/PhysRevE.70.046108](https://doi.org/10.1103/PhysRevE.70.046108), [author-hosted primary paper](https://fischer.net.technion.ac.il/files/2018/06/63.pdf).
- **[L2]** B. Vodonos et al., "Formation and Annihilation of Laser Light Pulse Quanta in a Thermodynamic-like Pathway," *Physical Review Letters* 93, 153901 (2004). [DOI: 10.1103/PhysRevLett.93.153901](https://doi.org/10.1103/PhysRevLett.93.153901), [author-hosted primary paper](https://fischer.net.technion.ac.il/files/2018/06/2004-PRL-93_153901-Formation-and-Annihilation-of-Laser-Pulse-Quanta-in-a-Thermodynamic-like-Pathway.pdf).
- **[L3]** A. Gordon, O. Gat, B. Fischer, F. X. Kartner, "Self-starting of passive mode locking," *Optics Express* 14 (2006), 11142-11154. [DOI: 10.1364/OE.14.011142](https://doi.org/10.1364/OE.14.011142), [author-hosted primary paper](https://fischer.net.technion.ac.il/files/2018/06/80.pdf).
- **[L4]** A. Gordon, B. Vodonos, V. Smulakovski, B. Fischer, "Melting and freezing of light pulses and modes in mode-locked lasers," *Optics Express* 11 (2003), 3418-3424. [DOI: 10.1364/OE.11.003418](https://doi.org/10.1364/OE.11.003418), [author-hosted primary paper](https://fischer.net.technion.ac.il/files/2018/06/57.pdf).
- **[A1]** Y. Xu, "When Do Attention Circuits Form? Developmental Trajectories of Capability and Attention-Sink Emergence Across Three 1B-Class Architectures," primary preprint (2026). [arXiv DOI: 10.48550/arXiv.2606.02378](https://doi.org/10.48550/arXiv.2606.02378), [arXiv full text](https://arxiv.org/html/2606.02378v2).

## Reproducible query log

Run date: 2026-07-18. Discovery surfaces were exact-phrase web search, DOI resolution, OpenReview, arXiv, publisher search, PubMed/PMC, institutional repositories, and full-text term search. Evidence selection was restricted to publisher pages, DOI records, arXiv/OpenReview proceedings, institutional primary manuscripts, and primary full texts. Secondary pages that appeared in discovery results were not used as technical evidence.

| Query or retrieval action | Primary-source outcome |
|---|---|
| `"Hopfield Networks is All You Need" OpenReview` | Located [H1] official ICLR record and PDF. |
| `"X softmax(beta X^T xi)" Hopfield` and full-text find for `first-order` | Located exact update/energy in [H1]; no first-order transition statement found. |
| `"Cooperative Phenomena in Coupled Oscillator Systems under External Fields" noise Lorentzian` | Located [K1], DOI, and model assumptions. |
| `"0.174" radians Kuramoto coherence window` | No relevant primary hit. |
| `"Calcium regulates cortex contraction in Physarum polycephalum"` | Located [P1] and accepted manuscript. |
| `Physarum "1200 s" advection period` | No exact period source; [P2]-[P3] instead give response/advection timescales. |
| `Physarum "gamma = 0.08" damping` | No relevant primary hit. |
| `Physarum "Poisson ratio" 0.42` | No relevant primary hit for the named quantity. |
| `"Encoding memory in tube diameter hierarchy of living flow network"` | Located [P2], including about 15 min imprint and 10-20 min decision times. |
| `Physarum ATP twice front rear` | Located [P4]; supports an ATP spatial gradient, not ATP identity as the [P2] wall-softening agent. |
| `"Social learning spreads knowledge about dangerous humans among American crows"` | Located [C1] and full text. |
| `"0.68" "dangerous mask" crows`; `"0.887" crow scolding Marzluff` | No matching primary parameter/ratio. |
| `"12.4 dB" crow mobbing` | No relevant primary hit. |
| `"Solution of a statistical mechanics model for pulse formation in lasers"` | Located [L1], exact dimensionless thresholds, and stationary solution. |
| `"4.91" mode locking laser phase transition` | Located `g*=4.91` in [L1]. |
| `"Self-starting of passive mode locking"` and full-text formula search | Located [L3], including exact `xi_p`, `gamma_c=4`, and `gamma_e approximately 4.91` in the source's scaled pulse-power model. |
| `"7.6 mW" mode-locked laser phase transition` | Located [L4]: about `7.6 mW` was fixed intracavity power; the swept transition was at `0.25 mW/nm` external-noise spectral density. |
| `"Formation and Annihilation of Laser Light Pulse Quanta"` | Located [L2], RF-power order parameter, DOI, and experiment. |
| `"latent manifold" "0.972" Fisher-Rao Bregman` | No relevant primary measurement. |
| `"attention sink" "126000" OLMo`; `"attention sink" "600000" OLMoE` | Located both checkpoint values in [A1]; surrounding results contradict universal onset semantics. |
| DOI resolution for every register entry | DOI/publisher metadata matched title, venue, and authorship. |
| Local arithmetic: `Kc=2*(0.25+0.12)`; both candidate `r` equations | `Kc=0.740000`; draft `r=1.646208`; source-normalized `r=0.886288`. |
| Local arithmetic: two-token softmax and tied/swapped value matrices | Weights `0.731059/0.268941`; equality only in tied construction. |
| Exact C08 field-name search in runnable experiment paths | Zero consumers found; current numeric perturbation sensitivity is structurally zero. |

For exact-value searches marked `not found`, the result means no relevant primary hit was found in this bounded pass, not proof that no paper anywhere contains the numeral.

## Promotion decision

Neither claim meets the `CLAIMS.md` promotion rule.

- `MOSM-C03` has an operational variable, baseline, result, and counterexample here, but lacks an independent repeat and any experiment linking the layer identity to cross-session M-OSM memory.
- `MOSM-C08` fails source preservation and has no operational transform or calibration experiment. It should be decomposed into domain-specific hypotheses before testing.

Recommended status in the claims ledger: retain both as `hypothesis`; attach this audit as the provenance objection. The existing scientific sources can motivate experiments, but they do not authorize the current software parameter values.
