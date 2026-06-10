#!/usr/bin/env python3
"""Build real showcase proof boards from reader-package visual assets."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = SKILL_ROOT / "assets" / "showcase-proof"

CANVAS_SIZE = (1600, 1000)
MARGIN = 56
GAP = 24
CARD_RADIUS = 28

PALETTE = {
    "paper": "#F7F2E8",
    "card": "#FFFDFC",
    "line": "#DED3C2",
    "ink": "#1F2725",
    "muted": "#5D6764",
    "accent": "#8A623F",
    "shadow": "#E8DECF",
}


@dataclass(frozen=True)
class Tile:
    label: str
    source_note: str
    path: Path


@dataclass(frozen=True)
class Board:
    filename: str
    title: str
    subtitle: str
    footer: str
    layout: str
    tiles: tuple[Tile, ...]


BOARDS = (
    Board(
        filename="reader_package_proof_wall.png",
        title="Reader-Package Proof Wall",
        subtitle="Three real contact sheets captured from paper-derived reading packages",
        footer="These boards are built from actual rendered pages, cropped figures, and asset-manifest outputs.",
        layout="triptych",
        tiles=(
            Tile(
                label="015 curing-agent structure",
                source_note="contact sheet from WER-EA chemistry and morphology package",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "contact_sheet.png",
            ),
            Tile(
                label="016 SBR-WER waterproof binder",
                source_note="contact sheet from binder performance and adhesion package",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "contact_sheet.png",
            ),
            Tile(
                label="017 AC-PCC fatigue",
                source_note="contact sheet from interlayer fatigue and tack-coat package",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "contact_sheet.png",
            ),
        ),
    ),
    Board(
        filename="wer_ea_figure_proof_board.png",
        title="WER-EA Figure Proof Board",
        subtitle="Mechanism, rheology, and FTIR evidence pulled from a real review package",
        footer="This front-door board uses source-grounded visual crops, not atlas placeholders or template-only cards.",
        layout="featured",
        tiles=(
            Tile(
                label="Reaction and crosslinking schematic",
                source_note="f015-01_fig-1-2.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-01_fig-1-2.png",
            ),
            Tile(
                label="Dosage-temperature rheology comparison",
                source_note="f015-03_fig-8.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-03_fig-8.png",
            ),
            Tile(
                label="FTIR evidence panel",
                source_note="f015-08_fig-14.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "figures" / "f015-08_fig-14.png",
            ),
        ),
    ),
    Board(
        filename="sbr_wer_performance_proof_board.png",
        title="SBR-WER Performance Proof Board",
        subtitle="FTIR, morphology, adhesion, and low-temperature behavior from a waterproof binder study",
        footer="The goal is product proof through real content density, not abstract style cards with renamed headings.",
        layout="featured",
        tiles=(
            Tile(
                label="Low-temperature flexibility, viscosity, and comparison table",
                source_note="f016-05_fig-8-10-table-6.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "figures" / "f016-05_fig-8-10-table-6.png",
            ),
            Tile(
                label="FTIR and SEM evidence sheet",
                source_note="f016-03_fig-3-4.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "figures" / "f016-03_fig-3-4.png",
            ),
            Tile(
                label="Aggregate adhesion table with annotated specimen photos",
                source_note="t016-01_table-7.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "016-sbr-wer-waterproof-binder" / "assets" / "tables" / "t016-01_table-7.png",
            ),
        ),
    ),
    Board(
        filename="interlayer_fatigue_proof_board.png",
        title="Interlayer Fatigue Proof Board",
        subtitle="Method fixture, tack-coat fatigue charts, and data table in one reviewer-facing board",
        footer="This board shows why the gallery should surface real method and results evidence before any template-driven figure examples.",
        layout="featured",
        tiles=(
            Tile(
                label="Tack-coat fatigue result panels",
                source_note="f017-02_fig-8-tack-coat-fatigue-results.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "figures" / "f017-02_fig-8-tack-coat-fatigue-results.png",
            ),
            Tile(
                label="Inclined shear fatigue apparatus",
                source_note="f017-01_fig-4-5-inclined-shear-fatigue-method.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "figures" / "f017-01_fig-4-5-inclined-shear-fatigue-method.png",
            ),
            Tile(
                label="Stress-ratio fatigue life table",
                source_note="t017-01_table-8-tack-coat-fatigue-table.png",
                path=REPO_ROOT / "outputs" / "wer-ea-30-reading-sample" / "017-ac-pcc-inclined-shear-fatigue" / "assets" / "tables" / "t017-01_table-8-tack-coat-fatigue-table.png",
            ),
        ),
    ),
)


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = ["DejaVuSans-Bold.ttf", "arialbd.ttf"] if bold else ["DejaVuSans.ttf", "arial.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = load_font(42, bold=True)
SUBTITLE_FONT = load_font(20)
LABEL_FONT = load_font(22, bold=True)
NOTE_FONT = load_font(16)
FOOTER_FONT = load_font(18)


def fit_panel(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        return ImageOps.fit(rgb, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def draw_card(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    tile: Tile,
    box: tuple[int, int, int, int],
) -> None:
    x0, y0, x1, y1 = box
    shadow_offset = 8
    draw.rounded_rectangle(
        (x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset),
        radius=CARD_RADIUS,
        fill=PALETTE["shadow"],
    )
    draw.rounded_rectangle((x0, y0, x1, y1), radius=CARD_RADIUS, fill=PALETTE["card"], outline=PALETTE["line"], width=2)

    label_height = 88
    inset = 14
    content_w = (x1 - x0) - inset * 2
    content_h = (y1 - y0) - inset * 2 - label_height
    image = fit_panel(tile.path, (content_w, content_h))

    mask = rounded_mask((content_w, content_h), 20)
    image_pos = (x0 + inset, y0 + inset)
    canvas.paste(image, image_pos, mask)

    label_top = y0 + inset + content_h + 10
    draw.rounded_rectangle(
        (x0 + inset, label_top, x1 - inset, y1 - inset),
        radius=18,
        fill="#FCF8F1",
        outline=PALETTE["line"],
        width=1,
    )
    draw.text((x0 + inset + 18, label_top + 14), tile.label, fill=PALETTE["ink"], font=LABEL_FONT)
    draw.text((x0 + inset + 18, label_top + 48), tile.source_note, fill=PALETTE["muted"], font=NOTE_FONT)


def render_triptych(board: Board, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    available_width = CANVAS_SIZE[0] - MARGIN * 2 - GAP * 2
    card_width = available_width // 3
    card_height = 760
    top = 164
    for index, tile in enumerate(board.tiles):
        x0 = MARGIN + index * (card_width + GAP)
        draw_card(canvas, draw, tile, (x0, top, x0 + card_width, top + card_height))


def render_featured(board: Board, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    available_width = CANVAS_SIZE[0] - MARGIN * 2
    top = 164
    hero_height = 394
    hero_tile = board.tiles[0]
    draw_card(canvas, draw, hero_tile, (MARGIN, top, MARGIN + available_width, top + hero_height))

    secondary_width = (available_width - GAP) // 2
    secondary_height = 300
    second_top = top + hero_height + GAP
    for index, tile in enumerate(board.tiles[1:]):
        x0 = MARGIN + index * (secondary_width + GAP)
        draw_card(canvas, draw, tile, (x0, second_top, x0 + secondary_width, second_top + secondary_height))


def render_board(board: Board) -> Image.Image:
    canvas = Image.new("RGB", CANVAS_SIZE, PALETTE["paper"])
    draw = ImageDraw.Draw(canvas)

    draw.text((MARGIN, 34), board.title, fill=PALETTE["ink"], font=TITLE_FONT)
    draw.text((MARGIN, 90), board.subtitle, fill=PALETTE["muted"], font=SUBTITLE_FONT)
    draw.line((MARGIN, 132, CANVAS_SIZE[0] - MARGIN, 132), fill=PALETTE["line"], width=3)

    if board.layout == "triptych":
        render_triptych(board, canvas, draw)
    else:
        render_featured(board, canvas, draw)

    footer_top = CANVAS_SIZE[1] - 62
    draw.line((MARGIN, footer_top - 18, CANVAS_SIZE[0] - MARGIN, footer_top - 18), fill=PALETTE["line"], width=2)
    draw.text((MARGIN, footer_top), board.footer, fill=PALETTE["muted"], font=FOOTER_FONT)
    return canvas


def save_outputs(images: dict[str, Image.Image], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, image in images.items():
        image.save(output_dir / filename, format="PNG", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--mirror-output-dir", default="", help="Optional second output directory to mirror the same PNG files into.")
    args = parser.parse_args()

    generated = {}
    for board in BOARDS:
        for tile in board.tiles:
            if not tile.path.is_file():
                raise FileNotFoundError(f"Missing source image: {tile.path}")
        generated[board.filename] = render_board(board)

    output_dir = Path(args.output_dir)
    save_outputs(generated, output_dir)

    if args.mirror_output_dir:
        mirror_dir = Path(args.mirror_output_dir)
        save_outputs(generated, mirror_dir)

    for filename in generated:
        print(filename)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
