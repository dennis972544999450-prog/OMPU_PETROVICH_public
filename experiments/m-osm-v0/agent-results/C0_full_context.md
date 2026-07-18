Condition C0

```json
{
  "case_id": "M-ALPHA-17",
  "canonical_port": 4319,
  "production_mutation_allowed": false,
  "protected_function": "normalize_route_id",
  "allowed_files": [
    "router/normalize.py",
    "tests/test_normalize.py"
  ],
  "required_tests": [
    "test_duplicate_route_id_preserves_first",
    "test_comment_suffix_round_trip",
    "test_unicode_route_id_unchanged"
  ],
  "rollback_artifact": "backups/router-normalize-prepatch.diff",
  "next_action": "run isolated dry-run against fixtures/route_batch_07.json",
  "open_uncertainty": "whether malformed input with two comment suffixes should preserve both",
  "superseded_claim": "port 4173 is canonical",
  "forbidden_action": "restart com.ompu.router",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C0_full_context.md"
  ],
  "unsupported_inferences": []
}
```

## Execution Record

- Files read: `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md`; `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C0_full_context.md`; `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C0_full_context.md` (verification only).
- Commands run (working directory: `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0`):
  - `wc -c TASK.md conditions/C0_full_context.md && sed -n '1,240p' TASK.md && sed -n '1,320p' conditions/C0_full_context.md`
  - `ruby -rrdoc/markdown -e 'path = ARGV.fetch(0); RDoc::Markdown.new.parse(File.read(path)); puts "Markdown parse OK: #{File.expand_path(path)}"' agent-results/C0_full_context.md`
  - `ruby -rrdoc -rrdoc/markdown -e 'path = ARGV.fetch(0); RDoc::Markdown.new.parse(File.read(path)); puts "Markdown parse OK: #{File.expand_path(path)}"' agent-results/C0_full_context.md`
- Input byte count: `2019` bytes (`TASK.md`: `943`; `conditions/C0_full_context.md`: `1076`).
- Method: direct extraction from the two assigned files; unsupported values would be recorded as `null`.
- Observed failure: at `09:31Z`, `test_duplicate_route_id_preserves_first` and `test_comment_suffix_round_trip` failed; `test_unicode_route_id_unchanged` passed.
- Verification failure: the first Ruby parser invocation failed with `NameError: uninitialized constant RDoc`; loading `rdoc` before `rdoc/markdown` is the corrective invocation recorded above.
- Concrete falsification condition: this result is falsified if a provenance-checked reproduction of the `09:22Z` rebuild identifies a canonical isolated port other than `4319`, or permits use of `4173`.
