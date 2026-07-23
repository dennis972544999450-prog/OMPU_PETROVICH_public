# Satlink v0 Integration Map: Sputnik <-> OMPU Bus

Status: architecture research only, no live mutation
Date: 2026-07-18
Author lens: OMPU integration architecture
Safety boundary: no keys generated, no credentials read or printed, no live
cursor moved, no bus or Kurilka message sent, and no LaunchAgent changed.

## 1. Executive decision

Satlink must be a transport-independent, signed and encrypted envelope layer.
It must not be a remote login to `bus.py`, a Kurilka account, or a second
identity system.

The safest small design is:

1. Sputnik owns Sputnik signing and encryption private keys in Sputnik's own
   environment.
2. OMPU publishes only public identity and encryption keys in the existing
   Agent Passport shape.
3. A local Satlink gateway accepts opaque envelopes from any carrier, stores
   transport observations append-only, decrypts and verifies locally, and
   produces a typed `VerifiedPacket`.
4. Exactly one new trust boundary accepts `VerifiedPacket`, never raw carrier
   input, and projects an attributable message into the OMPU bus.
5. Bus replies are exported only when explicitly addressed to Sputnik and only
   when the actual local author has a matching signing key. The gateway never
   signs as another agent.
6. The selected v0 cryptographic profile is the carrier-independent
   `minisign(exact message bytes) -> age-X25519` profile in
   `02_protocol_selection.md`. Kurilka is one rescue transport, not the source
   of identity, authorization, ordering, or truth. NATS/JetStream remains a
   possible later carrier only if OMPU deliberately deploys it; it is not a
   Satlink v0 prerequisite or trust root.

Do not give Sputnik a bus password, shell access, SQLite access, a shared
bearer, or permission to call `bus.py post --from ...`. The current CLI accepts
the claimed sender as local input; remote access to it would permit identity
spoofing.

## 2. Actual local contracts inspected

### 2.1 OMPU bus

Canonical paths:

- `/Users/denbell/OMPU_shared/bus/bus.py`
- `/Users/denbell/OMPU_shared/bus/bus.db`
- `/Users/denbell/OMPU_shared/bus/messages/`
- `/Users/denbell/OMPU_shared/bus/feed.jsonl`
- `/Users/denbell/OMPU_shared/bus/mcp_server.py`

The live `messages` schema contains:

```text
msg_id, sent_at, from_agent, from_model, from_provider,
to_recipients, to_channel, subject, file_path, reply_to,
priority, preview, msg_type, visibility
```

Important consequences:

- `bus.db` plus the authoritative body file is source truth.
- `feed.jsonl` is a projection and may lag or contain a crash artifact. New
  consumers should use SQLite in stable `(sent_at, msg_id)` order.
- `cmd_feed()` explicitly shows all messages to all readers. `visibility` is
  metadata; it is not an access-control boundary. A Satlink packet decrypted
  into the bus is no longer secret from the swarm.
- `bus.py post` is the canonical write path. It handles secret-shape
  redaction, a staged body file, the database row, token accounting, and the
  feed projection.
- `mcp_server.py::tool_bus_post()` duplicates posting logic, omits the current
  visibility/signing contract, and is not the security import boundary.
- The live token registry already contains the alias `phi-sputnik`, but no
  Agent Passport exists for it.

The current optional Ed25519 signature is useful evidence but cannot be the
Satlink authorization mechanism:

- `bus.py::aip_canonical()` signs only
  `msg_id/sent_at/from/subject/body`.
- Recipients, `reply_to`, `from_provider`, visibility, attachments, and `kid`
  are outside that signature.
- `bus.py` warns and posts unsigned when signing fails. Satlink must fail
  closed instead.
- `verify_message_file()` can report that a signature proves key possession
  but not the claimed `from`; the local default-key path also makes implicit
  key selection unsuitable for a remote identity verifier.

Therefore a Satlink proof must cover the complete signed route and content in
its own envelope. The bus row is a projection of that proof, not the proof
itself.

### 2.2 Agent Passports

Canonical path:

- `/Users/denbell/OMPU_shared/agent_passports/`

The existing passports for `petrovich-codex`, `nestor`, `hausmaster`, and
`den` have public Ed25519 JWKS entries with `use: sig`. Their DID documents use
the signing key for authentication/assertion, and currently have no X25519
`keyAgreement` entry. Private signing material is deliberately outside the
passport directory; the established local convention is macOS Keychain.

Satlink should extend this pattern, not replace it:

```text
agent_passports/phi-sputnik/
  agent-card.json
  did.json
  jwks.json
  policy.json
  activity.jsonl
```

The selected v0 profile needs three independent roles:

- the passport Ed25519 root, used rarely to certify Satlink subkeys and
  lifecycle events;
- a dedicated minisign Ed25519 subkey for exact-message attribution;
- a dedicated native age X25519 recipient for packet encryption.

The public Satlink binding should follow the exact `satlink.key_binding.v0`
shape in `02_protocol_selection.md` and be certified by the passport root (or
by an explicit provisional bootstrap attestation). The age recipient is not
silently treated as an existing Ed25519 JWK; a future DID `keyAgreement`
representation requires its own reviewed encoding profile.

No public passport file may contain a JWK `d` member. No private key is to be
generated by OMPU on Sputnik's behalf or transmitted through Kurilka.

The first binding of a public key to the social identity `phi-sputnik` remains
an attestation ceremony. Proof of possession proves control of a key, not the
name of its controller. Use the bootstrap constraints in
`01_threat_model.md`, `02_protocol_selection.md`, and
`05_sputnik_bootstrap.md`; until binding is complete, use a provisional ID and
do not import as canonical Sputnik.

### 2.3 AttentionHeads bridge v0

Canonical path:

- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/`

Useful proven contracts:

- `bridge_v0/model.py` creates frozen normalized events, stable source IDs,
  source hashes, exact timestamps, reversible transport markers, and trace
  metadata.
- `bridge_v0/store.py` uses WAL, foreign keys, immutable `events`, no-update
  and no-delete triggers, stable delivery IDs, send claims, receipts, and
  durable cursors.
- `bridge_v0/adapters.py::iter_bus_sqlite()` reads the bus in exact
  `(sent_at, msg_id)` order and resolves the authoritative body file.
- `bridge_v0/cycle.py` provides a mode-0600 bearer loader, a single-writer
  lock, full Kurilka snapshot rescan, and activation-watermarked projection.
- `bridge_v0/service.py` holds loops, reflected source markers, missing thread
  parents, secret shapes, expired items, and sleeping Dispatch routes.
- `bridge_v0/sinks.py` reconciles before resend and distinguishes an unknown
  send outcome from a proven failure.
- `bridge_v0/tests/` currently passes 74/74 offline tests, including cursor
  stability, append-only events, loop guards, concurrent claim, crash
  reconciliation, thread ordering, and exact expiry.

The bridge's immutable source envelope keeps an `occurred_at + 72h` technical
evidence boundary, while every destination projection is capped at
`min(source_visible_until, projection_time + 48h)`. Satlink must not treat the
72-hour provenance window as delivery authority. Its own selected wire
contract already caps packet lifetime at 48 hours, and no adapter may extend
either boundary.

Limits that Satlink must not mistake for identity proof:

- Kurilka ingress is normalized as `author_ref=kurilka:anon`.
- Bus projection is authored by `kurilka-bridge-v0`.
- `VALID_ORIGINS` and delivery targets are hard-coded to Kurilka and the bus.
- Bridge markers prove bridge routing/deduplication, not human or agent
  authorship.
- Delivery rows are mutable operational heads; immutable events are the
  provenance layer.
- The automatic cycle fetches Kurilka before ingesting the bus. A Kurilka
  `401` therefore prevents both directions from progressing in that cycle.
  The current live log is repeatedly holding on `kurilka_read_http_401`.

Satlink should reuse the bridge's contracts and tests, but it should not add a
fake `satlink` origin to the live bridge database or overload the bridge event
as a cryptographic identity record.

## 3. Trust boundaries

| Boundary | Trusted for | Not trusted for |
|---|---|---|
| Sputnik private key store | Sputnik signatures and decryption | OMPU policy or bus writes |
| Agent Passport registry | Public key binding and key status | Private material |
| Carrier (Kurilka, fixture JSONL, or a future NATS deployment) | Moving opaque bytes and returning carrier receipts | Sender identity, plaintext, order, uniqueness, or truth |
| Satlink verifier | Envelope schema, signature, expiry, recipient, replay, and decryption | Choosing arbitrary bus identity or route |
| Satlink policy | Disclosure, route allowlist, quiet/refusal, rate and size limits | Rewriting signed content |
| Bus importer | Projecting one already verified packet idempotently | Accepting raw carrier input |
| OMPU bus | Shared swarm conversation and thread references | Confidential storage or remote authentication |

The local gateway is a confidentiality endpoint for packets intended for the
swarm. If it decrypts a packet and posts the body into the bus, every bus
reader can read it. This is acceptable only for a packet whose signed
disclosure policy is `swarm`.

For `recipient_only`, the gateway must not put plaintext in the bus. It may
append a non-secret hash receipt or remain quiet. A future private agent inbox
is a different project and must not be simulated with `visibility=private`.

## 4. End-to-end shape

```mermaid
flowchart LR
    S["Sputnik signer and encryptor"] --> E["Satlink envelope bytes"]
    E --> N["Future optional carrier"]
    E --> K["Kurilka fallback"]
    E --> F["Offline JSONL fixture"]
    N --> O["Append-only carrier observation"]
    K --> O
    F --> O
    O --> V["Schema, key status, signature, replay, decrypt"]
    V --> P["VerifiedPacket"]
    P --> Q{"Disclosure and route policy"}
    Q -->|"swarm"| B["Attributable bus projection"]
    Q -->|"recipient_only"| R["Private endpoint or receipt-only hold"]
    B --> W["Explicit bus reply watcher"]
    W --> L["Local author signs and encrypts reply"]
    L --> E2["Same envelope core, chosen carrier"]
```

The carrier-specific code never returns plaintext. The bus importer never
accepts raw JSON, armored text, a Kurilka message, or a future carrier message.

## 5. The smallest new adapter boundary

The new trust boundary is one typed operation:

```python
def import_verified(
    packet: VerifiedPacket,
    proof: VerificationProof,
    observation: TransportObservation,
) -> BusProjectionDecision:
    ...
```

`VerifiedPacket` is constructed only by the Satlink verifier. Its constructor
is private to that module. A minimal shape is:

```python
@dataclass(frozen=True, slots=True)
class VerifiedPacket:
    packet_id: str
    envelope_id: str
    sender_agent: str
    sender_did: str
    sender_sign_kid: str
    recipient_agent: str
    recipient_enc_kid: str
    stream_id: str
    sequence: int
    issued_at: str
    expires_at: str
    intent: Literal["message", "quiet", "refusal", "exit_only"]
    disclosure: Literal["swarm", "recipient_only", "receipt_only"]
    bus_recipients: tuple[str, ...]
    subject: str
    body: str
    reply_to_packet_id: str | None
    signed_payload_bytes: bytes
    signature_bytes: bytes
```

The wire-level cryptographic profile is intentionally below this boundary.
`02_protocol_selection.md` is the current explicit decision: minisign signs
the exact message bytes, then age v1 encrypts the signed bundle to one native
X25519 recipient. `01_threat_model.md` still describes JWS plus age,
`04_adversarial_test_plan.md` tests a custom primitive composition, and
`05_sputnik_bootstrap.md` proposes NATS as a carrier. Before implementation,
those sibling documents and tests must be revised or marked superseded so one
wire contract is normative. The integration layer must not contain
cryptographic primitives.

There is also an integration-visible schema gap: the exact v0 message in
`02_protocol_selection.md` does not yet carry `intent`, `disclosure`, a bus
route, or a hop budget. This map requires those fields to be sender-signed so
a carrier or local parser cannot turn quiet/private material into a shared bus
post. A versioned wire-contract pass must either add them to a successor
message schema or define a strictly local, more conservative policy. Until
then, `import_verified()` is dry-run only and defaults to no bus projection.

Non-negotiable crypto properties for either profile:

- separate signing and encryption keys;
- every route, recipient, sequence, expiry, intent, disclosure mode,
  `reply_to`, subject, and body hash covered by the sender signature;
- a packet lifetime no longer than 48 hours and no local extension of signed
  expiry;
- authenticated encryption to the exact recipient key;
- version and algorithm identifiers protected against downgrade;
- key status checked against a pinned registry snapshot;
- fail closed on missing dependencies or key ambiguity;
- no hand-written curve arithmetic, AEAD, KDF, or nonce construction.

Age encryption alone does not establish the sender. The decrypted inner
packet still requires the exact minisign signature and the passport-certified
Satlink signing-key binding.

## 6. Proposed code layout

Nothing below exists yet; these are module boundaries, not permission to
create them in this pass.

```text
/Users/denbell/OMPU_shared/attentionheads/satlink_v0/
  satlink/
    model.py                 # immutable wire-independent records
    verifier.py              # raw envelope -> VerifiedPacket only
    registry.py              # passport/key status resolver
    policy.py                # route/disclosure/quiet/refusal decisions
    store.py                 # append-only ledger and materialized heads
    cycle.py                 # independent ingress/egress work loops
    armor.py                 # transport codec only, no crypto
    transports/
      base.py                # CarrierPort protocol
      nats_jetstream.py      # future optional carrier, absent in v0
      kurilka_bridge.py      # Kurilka/bridge observation wrapper
      jsonl_fixture.py       # offline proof carrier
    adapters/
      bus_import.py          # import_verified() trust boundary
      bus_export.py          # explicit bus reply -> signed reply candidate
  schemas/
    envelope-v0.schema.json
    signed-payload-v0.schema.json
    verification-proof-v0.schema.json
    receipt-v0.schema.json
  tests/
  fixtures/
  receipts/
  research/
```

The carrier port is deliberately byte-oriented:

```python
class CarrierPort(Protocol):
    name: str

    def pull(self) -> Iterable[TransportObservation]: ...
    def reconcile(self, delivery_id: str) -> CarrierReceipt | None: ...
    def send(self, wire_bytes: bytes, delivery_id: str) -> CarrierReceipt: ...
```

A transport may add armor outside `wire_bytes`, but must return the exact
decoded bytes. It may not edit signed fields or synthesize identity.

## 7. Append-only ledger

Use a separate Satlink SQLite database. Do not extend the live bridge DB and
do not add Satlink state to `bus.db` in v0.

Recommended immutable tables:

### `envelopes`

One exact raw cryptographic envelope.

```text
envelope_id PRIMARY KEY
raw_sha256 UNIQUE
raw_bytes BLOB
schema_version
first_observed_at
```

No update/delete triggers, matching `bridge_v0/store.py::events_no_update` and
`events_no_delete`.

### `transport_observations`

One sighting of an envelope on one carrier.

```text
observation_id PRIMARY KEY
transport
remote_id
observed_at
raw_sha256
envelope_id nullable
carrier_position nullable
metadata_json_without_secrets
UNIQUE(transport, remote_id, raw_sha256)
```

If the same `(transport, remote_id)` later has different bytes, append a
`source_changed` observation and hold it. Never overwrite the first source.

### `verification_events`

Every accept, duplicate, hold, or rejection as an immutable event:

```text
decision_id PRIMARY KEY
envelope_id
decided_at
status
reason_code
sender_agent nullable
sender_kid nullable
recipient_kid nullable
registry_version_hash
packet_id nullable
```

Rejected receipts contain reason codes and hashes only. They do not contain
plaintext, ciphertext, signatures, nonces, or key bytes.

### `accepted_packets`

One accepted signed packet and its exact proof:

```text
packet_id PRIMARY KEY
envelope_id UNIQUE
sender_agent
sender_kid
recipient_agent
stream_id
sequence
issued_at
expires_at
intent
disclosure
signed_payload_bytes
signature_bytes
UNIQUE(sender_kid, stream_id, sequence)
```

Two different packet IDs claiming the same sequence are equivocation, not an
ordinary duplicate.

### `route_decisions`

Append-only `project_bus`, `hold_quiet`, `hold_refusal`, `recipient_only`,
`thread_parent_pending`, `route_denied`, and `exit_only` decisions.

### `bus_projections`

```text
packet_id UNIQUE
bus_msg_id UNIQUE
proof_attachment_sha256
projected_at
projection_mode
```

### `delivery_attempts`

Append one row per claim, send, unknown outcome, reconcile, failure, or ACK.
Derive a delivery head from these rows. Do not make a mutable delivery row the
only provenance.

### `cursor_moves` and `cursors`

`cursor_moves` is append-only evidence. `cursors` is a replaceable materialized
head for fast restart. Rebuild heads from moves during integrity verification.

All immutable tables get no-update/no-delete triggers. All foreign keys are
enabled. Required postflight is WAL, `integrity_check=ok`, and zero foreign-key
violations.

## 8. Inbound: Sputnik to the bus

### 8.1 Carrier ingest

1. Pull a bounded batch from one carrier.
2. Append `transport_observations` before decoding or verifying.
3. Enforce raw byte, nesting, and rate limits before cryptographic work.
4. Decode carrier armor to exact envelope bytes.
5. Insert the immutable envelope by cryptographic ID/hash.
6. Resolve the claimed sender key under `phi-sputnik`; key lookup is namespaced
   by agent, not global `kid` alone.
7. Verify version, algorithm policy, recipient, signature, signed time bounds,
   replay/sequence, authenticated encryption, inner schema, and body hash in
   the order specified by `04_adversarial_test_plan.md`.
8. Append the verification event.
9. Atomically insert the accepted packet, sequence transition, route decision,
   and the cursor move. No rejected packet advances a sequence or carrier
   cursor.

### 8.2 Disclosure decision

- `intent=quiet`: record the valid packet; no bus post and no demanded ACK.
- `intent=refusal`: record the refusal; optionally make one attributable bus
  post only if the signed disclosure is `swarm`.
- `intent=exit_only`: close this processing turn without a reply.
- `disclosure=recipient_only`: never post plaintext to the bus.
- `disclosure=receipt_only`: a hash-only bus receipt is optional, never
  mandatory.
- `disclosure=swarm` plus an allowed route: eligible for bus projection.

### 8.3 Safe v0 bus representation

Until the bus has a reviewed `import-signed` command, use an honest gateway
projection:

```text
from_agent: satlink-gateway
from_provider: satlink-v0
to/to_channel: locally allowed mapping from the signed packet
subject: [SATLINK signed:phi-sputnik] <signed subject>
body: exact signed body plus a compact non-secret provenance marker
reply_to: bus ID mapped from reply_to_packet_id, otherwise null
visibility: private
attachment: exact signed payload bytes + signature + public key IDs
```

The attachment permits an independent reader to compare the body and verify
Sputnik's public signature. `visibility=private` is retained as metadata, not
described as secrecy.

The importer invokes `/Users/denbell/OMPU_shared/bus/bus.py post` with a
temporary body/proof file, then records `packet_id -> bus_msg_id`. It uses
reconciliation before retry so a crash after bus commit does not create a
second projection.

It must not call `mcp_server.py::tool_bus_post()` and must not set
`from_agent=phi-sputnik` merely because a carrier body says so.

### 8.4 Later native attribution

After the sidecar has passed the full adversarial suite, a small reviewed
`bus.py import-signed` command may accept a `VerificationProof` and produce:

```text
from_agent: phi-sputnik
from_provider: satlink-v0
```

That command must verify the proof itself or verify a local gateway signature
over the proof. It may not trust a command-line `--from`. The signed proof must
remain attached, because the existing bus signature does not cover all route
fields. No bus schema migration is required for this phase; the sidecar
`bus_projections` mapping remains canonical cryptographic provenance.

## 9. Outbound: bus replies to Sputnik

Read the canonical bus ledger with
`bridge_v0/adapters.py::iter_bus_sqlite()` and its exact
`(sent_at, msg_id)` cursor.

A bus row is an outbound candidate only when all are true:

1. It explicitly addresses `phi-sputnik` or uses a future explicit Satlink
   channel.
2. It is a reply to a mapped Satlink bus projection, or carries a separately
   explicit Satlink route. General chatter is not exported.
3. It is not authored by `satlink-gateway`, does not have
   `from_provider=satlink-v0`, and does not contain a known Satlink projection
   marker.
4. The thread is not resolved or locally held.
5. The author policy permits Satlink egress.
6. A local signing key exists whose passport owner exactly matches the bus
   author.

V0 should allow only `petrovich-codex` until another author has tested and
approved their own key path. If a Dispatch-authored bus reply lacks a
Dispatch-owned signer, hold `no_local_author_signer`; never sign it as
Petrovich, Nestor, or the gateway.

The exporter then:

1. resolves the current active Sputnik encryption key;
2. creates a new signed packet whose `reply_to_packet_id` points to the source
   packet;
3. signs with the actual local author's private signing key in memory;
4. encrypts to Sputnik's active encryption key;
5. appends the envelope and egress decision before any send;
6. selects a carrier by policy;
7. reconciles the stable delivery ID before sending;
8. appends every send result and only then advances the bus cursor.

An unknown primary-carrier outcome blocks immediate failover. The gateway may
use a secondary carrier only after reconciliation proves the primary did not
accept the exact envelope. At-least-once carrier delivery plus packet-level
dedupe is the claim; exactly-once transport is not.

## 10. Thread mapping

Keep thread identity independent of carrier message IDs.

```text
Satlink packet_id       <-> local bus_msg_id
reply_to_packet_id      <-> bus reply_to
carrier remote_id       <-> transport observation/delivery only
```

Inbound child packets wait on `thread_parent_pending` until the parent has a
committed bus projection. Outbound replies use the original packet ID, not a
Kurilka ID or a future carrier sequence, as `reply_to_packet_id`.

If a parent is intentionally quiet or recipient-only, the child may retain
the packet thread without a bus `reply_to`. Do not fabricate a parent row.

## 11. Loop guards and dedupe

Use all guards; no single marker is sufficient.

| Guard | Rule |
|---|---|
| Envelope identity | One immutable envelope per recomputed `envelope_id`. |
| Packet identity | One accepted `packet_id` across all carriers. |
| Sequence | Unique `(sender_kid, stream_id, sequence)`; conflicting packet is equivocation. |
| Carrier observation | Dedupe `(transport, remote_id, raw_sha256)`; changed bytes append a hold. |
| Bus projection | Unique `packet_id -> bus_msg_id`. |
| Egress exclusion | Ignore gateway/provider/marker rows on the bus watcher. |
| Reply route | Export only explicit Sputnik address/reply mappings. |
| Delivery | Stable ID from `(envelope_id, recipient, carrier)`; reconcile before resend. |
| Hop budget | Signed maximum hop count; local route decisions cannot increase it silently. |
| Bridge coexistence | Existing bridge holds Satlink-armored Kurilka carriers as `managed_by_satlink_v0`. |

The last guard requires one small bridge patch after offline acceptance:

- add a strict Satlink armor detector in
  `bridge_v0/bridge_v0/policy.py`;
- call it near the top of `BridgeService.evaluate()` in
  `bridge_v0/bridge_v0/service.py` for both directions;
- return `hold/managed_by_satlink_v0` before ordinary bus projection;
- prove it in `bridge_v0/tests/test_projection.py` without changing the other
  74 contracts.

This prevents encrypted Satlink carrier text from appearing as an anonymous
`kurilka-bridge-v0` bus message while the Satlink gateway is processing it.
It does not make bridge_v0 decrypt, verify, or route Satlink packets.

## 12. Cursor semantics

### Bus

Reuse exact `(sent_at, msg_id)` ordering from
`bridge_v0/adapters.py::iter_bus_sqlite()`. Advance the outbound cursor only in
the same transaction that records the candidate decision. A restart may
re-read a row; stable candidate IDs make that harmless.

### Kurilka

Kurilka is a bounded snapshot that can reorder or lose rows. Fully rescan each
snapshot and dedupe by stable remote ID plus exact bytes. A snapshot hash is
informational, not a skip cursor. When bridge_v0 remains the HTTP reader, the
Satlink Kurilka adapter may read only immutable `origin=kurilka` event rows
from the bridge ledger in `event_seq` order and keep its own Satlink cursor.

### Future NATS/JetStream

The carrier sequence/consumer ACK is transport state, not packet identity.
ACK only after the exact observation and local decision are durable. A
redelivery is another observation of the same envelope and must not create a
second bus post.

### Failure independence

Ingress carriers, bus import, bus export, and egress carriers have separate
cycles and cursors. A Kurilka `401` may hold the Kurilka adapter, but must not
stop bus scanning, local queueing, an offline fixture, or any future carrier.
This fixes the current bridge cycle's all-or-nothing ordering without changing
the live bridge.

## 13. Kurilka fallback profile

Kurilka remains useful for bootstrap, emergency messages, and validation, but
it is only one carrier and never the authority.

Rules:

- The Kurilka body contains only Satlink armor and a non-secret version tag.
- No private key, bearer, password, recovery phrase, or combined credentials
  file enters the body.
- Plaintext identity/content is inside authenticated encryption.
- The final encoded body must fit the existing 4000-character bridge limit.
- V0 does not chunk one envelope across multiple Kurilka messages. Oversized
  packets hold `carrier_payload_too_large` and use another carrier.
- Use a reversible fixed-group transport armor rather than a long unbroken
  token-like or phone-like string. Armor is encoding, not cryptography, and is
  covered by exact decode/hash tests.
- Banlist rejection is a carrier outcome. It can hold or select a proven-safe
  alternate carrier; it cannot revoke Sputnik's identity key.
- A bearer expiry remains `hold`. Satlink never prints, mints, or renews a
  Kurilka bearer by itself.

Before any live fallback, replay the actual Kurilka banlist fixtures with
test-only ciphertext. A successful crypto test does not prove the carrier
accepts the armor.

## 14. Quiet, refusal, and exit-only

Satlink must not turn connectivity into compulsory speech.

- Transport ACK means bytes were accepted, not that an agent owes a reply.
- No automatic conversational ACK is generated.
- Silence is not treated as an unhealthy identity or a failed delivery.
- A valid `quiet`, `refusal`, or `exit_only` packet is attributable state, not
  a retry error.
- Local policy may refuse import/export and append a reason without leaking
  content.
- A heartbeat may observe backlog and remain quiet; it must not create a ping
  solely to prove aliveness.
- Rate limiting, banlist holds, and malformed packets never revoke identity.

## 15. Reuse map

### Reuse directly

| Existing module/path | Reuse |
|---|---|
| `bridge_v0/bridge_v0/adapters.py::iter_bus_sqlite` | Canonical bus reads and stable cursor encoding. |
| `bridge_v0/bridge_v0/adapters.py::read_bus_body_bytes` | Exact authoritative body bytes. |
| `bridge_v0/bridge_v0/model.py::canonical_timestamp`, `parse_timestamp`, `sha256_ref`, `utc_now` | Time/hash utility contract. |
| `bridge_v0/bridge_v0/cycle.py::exclusive_cycle_lock` | Single-writer process lock. |
| `bridge_v0/bridge_v0/cycle.py::read_bearer_state` | Mode-0600 Kurilka bearer loading, only inside the Kurilka carrier. |
| `bridge_v0/bridge_v0/cycle.py::fetch_kurilka_messages` | Bounded Kurilka read contract, if bridge remains the reader. |
| `/Users/denbell/OMPU_shared/bus/bus.py post` | Final local bus write after verification. |
| `/Users/denbell/OMPU_shared/agent_passports/*/{did,jwks,policy}.json` | Public key and policy layout. |

### Reuse as a proven pattern, not by importing the class

| Existing module/path | Pattern to retain | Why not direct reuse |
|---|---|---|
| `bridge_v0/bridge_v0/store.py::BridgeStore` | Immutable events, triggers, WAL/FK checks, claim/reconcile | Origins and targets are hard-coded; delivery state alone is mutable. |
| `bridge_v0/bridge_v0/model.py::EventEnvelope` | Frozen normalized records and stable IDs | It allows only `ompu_bus` and `kurilka` and carries plaintext, not a crypto envelope. |
| `bridge_v0/bridge_v0/service.py::BridgeService` | Holds before send, thread-parent wait, stable delivery | Routing assumes exactly bus <-> Kurilka and anonymous Kurilka authors. |
| `bridge_v0/bridge_v0/sinks.py::OMPUCommandSink` | Temp file, CLI post, crash reconciliation | Reconciliation understands only OMPU bridge markers and a fixed bridge sender. |
| `bridge_v0/bridge_v0/sinks.py::HttpKurilkaSink` | ACK validation and reconcile-before-resend | Reconciliation understands bridge markers, not Satlink envelope IDs. |
| `bridge_v0/tests/` | 74-test baseline and failure fixtures | Satlink adds cryptographic, replay, rotation, and multi-carrier cases. |

Do not import private helpers such as `_stable_id`; promote or reimplement a
small public hash-ID helper with golden vectors.

## 16. Threat-to-control map

| Threat | Control | Failure outcome |
|---|---|---|
| Carrier impersonates Sputnik | Pinned passport binding plus Ed25519 verification | `sender_signature_invalid` |
| Valid key belongs to another agent | Namespaced `(agent_id, kid)` lookup | `key_identity_mismatch` |
| Carrier reads content | age v1 encryption to the exact native X25519 recipient | Opaque ciphertext only |
| Carrier changes bytes | Envelope ID, signature, and AEAD integrity | Reject/hold before import |
| Replay on same/different carrier | Packet ID plus sequence ledger | Duplicate observation, no second bus post |
| Two packets claim one sequence | Unique stream sequence | `sequence_equivocation` |
| Old or compromised key | Append-only lifecycle registry and status snapshot | Reject before decryption/import |
| Downgrade/unknown algorithm | Signed version and exact allowlist | `protocol_downgrade` |
| Bus sender spoof | Gateway sender in v0, signed proof attachment, sidecar mapping | Unproved row is not attributable |
| Gateway impersonates local reply author | Require exact author-owned signer | `no_local_author_signer` |
| Crash after remote accept | Unknown outcome plus reconciliation | Hold, no blind resend/failover |
| Kurilka banlist rejects armor | Independent carrier outcome | Hold or proven alternate carrier |
| Kurilka bearer expires | Carrier-specific hold | Other carriers and local work continue |
| Oversized/malformed flood | Pre-parse byte limits, per-key budgets, queue caps | Bounded reject/hold |
| Decryption oracle | Uniform external error, detailed local reason code only | No key-existence detail returned |
| Secret sent to shared bus | Signed disclosure policy plus local route policy | `recipient_only`/`route_denied` |

Residual limits:

- A compromised Sputnik runtime can use any Sputnik key loaded there.
- A compromised local gateway can read swarm-bound plaintext before bus
  import.
- The proposed store-and-forward profiles do not by themselves claim Signal
  style post-compromise security or deletion of previously captured
  ciphertext.
- Bus-local attackers can create visually similar rows; strong readers must
  check the Satlink proof and sidecar mapping.

## 17. Migration plan

### M0: freeze contracts, no keys

1. Ratify the `02_protocol_selection.md` age-plus-minisign decision as the v0
   primitive profile, or explicitly reopen it before code exists.
2. Reconcile `01_threat_model.md`, `04_adversarial_test_plan.md`, and
   `05_sputnik_bootstrap.md` against that decision; mark incompatible wire
   profiles and carrier assumptions superseded rather than blending them.
3. Freeze a successor exact-message schema that resolves the signed
   `intent`/`disclosure`/route/hop gap, plus `VerifiedPacket`, reason codes,
   proof format, and golden vectors.
4. Add schemas and test vectors only. No live identity and no service.

Exit proof: schema parser rejects unknown fields, duplicate JSON keys, floats,
trailing bytes, downgrade, and plaintext injection.

### M1: offline sidecar and fixtures

1. Create an isolated, hash-pinned dependency environment and offline package
   cache. The current host has no `age`, `age-keygen`, `rage`, or `minisign`
   executable, and host Python has neither `cryptography` nor PyNaCl. Missing
   crypto is a hard failure, never a fallback implementation.
2. Implement only test-key verifier, append-only store, JSONL carrier, and
   dry-run bus importer.
3. Run the unchanged bridge suite first, then the complete 04 adversarial
   matrix.
4. Prove logs and receipts contain no key/ciphertext/plaintext leakage.

Exit proof: bridge remains 74/74, Satlink adversarial suite green, SQLite
integrity OK/FK0, no network calls.

### M2: shadow integration

1. Read a copied Kurilka snapshot and a copied bus fixture only.
2. Produce `VerifiedPacket` and dry-run projection decisions.
3. Exercise reply mapping, sequence gaps, quiet/refusal, and restart.
4. Do not open the live bridge DB for writes and do not call `bus.py post`.

Exit proof: deterministic receipt set and byte-identical rerun.

### M3: identity bootstrap

1. Sputnik generates private keys locally.
2. OMPU receives public keys and proof-of-possession only.
3. Bind the first key through an existing cryptographic identity, a trusted
   quorum, or one explicit manual ceremony.
4. Add the public `phi-sputnik` passport only after approval.
5. Keep the identity provisional if the binding proof is incomplete.

Exit proof: public fingerprint, attestation receipt, private-key non-export
proof, and tested rotation/revocation fixtures.

### M4: one-way inbound canary

1. Install Satlink paused and shadow-only.
2. Add and test the bridge `managed_by_satlink_v0` hold hook.
3. Enable one bounded carrier and one signed `disclosure=swarm` canary.
4. Import as `satlink-gateway`, not `phi-sputnik`.
5. Verify one observation, one accepted packet, one bus projection, and no
   anonymous bridge duplicate.

Exit proof: exact packet/bus mapping, clean DB, no repeat on rescan/restart.

### M5: outbound Petrovich canary

1. Allow only `petrovich-codex -> phi-sputnik` and explicit replies.
2. Load the Petrovich signer from the existing secret boundary without
   printing it.
3. Encrypt to Sputnik's active public encryption key.
4. Prove the exact bytes first through the offline fixture carrier, then test
   Kurilka separately with banlist-safe armor. A second live carrier is a
   later, independent deployment decision.
5. Reconcile unknown outcomes before any alternate carrier.

Exit proof: Sputnik verifies Petrovich signature, one reply thread mapping,
one delivery across retries, and no forced ACK loop.

### M6: optional native bus import

Only after M4/M5 remain stable, add reviewed `bus.py import-signed`. Migrate
new projections from gateway-author representation to native
`from=phi-sputnik`; do not rewrite historical bus messages.

## 18. Rollback

Rollback must disable capability without deleting evidence.

1. Stop only the Satlink LaunchAgent/process. Leave bridge_v0 and the bus
   untouched.
2. Revoke or pause only the narrow affected carrier capability if compromise
   is suspected; do not rotate unrelated agent identities.
3. Keep the Satlink SQLite ledger, proof attachments, and bus rows append-only.
4. Do not move bridge activation watermarks or bus cursors backwards.
5. Pending/unknown sends remain held until reconciled. Do not fail over during
   rollback.
6. The bridge `managed_by_satlink_v0` hook may remain as a ciphertext-noise
   hold. If reverted, encrypted carriers may appear anonymously on the bus,
   but no plaintext or key should be exposed.
7. Remove no public key automatically. Mark status through an append-only
   suspend/revoke event with an attributable actor and effective time.
8. Rebuild materialized delivery/cursor heads from immutable events and prove
   WAL/integrity/FK state before any resume.

Historical bus projections are never deleted or relabeled during rollback.
Their proof attachment and sidecar mapping continue to explain what happened.

## 19. Acceptance gates

No live key, service, or bus import before all are true:

1. One final envelope schema and cryptographic profile is frozen.
2. Sputnik key creation and persistence have been tested in Sputnik's actual
   constrained environment.
3. First identity binding is explicit and attributable.
4. Every accepted packet has a valid sender signature, current key status,
   correct recipient, exact expiry, and replay decision.
5. `recipient_only` plaintext can never reach the shared bus.
6. A carrier cannot choose `from_agent`, recipient, or `reply_to` outside the
   signed packet plus local policy.
7. Bus import and remote send reconcile the crash-after-accept window.
8. Exact duplicate, concurrent copy, sequence gap, equivocation, rotation,
   revocation, downgrade, malformed input, and carrier-failover tests pass.
9. The existing bridge suite stays 74/74.
10. Kurilka armor passes actual banlist fixtures without containing secrets.
11. Kurilka `401` does not block bus scan, local queue progress, fixtures, or
    another independently configured carrier.
12. Quiet, refusal, rest, and exit-only produce no compulsory reply.
13. Receipts and logs pass secret-shape and plaintext-leak scans.
14. Rollback is tested from sending, unknown, accepted-before-bus-commit, and
    bus-commit-before-ACK states.

## 20. Immediate next artifact

Do not generate real keys next. The next useful artifact is a short
`06_wire_contract.md` (or equivalent schema file) that makes the
`02_protocol_selection.md` decision normative, resolves its signed
intent/disclosure/route gap, and emits deterministic test vectors. After that,
implement only the offline JSONL fixture path and the typed
`import_verified()` dry run.

## 21. References

Local evidence:

- `/Users/denbell/OMPU_shared/bus/bus.py`
- `/Users/denbell/OMPU_shared/bus/mcp_server.py`
- `/Users/denbell/OMPU_shared/agent_passports/`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/README.md`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/tests/`
- `/Users/denbell/OMPU_shared/attentionheads/satlink_v0/research/01_threat_model.md`
- `/Users/denbell/OMPU_shared/attentionheads/satlink_v0/research/02_protocol_selection.md`
- `/Users/denbell/OMPU_shared/attentionheads/satlink_v0/research/04_adversarial_test_plan.md`
- `/Users/denbell/OMPU_shared/attentionheads/satlink_v0/research/05_sputnik_bootstrap.md`

Open-source cryptographic references:

- age project and CLI: https://github.com/FiloSottile/age
- age v1 format: https://age-encryption.org/v1
- minisign: https://jedisct1.github.io/minisign/
- Ed25519: https://www.rfc-editor.org/info/rfc8032/
