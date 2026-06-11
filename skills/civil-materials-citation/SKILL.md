---
name: civil-materials-citation
description: >-
  Search, screen, organize, and map literature and citations for civil engineering and construction materials manuscripts. Use when building citation matrices, reference gap audits, claim-source maps, or search strategies for CBM, CCC, JBE, RMPD, IJPE, asphalt pavement materials, emulsified asphalt, waterborne epoxy, cement/concrete, durability, and mechanisms.
  
  Also trigger on:
  - English: literature search, citation matrix, reference gap, claim-source map, search strategy, bibliographic management, DOI lookup
  - Chinese: 文献检索、引文矩阵、参考文献缺口、查收查引、文献管理、文献筛选、引文映射、文献搜索、论文检索
  
  Specializes in:
  - Multi-source academic search (OpenAlex, Semantic Scholar, CrossRef, PubMed)
  - Claim-citation mapping for evidence-grounded manuscripts
  - Reference gap identification and source quality assessment
version: 2.0.0
author: Civil Materials Team, refactored into static/dynamic layers
---


# Civil Materials Citation

Build source-grounded literature search plans and claim-citation maps for civil materials manuscripts.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `task`, `journal_family`, and `material_domain`.
3. Load only the matching reference files.
4. Produce one of these outputs: search strategy, citation matrix, claim-source map, reference gap audit, or journal-specific source plan.
5. Do not invent papers, DOIs, impact factors, journal rules, or citation counts. Use live search or user-provided sources for current facts.

## Default Output

Use `assets/templates/citation-matrix-template.csv` as the matrix schema and `assets/templates/search-plan-template.md` for search planning. For WER-EA screening, source-quality, or reviewer-safe package requests, also load `references/wer-ea-screening-and-source-quality.md`.

For each claim, include:

- exact claim or knowledge gap,
- search query and database route,
- target journal family,
- evidence type needed,
- candidate source status,
- manuscript location,
- risk if uncited or weakly cited.
- WER-EA evidence layer, source role, source quality, reader anchor, figure handoff, and reviewer risk when a screening matrix is requested.

## Civil Materials Citation Rules

- Prefer primary research and authoritative review articles over generic web summaries.
- Separate mechanism citations from performance citations.
- For asphalt and pavement manuscripts, keep binder/emulsion, aggregate-interface, mixture, construction, and service-condition evidence separate.
- For cement/concrete manuscripts, keep fresh properties, strength, durability, hydration/microstructure, and sustainability boundary citations separate.
- For CBM/JBE/CSCM-style manuscripts, emphasize applied material performance and reviewer-safe engineering evidence.
- For CCC-style manuscripts, emphasize mechanism depth and composite-material logic.
- For RMPD/IJPE-style manuscripts, emphasize pavement performance, field relevance, test standards, and traffic/environment service conditions.

Use `scripts/build_citation_matrix.py` to create a CSV search-and-citation matrix from a topic, claims, and target journals.

Use `references/academic-search-mcp.md` when explaining or planning a future civil-materials academic-search MCP.