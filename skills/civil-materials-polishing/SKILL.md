---
name: civil-materials-polishing
description: >-
  Polish, translate, tighten, restructure, or risk-audit English manuscript prose for civil engineering and construction materials research. Use for claim-strength control, Chinese-to-English academic writing, CBM, CBM in Transportation, CCC, CSCM, JBE, RMPD, IJPE, JRE, asphalt pavement materials, cement/concrete, durability, sustainability, abstracts, highlights, introductions, results, discussions, conclusions, and cover letters.
  
  Also trigger on:
  - English: academic polishing, language editing, prose tightening, claim strength audit, overclaiming check, causality review, novelty assessment
  - Chinese: 学术写作、科研写作、论文润色、写paper、SCI写作、英文论文润色、语言编辑、润色、改写、学术英语、英文写作、论文降重、中译英
  
  Specializes in:
  - Nature-style academic prose polishing
  - Claim-evidence-mechanism boundary control
  - Journal-specific language optimization
version: 2.0.0
author: Civil Materials Team, refactored into static/dynamic layers
---


# Civil Materials Polishing

Polish civil materials prose while preserving scientific responsibility.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect the section, journal family, and language direction.
3. Load only the matching fragments.
4. Apply the language rulebook, claim-strength ladder, and domain language fragment.
5. Preserve facts, evidence strength, units, citations, and author intent.
6. Return polished text plus a short risk note when claims are too strong.

## Core Rule

Do not make weak evidence sound strong. Civil materials writing should be clear, engineering-grounded, and reviewer-safe.

Use `references/language-rulebook.md` for general manuscript language, `references/claim-strength-ladder.md` when causality or novelty is risky, and `references/chinese-to-english-patterns.md` for Chinese-to-English polishing.

Use `references/conclusions.md` for conclusion sections, especially when performance, mechanism, durability, or field-application claims could be overstated.

Use this module for English polishing. Use `civil-materials-research` first when the argument, journal fit, or evidence chain is unclear.

Use `examples/claim-strength-polishing-example.md` as a concrete model. Use `tests/pressure-tests/overclaim-and-literal-translation.md` to check that polishing improves language without inflating weak evidence.