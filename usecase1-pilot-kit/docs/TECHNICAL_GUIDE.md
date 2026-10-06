# Genuity evidence-first industrial reconciliation

This proof plugs into existing OCR output. It does not replace a client's OCR stack.

## Run the complete demonstration

Windows:

```text
run_demo.cmd
```

Cross-platform equivalent:

```text
python -m genuity_reconcile demo --output-dir demo_output
```

The command generates a 12-page non-confidential procurement/material packet, consumes mock existing-OCR JSON, runs a duplicate-aware 1,000-page smoke benchmark, and writes database-ready records, evidence, graph, exceptions, validation, accuracy, integrity, scale, and economics outputs.

## Process an OCR-result folder

```text
py -3 -m genuity_reconcile run --ocr-dir <folder> --output-dir <folder> --domain-pack domain_packs/industrial_material_packet.json --cache-dir <cache-folder>
```

The vendor-neutral contract is one JSON file per document with `page_count`, `text`, and `fields`. Each field supplies `name`, `value`, `confidence`, `page`, `region`, optional `unit`, and optional normalized `bbox`. The exact contract is exported as `ocr_input.schema.json`.

One `run` folder represents one connected procurement chain. For volume processing, isolate chains in subfolders and use:

```text
py -3 -m genuity_reconcile batch --ocr-root <packet-root> --output-root <output-root> --domain-pack domain_packs/industrial_material_packet.json
```

Each packet is independently reconciled, exported, and verified; `batch_summary.json` aggregates pages, fields, reviews, unresolved values, model use, costs, and semantic fingerprints without mixing entity scopes.

## Safety semantics

- `OBSERVED`, deterministic `RECOVERED_*`, and `DERIVED_DETERMINISTIC` fields may be accepted only with evidence and policy support.
- `PROPOSED_*` values always require confirmation.
- `ANALYTICS_ONLY` imputations never enter operational records.
- `CONFLICT` is never silently resolved; source-authority rank is shown to reviewers.
- `UNRESOLVED` remains blank until new evidence arrives.
- Unknown document types are quarantined; high OCR confidence alone cannot make them operational.
- Required fields omitted by OCR are materialized as unresolved exceptions.
- Cropped-model results use a content-addressed persistent cache; altered cache entries fail validation.
- `.genuity_cache` is ephemeral and excluded from the artifact manifest; every cache entry has its own integrity hash and is revalidated before reuse.
- Export fails closed if provenance, acceptance-policy, graph, cache, or duplicate-integrity checks fail.
- Text beginning with spreadsheet formula markers is neutralized in CSV exports; JSON and SQLite retain the original value.
- The demo's crop-only VLM adapter is simulated and can be disabled with `--no-vlm`.

## Important output files

- `SUMMARY.md` - executive result and connected answer.
- `genuity_demo.db` - SQLite handoff containing documents, decisions, evidence, exceptions, graph, validations, and metrics.
- `canonical_records.csv` / `.json` - system-ready connected record.
- `chemistry_results.csv`, `mechanical_results.csv`, `material_requirements.csv` - normalized engineering tables.
- `field_decisions.csv` / `.json` - complete candidate and decision audit trail.
- `evidence.json` and `field_evidence_links.csv` - page/region provenance and content hashes.
- `graph.json` and `document_links.csv` - relationships with join keys, corroboration, and evidence.
- `exceptions.csv` and `review_queue.json` - proposals, conflicts, analytics-only values, and unresolved fields, with owner, SLA, blocking state, reason code, and stable deduplication key.
- `ocr_input.schema.json` / `field_decision.schema.json` - portable JSON data contracts.
- `domain_pack_snapshot.json` - exact versioned policy/configuration used, bound into the run manifest by canonical hash.
- `demo_scorecard.json`, `accuracy_report.json`, `critical_field_benchmark.csv` - ten-behaviour and sealed-truth checks.
- `integrity_report.json` and `run_manifest.json` - fail-closed checks, artifact hashes, and semantic fingerprint.
- `cost_report.json`, `business_case.json`, and `BUSINESS_CASE.md` - dated token/cost calculation, scale, sensitivity, and break-even.
- `scale_benchmark.json` - duplicate-aware 1,000-page local smoke benchmark.
- `resilience_scorecard.json` - executable malformed-input, quarantine, omission, alias-collision, cache-tamper, and policy failure injections.

## Verification

Run the 51-test standard-library suite:

```text
py -3 -m unittest discover -s tests -p "test_genuity_reconcile.py" -v
```

Independently verify an exported run:

```text
py -3 -m genuity_reconcile verify --output-dir demo_output
```

The verifier checks safe manifest paths, artifact hashes, the semantic fingerprint, provenance status, resilience status, SQLite integrity, and database/JSON row-count consistency. Hashes detect uncoordinated changes; production signer authenticity still requires an external signature or trusted-key system.

Calculate a client-editable overlay ROI scenario (all assumptions can be overridden):

```text
py -3 -m genuity_reconcile estimate --pages 1000000 --human-hourly-cost 25 --implementation-cost 100000
```

Evaluate an exported run against client blind truth (start from `CLIENT_TRUTH_TEMPLATE.csv`):

```text
py -3 -m genuity_reconcile evaluate --decisions demo_output/field_decisions.json --truth-csv client_truth.csv --output client_evaluation.json
```

Turn reviewed exceptions into a validated, hash-chained audit ledger (start from `REVIEW_RESOLUTION_TEMPLATE.csv`):

```text
py -3 -m genuity_reconcile review-ledger --review-queue demo_output/review_queue.json --resolutions-csv review_resolutions.csv --output review_ledger.json
py -3 -m genuity_reconcile verify-review-ledger --ledger review_ledger.json --review-queue demo_output/review_queue.json
```

The ledger records dispositions without silently mutating canonical output; promotion into a client system remains a separate controlled integration step.

## Assumptions and scope

The packet is synthetic, so its accuracy report proves pipeline behavior, not production accuracy. External prices and human-review assumptions are dated and configurable. Image tokens use the official patch formula; prompt/output token counts remain planning assumptions until replaced by live usage telemetry.

See the neighboring executive, market/pilot, and dependency/license documents plus `../templates/PILOT_SCORECARD_TEMPLATE.csv`.
