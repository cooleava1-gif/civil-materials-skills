#!/usr/bin/env python3
"""Audit paper-production weakness-routing CSV and gate-report MD files."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

WEAKNESS_FIELDS = [
    "weakness_id", "source", "severity", "weakness_type", "evidence_gap",
    "route_to", "required_fix", "expected_artifact", "status", "regression_check",
]

GATE_FIELDS = [
    "gate_id", "gate_name", "status", "evidence_checked", "missing_inputs",
    "routed_weakness_ids", "next_skill", "reviewer_risk",
]

VALID_SEVERITY = {"major", "minor", "critical", "controlled"}
VALID_STATUS = {"open", "blocked", "done", "review-needed", "pass", "not_applicable"}
VALID_WEAKNESS_TYPE = {
    "source_anchor_missing", "mechanism_boundary", "overclaim", "underclaim",
    "missing_evidence", "figure_integrity", "logic_gap", "formatting",
    "citation_gap", "dosage_window", "durability_boundary", "service_boundary",
}

VALID_SOURCE_PATTERN = re.compile(r"^(reviewer:\d+|editor|gate:G\d+|self-audit)$")


def audit_files(weakness_path: str | Path, gate_path: str | Path) -> dict:
    weakness_path = Path(weakness_path)
    gate_path = Path(gate_path)
    issues: dict[str, list[str]] = {"weakness_routing": [], "gate_report": []}

    if weakness_path.exists():
        weakness_ids = set()
        with weakness_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != WEAKNESS_FIELDS:
                issues["weakness_routing"].append(f"header mismatch: {reader.fieldnames}")
            else:
                for row_num, row in enumerate(reader, 2):
                    weakness_ids.add(row.get("weakness_id", ""))
                    if row.get("severity") not in VALID_SEVERITY:
                        issues["weakness_routing"].append(
                            f"row {row_num}: invalid severity {row.get('severity')}"
                        )
                    if row.get("status") not in VALID_STATUS:
                        issues["weakness_routing"].append(
                            f"row {row_num}: invalid status {row.get('status')}"
                        )
                    source = row.get("source", "")
                    if source and not VALID_SOURCE_PATTERN.match(source):
                        issues["weakness_routing"].append(
                            f"row {row_num}: invalid source format {source}"
                        )
                    if not row.get("evidence_gap", "").strip():
                        issues["weakness_routing"].append(
                            f"row {row_num}: missing evidence_gap"
                        )
                    if row.get("regression_check", "").strip().lower() in ("maybe", "todo", "tbd", "n/a", ""):
                        issues["weakness_routing"].append(
                            f"row {row_num}: weak regression_check"
                        )

    if gate_path.exists():
        text = gate_path.read_text(encoding="utf-8")
        table_rows = re.findall(r"^\|(.+)\|$", text, re.MULTILINE)
        found_gate = False
        for row in table_rows:
            cells = [c.strip() for c in row.split("|")]
            if len(cells) >= 3 and re.match(r"G\d+$", cells[0]):
                found_gate = True
                gate_id = cells[0]
                status = cells[2]
                if status not in VALID_STATUS:
                    issues["gate_report"].append(f"{gate_id}: invalid status in row")
                if len(cells) >= 6:
                    routed = cells[5]
                    if routed and routed != "none":
                        for wid in re.findall(r"W[\w-]+", routed):
                            if weakness_ids and wid not in weakness_ids:
                                issues["gate_report"].append(
                                    f"{gate_id}: unknown weakness id {wid}"
                                )
        if not found_gate:
            issues["gate_report"].append("no gate rows found in table")

    status = "fail" if any(issues.values()) else "pass"
    return {"status": status, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("weakness_csv", help="Path to weakness-routing CSV.")
    parser.add_argument("gate_md", help="Path to gate-report MD.")
    args = parser.parse_args()

    report = audit_files(args.weakness_csv, args.gate_md)
    print(f"status: {report['status']}")
    for category, items in report["issues"].items():
        for item in items:
            print(f"  [{category}] {item}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    import argparse
    raise SystemExit(main())
