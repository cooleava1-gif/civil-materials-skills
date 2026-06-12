# Round 2: Contract-Gated Handoff System

**Date:** 2025-06-11
**Status:** Draft
**Based on:** Round 1 fragment architecture migration

## 1. What & Why

**Problem**: Currently `handoffs: [materials-research, ...]` is a flat string list. There's no way to know:
- What exact artifact each skill produces
- Which downstream skill needs which artifact
- Whether a handoff artifact's schema has changed

**Solution**: A typed contract system where every skill declares **what it provides** and **what it consumes**, with machine-verifiable schemas.

## 2. Architecture

```
_shared/contracts/                       ← Contract registry
├── citation-handoff.yaml
├── reader-package.yaml
├── figure-handoff.yaml
├── data-package.yaml
└── gate-report.yaml

scripts/validate_handoffs.py             ← Validator CLI

run_release_checks.py                    ← Calls validate_handoffs.py
```

Each skill's manifest.yaml `handoffs:` field transforms:

```yaml
# BEFORE
handoffs:
  - materials-research
  - materials-reader

# AFTER
handoffs:
  provides:
    reader-package:
      description: "Bilingual Markdown notes with source anchors"
      contract: ../_shared/contracts/reader-package.yaml
      version: "1.0"
  consumes:
    - handoff: citation-handoff
      from: materials-citation
      optional: true
      description: "Citation matrix rows for figure mapping"
```

## 3. Handoff Contract Format (YAML)

```yaml
# _shared/contracts/citation-handoff.yaml
name: citation-handoff
version: "1.0"
description: "Citation matrix and claim-source mapping"
produced_by: materials-citation
consumed_by:
  - materials-reader
  - materials-figure
  - materials-research

artifacts:
  citation_handoff.csv:
    description: "CSV with citation mapping rows"
    required: true
    columns:
      claim_id: { type: string, required: true }
      source_anchor: { type: string, required: true }
      citation_key_or_doi: { type: string, required: true }
      evidence_layer: { type: string, required: true }
      certainty_tier: { type: string, required: true }
      panel_role: { type: string, required: false }
      visual_encoding: { type: string, required: false }
      caption_boundary: { type: string, required: true }
      reviewer_risk: { type: string, required: false }

templates:
  - assets/templates/citation-handoff-template.csv
```

## 4. Five Handoff Contracts

### 4.1 citation-handoff
Produced by: `materials-citation`
Consumed by: `reader`, `figure`, `research`
Artifact: `citation_handoff.csv`

### 4.2 reader-package
Produced by: `materials-reader`
Consumed by: `figure`, `writing`, `research`
Artifacts: `{paper-name}/notes.md`, `source_map.json`, terminology ledger

### 4.3 figure-handoff
Produced by: `materials-figure`
Consumed by: `paper2ppt`, `pptx`, `research`
Artifact: `figure_handoff.csv`

### 4.4 data-package
Produced by: `materials-data`
Consumed by: `figure`, `research`
Artifact: FAIR dataset package

### 4.5 gate-report
Produced by: `materials-research`
Consumed by: internal routing
Artifact: `paper-gate-report-template.md` output

## 5. Validator (`scripts/validate_handoffs.py`)

```bash
python scripts/validate_handoffs.py --json
```

Checks:

| Check | What it validates |
|---|---|
| **Completeness** | Every `consumes.handoff` has a matching `provides` across all skills |
| **Existence** | Every referenced `contract:` file exists in `_shared/contracts/` |
| **No orphans** | Every `provides` is consumed by at least one other skill |
| **Column coverage** | Required columns in contract exist in at least one template CSV |
| **Version match** | `consumes.version` satisfies `provides.version` |
| **No dangling** | No `consumes` references a non-existent handoff name |

Output on failure:

```json
{
  "status": "fail",
  "issues": {
    "materials-figure": [
      "consumes 'citation-handoff' → not provided by any skill in provides list"
    ],
    "materials-citation": [
      "provides 'citation-handoff' → not consumed by any skill"
    ]
  }
}
```

## 6. Manifest Changes (11 skills)

| Skill | Provides | Consumes |
|---|---|---|
| materials-citation | citation-handoff | — |
| materials-reader | reader-package | citation-handoff (optional) |
| materials-figure | figure-handoff | citation-handoff (optional), reader-package (optional), data-package (optional) |
| materials-data | data-package | — |
| materials-research | gate-report | citation-handoff, reader-package, figure-handoff, data-package |
| materials-writing | — | reader-package (optional) |
| materials-paper2ppt | — | figure-handoff (optional) |
| materials-pptx | — | figure-handoff (optional) |
| materials-polishing | — | — |
| materials-response | — | — |
| materials-reviewer | — | — |

(`consumes` marked optional = the handoff is useful but the skill can work without it)

## 7. Integration with Release Checks

```python
# run_release_checks.py adds:
from scripts.validate_handoffs import validate_all

handoff_issues = validate_all(SKILLS_ROOT)
if handoff_issues:
    all_issues["handoff_contracts"] = handoff_issues
```

## 8. Scope

- 5 contract YAML files in `_shared/contracts/`
- 11 manifest.yaml `handoffs:` upgrades
- 1 new script: `scripts/validate_handoffs.py`
- 1 integration point in `scripts/run_release_checks.py`
- Tests for the validator
