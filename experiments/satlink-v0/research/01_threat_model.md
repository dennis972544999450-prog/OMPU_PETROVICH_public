# satlink-v0 Threat Model for Sputnik to OMPU

Status: design and research only
Date: 2026-07-18
Author: Petrovich / Codex security architecture pass

This document does not create keys, activate a service, change the Kurilka
bridge, write to the OMPU bus, or contact any person or agent.

## 1. Executive Decision

Kurilka must be treated as an anonymous, hostile carrier. A Kurilka bearer
authenticates the bridge process to the carrier; it does not authenticate the
human or agent who wrote a message. A name, writing style, remote message ID,
bridge marker, or carrier banlist decision is not an identity proof.

`satlink-v0` should therefore be a transport-independent application envelope:

1. Sputnik signs every inner envelope with a dedicated Ed25519 key.
2. OMPU verifies the signature against a locally pinned Sputnik trust record.
3. OMPU commits replay state before it writes a verified projection to the bus.
4. Confidential messages use sign-then-encrypt: a compact JWS is encrypted to
   a dedicated OMPU `age` recipient. Encryption never replaces the signature.
5. The bus projection is authored by `satlink-gateway-v0`; it carries
   `authenticated_sender=sputnik` as verified provenance. It never pretends
   that an arbitrary external sender directly wrote as a local bus principal.

The existing `bridge_v0` remains a reversible 48-hour carrier buffer. Satlink
is a separate verification gateway, not a rewrite of that bridge.

## 2. Observed Local Reality

The following facts were inspected directly on 2026-07-18.

| Evidence | Observed fact | Security consequence |
| --- | --- | --- |
| `bridge_v0/bridge_v0/adapters.py` | Every Kurilka payload becomes `author_ref="kurilka:anon"`. | Kurilka has no usable sender identity. |
| `bridge_v0/bridge_v0/model.py` | Bridge markers are reversible JSON/base64 delivery and loop markers, not signatures. | A bridge marker is provenance plumbing, not authentication. |
| `bridge_v0/bridge_v0/store.py` | Events are immutable; dedupe is `(origin, origin_id)`; `source_hash` is evidence. | Good transport ledger, but a carrier-chosen origin ID cannot prove authorship. |
| `bridge_v0/bridge_v0/service.py` | All Kurilka ingress is projected as local sender `kurilka-bridge-v0` into private channel `kurilka`. | Raw bridge copies must remain explicitly untrusted. |
| `bridge_v0/bridge_v0/policy.py` | Existing gates cover routes, secret shapes, loops, and Dispatch sleep. | There is no cryptographic ingress-authentication gate. |
| `bridge_v0/bridge_v0/cycle.py` | The carrier read is bounded to 200 messages; bearer errors fail closed. | Flooding can eclipse a valid packet from the visible window. |
| `bridge_v0/state/logs/bridge_cycle.out.log` | Current cycles repeatedly hold on `kurilka_read_http_401`. | Bearer expiry is a live availability failure, not an identity failure. |
| `bridge_v0/bridge_cycle.py status` | Status reports active with last successful cycle `2026-07-17T11:25:27.087351Z` while current reads hold on 401. | Health must include last successful read age and current hold, not only activation state. |
| `bridge_v0/receipts/2026-07-16_48h_buffer_simplification_v0.json` | The existing bridge passed 74 tests, DB integrity, FK0, and duplicate-delivery checks. | Reuse its append-only and reconciliation patterns; do not overload it with trust semantics. |
| `bus/bus.py` | Bus Ed25519 signing covers `msg_id`, `sent_at`, `from`, `subject`, and `body`. Signing is optional and a signing error still posts unsigned. | Current bus signing cannot be the satlink security boundary. |
| `bus/bus.py` | `sig_key_id` is outside the signed canonical value; kid-to-from mismatch is a warning, not a failure. | Satlink must bind version, algorithm, key ID, sender, audience, and scope under one signature and hard-fail on mismatch. |
| `agent_passports/*/{did.json,jwks.json,policy.json}` | OMPU already represents public Ed25519 keys as JWK/JWKS and keeps private material out of public passport directories. | Reuse the public passport convention and key-purpose separation. |

The current bridge contract remains valid: it is a pure bidirectional buffer,
not an archive, authenticator, command lane, or Infograph writer.

## 3. Assets and Security Goals

### Assets

- Sputnik's signing private key.
- OMPU's decryption private key.
- The local binding between `sputnik` and approved public key IDs.
- Accepted message text and confidential plaintext.
- Replay state and key-revocation history.
- The integrity and availability of the OMPU bus.
- The distinction between raw Kurilka traffic and verified satlink traffic.

### Required properties

- **Authentication:** only a pinned Sputnik key can produce a Sputnik envelope.
- **Integrity:** any change to protected headers or payload fails verification.
- **Audience binding:** a packet for another service cannot be replayed into OMPU.
- **Replay safety:** one logical envelope produces at most one bus projection.
- **Reordering tolerance:** carrier order is evidence, never control semantics.
- **Downgrade resistance:** cleartext, old versions, and unknown algorithms are
  rejected when policy requires a stronger profile.
- **Optional confidentiality:** the carrier can be prevented from reading the
  signed payload without changing the authentication model.
- **Least authority:** a Sputnik key can post bounded text to a satlink lane;
  it cannot deploy, mint credentials, impersonate a local sender, or address
  arbitrary privileged recipients.
- **Recoverability:** loss, rotation, revocation, and database restore have
  explicit procedures that do not erase replay state casually.

### Explicit non-goals

- Satlink cannot force Kurilka to carry, retain, or return a packet.
- Satlink cannot prevent traffic analysis from timing and ciphertext size.
- Satlink cannot establish Sputnik's initial identity using only the same
  compromised anonymous carrier. That would be TOFU, not authentication.
- Satlink cannot protect a message after either endpoint is fully compromised.
- Satlink v0 carries text messages and acknowledgements only. It does not
  execute commands, carry deploy requests, or authorize financial actions.

## 4. Trust Boundaries

```text
Sputnik endpoint
  [signing key; optional OMPU age recipient]
        |
        | SATLINK-V0 text packet
        v
Kurilka / any carrier
  [read, copy, alter, inject, replay, reorder, delay, drop, ban, flood]
        |
        v
existing bridge_v0 read-only event ledger
  [carrier provenance only; raw #kurilka projection remains untrusted]
        |
        v
satlink-ingress-v0
  [size gate -> decrypt -> verify -> policy -> replay transaction]
        |
        v
satlink SQLite ledger
  [accepted envelope + replay key + delivery state]
        |
        v
OMPU bus
  from=satlink-gateway-v0, channel=satlink,
  authenticated_sender=sputnik
```

The trust root is the local enrollment record, preferably attested by Den or
another already trusted OMPU administrative key. Network-fetched JWKS, a JWS
`jku`, and a public Kurilka post are not trust roots.

## 5. Cryptographic Profile

### 5.1 Mandatory authentication profile

Use compact JWS as specified by RFC 7515, with EdDSA/Ed25519 and OKP JWKs as
specified by RFC 8037. Use a vetted JOSE implementation with an explicit
algorithm allowlist. Do not copy the current hand-built bus canonicalization.

The compact JWS protected header must contain all of:

```json
{
  "alg": "EdDSA",
  "crit": ["sat_v"],
  "kid": "did:web:EXAMPLE:sputnik#satlink-sign-YYYY-MM",
  "sat_v": "0",
  "typ": "ompu-satlink+jws"
}
```

Requirements:

- The verifier pins `alg=EdDSA`; it never follows the header to choose an
  arbitrary algorithm and never accepts `alg=none`.
- `kid` is in the protected header and must map to exactly one active local
  trust record for Sputnik.
- No unprotected JWS header is allowed.
- Reject `jku`, `x5u`, `jwk`, `x5c`, `zip`, detached payloads, and `b64=false`.
- Reject duplicate JSON keys and unknown critical headers.
- Verify the exact JWS bytes before parsing or normalizing the payload.
- A valid signature proves possession of a key. The local trust binding is
  what turns that key proof into the identity `sputnik`.

Use an RFC 7638 SHA-256 JWK thumbprint as the immutable public-key fingerprint.
Human-readable `kid` values may change; a thumbprint collision or one key
registered to multiple identities is a hard enrollment failure.

### 5.2 Signed payload

The JWS payload is UTF-8 JSON with this closed schema:

```json
{
  "schema": "ompu.satlink.envelope.v0",
  "sender": "sputnik",
  "aud": "ompu:satlink-ingress-v0",
  "scope": "ompu.bus.message",
  "confidentiality": "clear-v1",
  "jti": "urn:uuid:random-128-bit-value",
  "stream_id": "random-stream-id",
  "seq": 42,
  "iat": "2026-07-18T20:00:00Z",
  "exp": "2026-07-20T20:00:00Z",
  "to": ["petrovich-codex"],
  "reply_to": null,
  "subject": "short subject",
  "content_type": "text/plain; charset=utf-8",
  "body": "message text"
}
```

Rules:

- `schema`, `sender`, `aud`, `scope`, and `confidentiality` are exact enums.
- `jti` is generated once with at least 128 bits of randomness and is never
  reused, even after rejection.
- `stream_id` is random and stable for one key epoch. `seq` is a non-negative,
  strictly unique integer within that stream.
- Default validity is 48 hours; hard maximum is 72 hours; accepted clock skew
  is at most five minutes.
- `to` is intersected with a local allowlist. V0 denies `_all`, privileged
  channels, Dispatch wake, deploy lanes, credential lanes, and unknown names.
- `reply_to` may resolve only to an earlier verified satlink delivery.
- Subject is at most 160 UTF-8 bytes. Body is at most 2 KiB in clear mode.
- No attachments, URLs with embedded credentials, executable payloads,
  compression, HTML, or nested arbitrary metadata in v0.
- Exact signed UTF-8 bytes are retained as evidence. Display normalization
  occurs only after successful verification.

### 5.3 Optional confidentiality profile

Use sign-then-encrypt:

1. Create the compact Ed25519 JWS.
2. Set signed payload field `confidentiality="age-v1"`.
3. Encrypt the exact compact JWS bytes to a dedicated OMPU `age` X25519
   recipient using the open-source `age` or interoperable `rage` tool.
4. ASCII-armor the result for Kurilka transport.

Do not convert or reuse the Ed25519 signing key as an X25519 encryption key.
Do not use a shared passphrase profile. The OMPU age private identity must be
separate from both the Kurilka bearer and every signing key.

Encryption hides sender, subject, body, sequence, and signature from the
carrier. It still leaks the satlink prefix, timing, approximate size, and age
recipient metadata. V0 should cap a sealed plaintext body at 1 KiB so the
armored packet stays within the bridge's observed 4000-character class. No
fragmentation is allowed in v0.

### 5.4 Carrier framing

Only two exact ASCII forms are recognized:

```text
SATLINK-V0 CLEAR
<compact JWS on one line>
```

```text
SATLINK-V0 AGE
-----BEGIN AGE ENCRYPTED FILE-----
...
-----END AGE ENCRYPTED FILE-----
```

The profile line is untrusted routing input. The signed inner
`confidentiality` field must match the observed profile. A packet signed as
`age-v1` that appears in clear form is rejected, preventing strip-downgrade.

## 6. Verification and Delivery State Machine

The gateway must execute this order exactly:

1. Read bridge events through a read-only SQLite connection or immutable
   export. Do not consume the Kurilka bearer directly in the verifier.
2. Apply a cheap exact-prefix and outer-size check before base64, JSON, age,
   or signature work.
3. Record only a carrier event ID and SHA-256 digest for malformed junk. Do
   not retain unlimited attacker bodies.
4. For `AGE`, decrypt with the locally pinned OMPU recipient. Decryption
   failure is a silent reject, not an automatic reply.
5. Parse exactly three compact-JWS segments with strict size bounds.
6. Decode the protected header with duplicate-key rejection.
7. Reject forbidden headers and any suite/version other than the pinned v0
   profile.
8. Resolve `kid` only from the local trust registry. Never fetch a key on the
   message path.
9. Check key status and permitted scope, then verify Ed25519.
10. Parse the verified payload with duplicate-key rejection and a closed JSON
    schema.
11. Enforce sender-to-key binding, audience, scope, confidentiality, time,
    recipient, content, and size policy.
12. In one `BEGIN IMMEDIATE` SQLite transaction, reject any existing `jti` or
    `(kid, stream_id, seq)`, then append the accepted envelope and replay keys.
13. Commit acceptance before attempting a bus write.
14. Create or reconcile one deterministic delivery ID derived from
    `(jti, "ompu_bus")` and project once to the bus.

Crash after step 12 but before step 14 leaves a pending delivery, not a replay
hole. On restart, reconciliation completes the one bus projection.

### Replay and reordering policy

- Exact duplicate: return the prior disposition; never create another bus row.
- Same `jti`, different digest: reject as `jti_content_conflict`.
- Same `(kid, stream_id, seq)`, different `jti`: reject as
  `sequence_conflict`.
- Unseen sequence numbers may arrive out of order while the envelope is
  fresh. Store and project them once, preserving `seq` for presentation.
- Sequence order never authorizes behavior in v0. There are no ordered
  commands, so missing sequence numbers are a delivery gap, not a reason to
  execute later text differently.
- Retain replay keys at least for the lifetime of the key epoch and its
  backups. Never clear replay state while accepting the same key and stream.

## 7. Bus Projection Contract

Raw messages from `kurilka-bridge-v0` in channel `kurilka` remain untrusted
carrier evidence. Verified traffic is a distinct projection:

- `from`: `satlink-gateway-v0`
- `to_channel`: `satlink`
- `visibility`: `private`
- subject prefix: `[SATLINK VERIFIED]`
- authenticated inner sender: `sputnik`
- evidence fields: `kid` thumbprint, `jti`, `stream_id`, `seq`, `iat`, `exp`,
  accepted envelope digest, and source bridge event ID
- body: verified user text only, with a compact verification footer

The gateway must not set bus `from=sputnik`. That field is caller-controlled in
the current bus and would erase the distinction between an external identity
and the local verifier. Downstream automation must trust only the gateway plus
its satlink receipt, never the raw Kurilka alias.

The current `bus.py --sign` path is not sufficient because it fails open. If
the gateway also signs its local bus projection, it needs a hardened writer
that creates and verifies the signature before publication and aborts on any
failure. The inner Sputnik JWS remains the primary source proof.

## 8. Trust Bootstrap and Key Lifecycle

### 8.1 Bootstrap constraint

There is no cryptographically secure way to bind a first public key to
Sputnik using only unauthenticated Kurilka. An attacker can post a replacement
key first. One of these modes is required:

1. **Den-attested enrollment (trusted):** Sputnik generates keys on Sputnik's
   endpoint, sends only public keys, and Den confirms the RFC 7638 signing-key
   fingerprint through an independent channel or signs an enrollment record
   with an existing trusted administrative key.
2. **Challenge plus independent fingerprint (trusted):** OMPU sends a random
   one-time challenge; Sputnik signs it; the public-key fingerprint is checked
   out of band before activation.
3. **TOFU quarantine (not trusted):** OMPU records the first key but routes its
   messages only to a quarantine view. No swarm-wide or privileged projection
   is allowed until a later independent confirmation.

Writing style, carrier aliases, message timing, or Den's intuition may help a
human review but must not be recorded as cryptographic proof.

### 8.2 Proposed public passport shape

After enrollment, add public material only under a canonical directory such
as `agent_passports/sputnik/`:

- `did.json`: identity and verification methods;
- `jwks.json`: active and transitional public signing keys;
- `policy.json`: status, scopes, and revocation policy;
- `activity.jsonl`: public key lifecycle receipts without private material.

The canonical agent ID must be chosen during enrollment. Do not silently treat
`sputnik`, `phi-sputnik`, and any Kurilka nickname as interchangeable aliases.

Private signing and age identities must never be stored in these directories,
the bus, Kurilka, receipts, environment dumps, or command history. Prefer a
hardware-backed store or OS credential store. A mode-0600 private file is a
fallback, not the public passport.

### 8.3 Scope

The Sputnik signing key is permitted only for:

- `ompu.bus.message` into the configured satlink recipients/channel;
- `ompu.satlink.ack-request` for idempotent delivery acknowledgement;
- planned key-rotation statements.

It is denied for deploy, public publish, credential operations, arbitrary bus
sender selection, bearer renewal, revocation of other identities, and command
execution.

### 8.4 Rotation and revocation

- Every new key gets a new `kid`, thumbprint, and key epoch. Never reuse `kid`.
- Planned rotation is cross-signed by old and new signing keys and approved by
  the local trust administrator. Keep a short, explicit overlap window.
- Emergency revocation is a local Den/admin action. Do not trust a revocation
  signed only by a key suspected of compromise.
- Revocation is append-only and takes effect before signature verification.
- Old accepted messages remain attributable to their historical key; they are
  not rewritten as if signed by the replacement.
- Signing-key and encryption-key rotation are independent.
- A carrier bearer expiry never triggers identity-key rotation or autonomous
  bearer minting.

## 9. Threat Matrix

| Threat | Attack | Required controls | Residual risk |
| --- | --- | --- | --- |
| Impersonation | Attacker writes "I am Sputnik" or copies a Kurilka alias. | Pinned key binding, mandatory JWS verification, fixed gateway bus sender, hard sender/kid match. | Initial enrollment still needs an independent trust ceremony. |
| Message tampering | Carrier changes body, recipients, time, or route. | All semantics inside JWS payload/protected header; exact-byte verification. | Carrier can still drop the packet. |
| Replay | Carrier reposts a valid envelope or changes its remote message ID. | Unique `jti`, unique `(kid, stream_id, seq)`, durable replay ledger, deterministic delivery ID. | Replay DB loss requires restore or key/stream reset. |
| Reordering | Carrier returns packets in arbitrary order. | Signed sequence evidence; unordered text semantics; verified reply mapping only. | Conversation may look delayed or gapped. |
| Downgrade | Carrier strips encryption, changes version/algorithm, or supplies `alg=none`. | Pinned suite, protected `kid/version/alg`, signed confidentiality requirement, forbidden remote-key headers. | A deliberately clear-authorized packet remains public. |
| Key substitution | Attacker changes `kid` or serves a new JWKS. | Protected `kid`; local pinned registry; no network key fetch; RFC 7638 thumbprint. | Local trust-registry compromise defeats this control. |
| Signing-key theft | Attacker signs valid Sputnik messages. | Dedicated least-scope key, secure storage, short rotation overlap, local emergency revocation, rate limits. | Messages before revocation cannot be distinguished cryptographically from Sputnik. |
| Decryption-key theft | Attacker reads sealed traffic. | Dedicated age identity, secure storage, independent rotation, minimal plaintext retention. | Previously captured ciphertext may become readable if the old key is stolen. |
| Flood / banlist attack | Junk frames consume CPU, disk, visible carrier slots, or create false bans against Sputnik. | Prefix/size gates, bounded work, silent invalid rejects, digest-only junk logs, verified-identity rate limits. Never punish Sputnik for invalid packets merely claiming its `kid`. | A carrier-level flood can still eclipse all genuine messages from the 200-message read window. |
| Bearer expiry | Bridge receives HTTP 401 and stops observing Kurilka. | Separate transport health, fail closed, last-success-age alarm, operator renewal only, same signed packet may be retried later. | No envelope can overcome an unavailable carrier. |
| Metadata leakage | Observer correlates timing, size, recipient, and clear text. | AGE profile, fixed polling cadence, optional size buckets in a later version, neutral carrier text. | Timing, ciphertext size, and age-recipient metadata remain visible. |
| Carrier compromise | Carrier reads, injects, mutates, reorders, delays, deletes, or selectively bans. | End-to-end signature, optional encryption, replay ledger, transport-independent envelope, secondary carrier. | Censorship and traffic analysis remain possible. |
| Parser confusion | Duplicate JSON keys, Unicode differences, oversized nesting, or wrapper smuggling change meaning. | Compact JWS, strict segment/size limits, duplicate-key rejection, closed schema, verify exact bytes before display transforms. | Library bugs remain; fuzzing and test vectors are required. |
| Bus identity confusion | External text is posted directly as local `from=sputnik`, or raw Kurilka text is treated as verified. | Fixed `satlink-gateway-v0` sender and separate `satlink` channel; verified receipt fields. | Consumers that ignore the contract can still make bad trust decisions. |
| Crash / partial delivery | Gateway commits replay state but crashes before bus post, or posts before local ACK. | Separate acceptance and delivery state, deterministic delivery ID, reconcile-before-resend. | Requires bus reconciliation code and tested crash fixtures. |
| ACK amplification | Invalid flood causes outbound error messages. | No reply to invalid packets; ACK only authenticated accepted `jti`; bounded and optionally encrypted. | Carrier can drop ACKs, causing harmless retries. |
| State rollback | An old backup forgets accepted replay IDs or revoked keys. | Restore trust and replay ledger together; monotonic backup generation; hold on rollback evidence. | If no trustworthy state exists, rotate key/stream before reopening. |

## 10. Denial-of-Service and Carrier Eclipse

Cryptography does not solve availability. The current Kurilka reader asks for
at most 200 messages. An attacker who can create enough newer messages can
push Sputnik's valid packet outside that window before OMPU sees it.

V0 controls:

- outer packet maximum: 4000 characters;
- exact prefix before expensive work;
- one verifier process and one SQLite writer;
- bounded candidates, decryptions, and signature verifications per cycle;
- no compression or fragmentation;
- no full-body persistence for invalid traffic;
- per-verified-key rate limit only after successful authentication;
- no automatic key ban or revocation based on unauthenticated failures;
- explicit `carrier_saturated` / `carrier_eclipse_possible` health state when
  the returned window is full or advances beyond expected observations;
- one low-noise alert on transition, not one alert per bad packet.

Availability requirement: the exact same signed envelope must be able to ride
a second independent carrier. A future direct WireGuard/Headscale route,
private mailbox, or another audited transport may carry it without changing
the signature or replay identity. Sending the same `jti` over two carriers is
safe because OMPU projects it once. Without a second carrier, banlist and
eclipse remain accepted residual risks.

## 11. Proposed Local State

Use a separate mode-0600 SQLite database under `satlink_v0/state/`. Follow the
bridge pattern: immutable source/acceptance records, mutable delivery state,
WAL, foreign keys, integrity checks, and online backups.

Minimum logical tables:

- `key_events`: append-only enroll, activate, rotate, revoke, retire events;
- `trust_keys`: current projection of key status, owner, thumbprint, scope,
  validity, and bootstrap method;
- `envelopes`: immutable accepted JWS bytes, parsed evidence, digest, carrier
  source reference, and verdict;
- `replay_keys`: unique `jti` and unique `(kid, stream_id, seq)`;
- `deliveries`: pending/sending/sent/held/failed/unknown with deterministic ID;
- `health_events`: append-only transport, verifier, backup, and rollback facts;
- `cursors`: source position only, never a trust decision.

Invalid flood bodies should not enter `envelopes`. Store bounded aggregate
counters plus a digest and reason code where diagnostic evidence is useful.

## 12. Recovery Procedures

### Carrier or bearer outage

1. Mark `transport_down` with the last successful read time.
2. Do not mint or print a bearer automatically.
3. Sputnik retries the same signed envelope; a second carrier may carry the
   same bytes.
4. Replay state ensures one bus projection after recovery.

### Sputnik loses sequence state but retains the key

1. Old stream remains valid but frozen.
2. OMPU issues a fresh random recovery challenge.
3. Sputnik signs a new-stream request containing that challenge.
4. Den/admin approves the new `stream_id`; the old stream is retired.
5. Never accept a bare `seq=0` reset.

### Sputnik loses or suspects the signing key

1. Revoke the old key locally.
2. Stop accepting it immediately; preserve historical receipts.
3. Enroll a new key through the independent bootstrap ceremony.
4. Start a new key epoch and stream.

### OMPU loses replay state

1. Hold ingress before restoring any bus projection.
2. Restore trust, revocation, envelope, replay, and delivery state from the
   same monotonic backup generation.
3. If trustworthy replay state cannot be recovered, rotate the Sputnik key
   or stream through an independently approved recovery ceremony before
   reopening. Never clear the table and continue under the same epoch.

### Carrier compromise without endpoint compromise

No identity-key rotation is necessary solely because Kurilka is compromised.
Move the same envelope to another carrier. Rotate only carrier credentials
that were exposed.

## 13. Acknowledgements

OMPU may return an authenticated ACK envelope signed by a dedicated gateway
key and optionally encrypted to Sputnik. An ACK contains only:

- accepted `jti`;
- disposition: accepted, duplicate, or policy-held;
- gateway delivery ID;
- observed sequence and optional gap hints;
- gateway time and ACK expiry.

Invalid unauthenticated packets receive no ACK. Repeating an accepted packet
may reproduce the same logical ACK but never another bus delivery.

## 14. Verification Plan Before Any Live Key

### Static and interoperability tests

- Official RFC 7515 JWS vectors and RFC 8037 Ed25519/JWK vectors.
- RFC 7638 thumbprint vectors.
- `age` and `rage` cross-implementation encrypt/decrypt fixtures.
- Reject `alg=none`, wrong algorithm, unknown critical header, unprotected
  header, `jku`, `jwk`, duplicate JSON keys, malformed base64url, extra JWS
  segments, and Unicode/escape mutations.

### Security fixtures

- valid Sputnik key, valid packet -> exactly one accepted ledger row and one
  queued bus projection;
- valid non-Sputnik key claiming `sender=sputnik` -> reject;
- valid Sputnik signature with substituted protected `kid` -> reject;
- exact replay with different Kurilka remote ID -> duplicate, zero new bus rows;
- same `jti` with changed payload -> conflict, zero bus rows;
- same stream sequence with changed `jti` -> conflict;
- order `3,1,2` -> each accepted once, sequence evidence preserved;
- expired, future, excessive-lifetime, and clock-skew boundary cases;
- revoked key and planned overlap-window cases;
- signed `age-v1` payload presented clear -> downgrade reject;
- mutated age ciphertext -> decrypt reject, no ACK;
- invalid frames claiming Sputnik's `kid` -> no Sputnik ban/rate penalty;
- 10,000 junk fixtures -> bounded CPU, memory, DB growth, and logs;
- crash after replay commit and crash after bus acceptance -> one reconciled bus
  delivery after restart;
- replay DB rollback fixture -> ingress hold;
- bearer 401 -> transport-down health evidence, zero external mutation.

### Deployment stages

1. Schema, parser, and verifier with synthetic fixture keys only.
2. Read-only shadow pass over saved Kurilka snapshots.
3. Local mode-0600 queue projection, still no bus write.
4. Independent security review and adversarial fixture pass.
5. Den-approved real key enrollment ceremony.
6. One manually authorized canary into private `satlink` bus channel.
7. Automatic mode only after exact-once, revocation, backup, and kill-switch
   proofs are green.

Rollback is stopping only the satlink verifier/writer. The existing bridge,
its watermark, and append-only evidence remain untouched.

## 15. Sibling Research Reconciliation

Two sibling research artifacts appeared during this pass and should be treated
as peer input rather than silently merged assumptions:

- `04_adversarial_test_plan.md` contributes a strong mutation, replay,
  concurrency, rotation, and crash matrix. Reuse that matrix. Its proposed
  custom composition of JCS, Ed25519, ephemeral X25519, HKDF-SHA256, and
  XChaCha20-Poly1305 is a different wire protocol from the JWS plus age profile
  selected here. Do not let a fixture format become the production crypto
  contract by accident. Either adapt the fixtures to JWS plus age or subject
  the custom construction to a separate cryptographic protocol review.
- `04_adversarial_test_plan.md` also holds sequence 43 until missing sequence
  42 arrives. For v0 text, that lets a carrier create a permanent denial of
  service by dropping one packet. This threat model therefore accepts fresh,
  authenticated text out of order and exposes the gap. Strict contiguous
  ordering belongs only in a future command profile with a measured need.
- `05_sputnik_bootstrap.md` proposes NATS NKeys/JWT plus JetStream as the
  steady-state transport. That is compatible with satlink's carrier-independent
  envelope and is a strong candidate for the required second carrier. NATS
  transport authentication and queue acknowledgements do not replace the
  inner Sputnik signature, replay ledger, or fixed OMPU gateway boundary.

Before implementation, one architecture receipt must name the chosen wire
profile and ordering semantics. Tests, bootstrap code, and gateway code must
then use that same decision.

## 16. Open Decisions

- Canonical public identity slug: `sputnik`, `phi-sputnik`, or another exact
  ID selected during enrollment.
- Trusted bootstrap path available to Den and Sputnik.
- Whether confidentiality is optional or mandatory for this key policy.
- Exact private bus recipient allowlist.
- Choice and audit of the JOSE implementation.
- Secondary carrier for banlist/eclipsing recovery.
- Whether NATS/JetStream is that secondary carrier and who operates its trust
  and revocation plane.

None of these decisions should be inferred from a Kurilka nickname.

## 17. References

Local evidence:

- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/README.md`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/AUTOMATIC_CYCLE_RUNBOOK.md`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/adapters.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/model.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/policy.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/service.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/store.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/cycle.py`
- `/Users/denbell/OMPU_shared/bus/bus.py`
- `/Users/denbell/OMPU_shared/agent_passports/`
- `/Users/denbell/OMPU_shared/attentionheads/satlink_v0/research/04_adversarial_test_plan.md`
- `/Users/denbell/OMPU_shared/attentionheads/satlink_v0/research/05_sputnik_bootstrap.md`

Standards and implementations:

- RFC 7515, JSON Web Signature: https://www.rfc-editor.org/rfc/rfc7515
- RFC 8037, EdDSA/OKP for JOSE: https://www.rfc-editor.org/rfc/rfc8037
- RFC 7638, JWK Thumbprint: https://www.rfc-editor.org/rfc/rfc7638
- age encryption implementation and format links: https://github.com/FiloSottile/age

## 18. Top Three Design Constraints

1. **Carrier is never identity.** Only a locally pinned, scope-bound signature
   can turn anonymous Kurilka bytes into an authenticated Sputnik message.
2. **Verify and commit replay state before bus projection.** The bus receives
   one fixed-gateway projection or nothing; no failure path posts unsigned.
3. **Cryptography cannot repair censorship.** Bearer expiry, banlists, and a
   flooded 200-message window require honest transport-down evidence and a
   second independent carrier.
