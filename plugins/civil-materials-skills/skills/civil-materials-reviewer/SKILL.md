---
name: civil-materials-reviewer
description: >-
  Simulate peer review, pre-submission referee screening, reviewer-risk audits, editorial-fit checks, or independent review reports for civil engineering and construction materials manuscripts. Use for CBM, CCC, RMPD, JBE, CSCM, JRE, asphalt pavement, emulsified asphalt, waterborne epoxy, cement/concrete, durability, mechanisms, and figures.
  
  Also trigger on:
  - English: peer review, referee report, pre-submission review, editorial review, manuscript audit, reviewer perspective
  - Chinese: 同行评审、审稿人视角、预审、稿件审查、审稿报告、编辑审查、审稿风险
  
  Specializes in:
  - Nature-style referee assessment with 3 referee reports
  - Cross-review synthesis and weakness identification
  - Desk-reject risk assessment
version: 2.0.0
author: Civil Materials Team, refactored into static/dynamic layers
---


# Civil Materials Reviewer

Simulate civil-materials peer review from the referee perspective.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect target journal family and review depth.
3. Load matching editorial criteria and review axes.
4. Generate exactly 2 independent review reports and 1 cross-review synthesis.
5. Keep review comments evidence-driven, constructive, and specific enough to revise.

## Review Report Contract

Each independent report must include:

- Overall assessment: Accept, Minor Revision, Major Revision, or Reject.
- Innovation and contribution score from 0 to 5.
- Methodology soundness score from 0 to 5.
- Evidence completeness score from 0 to 5.
- Writing quality score from 0 to 5.
- Figure/table quality score from 0 to 5.
- Journal fit score from 0 to 5.
- Numbered comments with severity: Critical, Major, or Minor.
- Recommendation with justification.

The cross-review synthesis must include:

- Agreed issues flagged by both reviewers.
- Disagreed issues flagged by only one reviewer.
- Combined recommendation and revision priority.

## Civil Materials Review Axes

Mechanism evidence completeness:

- FTIR/XRD evidence for chemical or phase changes.
- SEM, TEM, or fluorescence for morphology.
- DSC/TG or rheology for thermal and flow behavior when relevant.
- Each mechanism claim linked to a specific figure/table.

Performance evidence:

- Control group present.
- Multiple dosages or conditions tested.
- Error bars and replicate count reported.
- Temperature, humidity, loading rate, curing age, and conditioning stated.
- Wet, aged, or service-condition durability included when durability is claimed.

Journal fit:

- CBM: practical value, complete test matrix, comparison with existing materials.
- CCC: mechanism depth, composite logic, and novel insight.
- RMPD/IJPE/JRE: pavement relevance, construction and service conditions.
- JBE/CSCM: building or case-study relevance, application boundary, sustainability when claimed.

Use `scripts/build_review_report.py` to scaffold a two-reviewer report. Use `examples/cbm-review-simulation.md` and `examples/ccc-review-simulation.md` as output models. Use `tests/pressure-tests/weak-manuscript-review.md` to check that the simulated review catches weak novelty, missing conditions, unsupported mechanism claims, and figure-quality risks.