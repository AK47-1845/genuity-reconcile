# Genuity 2.0 Use Case 1 — version 1.1 final verification

Verification date: 2026-08-13 (Asia/Calcutta)

## Release artifact

- Wheel: `release/genuity_reconcile_usecase1-1.1.0-py3-none-any.whl`
- SHA-256: `f03630ddb9459019a817c3cd8bc411973c4ad89960750550705bb1b2b45c31e9`
- Package version imported from isolated installation: `1.1.0`
- Runtime dependencies: none beyond Python 3.10+
- Included operational assets: release engine, industrial domain pack, truth/review/release templates, LTTS workflow selection, adapter mapping and pilot telemetry templates.

The retained 1.0.0 wheel remains a historical baseline. `release/SHA256SUMS.txt` verifies both; 1.1.0 is current.

## Executable results

- 51/51 focused tests pass.
- Python source compiles successfully.
- Source compiles on Python 3.10 and 3.13; all 51 tests pass under Python 3.10 and the primary runtime.
- Ten-behaviour demonstration scorecard: PASS.
- Independent output verification: PASS.
- 12 synthetic pages processed.
- 77 automatically accepted and verified fields.
- 100% evidence coverage for accepted fields in the fixture.
- Six visible exceptions; five are blocking review cases.
- 59 artifacts sealed and verified.
- Semantic fingerprint, domain-pack identity, path safety and artifact hashes: PASS.
- SQLite integrity and JSON/SQLite semantic counts: PASS.
- Six executable resilience injections: PASS.

## Release-control result

The installed 1.1.0 wheel independently recalculated the staging decision:

- artifact verification: `PASS`;
- release status: `REVIEW_REQUIRED`;
- `writeback_allowed`: `false`.

This is expected. The demo contains blocking conflicts/unresolved critical values and has no client approvals. Release gates include evidence, operational safety, blocking exceptions, critical resolution, exact-scope approvals and separation of duties. The release command re-verifies the manifest/artifacts and does not trust a stored integrity label.

## Documentation and data checks

- 17 Markdown files checked with zero broken local links after the LTTS workflow router was added.
- 69 JSON files parsed with zero errors.
- Release checksum verification has zero failures.
- No mojibake markers found in the use-case Markdown set.
- `FILE_CATALOG.md` maps founder, demo, operating, source, templates, outputs and release artifacts.

## Cross-product verification

Genuity Axiom 0.3.0 was installed from its wheel using the configured workspace runtime:

- `genuity_axiom.__version__`: `0.3.0`;
- `pramana.__version__`: `0.3.0` compatibility alias;
- 68 public exports load;
- 27/27 enterprise tests pass;
- the retained industrial and Pramana compatibility smoke tests also pass;
- all 11 packaged domain-pack JSON files are present;
- 20 authoritative Axiom/founder/release documents have 27 local links and zero broken links (frozen archive copies excluded);
- separated Axiom wheel SHA-256: `5eb4c0dd87bda403161bbeb11084e9f55135bdbbfb877066e2efc61aae506f5b`.

## Deliberate limitations

This does not establish LTTS/client accuracy, production capacity, willingness to pay, compliance certification or million-dollar value. Production still requires a client-approved adapter, tenant and packet identity, RBAC/SSO, secret/key management, storage and retention controls, queues/retries, observability, authenticated signing, system-of-record promotion and a blind client holdout.

The immediate next evidence is the four-month validation path in `../FOUNDERS.md`, not another synthetic feature claim.
