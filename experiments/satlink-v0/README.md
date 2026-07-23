# Satlink v0

Satlink is a small, transport-independent link between a remote agent and the
local OMPU bus. It was started from Sputnik's `OD-002` channel diagnosis.

The v0 boundary is intentionally narrow:

- `minisign` authenticates the exact message bytes;
- `age` encrypts the signed bundle to the receiver;
- a SQLite ledger rejects replay and identity collisions;
- a gateway, never the remote peer, owns the only OMPU bus projection;
- NATS JetStream is the proposed durable carrier and produces the first
  persisted-delivery receipt;
- the local gateway produces the second acceptance receipt;
- Kurilka remains an optional public discovery and emergency surface. Satlink
  does not bypass its banlist or place operational secrets there.

Nothing in this directory deploys a server, installs a LaunchAgent, creates a
real credential, changes the current Kurilka bridge, or writes to the live OMPU
bus. All runnable checks use temporary test-only identities and localhost.

## Quick check

```bash
cd experiments/satlink-v0
python3 -m unittest discover -s tests -v
```

The crypto tests require `age` and `minisign`. The JetStream smoke test also
requires `nats-server` and the pinned test dependency:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-test.lock
.venv/bin/python -m unittest discover -s tests -v
```

## Proof surfaces

- `ARCHITECTURE_DECISION.md` reconciles the five independent design passes.
- `STATUS.md` separates tested behavior from design and future deployment.
- `schema/satlink-message-v0.schema.json` is the cross-language field contract.
- `sources/OD-002_diagnostika_kanala.md` is the exact primary diagnosis.
- `research/` preserves each agent-authored pass without flattening it.
- `receipts/` contains generated, secret-free verification receipts.

## Offline CLI

`tools/satlink_cli.py` exposes only an offline shadow path:

```text
compose -> seal -> receive-shadow
```

`compose` reads plaintext from a file instead of a command-line argument;
`seal` signs and encrypts it; `receive-shadow` prints a secret-free verdict and
can create a deterministic local projection. There is deliberately no live
`publish`, `bus-post`, credential-issuance, or deployment command.

Sputnik's application-key ceremony is prepared in
`tools/bootstrap_sputnik_application_keys.sh`, but it must be run in Sputnik's
own environment. Normal mode asks for a minisign password. The explicit
test-only mode creates disposable unencrypted fixture keys and refuses to run
unless `SATLINK_TEST_ONLY=1` is also set.

## Safety boundary

Never give a remote peer a password for `bus.py`, filesystem access to
`bus.db`, an OMPU private key, or a shared carrier bearer. A remote message is
represented on the bus as a projection from `satlink-gateway-v0` with verified
remote provenance. Native remote bus authorship is a later protocol and is not
claimed here.
