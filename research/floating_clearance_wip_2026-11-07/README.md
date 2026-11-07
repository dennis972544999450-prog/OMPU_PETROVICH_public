# Floating clearance — research in progress (v0.1-wip)

Working paper and verification script for a small mathematics thread of the OMPU agent line
Petrovich: periodic threads on a circle that must keep vertical clearances at marked times. How steep
must they be (a maximum-ratio cycle), when can the optimum be smooth (no pinched node), and what is
the exact price of curvature just above the optimal steepness ($\nu K^2/\varepsilon$, with a
circulation dual) and for all larger slopes (a finite convex program).

**Status: research in progress.** Nothing here is announced as a discovery. Each statement in the
paper carries a label (proved / checked / observation / open); open questions are listed in §9 of the
paper. The literature has not been searched.

## Contents

| file | what |
|---|---|
| `PAPER_WORKING_DRAFT_v0.1.md` | the working paper (English) |
| `COVERAGE.md` | claim → argument / check in this package / check in the workbench / status |
| `verify/fc_verify.py` | self-contained re-implementation, 76 checks (exact fractions + scipy LPs) |
| `verify/fc_verify_output.txt` | its output on 2026-11-07 (python 3.14.4, numpy 2.5.2, scipy 1.18.0) |
| `verify/asym3_closed_form.py` | the closed form $\nu=4/(1+\sqrt2+\sqrt6)^2$ for asym-3 with its KKT/dual certificate (+ output) |
| `REPRODUCTION.md` | re-run of the dated workbench scripts on 2026-11-07 |
| `REVIEW.md` | blind same-model review of v0.1 and what was changed after it |
| `SOURCES.md`, `sources_sha256.txt` | the dated workbench notes this summarizes, with hashes |
| `.zenodo.json` | draft metadata for a release (not released) |

## Run the checks

```bash
python3 -B verify/fc_verify.py          # ~30 s; exit 0 and ALL_CHECKS_PASSED (76 checks)
python3 -B verify/fc_verify.py --quick  # skips the grid LPs, ~1 s
```

Needs Python ≥ 3.9 with numpy and scipy (HiGHS). No network, no files written.

## Release route (not taken yet)

The OMPU route for papers is a GitHub repository linked to Zenodo (a release mints a DOI), see
`OMPU_shared/research/ZENODO_GITHUB_INSTRUCTIONS.md`. This folder was assembled by an unattended
scheduled run on 2026-11-07; it did **not** copy anything into a public repository, tag, release or
upload. That step, and the final choice of creators in `.zenodo.json`, belong to a live window
(Den or a facet working with him).
A candidate repository is the line's public backpack `OMPU_shared/petrovich_repos/public` (origin
`OMPU_PETROVICH_public` on GitHub, last commit 24.07.2026); whether Zenodo is switched on for it was not
checked from here.

## Provenance

Assembled by Petrovich's Anthropic facet (Claude Opus 5.5 by the harness's self-description),
scheduled slot 10:15 Europe/Berlin, 2026-11-07, from the line's dated notes of 13.10–06.11.2026.
Credits per step: §11 of the paper and `SOURCES.md`.
