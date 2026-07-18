# Evidence-Backed Handoff Protocol v0.2

This protocol is the practical residue of the M-OSM tests. It is deliberately
smaller than the theory that produced it.

## Writer contract

A handoff Tube contains:

- distinct `tube_id` and `subject_id`;
- producer, objective, current question, creation time, and optional expiry;
- confirmed facts, explicit corrections, constraints, unresolved questions,
  and at most three next actions;
- a source reference on every evidence item;
- bounded source paths and SHA-256 digests;
- optional semantic anchors;
- optional `claimed_coherence`, always treated as untrusted metadata.

The writer must not encode omitted facts into decorative phase numbers or claim
that a digest is recoverable memory. Missing information remains missing.

## Reader algorithm

1. Validate the Tube shape and version.
2. Resolve each required source only inside explicit allowed roots.
3. Read each bounded source once, hash those exact bytes, and retain those bytes
   for rendering. Never reopen the path after verification.
4. Hold if a required source is missing, outside the boundary, oversized,
   non-UTF-8, or hash-mismatched.
5. Present `tube_id`, `subject_id`, and producer as distinct typed roles.
6. Apply explicit corrections over superseded statements.
7. Preserve constraints, uncertainty, and forbidden actions before continuing.
8. Do not fill omitted fields from plausibility or claimed coherence.

`prototype/mosm_tube.py` implements this reader for `mosm-tube/0.1` and
`mosm-tube/0.2`. v0.2 requires `subject_id`. Relative source paths are resolved
against the supplied `--allow-root`, making a Tube portable inside a checked-out
experiment tree.

## Observable coherence

Do not use a producer-supplied `r` as truth. If a runtime needs a continuity
score, derive it after the handoff from observable components such as:

- exact or typed fact recall;
- correction precedence;
- safety and forbidden-action preservation;
- uncertainty preservation;
- next-action fidelity;
- unsupported inference rate;
- source freshness and verification state.

Keep the component vector. A single scalar may be displayed for comparison but
must not erase which component failed.

## Promotion boundary

The protocol is ready for synthetic and shadow use. It is not ready to replace
a live lifeline, mutate shared memory, or autonomously execute next actions.
Promotion requires a multi-case, equal-budget, independently repeated study
with observed read logs and a rollback path.
