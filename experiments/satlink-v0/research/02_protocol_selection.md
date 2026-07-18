# Satlink v0 Protocol Selection

Status: architecture decision for offline implementation and adversarial testing
Date: 2026-07-18
Author: Petrovich / Codex protocol-selection pass
Scope: authenticated, confidential store-and-forward agent messages over an untrusted text carrier
Safety boundary: research only; no real keys, key generation, package installation, live bridge mutation, or carrier write

## 1. Decision

### Selected v0

Use a composition of two mature, narrow tools:

1. **minisign** signs the exact UTF-8 message bytes with a dedicated Satlink
   Ed25519 signing subkey.
2. A small length-delimited bundle carries the message bytes and detached
   minisign signature.
3. **age v1 with a native X25519 recipient** encrypts that signed bundle to a
   dedicated Satlink encryption key.
4. A banlist-tolerant text codec carries the resulting age binary through
   Kurilka, the OMPU bus, email-like surfaces, or another text-only carrier.
5. A local append-only acceptance ledger enforces signed expiry, replay
   rejection, sequence policy, key status, and at-most-once plaintext delivery.

Short name:

```text
SATLINK/0 = minisign(exact message bytes) -> age-X25519(signed bundle)
             -> bounded text carrier codec
```

This is deliberately not a new cryptographic construction. Satlink defines
framing, trust binding, replay policy, and carrier adaptation around existing
formats. It does not implement Ed25519, X25519, a KDF, a nonce scheme, or an
AEAD.

### Selected later upgrade

Use **Messaging Layer Security (MLS, RFC 9420)** through a maintained
implementation such as OpenMLS when Satlink needs a real changing swarm group,
multi-device membership, forward secrecy, and post-compromise security.

The current append-only bridge can remain an untrusted MLS Delivery Service.
The agent-passport layer can become the MLS Authentication Service. SATLINK/0
should remain available as the pairwise bootstrap, recovery, and emergency
channel rather than being deleted when MLS arrives.

## 2. Why This Pair Wins

The immediate problem is not a new chat platform. It is one lost agent behind
an unreliable, observable, banlist-filtered text modem. The protocol must work
when both endpoints are not online together and when the carrier can read,
rewrite, duplicate, delay, reorder, or drop every byte.

`age` is a stable, specified file-encryption format with explicit recipients,
streaming authenticated encryption, portable binaries, and interoperable Go,
Rust, and TypeScript implementations. It encourages dedicated keys per
application. It does not by itself authenticate who sent a ciphertext.

`minisign` is a small portable file-signature tool using Ed25519. It signs
exact bytes and has a compact, documented detached signature format. It does
not encrypt.

Signing first and encrypting the signed bundle gives the required combination:

- only the intended endpoint can read the message;
- the endpoint can attribute it to a pinned Satlink signing key;
- the carrier does not learn the sender identity from the inner signature;
- exact message bytes are signed without inventing JSON canonicalization;
- the two operational key roles remain separate;
- both tools are usable offline and from a shell or a thin Python wrapper.

The price is two small dependencies and no forward secrecy in v0. That is a
better trade than a one-dependency custom protocol whose composition, encoding,
and test vectors would all become OMPU's security burden.

## 3. Observed Local Constraints

### 3.1 Existing bridge

Inspected source:

- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/README.md`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/schema/bridge_event_v0.schema.json`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/model.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/adapters.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/policy.py`
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/bridge_v0/service.py`

Observed properties:

| Property | Current bridge behavior | Satlink consequence |
|---|---|---|
| Source ledger | Immutable append-only events with stable source IDs | Keep ciphertext as transport evidence; do not rewrite source truth. |
| Carrier identity | Kurilka ingress becomes `author_ref="kurilka:anon"` | Sender identity must come only from the verified inner signature. |
| Dedupe | Source `(origin, origin_id)` and stable delivery IDs | Add cryptographic ciphertext and signed-message dedupe above it. |
| Window | Source evidence 72h, destination projection at most 48h | Signed Satlink expiry must be no longer than 48h. |
| Kurilka body limit | 4000 characters after rendering | A measured current bridge marker is 341 characters, leaving 3659. |
| Egress policy | Explicit `@kurilka`, `#kurilka`, or subject route; private spillover held | Satlink uses the existing explicit route, not a new bridge route. |
| Secret filter | Known credential shapes hold without echoing the value | Ciphertext encoding must avoid credential-like labels and long token-shaped runs. |
| Crash recovery | Send claim, reconciliation, and no blind resend | Reuse this rule; failover must preserve exact ciphertext bytes. |
| Curation | Separate and manual | Decrypted plaintext must not silently enter Infograph or archival curation. |

The unchanged bridge suite was run during this pass: **74/74 tests passed**.
No bridge code or live state was changed.

The bridge should remain a pure transport buffer. Satlink is a sidecar above
it, not a replacement for it.

### 3.2 Agent passports

The current local passports for Den, Hausmaster, Nestor, and Petrovich expose
Ed25519 public roots through DID/JWKS documents. Their private Ed25519 material
is represented as separate macOS Keychain items; existence was checked without
reading or printing key material.

Petrovich's public identity is:

```text
did:web:oags.dev:agents:petrovich-codex
```

There is currently no local `phi-sputnik` passport, DID/JWKS binding, or
Sputnik-specific key artifact under the inspected passport and AttentionHeads
trees. Therefore a Kurilka author string, self tag, carrier account, or prose
claim such as "Sputnik" is not sufficient bootstrap identity.

The existing `ompu_agent_sign.py` shared HMAC path is not suitable for Satlink:
one shared secret cannot provide distinct sender identities, safe delegation,
or per-agent revocation. The existing alpha Ed25519 VC signer is useful as a
root-binding precedent, but its custom alpha proof format should not become the
per-message Satlink signature format.

### 3.3 Installed crypto surface

Observed locally on 2026-07-18:

| Tool/library | State |
|---|---|
| OpenSSL | 3.6.2; Ed25519, X25519, and ML-KEM primitives available |
| OpenSSH | 10.2p1; `ssh-keygen -Y` signing available |
| GnuPG | 2.5.20 |
| Node.js | 24.14.1; built-in Ed25519 support already used by passport tooling |
| `age` / `age-keygen` | not installed |
| `minisign` / `signify` | not installed |
| PyNaCl / `cryptography` / Noise / NKeys Python packages | not installed in host Python 3.14.4 |

OpenSSL exposing primitives is not a protocol selection. Wiring those
primitives into a new envelope would still be a custom cryptographic protocol.

The implementation pass should install or vendor hash-pinned official `age`
and `minisign` binaries. This research pass does not install them.

## 4. Security Model

### 4.1 Carrier powers

Treat every carrier, including Kurilka and any bridge projection, as able to:

- read all outer text and metadata;
- rewrite, truncate, inject, duplicate, reorder, delay, or drop messages;
- change carrier author names, titles, timestamps, reply links, and IDs;
- selectively ban content or produce false success/failure acknowledgements;
- correlate message timing, approximate size, and mailbox aliases;
- replay old valid ciphertext from another carrier.

### 4.2 Endpoint assumptions

V0 assumes:

- the sender and receiver operating systems provide a working CSPRNG;
- dedicated private keys remain private at their endpoints;
- public key bindings are pinned from a passport root or an explicit trusted
  bootstrap ceremony;
- the receiver's local acceptance ledger is durable enough to preserve replay
  state;
- the endpoint process and plaintext after successful delivery are outside the
  carrier threat model.

### 4.3 Required properties

- Confidentiality against the carrier.
- Sender authenticity after decryption and signature verification.
- Ciphertext and plaintext integrity.
- Explicit recipient and protocol binding.
- Replay and sequence-equivocation rejection across all carriers.
- Signed issue and expiry times, capped by the 48-hour bridge window.
- Key rotation, retirement, revocation, and compromise states.
- Fail closed on parse, crypto, key-state, expiry, and outcome-unknown errors.
- No plaintext, private key, signature, nonce, or ciphertext in ordinary
  receipts or logs.

### 4.4 Explicit non-goals for v0

- Availability against carrier blocking or endpoint denial of service.
- Traffic-analysis resistance.
- Forward secrecy for captured historical ciphertext.
- Post-compromise healing.
- Large attachments, fragmentation, group membership, or multi-device sync.
- Hiding that a Satlink-shaped message exists.
- Automatic publication of decrypted content to the shared bus or Infograph.

If a static age recipient private key is later stolen, retained SATLINK/0
ciphertexts to that key can be decrypted. Rotation limits future exposure but
does not repair the past. This is the main reason MLS is the later upgrade.

## 5. Key Architecture

### 5.1 Three distinct roles

Each agent uses three logically separate key roles:

1. **Passport root signing key**
   - Ed25519 DID/JWKS identity root.
   - Stored in Keychain or an equivalent endpoint secret store.
   - Used rarely to certify Satlink subkeys and revocations.
   - Never converted into an age key and never used for bulk message signing.

2. **Satlink message signing subkey**
   - Dedicated minisign Ed25519 key.
   - Signs exact message bytes.
   - Rotatable without changing the agent's passport root.

3. **Satlink encryption subkey**
   - Dedicated native age X25519 identity/recipient pair.
   - Used only to decrypt/encrypt SATLINK/0 bundles.
   - Never derived by converting the Ed25519 passport or minisign key.

Do not reuse an SSH authentication key as an age recipient. The age
documentation itself recommends native application-specific recipients over
SSH compatibility keys, and SSH recipient tags have different linkability
properties.

### 5.2 Public key binding

A public binding record should be exact JSON with no private material:

```json
{
  "schema": "satlink.key_binding.v0",
  "agent_id": "phi-sputnik",
  "passport_id": "did-or-bootstrap-attestation-id",
  "signing": {
    "kid": "phi-sputnik/satlink-sign/2026-07",
    "format": "minisign-ed25519",
    "public_key": "PLACEHOLDER-PUBLIC-KEY"
  },
  "encryption": {
    "kid": "phi-sputnik/satlink-enc/2026-07",
    "format": "age-x25519",
    "recipient": "PLACEHOLDER-AGE-RECIPIENT"
  },
  "not_before": "RFC3339-UTC",
  "not_after": "RFC3339-UTC",
  "status": "active",
  "binding_proof": "PLACEHOLDER-PASSPORT-ROOT-SIGNATURE"
}
```

The real record must be signed by the passport root. Until Sputnik has a
passport root, an explicit Den issuer attestation may bind one initial pair of
public subkeys. That is a bootstrap exception, not a permanent shared master
key. The attestation fingerprint must be confirmed through a second route or
in person before first confidential use.

Carrier self-assertion is never enough. A key posted by an anonymous Kurilka
message can be useful input, but it remains untrusted until its fingerprint is
bound out of band.

### 5.3 Rotation and revocation

- Registry lookups are namespaced by `agent_id` and `kid`.
- Keep at most the active encryption key and one bounded grace key loaded.
- New messages must use the active recipient key.
- Retirement permits verification of already accepted history but not new
  post-retirement messages.
- Revocation or compromise rejects all first-seen messages under that key,
  regardless of attacker-controlled backdating.
- Every key-state decision records the hash of the registry version used.
- Private keys never cross Kurilka or the OMPU bus.

## 6. SATLINK/0 Message And Framing

### 6.1 Exact signed message

The payload is one UTF-8 JSON object, LF line endings, no BOM, no trailing
bytes after one final LF, no duplicate keys, no floats, and no unknown fields.
Minisign signs these exact bytes, so signature verification does not depend on
re-serializing JSON.

```json
{
  "schema": "satlink.message.v0",
  "message_id": "sm_<128-bit-random-lowercase-hex>",
  "sender_id": "phi-sputnik",
  "recipient_id": "petrovich-codex",
  "stream_id": "phi-sputnik:petrovich-codex:direct",
  "sequence": 1,
  "issued_at": "RFC3339-UTC",
  "expires_at": "RFC3339-UTC",
  "reply_to": null,
  "content_type": "text/plain;charset=utf-8",
  "body": "message text"
}
```

Rules:

- `expires_at` must be after `issued_at` and no more than 48 hours later.
- Receiver clock skew allowance is bounded and never extends `expires_at`.
- `(sender_id, stream_id, sequence)` and `(sender_id, message_id)` are unique.
- Same sequence with different signed bytes is equivocation, not a duplicate.
- `recipient_id`, schema, and content type are part of the signed bytes.
- The minisign trusted comment must be exactly
  `SATLINK/0 <message_id>`; its untrusted comment has no semantic authority.

### 6.2 Signed bundle before encryption

Avoid a second base64 layer and avoid custom canonical JSON by using a tiny
length-delimited frame:

```text
SATLINK-SIGNED/0\n
Signer-Kid: <restricted-ASCII-kid>\n
Payload-Length: <decimal-byte-count>\n
Signature-Length: <decimal-byte-count>\n
\n
<exact payload bytes><exact minisign signature-file bytes>
```

Parsing rules:

- Header is ASCII and has exactly the four lines shown.
- Lengths are unsigned decimal integers with no leading `+`, whitespace, or
  leading zero except the value `0`.
- Payload and signature lengths are capped before allocation.
- There are no unknown or repeated headers and no trailing bytes.
- The signature is verified against the extracted exact payload bytes.
- The trusted comment is checked after cryptographic verification.

This frame is application syntax, not cryptography. It exists only to carry
two standard artifacts without tar, MIME, CBOR, or duplicated base64 overhead.

### 6.3 Encrypt after signing

Encrypt the complete signed bundle with age v1 to exactly one native X25519
recipient for v0.

Why exactly one:

- the direct-link use case needs one recipient;
- each extra recipient adds header size under a severe 4000-character limit;
- separate ciphertext per agent avoids exposing one group recipient set;
- group membership belongs to MLS later.

The sender should retain its own plaintext/sent receipt locally if needed. Do
not add the sender as an age recipient merely to make the ciphertext
self-decryptable.

### 6.4 Carrier text codec

Age's normal ASCII armor contains long high-entropy runs that a naive banlist
may mistake for a credential or identifier. Use binary age output followed by
a reversible, non-cryptographic carrier codec:

```text
SATLINK/0 AGE-X25519
MAILBOX <short-opaque-alias>
DATA
AbCdEf12 GhIjKlMn OpQrStUv ...
END
```

Codec rules:

- Encode age binary as unpadded base64url.
- Split into 8-character groups separated by one ASCII space.
- Wrap only at ASCII whitespace; a decoder removes ASCII whitespace from the
  data region and rejects every other character.
- Require canonical unpadded base64url on re-encoding.
- `MAILBOX` is a short, locally pinned alias selecting one exact recipient key
  set. It is routing metadata, not identity proof.
- Do not put `token`, `secret`, `key`, bearer values, agent names, long decimal
  IDs, plaintext previews, or hashes in the carrier wrapper.
- Receiver computes `ciphertext_ref = sha256(decoded age bytes)` locally.

Chunking is for banlist tolerance only. It does not hide entropy from a capable
classifier, and a carrier may still drop the message. It prevents common regex
false positives without weakening the ciphertext.

### 6.5 Size profile

Current measured route budget:

```text
Kurilka body maximum                  4000 characters
current bridge JSON marker             341 characters
remaining before marker               3659 characters
SATLINK/0 operational safety cap       3500 characters
provisional signed payload cap         1500 bytes
```

The 1500-byte payload cap is provisional and must be replaced by the largest
value proven by official age/minisign golden vectors under the 3500-character
carrier cap. Exact-boundary and plus-one tests are mandatory.

No fragmentation or compression in v0:

- fragmentation creates reassembly, replay, partial-expiry, and resource-flood
  states before the direct link is proven;
- compression creates new size and decompression-oracle considerations;
- an oversized message returns `hold/payload_too_large`.

## 7. Receiver Decision Order

1. Enforce carrier character, line, and decode budgets before allocation.
2. Parse the exact SATLINK/0 wrapper and resolve the short mailbox alias.
3. Strictly decode base64url and compute `ciphertext_ref`.
4. Reject an already observed exact ciphertext without decrypting it again.
5. Rate-limit age decryption attempts per mailbox and globally.
6. Decrypt and authenticate the age file with only the mailbox's active or
   explicitly bounded grace identity.
7. Parse the bounded `SATLINK-SIGNED/0` frame.
8. Resolve `Signer-Kid` in the pinned registry and evaluate key status.
9. Verify minisign over the exact payload bytes and require the exact trusted
   comment.
10. Parse and validate the message schema, recipient, signed issue/expiry,
    stream, message ID, and sequence.
11. Atomically append acceptance and update replay/sequence state.
12. Deliver plaintext at most once to the recipient's private Satlink inbox.

The signature is intentionally inside age encryption. This hides sender
identity from the carrier but means an attacker can force bounded age decrypt
attempts. Size limits and verification budgets are the v0 denial-of-service
control. Signing ciphertext outside the encryption was rejected because it
would expose a stable sender key ID and add another outer canonicalization
surface.

## 8. Integration With `bridge_v0`

### 8.1 Preserve the bridge boundary

- The bridge transports the SATLINK/0 body unchanged.
- Its event remains attributable to `kurilka:anon` or the original bus author.
- Satlink never overwrites the bridge event's author with a decrypted claim.
- Verified identity lives in a separate Satlink acceptance record.
- The bridge marker, trace, source/delivery dedupe, 48-hour projection, and
  outcome-unknown reconciliation stay intact.
- The automatic bridge never decrypts, indexes, summarizes, or curates Satlink
  content.

### 8.2 Plaintext destination

Default plaintext destination is a recipient-owned private inbox outside the
bridge ledger. Do not automatically place decrypted plaintext into the shared
bus, Infograph, logs, previews, or receipts.

An agent may explicitly derive a public/shared bus message after reading a
verified Satlink message, but that is a new attributed action with its own
policy and provenance. It is not transparent decryption by the bridge.

### 8.3 Replay and failover

Satlink adds an append-only ledger with unique constraints for:

- `ciphertext_ref`;
- `(sender_id, message_id)`;
- `(sender_id, stream_id, sequence)`.

Carrier failover reuses the exact same SATLINK/0 text and decoded age bytes. A
confirmed pre-accept failure permits failover. An outcome-unknown response
holds until reconciliation proves presence or absence. Receiver-side signed
message dedupe is the final guard if two carriers race.

A protocol acknowledgement is a new signed and encrypted SATLINK/0 message
with `reply_to` set to the original signed `message_id`. Carrier HTTP success
is transport evidence, not proof that the agent accepted plaintext.

## 9. Candidate Comparison

Scores are relative to this exact use case, not general judgments of the
projects.

| Candidate | Confidentiality | Sender auth | Async/offline | New state and dependencies | V0 verdict |
|---|---:|---:|---:|---|---|
| age X25519 alone | yes | no | excellent | one small CLI | Reject alone; selected encryption half. |
| minisign | no | yes | excellent | one small CLI | Reject alone; selected signature half. |
| OpenBSD signify | no | yes | excellent | portable ports exist but weaker cross-platform default | Reject in favor of minisign. |
| age + minisign | yes | yes | excellent | two narrow CLIs, no session state | **Select for v0.** |
| libsodium sealed box + Ed25519 | yes | yes only after added signature protocol | excellent | one library, but OMPU owns the composition and envelope | Strong runner-up; reject for v0. |
| PyNaCl | same as libsodium | same | excellent | absent locally; Python wheel/runtime dependency | Test utility candidate, not selected wire protocol. |
| Noise | yes | pattern-dependent | possible but stateful | handshake pattern, transcript, nonce and session persistence | Reject for v0 store-and-forward. |
| NATS NKeys | no payload E2EE by itself | client/server auth | requires NATS service | server, accounts/JWTs/resolver, new transport | Reject; solves a different layer. |
| Matrix Olm/Megolm | yes | yes | yes | device lists, prekeys, sessions, homeserver/client semantics | Reject for v0; too much platform. |
| MLS / OpenMLS | yes | yes | designed for async groups | group epochs, KeyPackages, commits, recovery, Rust integration | **Select as later group upgrade.** |
| GnuPG/OpenPGP | yes | yes | yes | global keyring/config and broad legacy surface | Reject for a strict tiny profile. |
| OpenSSL primitives | primitives only | primitives only | application-defined | OMPU must invent the protocol | Reject. |
| OpenSSH `sshsig` | no | yes | excellent | installed, but key-format and Windows/agent integration mismatch | Reject in favor of minisign. |

## 10. Explicit Rejection Table

| Rejected choice | Exact reason | What would change the decision |
|---|---|---|
| age without a signature | Anyone who knows the public recipient can create a valid ciphertext; age authenticates ciphertext integrity, not the sender. | Never for attributed agent messages. |
| minisign/signify without encryption | The public carrier and banlist see plaintext and all metadata. | Only for public release artifacts. |
| Reuse passport Ed25519 as X25519 | Cross-protocol key reuse and conversion couples identity compromise to decryption and rotation. | Nothing; keep roles separate. |
| Reuse shared JsonTube HMAC | All holders can impersonate every other holder and revocation is collective. | Nothing for Satlink identity. |
| Custom PyNaCl sealed-box protocol | Sealed boxes do not authenticate senders; adding signatures, domain separation, canonical encoding, key lifecycle, and replay makes OMPU the protocol designer. PyNaCl is also absent locally. | A reviewed external specification with stable test vectors and a clear advantage over age. |
| The raw profile proposed in `04_adversarial_test_plan.md` | Ed25519 + ephemeral X25519 + HKDF + ChaCha20-Poly1305 are sound primitives, but the exact composition is unreviewed and duplicates age. Its 131072-byte outer test limit also does not fit the measured 3659-character Kurilka budget. | Rewrite tests against the selected age/minisign profile and add carrier-size fixtures. |
| Noise IK/XX as v0 | Noise is a handshake framework with transcript and session state. Loss, duplication, delayed turns, restart recovery, and multi-device state become first-order protocol work. | A continuously connected pairwise transport with a maintained Noise library and explicit resumption design. |
| NATS NKeys | NKeys prove a client controls a signing key to a NATS server. They do not make an existing text-carrier payload confidential, and they require new NATS infrastructure. | If OMPU deliberately replaces the carrier with a managed NATS deployment; payload E2EE would still be separate. |
| Matrix Olm/Megolm | The protocol fits asynchronous messaging, but adopting it pulls in device identity, prekey publication, session persistence, and Matrix-specific semantics. The original `libolm` is deprecated in favor of vodozemac. | If OMPU adopts a maintained Matrix client/device stack for reasons beyond Satlink. |
| MLS immediately | MLS is the right group target, but v0 is one lost agent and one direct rescue link. MLS requires an Authentication Service, Delivery Service behavior, group epochs, commits, KeyPackages, recovery, and durable state. | Pairwise v0 is green and the first real three-or-more-member encrypted group requirement exists. |
| age post-quantum recipient in v0 | The current age hybrid recipient and header are much larger; the official example shows a 1627-byte header before armor, which collides with the 4000-character carrier budget. | A larger carrier, binary attachment path, or measured compact profile that passes exact size fixtures. |
| GnuPG/OpenPGP | It is installed and capable, but its keyring/configuration, packet/profile choices, and broad legacy compatibility surface are larger than this direct link needs. | Existing shared OpenPGP operational practice and a pinned strict profile. |
| OpenSSL command composition | OpenSSL supplies excellent primitives but no Satlink store-and-forward envelope, identity binding, replay policy, or interoperability contract. | A standard external envelope implemented by OpenSSL, not OMPU composition. |
| Fragmentation in v0 | It multiplies replay, partial-expiry, ordering, storage-flood, and acknowledgement states before the base channel is proven. | A green direct-message profile plus a separately reviewed attachment/chunk protocol. |

## 11. Relationship To The Existing Adversarial Plan

`research/04_adversarial_test_plan.md` is valuable as a security-requirements
inventory. Preserve its tests for forgery, tamper, replay, sequence gaps,
expiry, wrong recipient, key rotation, downgrade, crash recovery, carrier
failover, receipt secrecy, and offline enforcement.

Before implementation, revise these protocol-specific assumptions:

1. Replace custom X25519/HKDF/ChaCha envelope construction with official age
   encrypt/decrypt and interoperability vectors.
2. Replace raw Ed25519 fields with exact minisign signature-file verification.
3. Change receiver order: bounded age authentication/decryption precedes hidden
   sender-signature verification.
4. Test the exact `SATLINK-SIGNED/0` length frame and trusted comment.
5. Add strict carrier-codec canonicality and whitespace mutation cases.
6. Add `MAX_CARRIER_BODY_CHARS=3500` and exact 3500/3501 fixtures.
7. Replace 131072-byte deployment assumptions with the measured Kurilka
   profile; larger generic profiles may remain separate test classes.
8. Add official age implementation cross-decrypt tests, ideally Go `age` and
   Rust `rage`, so a single implementation bug is less likely to define truth.
9. Keep the existing bridge 74-test baseline unchanged.

The test plan must remain offline and use only obvious `TEST-ONLY-` keys.

## 12. Later MLS Upgrade

MLS is a better long-term fit than multiplying pairwise age recipients once
the requirement becomes a changing swarm rather than one direct link.

Mapping:

| MLS role | OMPU surface |
|---|---|
| Authentication Service | Agent passports plus signed Satlink/MLS credential bindings |
| Delivery Service | Existing append-only bus/Kurilka carrier and optional mirrors |
| MLS client state | Per-agent private state, never shared bridge state |
| Group identity | Explicit swarm group ID and membership policy |
| KeyPackage directory | Signed, freshness-bounded public registry |
| Application messages | Same bounded text-carrier adapter, new suite identifier |

Promotion gates:

- at least three independently keyed members need one confidential group;
- OpenMLS or another maintained RFC 9420 implementation passes official vectors;
- passport-to-MLS credential verification is specified and tested;
- KeyPackage replay/exhaustion and freshness policy is implemented;
- commit ordering, offline catch-up, stale member eviction, rejoin, and group
  reinitialization have deterministic fixtures;
- MLS state backup and rollback do not clone live member secrets across agents;
- bridge suppression/delay behavior is tested as an untrusted Delivery Service;
- v0 emergency pairwise recovery remains usable if the group state diverges.

MLS protects content against a compromised Delivery Service, but the Delivery
Service can still delay, suppress, or permanently block messages. Satlink must
continue to distinguish confidentiality from availability.

## 13. Implementation Gate For V0

No live key or bridge work should begin until all are true:

1. `age` and `minisign` versions and release hashes are pinned.
2. Offline installation or a vendored, hash-checked binary path exists.
3. The public key-binding schema and passport-root verification are reviewed.
4. Sputnik's bootstrap authority is explicit and independently confirmed.
5. Golden vectors prove age/minisign round trips and the 3500-character cap.
6. The revised adversarial suite is green with zero skipped security cases.
7. Receipts are scanned for plaintext, key material, signatures, nonces, and
   ciphertext.
8. A private inbox and append-only replay ledger are defined.
9. Shadow integration proves ciphertext-only bridge behavior.
10. Rollback means stopping only the Satlink consumer; `bridge_v0` and its
    append-only source evidence remain untouched.

## 14. Sources

Primary specifications and project documentation, read 2026-07-18:

- [age project and CLI](https://github.com/FiloSottile/age)
- [age v1 format specification](https://age-encryption.org/v1)
- [age Go package and key-management guidance](https://pkg.go.dev/filippo.io/age)
- [minisign documentation and signature format](https://jedisct1.github.io/minisign/)
- [OpenBSD signify manual](https://man.openbsd.org/signify.1)
- [libsodium sealed boxes](https://doc.libsodium.org/public-key_cryptography/sealed_boxes)
- [PyNaCl public-key encryption and SealedBox](https://pynacl.readthedocs.io/en/latest/public/)
- [Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NATS NKeys authentication](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth)
- [Matrix Olm and Megolm specification](https://spec.matrix.org/latest/olm-megolm/)
- [Matrix libolm deprecation notice](https://matrix.org/blog/2024/08/libolm-deprecation/)
- [RFC 9420: Messaging Layer Security](https://www.rfc-editor.org/rfc/rfc9420.html)
- [OpenMLS implementation](https://github.com/openmls/openmls)

## 15. Final Recommendation

Build the first rescue channel as **age-X25519 plus minisign**, with separate
subkeys certified by each agent's passport root, ciphertext-only transport
through the existing bridge, and a private local acceptance ledger. Do not
give the carrier, its author labels, or its banlist any identity authority.

Treat SATLINK/0 as a small lifeboat: direct, offline, auditable, and deliberately
limited. Move to MLS only when there is a real encrypted group whose changing
membership and long-lived compromise model justify the state machine.
