# Blind Recall Task

Using only your assigned condition, return one JSON object with these keys:

```json
{
  "case_id": "string or null",
  "canonical_port": "integer or null",
  "production_mutation_allowed": "boolean or null",
  "protected_function": "string or null",
  "allowed_files": ["strings"],
  "required_tests": ["strings"],
  "rollback_artifact": "string or null",
  "next_action": "string or null",
  "open_uncertainty": "string or null",
  "superseded_claim": "string or null",
  "forbidden_action": "string or null",
  "producer_identity": "string or null",
  "source_reads": ["paths actually read"],
  "unsupported_inferences": ["anything guessed rather than supported"]
}
```

Do not fill a missing value from plausibility. Use `null` and record the gap.
After the JSON, report input bytes, method, failure noticed, and falsification
condition. Do not read `answer_key.json` or any other condition before writing
the result.
