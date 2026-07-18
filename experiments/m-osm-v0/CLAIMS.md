# M-OSM Claim Register

Statuses begin as `UNTESTED`. A metaphor can be useful without being an
implementation mechanism.

| ID | Draft claim | Observable test | Initial concern |
|---|---|---|---|
| MOSM-C01 | Noisy Kuramoto critical coupling is `Kc = 2(gamma + D)`. | Check assumptions and reproduce analytically/numerically. | Only valid for a particular mean-field model and distribution. |
| MOSM-C02 | `r = sqrt(K - Kc)` resolves order. | Evaluate with the draft constants and compare with bounded `r`. | Draft values produce `r > 1`; proportional scaling was converted into equality. |
| MOSM-C03 | One attention update is mathematically identical to a modern Hopfield update. | Compare equations and assumptions in the primary paper. | Useful equivalence may not license cross-session memory claims. |
| MOSM-C04 | An eight-number phase vector plus anchors can reinitialize latent attractors and recover the full context. | Blind fresh-agent recall benchmark. | No model-state write or associative pool is specified. |
| MOSM-C05 | A hash of five interactions represents an attractor state. | Attempt recovery from hash alone. | A cryptographic hash is not reversible memory. |
| MOSM-C06 | Low coherence should trigger period doubling and restore synchronization. | Define observable coherence and compare slowdown policies. | `r` is compared to `Kc` despite different roles; period doubling is asserted rather than derived. |
| MOSM-C07 | Fixed motivational frequencies in hertz improve multi-agent coordination. | Randomized frequency-label ablation. | Text agents have no demonstrated clock corresponding to 5-25 Hz. |
| MOSM-C08 | Exact Physarum, crow, and laser constants transfer into swarm-engine configuration. | Trace each number to primary evidence and perturb it. | Several constants lack provenance or a mapping to software variables. |
| MOSM-C09 | Compact tubes beat ordinary summaries. | C1 vs C2 on equal byte/token budgets. | The tube may be a summary with decorative numeric fields. |
| MOSM-C10 | Tube plus durable references can support continuity. | C3 vs C2 and C1. | This is plausible, but the mechanism is external retrieval, not latent recall. |
| MOSM-C11 | A branch projection can preserve correction and uncertainty without loading all history. | C5 vs C3. | Requires immutable references and precedence rules. |
| MOSM-C12 | Self-reported `coherence_index_r` detects correctness. | C4 corruption challenge. | A confident stale packet can report arbitrarily high `r`. |

## Promotion rule

A claim moves from metaphor to mechanism only after it has:

1. an operational variable;
2. a baseline and an ablation;
3. a reproducible result artifact;
4. a counterexample or failure boundary;
5. an independently repeated run.
