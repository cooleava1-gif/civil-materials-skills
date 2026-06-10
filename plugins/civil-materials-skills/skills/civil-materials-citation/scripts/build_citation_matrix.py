#!/usr/bin/env python3
"""Create a civil materials literature search and citation matrix CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


MCP_ROOT = Path(__file__).resolve().parents[1] / "mcp"
sys.path.insert(0, str(MCP_ROOT))

from academic_search.domain.classifier import DURABILITY_LAYERS, classify_evidence_layers, evidence_type_for_claim
from academic_search.domain.journals import expand_journal_terms


DEFAULT_CLAIMS = [
    "Research gap and novelty",
    "Material design rationale",
    "Performance improvement",
    "Mechanism explanation",
    "Durability or service-condition relevance",
]

CSV_FIELDS = [
    "claim_id",
    "priority",
    "claim_or_need",
    "evidence_layer",
    "source_role",
    "source_quality",
    "mechanism_directness",
    "durability_relevance",
    "service_relevance",
    "reader_anchor",
    "figure_handoff",
    "reviewer_risk",
    "search_query",
    "target_journals",
    "evidence_type",
    "candidate_source",
    "status",
    "manuscript_location",
    "risk_note",
]


def split_items(value: str) -> list[str]:
    items = []
    for item in value.replace(";", ",").split(","):
        cleaned = item.strip()
        if cleaned and cleaned not in items:
            items.append(cleaned)
    return items


def read_claims(path: str | None) -> list[str]:
    if not path:
        return DEFAULT_CLAIMS
    claims_path = Path(path)
    if not claims_path.exists():
        raise FileNotFoundError(f"claims file not found: {path}")
    lines = claims_path.read_text(encoding="utf-8").splitlines()
    claims = [line.strip(" -\t") for line in lines if line.strip()]
    return claims or DEFAULT_CLAIMS


def build_query(topic: str, claim: str, journals: list[str]) -> str:
    journal_terms = " OR ".join(f'"{journal}"' for journal in expand_journal_terms(journals))
    claim_terms = claim.replace("Research gap and novelty", "review OR recent progress")
    return f'("{topic}") AND ({claim_terms}) AND ({journal_terms})'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Research topic or material system.")
    parser.add_argument("--journals", default="CBM,JBE,RMPD,IJPE", help="Comma-separated journal aliases.")
    parser.add_argument("--claims-file", help="Optional text file with one claim/evidence need per line.")
    parser.add_argument("--output", default="civil-materials-citation-matrix.csv")
    args = parser.parse_args()

    topic = args.topic.strip()
    if not topic:
        raise ValueError("--topic must not be empty")

    journals = split_items(args.journals)
    journal_terms = expand_journal_terms(journals)
    claims = read_claims(args.claims_file)
    rows = []
    for idx, claim in enumerate(claims, 1):
        evidence_type = evidence_type_for_claim(claim)
        evidence_layer = (classify_evidence_layers(claim) or [_default_layer_for_evidence_type(evidence_type)])[0]
        rows.append(
            {
                "claim_id": f"CIT-{idx:03d}",
                "priority": "must-fix" if idx <= 2 else "strengthen",
                "claim_or_need": claim,
                "evidence_layer": evidence_layer,
                "source_role": _source_role_for_evidence_type(evidence_type),
                "source_quality": "screening needed",
                "mechanism_directness": _mechanism_directness(evidence_type),
                "durability_relevance": _durability_relevance(evidence_type, evidence_layer),
                "service_relevance": _service_relevance(evidence_layer),
                "reader_anchor": "[reader anchor needed]",
                "figure_handoff": "not assessed",
                "reviewer_risk": "must-fix" if idx <= 2 else "strengthen",
                "search_query": build_query(topic, claim, journals),
                "target_journals": "; ".join(journal_terms),
                "evidence_type": evidence_type,
                "candidate_source": "[search needed]",
                "status": "search needed",
                "manuscript_location": "[assign section]",
                "risk_note": "Do not make this claim until a confirmed source is mapped.",
            }
        )

    with Path(args.output).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)
    return 0


def _default_layer_for_evidence_type(evidence_type: str) -> str:
    if evidence_type == "mechanism":
        return "microstructure_chemistry"
    if evidence_type == "durability":
        return "moisture_aging_durability"
    if evidence_type == "review/positioning":
        return "review_background"
    if evidence_type == "performance":
        return "bonding_interface_performance"
    return "material_formulation"


def _source_role_for_evidence_type(evidence_type: str) -> str:
    if evidence_type == "review/positioning":
        return "review evidence"
    return "primary experimental evidence"


def _mechanism_directness(evidence_type: str) -> str:
    if evidence_type == "mechanism":
        return "direct mechanism evidence needed"
    return "not a mechanism claim"


def _durability_relevance(evidence_type: str, evidence_layer: str) -> str:
    if evidence_type == "durability" or evidence_layer in DURABILITY_LAYERS:
        return "direct durability evidence needed"
    return "not a durability claim"


def _service_relevance(evidence_layer: str) -> str:
    if evidence_layer == "service_field_relevance":
        return "direct service or field evidence needed"
    return "lab-scale unless field evidence is mapped"


if __name__ == "__main__":
    raise SystemExit(main())
