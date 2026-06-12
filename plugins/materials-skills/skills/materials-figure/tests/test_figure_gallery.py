import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
FIGURES_ROOT = SCRIPTS_ROOT / "figures4materials"


class FigureGalleryReferencesTest(unittest.TestCase):
    def test_chart_atlas_and_style_presets_exist(self):
        atlas = SKILL_ROOT / "references" / "chart-atlas.md"
        presets = SKILL_ROOT / "assets" / "templates" / "figure-style-presets.yaml"
        self.assertTrue(atlas.exists())
        self.assertTrue(presets.exists())
        text = atlas.read_text(encoding="utf-8")
        for phrase in ["bonding strength", "dosage-performance", "FTIR", "radar", "code pattern"]:
            self.assertIn(phrase, text)
        preset_text = presets.read_text(encoding="utf-8")
        for preset in ["cbm", "ccc", "rmpd_ijpe", "jbe"]:
            self.assertIn(f"{preset}:", preset_text)

    def test_all_figures4materials_scripts_exist(self):
        expected = [
            "plot_bonding_strength_comparison.py",
            "plot_dosage_performance_curve.py",
            "plot_ftir_curing_evidence.py",
            "plot_durability_retention.py",
            "plot_mechanical_property_radar.py",
            "plot_rheology_flow_curve.py",
            "plot_psd_gradation.py",
            "plot_creep_recovery.py",
            "plot_sn_fatigue.py",
            "plot_tg_dsc_thermal.py",
            "plot_hydration_heat.py",
            "plot_ternary_phase.py",
            "plot_weibull_strength.py",
            "plot_stress_strain.py",
            "plot_dma_thermomechanical.py",
            "plot_water_absorption.py",
            "plot_multi_panel_performance.py",
        ]
        for script in expected:
            self.assertTrue((FIGURES_ROOT / script).exists(), f"{script} should exist")

    def test_each_new_figures4materials_script_generates_svg_and_png(self):
        new_scripts = [
            "plot_rheology_flow_curve.py",
            "plot_psd_gradation.py",
            "plot_creep_recovery.py",
            "plot_sn_fatigue.py",
            "plot_tg_dsc_thermal.py",
            "plot_hydration_heat.py",
            "plot_ternary_phase.py",
            "plot_weibull_strength.py",
            "plot_stress_strain.py",
            "plot_dma_thermomechanical.py",
            "plot_water_absorption.py",
            "plot_multi_panel_performance.py",
        ]
        for script in new_scripts:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as tmp:
                result = subprocess.run(
                    [sys.executable, str(FIGURES_ROOT / script), "--output-dir", tmp],
                    check=True, capture_output=True, text=True,
                )
                self.assertIn("Caption:", result.stdout)
                svgs = list(Path(tmp).glob("*.svg"))
                pngs = list(Path(tmp).glob("*.png"))
                self.assertEqual(len(svgs), 1)
                self.assertEqual(len(pngs), 1)
                svg_text = Path(svgs[0]).read_text(encoding="utf-8")
                self.assertIn("<svg", svg_text)

    def test_all_plot_lib_functions_exposed(self):
        import importlib.util

        module_path = SCRIPTS_ROOT / "materials_plot_lib.py"
        spec = importlib.util.spec_from_file_location("materials_plot_lib", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        expected_functions = [
            "apply_pub_style",
            "make_grouped_bar",
            "make_line_trend",
            "make_radar",
            "make_xrd_pattern",
            "make_ftir_overlay",
            "add_panel_label",
            "add_error_bars",
            "finalize_figure",
            "make_heatmap",
            "make_stacked_bar",
            "make_boxplot",
            "make_tga_dtg_overlay",
            "make_flow_curve",
            "make_psd_curve",
            "make_creep_recovery",
            "make_sn_curve",
            "make_tg_dsc_overlay",
            "make_heat_flow_curve",
            "make_ternary",
            "make_weibull_plot",
            "make_stress_strain",
            "make_dma_curve",
            "make_absorption_curve",
            "make_multi_panel",
        ]
        for name in expected_functions:
            self.assertTrue(hasattr(module, name), f"{name} should be exposed in plot lib")


if __name__ == "__main__":
    unittest.main()
