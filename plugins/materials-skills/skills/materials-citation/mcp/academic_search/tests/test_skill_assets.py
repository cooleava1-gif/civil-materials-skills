import csv
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[3]


class CitationSkillAssetsTest(unittest.TestCase):
    def test_citation_matrix_template_contains_review_handoff_fields(self):
        template = SKILL_ROOT / "assets" / "templates" / "citation-matrix-template.csv"

        with template.open(encoding="utf-8-sig", newline="") as handle:
            fieldnames = next(csv.reader(handle))

        self.assertEqual(
            fieldnames[:12],
            [
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
            ],
        )

    def test_wer_ea_screening_reference_defines_source_quality_contract(self):
        reference = SKILL_ROOT / "references" / "wer-ea-screening-and-source-quality.md"
        text = reference.read_text(encoding="utf-8")

        for phrase in (
            "primary experimental evidence",
            "review evidence",
            "method evidence",
            "standard/specification",
            "weak background",
            "material_formulation",
            "moisture_aging_durability",
            "service_field_relevance",
            "exclusion flags",
            "short-term only",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_manifest_routes_wer_ea_screening_and_reviewer_safe_package(self):
        manifest = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")

        self.assertIn("wer-ea-screening", manifest)
        self.assertIn("source-quality", manifest)
        self.assertIn("reviewer-safe-package", manifest)
        self.assertIn("references/wer-ea-screening-and-source-quality.md", manifest)


if __name__ == "__main__":
    unittest.main()
