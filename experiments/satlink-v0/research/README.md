# Independent architecture passes

These five documents were written independently before the implementation was
selected. They are preserved in full because disagreement is part of the
evidence, not noise to erase during synthesis.

| File | Lens | Important contribution |
| --- | --- | --- |
| `01_threat_model.md` | identity and hostile-carrier analysis | carrier labels are not identity; replay commit precedes projection |
| `02_protocol_selection.md` | protocol comparison | standard `minisign -> age-X25519` composition |
| `03_integration_map.md` | OMPU boundary mapping | typed verified packet and gateway-owned attribution; signed route fields |
| `04_adversarial_test_plan.md` | attack harness | deterministic failure cases and secret-free receipts |
| `05_sputnik_bootstrap.md` | transport and lifecycle | NATS NKeys/JWT, JetStream, narrow subjects, local key generation |

`ARCHITECTURE_DECISION.md` records which recommendations were accepted,
rejected, or deferred. In particular, the implementation does not use the
custom cryptographic composition from pass 04 and does not encode ciphertext
to bypass Kurilka's banlist.
