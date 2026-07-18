# Satlink v0 Adversarial Test Plan

Status: implementation-ready test design, offline only
Date: 2026-07-18
Target: signed and encrypted store-and-forward envelopes between OMPU agents
Safety boundary: no live services, live bus, live Kurilka state, or operational keys

## 1. Decision Under Test

Satlink v0 must make agent identity independent of the carrier. A carrier may
delay, duplicate, reorder, drop, ban, or rewrite its own metadata, but it must
not be able to:

1. impersonate a sender;
2. read or alter plaintext;
3. cause the same plaintext to be delivered twice;
4. revive a revoked or compromised key;
5. force a receiver to accept plaintext or a weaker protocol;
6. turn an uncertain carrier acknowledgement into a blind duplicate send.

The expected v0 behavior is fail closed with attributable, non-secret
receipts. Availability can degrade to `hold`; authenticity and confidentiality
must not degrade.

## 2. Existing Bridge Baseline

The current bridge tests were inspected before this plan was written. The
offline baseline command is:

```bash
cd /Users/denbell/OMPU_shared/attentionheads/bridge_v0
python3 -m unittest discover -s tests -v
```

Observed baseline on 2026-07-18: `74/74` tests passed.

The useful contracts to retain are:

| Existing area | Current proof | Satlink reuse |
|---|---|---|
| Immutable source events | `test_bridge_v0.py`, `test_model_store_adapters.py` | Store the accepted encrypted envelope and acceptance receipt append-only. |
| Source dedupe | Unique `(origin, origin_id)` and stable event IDs | Add cryptographic `envelope_id` and per-stream sequence uniqueness. |
| Delivery dedupe | Stable delivery ID, one acknowledged delivery | Deliver each verified plaintext at most once across all carriers. |
| Crash reconciliation | Unknown send outcome is reconciled before resend | An unknown carrier result blocks failover until reconciliation proves accepted or absent. |
| Concurrent sender claim | One claim winner, stale claim recovery | One decrypt/deliver winner for concurrent carrier copies. |
| Reordering | Thread child waits for parent | Valid sequence gaps wait without delivering out of order. |
| Expiry | Exact 72-hour source boundary and 48-hour projection cap | Signed `expires_at` is enforced exactly at the boundary. |
| Size guard | Kurilka rendered body max is 4000 characters | Satlink applies byte limits before JSON and crypto work. |
| Cycle flood guard | Six accepted writes per direction per cycle | Satlink adds per-stream pending and verification budgets. |
| Secret-safe receipts | Secret shape codes are emitted without secret values | Satlink receipts contain hashes and reason codes, never keys, plaintext, nonces, or ciphertext. |
| Local key-state guard | Bearer state requires mode `0600` | Operational key loading remains separate; tests use only obvious test keys. |
| Database proof | WAL, `integrity_check=ok`, foreign keys zero | Required after every state-mutating adversarial case. |

The existing bridge does not currently prove sender identity, ciphertext
confidentiality, AEAD integrity, replay windows, key rotation, revocation,
downgrade resistance, or carrier-independent failover. Satlink tests must not
claim those properties from the existing 74-test result.

## 3. Test Safety Contract

Every Satlink adversarial run must satisfy all of these conditions:

- Use `tempfile.TemporaryDirectory()` for databases, outboxes, keyrings, and
  receipts during a case.
- Use only keys under `satlink_v0/fixtures/keys/` whose IDs begin with
  `TEST-ONLY-`.
- Patch `socket.create_connection`, `socket.socket.connect`, HTTP clients, and
  live sink constructors to raise `OfflineViolation`.
- Scrub bearer, token, and live key environment variables in test setup.
- Refuse reads from `~/.kurilka_state.json`, the live bus database, LaunchAgent
  plists, and any path outside the fixture root and temporary run root.
- Use fake carriers with deterministic scripts. No DNS, HTTP, Telegram,
  Kurilka, bus, or LaunchAgent calls are permitted.
- Do not log private fixture seeds, decrypted bodies, ciphertext, signatures,
  shared secrets, or nonces. A receipt may contain their SHA-256 references.
- Treat any skipped test as a failed aggregate run. Security cases are not
  optional because a dependency is missing.

The host Python currently has neither `cryptography` nor `PyNaCl`. Do not
replace the missing dependency with hand-written cryptography. Before the
harness is implemented, create a hash-pinned, test-only dependency lock and an
offline wheelhouse. The runner should use `--no-index` and fail with
`dependency_missing` if the wheelhouse is absent.

## 4. Proposed Envelope Profile

This profile exists to make the test expectations exact. It is not permission
to deploy the protocol before a separate design and code review.

### 4.1 Cryptographic profile

- Signature: Ed25519.
- Key agreement: ephemeral X25519 sender key to static recipient X25519 key.
- KDF: HKDF-SHA-256 with a domain-separated Satlink context.
- AEAD: ChaCha20-Poly1305 with a 96-bit nonce.
- Canonical encoding: RFC 8785 JSON Canonicalization Scheme.
- Binary encoding: unpadded base64url.
- Domain separator: ASCII `SATLINK-V0\x00`.

Use a reviewed library for every primitive. The harness may inject fixed test
randomness, but production code must use the operating system CSPRNG and must
not expose the test injection seam.

### 4.2 Outer envelope

The exact schema should reject unknown fields and floats.

```json
{
  "schema": "satlink.envelope.v0",
  "envelope_id": "se_<64 lowercase hex>",
  "sender_id": "sputnik",
  "sender_sign_kid": "TEST-ONLY-sputnik-sign-b",
  "recipient_id": "petrovich-codex",
  "recipient_enc_kid": "TEST-ONLY-petrovich-enc-a",
  "stream_id": "sputnik:petrovich-codex:direct",
  "seq": 41,
  "issued_at": "2030-01-02T03:04:05Z",
  "expires_at": "2030-01-04T03:04:05Z",
  "ephemeral_pub": "<base64url>",
  "nonce": "<base64url>",
  "alg": {
    "signature": "Ed25519",
    "kex": "X25519",
    "kdf": "HKDF-SHA256",
    "aead": "ChaCha20-Poly1305"
  },
  "ciphertext": "<base64url>",
  "signature": "<base64url>"
}
```

`signature` covers:

```text
SATLINK-V0\x00 || JCS(protected_header_without_envelope_id) ||
\x00 || raw_ciphertext
```

The protected header includes every outer field except `envelope_id`,
`ciphertext`, and `signature`. The same protected-header bytes are AEAD
associated data. `envelope_id` is recomputed as:

```text
se_ || hex(sha256(signable_bytes || raw_signature))
```

The receiver rejects a claimed ID that differs from the recomputed ID.

### 4.3 Encrypted payload

```json
{
  "schema": "satlink.message.v0",
  "message_id": "sm-00000041",
  "content_type": "text/plain;charset=utf-8",
  "body": "satlink roundtrip 0041\n",
  "reply_to": null,
  "body_sha256": "sha256:<64 lowercase hex>"
}
```

No plaintext `body`, subject, preview, or fallback content is allowed in the
outer envelope. V0 leaks routing metadata, key IDs, sequence, and timing. It
does not claim metadata privacy.

### 4.4 Receiver decision order

The harness must spy on each stage and prove this order:

1. Enforce raw byte and nesting limits.
2. Decode UTF-8 and parse JSON while rejecting duplicate keys and trailing
   bytes.
3. Enforce exact schema, protocol version, and algorithm allowlist.
4. Recompute and compare `envelope_id`.
5. Check that recipient ID and recipient key ID are local.
6. Resolve sender key ID under the claimed sender ID and evaluate key status.
7. Verify the Ed25519 signature.
8. Enforce signed issue/expiry bounds and replay/sequence policy.
9. Derive the one-envelope key and perform AEAD decryption.
10. Validate the inner schema and body hash.
11. Atomically record acceptance, update stream state, and enqueue at most one
    plaintext delivery.

No rejected case may advance the sequence cursor or enqueue plaintext.

## 5. Deterministic Fixture Set

### 5.1 Clock and identities

All cases use a fake UTC clock:

```text
T0              = 2030-01-02T03:04:05Z
T_ROTATE        = 2030-01-02T04:04:05Z
T_REVOKE        = 2030-01-02T05:04:05Z
T_EXPIRES       = 2030-01-04T03:04:05Z
T_EXACT_EXPIRED = 2030-01-04T03:04:05Z
```

Fixture identities:

| Agent | Signing keys | Encryption keys |
|---|---|---|
| `sputnik` | `TEST-ONLY-sputnik-sign-a`, `TEST-ONLY-sputnik-sign-b` | `TEST-ONLY-sputnik-enc-a` |
| `petrovich-codex` | `TEST-ONLY-petrovich-sign-a` | `TEST-ONLY-petrovich-enc-a`, `TEST-ONLY-petrovich-enc-b` |
| `hausmaster` | `TEST-ONLY-hausmaster-sign-a` | `TEST-ONLY-hausmaster-enc-a` |
| `mallory` | `TEST-ONLY-mallory-sign-a` | `TEST-ONLY-mallory-enc-a` |

Each test private key is a fixed 32-byte seed derived by the fixture builder
from `sha256("satlink-v0 TEST ONLY:<kid>")`. These keys are intentionally
public test material and must never be accepted by a non-test key loader.

### 5.2 Deterministic randomness

For case `<case_id>`:

```text
ephemeral_seed = sha256("satlink-v0 fixture:<case_id>:ephemeral")
nonce           = first_12_bytes(sha256("satlink-v0 fixture:<case_id>:nonce"))
```

This rule is fixture-only. The fixture generator must require
`SATLINK_TEST_MODE=1`; production constructors must not accept deterministic
ephemeral keys or nonces.

### 5.3 Key registry timeline

The test registry is a self-contained local fixture, not a live trust service:

- `sputnik-sign-a` is active before `T_ROTATE` and retired at `T_ROTATE`.
- `sputnik-sign-b` is active at and after `T_ROTATE`.
- A normal retired key may validate an envelope first observed after rotation
  only when its signed `issued_at` is before `T_ROTATE`, it is still unexpired,
  and the key is not revoked or compromised.
- At `T_REVOKE`, `sputnik-sign-a` becomes compromised. Any first observation
  under that key is rejected after `T_REVOKE`, even if the envelope is
  backdated. An envelope accepted before compromise remains an immutable
  historical record and is never redelivered.
- `petrovich-enc-a` retires at `T_ROTATE`; new envelopes must target
  `petrovich-enc-b`. The old private key must not decrypt an envelope addressed
  to the new key.

### 5.4 Fixture layout

```text
satlink_v0/
  fixtures/
    keys/TEST_ONLY_KEYRING.json
    registry/key_timeline.json
    golden/A01_valid_roundtrip.json
    mutations/A02_forged_sender.json
    mutations/A03_altered_ciphertext.json
    mutations/A12_malformed_*.bin
    carriers/failover_scripts.json
    manifest.json
  tests/
    test_adversarial_envelope.py
    test_adversarial_replay_sequence.py
    test_adversarial_keys.py
    test_adversarial_limits.py
    test_adversarial_carriers.py
    test_receipt_contract.py
  tools/
    build_fixtures.py
    run_adversarial.py
  receipts/
```

`manifest.json` records the SHA-256 and expected byte count of every fixture.
`build_fixtures.py --check` must reproduce every golden fixture byte-for-byte
and fail if any checked-in fixture has drifted.

## 6. Required Adversarial Matrix

All verdict reason codes below are stable API values. Human text is not used
for pass/fail decisions.

| ID | Scenario and deterministic mutation | Expected verdict | Required state proof |
|---|---|---|---|
| A00 | Run the existing `bridge_v0` suite unchanged. | `baseline_green` and 74 passes. | No Satlink DB or fixture is opened by the legacy suite. |
| A01 | Valid Sputnik-to-Petrovich envelope at sequence 41, then decrypt and render UTF-8 body. Re-encode and verify the golden byte hash. | `accepted` then `delivered`. | One envelope, one acceptance, stream cursor 41, one plaintext delivery, body hash exact. |
| A02 | Claim `sender_id=sputnik` and `sputnik-sign-b`, but sign with Mallory's key. Encrypt correctly for Petrovich so encryption alone cannot save the forgery. | `rejected/sender_signature_invalid`. | Zero decrypt calls, zero stream movement, zero plaintext delivery. |
| A03a | Flip bit 17 in ciphertext after the valid envelope is signed. | `rejected/sender_signature_invalid`. | Signature fails before AEAD; no decrypt call. |
| A03b | Build a fixture with a corrupted ciphertext/tag and a newly valid outer test signature. This isolates the inner AEAD boundary. | `rejected/ciphertext_authentication_failed`. | One AEAD attempt, no plaintext, no sequence advance. Receipt does not distinguish tag bytes. |
| A04 | Submit the exact accepted A01 bytes again at `T0+10m`, then through a different fake carrier at `T0+20m`. | `duplicate/replay_exact`. | Acceptance and plaintext delivery counts stay at one; two carrier observations may be appended. |
| A05 | Two fake carriers concurrently submit the same new envelope. Synchronize both immediately before the atomic accept. | One `accepted`, one `duplicate/concurrent_carrier_copy`. | Unique `envelope_id`, one stream transition, one delivery; DB integrity is clean. |
| A06 | Submit valid sequence 43 before sequence 42 on a stream whose cursor is 41. Then submit 42. | First `hold/sequence_gap`; then 42 `delivered`; then 43 `released_and_delivered`. | Delivery order is exactly 42, 43. Cursor never jumps from 41 to 43. |
| A07 | Submit a valid envelope at exactly its signed `expires_at`. Also run a subcase one microsecond before expiry. | Exact boundary: `rejected/envelope_expired`; pre-boundary: `accepted`. | Expired case performs no AEAD and no sequence change. |
| A08 | Use a valid Sputnik signature over an envelope addressed to Hausmaster and `hausmaster-enc-a`, then present it to Petrovich. | `rejected/wrong_recipient`. | Petrovich private-key lookup and decrypt are not called; no key-existence detail leaks. |
| A09a | Before rotation, accept `sputnik-sign-a`. At rotation, accept `sputnik-sign-b`. Reject a newly issued post-rotation envelope under retired `sign-a`. | `accepted`, `accepted`, `rejected/sender_key_retired`. | Receipt records key IDs and registry version hashes, not keys. |
| A09b | Mark `sputnik-sign-a` revoked at `T_REVOKE` and submit a first-seen envelope under it. | `rejected/sender_key_revoked`. | No decrypt, sequence, or plaintext side effect. |
| A10a | Possess the compromised old signing fixture key, sign a new envelope after `T_REVOKE`, and backdate `issued_at` before rotation. Signature is cryptographically valid. | `rejected/sender_key_compromised`. | Registry status wins over attacker-controlled time; no delivery. |
| A10b | Encrypt a new envelope to `petrovich-enc-b`, then attempt decryption with retired `petrovich-enc-a`. | Old key attempt fails; current key succeeds. | No fallback to old recipient key and no key-ID guessing loop. |
| A11a | Generate envelopes at exactly `MAX_ENVELOPE_BYTES` and at limit plus one byte. Repeat for decrypted plaintext limit. | Exact limit follows normal validation; plus one is `rejected/envelope_too_large` or `rejected/plaintext_too_large`. | Oversized outer input is rejected before JSON/crypto. Oversized plaintext is discarded and never delivered. |
| A11b | At one fake-clock instant, submit more than the configured per-sender verification budget and more sequence-gap envelopes than `MAX_PENDING_PER_STREAM`. | Bounded items are handled; excess is `hold/rate_limited` or `rejected/pending_window_full` per policy. | Memory, DB rows, and pending bytes stay within declared limits. No starvation of a second stream. |
| A12 | Parameterize invalid UTF-8, truncated JSON, trailing bytes, duplicate `sender_id`, duplicate nested `alg.aead`, missing field, unknown field, float `seq`, negative `seq`, excess nesting, invalid base64url, and overlong integer. | `rejected/malformed_envelope` with a non-secret subcode. | No key lookup or crypto for parse/schema failures; one bounded rejection receipt per input. |
| A13a | Send `schema=satlink.envelope.v-1`, an unapproved algorithm, or remove the algorithm block. | `rejected/protocol_downgrade`. | No fallback parser or legacy carrier path is called. |
| A13b | Inject raw bridge JSON or outer fields `body`, `subject`, or `plaintext`, with or without a fake signature. | `rejected/plaintext_injection`. | Receipt contains only field names/reason, never injected content. |
| A14a | Primary carrier returns a proven pre-accept failure. Secondary carrier then accepts the exact same envelope bytes. | `delivered_via_failover`. | Attempts are `[primary:confirmed_not_accepted, secondary:accepted]`; one envelope and one delivery. |
| A14b | Primary carrier returns timeout after possible acceptance. Secondary is available. | `hold/carrier_outcome_unknown`. | Secondary send count remains zero until reconciliation. No blind failover. |
| A14c | Reconciliation later proves A14b present at primary, or proves absent. | Present: reconcile and stop. Absent: send exact bytes to secondary. | In both subcases, at most one receiver delivery and one final acknowledged carrier path. |

### Recommended tail cases

These are not substitutes for the required matrix. They close high-value gaps
that often appear only after the main tests pass.

| ID | Scenario | Expected result |
|---|---|---|
| A15 | Two valid, differently encrypted and signed envelopes claim the same `(sender_id, stream_id, seq)` with different IDs. | First wins; second is `rejected/sequence_equivocation`, never treated as an ordinary duplicate. |
| A16 | Change only `envelope_id`, JSON key order, Unicode representation, or base64 padding. | Wrong ID is rejected; alternate non-canonical wire encodings are rejected or canonicalized before one unambiguous signature check according to schema policy. |
| A17 | Use a real key ID belonging to Mallory while claiming Sputnik, or collide key IDs across agents. | `rejected/key_identity_mismatch`; registry lookup is namespaced by agent ID. |
| A18 | Crash after durable acceptance but before plaintext-delivery ACK, restart, and reconcile. | One eventual plaintext delivery, never two; immutable acceptance survives restart. |
| A19 | Scan all receipts, logs, exceptions, and unittest output for known fixture plaintext, private seed hex, shared-secret hash inputs, ciphertext, signature, and nonce. | `receipt_secrecy=ok`, zero matches. |
| A20 | Flood stream A while sending one valid in-order message on stream B. | Stream B progresses within the fairness bound; stream A cannot monopolize the receiver. |

## 7. Exact Assertions Per Security Boundary

### Authenticity

- Sender identity comes only from a verified signing key bound to `sender_id`.
- Carrier author names, account IDs, banlists, and headers are observations,
  never identity proof.
- A valid signature under the wrong agent's key fails.
- A valid signature under a revoked or compromised key fails on first
  observation.

### Confidentiality and integrity

- The carrier fixture sees only outer metadata and ciphertext.
- Bit changes are detected before any plaintext reaches the application.
- Wrong-recipient processing never tries every local private key.
- Decryption failure produces a generic reason and no key oracle detail.

### Replay and ordering

- `envelope_id` is globally unique in the local acceptance ledger.
- `(sender_id, stream_id, seq)` is unique.
- Exact duplicate bytes are idempotent.
- Different valid content at the same sequence is equivocation, not duplicate.
- Sequence gaps are bounded holds. They do not move the delivery cursor.
- Expiry can remove a gap-held message, but cannot make later content appear to
  have been delivered in order without an explicit gap policy receipt.

### Carrier failover

- Failover reuses exact envelope bytes and the same `envelope_id`.
- A confirmed pre-accept failure permits immediate failover.
- An outcome-unknown response requires reconciliation before failover.
- Receiver dedupe is the final safety boundary if two carriers race despite
  sender precautions.

### Key lifecycle

- Registry decisions use an immutable registry-version hash in each receipt.
- Rotation, retirement, revocation, and compromise are distinct states.
- Backdating cannot bypass compromise.
- Previously accepted history is not reprocessed when a key is later revoked.
- Current encryption never silently falls back to a retired recipient key.

## 8. Resource Limits Used By The Harness

Initial deterministic values for tests:

```text
MAX_ENVELOPE_BYTES       = 131072
MAX_CIPHERTEXT_BYTES     = 98304
MAX_PLAINTEXT_BYTES      = 65536
MAX_JSON_DEPTH           = 16
MAX_PENDING_PER_STREAM   = 16
MAX_PENDING_BYTES_STREAM = 1048576
VERIFY_BUDGET_PER_SENDER = 32 per 60 fake-clock seconds
VERIFY_BUDGET_GLOBAL     = 128 per 60 fake-clock seconds
```

These values are test-contract proposals, not deployment tuning. Changing one
requires changing the fixture manifest and producing a receipt that names the
old and new limits.

The flood tests must measure bounded effects rather than wall-clock speed:
peak pending row count, peak pending bytes, crypto-call count, delivery count,
and fairness progress. Wall-clock thresholds are too noisy to be the primary
security assertion.

## 9. Fake Carrier Scripts

The fake carrier API is deterministic:

```python
class FakeCarrier:
    def send(self, envelope_bytes: bytes, envelope_id: str) -> CarrierResult: ...
    def reconcile(self, envelope_id: str) -> CarrierResult: ...
```

Allowed scripted results:

- `accepted(remote_id)`
- `confirmed_not_accepted(code)`
- `outcome_unknown(code)`
- `already_present(remote_id)`
- `unavailable(code)`

Carrier fixtures must record only carrier name, call ordinal, input SHA-256,
result class, and opaque fake remote ID. A carrier script may not inspect or
alter plaintext because it never receives plaintext.

## 10. Pass/Fail Receipts

### 10.1 Per-case receipt

Each case writes one JSON receipt to a temporary directory and, only when the
whole run completes, copies the redacted receipt into
`satlink_v0/receipts/cases/`.

```json
{
  "schema": "satlink.adversarial.case_receipt.v0",
  "run_id": "run_<fixture-manifest-hash-prefix>",
  "case_id": "A05",
  "fixture_sha256": "sha256:<hex>",
  "status": "pass",
  "expected": {
    "verdicts": ["accepted", "duplicate/concurrent_carrier_copy"],
    "plaintext_deliveries": 1
  },
  "observed": {
    "verdicts": ["accepted", "duplicate/concurrent_carrier_copy"],
    "envelope_rows": 1,
    "acceptance_rows": 1,
    "plaintext_deliveries": 1,
    "decrypt_calls": 1
  },
  "state_proof": {
    "integrity_check": "ok",
    "foreign_key_violations": 0,
    "stream_cursor": 41
  },
  "privacy_proof": {
    "keys_printed": false,
    "plaintext_printed": false,
    "ciphertext_printed": false,
    "known_secret_match_count": 0
  }
}
```

No receipt field may contain the outer envelope, inner message, raw key,
signature, nonce, ciphertext, or exception traceback with those values.

### 10.2 Aggregate receipt

`satlink_v0/receipts/satlink_v0_adversarial_<UTC>.json` contains:

- fixture manifest hash;
- source revision or `not_a_git_repository`;
- Python and pinned crypto-library versions;
- exact command;
- required case IDs and pass count;
- failed and skipped counts;
- existing bridge baseline result;
- `integrity_check` and foreign-key result for every persistent test DB;
- network-call count, which must be zero;
- live-key-path access count, which must be zero;
- receipt privacy scan result.

Aggregate status is `green` only when:

```text
required_failed == 0
required_skipped == 0
legacy_bridge_failed == 0
network_call_count == 0
live_key_path_access_count == 0
known_secret_match_count == 0
all_database_integrity_checks == "ok"
all_foreign_key_violation_counts == 0
```

## 11. Runnable Commands

After the harness and offline dependency wheelhouse are implemented:

```bash
cd /Users/denbell/OMPU_shared/attentionheads/satlink_v0

python3 -m venv .venv-test
.venv-test/bin/python -m pip install \
  --no-index --require-hashes \
  --find-links vendor/wheels \
  -r requirements-test.lock

SATLINK_TEST_MODE=1 PYTHONHASHSEED=0 \
  .venv-test/bin/python tools/build_fixtures.py --check

SATLINK_TEST_MODE=1 PYTHONHASHSEED=0 \
  .venv-test/bin/python -m unittest discover \
  -s tests -p 'test_adversarial_*.py' -v

SATLINK_TEST_MODE=1 PYTHONHASHSEED=0 \
  .venv-test/bin/python tools/run_adversarial.py \
  --offline \
  --manifest fixtures/manifest.json \
  --receipt-dir receipts

cd /Users/denbell/OMPU_shared/attentionheads/bridge_v0
python3 -m unittest discover -s tests -v
```

`tools/run_adversarial.py` exits:

- `0`: all required cases and receipt checks are green;
- `2`: fixture or dependency problem;
- `3`: security assertion failed;
- `4`: offline boundary or live-key-path violation;
- `5`: receipt privacy violation.

## 12. Implementation Order

1. Build the duplicate-key-rejecting parser, exact schema, canonical encoder,
   offline guard, fixture key loader, and receipt redactor.
2. Implement A01, A02, A03, A08, A12, and A13 before adding persistence.
3. Add append-only acceptance storage and implement A04, A05, A06, A15, and
   A18 using SQLite WAL and atomic unique constraints.
4. Add registry timeline logic and implement A09, A10, and A17.
5. Add resource budgets and implement A11, A19, and A20.
6. Add fake carriers and implement A14 only after receiver idempotency is
   green.
7. Run the unchanged 74-test bridge baseline and emit the aggregate receipt.

No live carrier adapter should be written in this test phase. The promotion
gate is a separate review that requires a green aggregate receipt, protocol
review, operational key-management design, rollback plan, and a bounded
shadow-mode integration fixture.

## 13. Known Limit That Tests Must Not Hide

Ephemeral-sender X25519 to a static recipient key does not provide full
post-compromise secrecy for historical ciphertext if the recipient's old
private encryption key is later stolen and retained. A ratchet or one-time
prekey design is a later protocol decision. Satlink v0 may prove carrier
independence, authenticated encryption, rotation, revocation, and bounded
replay behavior without claiming Signal-style forward secrecy.

That limitation belongs in the aggregate receipt as
`forward_secrecy_profile: static_recipient_key_no_historical_pcs` until a
separately tested ratchet replaces it.
