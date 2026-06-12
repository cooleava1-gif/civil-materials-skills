---
name: materials-pptx
version: "1.0.0"
stability: stable
description: Use when generating or converting real PowerPoint .pptx slide decks for civil engineering and construction materials research.
---

# Materials Science PPTX

Generate real `.pptx` decks for materials research, not only slide outlines.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `deck_type`, `material_domain`, `source_type`, and `template`.
3. Load only the matching fragments.
4. Build a slide plan first unless the user already provided one.
5. Use `scripts/build_materials_pptx.py` for one-click `.pptx` generation.

## Gates

- Keep claims tied to figures, tests, or source papers.
- One main message per slide.
- Use Chinese slide titles by default, English only when requested.
- Do not crop away data labels, axes, legends, or scale bars.
- Separate measured results from inferred mechanisms.
