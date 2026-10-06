import json
import hashlib
import csv
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from genuity_reconcile.config import load_domain_pack, resolve_default_pack
from genuity_reconcile.cli import validate_output_boundary
from genuity_reconcile.batch import run_packet_batch
from genuity_reconcile.fixtures import generate_demo_packet
from genuity_reconcile.economics import estimate_customer_roi
from genuity_reconcile.evaluation import evaluate_decisions
from genuity_reconcile.pipeline import ReconciliationPipeline, export_result, run_demo
from genuity_reconcile.review_ledger import create_review_ledger, verify_review_ledger
from genuity_reconcile.release import build_operational_release, build_release_from_output, release_scope_sha256
from genuity_reconcile.verification import verify_output


class GenuityReconcileDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls._temp.name) / "demo"
        cls.result = run_demo(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls._temp.cleanup()

    def decision(self, status):
        return next(item for item in self.result.decisions if item.status == status)

    def test_all_ten_behaviours_are_materially_proved(self):
        scorecard = self.result.scorecard
        self.assertTrue(scorecard["all_ten_behaviours_proved"])
        self.assertEqual(10, len(scorecard["behaviours"]))
        self.assertTrue(all(item["result"] == "PASS" for item in scorecard["behaviours"]))

    def test_ocr_error_is_recovered_with_audit_trail(self):
        field = self.decision("RECOVERED_OCR")
        self.assertEqual("PN-7O725", field.original_extraction)
        self.assertEqual("PN-70725", field.value)
        self.assertEqual("ACCEPTED", field.acceptance)
        self.assertTrue(field.evidence_ids)
        self.assertTrue(field.rule_results)
        self.assertTrue(field.alternatives_rejected)

    def test_missing_invoice_part_is_recovered_by_exact_po_join(self):
        field = self.decision("RECOVERED_CROSS_DOCUMENT")
        self.assertIsNone(field.original_extraction)
        self.assertEqual("PN-70725", field.value)
        self.assertGreaterEqual(len(field.evidence_ids), 2)
        self.assertEqual("cross_document_exact_join", field.method)
        self.assertIn("supplier_corroboration", {item["rule"] for item in field.rule_results})

    def test_deterministic_total_is_accepted_but_proposals_are_not(self):
        total = self.decision("DERIVED_DETERMINISTIC")
        self.assertEqual(5625.0, total.value)
        self.assertEqual("ACCEPTED", total.acceptance)
        proposal = self.decision("PROPOSED_CROSS_DOCUMENT")
        self.assertEqual(0.0002, proposal.value)
        self.assertEqual("REVIEW", proposal.acceptance)
        self.assertFalse(proposal.safe_for_operational_use)
        self.assertIn("material_grade_corroboration", {item["rule"] for item in proposal.rule_results})

    def test_statistical_imputation_is_analytics_only(self):
        field = self.decision("ANALYTICS_ONLY")
        self.assertEqual(39.0, field.value)
        self.assertTrue(field.analytics_only)
        self.assertNotEqual("ACCEPTED", field.acceptance)

    def test_conflict_is_not_silently_resolved(self):
        conflict = self.decision("CONFLICT")
        self.assertIsNone(conflict.value)
        self.assertEqual({44, 45}, {item["value"] for item in conflict.alternatives_rejected})
        ranks = {item["document_type"]: item["authority_rank"] for item in conflict.alternatives_rejected}
        self.assertEqual({"purchase_order": 1, "invoice": 2}, ranks)
        self.assertEqual("CONFLICT", self.result.connected_record["quantity"]["status"])
        self.assertIsNone(self.result.connected_record["quantity"]["value"])

    def test_unknowable_field_remains_unresolved(self):
        signoff = next(item for item in self.result.decisions if item.name == "inspector_signoff")
        self.assertIsNone(signoff.value)
        self.assertNotEqual("ACCEPTED", signoff.acceptance)
        queue_item = next(item for item in self.result.exceptions if item["field_name"] == "inspector_signoff")
        self.assertEqual("UNRESOLVED", queue_item["status"])

    def test_cache_revision_and_crop_routing_are_visible(self):
        self.assertEqual(1, self.result.metrics["cache_hits"])
        duplicate = next(doc for doc in self.result.documents if doc.duplicate_of)
        self.assertIn("06_CERTIFICATE", duplicate.duplicate_of)
        old_spec = next(doc for doc in self.result.documents if doc.superseded_by)
        self.assertIn("04_MATERIAL_SPEC", old_spec.superseded_by)
        self.assertEqual(1, self.result.metrics["external_regions_routed"])
        self.assertLess(self.result.scorecard["external_routing_rate"], 0.10)
        vlm = self.decision("PROPOSED_VLM")
        self.assertEqual("REVIEW", vlm.acceptance)

    def test_graph_connects_po_to_test_results_with_evidence(self):
        path = self.result.connected_record["path"]
        self.assertEqual("PO:PO-1001", path[0])
        self.assertEqual("TEST:MECH-W3535", path[-1])
        evidence_edges = [edge for edge in self.result.graph["edges"] if edge["type"] != "duplicate_of"]
        self.assertTrue(any(edge.get("evidence") for edge in evidence_edges))
        cert_link = next(edge for edge in self.result.graph["edges"] if edge["type"] == "references_certificate")
        self.assertEqual(["certificate_number"], cert_link["join_keys"])
        self.assertIn("heat_number", cert_link["corroboration"])
        self.assertGreaterEqual(len(cert_link["evidence"]), 2)
        explanation = self.result.connected_record["material_certificate_link_explanation"]
        self.assertEqual("MTR-900", explanation["answer"])
        self.assertEqual("EVIDENCE_LINKED", explanation["status"])

    def test_safety_targets_and_cost_advantage_pass(self):
        accuracy = self.result.accuracy_report
        self.assertEqual(1.0, accuracy["automatic_acceptance_evidence_coverage"])
        self.assertEqual([], accuracy["unsupported_critical_auto_fills"])
        self.assertEqual(0, accuracy["synthetic_values_represented_as_observed_facts"])
        self.assertEqual(0, accuracy["silent_conflict_resolutions"])
        self.assertEqual(28, accuracy["critical_fields_evaluated"])
        self.assertEqual(1.0, accuracy["critical_field_precision"])
        self.assertEqual(1.0, accuracy["critical_field_automatic_coverage"])
        comparison = self.result.cost_report["comparison"]
        full_page = next(item for item in comparison if item["scenario"] == "D_full_page_VLM")
        selective = next(item for item in comparison if item["scenario"] == "E_Genuity_selective_routing")
        self.assertLess(selective["cost_per_verified_field_usd"], full_page["cost_per_verified_field_usd"])
        self.assertGreater(selective["external_api_cost_usd"], 0)
        self.assertIn("planning assumptions", self.result.cost_report["comparison_basis"]["warning"])

    def test_database_ready_exports_exist_and_parse(self):
        expected = {
            "canonical_records.csv",
            "canonical_records.json",
            "field_decisions.csv",
            "field_decisions.json",
            "evidence.json",
            "exceptions.csv",
            "graph.json",
            "metrics.json",
            "accuracy_report.json",
            "critical_field_benchmark.csv",
            "chemistry_results.csv",
            "mechanical_results.csv",
            "material_requirements.csv",
            "document_links.csv",
            "field_evidence_links.csv",
            "cost_report.json",
            "business_case.json",
            "BUSINESS_CASE.md",
            "integrity_report.json",
            "ocr_input.schema.json",
            "field_decision.schema.json",
            "review_queue.json",
            "resilience_scorecard.json",
            "scale_benchmark.json",
            "genuity_demo.db",
            "run_manifest.json",
            "demo_scorecard.json",
            "domain_pack_snapshot.json",
            "SUMMARY.md",
        }
        self.assertTrue(expected.issubset({path.name for path in self.output.iterdir()}))
        scorecard = json.loads((self.output / "demo_scorecard.json").read_text(encoding="utf-8"))
        self.assertTrue(scorecard["all_ten_behaviours_proved"])

    def test_arbitrary_ocr_input_does_not_inherit_demo_facts(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "PURCHASE ORDER\nPO NUMBER: CLIENT-42\nPART NUMBER: CLIENT-PART",
                "fields": [
                    {"name": "po_number", "value": "CLIENT-42", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "part_number", "value": "CLIENT-PART", "confidence": 0.99, "page": 1, "region": "line"},
                    {"name": "supplier", "value": "Client Supplier", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "quantity", "value": 2, "unit": "pcs", "confidence": 0.99, "page": 1, "region": "line"},
                ],
            }
            (ocr_dir / "client_po.json").write_text(json.dumps(payload), encoding="utf-8")
            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            self.assertEqual("CLIENT-42", result.connected_record["po_number"])
            self.assertEqual("CLIENT-PART", result.connected_record["part_number"])
            self.assertNotIn("PO-1001", json.dumps(result.connected_record))
            self.assertFalse(result.accuracy_report["fixture_ground_truth_available"])

    def test_optional_vlm_route_can_be_disabled(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_demo(Path(temp) / "no_vlm", allow_vlm=False)
            self.assertEqual(0, result.metrics["external_model_calls"])
            self.assertEqual(0, result.metrics["external_regions_routed"])
            certificate_tensile = next(
                item
                for item in result.decisions
                if item.name == "tensile_strength_mpa" and "05_MATERIAL" in item.document_id
            )
            self.assertIsNone(certificate_tensile.value)
            self.assertEqual("MISSING", certificate_tensile.status)

    def test_official_patch_formula_drives_token_cost(self):
        token_calc = self.result.cost_report["token_calculation"]
        self.assertEqual(162, token_calc["crop"]["patch_count"])
        self.assertEqual(263, token_calc["crop"]["image_tokens"])
        self.assertEqual(350, token_calc["crop"]["input_tokens"])
        self.assertEqual(2503, token_calc["full_page"]["input_tokens"])
        self.assertIn("images-vision", token_calc["source"])

    def test_fail_closed_integrity_gate_passes(self):
        report = self.result.integrity_report
        self.assertEqual("PASS", report["status"])
        self.assertEqual(report["checks_total"], report["checks_passed"])
        self.assertTrue(all(item["result"] == "PASS" for item in report["checks"]))
        self.assertTrue(self.result.scorecard["targets"]["provenance_integrity_gate_passed"])

    def test_business_case_is_bottom_up_and_has_sensitivity(self):
        case = self.result.business_case
        self.assertEqual("bottom_up_scenario_not_market_forecast", case["model_type"])
        self.assertEqual(5, len(case["scale_scenarios"]))
        self.assertEqual(4, len(case["human_cost_sensitivity"]))
        self.assertEqual(5, len(case["routing_sensitivity"]))
        self.assertGreater(
            case["unit_economics"]["savings_per_page_vs_full_page_vlm_usd"], 0
        )
        self.assertIn("not a market-size forecast", case["billion_dollar_threshold"]["interpretation"])

    def test_manifest_hashes_and_reproducibility_fingerprint(self):
        manifest = json.loads((self.output / "run_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("PASS", manifest["integrity_status"])
        snapshot = json.loads((self.output / "domain_pack_snapshot.json").read_text(encoding="utf-8"))
        snapshot_hash = hashlib.sha256(
            json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(snapshot_hash, manifest["domain_pack_canonical_sha256"])
        for relative, expected_hash in manifest["artifact_sha256"].items():
            actual = hashlib.sha256((self.output / relative).read_bytes()).hexdigest()
            self.assertEqual(expected_hash, actual, relative)
        with tempfile.TemporaryDirectory() as temp:
            second_output = Path(temp) / "second"
            run_demo(second_output)
            second = json.loads((second_output / "run_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["reproducibility_fingerprint"], second["reproducibility_fingerprint"]
            )
        self.assertEqual("PASS", verify_output(self.output)["status"])

    def test_domain_pack_rejects_unsafe_threshold(self):
        pack = json.loads(resolve_default_pack().read_text(encoding="utf-8"))
        pack["review_threshold"] = 1.1
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.json"
            path.write_text(json.dumps(pack), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "review_threshold"):
                load_domain_pack(path)

    def test_domain_pack_validation_catches_runtime_key_and_authority_errors(self):
        base = json.loads(resolve_default_pack().read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.json"
            missing_dimension = json.loads(json.dumps(base))
            del missing_dimension["pricing"]["vision_tokenization"]["full_page_width_pixels"]
            path.write_text(json.dumps(missing_dimension), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "full_page_width_pixels"):
                load_domain_pack(path)
            bad_authority = json.loads(json.dumps(base))
            bad_authority["source_authority"]["quantity"] = ["invented_document_type"]
            path.write_text(json.dumps(bad_authority), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source_authority"):
                load_domain_pack(path)

    def test_client_roi_calculator_is_editable_and_common_cost_is_fair(self):
        pricing = load_domain_pack(resolve_default_pack())["pricing"]
        report = estimate_customer_roi(
            pricing,
            annual_pages=1_000_000,
            human_hourly_cost_usd=25.0,
            review_minutes_per_case=1.5,
            current_review_cases_per_page=1.0,
            genuity_review_cases_per_page=0.4,
            routed_regions_per_page=0.05,
            existing_extraction_cost_per_page_usd=0.03,
            implementation_cost_usd=100_000,
        )
        self.assertEqual("client_editable_overlay_roi_not_quote", report["scenario_type"])
        self.assertGreater(report["annual"]["recurring_savings_usd"], 0)
        self.assertIsNotNone(report["annual"]["payback_months"])
        self.assertEqual(0.03, report["inputs"]["existing_extraction_cost_per_page_usd"])
        with self.assertRaisesRegex(ValueError, "annual_pages"):
            estimate_customer_roi(
                pricing,
                annual_pages=0,
                human_hourly_cost_usd=25,
                review_minutes_per_case=1.5,
                current_review_cases_per_page=1,
                genuity_review_cases_per_page=0.4,
                routed_regions_per_page=0.05,
                existing_extraction_cost_per_page_usd=0.03,
                implementation_cost_usd=100000,
            )

    def test_client_blind_truth_evaluator_reports_precision_and_abstention(self):
        with tempfile.TemporaryDirectory() as temp:
            decisions_path = Path(temp) / "decisions.json"
            truth_path = Path(temp) / "truth.csv"
            decisions_path.write_text(
                json.dumps(
                    [
                        {"document_id": "D1", "name": "part", "value": "P-1", "acceptance": "ACCEPTED", "evidence_ids": ["E1"]},
                        {"document_id": "D1", "name": "quantity", "value": None, "acceptance": "NOT_ACCEPTED", "evidence_ids": ["E2"]},
                    ]
                ),
                encoding="utf-8",
            )
            truth_path.write_text(
                'document_id,field_name,expected_json,critical\nD1,part,"""P-1""",true\nD1,quantity,45,true\n',
                encoding="utf-8",
            )
            report = evaluate_decisions(decisions_path, truth_path)
            self.assertEqual(1.0, report["critical"]["precision"])
            self.assertEqual(0.5, report["critical"]["automatic_coverage"])
            self.assertEqual(0, report["critical"]["incorrect_auto_accepts"])
            self.assertTrue(report["gate_recommendation"]["zero_incorrect_critical_auto_accepts"])

    def test_thousand_page_scale_smoke_is_duplicate_aware_and_model_free(self):
        scale = self.result.scale_benchmark
        self.assertEqual(1000, scale["documents"])
        self.assertEqual(1000, scale["pages"])
        self.assertEqual(800, scale["unique_documents"])
        self.assertEqual(200, scale["cache_hits"])
        self.assertEqual(0, scale["external_model_calls"])
        self.assertEqual("PASS", scale["integrity_status"])
        self.assertGreater(scale["documents_per_second"], 0)

    def test_executable_failure_injection_scorecard_passes(self):
        resilience = self.result.resilience_scorecard
        self.assertEqual("PASS", resilience["status"])
        self.assertEqual(6, resilience["checks_total"])
        self.assertEqual(6, resilience["checks_passed"])
        self.assertTrue(all(item["result"] == "PASS" for item in resilience["checks"]))

    def test_malformed_ocr_contract_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "PURCHASE ORDER",
                "fields": [
                    {"name": "po_number", "value": "BAD", "confidence": 1.7, "page": 1, "region": "header"}
                ],
            }
            (ocr_dir / "invalid.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "confidence must be between 0 and 1"):
                ReconciliationPipeline(allow_vlm=False).run(ocr_dir)

    def test_vendor_alias_collision_is_rejected_instead_of_first_wins(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "PURCHASE ORDER",
                "fields": [
                    {"name": "po_no", "value": "PO-A", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "po_number", "value": "PO-B", "confidence": 0.99, "page": 1, "region": "header"},
                ],
            }
            (ocr_dir / "collision.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "aliases collapse multiple inputs"):
                ReconciliationPipeline(allow_vlm=False).run(ocr_dir)

    def test_filename_normalization_cannot_create_duplicate_document_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {"page_count": 1, "text": "UNCONFIGURED", "fields": []}
            (ocr_dir / "client-a.json").write_text(json.dumps(payload), encoding="utf-8")
            (ocr_dir / "client_a.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate canonical document IDs"):
                ReconciliationPipeline(allow_vlm=False).run(ocr_dir)

    def test_page_count_is_part_of_content_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            base = {
                "text": "UNCONFIGURED LEGACY SHEET",
                "fields": [
                    {"name": "legacy_id", "value": "L-1", "confidence": 0.99, "page": 1, "region": "header"}
                ],
            }
            (ocr_dir / "one.json").write_text(json.dumps({"page_count": 1, **base}), encoding="utf-8")
            (ocr_dir / "two.json").write_text(json.dumps({"page_count": 2, **base}), encoding="utf-8")
            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            self.assertNotEqual(result.documents[0].content_hash, result.documents[1].content_hash)
            self.assertEqual(0, result.metrics["cache_hits"])

    def test_multiple_po_chains_cannot_be_silently_mixed(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            for index in (1, 2):
                payload = {
                    "page_count": 1,
                    "text": f"PURCHASE ORDER\nPO NUMBER: PO-{index}",
                    "fields": [
                        {"name": "po_number", "value": f"PO-{index}", "confidence": 0.99, "page": 1, "region": "header"},
                        {"name": "part_number", "value": f"PART-{index}", "confidence": 0.99, "page": 1, "region": "line"},
                        {"name": "supplier", "value": "Supplier", "confidence": 0.99, "page": 1, "region": "header"},
                        {"name": "quantity", "value": index, "unit": "pcs", "confidence": 0.99, "page": 1, "region": "line"},
                    ],
                }
                (ocr_dir / f"po_{index}.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Use the batch command"):
                ReconciliationPipeline(allow_vlm=False).run(ocr_dir)

    def test_packet_batch_isolates_chains_and_aggregates_verified_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source"
            for index in (1, 2):
                folder = source / f"packet_{index}"
                folder.mkdir(parents=True)
                payload = {
                    "page_count": 1,
                    "text": f"PURCHASE ORDER\nPO NUMBER: BATCH-{index}",
                    "fields": [
                        {"name": "po_number", "value": f"BATCH-{index}", "confidence": 0.99, "page": 1, "region": "header"},
                        {"name": "part_number", "value": f"PART-{index}", "confidence": 0.99, "page": 1, "region": "line"},
                        {"name": "supplier", "value": "Supplier", "confidence": 0.99, "page": 1, "region": "header"},
                        {"name": "quantity", "value": index, "unit": "pcs", "confidence": 0.99, "page": 1, "region": "line"},
                    ],
                }
                (folder / "po.json").write_text(json.dumps(payload), encoding="utf-8")
            output = Path(temp) / "output"
            report = run_packet_batch(source, output, allow_vlm=False)
            self.assertEqual("PASS", report["status"])
            self.assertEqual(2, report["totals"]["packets"])
            self.assertEqual(2, report["totals"]["pages_processed"])
            self.assertEqual("PASS", verify_output(output / "packet_1")["status"])
            self.assertTrue((output / "batch_summary.json").exists())

    def test_csv_exports_neutralize_spreadsheet_formula_text(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "PURCHASE ORDER\nPO NUMBER: SAFE-1",
                "fields": [
                    {"name": "po_number", "value": "SAFE-1", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "part_number", "value": "PART-1", "confidence": 0.99, "page": 1, "region": "line"},
                    {"name": "supplier", "value": "=HYPERLINK(\"https://bad.invalid\")", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "quantity", "value": 1, "unit": "pcs", "confidence": 0.99, "page": 1, "region": "line"},
                ],
            }
            (ocr_dir / "po.json").write_text(json.dumps(payload), encoding="utf-8")
            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            output = Path(temp) / "output"
            export_result(result, output)
            with (output / "field_decisions.csv").open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            supplier = next(item for item in rows if item["name"] == "supplier")
            self.assertTrue(supplier["value"].startswith("'="))

    def test_sqlite_handoff_is_queryable_and_consistent(self):
        with closing(sqlite3.connect(self.output / "genuity_demo.db")) as connection:
            self.assertEqual("ok", connection.execute("PRAGMA integrity_check").fetchone()[0])
            self.assertEqual(12, connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0])
            self.assertEqual(77, connection.execute("SELECT COUNT(*) FROM field_decisions WHERE acceptance='ACCEPTED'").fetchone()[0])
            self.assertEqual(6, connection.execute("SELECT COUNT(*) FROM exceptions").fetchone()[0])
            conflict = connection.execute("SELECT status FROM exceptions WHERE field_name='quantity'").fetchone()[0]
            self.assertEqual("CONFLICT", conflict)

    def test_exception_queue_has_routing_sla_and_stable_deduplication(self):
        keys = [item["dedupe_key"] for item in self.result.exceptions]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertTrue(all(item["suggested_owner"] for item in self.result.exceptions))
        self.assertTrue(all(item["reason_code"] for item in self.result.exceptions))
        self.assertTrue(all(item["sla_hours"] > 0 for item in self.result.exceptions))
        conflict = next(item for item in self.result.exceptions if item["status"] == "CONFLICT")
        self.assertTrue(conflict["blocking"])
        self.assertEqual("procurement_operations", conflict["suggested_owner"])
        self.assertEqual(4, conflict["sla_hours"])

    def test_human_review_ledger_is_validated_and_tamper_evident(self):
        queue = json.loads((self.output / "review_queue.json").read_text(encoding="utf-8"))
        candidate = next(item for item in queue if item["status"] == "PROPOSED_VLM")
        with tempfile.TemporaryDirectory() as temp:
            resolutions = Path(temp) / "resolutions.csv"
            ledger_path = Path(temp) / "ledger.json"
            resolutions.write_text(
                "exception_id,disposition,resolved_value_json,reviewer,reviewed_at_utc,evidence_reference,note\n"
                f'{candidate["exception_id"]},CONFIRM_CANDIDATE,,qa@example.com,2026-08-12T13:30:00Z,'
                f'{candidate["evidence_ids"][0]},crop inspected\n',
                encoding="utf-8",
            )
            ledger = create_review_ledger(self.output / "review_queue.json", resolutions, ledger_path)
            self.assertEqual(1, ledger["event_count"])
            self.assertEqual("PASS", verify_review_ledger(ledger_path, self.output / "review_queue.json")["status"])
            tampered = json.loads(ledger_path.read_text(encoding="utf-8"))
            tampered["events"][0]["note"] = "silently changed"
            ledger_path.write_text(json.dumps(tampered), encoding="utf-8")
            self.assertEqual("FAIL", verify_review_ledger(ledger_path)["status"])

    def test_independent_verifier_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "copied"
            shutil.copytree(self.output, copied)
            (copied / "SUMMARY.md").write_text("tampered", encoding="utf-8")
            report = verify_output(copied)
            self.assertEqual("FAIL", report["status"])
            self.assertIn("SUMMARY.md", report["hash_mismatches"])

    def test_verifier_rejects_manifest_path_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "copied"
            shutil.copytree(self.output, copied)
            manifest_path = copied / "run_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["artifact_sha256"]["../outside.txt"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report = verify_output(copied)
            self.assertEqual("FAIL", report["status"])
            self.assertEqual(["../outside.txt"], report["unsafe_artifact_paths"])

    def test_verifier_cross_checks_sqlite_counts_even_if_hash_is_recomputed(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "copied"
            shutil.copytree(self.output, copied)
            database_path = copied / "genuity_demo.db"
            with closing(sqlite3.connect(database_path)) as connection:
                connection.execute("DELETE FROM exceptions WHERE exception_id = 'EX-001'")
                connection.commit()
            manifest_path = copied / "run_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["artifact_sha256"]["genuity_demo.db"] = hashlib.sha256(database_path.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report = verify_output(copied)
            self.assertEqual("FAIL", report["status"])
            self.assertFalse(report["sqlite_semantic_counts_match"])

    def test_unknown_document_fields_are_quarantined(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "UNCONFIGURED LEGACY SHEET",
                "fields": [
                    {"name": "part_number", "value": "PN-70725", "confidence": 0.99, "page": 1, "region": "body"}
                ],
            }
            (ocr_dir / "unknown.json").write_text(json.dumps(payload), encoding="utf-8")
            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            field = result.decisions[0]
            self.assertEqual("UNCLASSIFIED_SOURCE", field.status)
            self.assertEqual("REVIEW", field.acceptance)
            self.assertFalse(field.safe_for_operational_use)
            self.assertEqual("PASS", result.integrity_report["status"])

    def test_tied_document_classification_is_quarantined(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "PURCHASE ORDER\nPO NUMBER\nSUPPLIER INVOICE\nINVOICE NUMBER",
                "fields": [
                    {"name": "po_number", "value": "PO-MIXED", "confidence": 0.99, "page": 1, "region": "header"}
                ],
            }
            (ocr_dir / "mixed.json").write_text(json.dumps(payload), encoding="utf-8")
            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            self.assertEqual("unknown", result.documents[0].document_type)
            self.assertEqual("UNCLASSIFIED_SOURCE", result.decisions[0].status)
            self.assertEqual("REVIEW", result.decisions[0].acceptance)

    def test_persistent_model_cache_prevents_repeat_call(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = generate_demo_packet(Path(temp) / "packet")
            cache_dir = Path(temp) / "cache"
            first = ReconciliationPipeline(allow_vlm=True, cache_dir=cache_dir).run(packet["ocr"])
            second = ReconciliationPipeline(allow_vlm=True, cache_dir=cache_dir).run(packet["ocr"])
            self.assertEqual(1, first.metrics["external_model_calls"])
            self.assertEqual(0, first.metrics["model_cache_hits"])
            self.assertEqual(0, second.metrics["external_model_calls"])
            self.assertEqual(1, second.metrics["model_cache_hits"])
            first_value = next(item.value for item in first.decisions if item.status == "PROPOSED_VLM")
            second_value = next(item.value for item in second.decisions if item.status == "PROPOSED_VLM")
            self.assertEqual(first_value, second_value)

    def test_pipeline_instance_resets_batch_state_between_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = generate_demo_packet(Path(temp) / "packet")
            pipeline = ReconciliationPipeline(allow_vlm=False)
            first = pipeline.run(packet["ocr"])
            second = pipeline.run(packet["ocr"])
            self.assertEqual(first.metrics["pages_processed"], second.metrics["pages_processed"])
            self.assertEqual(len(first.evidence), len(second.evidence))
            self.assertEqual(len(first.decisions), len(second.decisions))
            self.assertEqual(first.connected_record, second.connected_record)

    def test_tampered_model_cache_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            packet = generate_demo_packet(Path(temp) / "packet")
            cache_dir = Path(temp) / "cache"
            ReconciliationPipeline(allow_vlm=True, cache_dir=cache_dir).run(packet["ocr"])
            cache_path = next(cache_dir.glob("*.json"))
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            cached["candidate"] = 999999
            cache_path.write_text(json.dumps(cached), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "failed integrity validation"):
                ReconciliationPipeline(allow_vlm=True, cache_dir=cache_dir).run(packet["ocr"])

    def test_domain_pack_can_forbid_an_auto_reconstruction(self):
        with tempfile.TemporaryDirectory() as temp:
            pack = json.loads(resolve_default_pack().read_text(encoding="utf-8"))
            pack["permitted_reconstruction_methods"].remove("quantity_times_unit_price")
            pack_path = Path(temp) / "restricted_pack.json"
            pack_path.write_text(json.dumps(pack), encoding="utf-8")
            packet = generate_demo_packet(Path(temp) / "packet")
            with self.assertRaisesRegex(RuntimeError, "integrity gate rejected output"):
                ReconciliationPipeline(domain_pack=pack_path, allow_vlm=False).run(packet["ocr"])

    def test_omitted_required_fields_become_visible_exceptions(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            payload = {
                "page_count": 1,
                "text": "PURCHASE ORDER\nPO NUMBER: CLIENT-7",
                "fields": [
                    {"name": "po_number", "value": "CLIENT-7", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "part_number", "value": "CLIENT-PART", "confidence": 0.99, "page": 1, "region": "line"},
                ],
            }
            (ocr_dir / "po.json").write_text(json.dumps(payload), encoding="utf-8")
            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            unresolved = {item["field_name"] for item in result.exceptions if item["status"] == "UNRESOLVED"}
            self.assertEqual({"supplier", "quantity"}, unresolved)

    def test_ambiguous_exact_join_is_escalated_not_guessed(self):
        with tempfile.TemporaryDirectory() as temp:
            ocr_dir = Path(temp) / "ocr"
            ocr_dir.mkdir()
            common = {
                "page_count": 1,
                "text": "PURCHASE ORDER\nPO NUMBER: PO-DUP",
            }
            for suffix, part in (("a", "PART-A"), ("b", "PART-B")):
                payload = {
                    **common,
                    "fields": [
                        {"name": "po_number", "value": "PO-DUP", "confidence": 0.99, "page": 1, "region": "header"},
                        {"name": "supplier", "value": "Same Supplier", "confidence": 0.99, "page": 1, "region": "header"},
                        {"name": "part_number", "value": part, "confidence": 0.99, "page": 1, "region": "line"},
                        {"name": "quantity", "value": 1, "unit": "pcs", "confidence": 0.99, "page": 1, "region": "line"},
                    ],
                }
                (ocr_dir / f"po_{suffix}.json").write_text(json.dumps(payload), encoding="utf-8")
            invoice = {
                "page_count": 1,
                "text": "SUPPLIER INVOICE\nINVOICE NUMBER: INV-DUP\nPO NUMBER: PO-DUP",
                "fields": [
                    {"name": "invoice_number", "value": "INV-DUP", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "po_number", "value": "PO-DUP", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "supplier", "value": "Same Supplier", "confidence": 0.99, "page": 1, "region": "header"},
                    {"name": "part_number", "value": None, "confidence": 0.0, "page": 1, "region": "line"},
                    {"name": "quantity", "value": 1, "unit": "pcs", "confidence": 0.99, "page": 1, "region": "line"},
                ],
            }
            (ocr_dir / "invoice.json").write_text(json.dumps(invoice), encoding="utf-8")

            result = ReconciliationPipeline(allow_vlm=False).run(ocr_dir)
            field = next(
                item for item in result.decisions
                if item.document_id == "INVOICE" and item.name == "part_number"
            )
            self.assertEqual("AMBIGUOUS_LINK", field.status)
            self.assertEqual("REVIEW", field.acceptance)
            self.assertIsNone(field.value)
            self.assertEqual({"PART-A", "PART-B"}, {item["value"] for item in field.alternatives_rejected})
            self.assertTrue(any(item["status"] == "AMBIGUOUS_LINK" for item in result.exceptions))
            self.assertIsNone(result.connected_record["part_number"])
            self.assertEqual("part_number", result.connected_record["identity_conflicts"][0]["field_name"])

    def test_demo_is_explicitly_blocked_from_operational_writeback(self):
        release = json.loads((self.output / "operational_release.json").read_text(encoding="utf-8"))
        self.assertEqual("REVIEW_REQUIRED", release["status"])
        self.assertFalse(release["writeback_allowed"])
        self.assertIn("blocking_exceptions", release["safety_failures"])
        self.assertIn("critical_fields_resolved", release["safety_failures"])
        rechecked = build_release_from_output(self.output)
        self.assertEqual("PASS", rechecked.pop("artifact_verification_status"))
        self.assertEqual(release, rechecked)

    def test_approvals_cannot_override_a_failed_safety_gate(self):
        decisions = [{
            "field_id": "F-1", "acceptance": "ACCEPTED", "safe_for_operational_use": True,
            "critical": True, "evidence_ids": [],
        }]
        connected = {"record_id": "R-1"}
        pack = {"name": "test", "version": "1"}
        scope = release_scope_sha256(connected, decisions, pack)
        approvals = [
            {
                "approval_id": f"A-{role}", "role": role, "reviewer": "Named Reviewer",
                "approved_at_utc": "2026-08-13T00:00:00Z", "scope_sha256": scope,
                "target": "QMS_STAGING", "decision": "APPROVE",
            }
            for role in ("domain_owner", "quality_owner", "system_owner")
        ]
        release = build_operational_release(
            connected_record=connected, decisions=decisions, exceptions=[],
            integrity_report={"status": "PASS"}, domain_pack=pack, approvals=approvals,
        )
        self.assertEqual("REVIEW_REQUIRED", release["status"])
        self.assertFalse(release["writeback_allowed"])
        self.assertIn("accepted_field_evidence", release["safety_failures"])

    def test_clean_scoped_record_requires_all_named_roles(self):
        decisions = [{
            "field_id": "F-1", "acceptance": "ACCEPTED", "safe_for_operational_use": True,
            "critical": True, "evidence_ids": ["E-1"],
        }]
        connected = {"record_id": "R-1"}
        pack = {"name": "test", "version": "1"}
        scope = release_scope_sha256(connected, decisions, pack)
        approvals = [
            {
                "approval_id": f"A-{role}", "role": role, "reviewer": f"Reviewer {role}",
                "approved_at_utc": "2026-08-13T00:00:00Z", "scope_sha256": scope,
                "target": "QMS_STAGING", "decision": "APPROVE",
            }
            for role in ("domain_owner", "quality_owner", "system_owner")
        ]
        pending = build_operational_release(
            connected_record=connected, decisions=decisions, exceptions=[],
            integrity_report={"status": "PASS"}, domain_pack=pack, approvals=approvals[:2],
        )
        approved = build_operational_release(
            connected_record=connected, decisions=decisions, exceptions=[],
            integrity_report={"status": "PASS"}, domain_pack=pack, approvals=approvals,
        )
        self.assertEqual("REVIEW_REQUIRED", pending["status"])
        self.assertEqual("APPROVED_FOR_CONTROLLED_STAGING", approved["status"])
        self.assertTrue(approved["writeback_allowed"])

    def test_programmatic_release_cannot_bypass_approval_validation(self):
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            build_operational_release(
                connected_record={"record_id": "R-1"},
                decisions=[],
                exceptions=[],
                integrity_report={"status": "PASS"},
                domain_pack={"name": "test"},
                approvals=[{"role": "domain_owner"}],
            )

    def test_one_reviewer_cannot_hold_multiple_required_release_roles(self):
        decisions = [{
            "field_id": "F-1", "acceptance": "ACCEPTED", "safe_for_operational_use": True,
            "critical": True, "evidence_ids": ["E-1"],
        }]
        connected = {"record_id": "R-1"}
        pack = {"name": "test", "version": "1"}
        scope = release_scope_sha256(connected, decisions, pack)
        approvals = [
            {
                "approval_id": f"A-{role}", "role": role, "reviewer": "Same Person",
                "approved_at_utc": "2026-08-13T00:00:00Z", "scope_sha256": scope,
                "target": "QMS_STAGING", "decision": "APPROVE",
            }
            for role in ("domain_owner", "quality_owner", "system_owner")
        ]
        release = build_operational_release(
            connected_record=connected, decisions=decisions, exceptions=[],
            integrity_report={"status": "PASS"}, domain_pack=pack, approvals=approvals,
        )
        self.assertEqual("REVIEW_REQUIRED", release["status"])
        self.assertIn("separation_of_duties", release["governance_failures"])
        self.assertFalse(release["writeback_allowed"])

    def test_release_check_independently_rejects_tampered_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "tampered"
            shutil.copytree(self.output, copied)
            decisions_path = copied / "field_decisions.json"
            decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
            decisions[0]["value"] = "TAMPERED"
            decisions_path.write_text(json.dumps(decisions), encoding="utf-8")
            release = build_release_from_output(copied)
            self.assertEqual("FAIL", release["artifact_verification_status"])
            self.assertIn("integrity", release["safety_failures"])
            self.assertFalse(release["writeback_allowed"])

    def test_cli_rejects_output_overlap_and_nonempty_run_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_dir = root / "input"
            input_dir.mkdir()
            with self.assertRaisesRegex(ValueError, "must not overlap"):
                validate_output_boundary(input_dir / "result", input_paths=[input_dir])
            output = root / "prior_run"
            output.mkdir()
            (output / "run_manifest.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not empty"):
                validate_output_boundary(output)
            self.assertEqual(output.resolve(), validate_output_boundary(output, allow_existing=True))


if __name__ == "__main__":
    unittest.main()
