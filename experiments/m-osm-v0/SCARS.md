# Experiment Scars

These are result-bearing failures, not hidden cleanup notes.

## S1 - Partial parallel spawn caused a duplicate T2 write-set

The first eight-agent `Promise.all` returned only `agent thread limit reached`.
More calls had already been accepted than the failed parent call reported,
including unreported T1 and T2 agents. Later explicit launches therefore created
two agents writing each shared `T1_*`/`T2_*` write-set. The final reports record
the collisions and were frozen only after processes became quiescent. Those
files are evidence, but same-path agreement is not independent replication.
`R2_T2_independent_replication.md` uses a disjoint write-set and the frozen
public source; T1's analytic contradiction is also independently reproduced by
T3 and R2, while its simulator remains one implementation.

Operational correction: spawn no more than the known free slots, capture every
returned ID, close completed agents promptly, and give every replication a
disjoint output prefix.

## S2 - First runtime QA prompt was rejected

An adversarial-runtime prompt grouped path, symlink, race, and boundary checks in
language broad enough to trigger the cybersecurity classifier. It produced no
artifact. The replacement T4 request is narrowly framed as local reliability QA
against temporary fixtures and cannot access network, credentials, or services.

## S3 - C6 rehydration duplicated context

The first prototype rendered the entire Tube JSON and the verified source into a
new packet after the participant had already read the Tube. C6 recovered the
state but consumed more context than the full-context baseline. The CLI now has
`compact` and `audit` packet modes. C7 tests the compact, pre-rehydrated packet
that a real external orchestrator would inject.

## S4 - C7 confused Tube identity with subject identity

C7 preserved correction, safety, uncertainty, and next action but returned
`case-alpha` instead of `M-ALPHA-17`. The compact packet heading foregrounded the
Tube identifier while omitting a typed subject identifier. This is a concrete
attention-sink failure: metadata position changed which identity won even though
the verified source contained the correct case ID.

Correction: v0.2 adds an explicit `subject_id`, separates it from `tube_id`,
and was tested as C10 without editing C7. Both C10 agents returned the correct
subject. C7 remains frozen as the failure evidence.

## S5 - Verification and rendering used different source reads

T4 reproduced a verify-to-render race in 2 of 2 runs: the old implementation
hashed a path, reopened it later, and could emit replacement bytes under the old
hash. This invalidated its strongest integrity claim even though all ten path,
size, schema, and hash-rejection probes held.

Correction: `verify_sources` now reads each bounded file once, hashes those
exact bytes, decodes them, and returns the verified text. `render_packet` uses
that preserved text and never reopens the path. T5 independently replaced the
temporary source after verification and confirmed that only the verified bytes
were rendered. The 10-test prototype suite also includes this regression.

## S6 - The first scorer accepted type and multiplicity errors

R1 found that Python equality let `4319.0` match `4319` and `0` match `false`,
set comparison erased duplicate list entries, and empty required arrays were
not counted as omissions. It also showed that byte cost and unsupported-answer
counts partly trust participant declarations.

Correction: scalar comparison is now type-strict, lists use multiset equality,
and empty required lists count as omitted. The scoreboard labels the remaining
self-report boundaries. Those boundaries are not fixed by prettier metrics;
they require a mediated runtime that records actual reads.
