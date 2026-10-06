# LTTS adjacent-workflow router

This is a discovery map, not a claim that seven products are already built. Use it to select the next workflow only after the material-traceability wedge has an owner, baseline and pilot result.

## Selection rule

Score every candidate from 1–5 on pain, repeat volume, cost of error, buyer access, data readiness and reuse of the current evidence/release core. Subtract 1–5 for integration complexity and security delay.

```text
priority = pain + volume + error_cost + buyer_access + data_readiness + core_reuse
           - integration_complexity - security_delay
```

Require evidence beside every score in `templates/LTTS_WORKFLOW_SELECTION_TEMPLATE.csv`. Do not select purely because a use case sounds futuristic.

## Candidate map

| Workflow | Typical buyer/user | Connected evidence | Critical reconciliation | Primary success metric | Reuse | New work required |
|---|---|---|---|---|---|---|
| Supplier material/component acceptance | Head of Supplier Quality; receiving inspector | PO, BoM, specification/revision, CoC/MTR, chemistry/mechanical tests, inspection | part/heat/lot, revision, quantity, test-to-limit, signoff | exception minutes and false critical accepts | Current wedge | client adapter, policy and QMS staging |
| Drawing–BoM–specification change impact | Engineering change/configuration lead | drawing revisions, BoM, requirements, deviation, approval | revision authority, affected part/configuration, unresolved downstream reference | change-review cycle time and escaped mismatches | High | drawing/requirement extraction and change graph |
| Inspection–NCR–CAPA evidence | Quality operations/CAPA owner | inspection results, NCR, root cause, corrective action, verification | defect/lot identity, closure evidence, approval authority | closure time and reopened cases | High | lifecycle states and controlled reviewer roles |
| Plant build/commissioning handover | Project/asset-information manager | equipment list, datasheet, vendor book, test certificate, punch list, as-built record | tag/equipment identity, document revision, missing handover evidence | handover backlog and retrieval/rework time | Medium-high | asset hierarchy and project-scale packetization |
| Maintenance/work-order/spares evidence | Maintenance/reliability head | asset master, work order, inspection, sensor event, part/spares record, manual | asset identity, chronology, failure/repair link, allowable part | diagnostic preparation time and repeat failure visibility | Medium | temporal links and CMMS/EAM connector |
| Medical-device design/quality traceability | Design assurance/quality systems | user need, requirement, risk control, test, nonconformance, design change | requirement-to-risk-to-test coverage and approved revision | traceability review effort and uncovered controls | Medium | regulated ontology, validation and legal review |
| Automotive/embedded requirement-to-test evidence | Systems/software quality lead | system/software requirement, interface, change, test case/result, defect | version/baseline, requirement coverage, result authority | release-readiness review time and escaped trace gaps | Medium | ALM connectors, hierarchy and software baselines |

## Routing questions

### If the input is mostly documents

Use the existing adapter → evidence graph → authority/constraint → exception → release architecture. Add only the domain pack, identity graph and connector required by the selected workflow.

### If the input includes time series or telemetry

Use Axiom's temporal/rare-edge components for validation and scenario testing. Do not force telemetry into the document packet model. Connect the result only through stable asset/event identity and explicit time windows.

### If the input is image/video/3D

Use a client-approved specialist perception/simulation adapter. Axiom currently validates or orchestrates some modalities; it does not claim native high-fidelity generation for all of them. Preserve modality-specific evidence and uncertainty.

### If someone asks for a world model

Ask for the decision, state, action, outcome, intervention cadence, counterfactual baseline and deployment owner. If any is missing, treat the request as research discovery rather than the next product.

## Stop conditions

Reject or pause a candidate when:

- no accountable economic buyer exists;
- the exception workload cannot be measured;
- connected evidence or independent truth cannot be accessed;
- identifiers cannot isolate assets/packets safely;
- the incumbent already meets the safety/economic gate at lower change cost;
- more than half of delivery is bespoke extraction with little reusable policy/integration;
- production data cannot remain inside an approved security boundary.

## Expansion evidence required

Move from the first workflow to a second only when the first has:

1. a paid pilot or equivalent committed client resource;
2. blind held-out results;
3. measured review/cost improvement;
4. a controlled staging integration;
5. a versioned reusable adapter/domain pack;
6. a second buyer who confirms the adjacent pain independently.

This discipline turns LTTS exposure into a repeatable platform instead of a catalogue of disconnected demonstrations.

