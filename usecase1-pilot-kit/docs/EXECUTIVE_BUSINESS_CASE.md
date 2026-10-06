# Genuity industrial reconciliation: executive decision case

## Decision

Approve a paid, falsifiable pilot for the evidence-and-reconciliation layer. Do not fund a new OCR platform and do not make a billion-dollar revenue claim from a synthetic packet.

The product wedge is narrow and valuable:

`client OCR/VLM -> Genuity evidence, reconciliation, policy gates -> ERP/QMS/PLM-ready records`

The buyer pays for fewer exception minutes, fewer unsupported critical-field fills, faster completion, and a defensible audit trail. The client keeps its extraction stack, templates, models, and confidential documents.

## What the working proof establishes

The one-command 12-page packet currently demonstrates all ten required behaviors. It emits 77 evidence-backed accepted fields, six visible exceptions (five blocking review cases and one analytics-only value), one unresolved signoff, a connected PO-to-test graph, normalized engineering tables, SQLite/CSV/JSON handoffs, and cost telemetry. The sealed synthetic benchmark reports 100% precision and automatic coverage across 28 controlled critical fields; that proves the fixture behavior, not client production accuracy.

Safety is testable rather than rhetorical:

- 21/21 provenance and policy integrity controls pass.
- Six executable failure injections pass.
- 51 focused tests pass, including non-compensating release, scoped approvals, separation of duties, release-time artifact verification and immutable output-path boundaries.
- Unknown or ambiguously classified documents are quarantined.
- Non-unique joins and identity conflicts remain blank and enter review.
- Every nonaccepted field appears exactly once in the exception queue.
- Domain policy, cache integrity, artifact integrity, and JSON/SQLite consistency are independently checked.

## Unit-economic thesis

The value equation for a client pilot is:

`annual value = pages x avoided review cases/page x minutes/case x loaded labor cost/minute - incremental compute - annualized integration cost`

Under the controlled packet assumptions, the generated model currently estimates:

| Measure | Scenario result |
|---|---:|
| Genuity selective pipeline | $0.470337/page |
| Full-page VLM planning scenario | $1.129127/page |
| OCR-only plus review planning scenario | $2.720250/page |
| Saving versus full-page VLM | $0.658790/page |
| Saving versus OCR-only plus review | $2.249913/page |

These values are driven mainly by assumed reviewer workload, not API tokens. Scenario E conservatively charges every inspected crop as a cold-cache model call. The A-D review rates remain labeled planning assumptions. Replace them with timestamped reviewer telemetry before quoting a customer.

At one billion annual pages, the arithmetic produces a $659 million value pool versus the full-page VLM scenario and $2.25 billion versus OCR-only plus configured review. This is portfolio-scale avoided cost, not Genuity revenue or market size. At an illustrative 15% share of the full-page-VLM saving, the same scenario yields about $99 million annual revenue; a billion-dollar recurring business would require much greater verified throughput, a larger captured share, additional workflow value, or multiple product lines.

External price anchors are documented from [AWS Textract](https://aws.amazon.com/textract/pricing/), [Google Document AI](https://cloud.google.com/document-ai/pricing), and the [official GPT-5.4 mini model page](https://developers.openai.com/api/docs/models/gpt-5.4-mini). They measure extraction compute, not downstream exception handling.

## Commercial design

Use a three-part contract whose variables are replaced with pilot evidence:

1. A fixed integration fee for the versioned domain pack, adapters, system mappings, and acceptance policy.
2. Auditable usage pricing per reconciled page or completed record, with OCR/model charges visible or passed through.
3. An optional outcome component capped at an agreed share of independently verified avoided exception cost.

Do not sell generic accuracy. Sell a service-level result: critical-field precision, evidence coverage, abstention behavior, exception time, completed-record cost, and turnaround time.

## 90-day deployment path

| Window | Deliverable | Exit condition |
|---|---|---|
| Days 0-15 | Baseline instrumentation and data contract | Reviewer time, correction, API usage, document family, and system-of-record outcomes can be measured |
| Days 16-35 | Client-owned domain pack and adapters | Authorities, aliases, joins, critical fields, permitted reconstructions, and acceptance policy are frozen |
| Days 36-55 | Shadow processing | No operational writes; every candidate is compared with the current process |
| Days 56-70 | Blind 10,000-page evaluation | At least 1,000 independently adjudicated critical fields; no truth leakage into configuration |
| Days 71-90 | Holdout and limited production gate | Pre-agreed safety and unit-economic gates pass on unseen suppliers/templates |

## Pilot gates and kill criteria

Proceed only if the same held-out packet shows:

- 100% resolvable evidence coverage for accepted fields.
- Zero unsupported or incorrect critical-field auto-accepts.
- Zero silent conflict resolution.
- 100% exception visibility.
- Critical-field precision at or above the client's production threshold; target 99.5% or higher.
- At least 30% lower exception minutes per completed record.
- At least 30% lower all-in cost per verified field than the current process and full-page VLM arm.
- External routing below 10% unless the client explicitly buys a different coverage/cost tradeoff.

Stop or redesign if two consecutive held-out evaluations miss a safety gate, if review savings disappear after including integration operations, or if packet/entity isolation cannot be established from available identifiers.

## Defensibility

The durable asset is not a model call. It is the compounding collection of client-owned, versioned domain policies; adapter contracts; resolved exception patterns; regression packets; evidence graphs; reviewer telemetry; and cost-aware routing rules. Each deployment can become faster without pooling confidential documents or retraining a large model.

The proof already supports isolated multi-packet processing, content-addressed model caching, blind-truth evaluation, tamper-evident review ledgers, database-ready exports, and deterministic abstention. Production scale still needs orchestration, access control, external signing/key management, retention policy, observability, and client-approved quality authority.

## Bottom line

The defensible next step is a paid evidence-generating pilot, not a valuation narrative. If the holdout demonstrates high critical precision and materially fewer exception minutes, Genuity can become the trust layer that service companies attach to existing document programs. If it does not, the gates make that failure cheap and visible.
