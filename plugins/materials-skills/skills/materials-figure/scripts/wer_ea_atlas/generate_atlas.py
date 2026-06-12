#!/usr/bin/env python3
"""Generate WER-EA figure atlas SVG/PNG template assets."""

from __future__ import annotations

import argparse
import csv
import json
import struct
import zlib
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_ROOT.parents[1]
ATLAS_ROOT = SKILL_ROOT / "assets" / "wer-ea-atlas"
SPEC_PATH = ATLAS_ROOT / "asset-specs.csv"
CERTAINTY_TIERS = ("measured", "inferred", "speculative", "missing")


def slug_to_filename(asset_id: str) -> str:
    return asset_id.replace("-", "_")


def load_specs(path: Path = SPEC_PATH) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def svg_for_spec(spec: dict[str, str]) -> str:
    title = spec["family"].replace("-", " ").title()
    use = spec["review_use"]
    boundary = spec["claim_boundary"]
    evidence = spec["required_evidence"]
    panels = [part.strip() for part in spec["panel_structure"].split("|")]
    colors = {
        "measured": "#2f6f4e",
        "inferred": "#3e7cb1",
        "speculative": "#9a6b00",
        "missing": "#777777",
    }

    panel_shapes = []
    x = 42
    for index, panel in enumerate(panels[:6]):
        tier = CERTAINTY_TIERS[index % len(CERTAINTY_TIERS)]
        fill = colors[tier]
        dash = "6 4" if tier == "inferred" else "2 4" if tier == "speculative" else ""
        opacity = "0.25" if tier == "missing" else "0.92"
        panel_shapes.append(
            f'<rect x="{x}" y="108" width="112" height="58" rx="6" fill="{fill}" '
            f'fill-opacity="{opacity}" stroke="#223" stroke-width="1.2" stroke-dasharray="{dash}"/>'
        )
        panel_shapes.append(
            f'<text x="{x + 56}" y="137" font-size="10" text-anchor="middle" fill="#111">{_xml(panel[:18])}</text>'
        )
        panel_shapes.append(
            f'<text x="{x + 56}" y="152" font-size="8" text-anchor="middle" fill="#111">{tier}</text>'
        )
        x += 124

    legend = []
    lx = 48
    for tier in CERTAINTY_TIERS:
        legend.append(f'<rect x="{lx}" y="214" width="20" height="10" fill="{colors[tier]}" opacity="0.85"/>')
        legend.append(f'<text x="{lx + 26}" y="223" font-size="10" fill="#222">{tier}</text>')
        lx += 128

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="300" viewBox="0 0 820 300">
  <rect width="820" height="300" fill="#f8f9f6"/>
  <text x="40" y="38" font-size="22" font-family="Arial" fill="#1f2a2e">{_xml(title)}</text>
  <text x="40" y="62" font-size="12" font-family="Arial" fill="#40505a">WER-EA figure atlas - template only</text>
  <text x="40" y="84" font-size="11" font-family="Arial" fill="#40505a">Use: {_xml(use)}</text>
  {''.join(panel_shapes)}
  <text x="40" y="196" font-size="11" font-family="Arial" fill="#222">Required evidence: {_xml(evidence[:110])}</text>
  {''.join(legend)}
  <text x="40" y="258" font-size="11" font-family="Arial" fill="#222">Claim boundary: {_xml(boundary[:118])}</text>
</svg>
'''


def write_png(path: Path, *, width: int = 320, height: int = 180) -> None:
    """Write a simple valid RGB PNG using only the standard library."""
    raw_rows = []
    for y in range(height):
        shade = 242 - (y % 12)
        row = bytes([0]) + bytes([shade, 246, 238]) * width
        raw_rows.append(row)
    raw = b"".join(raw_rows)

    def chunk(kind: bytes, data: bytes) -> bytes:
        payload = kind + data
        return struct.pack(">I", len(data)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, level=6))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def generate_atlas(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for spec in load_specs():
        stem = slug_to_filename(spec["asset_id"])
        svg_path = output_dir / f"{stem}.svg"
        png_path = output_dir / f"{stem}.png"
        svg_path.write_text(svg_for_spec(spec), encoding="utf-8")
        write_png(png_path)
        generated.append(
            {
                "asset_id": spec["asset_id"],
                "family": spec["family"],
                "svg": str(svg_path),
                "png": str(png_path),
                "caption_boundary": spec["claim_boundary"],
            }
        )
    return {"status": "pass", "generated": generated, "warnings": []}


def _xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = generate_atlas(Path(args.output_dir))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for row in report["generated"]:
            print(row["svg"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
