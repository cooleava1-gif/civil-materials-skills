#!/usr/bin/env python3
"""Generate all 19 civil materials figures."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1] / "skills" / "civil-materials-figure"
SCRIPTS_ROOT = SKILL_ROOT / "scripts" / "figures4materials"
OUTPUT_ROOT = Path(__file__).resolve().parents[1] / "outputs" / "generated-figures"

SCRIPTS = [
    "plot_bonding_strength_comparison.py",
    "plot_dosage_performance_curve.py",
    "plot_ftir_curing_evidence.py",
    "plot_durability_retention.py",
    "plot_mechanical_property_radar.py",
    "plot_rheology_curve.py",
    "plot_tga_dtg_curve.py",
    "plot_dosage_window.py",
    "plot_particle_size_distribution.py",
    "plot_sem_analysis.py",
    "plot_xrd_pattern.py",
    "plot_property_correlation.py",
    "plot_freeze_thaw_cycle.py",
    "plot_aging_test.py",
    "plot_mechanism_diagram.py",
    "plot_screening_flow.py",
    "plot_graphical_abstract.py",
    "plot_lca_boundary.py",
    "plot_research_gap_matrix.py",
]


def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    success_count = 0
    fail_count = 0

    for script_name in SCRIPTS:
        script_path = SCRIPTS_ROOT / script_name
        if not script_path.exists():
            print(f"SKIP: {script_name} (not found)")
            continue

        print(f"Running: {script_name}")
        try:
            result = subprocess.run(
                [sys.executable, str(script_path), "--output-dir", str(OUTPUT_ROOT)],
                cwd=str(SCRIPTS_ROOT),
                check=True,
                capture_output=True,
                text=True,
            )
            if result.stdout:
                print(f"  Caption: {result.stdout.strip().split('Caption: ')[-1][:80]}...")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: {e.stderr[:200] if e.stderr else str(e)}")
            fail_count += 1

    print(f"\nDone: {success_count} succeeded, {fail_count} failed")
    print(f"Output directory: {OUTPUT_ROOT}")

    # List generated files
    svg_files = sorted(OUTPUT_ROOT.glob("*.svg"))
    png_files = sorted(OUTPUT_ROOT.glob("*.png"))
    print(f"Generated: {len(svg_files)} SVG files, {len(png_files)} PNG files")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())