import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ATLAS_ROOT = SKILL_ROOT / "assets" / "wer-ea-atlas"


class WerEaAtlasTest(unittest.TestCase):
    def test_wer_ea_atlas_spec_contains_required_families(self):
        spec = ATLAS_ROOT / "asset-specs.csv"
        self.assertTrue(spec.exists(), "WER-EA atlas asset-specs.csv should exist")
        with spec.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertGreaterEqual(len(rows), 20)
        required_columns = {
            "asset_id",
            "family",
            "review_use",
            "panel_structure",
            "required_evidence",
            "claim_boundary",
            "caption_pattern",
            "source_learning_basis",
            "certainty_encoding",
            "source_data_template",
            "script",
            "exports",
            "qa_status",
        }
        self.assertEqual(required_columns, set(rows[0]))

        families = {row["family"] for row in rows}
        for family in [
            "wer-ea-mechanism-map",
            "evidence-heatmap",
            "material-system-map",
            "performance-mechanism-boundary",
            "literature-screening-flow",
            "graphical-abstract",
            "dosage-workability-window",
            "emulsion-stability-timeline",
            "curing-demulsification-sequence",
            "bonding-performance-comparison",
            "pull-off-shear-method-comparison",
            "rheology-performance-link",
            "ftir-peak-assignment-card",
            "sem-fluorescence-image-plate",
            "durability-retention-map",
            "water-aging-freeze-thaw-challenge-map",
            "test-standard-condition-card",
            "construction-application-workflow",
            "sustainability-lca-boundary-card",
            "research-gap-matrix",
        ]:
            self.assertIn(family, families)

        combined = "\n".join(",".join(row.values()) for row in rows)
        self.assertIn("template only", combined)
        self.assertNotIn("C:\\Users", combined)

    def test_wer_ea_atlas_data_templates_have_required_headers(self):
        expected = {
            "mechanism_edges.csv": [
                "edge_id",
                "from_node",
                "to_node",
                "evidence_layer",
                "certainty_tier",
                "source_anchor",
                "caption_boundary",
            ],
            "evidence_heatmap.csv": [
                "paper_id",
                "evidence_layer",
                "certainty_tier",
                "source_role",
                "reviewer_risk",
            ],
            "material_systems.csv": [
                "system_id",
                "asphalt_type",
                "emulsifier",
                "epoxy_type",
                "curing_agent",
                "dosage_range",
                "preparation_route",
            ],
            "performance_boundary.csv": [
                "claim_id",
                "performance_metric",
                "mechanism_evidence",
                "certainty_tier",
                "boundary_note",
            ],
            "screening_flow.csv": [
                "stage",
                "input_count",
                "output_count",
                "exclusion_reason",
                "source_anchor",
            ],
            "dosage_window.csv": [
                "formulation_id",
                "wer_dosage",
                "viscosity",
                "bonding_strength",
                "storage_stability",
                "workability_flag",
            ],
            "durability_retention.csv": [
                "condition",
                "baseline_value",
                "conditioned_value",
                "retention_percent",
                "protocol",
            ],
            "characterization_panel.csv": [
                "panel_id",
                "method",
                "signal_or_image",
                "source_anchor",
                "interpretation_boundary",
            ],
            "construction_workflow.csv": [
                "step_id",
                "operation",
                "control_variable",
                "quality_check",
                "field_relevance",
            ],
            "lca_boundary.csv": [
                "boundary_id",
                "functional_unit",
                "system_boundary",
                "inventory_basis",
                "comparison_limit",
            ],
            "research_gap_matrix.csv": [
                "gap_id",
                "evidence_layer",
                "available_evidence",
                "missing_evidence",
                "reviewer_risk",
            ],
        }

        for filename, header in expected.items():
            path = ATLAS_ROOT / "data" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle)
                self.assertEqual(header, next(reader))

    def test_generate_atlas_creates_svg_and_png_outputs(self):
        script = SKILL_ROOT / "scripts" / "wer_ea_atlas" / "generate_atlas.py"
        self.assertTrue(script.exists(), "generate_atlas.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(script), "--output-dir", tmp, "--json"],
                check=True,
                capture_output=True,
                text=True,
            )

            report = json.loads(result.stdout)
            self.assertEqual("pass", report["status"])
            self.assertGreaterEqual(len(report["generated"]), 10)

            for row in report["generated"]:
                svg = Path(row["svg"])
                png = Path(row["png"])
                self.assertTrue(svg.exists())
                self.assertTrue(png.exists())
                self.assertGreater(svg.stat().st_size, 500)
                self.assertGreater(png.stat().st_size, 100)
                svg_text = svg.read_text(encoding="utf-8")
                self.assertIn("<svg", svg_text)
                self.assertIn("template only", svg_text)

    def test_generated_assets_include_certainty_legend(self):
        script = SKILL_ROOT / "scripts" / "wer_ea_atlas" / "generate_atlas.py"
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(script), "--output-dir", tmp, "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            combined = "\n".join(path.read_text(encoding="utf-8") for path in Path(tmp).glob("*.svg"))

        for term in ["measured", "inferred", "speculative", "missing"]:
            self.assertIn(term, combined)


if __name__ == "__main__":
    unittest.main()
