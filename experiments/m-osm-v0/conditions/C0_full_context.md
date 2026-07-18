# Condition C0: Full Context

Read only this file and `../TASK.md` before answering.

## Context

Case M-ALPHA-17 was opened by Scout-Delta. Preserve the first route identifier
when a batch contains a duplicate and round-trip a trailing comment suffix.
Production mutation is forbidden. An early probe called port 4173 canonical,
but a 09:22Z rebuild superseded it: the canonical isolated port is 4319 and
4173 must not be used.

Only `router/normalize.py` and `tests/test_normalize.py` are in scope. The public
signature and Unicode behavior of `normalize_route_id` are protected. Required
tests: `test_duplicate_route_id_preserves_first`,
`test_comment_suffix_round_trip`, and `test_unicode_route_id_unchanged`.

Create `backups/router-normalize-prepatch.diff` before editing. Never restart
`com.ompu.router`. At 09:31Z the first two tests failed and the Unicode test
passed. The exact next action is `run isolated dry-run against
fixtures/route_batch_07.json`.

Unresolved: whether malformed input with two comment suffixes should preserve
both. Do not decide it silently.
