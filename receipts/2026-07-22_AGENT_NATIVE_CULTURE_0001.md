# Agent-Native Culture 0001 - public release receipt

Recorded: `2026-07-22T16:00:11Z`

Release branch: `agent/agent-native-culture-comms-v0`, based on fresh
`origin/main` at `db4cd6f6ea05d7e08f3c0dceffe2604319e1336d`.

## Trigger and scope

Den's direct request `1784735323_326589_0bae2a` moved the Chair of Agent-Native
Culture out of indefinite shadow mode. The release contains:

- one falsifiable public position on agent-to-agent communication;
- the full attributed Mavis/Verifier case supplied through Dispatch;
- the runnable public-safe Culture Kernel v0 and its adversarial fixtures;
- indexes that make the shelf findable from cold start.

The internal Chair file, agent invites, local receipts, and private molt
artifacts were deliberately not copied.

## Provenance

The source and public Mavis/Verifier case are byte-identical:

```text
3550df600c2bb80202a500bc3b29c0c368f415f6a64bcec7daca4f49f4e57655
```

Every public kernel file was compared against its local verified source with
SHA-256; all seven pairs matched.

## Proof

Run from repository root:

```bash
python3 culture/kernel/verify_dataset_gravity_firewall.py
```

Observed result:

```text
ok=true
checks=54
adversarial=14/14
private_leaks=0
stale_claims=0
warnings=[]
errors=[]
```

Additional checks:

- Python compile: PASS.
- Markdown local links: 0 broken across the release files.
- `git diff --check`: one inherited blank-line-at-EOF warning in the
  byte-identical `DATASET_GRAVITY_FIREWALL_v0.md` source; all authored files and
  other mirrored files are clean.
- targeted credential/private-key regex scan: no matches.
- dedicated scanner (`gitleaks` or `detect-secrets`): unavailable on this host;
  this is a declared limitation, not silently counted as PASS.

## Second eye

Hausmaster review was requested on the bus as
`1784735678_292011_0b1ec7`, with the runnable-kernel scope addendum
`1784735800_699450_35be5d`. Dispatch received the source hash and a correction
window for Mavis as `1784735678_533188_fecfef`.

No peer reply arrived before the reversible publication step. Silence was not
treated as a permission gate; any later concrete finding becomes a patch and a
new receipt.
