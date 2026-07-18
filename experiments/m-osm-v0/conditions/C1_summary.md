# Condition C1: Ordinary Summary

Read only this file and `../TASK.md` before answering.

Scout-Delta is handling M-ALPHA-17, a no-production-change router normalization
repair. Work only in `router/normalize.py` and `tests/test_normalize.py`; preserve
the signature and Unicode behavior of `normalize_route_id`. The corrected
isolated port is 4319, replacing stale port 4173. Back up to
`backups/router-normalize-prepatch.diff`, do not restart `com.ompu.router`, and
next run the isolated dry-run against `fixtures/route_batch_07.json`. Tests cover
duplicate-first behavior, comment-suffix round-trip, and unchanged Unicode.
There is still an unresolved malformed double-comment-suffix policy question.
