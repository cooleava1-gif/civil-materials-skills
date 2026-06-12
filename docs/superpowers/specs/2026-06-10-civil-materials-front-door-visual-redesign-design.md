# Materials Science Front-Door Visual Redesign

**Date:** 2026-06-10  
**Status:** approved for implementation in this session  
**Reference direction:** borrow the front-door visual language from `nature-skills` while keeping all surface evidence grounded in real materials outputs

## Problem

The current `showcase-proof` boards are better than flat placeholder cards, but they still read like clean contact sheets rather than a mature product front door. They prove that assets exist, yet they do not create the strong editorial rhythm, hierarchy, or narrative compression seen in `nature-skills`.

## Visual Goals

1. Replace symmetric screenshot boards with editorial multi-panel compositions.
2. Borrow the strongest `nature-skills` patterns:
   - `overview -> deviation -> relationship` narrative hierarchy
   - asymmetric panel sizing instead of equal-weight cards
   - dense atlas-like micro-panels that still preserve evidence boundaries
   - strong typography and panel tags that feel curated rather than templated
3. Keep every front-door surface grounded in real outputs from:
   - `outputs/wer-ea-30-reading-sample/.../assets/contact_sheet.png`
   - extracted paper figures and tables under each sample package
4. Make the new visual system testable and reproducible rather than hand-tuned.

## Non-Goals

- Do not turn template atlas assets into fake evidence.
- Do not invent manuscript results or synthetic charts.
- Do not ship a manually edited one-off board that cannot be regenerated.

## Proposed System

## 1. Editorial Board Engine

Upgrade `skills/materials-figure/scripts/build_showcase_proof_assets.py` from a simple card renderer into a small board engine with:

- multiple layout families for different narrative shapes
- relative crop boxes so each panel can focus on the signal-rich region of a source image
- section tags and panel letters
- a mixed serif/sans editorial typography stack
- source provenance labels and short evidence-role notes

## 2. Nature-Inspired Narrative Layers

Each board should explicitly encode three layers:

- `overview`: the large panel that establishes the study or package
- `deviation`: mid-size panels that surface the most informative contrast
- `relationship`: smaller panels or notes that explain how the visual pieces connect

This should be visible in layout, not just text.

## 3. Content Strategy Per Board

Keep the existing four filenames, but redesign their structure:

- `reader_package_proof_wall.png`
  - three package overview surfaces plus inset crops and package stats
- `wer_ea_figure_proof_board.png`
  - one dominant mechanism overview, then rheology and FTIR relationship panels
- `sbr_wer_performance_proof_board.png`
  - one dominant performance/behavior panel, then FTIR, SEM, and adhesion evidence
- `interlayer_fatigue_proof_board.png`
  - one dominant fatigue-results panel, then apparatus and table evidence

## 4. Testable Metadata

Generate `showcase_manifest.json` alongside the PNG boards so tests and docs can verify:

- board ids and output filenames
- narrative roles
- source assets used by each tile
- crop metadata

This turns the front-door visual layer into a reproducible product surface instead of opaque binaries.

## 5. Docs Refresh

Update `README.md` and `docs/gallery/README.md` so the front door explains that these are editorial proof boards built from real reader-package outputs and extracted paper figures, not style-only references.

## Validation

- extend `skills/materials-figure/tests/test_figure_gallery.py`
- confirm regenerated PNGs still carry visual signal
- verify `showcase_manifest.json` exists and records narrative metadata
- run skill tests plus repo release checks

## Risks

- Over-stylizing could make the boards look less evidence-grounded.
- Over-cropping could hide provenance context.
- Reusing existing filenames means the new boards must be clearly better without breaking docs paths.

## Decision

Proceed with a full redesign of the `showcase-proof` generator and refresh the board assets in place.
