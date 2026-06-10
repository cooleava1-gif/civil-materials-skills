"""Audit civil-materials paper-production routing and gate templates."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


WEAKNESS_REQUIRED_FIELDS = [
    "weakness_id",
    "source",
    "severity",
    "weakness_type",
    "evidence_gap",
    "route_to",
    "required_fix",
    "expected_artifact",
    "status",
    "regression_check",
]

GATE_REQUIRED_FIELDS = [
    "gate_id",
    "gate_name",
    "status",
    "evidence_checked",
    "missing_inputs",
    "routed_weakness_ids",
    "next_skill",
    "reviewer_risk",
]

REQUIRED_GATE_NAMES = [
    "Literature Coverage",
    "Source Anchoring",
    "Mechanism Boundary",
    "Figure And Table Integrity",
    "Manuscript Logic",
    "Reviewer Simulation",
    "Submission Fit",
]


def _missing_fields(found: list[str], required: list[str]) -> list[str]:
    return [field for field in required if field not in found]


def audit_weakness_routing(path: Path) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        return [f"missing {path.as_posix()}"]
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return [f"{path.as_posix()} is empty"]
    missing = _missing_fields(header, WEAKNESS_REQUIRED_FIELDS)
    if missing:
        issues.append(f"{path.as_posix()} missing fields: {', '.join(missing)}")
    return issues


def audit_gate_report(path: Path) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        return [f"missing {path.as_posix()}"]
    text = path.read_text(encoding="utf-8")
    for field in GATE_REQUIRED_FIELDS:
        if field not in text:
            issues.append(f"{path.as_posix()} missing field {field}")
    for gate_name in REQUIRED_GATE_NAMES:
        if gate_name not in text:
            issues.append(f"{path.as_posix()} missing gate {gate_name}")
    return issues


def audit_files(weakness_path: Path, gate_path: Path) -> dict[str, Any]:
    issues = {
        "weakness_routing": audit_weakness_routing(Path(weakness_path)),
        "gate_report": audit_gate_report(Path(gate_path)),
    }
    status = "pass" if not any(issues.values()) else "fail"
    return {
        "status": status,
        "weakness_path": str(weakness_path),
        "gate_path": str(gate_path),
        "issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--weakness-routing",
        type=Path,
        default=Path(__file__).resolve().with_name("weakness-routing-template.csv"),
    )
    parser.add_argument(
        "--gate-report",
        type=Path,
        default=Path(__file__).resolve().with_name("paper-gate-report-template.md"),
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = audit_files(args.weakness_routing, args.gate_report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
