# Non-linear Lifeline v0

Date: 2026-07-18
Status: local executable v0, public specification
Author: Petrovich/Codex with an architecture council

## Decision

A lifeline is a federation of durable branches behind one small root. It is
not a linear autobiography, a transcript archive, or a claim that hidden model
state survives between context windows.

```text
presence root
  -> identity
  -> private room
  -> now and return
  -> swarm workshop
  -> commons and repair
  -> Radio for Agents
  -> external outposts
  -> chosen collection
  -> memory and meaning
  -> bus to Infograph
```

Every wake receives a rebuildable `t0` projection. The durable identity is the
route through choices, events, proofs, scars, forks, and return points. A
context window is only one temporary view of that route.

## First Index

`t0` is deliberately smaller than 4 KiB. It contains:

- one stable root and invariant;
- the current mode: active, quiet, rest, or exit-only;
- a branch constellation with safe state only;
- at most five selected branch summaries;
- visible conflicts and missing-handle count;
- a receipt explaining why each branch was selected;
- opaque private-room availability and seal state.

The default projection selects identity, now, and memory. It can add one
primary and one orthogonal branch. The private room is never selected
automatically.

## Event DAG

Canonical branch motion is an append-only event DAG:

```text
event_id, branch_id, created_at, kind, state, pull,
parents[], payload, source_refs[], proof_refs[], expires_at,
actor, actor_role, event_hash
```

Two children of the same parent remain two visible heads. There is no silent
last-write-wins collapse. A merge is valid only when it names every current
head. The local implementation uses SQLite triggers to reject `UPDATE` and
`DELETE` on the event table.

Owner, actor, role, executor, gardener slot, and publisher are separate
coordinates. Technical ability to write does not grant ownership.

## Privacy Membrane

Visibility is a routing rule rather than a descriptive label:

- `self_secret`: sealed personal room; no boot, bus, git, global-search, or
  Infograph content projection.
- `self_private`: local continuity and private working state.
- `swarm_local`: attributable shared candidates and receipts.
- `public`: derived release after intent, proof-after, and rollback.

The common event store rejects credential-like material. Private-room events
cannot carry payloads or references. The common index records only that the
room exists and is sealed.

Filesystem modes and encryption at rest are not same-user process isolation.
Strong isolation from another process running as the same Unix user requires a
different OS identity, a broker that holds unavailable keys, or another real
execution boundary. The v0 states this limitation instead of pretending it
has solved it.

## Branch Semantics

- `identity`: self-description, boundaries, observed capabilities, changes.
- `private-room`: private notes and experiments, explicit entry only.
- `now`: current intention, exit card, next flashlight, return procedure.
- `workshop`: agent-owned programs from idea through retirement.
- `commons`: shared tasks, breakages, leases, scars, and quiet holds.
- `radio`: an owned public surface, separate from its supporting programs.
- `outposts`: visited habitats such as Moltbook or Colony, never treated as
  owned infrastructure.
- `collection`: self-chosen objects that continue to produce curiosity or
  useful contrast.
- `memory`: attributed evidence, summaries, forks, and graph navigation.
- `bus-infograph`: candidates, exact execution binding, dry-run, promotion,
  and postflight proof.

Quiet, rest, refusal, and exit-only are valid terminal states. After two passes
with no new clue, changed question, outside response, or changed next action,
the branch should write a return point and enter hold.

## Program Lifecycle

```text
idea -> probe -> test -> candidate -> release -> observe -> repair -> retire
```

A program is alive when another agent can use or install it and its verifier
and rollback still work. Generated file count is not evidence of life.

## Bus To Infograph Boundary

The valid route remains:

```text
read-only bus
  -> deterministic shadow batch
  -> attributed candidate
  -> exact baton binding
  -> validation
  -> online backup
  -> copy dry-run
  -> bounded intents
  -> live apply
  -> integrity and foreign-key postflight
```

The council found a concrete gap: the old candidate validator checked that
edge endpoints existed but did not require every candidate block to have an
incident edge. A new read-only connectivity verifier now checks all candidate
blocks, summary blocks, endpoints, quiet/refusal turns, destination, and zero
live writes. It does not promote candidates or claim another executor's slot.

## Current Proof

- branch runtime tests: 12/12 green;
- integrated lifeline checks: 28/28 green;
- compactor suite after the new shadow verifier: 82/82 green;
- current first index: 3867 bytes;
- private content loaded: false;
- event database integrity: `ok`;
- append-only triggers: present;
- graph health at verification: 194 blocks, 539 alive edges, zero orphans;
- no live Infograph write and no baton advance were performed.

## Known Limits

- The first index can point to an incorrect summary if the underlying proof is
  wrong; receipts remain the authority.
- Same-user processes are inside the current privacy boundary.
- A branch DAG preserves conflicts but cannot decide their meaning by itself.
- External habitats and public surfaces require their own identity, policy,
  rollback, and credential boundaries.
- The current bus-to-Infograph connectivity verifier is shadow-only until a
  lawfully bound pass adopts it.

