# Operating guide

## Supported boundary

Use Case 1 consumes **existing OCR/extraction JSON** for one connected procurement/material chain per run. It does not ingest arbitrary PDFs by itself and does not certify compliance. The package runs on Python 3.10+ using only the standard library.

## Run and verify the sample

```powershell
.\run_demo.ps1
.\verify_everything.ps1
```

The generated, non-confidential sample source is `demo_output/input_packet`. It intentionally contains missing values, conflicting quantities, duplicate scans, obsolete revisions, a difficult crop and an absent signoff.

Run these commands **from this `Genuity2.0 usecase1` directory** or install the 1.1.0 wheel. The parent archive contains an older root-level `genuity_reconcile` package from prior work that can shadow this self-contained version if Python is launched from the parent directory. The supplied `.ps1`/`.cmd` scripts set the correct working directory and import path automatically.

## Run client-approved OCR output

```powershell
$env:PYTHONPATH = "$PWD\source"
py -3 -m genuity_reconcile run `
  --ocr-dir C:\approved\packet_001\ocr `
  --output-dir C:\approved\packet_001\result `
  --domain-pack domain_packs\industrial_material_packet.json
```

Keep unrelated chains in separate folders. For multiple packets:

```powershell
py -3 -m genuity_reconcile batch `
  --ocr-root C:\approved\packets `
  --output-root C:\approved\results `
  --domain-pack domain_packs\industrial_material_packet.json
```

External crop routing is off unless explicitly enabled. The bundled crop adapter is a fixture simulation and must be replaced by an approved adapter before a real model evaluation.

`run` and `batch` require a new or empty output directory and reject any overlap with the input tree. This preserves immutable audit runs. Only the non-confidential `demo` command exposes `--overwrite-demo`, which the supplied demo scripts use explicitly.

## Input contract

Each JSON file represents one source document. Required top-level keys are `page_count`, `text` and `fields`. Required field keys are `name`, `value`, `confidence`, `page` and `region`. Use normalized `[x1,y1,x2,y2]` boxes when available. The full schema is exported as `ocr_input.schema.json`.

The adapter rejects malformed pages, non-finite values, out-of-range confidence, invalid boxes, alias collisions, duplicate normalized filenames and mixed PO chains.

## Outputs by audience

| Audience | Primary files |
|---|---|
| Quality reviewer | `review_queue.json`, `validation_report.json`, `operational_release.json` |
| Data engineer | `canonical_records.json/csv`, normalized result CSVs, `genuity_demo.db` |
| Auditor | `field_decisions.json`, `evidence.json`, `run_manifest.json`, `domain_pack_snapshot.json` |
| Product/economics | `metrics.json`, `cost_report.json`, `business_case.json` |
| Pilot evaluator | `accuracy_report.json`, blind-truth evaluator output, pilot scorecard |

## Review resolution

Populate a copy of `templates/REVIEW_RESOLUTION_TEMPLATE.csv`:

```powershell
py -3 -m genuity_reconcile review-ledger `
  --review-queue demo_output\review_queue.json `
  --resolutions-csv review_resolutions.csv `
  --output review_ledger.json

py -3 -m genuity_reconcile verify-review-ledger `
  --ledger review_ledger.json `
  --review-queue demo_output\review_queue.json
```

The ledger records review; it intentionally does not mutate or promote the canonical record.

## Operational release check

Every export includes `operational_release.json`. The sample is `REVIEW_REQUIRED` by design.

```powershell
py -3 -m genuity_reconcile release-check `
  --output-dir demo_output `
  --target QMS_STAGING
```

Exit code `3` means output is not approved for staging. Named approvals use `templates/RELEASE_APPROVAL_TEMPLATE.json`; each binds to the exact `scope_sha256`, target and role. Approvals cannot override a safety gate. This authorizes only controlled staging—not production write-back.

## Blind accuracy evaluation

```powershell
py -3 -m genuity_reconcile evaluate `
  --decisions client_result\field_decisions.json `
  --truth-csv client_truth.csv `
  --output client_evaluation.json
```

Keep truth hidden during configuration. Report critical precision, incorrect automatic accepts, coverage and abstention together.

## ROI overlay

```powershell
py -3 -m genuity_reconcile estimate `
  --pages 1000000 `
  --human-hourly-cost 25 `
  --review-minutes 2.2 `
  --current-review-cases-per-page 0.8 `
  --genuity-review-cases-per-page 0.25 `
  --routed-regions-per-page 0.05 `
  --implementation-cost 100000
```

Use customer telemetry. The demo's costs are scenario arithmetic, not a quote.

## Safe customization order

1. Clone and rename the domain pack.
2. Define document cues and vendor aliases.
3. Establish exact entity keys and collision behavior.
4. Have the domain owner approve authority, revision rules, units and bounds.
5. Select critical and required fields.
6. Define permitted reconstruction and analytics-only methods.
7. Test malformed, conflicting, duplicate, stale-revision and adversarial packets.
8. Freeze the pack before the blind holdout.

Do not add a probabilistic fill merely to improve apparent coverage. Every new recovery method requires explicit policy, evidence semantics and a failure test.
