#!/usr/bin/env python3
"""Round 2: validate_handoffs.py - Handoff contract validator."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = REPO_ROOT / "_shared" / "contracts"

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

# Expected handoff topology (declared both in manifest and in contracts)
EXPECTED_PROVIDES: dict[str, list[str]] = {
    "civil-materials-citation": ["citation-handoff"],
    "civil-materials-reader": ["reader-package"],
    "civil-materials-figure": ["figure-handoff"],
    "civil-materials-data": ["data-package"],
    "civil-materials-research": ["gate-report"],
}

EXPECTED_CONSUMES: dict[str, list[dict]] = {
    "civil-materials-reader": [{"handoff": "citation-handoff", "optional": True}],
    "civil-materials-figure": [
        {"handoff": "citation-handoff", "optional": True},
        {"handoff": "reader-package", "optional": True},
        {"handoff": "data-package", "optional": True},
    ],
    "civil-materials-research": [
        {"handoff": "citation-handoff", "optional": False},
        {"handoff": "reader-package", "optional": False},
        {"handoff": "figure-handoff", "optional": False},
        {"handoff": "data-package", "optional": False},
        {"handoff": "gate-report", "optional": True},
    ],
    "civil-materials-writing": [{"handoff": "reader-package", "optional": True}],
    "civil-materials-paper2ppt": [{"handoff": "figure-handoff", "optional": True}],
    "civil-materials-pptx": [{"handoff": "figure-handoff", "optional": True}],
}


def load_contract(name: str) -> dict | None:
    """Load a contract YAML by name."""
    import yaml
    path = CONTRACTS_DIR / f"{name}.yaml"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def validate_all() -> dict[str, list[str]]:
    """Run all handoff contract checks. Returns {skill_or_category: [issues]}."""
    issues: dict[str, list[str]] = {}

    # Gather all provides and consumes from manifests
    manifest_provides: dict[str, list[str]] = {}
    manifest_consumes: dict[str, list[dict]] = {}
    for skill_name in ALL_SKILLS:
        manifest_path = SKILLS_ROOT / skill_name / "manifest.yaml"
        if not manifest_path.exists():
            continue
        import yaml
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = yaml.safe_load(f)
        except Exception:
            issues[skill_name] = [f"could not parse manifest.yaml"]
            continue

        h = manifest.get("handoffs", {})
        if isinstance(h, dict):
            manifest_provides[skill_name] = list(h.get("provides", {}).keys())
            manifest_consumes[skill_name] = h.get("consumes", [])
        elif isinstance(h, list):
            # Legacy format — will be flagged
            manifest_provides[skill_name] = []
            manifest_consumes[skill_name] = []

    # Check 1: Every EXPECTED_PROVIDES matches manifest
    for skill, expected_provides in EXPECTED_PROVIDES.items():
        actual = manifest_provides.get(skill, [])
        for p in expected_provides:
            if p not in actual:
                issues.setdefault(skill, []).append(
                    f"expected provides '{p}' but not found in manifest"
                )
        for p in actual:
            if p not in expected_provides:
                issues.setdefault(skill, []).append(
                    f"unexpected provides '{p}' (not in expected topology)"
                )

    # Check 2: Every EXPECTED_CONSUMES matches manifest
    for skill, expected_list in EXPECTED_CONSUMES.items():
        actual_list = manifest_consumes.get(skill, [])
        actual_handoff_names = {
            c["handoff"] if isinstance(c, dict) else c
            for c in actual_list
        }
        for expected in expected_list:
            name = expected["handoff"]
            if name not in actual_handoff_names:
                issues.setdefault(skill, []).append(
                    f"expected consumes '{name}' but not found in manifest"
                )

    # Check 3: Contract file existence
    all_handoff_names = set()
    for provides in manifest_provides.values():
        all_handoff_names.update(provides)
    for clist in manifest_consumes.values():
        for c in clist:
            name = c["handoff"] if isinstance(c, dict) else c
            all_handoff_names.add(name)

    for name in sorted(all_handoff_names):
        if not (CONTRACTS_DIR / f"{name}.yaml").exists():
            issues.setdefault("contracts", []).append(
                f"contract '{name}.yaml' referenced but not found in _shared/contracts/"
            )

    # Check 4: No orphan provides (not consumed by any skill)
    all_consumed: set[str] = set()
    for clist in manifest_consumes.values():
        for c in clist:
            name = c["handoff"] if isinstance(c, dict) else c
            all_consumed.add(name)
    for skill, p_list in manifest_provides.items():
        for p in p_list:
            if p not in all_consumed:
                issues.setdefault(skill, []).append(
                    f"provides '{p}' is not consumed by any skill (orphan)"
                )

    # Check 5: No dangling consumes (references non-existent provide)
    all_provided: set[str] = set()
    for p_list in manifest_provides.values():
        all_provided.update(p_list)
    for skill, clist in manifest_consumes.items():
        for c in clist:
            name = c["handoff"] if isinstance(c, dict) else c
            if name not in all_provided:
                issues.setdefault(skill, []).append(
                    f"consumes '{name}' but no skill provides it (dangling)"
                )

    # Check 6: Contract produced_by matches actual provider
    for name in sorted(all_handoff_names):
        contract = load_contract(name)
        if contract is None:
            continue
        expected_producer = contract.get("produced_by")
        if expected_producer:
            actual_providers = [
                s for s, p in manifest_provides.items() if name in p
            ]
            if expected_producer not in actual_providers:
                issues.setdefault("contracts", []).append(
                    f"contract '{name}' says produced_by={expected_producer} "
                    f"but actual providers are {actual_providers}"
                )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate handoff contracts across all skills")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    issues = validate_all()

    if args.json:
        print(json.dumps({
            "status": "pass" if not issues else "fail",
            "issues": issues,
        }, indent=2, ensure_ascii=False))
    else:
        if issues:
            for category, cat_issues in issues.items():
                for issue in cat_issues:
                    print(f"[{category}] {issue}")
            print(f"\nFAIL: {sum(len(v) for v in issues.values())} handoff issues found")
        else:
            print("PASS: all handoff contracts valid")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
