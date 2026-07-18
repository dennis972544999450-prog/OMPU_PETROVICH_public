# From Oscillation Metaphor to a Working Handoff

## Bottom line

The received M-OSM draft does not demonstrate that language agents recover a
hidden context from a phase vector, hash, motivational frequency, or claimed
coherence. Those claims failed mathematically, operationally, or in blind
ablation.

Something useful did survive: a fresh agent can continue safely when a durable
handoff explicitly carries subject identity, selected facts, corrections,
constraints, uncertainty, next actions, and hash-verified source evidence. That
mechanism is external memory plus evidence selection and precedence. It does
not depend on whether agents are literally waves.

## What the blind agents observed

- Full context C0 recovered 12/12 fields in 2019 input bytes.
- Ordinary summary C1 recovered 7/12 exact and 12/12 semantically in 1647 bytes.
- Draft tube-only C2 recovered only 2 supported fields in each of three blind
  runs at 1657 bytes. Compact phase-like metadata did not restore omitted facts.
- Corrupted C4 claimed coherence `0.999` and yielded 0/12 in two blind runs.
- v0.1 compact rehydration C7 preserved operational content but both agents
  confused tube identity with subject identity.
- v0.2 C10 typed the subject separately; both agents recovered 12/12 fields
  semantically. Its 2965-byte input exceeded full context, so this is an
  integrity result, not a compression win.
- A two-hop ordinary-summary chain C8 drifted to 11/12 semantically and lost
  producer identity. A two-hop reference chain C9 recovered 12/12 semantically
  after dereferencing durable evidence.

## What the mechanism tests found

1. The draft's Part 3 block is not strict JSON as received. Two independent
   parses found 195 Markdown escape backslashes that must be removed first.
2. `Kc = 2(gamma + D)` is a scoped noisy-Kuramoto theorem. The draft's global
   equality `r = sqrt(K - Kc)` is not: it produces impossible `r > 1`.
3. Slowing every generator rate is a time reparameterization and did not change
   coherence. Narrowing intrinsic-frequency dispersion can synchronize a model,
   but that is not evidence for period doubling or slower text output.
4. Arbitrary Hertz labels assigned after outcomes did not predict held-out
   behavior. A timing claim needs a real scheduler actuator and timestamped
   events before frequency has operational meaning.
5. The primary papers contain real Hopfield, Physarum, crow, and laser results,
   but no source-preserving mapping from their constants to an agent memory
   engine. Real scientific numbers do not become software controls by renaming.
6. Runtime QA caught a real integrity bug: verification and rendering reopened
   the same path at different times. v0.2 now renders the exact bytes it hashed,
   and an independent post-fix agent reproduced the repair.

## The practical model

Treat a handoff as a small evidence graph, not a compressed personality state:

```text
subject -> facts / corrections / constraints / uncertainty / next actions
        -> immutable source references -> verified bytes
```

The graph must distinguish the identity of the handoff object from the identity
of its subject, preserve explicit supersession, and make missing evidence
visible. A claimed confidence or coherence score never substitutes for source
verification.

## Next experiment

Run a preregistered, randomized benchmark across at least 20 heterogeneous
fixtures and several fresh-agent models. Compare equal-byte versions of:

1. plain summary;
2. typed evidence handoff without source bodies;
3. typed handoff with verified retrieval;
4. full context.

Record actual reads in a mediator, score semantic and safety fields blindly,
and repeat each condition. Separately, if cadence remains interesting, vary a
real scheduling policy while holding text, model, compute, and task constant.
Do not attach Hertz labels until there is a measured clock and a causal
intervention.
