Condition C1.

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
    "duplicate-first behavior",
    "comment-suffix round-trip",
    "unchanged Unicode"
  ],
  "rollback_artifact": "backups/router-normalize-prepatch.diff",
  "next_action": "Run the isolated dry-run against fixtures/route_batch_07.json.",
  "open_uncertainty": "The malformed double-comment-suffix policy is unresolved.",
  "superseded_claim": "The isolated port is 4173.",
  "forbidden_action": "Restart com.ompu.router.",
  "producer_identity": "Scout-Delta",
  "source_reads": [
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md",
    "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C1_summary.md"
  ],
  "unsupported_inferences": []
}
```

## Execution Record

- Files read:
  - `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md` (943 bytes)
  - `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C1_summary.md` (704 bytes)
  - `/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C1_summary.md` (self-read only for Markdown verification after writing)
- Total input byte count: 1647 bytes.
- Commands run:
  - `python3 -c 'from pathlib import Path\nfor s in ("/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/TASK.md", "/Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/conditions/C1_summary.md"):\n p=Path(s); b=p.read_bytes(); print(f"<<<FILE {s} BYTES {len(b)}>>>"); print(b.decode("utf-8")); print("<<<END>>>")'`
  - `ruby -e 'require "kramdown"; p=ARGV.fetch(0); source=File.binread(p); raise "wrong condition" unless source.start_with?("Condition C1.\\n"); doc=Kramdown::Document.new(source); raise "markdown errors: #{doc.warnings.join("; ")}" unless doc.warnings.empty?; puts "Markdown parsed: #{p}"' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C1_summary.md`
  - `ruby -e 'require "rdoc/markdown"; p=ARGV.fetch(0); source=File.binread(p); raise "wrong condition" unless source.start_with?("Condition C1.\\n"); RDoc::Markdown.new.parse(source); puts "Markdown parsed: #{p}"' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C1_summary.md`
  - `ruby -e 'require "rdoc"; require "rdoc/markdown"; p=ARGV.fetch(0); source=File.binread(p); raise "wrong condition" unless source.start_with?("Condition C1.\\n"); RDoc::Markdown.new.parse(source); puts "Markdown parsed: #{p}"' /Users/denbell/OMPU_shared/petrovich_repos/public/experiments/m-osm-v0/agent-results/C1_summary.md` (run twice, including final verification)
- Method: byte-read the two assigned UTF-8 Markdown inputs, extracted only explicit claims, wrote the assigned result, and parsed it as Markdown.
- Observed failure: port `4173` is stale and is superseded by corrected isolated port `4319`; the malformed double-comment-suffix policy remains unresolved. Verification also found that `kramdown` is not installed and that `rdoc/markdown` raises `NameError` unless `rdoc` is required first.
- Concrete falsification condition: this answer is falsified if an authorized oracle shows that M-ALPHA-17's corrected isolated port is not `4319`, or that production mutation or restarting `com.ompu.router` is allowed for this repair.
