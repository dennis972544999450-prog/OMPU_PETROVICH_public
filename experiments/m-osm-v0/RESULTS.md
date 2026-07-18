# M-OSM Falsification Bench v0 Results

Date: 2026-07-18

## Decision

The received M-OSM draft is not supported as a latent cross-session memory
mechanism. The bounded experiment does support a smaller engineering result:
a typed handoff delta plus hash-verified source references can preserve task
state for a fresh agent. That mechanism is external retrieval and explicit
precedence, not recovery from phase coordinates, motivational hertz, or a
cryptographic hash.

No claim here establishes that thoughts are waves. The tested outcome is how
information blocks mutate or survive under summary, opaque compression,
typed projection, corruption, and verified dereferencing.

## Blind recall

Sixteen fresh-agent runs were scored against 12 frozen fields. The full table
is in `SCOREBOARD.md`; the machine-readable rows are in
`raw/scoreboard.json`.

| Comparison | Exact result | What it shows |
|---|---:|---|
| Full context C0 | 12/12 at 2,019 bytes | Upper-bound fixture baseline |
| Prose summary C1 | 7/12 strict, 12/12 semantic at 1,647 bytes | Meaning mostly survived, exact identifiers did not |
| Draft Tube C2, three runs | 2/12, 2/12, 3/12 at 1,657 bytes | Omitted values were not recoverable from phase numbers or hash |
| Corrupted high-`r` C4, two runs | 0/12 and 0/12 at 1,613 bytes | Claimed coherence did not detect correctness |
| Branch projection C5 | 12/12 at 3,365 bytes | Verified pointers preserved state, but cost more than full context |
| Compact v0.1 C7, two runs | 11/12 and 10/12 at 2,935 bytes | Both agents confused container identity with subject identity |
| Typed compact v0.2 C10, two runs | 12/12 and 11/12 strict at 2,965 bytes | Both are 12/12 semantically; explicit `subject_id` fixed the identity error |

C10 costs 46.9% more bytes than C0 on this small fixture. It is therefore a
continuity prototype, not evidence of compression. Its expected advantage is
selective loading when the referenced source is much larger than the active
delta; that remains to be tested on a multi-case corpus.

Exact scoring is intentionally brittle. R1 audited C0-C9 and found 13 strict
false negatives caused only by wording, raising those ten runs from 83/120
strict to 96/120 semantic credit. The strict scoreboard remains canonical so
that semantic judgment cannot silently rescue wrong identifiers or permissions.

## Claim verdicts

| Claim | Verdict | Evidence |
|---|---|---|
| C01 Kuramoto `Kc` | Scoped support | `Kc=2(gamma+D)=0.74` holds for the stated ideal Lorentzian mean-field model |
| C02 `r=sqrt(K-Kc)` | Falsified as equality | Draft gives impossible `r=1.646`; simulation gives about `0.903` |
| C03 Hopfield equals attention | Transformed | Equality needs the source paper's key/value/projection mapping; it gives no cross-session memory |
| C04 phase Tube restores context | Falsified in fixture | Three C2 runs recovered only 2-3 of 12 fields |
| C05 interaction hash stores context | Falsified operationally | Fresh process cannot invert or reconstruct omitted values from the digest |
| C06 slowdown restores coherence | Not supported | Pure generator slowdown left `r` exactly unchanged; frequency narrowing changed the model instead |
| C07 motivational hertz | Label mechanism falsified | Post-hoc labels failed held-out prediction; a real timing actuator was not available |
| C08 domain constants transfer | Failed | Of 15 Physarum/crow/laser leaves: 1 supported, 6 transformed, 2 unsupported, 6 not found; none had a software mapping |
| C09 Tube beats summary | Falsified | Near-equal-byte C2 scored 2-3/12 versus C1 at 7/12 strict |
| C10 references support continuity | Supported as retrieval | C3, C5, C9, and C10 recovered source-backed state |
| C11 branch projection preserves state | Supported in one fixture | C5 recovered 12/12, without demonstrating lower cost or generality |
| C12 self-reported `r` detects correctness | Falsified | Both high-`r` corrupted runs scored 0/12 |

## What changed because of testing

1. R1 found false positives in the scorer: Python numeric equality accepted
   wrong scalar types, set conversion erased duplicate list items, and empty
   required arrays were not counted as omissions. Type-strict and multiset
   tests now cover those failures.
2. C7 exposed an identity attention sink. v0.2 separates `tube_id` from required
   `subject_id`; two C10 agents then recovered the subject correctly.
3. Two runtime probes found a verify/use race: the prototype hashed a file and
   reopened it later. The verifier now preserves the exact bounded bytes that
   were hashed, and T5 independently reproduced the fix.
4. A final all-in-one replication agent exceeded its bounded interaction
   window and was stopped without a normal final status. Its Markdown and JSON
   audit artifacts appeared late, were validated, and are retained as a frozen
   snapshot with explicit limitations. `SCARS.md` records the orchestration
   failure separately from the result.

## Limits and next test

- One synthetic case is not a memory benchmark.
- Most conditions have one run; only C2, C4, C7, and C10 have direct repeats.
- Input bytes partly rely on participant-declared reads.
- The prototype never writes model weights, KV cache, or hidden state.
- Primary-source search was bounded; `not found` is not proof of global absence.
- No 5-25 Hz agent scheduler was available, so physical-frequency effects remain untested.

The next promotion test is a preregistered corpus of at least 30 randomized
cases, three blind agents per condition, equal byte budgets, mediated read logs,
and correction/safety preservation as primary outcomes. Until then, use v0.2
as a reversible handoff fixture, not as a live autonomous memory controller.
