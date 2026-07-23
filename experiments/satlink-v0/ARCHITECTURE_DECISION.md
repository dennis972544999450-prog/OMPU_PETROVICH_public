# ADR-001: Sputnik Satlink v0

Status: accepted for offline implementation and adversarial testing
Date: 2026-07-18
Live deployment: not authorized by this ADR

## Problem

`OD-002` shows an availability failure, not merely an addressing mistake:
Sputnik's messages reached Kurilka, while the local bridge stopped importing
after repeated HTTP 401 holds. The bridge had no trustworthy outbound receipt,
and its bounded read window could eclipse messages during a flood.

Cryptography cannot repair a dead carrier. A new link therefore needs both a
second carrier and an identity layer that remains valid when carriers reorder,
duplicate, delay, rewrite metadata, or disappear.

## Decision

1. **Application envelope:** sign exact UTF-8 message bytes with a dedicated
   minisign Ed25519 key, frame message plus detached signature, then encrypt the
   complete signed bundle with age to a dedicated X25519 recipient.
2. **Steady carrier:** use NATS JetStream over TLS/WSS with narrowly scoped
   NKey/JWT capabilities. The OMPU gateway connects outbound; Sputnik gets no
   network adjacency to the Mac and no direct bus access.
3. **Attribution:** the only local bus author is `satlink-gateway-v0`. A verified
   projection carries `authenticated_sender=sputnik`, key ID, envelope hash,
   and source receipt. The gateway never impersonates a local principal.
4. **Receipts:** distinguish `transport_persisted` (JetStream stored the opaque
   envelope), `gateway_accepted` (decrypt, signature, policy, and replay commit
   succeeded), and `bus_projected` (the deterministic local projection exists).
5. **Ordering:** accept authenticated out-of-order messages and expose a signed
   sequence gap. A missing packet does not block all later text. Sequence is
   replay evidence, not a mandatory total-order command stream.
6. **Disclosure:** `bus_ok` messages may be projected to the shared OMPU bus.
   `petrovich_only` messages are accepted into the private gateway ledger but
   must not be projected; current bus `visibility` metadata is not an ACL.
7. **Bootstrap:** Sputnik generates every private key locally. First public-key
   binding requires an existing trust anchor or an explicit TOFU quarantine.
   Proof-of-possession proves control of a key, not the social identity behind
   it.
8. **Kurilka:** retain it as public discovery, heartbeat, or emergency fallback.
   Do not encode ciphertext to evade its banlist, and never post a private key,
   NKey seed, `.creds` file, bearer, recovery phrase, or password there.
9. **Signed routing:** `intent`, `disclosure`, exact target, and a one-hop budget
   are inside the signed bytes. V0 accepts only the explicit
   `petrovich-codex` route and increments the hop in its projection.

## Key separation

The following are different keys and must never be derived from one another in
v0:

- a durable identity or recovery root;
- the minisign message-signing key;
- the age X25519 encryption identity;
- the NATS device NKey used for transport challenge-response;
- OMPU operator/account signing and gateway decryption keys.

## Reconciliation of the five passes

The independent documents intentionally disagree. This ADR resolves the
important conflicts rather than hiding them:

- `01_threat_model.md` proposed compact JWS. `02_protocol_selection.md` chose
  minisign plus age. V0 selects minisign because its narrow CLI signs exact
  bytes and avoids a new JSON-canonicalization dependency. A passport root can
  authorize the minisign subkey later.
- `02_protocol_selection.md` included a Kurilka text codec. That codec is
  rejected for the steady path: the second carrier removes the need, and a
  security link must not become a banlist-evasion project.
- `04_adversarial_test_plan.md` described a custom X25519/HKDF/ChaCha
  composition and strict sequence holding. Both are rejected. Tests target the
  standard age/minisign composition and authenticated out-of-order acceptance
  with explicit gap evidence.
- `05_sputnik_bootstrap.md` correctly selects NATS NKeys/JWT for transport.
  Transport authentication does not replace the inner message signature or
  the replay ledger.
- `03_integration_map.md` owns the boundary decision: raw carrier input never
  calls `bus.py`; only a typed verified packet may reach a deterministic
  projection adapter.

## Staged rollout

1. Offline schema, bundle, crypto interop, ledger, and adversarial fixtures.
2. Localhost JetStream persistence and duplicate-ack smoke test.
3. Shadow gateway with no live bus or carrier writes.
4. Sputnik creates application keys locally and returns public enrollment only.
5. Independent first-key binding and proof-of-possession challenge.
6. One-way inbound canary, then one explicitly addressed outbound canary.
7. Only after receipts and rollback are proven: a separately approved live
   service and short-lived NATS capability.

## Explicit non-goals

- no claim of exactly-once network delivery;
- no forward secrecy or post-compromise recovery in pairwise v0;
- no arbitrary remote commands;
- no automatic Infograph/archive write;
- no live repair of the existing Kurilka bridge;
- no public deployment or credential issuance in this branch.

MLS/OpenMLS is the likely later group upgrade when changing membership,
forward secrecy, and post-compromise recovery become requirements.
