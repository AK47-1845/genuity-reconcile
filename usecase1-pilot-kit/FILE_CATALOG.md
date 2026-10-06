# File catalog

This catalog explains what every part of the bundle is for. Paths are relative to `Genuity2.0 usecase1/`.

## Root files

| File | Purpose | Primary reader |
|---|---|---|
| `README.md` | Very short entry point pointing to the complete guide | Everyone |
| `START_HERE.md` | Full business, technical, operational, safety, and pilot orientation | Everyone |
| `DEMO.md` | Exact first LTTS demonstration, narrative, data request, gates, questions and objection handling | Founder/sales/engineering |
| `HOW_TO_USE.md` | Concise operating, input, review, release, evaluation and customization guide | Engineering/quality |
| `FOUNDERS.md` | Company direction, product logic, four-month LTTS plan, research handoff, risks and commercial roadmap | Founder/leadership |
| `FILE_CATALOG.md` | This file-by-file map | Everyone |
| `pyproject.toml` | Standalone Python package/build definition; the use case has no third-party runtime dependencies | Engineering/release |
| `run_demo.cmd` | Windows Command Prompt one-command demo using bundled source | Evaluator/engineering |
| `run_demo.ps1` | PowerShell one-command demo using bundled source | Evaluator/engineering |
| `verify_everything.cmd` | Runs 51 tests and independent artifact verification | Evaluator/QA |
| `verify_everything.ps1` | PowerShell equivalent of the full verification | Evaluator/QA |

## `docs/`

| File | Purpose |
|---|---|
| `EXECUTIVE_BUSINESS_CASE.md` | Decision memo: buyer, value equation, economics, 90-day plan, commercial model, gates, risks, and honest billion-dollar interpretation |
| `MARKET_EVIDENCE_AND_PILOT.md` | Primary-source manufacturing/AI references, official price anchors, 10,000-page pilot design, acceptance gates, and commercialization approach |
| `TECHNICAL_GUIDE.md` | Detailed original implementation guide and command reference |
| `DEPENDENCY_AND_LICENSE_NOTES.md` | Runtime dependency boundary, missing-license warning, and production due-diligence checklist |
| `ORIGINAL_PROJECT_DIRECTIVE.txt` | Exact source brief that defined the business objective, engineering rules, ten behaviors, cost requirements, and demonstration targets |
| `BRUTAL_REVIEW_LOG.md` | Fatal assumptions, version 1.1 changes, remaining rejection reasons and claim boundaries |
| `V1_1_FINAL_VERIFICATION.md` | Exact wheel hash, tests, demo evidence, release decision, documentation checks, Axiom cross-check and remaining gaps |
| `LTTS_ADJACENT_WORKFLOW_ROUTER.md` | Scored map of seven adjacent LTTS workflows, reuse boundaries, routing questions and stop conditions |

## `domain_packs/`

| File | Purpose |
|---|---|
| `industrial_material_packet.json` | Versioned policy/configuration for document types, aliases, required/critical fields, authorities, joins, normalization, permitted reconstruction, imputation, review, and pricing |

Copy and version this file for a client deployment. Client quality owners must approve policy content. The runtime validates it before processing.

## `templates/`

| File | Purpose |
|---|---|
| `CLIENT_TRUTH_TEMPLATE.csv` | Starting schema for independently adjudicated blind truth used by the `evaluate` command |
| `PILOT_SCORECARD_TEMPLATE.csv` | Baseline/target/actual/result/evidence scorecard for a falsifiable pilot |
| `REVIEW_RESOLUTION_TEMPLATE.csv` | Input template for reviewer dispositions and the hash-chained review-ledger command |
| `RELEASE_APPROVAL_TEMPLATE.json` | Named, target- and scope-bound operational staging approval template |
| `LTTS_WORKFLOW_SELECTION_TEMPLATE.csv` | Evidence-based scorecard for choosing the first LTTS workflow rather than selecting by enthusiasm |
| `LTTS_PILOT_TELEMETRY_TEMPLATE.csv` | Packet-level precision, coverage, exception, time, model, cost, latency and release telemetry |
| `CLIENT_ADAPTER_MAPPING_TEMPLATE.csv` | Source-to-canonical field, unit, identity, authority, criticality and recovery mapping |

## `source/genuity_reconcile/`

| File | Responsibility |
|---|---|
| `__init__.py` | Package identity and public metadata |
| `__main__.py` | Enables `python -m genuity_reconcile` |
| `cli.py` | Commands: `demo`, `run`, `batch`, `verify`, `estimate`, `evaluate`, review-ledger commands, and `release-check` |
| `models.py` | Serializable evidence, field-decision, document, metrics, and pipeline-result data models |
| `config.py` | Default domain-pack resolution plus fail-closed configuration validation |
| `contracts.py` | Portable JSON Schemas for OCR input and field-decision output |
| `adapters.py` | Existing-OCR JSON ingestion, validation, classification, content deduplication, and simulated crop-model adapter/cache |
| `pipeline.py` | Core normalization, reconstruction, linking, validation, conflict handling, graph building, economics, exports, SQLite, scorecard, manifest, and demo orchestration |
| `audit.py` | 21 provenance and policy invariants plus fail-closed enforcement |
| `economics.py` | Token arithmetic, five-arm cost comparison, scale/sensitivity scenarios, and editable ROI estimator |
| `evaluation.py` | Blind-truth precision, automatic coverage, abstention, and incorrect-auto-accept evaluation |
| `verification.py` | Independent manifest, path, hash, semantic, domain-pack, resilience, and SQLite verification |
| `batch.py` | Multi-packet orchestration with one connected chain per subfolder, packet isolation, verification, aggregation, and fingerprints |
| `review_ledger.py` | Validated reviewer resolution import, hash-chained decision ledger, and tamper checks |
| `release.py` | Non-compensating release gates, exact scope hashing and named role approval validation |
| `resilience.py` | Executable failure injections for malformed input, unknown types, omissions, alias collision, cache tampering, and forbidden policy |
| `fixtures.py` | Synthetic, non-confidential industrial packet and sealed controlled truth |
| `scale_benchmark.py` | 1,000-document duplicate-aware, model-free local smoke benchmark |

`__pycache__/`, if created by Python, is disposable bytecode and is not part of the logical source.

`source/genuity_reconcile_usecase1.egg-info/` is generated package metadata used during wheel construction. The authoritative package definition is the root `pyproject.toml`.

`archive/` contains superseded isolated-install and release-candidate directories retained non-destructively. It is not authoritative product source or a current release.

## `tests/`

| File | Purpose |
|---|---|
| `test_genuity_reconcile.py` | 51 focused standard-library tests covering all ten behaviors, arbitrary input isolation, safety, ambiguity, conflicts, policy, caching, tampering, export/path security, batch isolation, economics, evaluation, review/release gates, separation of duties, release-time verification, scale smoke, packaging contracts, and verifier behavior |

Run with `verify_everything.cmd` or the command documented in `START_HERE.md`.

## `demo_output/` executive and manifest files

| File | Purpose |
|---|---|
| `SUMMARY.md` | Human-readable result, core metrics, connected path, safety, and cost summary |
| `BUSINESS_CASE.md` | Generated short bottom-up economics summary |
| `run_manifest.json` | Input hashes, artifact hashes, semantic fingerprint, domain-pack identity/hash, and excluded ephemeral paths |
| `domain_pack_snapshot.json` | Exact configuration/policy used for this run |
| `operational_release.json` | Explicit sandbox/review/staging status, failed gates, required approvals and write-back prohibition |

## `demo_output/` canonical and database handoff

| File | Purpose |
|---|---|
| `canonical_records.json` | Connected canonical operational record with explicit conflict/proposal/unresolved state |
| `canonical_records.csv` | Spreadsheet/database-friendly version of the connected record |
| `genuity_demo.db` | SQLite handoff with documents, decisions, evidence, field-evidence links, exceptions, graph, validations, and metrics |
| `field_decisions.json` | Complete audit record for every observed, normalized, recovered, derived, proposed, conflicted, analytics-only, or missing field |
| `field_decisions.csv` | Tabular field-decision export; spreadsheet formula markers are neutralized |
| `field_decision.schema.json` | Machine-readable contract for a field decision |

## `demo_output/` evidence and relationships

| File | Purpose |
|---|---|
| `evidence.json` | Evidence references with document, page, region, quote, bounding box, content hash, and evidence type |
| `field_evidence_links.csv` | Many-to-many mapping from decisions to evidence IDs |
| `graph.json` | Evidence-linked nodes and edges for PO, part, BoM, spec, certificate, heat, and tests |
| `document_links.csv` | Tabular graph edges with join keys, corroboration, status, and evidence |

## `demo_output/` normalized engineering tables

| File | Purpose |
|---|---|
| `chemistry_results.csv` | Normalized chemistry values and their decision/evidence state |
| `mechanical_results.csv` | Normalized mechanical properties, including safe unit recovery |
| `material_requirements.csv` | Latest non-superseded specification limits |
| `validation_report.json` | Chemistry/mechanical validation results plus superseded-revision decisions |

## `demo_output/` exceptions and review

| File | Purpose |
|---|---|
| `exceptions.csv` | Operational exception queue in tabular form |
| `review_queue.json` | Rich reviewer work item including reason, rules, alternatives, owner, SLA, priority, blocking flag, and deduplication key |

The review queue contains the quantity conflict, same-heat chemistry proposal, crop-model proposal, analytics-only hardness value, unresolved signoff, and any other nonaccepted decision. Analytics-only items are visible but not counted as blocking review cases.

## `demo_output/` metrics, quality, and resilience

| File | Purpose |
|---|---|
| `metrics.json` | Pages, fields, cache, OCR, rules, local/external model use, tokens, review, acceptance, unresolved, and timing metrics |
| `demo_scorecard.json` | Pass/fail evidence for each of the ten required behaviors |
| `accuracy_report.json` | Controlled fixture checks, critical-field benchmark, precision/coverage, evidence coverage, and leakage boundary |
| `critical_field_benchmark.csv` | Field-by-field controlled expected/actual/acceptance/evidence result |
| `integrity_report.json` | 21 fail-closed provenance and policy checks |
| `resilience_scorecard.json` | Six executable failure-injection results |
| `scale_benchmark.json` | 1,000-document local smoke metrics, duplicates, cache hits, throughput, and scope disclaimer |

## `demo_output/` economics

| File | Purpose |
|---|---|
| `cost_report.json` | Dated pricing, vision token calculation, actual usage, conservative cache treatment, five scenarios, savings explanation, and limitations |
| `cost_comparison.csv` | Side-by-side five-arm unit-cost comparison |
| `business_case.json` | Page-level economics, scale scenarios, break-even, sensitivities, billion-value-pool thresholds, and commercial principle |
| `business_scale_scenarios.csv` | 100,000 through 1-billion-page scenario table |
| `business_sensitivity.csv` | Human hourly-cost sensitivity |

All economics are scenario arithmetic. They are not invoices, quotes, market size, revenue forecasts, or production measurements.

## `demo_output/` contracts and source fixture

| File/folder | Purpose |
|---|---|
| `ocr_input.schema.json` | Machine-readable existing-OCR input contract |
| `input_packet/raw_documents/` | Human-readable synthetic documents before mock extraction |
| `input_packet/mock_ocr/` | Vendor-neutral mock existing-OCR JSON consumed by the pipeline |
| `input_packet/fixture_manifest.json` | Sequence and raw/OCR filename mapping |
| `input_packet/ground_truth.json` | Sealed controlled truth; not located in or read from the OCR input folder |

`demo_output/.genuity_cache/` is created after a local demo run. It is disposable runtime state, excluded from `run_manifest.json`, and safe to omit when sharing verified artifacts. Every entry is independently integrity-checked before reuse.

## `release/`

This folder contains the retained 1.0.0 baseline and the current standalone `genuity_reconcile_usecase1-1.1.0` wheel. `SHA256SUMS.txt` verifies both files.

Install the wheel with:

```powershell
py -3 -m pip install release\genuity_reconcile_usecase1-1.1.0-py3-none-any.whl
```

`SHA256SUMS.txt` records the wheel's release checksum. Verify it before installation. The root `build/` directory is disposable setuptools staging created while producing the wheel; do not edit or import code from it.

## Files intentionally not included

- unrelated Genuity projects, pitch decks, resumes, PDFs, and datasets from the parent workspace;
- confidential client documents;
- model credentials, private signing keys, and any client cache from outside this synthetic demo;
- third-party dependency folders from unrelated projects;
- a license chosen without owner approval.

This keeps the handoff complete for Use Case 1 without mixing unrelated or legally ambiguous material.
