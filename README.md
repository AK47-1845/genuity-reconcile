# Genuity Reconcile Engine

**Author:** Adari Karthikeya
**Status:** Open Source Core

An industrial-grade, evidence-first data reconciliation and validation framework built for complex agentic pipelines.

This engine is designed to ingest raw OCR outputs (or multi-modal extractions) from highly complex documents, run multi-layered policy checks, build deterministic graph links, and output fully reconciled, database-ready canonical records. It does not blindly trust ML models—it enforces strict auditing, source-authority ranking, and falsifiable validation.

## Repository map

- `adapters.py`, `pipeline.py`, `audit.py`, ... — core reconcile engine (root)
- `usecase1-pilot-kit/` — complete self-contained proof + pilot kit for the first
  industrial-document reconciliation use case. Start at
  [`usecase1-pilot-kit/START_HERE.md`](usecase1-pilot-kit/START_HERE.md), then
  `DEMO.md`. One-command demo: `run_demo.ps1`.
- `proof-batch-9-images/` — concrete worked proof: nine real MTR/inspection
  images reconciled into chemistry, hardness, mechanical, and exception tables
  with nothing invented for obscured cells.

Live client demo of this engine: [ltts-aerospace-mtr-validation](https://github.com/AK47-1845/ltts-aerospace-mtr-validation) —
12-document SA-240 304L chain processed in under a second.

## Key Features
- **Deterministic Reconciliation:** Plugs directly into existing extraction outputs to synthesize conflict-free records.
- **Fail-Closed Architecture:** Strict provenance tracing, graph integrity, cache validation, and duplicate rejection.
- **Immutable Auditing:** Generates SQLite ledgers with full decision audit trails, candidate fields, and block-chain-like content hashes.
- **Agentic Resilience:** Includes self-testing injections (malformed-input, quarantine, omission, cache-tamper).
- **Scale-Ready:** Fully isolated batch processing capable of 1,000+ page concurrency without mixing entity scopes.

## Installation
Clone the repository and run the framework locally:

```bash
git clone https://github.com/AK47-1845/genuity-reconcile.git
cd genuity-reconcile
```

## Running the Engine
Execute a full end-to-end reconciliation demonstration which generates mock packets, reconciles them, runs a 1,000-page benchmark, and outputs validation metrics:
```bash
python -m genuity_reconcile demo --output-dir genuity_demo_output
```

Process a real OCR-result folder:
```bash
python -m genuity_reconcile run \
  --ocr-dir <folder> \
  --output-dir <folder> \
  --domain-pack domain_packs/industrial_material_packet.json \
  --cache-dir <cache-folder>
```

Or run the pilot kit end to end:

```bash
cd usecase1-pilot-kit
./run_demo.ps1
```

## Safety Semantics
- `PROPOSED` values always require confirmation.
- `CONFLICT` is never silently resolved.
- Required fields omitted by OCR are materialized as unresolved exceptions.
- Export fails closed if provenance, acceptance-policy, or integrity checks fail.

## Verification
The engine ships with a full 51-test standard library suite:
```bash
python -m unittest discover -s tests -p "test_genuity_reconcile.py" -v
```

*Built to handle the sim-to-real gap and deterministic reconciliation for high-stakes industrial use cases.*
