---
name: civil-materials-citation
version: "1.1.0"
stability: stable
description: Use when searching, screening, organizing, or mapping literature and citations for civil engineering and construction materials manuscripts.
---

# Civil Materials Citation

Build source-grounded literature search plans and claim-citation maps for civil materials manuscripts.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `task`, `journal_family`, and `material_domain`.
3. Load only the matching fragment files.
4. Produce: search strategy, citation matrix, claim-source map, reference gap audit, or journal-specific source plan.
5. Do not invent papers, DOIs, impact factors, journal rules, or citation counts.

## Gates

- Prefer primary research and authoritative review articles over generic web summaries.
- Separate mechanism citations from performance citations.
