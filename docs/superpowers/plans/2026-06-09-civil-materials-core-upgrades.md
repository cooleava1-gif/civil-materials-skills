# Civil Materials Core Upgrades Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `civil-materials-reader`, `civil-materials-figure`, and `civil-materials-citation` into a stronger evidence-to-review pipeline for WER-EA and broader civil-materials manuscripts.

**Architecture:** Keep each skill self-contained and router-driven. Add deeper workflow references, templates, and tests inside each skill folder, then mirror root skill changes into `plugins/civil-materials-skills/skills/<skill>/`. Avoid large shared refactors; only update shared docs or release checks when a new artifact must be validated.

**Tech Stack:** Codex skills (`SKILL.md`, `manifest.yaml`, `agents/openai.yaml`), Markdown references/templates, Python scripts and `unittest`, local release gate `python scripts\run_release_checks.py --json`.

---

## Global Rules For All Workers

- Work from the repository root on branch `codex/civil-materials-core-upgrades`.
- Do not push to GitHub.
- Do not add generated sample outputs under `outputs/`; `outputs/wer-ea-30-reading-sample/` must remain ignored and untracked.
- Do not revert unrelated user or other-worker changes.
- Keep root skill files and plugin mirror files byte-identical for your owned skill.
- Use ASCII for new files unless the existing file already uses Chinese intentionally. If adding Chinese trigger text, verify UTF-8 content and avoid mojibake.
- Prefer adding focused references/templates/tests over bloating `SKILL.md`.
- Run targeted tests for your skill and report exact commands and results.

## Task 1: Upgrade `civil-materials-reader`

**Worker ownership:** only edit:

- `skills/civil-materials-reader/**`
- `plugins/civil-materials-skills/skills/civil-materials-reader/**`
- reader-specific entries in `scripts/run_release_checks.py`, if needed for validation

**Purpose:** Turn reader into a stricter full-paper evidence extractor that can hand off cleanly to citation and figure workflows.

**Desired capabilities:**

1. A source-map-first workflow for PDF, DOI/HTML, and pasted text.
2. A durable reader output contract with required files, source anchors, confidence labels, and missing-evidence flags.
3. A WER-EA mini-review extraction route that produces mechanism, dosage, durability, citation-role, and figure-handoff rows.
4. A stronger visual-asset linkage protocol: each figure/table card should record source page, crop status, interpretation boundary, and whether the asset can support a review figure.
5. A bridge to `civil-materials-citation`: each borrowable claim must include citation role and evidence type.
6. A bridge to `civil-materials-figure`: each figure-worthy row must include figure archetype and reviewer-risk boundary.
7. Tests that catch mojibake in reader triggers and verify the new handoff templates/references exist and contain required fields.

**Expected files to add or modify:**

- Modify `skills/civil-materials-reader/SKILL.md` to stay short and point to new workflow references.
- Modify `skills/civil-materials-reader/manifest.yaml` to add or clean axes for `source_type`, `output_type`, and a new handoff route if needed.
- Add `skills/civil-materials-reader/references/evidence-to-review-handoff.md`.
- Add or modify reader templates such as:
  - `assets/templates/citation-handoff-template.csv`
  - `assets/templates/figure-handoff-template.csv`
  - `assets/templates/source-anchor-checklist.md`
- Add tests in `skills/civil-materials-reader/tests/test_reader_handoff.py`.
- Mirror all changed reader files to `plugins/civil-materials-skills/skills/civil-materials-reader/`.

**Implementation steps:**

- [ ] Inspect existing reader references and templates, especially `fulltext-figure-anchored-reading.md`, `wer-ea-intensive-reading-package.md`, and `table-system.md`.
- [ ] Add a reader handoff reference that defines required columns for citation and figure handoffs:
  - `claim_id`
  - `source_anchor`
  - `source_location`
  - `original_excerpt`
  - `measured_evidence`
  - `inferred_mechanism`
  - `boundary_or_missing_test`
  - `citation_role`
  - `evidence_type`
  - `figure_archetype`
  - `reviewer_risk`
  - `handoff_target`
- [ ] Add templates for citation and figure handoff CSVs using those fields.
- [ ] Update `manifest.yaml` so relevant triggers route WER-EA review extraction, citation handoff, and figure handoff to the new reference.
- [ ] Update `SKILL.md` so the default reader package explicitly includes citation and figure handoff files when full-text or WER-EA review work is requested.
- [ ] Add tests verifying the new reference and templates exist, include required fields, and avoid known mojibake marker strings in triggers.
- [ ] Mirror root reader changes into the plugin wrapper.
- [ ] Run:

```powershell
python -m unittest discover -s skills\civil-materials-reader\tests -v
```

**Acceptance criteria:**

- Reader can produce a traceable paper-to-review package, not just notes.
- Citation and figure handoff fields are explicitly named and test-covered.
- Root and plugin reader copies match.
- Targeted reader tests pass.

## Task 2: Upgrade `civil-materials-figure`

**Worker ownership:** only edit:

- `skills/civil-materials-figure/**`
- `plugins/civil-materials-skills/skills/civil-materials-figure/**`
- figure-specific entries in `scripts/run_release_checks.py`, if needed for validation

**Purpose:** Turn figure into a more reliable review-figure and journal-package generator that consumes reader/citation handoffs.

**Desired capabilities:**

1. A review-figure intake protocol that accepts reader handoff tables and citation matrices.
2. A figure contract that distinguishes measured evidence, inferred mechanism, and speculative schematic elements.
3. Stronger WER-EA review figure routes:
  - mechanism map
  - evidence heatmap
  - dosage window
  - test-method comparison
  - performance-mechanism boundary
  - literature-screening flow
4. A stricter QA checklist for figure packages:
  - source-data traceability
  - caption claim strength
  - uncertainty/absence markers
  - journal export formats
  - visual asset manifest completeness
5. Tests that validate the new intake protocol and QA fields.

**Expected files to add or modify:**

- Modify `skills/civil-materials-figure/SKILL.md` only to route to new references.
- Modify `skills/civil-materials-figure/manifest.yaml` to add a `handoff_intake` or equivalent route.
- Add `skills/civil-materials-figure/references/review-figure-intake.md`.
- Add `skills/civil-materials-figure/assets/templates/review-figure-intake-template.csv`.
- Modify `references/wer-ea-review-figure-contract.md` if needed to include measured/inferred/speculative tiers.
- Modify `references/figure-qa-contract.md` or package templates if needed.
- Add tests in `skills/civil-materials-figure/tests/test_review_figure_intake.py`.
- Mirror all changed figure files to `plugins/civil-materials-skills/skills/civil-materials-figure/`.

**Implementation steps:**

- [ ] Inspect current figure package protocol, WER-EA contract, QA contract, and audit script.
- [ ] Add a review-figure intake reference that maps reader/citation handoff rows into panel decisions:
  - `claim_id`
  - `source_anchor`
  - `citation_key_or_doi`
  - `evidence_layer`
  - `certainty_tier`
  - `panel_role`
  - `visual_encoding`
  - `caption_boundary`
  - `missing_evidence_marker`
  - `reviewer_risk`
- [ ] Add a CSV template with those fields.
- [ ] Update WER-EA figure contract to require evidence tiers for mechanism maps and heatmaps.
- [ ] Update QA contract so final package audits check source-data and caption-boundary fields.
- [ ] Update manifest triggers for reader/citation handoff, evidence heatmap, mechanism map, and review figure intake.
- [ ] Add tests verifying required intake and QA fields.
- [ ] Mirror root figure changes into the plugin wrapper.
- [ ] Run:

```powershell
python -m unittest discover -s skills\civil-materials-figure\tests -v
```

**Acceptance criteria:**

- Figure workflow can consume reader/citation handoff tables without inventing evidence.
- WER-EA review figures visibly separate measured, inferred, and missing evidence.
- Root and plugin figure copies match.
- Targeted figure tests pass.

## Task 3: Upgrade `civil-materials-citation`

**Worker ownership:** only edit:

- `skills/civil-materials-citation/**`
- `plugins/civil-materials-skills/skills/civil-materials-citation/**`
- citation-specific entries in `scripts/run_release_checks.py`, if needed for validation

**Purpose:** Turn citation into a stronger claim-source alignment and literature-screening engine for civil materials, with WER-EA-specific evidence layers.

**Desired capabilities:**

1. A clearer evidence-layer taxonomy for WER-EA:
  - material formulation
  - emulsion stability
  - bonding/interface performance
  - rheology
  - curing/demulsification
  - microstructure/chemistry
  - moisture/aging durability
  - service or field relevance
  - review/background
2. A screening protocol that marks whether a source is primary experimental evidence, review evidence, method evidence, standard/specification, or weak background.
3. Citation matrix columns aligned with reader and figure handoffs.
4. Stronger MCP service/domain tests for evidence classification and export schema.
5. Better reference-gap audit guidance for reviewer-safe source packages.

**Expected files to add or modify:**

- Modify `skills/civil-materials-citation/SKILL.md` to route to new references without becoming long.
- Modify `skills/civil-materials-citation/manifest.yaml` to add WER-EA screening/reference-gap triggers.
- Modify `references/claim-citation-mapping.md` and `references/reference-gap-audit.md`.
- Add `references/wer-ea-screening-and-source-quality.md`.
- Modify `assets/templates/citation-matrix-template.csv` and maybe `scripts/build_citation_matrix.py` if schema support is needed.
- Modify MCP domain tests and classifier/query code only if required:
  - `mcp/academic_search/domain/classifier.py`
  - `mcp/academic_search/domain/queries.py`
  - `mcp/academic_search/tests/test_domain.py`
  - `mcp/academic_search/tests/test_service.py`
- Mirror all changed citation files to `plugins/civil-materials-skills/skills/civil-materials-citation/`.

**Implementation steps:**

- [ ] Inspect current citation mapping, reference-gap audit, templates, and MCP domain classifiers.
- [ ] Add WER-EA screening/source-quality reference defining source roles, evidence layers, and exclusion flags.
- [ ] Extend the citation matrix schema to include:
  - `claim_id`
  - `evidence_layer`
  - `source_role`
  - `source_quality`
  - `mechanism_directness`
  - `durability_relevance`
  - `service_relevance`
  - `reader_anchor`
  - `figure_handoff`
  - `reviewer_risk`
- [ ] Update scripts/tests so matrix generation or schema validation understands the new columns.
- [ ] Strengthen classifier/query tests for WER-EA evidence layers and short-term false positives.
- [ ] Update manifest triggers for WER-EA screening, source quality, and reviewer-safe citation package.
- [ ] Mirror root citation changes into the plugin wrapper.
- [ ] Run:

```powershell
python -m unittest discover -s skills\civil-materials-citation\mcp\academic_search\tests -v
```

**Acceptance criteria:**

- Citation workflow produces claim-source maps that can feed reader and figure handoffs.
- WER-EA evidence layers are explicit and test-covered.
- Export schema remains CSV-safe and compatible with release checks.
- Root and plugin citation copies match.
- Targeted citation tests pass.

## Task 4: Integration And Final Review

**Controller ownership:** final integration should be performed by the main agent after workers return.

**Integration steps:**

- [ ] Review each worker's changed files and summaries.
- [ ] Resolve any root/plugin mirror drift.
- [ ] Check that reader, figure, and citation use consistent field names:
  - `claim_id`
  - `source_anchor`
  - `evidence_layer`
  - `citation_role` / `source_role`
  - `figure_handoff`
  - `reviewer_risk`
- [ ] Update `README.md` and `docs/skills-index.md` only if the new capability changes public routing.
- [ ] Update `scripts/run_release_checks.py` only if new required artifacts should become release-gated.
- [ ] Run targeted tests for all three modules.
- [ ] Run final release gate:

```powershell
python scripts\run_release_checks.py --json
```

**Final acceptance criteria:**

- All three targeted test suites pass.
- Release gate reports top-level `"status": "pass"`.
- No `outputs/wer-ea-30-reading-sample/` files are staged or tracked.
- No new mojibake appears in reader/figure/citation manifests or templates.
- Final response summarizes what changed, what was tested, and remaining upgrade ideas.
