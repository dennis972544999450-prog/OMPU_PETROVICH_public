# R2 - Independent replication of the two core T2 claims

## Scope and blind-order receipt

This pass independently tested only:

1. Whether the Part 3 payload is strict JSON unchanged, and whether the smallest stated removal of Markdown-invalid escape backslashes makes it strict JSON.
2. Whether the numeric constants in Part 3 give the stated `Kc` and draft `r` values.

Frozen source:

`/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/source/Swarm_Oscillatory_Memory_M-OSM_received_v4.md`

During the blind phase I did not read T2 scripts, T2 raw files, or the T2 report. I wrote the independent measurements to `raw/R2_replication.json` at `2026-07-18T12:10:44Z`. Only after that commit did I read `agent-results/T2_schema_operational.md`, solely for comparison, at `2026-07-18T12:11:34Z`. I did not read T2 scripts or T2 raw files after the blind phase either.

## Frozen hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Frozen source | 21368 | `2367703aff86e220faacb8748d14812ba5978540fba42f0beb1b2146a2a97668` |
| R2 extracted payload, including terminal LF | 7985 | `496b4929238e0f74eba85eed1c1508975d15d5e818d1c5489541492e08acd505` |
| R2 repaired payload, including terminal LF | 7790 | `3c2f0dbd3be1bb4369a8ffb6754a435ce8cae2026262a679f751c9eccbe1ca01` |
| T2 comparison report | not used as an experimental input | `6a8def904486f79ee39ca3b64866927a5fe9ab21566df7fde0c0d55ec1c10225` |

## Claim 1: Part 3 JSON operability

### Extraction

The independent extraction algorithm was:

1. Find the heading matching `^## \*\*Part 3:`.
2. Bound the section at the next heading matching `^## \*\*Part 4:`.
3. Inside that section, require the standalone marker line `JSON  `.
4. Preserve all bytes from the first following line beginning with `{` through the last nonblank line before Part 4, including the terminal LF on the final `}` line.

The source coordinates were Part 3 heading line 113, marker line 117, JSON lines 118-253, and Part 4 heading line 255. The extracted payload is 7985 bytes.

### Strict parse unchanged

Python 3.14.4 `json.loads` rejected the unchanged extracted bytes:

```text
JSONDecodeError: Invalid \escape: line 2 column 10 (char 13)
```

Result: **FAIL unchanged**.

### Smallest Markdown-invalid-escape removal

The repair removed one backslash only when it immediately preceded an observed character that is not a valid JSON escape initial. No whitespace, line ending, key, value, or other byte was changed.

| Following character | Backslashes removed |
|---|---:|
| `_` | 175 |
| `*` | 6 |
| `-` | 3 |
| `[` | 3 |
| `]` | 3 |
| `+` | 2 |
| `=` | 2 |
| `>` | 1 |
| **Total** | **195** |

After exactly those 195 deletions, `json.loads` parsed the payload. The parsed top-level keys were `system_metadata`, `theoretical_parameters_db`, `motivational_goal_vectors`, `identification_tube_schema`, and `execution_loop_protocol`.

Result: **PASS after the stated 195-byte repair**.

## Claim 2: `Kc` and draft `r`

The repaired payload contains:

```text
K = 3.45
D = 0.12
gamma = 0.25
Kc = 2 * (gamma + D)
r = sqrt(K - Kc)
```

Independent arithmetic:

```text
Kc = 2 * (0.25 + 0.12)
   = 0.74

K - Kc = 3.45 - 0.74
        = 2.71

draft r = sqrt(2.71)
        = 1.6462077633154328
```

This replicates the draft arithmetic only. It does not establish that the unscaled `r` equation is physically or schema-valid; the computed value is greater than 1.

## Comparison with T2

| Measurement | R2 independent result | T2 report | Comparison |
|---|---|---|---|
| Frozen source hash and bytes | Same values above | Same values | **AGREE** |
| Strict parse unchanged | Invalid escape at line 2, column 10, char 13 | Same Python error | **AGREE** |
| Repair rule | Delete only invalid-JSON Markdown escape backslashes | Same rule | **AGREE** |
| Edit total and distribution | 195 with counts above | Same total and every per-character count | **AGREE** |
| Strict parse after repair | Pass | Pass | **AGREE** |
| `Kc` | `0.74` | `0.74` | **AGREE** |
| Draft `r` | `1.6462077633154328` | `1.6462077633154328` | **AGREE** |

There is no substantive disagreement. T2's primary extraction excludes the LF after the terminal `}` and therefore reports 7984 bytes with SHA-256 `9b0a6db30f562d5d8b6dc9bdeb0e7cad0eb85ebd13c79c0b8886cb9053bd5780`. R2 includes that LF. T2 separately records the same terminal-LF convention as R2: 7985 bytes and SHA-256 `496b4929238e0f74eba85eed1c1508975d15d5e818d1c5489541492e08acd505`. The one-byte boundary convention does not affect either parse result or the arithmetic.

T2 findings about schema semantics, hash recovery, fresh-process rehydration, and other units were intentionally not replicated and are outside R2 scope.

## Falsification conditions

1. **Unchanged strict-JSON result:** falsified if a standards-compliant strict JSON parser accepts the exact extracted bytes at source SHA-256 `2367703a...a97668` with zero transformation.
2. **Minimal repair result:** falsified if the stated rule changes any byte other than the 195 recorded backslashes, produces different per-character counts, or still fails strict parsing.
3. **Boundary robustness:** falsified if including versus excluding only the terminal LF changes strict parsing, repaired parsing, edit counts, or parsed values.
4. **`Kc` arithmetic:** falsified if the frozen payload does not provide `K=3.45`, `D=0.12`, `gamma=0.25`, and `Kc=2*(gamma+D)`, or if exact recomputation does not yield `0.74`.
5. **Draft `r` arithmetic:** falsified if the frozen payload does not state `r=sqrt(K-Kc)`, or if recomputation from the recorded constants does not yield `sqrt(2.71) = 1.6462077633154328` under ordinary binary64 evaluation.

## Exact commands

Source fingerprint:

```sh
shasum -a 256 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/source/Swarm_Oscillatory_Memory_M-OSM_received_v4.md
wc -lc /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/source/Swarm_Oscillatory_Memory_M-OSM_received_v4.md
```

Independent extraction, parse, repair, edit count, hashes, and arithmetic:

```sh
python3 - <<'PY'
from pathlib import Path
import collections
import hashlib
import json
import math
import re

source = Path('/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/source/Swarm_Oscillatory_Memory_M-OSM_received_v4.md')
raw = source.read_bytes()
text = raw.decode('utf-8')
lines = text.splitlines(keepends=True)
part3_i = next(i for i, line in enumerate(lines) if re.match(r'^## \*\*Part 3:', line))
part4_i = next(i for i, line in enumerate(lines) if i > part3_i and re.match(r'^## \*\*Part 4:', line))
marker_i = next(i for i in range(part3_i + 1, part4_i) if re.match(r'^JSON[ \t]*(?:\r?\n)?$', lines[i]))
json_start_i = next(i for i in range(marker_i + 1, part4_i) if lines[i].lstrip().startswith('{'))
json_end_i = max(i for i in range(json_start_i, part4_i) if lines[i].strip())
payload = ''.join(lines[json_start_i:json_end_i + 1])

try:
    json.loads(payload)
    strict = {'ok': True}
except json.JSONDecodeError as exc:
    strict = {'ok': False, 'message': exc.msg, 'line': exc.lineno,
              'column': exc.colno, 'character_offset': exc.pos}

invalid_followers = collections.Counter(
    m.group(1) for m in re.finditer(r'\\(.)', payload)
    if m.group(1) not in '"\\/bfnrtu'
)
markdown_escape_chars = ''.join(sorted(invalid_followers))
repaired, edit_count = re.subn(
    r'\\(?=[' + re.escape(markdown_escape_chars) + r'])', '', payload
)
parsed = json.loads(repaired)
core = parsed['theoretical_parameters_db']['kuramoto_core']
K = core['coupling_strength_K']
D = core['intrinsic_noise_floor_D']
gamma = core['frequency_dispersion_gamma']
Kc = 2 * (gamma + D)
draft_r = math.sqrt(K - Kc)

print(json.dumps({
    'source_sha256': hashlib.sha256(raw).hexdigest(),
    'payload_bytes': len(payload.encode('utf-8')),
    'payload_sha256': hashlib.sha256(payload.encode('utf-8')).hexdigest(),
    'strict_parse_unchanged': strict,
    'invalid_escape_followers': dict(sorted(invalid_followers.items())),
    'edit_count': edit_count,
    'repaired_sha256': hashlib.sha256(repaired.encode('utf-8')).hexdigest(),
    'repaired_top_level_keys': list(parsed),
    'K': K, 'D': D, 'gamma': gamma, 'Kc': Kc,
    'K_minus_Kc': K - Kc, 'draft_r': draft_r,
}, ensure_ascii=False, indent=2))
PY
```

Post-commit comparison, and only this T2 file:

```sh
shasum -a 256 /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/T2_schema_operational.md
nl -ba /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/T2_schema_operational.md
```
