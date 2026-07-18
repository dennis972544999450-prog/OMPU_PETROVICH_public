# T4 Runtime Reliability QA

Date: 2026-07-18  
Target: `prototype/mosm_tube.py`  
Target SHA-256: `8865195188325f151859f5b2d77d9a08c4beae715a1adc8cba12ded4f1bdb655`

## Scope and verdict

This was a local, defensive QA pass. It used generated fixtures only under
`/tmp/mosm_t4_runtime_reliability_20260718`, did not access network,
credentials, or live services, and did not modify the implementation.

Result: the baseline succeeded and all 10 invalid-input/path/size probes held
with exit 2 and no output packet. The verify-to-render mutation probe failed:
the parser returned exit 0 and rendered changed source bytes while reporting
the SHA-256 verified for the previous bytes. The stale-read condition reproduced
identically in 2 of 2 runs.

`PASS` below means the parser rejected the unsafe fixture as expected. `FAIL`
means it accepted and rendered a stale or unverified state.

## Observed results

| Probe | Result | Exit | Observed behavior |
| --- | --- | ---: | --- |
| Valid temporary baseline | PASS | 0 | One source verified and a compact packet was written. |
| Missing required source file | PASS | 2 | `required source missing`; no packet. |
| Empty `source_refs` | PASS | 2 | `source_refs must be a non-empty array`. |
| Evidence cites undeclared ref | PASS | 2 | `evidence cites unknown source refs: not-declared`. |
| Wrong SHA-256 | PASS | 2 | `source hash mismatch`; no packet. |
| Duplicate source-ref ID | PASS | 2 | `duplicate source ref id: duplicate`. |
| Duplicate evidence-item ID | PASS | 2 | `duplicate evidence item id: fact-1`. |
| Source is 65,537 bytes | PASS | 2 | `source exceeds per-file limit`; no packet. |
| Five 65,536-byte sources | PASS | 2 | `sources exceed total limit: 327680 bytes`; no packet. |
| Direct path outside allow-root | PASS | 2 | `source is outside allowed roots or not a file`. |
| In-root symlink to outside file | PASS | 2 | Resolved escape was rejected with the same allow-root error. |
| Same-size source change after verify, before render | **FAIL** | 0 | Packet contained changed text but retained the old SHA-256; CLI reported `status: ok`. |

Harness summary on each run:

```text
SUMMARY protective_passes=11 total_probes=12
```

The count includes the valid baseline among the 11 passes.

## Exact commands

The temporary harness was created at
`/tmp/mosm_t4_runtime_reliability_20260718/T4_probe.py`; its SHA-256 was
`296c92b2d5368d01f1821bd494ee5f7d9c6dcc7f9f9c269365959f16ce244993`.
It created each fixture tree with Python `tempfile.TemporaryDirectory`, invoked
the target as a subprocess for the validation probes, and removed each fixture
tree on exit.

Commands issued:

```sh
test ! -e /tmp/mosm_t4_runtime_reliability_20260718 && mkdir -p /tmp/mosm_t4_runtime_reliability_20260718
python3 -m py_compile /tmp/mosm_t4_runtime_reliability_20260718/T4_probe.py && shasum -a 256 /tmp/mosm_t4_runtime_reliability_20260718/T4_probe.py
python3 /tmp/mosm_t4_runtime_reliability_20260718/T4_probe.py
python3 /tmp/mosm_t4_runtime_reliability_20260718/T4_probe.py
python3 -c 'from pathlib import Path; import shutil; p=Path("/tmp/mosm_t4_runtime_reliability_20260718").resolve(); assert p.parent == Path("/private/tmp") and p.name == "mosm_t4_runtime_reliability_20260718"; shutil.rmtree(p); assert not p.exists()'
shasum -a 256 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py
```

Both harness invocations exited 1 because the harness treats the reproduced
stale-read as an overall QA failure. The individual parser outcomes are in the
table above.

The first run generated these exact target command vectors. Paths under the
`fixtures-xg37lkd0` directory were temporary and were deleted automatically:

```text
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/baseline.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/baseline.md"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/missing_required_source.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/missing_required_source.md"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "validate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/empty_source_refs.json"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "validate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/unknown_evidence_ref.json"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/wrong_hash.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/wrong_hash.md"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "validate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/duplicate_source_ref_id.json"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "validate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/duplicate_evidence_id.json"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/oversized_single_source.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/oversized_single_source.md"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/oversized_aggregate.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/oversized_aggregate.md"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/outside_allow_root.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/outside_allow_root.md"]
["/opt/homebrew/opt/python@3.14/bin/python3.14", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/mosm_tube.py", "rehydrate", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/symlink_escape.json", "--allow-root", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/allowed", "--output", "/tmp/mosm_t4_runtime_reliability_20260718/fixtures-xg37lkd0/symlink_escape.md"]
```

## Reproducible stale-read

The controlled probe imported the unmodified target, wrapped
`verify_sources()` only in process, and changed the source immediately after
the original verifier returned and immediately before `main()` called
`render_packet()`:

```python
original_verify = module.verify_sources

def verify_then_mutate(value, roots):
    verified = original_verify(value, roots)
    source.write_text("version-two\n", encoding="utf-8")
    return verified

module.verify_sources = verify_then_mutate
exit_code = module.main()
```

The original and replacement strings were both 12 bytes, ruling out size drift
as an incidental signal.

Observed on both runs:

```text
exit=0
original_sha=89c04515823a2b8904a7b94eb9e403dd1a6af7521a6af8c7ef41bc6bc30e0c8f
rendered_source_sha=cf0feff65eb1c8d3f640caad9d41950bffa11efe9bcf65329c09dce875b2705e
same_size=True
packet_contains_replacement=True
packet_reports_original_sha=True
packet_reports_replacement_sha=False
stdout={"status": "ok", "tube_id": "t4-temporary-fixture", "verified_sources": 1, "packet_mode": "compact", ...}
```

This is a verify/use time-of-check-to-time-of-use stale-read. `verify_sources()`
hashes each path and stores the path plus verified metadata
(`prototype/mosm_tube.py:171-182`). `render_packet()` later reopens that path
and reads its current text without comparing it to the verified bytes or
rehashing (`prototype/mosm_tube.py:209-220`). A source edit or replacement in
that interval can therefore make the packet body disagree with the packet's
own SHA-256 while still returning success.

## Cleanup and mutation boundary

The dedicated temporary root was removed and its absence asserted. No optional
raw logs were retained. The only persistent file created by this pass is this
report; `prototype/mosm_tube.py` was not edited.
