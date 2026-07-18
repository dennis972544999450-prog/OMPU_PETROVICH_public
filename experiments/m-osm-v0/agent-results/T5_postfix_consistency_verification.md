# T5 Post-Fix Consistency Verification

Verified: 2026-07-18 14:22:37 CEST

## Result

**PASS.** Against the current `prototype/mosm_tube.py`, `render_packet` used
the bytes preserved by `verify_sources`; it did not reread or emit the later
replacement from the temporary path.

## Temporary-File Reproduction

The T4 timing experiment was repeated in an isolated `TemporaryDirectory`:

1. Copied the harmless version-one fixture bytes from
   `fixtures/case-alpha/full_context.md` to a temporary `source.md`.
2. Pointed an in-memory copy of the case-alpha tube at that temporary file and
   called `verify_sources(tube, [temp_root])`.
3. Replaced the temporary file with the harmless version-two bytes
   `This is a harmless later replacement.\n`.
4. Called `render_packet(tube, verified)` using the already returned
   verification record.

Observed byte evidence:

- version one: `1365` bytes, SHA-256
  `a1eee6c51f51f38a2332f2024a3dc400893f7e0349ff37ead02d9b5e2e8a0b7c`
- returned record: `1365` bytes, the same SHA-256, and its UTF-8 text encoded
  back to exactly the version-one bytes
- version two: `38` bytes, SHA-256
  `1976a1faa408005ba03c5fcb381feab6882550731155f1304fcb17b454a33845`
- the temporary path contained exactly version two before rendering
- the rendered packet contained the complete version-one byte sequence
  exactly once
- the rendered source body was exactly equal to version one
- the rendered packet did not contain version two

All assertions passed.

## Prototype Test Suite

Command:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/prototype/test_mosm_tube.py
```

Result:

```text
..........
----------------------------------------------------------------------
Ran 10 tests in 0.002s

OK
```

## Mutation Boundary

No implementation, fixture, tube, or live surface was modified. The temporary
file was removed with its temporary directory. The only persistent output from
this verification is this receipt; no optional raw artifact was needed.
