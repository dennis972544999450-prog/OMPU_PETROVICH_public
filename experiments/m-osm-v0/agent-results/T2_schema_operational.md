# T2 - Part 3 schema and operational-machine-readability test

## Scope and provenance

- Received draft: `/Users/denbell/Downloads/Swarm Oscillatory Memory (M-OSM).md`
- Draft SHA-256: `2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668`
- Draft bytes: `21368`; the value matches `SOURCE_FINGERPRINT.md`.
- Claim register SHA-256: `2e1c9865466455e2453986778eb133859a0d5f88c5cdccf0fdd067b5ee8ac69b`
- Tested claims: machine readability of Part 3; `MOSM-C04`, `MOSM-C05`, and the unit/trigger portions of `MOSM-C06`-`MOSM-C08`.
- No live service, bus, source draft, claim register, condition, fixture, or prototype was modified.

## Verdict

| Surface | Result | Evidence |
|---|---|---|
| Part 3, unchanged | **FAIL** | Python and `jq` reject the first Markdown escape, `\_`. |
| Part 3, smallest documented Markdown unescape | **PASS** | Delete 195 backslashes before invalid-JSON Markdown punctuation; Python and `jq` then parse the object. |
| Identification Tube schema | **PARTIAL SHAPE ONLY** | It enforces required fields, eight phase numbers, and `r` bounds, but accepts scalars and semantic nonsense. |
| Hash recoverability (`MOSM-C05`) | **FAIL / NOT SPECIFIED** | The schema declares no hash, algorithm, canonicalization, decoder, candidate corpus, or source relation. |
| Dimensional and unit consistency | **MIXED, OPERATIONALLY FAILING** | Some conversions agree, but the `r` equality exceeds its range and `r < Kc` compares different roles/dimensions. |
| Fresh-process rehydration (`MOSM-C04`) | **FAIL** | Two isolated processes recover only explicit fields; an identical valid tube cannot distinguish two different hidden contexts. |

Part 3 is therefore **Markdown-repairable JSON, not strict JSON as received**. Successful parsing after export repair does not make the embedded tube an operational context-rehydration mechanism.

## Exact extraction and parse

Extraction rule: between the exact Part 3 and Part 4 headings, require the standalone line `JSON  `, then copy from the first `{` after that marker through the last `}`, inclusive. No byte inside those boundaries is changed.

- Source byte offsets: `[11694, 19678)`
- Extracted bytes: `7984`
- Extracted SHA-256: `9b0a6db30f562d5d8b6dc9bdeb0e7cad0eb85ebd13c79c0b8886cb9053bd5780`
- Raw block: `raw/T2_part3_raw_block.txt`

Primary command, run from the experiment root:

```sh
python3 tools/T2_schema_operational.py
```

The harness performed Python `json.loads` on the unchanged substring:

```text
JSONDecodeError: Invalid \escape: line 2 column 10 (char 13)
```

It independently invoked:

```sh
/usr/bin/jq -e . /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/raw/T2_part3_raw_block.txt
```

Exit `5`:

```text
jq: parse error: Invalid escape at line 2, column 20
```

## Minimal Markdown unescape

Rule: delete a backslash only when its following character is ASCII punctuation and is not a valid JSON escape initial (`"`, `\`, `/`, `b`, `f`, `n`, `r`, `t`, `u`). Do not strip whitespace, rename keys, change values, evaluate formulas, or normalize line endings inside the extraction.

Observed deletions: `_` 175, `*` 6, `-` 3, `[` 3, `]` 3, `+` 2, `=` 2, `>` 1; total **195**. Each deletion repairs one otherwise-invalid JSON escape. The event-by-event offsets are in `raw/T2_unescape_manifest.json`.

After that transformation, Python `json.loads` returns a top-level object and this command exits `0` with empty stderr:

```sh
/usr/bin/jq -e . /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/raw/T2_part3_markdown_unescaped.json
```

A second T2 extraction receipt selected the same object plus its terminal LF (`7985` bytes, SHA-256 `496b4929238e0f74eba85eed1c1508975d15d5e818d1c5489541492e08acd505`) and independently reported the same 195 deletions and parse outcomes in `raw/T2_parse_receipt.json`. The one-byte boundary difference does not affect either strict parser. Because the earlier implementation was concurrently replaced at the same tool path, treat this as repeat evidence, not a fully independent external replication.

## Schema validation

The dependency-free evaluator implements every assertion keyword used by the embedded schema: `type`, `properties`, `required`, `items`, `minItems`, `maxItems`, `minimum`, `maximum`, and `additionalProperties`. Under standard JSON Schema semantics:

- Positive: missing `tube_id`, seven `phase_state` items, and `coherence_index_r = 1.01` are rejected.
- Root failure: there is no `type: object`; `object_type` is an unregistered/ignored keyword. Scalar `7` therefore validates.
- Open-world failure: there is no `additionalProperties: false`.
- Semantic counterexample that validates: `tube_id = "not-a-uuid"`, target `M9_NOT_DEFINED`, empty anchors, beta `-999`, one-element momentum, and an undeclared payload.
- No `$schema` dialect, schema/version field, UUID format, target enum, anchor minimum, beta bounds, momentum dimensionality, provenance, context, interaction history, or hash property is declared.
- The existing C2 tube's `attractor_state_hash` is accepted only as an undeclared extra property; it is not part of the embedded contract.

Raw checks: `raw/T2_schema_checks.json` and the agreeing `raw/T2_schema_validation.json`.

## Hash and context counterexamples

For a concrete SHA-256 variant, a supplied five-interaction candidate verifies against its digest and an altered candidate does not. From the digest alone, recovery is `null`: no inverse operation or candidate corpus exists. This is the distinction between **verification of a supplied preimage** and **recovery of a missing preimage**. See `raw/T2_hash_recoverability.json` and `raw/T2_hash_only_stdout.json`.

The stronger context counterexample associates one schema-valid tube with two distinct contexts whose protected function, forbidden action, and uncertainty all differ. A deterministic fresh process receives identical bytes for both, so it must emit identical output and cannot be correct for both contexts. The schema contains no encoder invariant that forbids this collision-by-omission. See `raw/T2_rehydration_counterexample.json` and `raw/T2_hash_counterexample.json`.

Fresh-process commands/receipts:

```sh
/opt/homebrew/opt/python@3.14/bin/python3.14 -I /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/tools/T2_fresh_process_probe.py --mode tube-only < /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/raw/T2_fresh_process_input.json
/opt/homebrew/opt/python@3.14/bin/python3.14 -I /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/tools/T2_fresh_process_probe.py --mode hash-only < /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/raw/T2_hash_only_input.json
```

Both exit `2`: `insufficient_information` and `hash_not_recovered`. A separate `-I -S` probe disabled post-startup file reads, accepted only stdin, recovered `0/3` hidden fields for both contexts, and returned `explicit_tube_fields_only`; exact argv and environment are in `raw/T2_fresh_process_receipt.json`.

## Dimensional and unit audit

- Arithmetic: `Kc = 2 * (0.25 + 0.12) = 0.74` passes numerically.
- Range failure: the declared equality gives `r = sqrt(3.45 - 0.74) = 1.6462077633154328`, above the schema maximum `1.0`. Part 1 described proportional scaling; Part 3 turned it into an unscaled equality.
- Dimensional failure unless unstated normalization exists: if `K`, `gamma`, and `D` carry frequency units, `sqrt(K - Kc)` has square-root-frequency units, not dimensionless coherence.
- Trigger failure: execution step 4 compares dimensionless `r` with coupling/frequency threshold `Kc`.
- Unbound units: fixed hertz values have no scheduler clock or operation-to-cycle map; `omega_k` also normally denotes angular frequency while the values are cycles/s. The 12.4 dB gain has no amplitude/power ratio or reference level.
- Consistent checks: 1.2 km equals 1200 m; 100000 ms equals 100 s; 1200000 ms equals 1200 s; 0.174 rad is about 9.97 degrees.

Raw checks: `raw/T2_unit_checks.json` and `raw/T2_dimensional_consistency.json`.

## Falsification and promotion conditions

1. **Strict-as-received conclusion:** falsified if a standards-compliant strict JSON parser accepts the extracted bytes at the recorded source hash with zero transformation. Parser-specific permissive modes do not count.
2. **Minimal-unescape conclusion:** falsified if reproducing the stated rule changes anything besides the 195 listed backslashes, or if a strict parser still rejects the output.
3. **Schema inadequacy:** overcome by a versioned JSON Schema dialect/root object contract that rejects both scalar and semantic counterexamples while accepting preregistered valid tubes.
4. **Hash recovery:** `MOSM-C05` needs a defined digest algorithm, canonicalization, domain, and blind recovery test. A hash can support candidate verification or external lookup; arbitrary preimage recovery from the digest alone is not an operational mechanism.
5. **Fresh rehydration:** `MOSM-C04` needs a preregistered blind fresh-process benchmark that recovers hidden facts, corrections, constraints, and uncertainty above equal-budget summary/baseline performance without source files, model-session state, retrieval, or a candidate corpus.
6. **Dimensional consistency:** requires explicit nondimensionalization/scaling, a bounded `r` equation over the supported parameter domain, a dimensionally valid trigger, and an executable mapping from hertz/dB fields to measured scheduler variables.

The promotion rule in `CLAIMS.md` is not met: the syntax repair is reproducible, but the context-recovery mechanism lacks an operational decoder, survives counterexamples poorly, and has no positive blind recovery result.
