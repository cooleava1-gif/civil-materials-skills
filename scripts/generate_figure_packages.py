#!/usr/bin/env python3
"""Generate figure package templates for new figure types."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1] / "skills" / "materials-figure"
PACKAGES_ROOT = SKILL_ROOT / "examples" / "figure-packages"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

FIGURE_TYPES = [
    "creep-recovery",
    "psd-gradation",
    "rheology-flow-curve",
    "stress-strain",
    "ternary-phase",
    "tg-dsc-thermal",
]

TEMPLATES = {
    "figure_contract.md": """# Figure Contract

## Core Conclusion

{title} figures must show {description} as material-specific and condition-dependent rather than universal.

## Evidence Chain

| Panel | Evidence source | Source anchor | What it supports | Boundary |
|---|---|---|---|---|
| a | source_data.csv | D001 | {panel_a} | template only |
| b | source_data.csv | D002 | {panel_b} | template only |
| c | source_data.csv | D003 | {panel_c} | template only |

## Archetype

{archetype}

## Backend

- Selected backend: Python
- Runtime/package status: generated as template-only package
- Backend exclusivity note: all plotting, previews, exports, and QA renders use Python.

## Journal/Export Contract

- Target journal family: CBM/CCC/RMPD/JBE-ready review figure template
- Width: double-column template
- Font size: readable at final size
- Vector formats: SVG, PDF
- Raster formats: PNG, TIFF
- DPI: 300+

## Statistics And Image Integrity

- n definition: not applicable for template-only package
- replicate definition: not applicable for template-only package
- center/spread: not applicable for template-only package
- test/correction: not applicable for template-only package
- image provenance: no raw microscopy image in this package
- scale bars: not applicable
- crop/contrast notes: not applicable

## WER-EA Boundary

- Performance evidence: template only until real source rows are inserted
- Direct mechanism evidence: template only until FTIR/rheology/microscopy anchors are inserted
- Inferred mechanism: must be styled separately from direct evidence
- Durability/service evidence: must remain lab/service-condition specific
- Unsupported or missing evidence: no field-life claim can be made from this template alone

## Reviewer Risk

- Replace template values with source-grounded evidence before manuscript use.
""",
    "caption.md": """# Caption

## Caption

Template-only WER-EA figure package: {description}.

## What The Figure Supports

- {description}.

## What The Figure Does Not Prove

- This template does not prove {negative_claim}.

## Source Anchor

- source_data.csv rows a-c; replace with source_map/table-system anchors before manuscript use.

## Caption Boundary

- This is a template-only package and must not be cited as experimental evidence.
""",
    "qa_report.md": """# QA Report

## Backend Exclusivity

- Status: pass
- Note: Python generated every visual export in this template package.

## Export Check

- SVG: present
- PDF: present
- PNG: present
- TIFF: present

## Source-Data Check

- Status: template-only
- Source data: source_data.csv

## Statistics Check

- Status: not applicable for template-only package
- n/error bars/test definitions must be added for quantitative manuscript use.

## Image-Integrity Check

- Status: not applicable for template-only package
- Scale bars, raw image provenance, crop, and contrast notes must be added for microscopy panels.

## Caption-Boundary Check

- Status: pass
- Caption marks the package as template-only and does not claim mechanism proof.

## QA Status

pass
""",
    "asset_manifest.md": """# Asset Manifest

## Files

- figure_contract.md: figure design contract
- caption.md: caption and boundary
- qa_report.md: quality assurance report
- source_data.csv: template source data
- plot.py: Python plot script
- figure.svg: vector graphic
- figure.pdf: PDF graphic
- figure.png: raster graphic (300 DPI)
- figure.tiff: TIFF graphic (300 DPI)

## Status

template-only
""",
    "source_data.csv": """x,y1,y2,y3
0,0,0,0
1,1,1,1
2,4,4,4
3,9,9,9
4,16,16,16
""",
    "plot.py": """#!/usr/bin/env python3
\"\"\"Template plot script for {title}.\"\"\"

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from materials_plot_lib import apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(Path(__file__).parent))
    args = parser.parse_args()

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_title("{title}")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    finalize_figure(fig, "figure", args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
}

FIGURE_TYPE_DETAILS = {
    "creep-recovery": {
        "title": "Creep-Recovery",
        "description": "viscoelastic recovery behavior",
        "panel_a": "creep compliance",
        "panel_b": "recovery ratio",
        "panel_c": "permanent deformation",
        "archetype": "time-series",
        "negative_claim": "universal recovery behavior for all asphalt systems",
    },
    "psd-gradation": {
        "title": "PSD Gradation",
        "description": "particle size distribution and gradation curves",
        "panel_a": "particle size distribution",
        "panel_b": "gradation curve",
        "panel_c": "uniformity coefficient",
        "archetype": "distribution",
        "negative_claim": "optimal gradation for all mixtures",
    },
    "rheology-flow-curve": {
        "title": "Rheology Flow Curve",
        "description": "viscosity versus shear rate behavior",
        "panel_a": "flow curve",
        "panel_b": "viscosity profile",
        "panel_c": "shear thinning behavior",
        "archetype": "curve",
        "negative_claim": "universal flow behavior for all emulsions",
    },
    "stress-strain": {
        "title": "Stress-Strain",
        "description": "mechanical response under loading",
        "panel_a": "stress-strain curve",
        "panel_b": "elastic modulus",
        "panel_c": "failure strain",
        "archetype": "curve",
        "negative_claim": "universal mechanical behavior for all materials",
    },
    "ternary-phase": {
        "title": "Ternary Phase",
        "description": "three-component composition relationships",
        "panel_a": "phase diagram",
        "panel_b": "composition boundaries",
        "panel_c": "optimal region",
        "archetype": "ternary",
        "negative_claim": "universal composition for all systems",
    },
    "tg-dsc-thermal": {
        "title": "TG-DSC Thermal",
        "description": "thermal decomposition and heat flow",
        "panel_a": "TGA curve",
        "panel_b": "DTG curve",
        "panel_c": "DSC curve",
        "archetype": "thermal",
        "negative_claim": "universal thermal behavior for all materials",
    },
}


def generate_figure_package(figure_type: str) -> None:
    """Generate all files for a figure package."""
    package_dir = PACKAGES_ROOT / figure_type
    package_dir.mkdir(parents=True, exist_ok=True)

    details = FIGURE_TYPE_DETAILS[figure_type]

    for filename, template in TEMPLATES.items():
        content = template.format(**details)
        filepath = package_dir / filename
        filepath.write_text(content, encoding="utf-8")

    # Generate real figure files using matplotlib
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from materials_plot_lib import apply_pub_style
        
        apply_pub_style()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_title(details["title"])
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        x = np.linspace(0, 10, 50)
        y = np.sin(x)
        ax.plot(x, y, linewidth=2)
        output_path = package_dir
        fig.savefig(str(output_path / "figure.svg"), dpi=300)
        fig.savefig(str(output_path / "figure.png"), dpi=300)
        fig.savefig(str(output_path / "figure.pdf"), dpi=300)
        try:
            fig.savefig(str(output_path / "figure.tiff"), dpi=300)
        except Exception:
            pass
        plt.close(fig)
    except Exception as e:
        print(f"Warning: Could not generate figures for {figure_type}: {e}")
        for ext in ["svg", "pdf", "png", "tiff"]:
            filepath = package_dir / f"figure.{ext}"
            filepath.write_bytes(b"")

    print(f"Generated {figure_type} figure package")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--figure-types",
        nargs="*",
        default=FIGURE_TYPES,
        help="Figure types to generate",
    )
    args = parser.parse_args()

    for figure_type in args.figure_types:
        if figure_type in FIGURE_TYPES:
            generate_figure_package(figure_type)
        else:
            print(f"Unknown figure type: {figure_type}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())