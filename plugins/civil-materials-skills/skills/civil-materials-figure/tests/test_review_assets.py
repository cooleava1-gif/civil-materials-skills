import csv
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_INTAKE_FIELDS = [
    "claim_id", "source_anchor", "citation_key_or_doi", "evidence_layer",
    "certainty_tier", "panel_role", "visual_encoding", "caption_boundary",
    "missing_evidence_marker", "reviewer_risk",
]
REQUIRED_CERTAINTY_TIERS = ["measured", "inferred", "speculative", "missing"]


class ReviewFigureIntakeContractTest(unittest.TestCase):
    def test_intake_reference_and_template_define_required_fields(self):
        reference = SKILL_ROOT / "references" / "review-figure-intake.md"
        template = SKILL_ROOT / "assets" / "templates" / "review-figure-intake-template.csv"
        self.assertTrue(reference.exists())
        self.assertTrue(template.exists())
        reference_text = reference.read_text(encoding="utf-8")
        for field in REQUIRED_INTAKE_FIELDS:
            self.assertIn(field, reference_text)
        with template.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(REQUIRED_INTAKE_FIELDS, list(rows[0].keys()))
        self.assertGreaterEqual(len(rows), 4)
        self.assertEqual(set(REQUIRED_CERTAINTY_TIERS), {row["certainty_tier"] for row in rows})

    def test_review_asset_specs_define_thirty_sanitized_assets(self):
        spec = SKILL_ROOT / "assets" / "review-first" / "asset-specs.csv"
        self.assertTrue(spec.exists())
        with spec.open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 30)
        required_columns = {
            "asset_id", "family", "review_use", "panel_structure",
            "required_evidence", "claim_boundary", "caption_pattern", "source_learning_basis",
        }
        self.assertEqual(required_columns, set(rows[0]))
        combined = "\n".join(",".join(row.values()) for row in rows)
        self.assertNotIn("C:\\Users", combined)
        self.assertIn("template only", combined)

    def test_paper_derived_reference_documents_learning_boundary(self):
        reference = SKILL_ROOT / "references" / "paper-derived-visual-patterns.md"
        self.assertTrue(reference.exists())
        text = reference.read_text(encoding="utf-8")
        for phrase in [
            "paper-derived visual patterns", "do not copy paper figures",
            "claim-evidence-boundary", "dosage-workability-window",
            "performance-comparison", "test-matrix-standard",
            "interface-mechanism-map", "30 assets",
        ]:
            self.assertIn(phrase, text)

    def test_contracts_and_qa_distinguish_evidence_certainty(self):
        intake_text = (SKILL_ROOT / "references" / "review-figure-intake.md").read_text(encoding="utf-8")
        qa_text = (SKILL_ROOT / "references" / "figure-qa-contract.md").read_text(encoding="utf-8")
        for text in [intake_text, qa_text]:
            for tier in REQUIRED_CERTAINTY_TIERS:
                self.assertIn(tier, text)


if __name__ == "__main__":
    unittest.main()
