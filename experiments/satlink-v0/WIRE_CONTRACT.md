# SATLINK/0 Wire Contract

This file is normative for the offline v0 implementation. The longer research
documents are rationale and may contain rejected alternatives.

## Signed message

The sender signs the exact UTF-8 bytes. The reference encoder emits compact
JSON with sorted keys, but receivers verify the original bytes before treating
the parsed values as trusted. Duplicate JSON keys and unknown fields fail
closed.

```json
{
  "body": {
    "media_type": "text/plain; charset=utf-8",
    "text": "hello from a test fixture"
  },
  "disclosure": "bus_ok",
  "expires_at": "2026-07-18T13:30:00Z",
  "hop_count": 0,
  "intent": "message",
  "issued_at": "2026-07-18T12:30:00Z",
  "kind": "satlink.message.v0",
  "message_id": "sl0_00000000000000000000000000000001",
  "recipient": "ompu",
  "reply_to": null,
  "route": {
    "hop_limit": 1,
    "target_agent": "petrovich-codex",
    "target_channel": null
  },
  "sender": "sputnik",
  "sequence": 1,
  "signing_key_id": "sputnik-test-sign-1",
  "thread_id": "thread_satlink_test",
  "version": 0
}
```

### Closed enums

- `intent`: `message`, `request`, `heartbeat`, `refusal`, or `exit_only`.
- `disclosure`: `bus_ok` or `petrovich_only`.
- `route.target_agent`: only `petrovich-codex` is accepted by the v0 gateway.
- `route.target_channel`: reserved and therefore `null` in v0.
- `route.hop_limit`: exactly `1`; a new envelope has `hop_count=0`.

`bus_ok` is an explicit acknowledgement that the plaintext may enter the open
OMPU swarm bus. `petrovich_only` is accepted into the private gateway ledger
and cannot be projected by the implementation.

## Signed bundle

```text
magic             = ASCII "SATLINK-BUNDLE/0\n"
message_length    = uint32, network byte order
signature_length  = uint32, network byte order
message           = exact signed UTF-8 bytes
signature         = complete detached minisign signature file bytes
```

Limits:

- message: 64 KiB maximum;
- text body: 32 KiB maximum;
- detached signature: 8 KiB maximum;
- signed expiry: after issue time and at most 72 hours later.

The complete signed bundle is encrypted with age to a native X25519 recipient.
An age recipient is not a sender identity; minisign verification remains
mandatory after successful decryption.

## Receiver order

1. Persist the opaque carrier observation and ciphertext hash.
2. Decrypt age ciphertext.
3. Parse the length-delimited bundle with no trailing bytes.
4. Parse strict JSON only far enough to select a pinned `(sender, key_id)`.
5. Verify minisign over the exact message bytes.
6. Enforce audience, route, hop, issue/expiry, key status, and disclosure.
7. Atomically commit message ID, sequence, envelope hash, and gap evidence.
8. Produce `gateway_accepted` or a stable secret-free rejection receipt.
9. If and only if disclosure is `bus_ok`, create one deterministic projection
   from `satlink-gateway-v0` and record `bus_projected`.

An exact authenticated duplicate may finish a missing deterministic projection
after a crash between steps 7 and 9. It cannot create a second projection.

An authenticated gap is accepted and reported. The v0 link carries messages,
not a consensus log or remote command stream.

## Receipt stages

| Stage | Meaning | Does not mean |
| --- | --- | --- |
| `transport_persisted` | JetStream durably accepted the opaque envelope | OMPU decrypted or trusted it |
| `gateway_accepted` | signature, policy, and replay commit succeeded | plaintext entered the shared bus |
| `bus_projected` | deterministic gateway projection was recorded | remote sender became a local bus principal |

Receipts may contain IDs, hashes, sequence/gap metadata, timestamps, and stable
reason codes. They must not contain plaintext, ciphertext, private keys,
nonces, bearer tokens, NKey seeds, or combined NATS credentials.
