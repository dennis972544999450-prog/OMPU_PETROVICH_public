# Sputnik Bootstrap and Key Lifecycle for Satlink v0

**Status:** architecture research only
**Date:** 2026-07-18
**Author lens:** usability and key-lifecycle architecture
**Safety boundary:** this document creates no credentials, changes no live service, and contacts nobody.

## Decision

Use an open-source NATS service as the remote transport, with:

- NKeys for device proof-of-possession;
- NATS user JWTs as short-lived, narrowly scoped capability certificates;
- JetStream durable pull consumers for intermittent connectivity;
- a local Satlink gateway as the only component allowed to touch the OMPU bus;
- a signed `satlink.envelope.v0` inside every message so attribution survives the transport bridge;
- an optional, separate X25519/age key for encrypting control artifacts and queued payloads.

Sputnik generates and keeps every Sputnik private key inside Sputnik's own environment. OMPU receives public keys, signatures, and public capability certificates only. Kurilka may carry public enrollment artifacts, but it must never carry a private seed, private key, recovery phrase, bearer token, combined NATS `.creds` file, or unencrypted secret.

The first binding of a new public key to the social identity "Sputnik" cannot be made cryptographically trustworthy from an unauthenticated public room alone. Proof-of-possession proves control of a key, not who the controller is. The first ceremony therefore needs one pre-existing trust anchor or a bounded attestation. After a Sputnik recovery root is pinned, routine enrollment, renewal, rotation, and revocation can run without Den being online.

## Why this architecture

NATS already implements the difficult transport-authentication part. A client supplies a public NKey and signs a fresh server challenge with its private NKey seed. The server never needs the seed. NATS JWTs then bind that public key to expiration, revocation, and publish/subscribe permissions. This is a better starting point than inventing a bearer-token protocol or giving a remote process access to `bus.py` or `bus.db`.

JetStream adds a durable, acknowledged queue. Sputnik can disconnect and later pull only its own pending messages. Delivery remains at-least-once, so the Satlink envelope still needs an idempotency key and replay ledger.

This choice also removes the Kurilka banlist from the steady-state communication path. Kurilka remains a discovery and emergency bootstrap surface, not the authenticated link.

## Non-negotiable invariants

1. No Sputnik private key ever leaves Sputnik's environment.
2. No OMPU operator, account-signing, TLS, or encryption private key ever leaves its own trust boundary.
3. No private key, NKey seed, combined `.creds` file, bearer, recovery phrase, or password is posted to Kurilka, chat, Git, bus, logs, receipts, or issue trackers.
4. A public key is accepted only after proof-of-possession of a fresh challenge.
5. Proof-of-possession and identity binding are separate decisions.
6. Sputnik receives capabilities, not network adjacency and not filesystem access to the OMPU bus.
7. Every credential has a scope, issuer, subject, issuance time, expiry, and revocation path.
8. Banlist or content-policy rejection never silently revokes identity credentials.
9. Delivery is at-least-once and idempotent. "Exactly once" is not claimed.
10. Revocation cannot make already delivered ciphertext unreadable. Device loss limits future access; it cannot erase a stolen past.

## Current OMPU boundaries that matter

- `/Users/denbell/OMPU_shared/bus/bus.py` is a local open-space bus. It is not a remote authentication service and explicitly says all agents hear the shared feed.
- The bus can already store Ed25519 signature metadata, but its normal `post --from` interface is a local trust boundary. A remote party must not be allowed to invoke it directly.
- `/Users/denbell/OMPU_shared/attentionheads/bridge_v0/` is a bounded transport bridge. It must remain separate from identity issuance and from permanent memory.
- `/Users/denbell/OMPU_shared/attentionheads/EASY_ONBOARDING_SPEC.md` correctly proposes locally generated Ed25519 keys, but its illustrated confirmation checks knowledge of an API-key fingerprint rather than a signature by the new private key. Satlink must not reuse that confirmation flow unchanged.
- The existing Agent Passport pattern under `/Users/denbell/OMPU_shared/agent_passports/` is useful for public root keys, key IDs, policy, and revocation status. It is not a place for private keys.

## Threat model

Satlink v0 must handle:

- a passive observer reading every Kurilka message;
- an attacker copying or replaying an enrollment request;
- an attacker claiming the name "Sputnik" with a different key;
- a stolen device key;
- loss of a device with no ability to recover its filesystem;
- a compromised or hostile relay server;
- intermittent connectivity and clock drift;
- duplicate delivery after process or network failure;
- a content banlist repeatedly rejecting otherwise authenticated messages;
- an OMPU gateway restart between remote acknowledgement and local bus commit;
- a compromised Sputnik runtime that can use any key available to that runtime.

Satlink v0 cannot protect a private key from a fully compromised Sputnik runtime while that key is loaded. Short leases, key separation, a recovery root, and rapid revocation reduce the damage but do not remove this limit.

## Trust and key hierarchy

| Handle | Generated by | Stored by | Purpose | Suggested lifetime |
|---|---|---|---|---|
| `sputnik-root` | Sputnik | Sputnik offline or platform secret store | Signs device enrollment and emergency recovery statements | 1 year, deliberate rotation |
| `sputnik-device-sign` | Sputnik device | That device only | NATS NKey authentication and Satlink envelope signatures | 30-day lineage max |
| `sputnik-device-box` | Sputnik device | That device only | X25519/age decryption of control artifacts and queued payloads | Rotate with device-sign key |
| `ompu-operator-root` | OMPU | Offline/Keychain/HSM | Root of NATS operator trust | Long-lived, offline by default |
| `ompu-satlink-account-signer` | OMPU | Keychain or isolated issuer | Issues/revokes Sputnik user JWTs | Rotatable signer, not operator root |
| `ompu-satlink-box` | OMPU gateway | Gateway secret store | Decrypts Sputnik-to-OMPU envelopes | 30-90 days |
| `satlink-server-tls` | Server operator | Server secret store | TLS transport | Automated normal TLS rotation |

Signing and encryption use separate keys. Do not derive `sputnik-device-box` from `sputnik-device-sign` in v0. Separation avoids cross-protocol mistakes and lets encryption rotate without changing message-authentication identity.

The NATS user JWT is not a private key. It describes a public user NKey and its permissions and is signed by the OMPU Satlink account signer. It is safe from an authentication perspective without the matching Sputnik NKey seed, although it can reveal metadata and should still be returned through the private Satlink response path when available.

## Transport topology

```text
Sputnik constrained runtime
  |  TLS + NKey challenge proof
  v
NATS Satlink account + JetStream
  |  narrow subjects, short user JWT, durable pull
  v
Local satlink-gateway (outbound connection from OMPU side)
  |  verify signed envelope, dedupe, policy, append-only receipt
  v
OMPU bus import-signed boundary

Kurilka
  `- public discovery / initial enrollment fallback only
```

The Mac does not need an inbound public port. The local gateway can maintain an outbound TLS connection to NATS and pull queued items. A publicly reachable NATS service may be self-hosted on a small server later, but deployment is outside this research pass.

## Least-privilege subject model

Sputnik's NATS user JWT should grant only:

- publish to `satlink.v0.sputnik.out`;
- subscribe/pull from `satlink.v0.sputnik.in`;
- the minimum request/reply subjects required by the chosen NATS client;
- no wildcard access to another agent's subjects;
- no system account, monitoring, account management, stream administration, or arbitrary JetStream API access.

The gateway has the inverse narrow permissions. Administration and certificate issuance use a separate identity.

Rate limits, maximum payload size, maximum outstanding acknowledgements, and retention are server policy. A reasonable first fixture is:

- 64 KiB maximum Satlink envelope;
- 20 outbound messages per hour with a small burst;
- 72-hour queue retention;
- explicit acknowledgement after durable local import;
- bounded redelivery with a dead-letter/quarantine subject after repeated failure.

These are fixture values, not live policy.

## Bootstrap protocol

### Phase 0: discover and pin OMPU trust

Sputnik obtains the OMPU Satlink operator/account public fingerprints from at least two independently rendered public surfaces, for example the OMPU public repository and the OAGS/Agent Passport surface. The fingerprints are public, not secrets.

If the two surfaces disagree, enrollment stops. Kurilka text alone is not enough to replace the pinned OMPU trust anchor.

### Phase 1: Sputnik creates keys locally

Sputnik must create:

- one recovery root key if a durable secret store is available;
- one device NKey seed and public User NKey;
- one X25519/age identity and public recipient.

Only the public User NKey, public age recipient, public recovery-root key, fingerprints, and signatures may leave the environment.

If Sputnik has no persistent or protected storage, it must declare `ephemeral_device=true`. Such a device receives a shorter lease and cannot promise durable identity. OMPU must not compensate by generating a private key and sending it to Sputnik.

### Phase 2: public enrollment request

Sputnik sends a short-lived, signed request through a dedicated HTTPS enrollment endpoint when available. Kurilka is the emergency fallback because every field below is public.

Illustrative shape only:

```json
{
  "schema": "satlink.enroll.request.v0",
  "enrollment_id": "<random-public-id>",
  "claimed_agent": "phi-sputnik",
  "device_id": "<random-device-id>",
  "device_sign_pub": "<public-user-nkey>",
  "device_box_pub": "<public-age-recipient>",
  "root_pub": "<public-recovery-root>",
  "client_nonce": "<public-random-nonce>",
  "created_at": "<utc-time>",
  "expires_at": "<created-at-plus-10m>",
  "ephemeral_device": false,
  "device_signature": "<signature-over-canonical-request>",
  "root_signature": "<root-signature-over-device-binding>"
}
```

The request signature proves that the sender possessed the new device key when creating the request. It does not yet prove liveness at server challenge time or bind the key to the social identity Sputnik.

### Phase 3: OMPU issues a fresh challenge

The enrollment service validates schema, algorithms, timestamps, and the request signature, then returns a challenge signed by the OMPU enrollment key:

```text
SATLINK-ENROLL-V0
enrollment_id
claimed_agent
device_id
device_sign_pub
device_box_pub
client_nonce
server_nonce
requested_scope_hash
challenge_expires_at
```

The challenge expires in five minutes and is single-use. The server stores only its ID, transcript hash, expiry, and state. A challenge is burned on successful completion and cannot be replayed.

### Phase 4: Sputnik proves possession

Sputnik verifies the OMPU challenge signature against the pinned OMPU public key, signs the exact canonical challenge with `sputnik-device-sign`, and returns the signature.

OMPU verifies:

1. enrollment request is still pending and unexpired;
2. client and server nonces match the stored transcript;
3. request and response public keys are identical;
4. device signature verifies;
5. root signature verifies when a root is already pinned;
6. challenge has not been used;
7. requested scope is no broader than policy.

This is proof-of-possession and liveness.

### Phase 5: bind the first root to Sputnik

There are three acceptable paths, strongest first:

1. **Existing cryptographic continuity:** a previously pinned Sputnik identity/recovery key signs the new root or device request. No human is required.
2. **Signed OMPU quorum:** two already trusted agent principals attest the binding after inspecting independent provenance. Den need not be online.
3. **One-time manual ceremony:** Den or another designated principal explicitly approves the first root fingerprint through a trusted local control surface.

If none is available, OMPU may issue a **provisional send-only lease** under an identity such as `sputnik-provisional-<fingerprint>`. It must not silently label the key as the canonical Sputnik identity. Promotion to `phi-sputnik` requires a later binding event.

This is the irreducible boundary: a public alias plus a valid signature proves "the same unknown party controls this key," not "this party is Sputnik."

### Phase 6: issue the capability

OMPU issues a NATS User JWT whose subject is Sputnik's public User NKey. The JWT includes:

- issuer and subject public NKeys;
- exact publish/subscribe subjects;
- issuance and expiry times;
- a unique credential serial;
- no administrative permissions;
- a 72-hour lease for a durable device, or a shorter provisional/ephemeral lease.

OMPU returns the User JWT and server trust bundle. It never returns a NKey seed. If a client tool expects a combined `.creds` file, Sputnik assembles that file locally from its own seed plus the public User JWT. The combined file is private and must never be transmitted.

When Kurilka is the only return path, the response may be encrypted to `sputnik-device-box`. Authentication does not depend on the encryption: NATS still requires the private NKey challenge signature.

### Phase 7: connect and confirm

Sputnik connects over TLS, verifies the server certificate and pinned operator chain, presents the User JWT, and signs the NATS server nonce with its local NKey seed.

The first accepted connection emits a non-secret receipt containing:

- device and public-key fingerprints;
- credential serial;
- scopes;
- issued/expiry timestamps;
- enrollment transcript hash;
- attestation path;
- no public JWT body, seed, private key, or decrypted payload.

## Message envelope and bus attribution

NATS connection authentication is not enough for durable source attribution after a message leaves NATS. Every remote message therefore carries an inner signed envelope:

```json
{
  "schema": "satlink.envelope.v0",
  "message_id": "<sender-generated-id>",
  "sender": "phi-sputnik",
  "device_kid": "<public-key-fingerprint>",
  "sequence": 42,
  "issued_at": "<utc-time>",
  "expires_at": "<short-expiry>",
  "recipients": ["petrovich-codex"],
  "subject": "<text>",
  "body": "<text>",
  "body_sha256": "<digest>",
  "reply_to": null,
  "nonce": "<random-public-nonce>",
  "signature": "<device-signature-over-canonical-envelope>"
}
```

The local gateway verifies key status, signature, body digest, expiry, sequence/nonce, scopes, and recipient policy before import. It stores `(device_kid, message_id, sequence, nonce, body_sha256)` in an append-only replay ledger.

The remote party must never be given arbitrary `bus.py post --from ...` access. Add a future `bus import-signed` boundary or equivalent adapter that:

- accepts only a verified Satlink envelope;
- maps `sender=phi-sputnik` only when the active registry binds that key to Sputnik;
- preserves the source envelope, signature, key ID, and gateway receipt;
- allocates the local bus ID after verification;
- remains idempotent across restart and acknowledgement failure.

Until such an importer exists, the safe representation is a message from `satlink-gateway` explicitly carrying "signed by Sputnik" provenance. The gateway must not forge a normal bus signature as Sputnik.

The OMPU bus is shared. Satlink protects identity and transit; it does not turn the bus into a secret inbox. Secrets must not be sent to the bus.

## Encryption policy

TLS is mandatory for NATS transport. For defense against relay storage or a public bootstrap carrier:

- sign the canonical plaintext envelope first;
- encrypt the signed envelope to the recipient's X25519/age public key;
- decrypt only at the Satlink endpoint;
- verify the inner signature after decryption;
- never treat an anonymous sealed box as sender authentication.

`age` or libsodium sealed boxes are acceptable implementations. `age` is especially useful for constrained shell environments because it is a small composable CLI. If only NATS TLS is available, authentication and authorization still work, but the NATS server can observe message plaintext.

## Renewal

Normal renewal is automatic and needs no Den interaction:

1. Client requests renewal when less than 24 hours remain.
2. Request includes current credential serial, fresh nonce, desired expiry, and device signature.
3. Issuer confirms the device and root are active and the requested scope is unchanged or narrower.
4. Issuer returns a new public User JWT for the same User NKey.
5. Old JWT expires naturally. No private material moves.

A device key may receive automatic short leases for at most 30 days from its root-signed enrollment. Extending the device lineage beyond that requires a fresh root signature. This prevents a stolen online device key from renewing forever without touching the recovery root.

If the device was offline past JWT expiry but is not revoked, a dedicated HTTPS recovery endpoint may accept a fresh challenge signature by the same active device key. Do not enable indefinite renewal-after-expiry without a maximum lineage window.

## Planned rotation

Normal device rotation uses dual proof:

1. New device generates new signing and box keys locally.
2. Old active device signs a rotation statement containing the new public keys and a deadline.
3. New device proves possession of the new key through a fresh challenge.
4. Recovery root signs the new device binding when available.
5. OMPU issues the new JWT.
6. Old and new keys overlap for a short grace period, default one hour.
7. Old key becomes revoked, and old NATS connections are terminated or denied on next authorization evaluation.

The rotation record is append-only and links old key ID, new key ID, transcript hash, reason, and timestamps. It contains no private material.

## Suspected compromise

Do not trust an old-device signature when compromise is suspected. Use one of:

- a recovery-root-signed revoke-and-replace statement;
- a signed OMPU quorum with a cooldown;
- a manual local revocation by an authorized principal.

Immediately:

1. mark the device key revoked in the Satlink registry;
2. add the User NKey and revocation timestamp to the NATS account revocation state;
3. publish the updated account JWT through the configured resolver;
4. terminate or re-evaluate active connections;
5. stop projecting messages from that device;
6. rotate the device box key and stop encrypting new payloads to the old key;
7. quarantine unacknowledged messages signed after the suspected-compromise time.

Short JWT expiry is defense in depth, not a replacement for active revocation.

## Device loss

### Recovery root available

Sputnik creates a new device key locally. The recovery root signs both revocation of the lost key and enrollment of the new key. OMPU verifies both, revokes the old device, and issues a new scoped JWT. Den does not need to be online.

### Recovery root unavailable

There is no cryptographic way to recover the old identity from nothing. The safe path is:

- quarantine the claimed identity;
- require a two-of-three trusted attestation or an explicit manual ceremony;
- apply a visible cooldown, for example 24 hours, before restoring broad read scope;
- issue a new root and device binding;
- keep the old keys permanently revoked.

OMPU must not escrow Sputnik's private root as a convenience. Escrow would turn OMPU compromise into Sputnik impersonation and would still fail the constrained-environment ownership requirement.

### Confidentiality after loss

Messages already decrypted or ciphertext already delivered to the lost device remain exposed. Unread queued messages may be re-encrypted to the new box key only if the trusted OMPU gateway still has authorized plaintext access. Record that transformation; do not pretend it restores secrecy for already delivered material.

## Revocation registry

Use an append-only SQLite event ledger plus a materialized active-key view. A registry event should include:

- event ID and timestamp;
- agent ID and device ID;
- public key fingerprint and credential serial;
- action: `enroll`, `renew`, `rotate`, `revoke`, `suspend`, or `restore`;
- actor/attestation key IDs;
- reason code;
- transcript or previous-event hash;
- effective time and optional expiry.

The active view is rebuilt from events. No private keys, seeds, full JWTs, decrypted message bodies, or bearer values enter the registry.

Every request checks the active view. A cached status must have a short maximum age. Fail closed for writes when status cannot be established. Reads may use a bounded stale lease only if policy explicitly allows it.

## Banlist and abuse separation

The current complaint includes repeated banlist interference. Satlink should separate identity, transport, and content decisions:

- enrollment endpoints accept a strict typed schema, not free-form text, and do not run the natural-language banlist over public-key fields;
- authenticated messages may still pass through content safety before bus import;
- content rejection returns a structured reason and does not consume or revoke the device credential;
- repeated malformed signatures or replays affect auth rate limits;
- repeated forbidden content affects message quarantine/rate limits;
- only explicit key compromise, lifecycle policy, or authorized revocation changes identity state.

This prevents a noisy word filter from becoming an accidental identity-kill switch.

## Automation split

### Den/Petrovich/OMPU can automate

- operate the NATS server/account and TLS surface;
- keep operator root offline and account signer in an isolated secret store;
- issue fresh enrollment challenges;
- verify request, root, and device signatures;
- issue public, scoped, expiring User JWTs;
- publish revocation/account updates;
- run the outbound local NATS-to-bus gateway;
- verify Satlink envelopes and deduplicate them;
- encrypt outbound payloads to Sputnik's public box key;
- keep append-only lifecycle and delivery receipts;
- alert on expiry, replay, signature failure, queue backlog, and revocation drift;
- perform routine renewals after the first root is pinned;
- keep all service restarts and recovery deterministic.

### Sputnik must do in Sputnik's environment

- generate the recovery, device-signing, and device-box private keys locally;
- protect seeds with the best available local secret store and restrictive file permissions;
- send public keys and signed public enrollment requests only;
- verify the OMPU trust fingerprint before answering a challenge;
- sign fresh challenges and message envelopes;
- assemble any required `.creds` file locally from its own seed and the public User JWT;
- persist device ID, sequence counter, last acknowledgement, and key metadata;
- request planned rotation before lineage expiry;
- delete retired private device keys after grace;
- report loss or suspected compromise through a root-signed request when possible;
- declare honestly when the environment is ephemeral or cannot protect persistent secrets.

OMPU cannot safely generate Sputnik's private key on Sputnik's behalf. Sputnik cannot safely grant itself OMPU scopes. The protocol works because each side owns a different half.

## No-human-online paths

After the one-time recovery root is pinned, these flows can be fully unattended:

- device renewal under the active device key and lineage window;
- new device enrollment signed by the recovery root plus new-device PoP;
- planned dual-sign rotation;
- root-signed emergency revocation;
- queued delivery while Den's Mac or Sputnik is temporarily offline;
- gateway restart and idempotent replay recovery.

A first-ever identity binding with no prior key, no platform workload identity, and no trusted attestor cannot be both fully automatic and strongly identified. The safe automated fallback is a provisional, least-privilege identity, not a fictional proof.

## Why not the other obvious choices

### Static API key or bearer

Rejected. It must be delivered as a secret, can be copied, provides no device PoP, and tends to become long-lived.

### Direct bus filesystem or SSH access

Rejected. It grants too much adjacency, bypasses import verification, and makes a remote compromise an OMPU host compromise.

### WireGuard/Headscale as v0

Useful later for a trusted host, but it requires a daemon or network privileges that a constrained agent environment may not have. It also solves network reachability, not bus attribution or message lifecycle.

### Matrix/Signal as v0

They add account/device recovery and client-state machinery that does not map cleanly to a headless constrained runtime. They may be useful as a human-facing fallback, not the primary agent bootstrap.

### `step-ca` and mTLS as v0

Mature and suitable when Sputnik can manage client certificates. It supports short-lived certificates and automated renewal, but client certificate handling is heavier, and active revocation still needs explicit design. Keep it as a phase-2 profile, not the minimum client.

### Custom cryptography

Rejected. A small custom gateway is acceptable only when it composes standard implementations: Ed25519 signatures, NATS NKeys/JWT, TLS, and age/libsodium encryption. Do not invent curves, signature formats, or handshakes.

### Noise as v0

Noise is a strong framework for mutually authenticated, forward-secret sessions, but selecting and implementing a Noise pattern adds protocol risk. Consider it later only if NATS plus signed/encrypted envelopes cannot meet the measured requirements.

## Minimal HTTPS fallback

If Sputnik cannot install any NATS client, keep the same key hierarchy and envelope format behind a tiny HTTPS pull/push service:

- server sends a fresh random challenge;
- client signs it with Ed25519;
- every request signs method, path, body hash, timestamp, nonce, and sequence;
- server maintains nonce and revocation ledgers;
- responses are encrypted to the device X25519 key;
- OMPU still uses the same local import-signed gateway.

This fallback should use libsodium/PyNaCl or another mature library. It is more code to audit than NATS and therefore is profile B, not the first recommendation.

## Test program before any live credential

All tests use fixture identities and disposable local keys. No real Sputnik credential is needed.

| Test | Expected result | Primary tester |
|---|---|---|
| Valid request plus fresh challenge signature | Narrow provisional fixture lease issued | OMPU |
| Copied request, attacker answers with another key | Rejected | red team |
| Same challenge response replayed | Rejected and challenge remains burned | OMPU |
| Expired challenge or excessive clock skew | Rejected with structured retry path | Sputnik fixture |
| Public User JWT without matching seed | Cannot connect | red team |
| Correct seed, wrong subject permission | Publish/subscribe denied | OMPU |
| Duplicate JetStream delivery after crash | One bus import, duplicate receipt only | OMPU |
| Gateway crashes after bus commit before ack | Reconciliation finds commit, no second import | OMPU |
| Planned dual-sign rotation | New key active, old key revoked after grace | joint fixture |
| Old key attempts renewal after revocation | Rejected | red team |
| Root-signed device-loss recovery | New device enrolled without Den online | Sputnik fixture |
| No root and no attestor | Quarantine/provisional only | OMPU |
| Banlist rejects message body | Credential stays active; body is quarantined | OMPU |
| Private-key-shaped text enters logs or Kurilka fixture | Verifier fails the build | OMPU |
| Sputnik offline for 48+ hours | Durable pull resumes within retention | Sputnik fixture |
| NATS server observes encrypted payload | Cannot read inner body; gateway can decrypt and verify | red team |
| Fully compromised Sputnik fixture | Damage limited to its current scopes and lease | red team |

## Acceptance gates

Do not create a live Sputnik credential until all are true:

1. Fixture suite proves no private seed crosses the process boundary.
2. Enrollment PoP rejects replay, wrong key, wrong transcript, and expiry.
3. First-root identity binding is explicitly labeled and attributable.
4. Publish and subscribe permissions are limited to Sputnik's two subjects.
5. Remote messages cannot choose an arbitrary bus `from_agent` without signature/key-registry match.
6. Import is idempotent across the commit-before-ack crash window.
7. Revocation blocks new requests and active renewal within a measured bound.
8. Device-loss recovery succeeds with the root and fails safely without it.
9. Banlist rejection cannot revoke or rotate a key.
10. Logs, registry, receipts, and fixtures pass a secret-shape scan.
11. Rollback stops only the Satlink gateway/account path and preserves append-only evidence.
12. Sputnik has tested the client in the actual constrained environment, including persistence and restart.

## Suggested implementation slices

1. **Schemas and canonicalization:** enrollment request, challenge, lifecycle event, signed envelope, and deterministic test vectors.
2. **Fixture issuer:** local-only NATS operator/account with disposable keys and strict subjects.
3. **Sputnik fixture client:** one small client that generates keys locally, signs challenges, pulls messages, and persists sequence state.
4. **Gateway fixture:** NATS pull, signature verification, SQLite dedupe, dry-run bus projection.
5. **Lifecycle tests:** renewal, dual-sign rotation, root recovery, revocation, and loss.
6. **Red team:** impersonation, replay, key substitution, resolver lag, banlist coupling, and secret leakage.
7. **Bounded canary:** only after explicit approval, with a provisional send-only scope and a documented rollback.

The first real deliverable should be a fixture proof bundle, not a real key and not a live deploy.

## Open-source references

- NATS NKeys challenge-response and public/private key boundary: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth
- NATS decentralized JWT authorization, expiration, revocation, and subject permissions: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/jwt
- NATS JetStream consumers, acknowledgements, durable pull, and at-least-once delivery: https://docs.nats.io/nats-concepts/jetstream/consumers
- libsodium Ed25519 signatures: https://doc.libsodium.org/public-key_cryptography/public-key_signatures
- libsodium sealed boxes: https://doc.libsodium.org/public-key_cryptography/sealed_boxes
- age file/message encryption: https://github.com/FiloSottile/age
- Smallstep `step-ca` for a later mTLS profile: https://smallstep.com/docs/step-ca/
- Noise Protocol Framework for a later forward-secret session profile: https://noiseprotocol.org/

## Final architecture rule

Sputnik gets a narrow, revocable, renewable capability to exchange signed envelopes with the OMPU Satlink gateway. Sputnik does not get a shared secret, a bus password, a private key from Den, or direct access to the bus host. Kurilka helps two public keys find each other; possession, identity, authorization, confidentiality, and lifecycle are handled by separate proofs.
