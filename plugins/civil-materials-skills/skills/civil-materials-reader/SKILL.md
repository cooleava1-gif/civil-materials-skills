---
name: civil-materials-reader
version: "1.2.0"
stability: stable
description: Use when reading, translating, extracting, auditing, or structuring civil engineering and construction materials papers, especially for source-grounded notes, evidence-chain reading, claim-evidence-mechanism matrices, Chinese-English paper notes, figure/table-aware reading, literature matrices, journal-club preparation, asphalt pavement materials, cement/concrete, durability, sustainability, and waterborne epoxy modified emulsified asphalt.
---

# Civil Materials Reader — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core principles, the reading workflow, the output contract, and per-source-format extraction guidance).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's source format and loads only the fragments needed for the current job.

Do not try to apply the reading logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the `source_format` axis, the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load`. These hold the core principles, the reading workflow, and the output contract that apply to every reading job.

### 2. Detect the source format

Decide the `source_format` value using the manifest's `detect:` hint and the user's input:

- `pdf-text` — selectable-text PDF. Default for PDF files.
- `scanned-pdf` — image-only or OCR-required PDF.
- `doi-arxiv` — a bare DOI or arXiv link that must be resolved first.
- `html` — publisher or preprint HTML page.
- `pasted-text` — pasted prose or notes with no retrievable original layout.

State the detected value in one short line to the user before processing, so they can correct you cheaply. A source may map to more than one value (for example a DOI that resolves to a PDF); load the resolution fragment first, then the fragment for the resolved artifact.

### 3. Load the matching fragment(s)

Read the file mapped for the detected `source_format`. Do **not** read every fragment in `static/`. Load only what step 2 selected.

### 4. Build the reader using the loaded material

Apply the loaded fragments in this priority order:

1. Core principles — bilingual reader by default, translate for meaning, never degrade to a summary, copyright caution.
2. Source-format fragment — how to extract text, figures, and tables for this input.
3. Reading workflow — the seven-step process for civil materials papers.
4. Output contract — required files and the pre-response verification checklist.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand:

- full-text figure-anchored reading → `references/fulltext-figure-anchored-reading.md`.
- evidence chain audit → `references/evidence-chain-audit.md`.
- literature matrix → `references/literature-matrix.md`.
- microstructure interpretation (SEM/AFM/DSC/TG) → `references/microstructure-interpretation.md`.
- PDF visual asset extraction → `references/pdf-visual-asset-extraction.md`.
- table system → `references/table-system.md`.
- journal club reading → `references/journal-club-reading.md`.
- WER-EA intensive reading package → `references/wer-ea-intensive-reading-package.md`.

## Protocol

1. Follow the routing protocol above.
2. Detect the `source_format` and `output_type`.
3. Load only the matching fragments and references.
4. Produce a Markdown reader, matrix, or evidence-chain audit that preserves the paper's evidence chain.
5. Keep all numbers, figures, tables, mechanisms, and limitations tied to the source.

## Default Output

Use `assets/templates/literature-reading-template.md` as the base structure unless the user requests another format.

For full-text intensive reading, PDF/text-to-`paper.md`, figure/table anchoring, source mapping, or WER-EA mini-review extraction, load `references/fulltext-figure-anchored-reading.md` and `references/evidence-to-review-handoff.md`, then use:

- `assets/templates/paper-md-template.md`,
- `assets/templates/source-map-template.json`,
- `assets/templates/source-anchor-checklist.md`,
- `assets/templates/translation-notes-template.md`,
- `assets/templates/figure-table-card-template.md`,
- `assets/templates/mechanism-evidence-table-template.md`,
- `assets/templates/dosage-window-table-template.md`,
- `assets/templates/citation-handoff-template.csv`,
- `assets/templates/figure-handoff-template.csv`,
- `assets/templates/review-handoff-template.md`,
- `assets/templates/obsidian-note-template.md`.

For WER-EA 30-paper intensive-reading packages, also load `references/wer-ea-intensive-reading-package.md`. Produce a linked package with:

- `paper.md`,
- `source_map.json`,
- `translation_notes.md`,
- `figure_table_cards.md`,
- `mechanism_evidence_table.md`,
- `dosage_window_table.md`,
- `citation_handoff.csv`,
- `figure_handoff.csv`,
- `source_anchor_checklist.md`,
- `review_handoff.md`,
- `obsidian_note.md`,
- `visual_asset_spec.json`,
- `assets/`.

When a source PDF is available and figure/table visual verification is requested, also load `references/pdf-visual-asset-extraction.md` and use `scripts/extract_pdf_visual_assets.py` to create rendered pages, cropped assets, `asset_manifest.md`, `visual_asset_report.json`, and `contact_sheet.png`.

The output should include:

- paper identity,
- research question,
- material system,
- experiment matrix,
- figure/table evidence map,
- mechanism chain,
- limitations,
- what the user can borrow for their own topic.
- claim-evidence-mechanism-boundary audit when the paper will inform a manuscript or review.
- paper.md, source_map.json, source_anchor_checklist.md, translation_notes.md, assets/, visual_asset_spec.json, asset_manifest.md, contact_sheet.png, original excerpt, Chinese understanding, figure card, table card, mechanism_evidence_table.md, dosage_window_table.md, citation_handoff.csv, figure_handoff.csv, review_handoff.md, obsidian_note.md, and borrowable writing when full-text anchoring is requested.

## Civil Materials Reading Rules

- Extract test conditions and standards when present.
- Do not convert figure captions into unsupported conclusions.
- Separate measured results from inferred mechanisms.
- For asphalt/pavement papers, always capture binder/emulsion, interface, mixture, and service-condition evidence separately.
- For cement/concrete papers, always capture fresh properties, strength, durability, hydration/microstructure, and sustainability boundary separately.
- For review writing, convert each borrowable idea into: claim -> evidence -> mechanism -> boundary -> citation role.
- Flag reviewer risks when a conclusion is stronger than the measurements.
- Use `references/microstructure-interpretation.md` when interpreting SEM, fluorescence microscopy, AFM, DSC/TG, or morphology figures.

If the user asks for a PPT after reading, hand off to `civil-materials-paper2ppt`. If the user asks for polished English after reading, hand off to `civil-materials-polishing`.

For literature tables, mechanism tables, method comparison tables, performance tables, durability tables, or journal positioning tables, load `references/table-system.md` and use `assets/templates/table-system-template.md`.

Use `examples/waterborne-epoxy-evidence-chain-example.md` as a concrete model for evidence-chain reading. Use `tests/pressure-tests/overclaim-from-figure-caption.md` to check that figure captions are not converted into unsupported conclusions.

## WER-EA mini-review reading protocol

Use this protocol for WER-EA, waterborne epoxy resin modified emulsified asphalt, or small-review preparation tasks.

- Literature screening: tag each source by material system, WER dosage, curing agent, emulsifier, asphalt/emulsion type, substrate/interface, and whether it is experimental, review, field, or method evidence.
- Mechanism evidence chain: extract claim -> evidence -> mechanism -> boundary rows for bonding strength, rheology, storage stability, demulsification/curing behavior, FTIR, fluorescence microscopy, SEM/AFM, thermal analysis, moisture/aging durability, and service-condition evidence.
- Review outline handoff: summarize each paper's borrowable role as background, mechanism support, performance comparison, method reference, durability gap, or reviewer-risk caution.
- Citation handoff: write `citation_handoff.csv` rows with source anchors, citation role, evidence type, confidence label, and missing-evidence flags for `civil-materials-citation`.
- Figure planning handoff: write `figure_handoff.csv` rows with source anchors, figure archetype, visual-asset status, reviewer-risk boundary, and review-figure support for `civil-materials-figure`.
- PDF visual asset handoff: when the PDF is available, render source pages, crop key figures/tables, record `visual_checked`, `asset_file`, `crop_status`, `defects`, and `qa_status`, and keep local PDF paths out of release artifacts.
- Submission route handoff: flag whether the paper supports pavement/asphalt journals, construction-materials journals, or only background context.
- Obsidian handoff: produce a three-layer `obsidian_note.md` with `1 快读判断`, `2 实验证据层`, `3 写作转化层`, and concept links centered on WER-EA knowledge nodes rather than paper-title chains.

Never treat performance improvement alone as proof of WER-EA mechanism. Keep direct evidence, inferred mechanism, and missing tests visibly separate.
