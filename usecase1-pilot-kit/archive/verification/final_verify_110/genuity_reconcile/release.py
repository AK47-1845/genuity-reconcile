"""Fail-closed operational release decisions for reconciled records.

Reconciliation answers whether a value is supported.  This module answers a
different question: may the connected record be written to a controlled target
system?  Those decisions must never be inferred from an average quality score.
"""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


ALLOWED_TARGETS = {"SANDBOX", "QMS_STAGING", "ERP_STAGING", "PLM_STAGING"}
REQUIRED_APPROVAL_ROLES = ("domain_owner", "quality_owner", "system_owner")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def release_scope_sha256(
    connected_record: dict[str, Any],
    decisions: list[dict[str, Any]],
    domain_pack: dict[str, Any],
) -> str:
    """Bind approval to the exact record, field decisions, and policy pack."""
    return hashlib.sha256(_canonical({
        "connected_record": connected_record,
        "field_decisions": decisions,
        "domain_pack": domain_pack,
    })).hexdigest()


def load_approvals(path: str | Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Release approvals must be a JSON array")
    required = {"approval_id", "role", "reviewer", "approved_at_utc", "scope_sha256", "target", "decision"}
    seen: set[str] = set()
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict) or not required.issubset(item):
            raise ValueError(f"Approval {index} is missing required fields")
        if item["approval_id"] in seen:
            raise ValueError(f"Duplicate approval_id: {item['approval_id']}")
        seen.add(item["approval_id"])
        if item["role"] not in REQUIRED_APPROVAL_ROLES:
            raise ValueError(f"Approval {index} has unsupported role: {item['role']}")
        if item["decision"] != "APPROVE":
            raise ValueError(f"Approval {index} must explicitly use decision APPROVE")
        if not str(item["reviewer"]).strip():
            raise ValueError(f"Approval {index} requires a named reviewer")
        try:
            timestamp = datetime.fromisoformat(str(item["approved_at_utc"]).replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"Approval {index} approved_at_utc must be ISO-8601") from exc
        if timestamp.utcoffset() is None or timestamp.utcoffset().total_seconds() != 0:
            raise ValueError(f"Approval {index} approved_at_utc must be UTC")
    return payload


def build_operational_release(
    *,
    connected_record: dict[str, Any],
    decisions: list[dict[str, Any]],
    exceptions: list[dict[str, Any]],
    integrity_report: dict[str, Any],
    domain_pack: dict[str, Any],
    target: str = "QMS_STAGING",
    approvals: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return an auditable, non-compensating operational release decision."""
    if target not in ALLOWED_TARGETS:
        raise ValueError(f"Unsupported release target {target!r}; allowed: {sorted(ALLOWED_TARGETS)}")
    approvals = approvals or []
    scope_hash = release_scope_sha256(connected_record, decisions, domain_pack)
    accepted = [item for item in decisions if item.get("acceptance") == "ACCEPTED"]
    unsupported_accepted = [item["field_id"] for item in accepted if not item.get("evidence_ids")]
    unsafe_accepted = [item["field_id"] for item in accepted if not item.get("safe_for_operational_use")]
    blocking = [item["exception_id"] for item in exceptions if item.get("blocking")]
    unresolved_critical = [
        item["field_id"] for item in decisions
        if item.get("critical") and item.get("acceptance") != "ACCEPTED"
    ]
    scoped = [
        item for item in approvals
        if item.get("scope_sha256") == scope_hash and item.get("target") == target
    ]
    approved_roles = sorted({item["role"] for item in scoped})
    missing_roles = [role for role in REQUIRED_APPROVAL_ROLES if role not in approved_roles]

    gates = [
        {"gate": "integrity", "pass": integrity_report.get("status") == "PASS", "detail": integrity_report.get("status")},
        {"gate": "accepted_field_evidence", "pass": not unsupported_accepted, "detail": unsupported_accepted},
        {"gate": "accepted_field_operational_safety", "pass": not unsafe_accepted, "detail": unsafe_accepted},
        {"gate": "blocking_exceptions", "pass": not blocking, "detail": blocking},
        {"gate": "critical_fields_resolved", "pass": not unresolved_critical, "detail": unresolved_critical},
    ]
    safety_failures = [item["gate"] for item in gates if not item["pass"]]
    approval_gate = {
        "gate": "named_scoped_approvals",
        "pass": target == "SANDBOX" or not missing_roles,
        "detail": {"approved_roles": approved_roles, "missing_roles": missing_roles},
    }
    gates.append(approval_gate)

    if target == "SANDBOX":
        status = "SANDBOX_ONLY"
        writeback_allowed = False
    elif safety_failures or missing_roles:
        status = "REVIEW_REQUIRED"
        writeback_allowed = False
    else:
        status = "APPROVED_FOR_CONTROLLED_STAGING"
        writeback_allowed = True

    return {
        "schema_version": "1.0.0",
        "status": status,
        "target": target,
        "writeback_allowed": writeback_allowed,
        "scope_sha256": scope_hash,
        "gates": gates,
        "safety_failures": safety_failures,
        "required_approval_roles": list(REQUIRED_APPROVAL_ROLES),
        "accepted_approval_ids": [item["approval_id"] for item in scoped],
        "operating_rule": "No weighted score can override a failed gate; production write-back requires a separate client-controlled promotion.",
    }


def build_release_from_output(
    output_dir: str | Path,
    *,
    target: str = "QMS_STAGING",
    approvals_path: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(output_dir)
    read = lambda name: json.loads((root / name).read_text(encoding="utf-8"))
    return build_operational_release(
        connected_record=read("canonical_records.json"),
        decisions=read("field_decisions.json"),
        exceptions=read("review_queue.json"),
        integrity_report=read("integrity_report.json"),
        domain_pack=read("domain_pack_snapshot.json"),
        target=target,
        approvals=load_approvals(approvals_path),
    )
