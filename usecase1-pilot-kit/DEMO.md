# LTTS first-impression demo

## The one sentence to say first

> Genuity keeps the client's OCR and models, then converts their imperfect outputs into evidence-linked engineering records, sends only genuine uncertainty to people, and blocks write-back until every critical safety and approval gate passes.

Do **not** introduce this as synthetic data, a world model, an OCR replacement, or an autonomous compliance system. Those frames hide the immediate, measurable workflow.

## What problem the 12-page packet represents

A supplier-quality engineer receives a connected material packet: purchase order, invoice, bill of materials, specification revisions, material certificate, certificate of conformance, chemistry, mechanical results, hardness results, duplicate scans and final inspection. Existing extraction produces values, but it does not safely decide:

- whether `PN-7O725` is an OCR error or a real part;
- which specification revision is authoritative;
- whether an absent invoice field can be recovered from the PO;
- whether two same-heat measurements are interchangeable;
- whether PO quantity 45 and invoice quantity 44 may be silently resolved;
- whether an analytics-only estimate can enter QMS/ERP;
- whether the final connected record is safe to release.

That reconciliation work—not character recognition—is the wedge.

## Five-minute live run

From this folder:

```powershell
.\run_demo.ps1
```

Expected console outcome: the ten-behaviour scorecard passes. The run recreates `demo_output` from the supplied, non-confidential sample packet.

Then show these files in order:

1. `demo_output/input_packet/raw_documents/03_bom_revision_3.txt`—point to the `O/0` part-number defect.
2. `demo_output/field_decisions.json`—show the recovered value, method, rationale and evidence IDs.
3. `demo_output/graph.json`—show how PO, BoM, specification, certificate, heat and tests are connected.
4. `demo_output/review_queue.json`—show the quantity conflict, proposed boron value and missing signoff. Explain that abstention is a feature.
5. `demo_output/canonical_records.json`—show the operational view.
6. `demo_output/operational_release.json`—finish with `REVIEW_REQUIRED` and `writeback_allowed: false`.

The final file is the strongest moment: Genuity refuses to convert a good-looking aggregate score into permission to write unsafe data.

## Ten-minute narrative

### Existing tools stop too early

“OCR/VLMs extract candidates. Industrial operations still need cross-document identity, revision authority, physical constraints, evidence, exception ownership and a controlled release decision.”

### Genuity recovers only what can be defended

- **accepted:** direct evidence, exact joins, approved normalization or deterministic calculation;
- **review:** plausible proposal, conflict or ambiguous relationship;
- **never operational:** analytics-only estimate or unresolved value.

### Genuity routes expensive models selectively

The demo processes deterministic documents locally and inspects one difficult region. A cold run can route that crop through the simulated adapter; a repeated run can reuse its content-addressed cache without a new call. Be explicit that the adapter is simulated; routing, metering, cache, policy and review behavior are real. Do not present simulated model accuracy as a customer result.

### Genuity creates evidence, not another black box

Every accepted field points back to the document, page, region, quote and content hash. The domain-pack version, decisions, outputs and artifact hashes are sealed in the run manifest.

### Genuity makes the pilot falsifiable

The customer pilot compares the current workflow, full-page model baseline and Genuity on a blind holdout. The decision is based on critical-field precision, incorrect automatic accepts, evidence coverage, exception minutes, route rate and all-in cost per verified field.

## Business impact to sketch

```text
Current packets × current review minutes × loaded reviewer cost
                         ↓
Genuity auto-accepts only evidenced fields and concentrates review on exceptions
                         ↓
Measured savings = avoided review cost + evidenced avoided rework
                  - extraction/model cost - run cost - integration cost
```

Ask LTTS for actual volumes and reviewer timestamps. Never quote the bundled synthetic ROI as an LTTS saving.

## Questions for Dr. Madhusudan

1. Which client workflow currently spends the most senior-engineer time reconciling documents after extraction?
2. Which packet type has repeated volume, painful exceptions and an accountable quality owner?
3. Which fields can cause rejection, rework, warranty exposure or a safety hold if accepted incorrectly?
4. What receives the final record—QMS, ERP, PLM, MES, asset management or a client database?
5. What are the present exception rate and median/P90 handling times?
6. Is a private model endpoint allowed, or must all processing remain inside the client boundary?
7. Who owns source authority and revision rules?
8. What blind holdout and stop conditions would satisfy the client CTO and quality head?

## Data request after the meeting

Request 100–300 de-identified connected packets for discovery, not a random document dump. For each packet request:

- existing OCR/extraction JSON and raw source-page reference;
- document type, client template/supplier and system-of-record identifier;
- independently adjudicated values for a limited set of critical fields;
- current exception disposition and reviewer time if available;
- known revision, duplicate, unit, missing-field and conflicting-source cases;
- data residency, retention, model-routing and export restrictions.

Do not ingest client documents until a named owner confirms the approved boundary.

## Success after the first demo

The next step is agreement on one workflow, one buyer, one truth set, one security boundary and a paid pilot with written pass/fail gates:

- zero unsupported or incorrect critical-field automatic accepts;
- 100% evidence coverage for automatically accepted fields;
- 100% visibility of conflicts, ambiguity and missing critical values;
- at least 30% lower exception minutes per completed record;
- at least 30% lower all-in cost per verified field than the agreed comparison arm;
- external model routing below the approved ceiling;
- no operational write-back without scoped domain, quality and system-owner approvals.

## Honest answers to objections

**“Is this just rules?”** The product is the governed combination of adapters, evidence graph, deterministic authority, constraints, selective models, review and release. Rules are deliberately used where safer and cheaper.

**“Why cannot our OCR vendor do this?”** Some can add post-processing. The pilot must show whether Genuity reduces exception work without forcing extraction replacement. If the incumbent achieves the same held-out result at lower switching cost, Genuity should not win that workflow.

**“Is this production ready?”** The deterministic proof is runnable and verified; production still needs a client-approved adapter, identity/access controls, tenant isolation, observability, key management, retention and controlled write-back.

**“Where is synthetic data?”** Axiom generates policy-constrained rare and messy cases to test this release system when real failures are scarce or confidential. It supports the wedge; it is not the opening pitch.

**“Where are world models?”** They become relevant after Genuity owns reliable engineering state, constraints and outcome feedback. Do not sell that future before this wedge is validated.
