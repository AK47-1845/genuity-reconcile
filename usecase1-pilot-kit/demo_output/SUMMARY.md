# Genuity evidence-first industrial reconciliation run

## Outcome

- Ten required behaviours: **PASS**
- Documents/pages processed: **12**
- Existing OCR results consumed: **12**; incremental OCR calls: **0**
- Automatically accepted fields: **77**
- Evidence coverage of accepted fields: **100.0%**
- Critical-field fixture precision/automatic coverage: **100.0% / 100.0%** across **28** fields
- External regions routed: **0** (0.00% of pages)
- Model-result cache hits: **1**
- Human-review cases: **5**
- Unresolved fields: **1**
- Estimated selective-pipeline batch cost: **$5.6440**
- Cost-per-verified-field saving vs full-page VLM scenario: **58.35%**
- Provenance integrity checks: **21/21 PASS**
- Operational release: **REVIEW_REQUIRED**; write-back allowed: **false**

## Connected answer

`PO:PO-1001 -> PART:PN-70725 -> BOM:BOM-725-A -> SPEC:SPEC-725:R9 -> CERT:MTR-900 -> HEAT:W3535 -> TEST:CHEM-W3535 -> TEST:MECH-W3535`

The material certificate is linked through the CoC certificate number and shared heat/part evidence. Displayed chemistry passes the latest displayed specification. Invoice quantity 44 conflicts with PO quantity 45 and is not silently resolved. Certificate boron 0.0002 is only a proposal from the same-heat ladle table. The missing hardness cell is a 39.0 HRC analytics-only median. Inspector signoff remains `UNRESOLVED`.

## Safety and cost notes

The demo VLM adapter is simulated and sees only one crop. Its candidate is not auto-accepted. `operational_release.json` blocks system-of-record write-back while safety exceptions or scoped approvals remain. Pricing is dated `2026-08-12` and human/token assumptions are explicit in `cost_report.json`; they are planning estimates, not invoices.
