# Dependency and license notes

## Reconciliation module

`genuity_reconcile` uses only the Python standard library at runtime. Its demo, reconciliation, batch processing, SQLite export, verification, blind-truth evaluation, ROI estimator, review ledger, resilience checks, and tests do not require NumPy, pandas, a model SDK, or a network call.

The optional crop adapter in the demo is simulated. A production model adapter will introduce its own SDK terms, data-processing terms, model usage policy, regional availability, and pricing obligations; approve those separately with the client.

## Distribution boundary

The repository's existing `genuity-axiom` distribution declares NumPy and pandas dependencies for other packages. Those dependencies are not imported by `genuity_reconcile`, but they remain installation requirements of the combined wheel as currently packaged. A production release should either:

1. split reconciliation into its own minimal distribution, or
2. retain the combined distribution and complete dependency/license review for every shipped package.

## License status

No root `LICENSE` or `NOTICE` file was found during this implementation pass. That means the code should not be offered to external customers or published as open source until the owner selects and documents the intended license and confirms rights to all pre-existing repository content.

The generated industrial fixture is synthetic and non-confidential. External web sources are linked as factual pricing/standards references; their page content is not redistributed.

## Production due-diligence checklist

- Add the owner-approved root license and copyright notice.
- Generate an SBOM from the final release artifact, not the development workspace.
- Scan the release artifact for vulnerabilities and prohibited licenses.
- Review OCR/model vendor terms, data residency, retention, and training-use settings.
- Define ownership and permitted reuse of each client domain pack and regression packet.
- Add a data-retention/deletion schedule for OCR payloads, evidence, caches, review ledgers, and exports.
- Add external signing/key management if artifact or reviewer authenticity is required.
