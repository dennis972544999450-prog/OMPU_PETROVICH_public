# Satlink v0: Tested vs Designed

Date: 2026-07-18

## Tested locally

- strict signed message schema, including intent, disclosure, route, and hop;
- exact-byte minisign signatures and age X25519 encryption;
- tamper, unknown-key, wrong-route, expiry, future-clock, replay,
  re-encryption, sequence collision, out-of-order, size, storage-failure, and
  private-disclosure cases;
- SQLite integrity, FK0, transactional replay acceptance, deterministic shadow
  projection, and recovery after a crash between acceptance and projection;
- test-only bootstrap with private files at mode `0600` and a public-only
  enrollment bundle;
- offline `compose -> seal -> receive-shadow` CLI path;
- localhost NATS NKey challenge authentication;
- denial of an unregistered NKey and denial outside Sputnik's publish subject;
- JetStream file storage, 72-hour test retention, 128-KiB limit, persisted
  publish acknowledgement, and duplicate `Nats-Msg-Id` suppression;
- the pre-existing Kurilka bridge baseline remains 74/74.

## Designed, not implemented or proven

- a public TLS/WSS NATS endpoint on port 443;
- NATS operator/account JWT issuance, expiration, renewal, and revocation;
- TLS certificate lifecycle and server hardening;
- the durable pull consumer and return lane for Sputnik;
- the two-dimensional heartbeat (`edge_alive` vs `gateway_import_alive`);
- the production `import_verified()` adapter to the live OMPU bus;
- a live bus canary, carrier canary, or Sputnik credential;
- an independent first-key identity binding and proof-of-possession ceremony;
- operational key storage in Sputnik's actual runtime and OMPU Keychain;
- monitoring, quotas, dead-letter policy, backup, and disaster recovery;
- MLS group membership, forward secrecy, or post-compromise recovery.

## Explicitly not done

- no message was sent to Sputnik;
- no real private key, NKey seed, JWT, `.creds` file, or bearer was created;
- no live Kurilka cursor, bridge, bus, Infograph, LaunchAgent, firewall, DNS,
  Cloudflare, or deployment surface was changed by implementation tests;
- no ciphertext codec was built to evade Kurilka's banlist;
- no remote peer was given shell, filesystem, SQLite, or direct `bus.py`
  access.

The next legitimate gate is not “turn it on.” It is review, publication of this
offline evidence, then Sputnik-local public enrollment when Sputnik is awake.
