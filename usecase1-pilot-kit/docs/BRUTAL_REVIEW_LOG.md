# Brutal review log

## Verdict before version 1.1

The implementation was a strong, honest proof of reconciliation behavior, but an enterprise reviewer could still ask: “What prevents a complete-looking record from being pushed into QMS after the demo?” Evidence integrity existed; operational release authority did not.

## Fatal assumptions tested

| Assumption | Failure | Response |
|---|---|---|
| Good extraction means safe data | conflicts/revisions remain | evidence graph and field decisions |
| A high score permits release | one critical error hidden | non-compensating gates |
| Approval makes unsafe data safe | signatures override evidence | approvals cannot override failures |
| Any reviewer can approve | unaccountable override | named domain/quality/system roles |
| Approval survives a change | policy/record mutates | scoped SHA binding |
| Fixture predicts client accuracy | false production claim | blind holdout |
| More model calls means better | cost/privacy/latency | deterministic-first routing |
| LTTS wants new extraction | switching resistance | preserve OCR/VLM |
| World models are immediate | no buyer/metric | gated long-term expansion |

## Version 1.1 changes

- Added `release.py` and `operational_release.json`.
- Added `release-check` for sandbox/QMS/ERP/PLM staging.
- Added scoped named-approval validation and template.
- Added tests proving approvals cannot override safety and all roles are required.
- Added separation-of-duties enforcement so one reviewer cannot satisfy multiple required release roles.
- Added fresh manifest/hash/semantic/SQLite verification inside `release-check`; a stored integrity label is no longer trusted by itself.
- Added CLI path guards that reject input/output overlap and non-empty real-run destinations; demo overwrite is explicit.
- Added `DEMO.md`, `HOW_TO_USE.md` and `FOUNDERS.md`.

## Remaining rejection reasons

1. No held-out LTTS/client evidence.
2. No production identity, authorization, tenant, secrets or retention implementation.
3. No real OCR/model connector in this self-contained proof.
4. No measured willingness to pay.
5. One pack does not prove repeatability.
6. Hash chaining is not authenticated signing.
7. Linear ROI omits integration and infrastructure step costs.

These require the four-month pilot; copy cannot fix them.

Safe claim: “A verified synthetic proof and pilot kit that converts existing extraction into evidence-linked decisions and blocks unsafe staging release.”

Unsafe claim: “Production-ready autonomous compliance platform saving millions.”
