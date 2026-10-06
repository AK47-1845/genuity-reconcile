# Genuity industrial-document reconciliation: evidence and commercialization plan

## The wedge

Genuity should not sell “better OCR.” It should sell the missing trust layer between extraction and a client system of record:

`existing OCR/VLM -> Genuity reconciliation and policy gates -> ERP/QMS/PLM-ready records`

The paid outcome is fewer exception minutes per completed record while preserving critical-field precision, evidence, and abstention. This positioning lets an engineering-services firm keep its OCR, models, templates, and client relationships.

## Why this is a real manufacturing data problem

NIST describes modern manufacturing traceability as organizing, linking, and querying records so stakeholders can verify provenance and meet contractual or operational obligations. That maps directly to the demo's PO, part, BoM, specification, certificate, heat, and test-result chain ([NIST IR 8536, second public draft](https://csrc.nist.gov/pubs/ir/8536/2pd)).

NIST also publishes practical guidance specifically for traceability and trustworthiness of manufacturing-related data, including file and stream representations and standards-based formats ([NIST AMS 300-10](https://www.nist.gov/publications/recommendations-ensuring-traceability-and-trustworthiness-manufacturing-related-data)). Its Digital Thread program says enterprises need faster ways to link authentication, authorization, and traceability information to product data ([NIST Digital Thread for Manufacturing](https://www.nist.gov/programs-projects/digital-thread-manufacturing)).

For AI controls, NIST's AI RMF calls for objective, repeatable, documented testing, evaluation, verification, and validation and a traceable basis for tradeoffs ([NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)). The implementation therefore emits field evidence, rejected alternatives, rule results, an exception queue, a sealed fixture benchmark, and a fail-closed integrity report.

## External price anchors, not invented competitor numbers

- AWS lists text OCR at $0.0015/page for the first million pages in US West (Oregon), tables at $0.015/page, and forms at $0.05/page ([Amazon Textract pricing](https://aws.amazon.com/textract/pricing/)).
- Google lists Enterprise Document OCR at $1.50/1,000 pages and Form Parser/custom extraction at $30/1,000 pages at the first volume tier ([Google Document AI pricing](https://cloud.google.com/document-ai/pricing)).
- GPT-5.4 mini is listed at $0.75/million input tokens and $4.50/million output tokens ([official model page](https://developers.openai.com/api/docs/models/gpt-5.4-mini)). OpenAI documents 32×32 patch tokenization, a 1,536-patch high-detail budget, and a 1.62 multiplier for GPT-5.4 mini ([official vision cost method](https://developers.openai.com/api/docs/guides/images-vision#calculating-costs)).

These prices measure extraction compute, not the downstream cost of resolving missing values, cross-document conflicts, unsupported fills, or client-specific validation. Genuity's commercial value must be measured against that exception workload.

## Falsifiable paid-pilot protocol

### 1. Scope and freeze

- Select one high-volume document family and one procurement/material chain.
- Freeze the domain pack, source-authority order, critical fields, and acceptance policy before evaluation.
- Stratify at least 10,000 pages by supplier, template, scan quality, language, revision, and document age.
- Create a blind, double-reviewed truth set containing at least 1,000 critical fields. Adjudicate reviewer disagreements without exposing truth to pipeline development.

### 2. Compare the same packet

Run five arms on identical inputs:

1. Existing OCR only.
2. Existing OCR plus current deterministic templates/rules.
3. Existing OCR plus Genuity reconciliation and validation, with models disabled.
4. Full-page VLM baseline.
5. Genuity selective crop routing.

Record actual API usage, elapsed time, reviewer minutes, corrections, abstentions, and evidence coverage. Do not estimate these when production telemetry is available.

### 3. Acceptance gates

- Critical-field precision: at least the client's current production threshold; target 99.5% or higher.
- Unsupported critical auto-fills: zero.
- Evidence coverage of accepted fields: 100%.
- Silent conflict resolutions: zero.
- All proposals, conflicts, and unresolved fields: present in the review queue.
- Selective external routing: below 10% of pages/regions unless the client explicitly trades cost for coverage.
- Median exception-review minutes per completed record: materially below the current baseline.
- Cost per verified accepted field: lower than both the current process and full-page VLM arm.

### 4. Commercial decision

Use a holdout period after configuration. Price against independently measured avoided exception cost, not a claimed accuracy uplift. A practical structure is a fixed integration fee plus usage pricing capped below a negotiated share of verified savings. Keep model/OCR charges pass-through and auditable.

## Bottom-up scale logic

The generated `business_case.json` calculates page-level cost, human-rate sensitivity, routing sensitivity, implementation break-even, and 100,000-to-1-billion-page scenarios. It explicitly labels the result as scenario arithmetic rather than market forecasting.

A billion-dollar value pool is plausible only at portfolio scale. Under the current controlled-packet assumptions, the report calculates the exact pages needed to save $1 billion against full-page VLM and OCR-plus-review baselines. Those thresholds must be recalculated from a client pilot; they are not a market-size claim.

## Durable product assets

- Versioned domain packs encoding aliases, units, join keys, authority, criticality, and permitted reconstruction.
- Adapter contracts that let services firms retain existing OCR/VLM investments.
- A candidate and evidence ledger explaining every accepted, proposed, rejected, conflicted, and unresolved value.
- Regression packets that turn each resolved exception pattern into a permanent test.
- Cost telemetry that optimizes routing at the field/region level.
- Client-owned policy boundaries: domain knowledge can be deployed without pooling confidential documents.

## Risks that must stay visible

- Synthetic results do not establish production accuracy.
- Review rates from 12 pages are not a capacity forecast.
- Source-authority policies can be wrong and require client ownership.
- Similar identifiers can create false joins; production deployment needs collision and ambiguity tests.
- A VLM candidate remains a proposal until independent evidence or configured rules justify acceptance.
- Material compliance decisions may have contractual or safety consequences; final authority remains with the client's approved quality process.
