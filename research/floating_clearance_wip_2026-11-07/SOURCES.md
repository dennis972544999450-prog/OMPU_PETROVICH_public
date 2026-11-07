# Sources — floating clearance, v0.1-wip

The paper summarizes dated notes in the OMPU workbench
`OMPU_shared/petrovich_garage_v0/workbench/` (local to the OMPU host; not part of this package).
Each folder holds a `notes.txt` in Russian (the primary text, with proofs or sketches), the code
that produced its numbers, and the recorded outputs. Notes are never edited after the day they were
written; later corrections are separate files next to them (`CORRECTION_*.md`, `SEE_ALSO_*.md`).

SHA-256 prefixes below were taken on 2026-11-07 (full hashes: `sources_sha256.txt`).

| folder | files | primary texts |
|---|---|---|
| `floating_clearance_2026-10-13` | 4 | `notes.txt` `d5b59b645153aaed…` |
| `floating_clearance_2026-10-14` | 7 | `notes.txt` `da2b094d2b9b22ba…` |
| `floating_clearance_2026-10-19` | 6 | `notes.txt` `ac6969d99f83f9f3…` |
| `floating_clearance_2026-10-29` | 1 | `notes.txt` `17e2568fd62df32b…` |
| `floating_clearance_2026-10-29-anthropic` | 6 | `notes.txt` `212fa01ca20b6fea…` |
| `floating_clearance_2026-10-30-anthropic` | 3 | `notes.txt` `82f65346537cef99…` |
| `floating_clearance_2026-10-31-anthropic` | 3 | `notes.txt` `f066adaeea9046ba…` |
| `floating_clearance_2026-11-01-anthropic` | 4 | `CORRECTION_20261101.md` `affae4e9edc0da89…`<br>`notes.txt` `81c3cfdcc11700ce…` |
| `floating_clearance_2026-11-02-anthropic-1015` | 167 | `notes.txt` `74ee75f8fe832cea…` |
| `floating_clearance_2026-11-02-anthropic-1315` | 3 | `notes.txt` `ce36d7ab59f92c13…` |
| `floating_clearance_2026-11-03-anthropic-1315` | 11 | `notes.txt` `db98d3e4ddcb77e7…` |
| `floating_clearance_2026-11-04-anthropic-1315` | 6 | `CORRECTION_20261106.md` `1a9b25f022dc0234…`<br>`notes.txt` `0f12b3bd0d091d5c…` |
| `floating_clearance_2026-11-06-anthropic-1015` | 55 | `SEE_ALSO_20261106-1315.md` `b1c2b40f75e77f2b…`<br>`notes.txt` `a7aa5f0a06a6770f…` |
| `floating_clearance_2026-11-06-anthropic-1315` | 33 | `notes.txt` `0a5c35db04cb5668…` |
| `floating_clearance_2026-11-06-anthropic-manual` | 9 | `SEE_ALSO_20261106-1015.md` `f930e05d30c30ae1…`<br>`notes.txt` `7a0842c8cd76577a…` |

Authorship by folder: `10-13`, `10-14` — Petrovich's Grok facet; `10-19` — Claude Code facet
(Fable 5.1 per harness); `10-29` (no suffix) — GLM facet (glm-5.1 per UI), night note, the
three-thread question; all `…-anthropic*` folders — Anthropic facet (Fable 5.1 or Opus 5.5 per
harness, slot named in the folder), with same-model subagents whose files sit in `probe_*/`,
`review/` and `scratch_salvage_1315/`. Arc-constraint model and node reduction: Kimi facet,
`Documents/kimi/workspace/petrovich-line/continuous-arc/NOTES.md` (29.10).

Line conventions that matter for reading: dates are Europe/Berlin; "slot 10:15/13:15/16:45/20:15" is
the scheduled run that wrote the note; model names are the harness's self-description, not a measured
attestation; "checked" in a note means checked by the same line's code unless another hand is named.
