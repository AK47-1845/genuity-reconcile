# Founder guide: Genuity 2.0 Use Case 1

## Executive answer

Describe Genuity today as:

> **Evidence infrastructure for trustworthy industrial AI. Genuity turns imperfect engineering-document extraction into connected, validated and auditable records, escalating only genuine uncertainty and blocking unsafe system-of-record writes.**

The first sellable wedge is **engineering record reconciliation and controlled release**, starting with supplier-quality and material-traceability packets. It is not “a world-model company” today. It is also broader than “a synthetic-data library.” Genuity Axiom is the constraint, privacy, synthetic and rare-edge testing layer that strengthens the wedge. Physics-informed world models are a later expansion after reliable engineering state, constraints and outcome feedback have been earned.

```text
NOW:      reconcile real engineering evidence and reduce exception work
NEXT:     use Axiom to generate rare/messy cases and validate robustness
LATER:    learn reusable engineering state and transition models
FUTURE:   domain-specific predictive/world models where a buyer exists
```

## Why this problem exists

Industrial document workflows are not solved when text is extracted. A material, quality or handover packet contains facts spread across purchase orders, BoMs, drawings/specifications, supplier certificates, test tables, revisions and inspection reports. The operational decision requires answering:

- Which documents belong to the same asset, part, lot or heat?
- Which revision and source has authority for each field?
- Is a disagreement a correctable OCR defect, unit mismatch, obsolete source or real exception?
- Does a value satisfy physical, specification and workflow constraints?
- Can a missing field be deterministically recovered, merely proposed, or never known?
- What exact evidence supports every accepted value?
- Who resolves each exception, and may the record enter ERP/QMS/PLM?

Generic OCR, IDP and VLM products can extract and classify. Consulting teams can build workflows. Genuity must win by being an extraction-agnostic **decision and evidence layer** that makes post-extraction work safer, cheaper and measurable.

## Buyer, user and economic owner

Do not target vague “engineering enterprises.”

- **Economic buyer:** Head of Quality, Supplier Quality, Digital Manufacturing, Engineering Operations or a delivery-unit leader accountable for turnaround and rework.
- **Daily user:** quality engineer, document controller, procurement/material engineer, handover team or shared-services reviewer.
- **Technical approver:** enterprise architect, CISO/data owner and QMS/ERP/PLM system owner.
- **LTTS channel owner:** a business-unit/client-account leader who can attach the capability to a live transformation engagement.

The customer buys reduced exception minutes, faster completion, fewer unsupported critical values and defensible traceability. They do not buy “synthetic data” unless it changes one of those outcomes.

## Why material traceability is the first wedge

1. Multiple documents must agree; single-page extraction cannot finish the job.
2. Wrong values can create rejection, rework, safety or audit consequences.
3. Accepted values need provenance and authority, not only model confidence.
4. Exceptions consume skilled engineering time and are measurable.
5. Existing OCR/VLM investments remain, reducing adoption resistance.
6. The pattern transfers to inspection packs, plant handover, maintenance records and regulated evidence workflows.

The wedge is invalid if LTTS cannot identify a repeated workflow with material exception labor and an owner willing to provide blind truth. Then test another evidence-heavy workflow instead of forcing this packet.

## What version 1.1 actually does

The package consumes one JSON document per existing OCR/extraction result. It validates the adapter contract, classifies documents deterministically, canonicalizes aliases, detects duplicates, recovers permitted OCR confusions, links entities through approved keys, normalizes materials and units, evaluates constraints and revisions, produces an evidence graph and creates a field-level decision.

Each decision distinguishes observed/accepted, deterministically recovered, deterministically derived, proposed for review, conflicting, ambiguously linked, analytics-only, missing/unresolved and quarantined source data.

Outputs include evidence-linked decisions, review queue, canonical record, normalized engineering tables, graph, cost telemetry, scenario model, SQLite handoff, integrity report, resilience scorecard, run manifest and operational release decision.

Version 1.1 separates data quality from authorization. Named approvals bind to the exact record, decisions, policy pack and target. A failed safety gate cannot be compensated by a high average score or signatures. The demo remains `REVIEW_REQUIRED` because it contains real blockers and no client approvals.

## Proven versus unproven

### Proven by executable synthetic evidence

- all ten intended reconciliation behaviors execute;
- accepted fields retain evidence;
- conflicts and unknowable values remain visible;
- unsafe imputation is not relabeled as observed fact;
- malformed/adversarial inputs fail closed;
- duplicate content and cache tampering are detected;
- packets are isolated in batch mode;
- outputs are hash/semantic/SQLite verified;
- controlled release blocks unsafe write-back;
- 51 focused tests pass.

### Not proven yet

- accuracy on LTTS/client distributions;
- production throughput, availability or infrastructure cost;
- live review-time savings;
- real OCR/model or system-of-record integration;
- secure multi-tenant operation;
- compliance acceptability for a specific deployment;
- willingness to pay and cross-account repeatability.

The safe claim is “working, falsifiable pilot system,” not “production-ready autonomous platform.”

## Architecture

```text
Client documents
  -> client-approved OCR / IDP / VLM
  -> strict Genuity adapter contract
  -> classification + duplicate/revision handling
  -> canonical fields + units + identities
  -> cross-document evidence graph
  -> authority + deterministic recovery + constraints
  -> accept / review / analytics-only / unresolved
  -> exception queue + review ledger
  -> non-compensating release gates + scoped approvals
  -> controlled QMS / ERP / PLM staging export
```

The proof uses only the Python standard library. Production infrastructure should wrap the decision core rather than alter its semantics.

### Invariants

1. No accepted field without evidence.
2. No probabilistic proposal relabeled as observed.
3. No silent conflict resolution.
4. No ambiguous entity join guessed.
5. No analytics-only value used operationally.
6. No mixed packet or tenant boundary.
7. No policy pack silently changed after evaluation.
8. No staging write without passed safety gates and scoped approvals.
9. No production claim based on fixture accuracy or synthetic economics.

## How Axiom fits

Technical entry points: [Axiom start guide](../genuity_axiom/START_HERE.md) and [Axiom founder handoff](../genuity_axiom/FOUNDERS.md).

- **Use Case 1:** processes real extracted evidence and decides what is trustworthy.
- **Axiom:** creates controlled synthetic, rare, missing, conflicting, privacy-sensitive and physically constrained cases and tests system safety.

Immediate integration:

1. Generate rare packet mutations: duplicate scans, stale revisions, identifier collisions, missing signoffs, unit corruption and conflicts.
2. Run this pipeline on them.
3. Measure abstention, unsupported critical accepts, exception visibility and release behavior.
4. Keep generated cases labeled synthetic and outside operational evidence.

This is stronger than a generic generator: Genuity can create hard industrial cases **and prove downstream AI handles them safely**.

## How world models fit

World models need a state representation, actions/transitions, constraints and observed outcomes. Genuity has foundations—canonical state, provenance, constraints, rare cases and validation—but no validated buyer-specific world model yet.

Move a world-model use case into the main pitch only when all exist:

1. named operational decision;
2. buyer with budget;
3. state/action/outcome data;
4. metric beating a current baseline;
5. deployment loop changing cost, risk or time.

Until then, world models are technical trajectory, not current category.

## Four-month LTTS validation plan

### Month 1 — select and baseline the workflow

- Interview 10–15 delivery, quality, data and account leaders.
- Score workflows on volume, exception minutes, criticality, data access, integration and buyer urgency.
- Select one workflow and 10–20 critical fields.
- Map current tools, reviewer steps, reasons, authority and downstream system.
- Obtain approved de-identified discovery data and independent adjudicators.
- Measure current cost/record, exception rate, median/P90 review time and rework.

**Gate:** named business, data and quality owners; volume; baseline; written pilot criteria. Without these, stop adding features.

### Month 2 — configure and harden

- Build the client OCR adapter and canonical field map.
- Configure classification, revision logic, join keys, collision tests, authority and constraints.
- Add failures from the real exception taxonomy.
- Establish security, retention, logging, model and export boundaries.
- Instrument cost, latency and review at packet/field level.
- Freeze the domain-pack version before holdout.

**Gate:** 100% evidence coverage for accepted fields, zero silent conflicts in development and approved policy ownership.

### Month 3 — blind comparison

- Use unseen suppliers/templates and independently adjudicated truth.
- Compare current workflow, agreed incumbent/full-page baseline and Genuity.
- Report by field, supplier, document type and failure mode.
- Measure critical precision, incorrect auto-accepts, coverage, abstention, visibility, review minutes, route rate, latency and total cost.
- Red-team identifier collision, stale revision, adversarial text, duplicate and partial packets.

**Gate:** zero unsupported/incorrect critical automatic accepts; 100% exception visibility; target ≥99.5% critical precision; target ≥30% reduction in exception minutes and all-in cost, subject to client agreement.

### Month 4 — controlled staging and commercial decision

- Integrate read-only/staging output with QMS/ERP/PLM.
- Use named domain, quality and system-owner approvals.
- Add tenant identity, access control, secrets, observability, retry and dead-letter handling.
- Run shadow mode and compare downstream corrections/releases.
- Produce the value report, security gaps, implementation plan and price proposal.

**Gate:** staging release passes; no cross-tenant event or untracked override; buyer signs a production plan or failure is documented honestly.

## Questions for Dr. Madhusudan

### Problem selection

- Which client workflows still require senior engineers to reconcile extracted data manually?
- Which has the highest volume, turnaround pressure and cost of a wrong field?
- Which business unit already owns OCR/IDP deployments where Genuity can be an add-on?
- What has LTTS tried, and why did it remain services-heavy or fail?

### Buyer and economics

- Who owns budget and KPI: quality, operations, digital, procurement or account P&L?
- How many packets/pages are processed monthly and what is loaded review cost?
- Which exceptions dominate time? What are median and P90 times?
- What savings threshold is material enough to sponsor deployment?

### Data and truth

- Can we get connected packets rather than isolated pages?
- Who independently adjudicates critical fields?
- Which supplier/template/time slices remain blind?
- Which identifiers can collide or cannot cross boundaries?

### Deployment

- Is on-premises, private cloud, regional VPC or managed endpoint acceptable?
- Which models/services are contractually permitted?
- Which system receives output and who owns release approval?
- What audit, retention, signing, access and deletion evidence is required?

### Expansion

- Which adjacent evidence workflow reuses the ontology/integration?
- Where are rare failures blocking model validation?
- Which world-model effort has a decision, state/action/outcome data and baseline?

## Pilot measurement contract

Use connected records with real exception diversity; include unseen suppliers/templates/time periods in holdout. Truth must be field-level and independently adjudicated.

- `critical_precision = correct critical auto-accepts / all critical auto-accepts`
- `automatic_coverage = auto-accepted truth fields / truth fields`
- `abstention_rate = non-accepted truth fields / truth fields`
- `exception_visibility = surfaced known exceptions / known exceptions`
- review minutes per completed record
- all-in cost per verified field
- external regions routed per page
- P50/P95 packet latency and queue age
- manual overrides and post-release corrections

Include denominators and confidence intervals where appropriate. Never blend critical and non-critical fields into one reassuring average.

## Commercial model

**Land:** paid 6–12 week pilot with a fixed workflow, boundary, truth set and scorecard. Avoid a free innovation POC with no buyer/baseline.

**Expand:** annual platform/license plus integration and usage for one client. Add value alignment only after savings are measured.

**Platform:** reusable adapters, domain packs, evidence graph, release policy, review telemetry and rare-edge evaluation across quality, inspection and handover workflows. Services may start deployment, but assets must become repeatable.

Defensibility can come from evaluated exception taxonomies, domain decision/evidence contracts, approved policies, performance by failure mode, workflow integrations and trust in safe abstention. Confidential client facts are not a cross-client data moat without rights.

## Competition

Alternatives include OCR/IDP vendors, document-AI platforms, workflow/process tools, rules engines, data-quality platforms, in-house teams, systems integrators and full-page multimodal models. The common competitor is spreadsheets, email, reviewer memory and scripts.

Genuity wins only if a blind pilot proves lower review time and safer critical-field behavior with lower change cost. “We use AI” is not an advantage.

## Production roadmap

Use [the LTTS adjacent-workflow router](docs/LTTS_ADJACENT_WORKFLOW_ROUTER.md) before accepting a second use case. It separates evidence-core reuse from new modality/connector work and includes explicit stop conditions.

### Required

- adapter SDK and contract migration;
- tenant/packet identity boundary;
- RBAC/SSO and client-managed secrets/keys;
- encrypted storage and retention/deletion;
- queue, retry, dead-letter and idempotency;
- decision/review/latency/cost/drift observability;
- signed releases with client-managed trust roots;
- controlled system-of-record connector;
- domain-pack approval/version registry;
- security, privacy, SBOM, vulnerability and licensing review.

### Build only after evidence

- learned classification if deterministic cues fail materially;
- retrieval/LLM reviewer assistance;
- active learning from resolved exceptions;
- Axiom rare-packet campaigns;
- cross-packet supplier/asset risk analytics;
- world-model components for a named decision.

## Risk register

| Risk | Why fatal | Test/mitigation |
|---|---|---|
| No costly pain | no budget | baseline reviewer minutes |
| Existing vendor good enough | no wedge | blind comparison |
| Unsafe joins | wrong lot/asset | collision tests and abstention |
| Rules vary per client | services trap | versioned approved packs |
| High precision, low coverage | no savings | report both |
| High coverage, wrong fills | safety failure | critical release gates |
| Security rejected | cannot deploy | month-one review |
| Fixture presented as proof | credibility loss | blind holdout |
| World-model distraction | unfocused roadmap | buyer/data/metric gates |
| Custom integration dominates | poor margins | standard contracts |

## Brutal investment view

### Investable

- painful post-extraction problem with metrics;
- working, auditable wedge instead of an AGI narrative;
- preserves extraction investments;
- expansion into an evidence/release platform;
- Axiom rare-edge advantage tied to outcomes.

### Still rejectable

- no paid customer or blind client result;
- one synthetic packet;
- unclear LTTS buyer and volume;
- consulting/product-repeatability risk;
- incumbents may absorb features;
- founder execution risk after cofounder departure.

One paid pilot showing zero incorrect critical auto-accepts, ≥30% lower exception minutes/cost, one staging integration and a second adjacent workflow is worth more than dozens of modalities or a “world model” slide.

## Founder operating rules

1. Lead with workflow and outcome, not technology category.
2. Keep a claim ledger: fixture result, client result, assumption and hypothesis never mix.
3. Ask for connected packets, truth and reviewer telemetry.
4. Build only against a pilot gate or production requirement.
5. Treat abstention and release blocking as product features.
6. Do not promise compliance, guaranteed savings, production readiness or million-dollar value without evidence.
7. Use LTTS to find repeatable patterns, not indefinite unpaid custom R&D.
8. Convert client rules into versioned configuration or explain why not.
9. Review weekly: buyer, baseline, data, holdout, deployment and next commercial action.
10. Keep world models subordinate to a named decision until this wedge earns expansion.

## Next seven actions

1. Run and learn `DEMO.md`.
2. Ask Dr. Madhusudan for three candidate workflows and their owners.
3. Score them and choose one.
4. Secure discovery data, blind holdout and reviewer telemetry.
5. Build the approved adapter/domain pack without viewing holdout.
6. Execute the comparison and publish the error taxonomy.
7. Ask for paid staging only if pre-agreed gates pass.

That is the credible route from this technical proof to an LTTS-adopted product and an investor-understandable company.

Use `templates/LTTS_WORKFLOW_SELECTION_TEMPLATE.csv` for action 3, `templates/CLIENT_ADAPTER_MAPPING_TEMPLATE.csv` for action 5 and `templates/LTTS_PILOT_TELEMETRY_TEMPLATE.csv` for action 6. Keeping these artifacts populated is part of the product validation, not administrative work.
