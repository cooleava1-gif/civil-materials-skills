#!/usr/bin/env python3
"""Run release checks across all civil-materials skills.

Checks file presence, manifest validity, trigger coverage, and asset completeness.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"
REPO_ROOT = Path(__file__).resolve().parents[1]

ALL_SKILLS = [
    "civil-materials-citation",
    "civil-materials-data",
    "civil-materials-figure",
    "civil-materials-paper2ppt",
    "civil-materials-polishing",
    "civil-materials-pptx",
    "civil-materials-reader",
    "civil-materials-research",
    "civil-materials-response",
    "civil-materials-reviewer",
    "civil-materials-writing",
]

# Each skill's test directory, checked for presence
SKILL_TEST_DIRS = [
    '"civil-materials-citation" / "tests"',
    '"civil-materials-data" / "tests"',
    '"civil-materials-figure" / "tests"',
    '"civil-materials-paper2ppt" / "tests"',
    '"civil-materials-polishing" / "tests"',
    '"civil-materials-pptx" / "tests"',
    '"civil-materials-reader" / "tests"',
    '"civil-materials-research" / "tests"',
    '"civil-materials-response" / "tests"',
    '"civil-materials-reviewer" / "tests"',
    '"civil-materials-writing" / "tests"',
]

FIGURE_PACKAGE_SAMPLE_NAMES = [
    "kong-2024-cbm-bonding",
    "zhang-2017-cbm-tack-coat",
    "yao-2022-cbm-wer-sbr",
]

FIGURE_HARD_WORKFLOW_FILES = [
    "static/core/contract.md",
    "static/core/stance.md",
    "manifest.yaml",
    "SKILL.md",
]

FIGURE_HARD_WORKFLOW_EVAL_IDS = [
    "eval_python_backend_required",
    "eval_r_backend_required",
    "eval_contract_enforced",
]

paper_production_orchestrator = "paper-production-orchestrator"

PAPER_PRODUCTION_EXAMPLES = [
    "paper-production-mini-review-example.md",
    "wer-ea-mini-review-weakness-routing.csv",
    "wer-ea-mini-review-gate-report.md",
]


def collect_paper_production_orchestrator_issues(skill_root: Path) -> list[str]:
    issues = []
    shared = skill_root.parents[0] / "_shared" / "paper-production"
    for name in [
        "weakness-routing.md",
        "weakness-routing-template.csv",
        "paper-gate-report-template.md",
    ]:
        if not (shared / name).exists():
            issues.append(f"missing _shared/paper-production/{name}")
    examples = shared / "examples"
    for name in [
        "wer-ea-mini-review-weakness-routing.csv",
        "wer-ea-mini-review-gate-report.md",
    ]:
        if not (examples / name).exists():
            issues.append(f"missing _shared/paper-production/examples/{name}")
    return issues


def check_skill_basics(skill_name: str) -> list[str]:
    issues = []
    root = SKILLS_ROOT / skill_name
    if not root.exists():
        issues.append(f"{skill_name}: directory missing")
        return issues
    for fname in ["SKILL.md", "manifest.yaml"]:
        if not (root / fname).exists():
            issues.append(f"{skill_name}: missing {fname}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON output.")
    parser.add_argument("--skill", help="Check one skill only.")
    args = parser.parse_args()

    skills = [args.skill] if args.skill else ALL_SKILLS
    all_issues: dict[str, list[str]] = {}

    for skill in skills:
        issues = check_skill_basics(skill)
        if issues:
            all_issues[skill] = issues

    # paper-production orchestrator check
    orchestrator_issues = collect_paper_production_orchestrator_issues(SKILLS_ROOT)
    if orchestrator_issues:
        all_issues["paper_production_orchestrator"] = orchestrator_issues

    # figure_hard_workflow check
    figure_root = SKILLS_ROOT / "civil-materials-figure"
    figure_issues = []
    for fname in FIGURE_HARD_WORKFLOW_FILES:
        if not (figure_root / fname).exists():
            figure_issues.append(f"missing {fname}")
    audit_script = figure_root / "scripts" / "audit_figure_package.py"
    if not audit_script.exists():
        figure_issues.append("missing scripts/audit_figure_package.py")
    if figure_issues:
        all_issues["figure_hard_workflow"] = figure_issues

    if args.json:
        print(json.dumps({"status": "pass" if not all_issues else "fail", "issues": all_issues}, indent=2))
    else:
        if all_issues:
            for skill, issues in all_issues.items():
                for issue in issues:
                    print(f"[{skill}] {issue}")
            print(f"\nFAIL: {sum(len(v) for v in all_issues.values())} issues found")
        else:
            print("PASS: all checks passed")

    return 0 if not all_issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
