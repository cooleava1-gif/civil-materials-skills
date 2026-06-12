# Materials Science Front-Door Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the `showcase-proof` front-door visuals so they feel closer to `nature-skills` while remaining grounded in real materials evidence outputs.

**Architecture:** Keep the existing showcase PNG filenames, but replace the current equal-card renderer with an editorial board engine that supports crop metadata, asymmetric layouts, and manifest generation. Tie the redesign to tests so the new surface is reproducible and mirror-safe.

**Tech Stack:** Python, Pillow, unittest, Markdown docs

---

### Task 1: Lock the new contract in tests

**Files:**
- Modify: `skills/materials-figure/tests/test_figure_gallery.py`
- Modify: `plugins/materials-skills/skills/materials-figure/tests/test_figure_gallery.py`

- [ ] Add failing assertions for `showcase_manifest.json`.
- [ ] Add failing assertions that each board entry records narrative roles and tile metadata.
- [ ] Run the targeted test file and confirm failure before implementation.

### Task 2: Upgrade the showcase proof builder

**Files:**
- Modify: `skills/materials-figure/scripts/build_showcase_proof_assets.py`
- Modify: `plugins/materials-skills/skills/materials-figure/scripts/build_showcase_proof_assets.py`

- [ ] Add crop-aware tile metadata and richer board definitions.
- [ ] Replace equal-card rendering with editorial asymmetric compositions.
- [ ] Emit `showcase_manifest.json` together with the PNG outputs.
- [ ] Re-run the targeted tests and confirm they pass.

### Task 3: Refresh generated assets and front-door docs

**Files:**
- Modify: `README.md`
- Modify: `docs/gallery/README.md`
- Refresh: `skills/materials-figure/assets/showcase-proof/*`
- Refresh: `plugins/materials-skills/skills/materials-figure/assets/showcase-proof/*`

- [ ] Regenerate the four PNG boards and the manifest in source and plugin mirror.
- [ ] Update docs copy so the new editorial proof layer is explained accurately.
- [ ] Run repo verification commands and confirm the release surface still passes.

### Task 4: Commit the validated round

**Files:**
- Stage only the files touched for this redesign

- [ ] Review `git status` to avoid unrelated dirty files.
- [ ] Create one commit for the redesign after tests and release checks pass.
