#!/usr/bin/env python3
"""Stress-strain curves for mechanical characterization."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_stress_strain


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("stress_strain.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    strain = column(rows, "strain_pct", as_float=True)
    stress = [
        column(rows, "stress_mpa_control", as_float=True),
        column(rows, "stress_mpa_modified", as_float=True),
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    make_stress_strain(
        ax, strain, stress, ["Control", "Modified"], PALETTE_CBM,
        failure_points={"×": (3.0, 47.5), "×": (2.5, 56.0)},
    )
    add_panel_label(ax, "(h)")
    fig.tight_layout()
    finalize_figure(fig, "stress_strain", args.output_dir)
    print_caption(
        "Stress-strain curves under uniaxial compression. "
        "Failure points are approximate; elastic modulus and Poisson ratio require strain gauge or extensometer data."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
