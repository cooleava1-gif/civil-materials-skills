# Architecture Migration — Round 1 Design

**Date:** 2025-06-11
**Status:** Draft
**Scope:** 7-skill fragment migration + SKILL.md slimming (11 skills)

## 1. Why This Migration

Current problem: 7 out of 11 skills have `manifest.yaml` but no `static/fragments/` — routing instructions, protocol steps, and deep rules all live in SKILL.md, making it >50 lines for most skills and 152 lines for reader. This wastes tokens on every invocation and makes routing logic untestable.

Goal: Every skill follows the same **Router/Static-Dynamic v2** pattern:

```
skills/civil-materials-<name>/
├── SKILL.md              ← ≤40 lines: identity + protocol steps only
├── manifest.yaml          ← always_load + axes.detect/values + references.on_demand
├── static/
│   ├── core/              ← always loaded (contract, stance, workflow)
│   │   ├── contract.md
│   │   ├── <name>-contract.md
│   │   └── workflow.md
│   └── fragments/         ← loaded per detected axis value
│       └── <axis>/
│           └── <value>.md
└── references/            ← on_demand (deep reference, examples)
```

## 2. Standardized Manifest Template

Every skill's `manifest.yaml` after migration follows this structure:

```yaml
version: "x.y.z"

always_load:
  - static/core/contract.md
  - ../_shared/core/stance.md
  - ../_shared/core/evidence-contract.md
  - static/core/<name>-contract.md
  - static/core/workflow.md

axes:
  <axis1>:
    default: <value>
    values:
      <value>:
        path: static/fragments/<axis1>/<value>.md
        triggers: [">=2 trigger words/phrases"]

  <axis2>: ...

references:
  on_demand:
    - condition: "..."
      path: references/<name>.md

quality_gates:
  - release gate must report no issues for this skill

handoffs:
  provides:
    <handoff-name>:
      description: "..."
  consumes:
    - handoff: <handoff-name>
      from: <source-skill>
      optional: true|false

release_checks:
  - scripts/run_release_checks.py --json
```

## 3. Seven-Skill Fragment Layouts

### 3.1 civil-materials-citation

New domain fragments:
- material_domain/asphalt → static/fragments/domain/asphalt.md
- material_domain/cement-concrete → static/fragments/domain/cement-concrete.md
- material_domain/civil-materials → static/fragments/domain/civil-materials.md

`task` and `journal_family` axes stay pointing to `references/` for now.

### 3.2 civil-materials-data

New data_task fragments:
- data_task/availability-statement → static/fragments/data_task/availability-statement.md
- data_task/repository-plan → static/fragments/data_task/repository-plan.md
- data_task/fair-check → static/fragments/data_task/fair-check.md

New domain fragments (same as citation):
- domain/asphalt → static/fragments/domain/asphalt.md
- domain/cement-concrete → static/fragments/domain/cement-concrete.md
- domain/civil-materials → static/fragments/domain/civil-materials.md

### 3.3 civil-materials-paper2ppt

New task fragments:
- task/slide-outline → static/fragments/task/slide-outline.md
- task/pptx-deck → static/fragments/task/pptx-deck.md

### 3.4 civil-materials-polishing

New language fragments:
- language/en → static/fragments/language/en.md
- language/zh-to-en → static/fragments/language/zh-to-en.md

New paper_type fragments:
- paper_type/research → static/fragments/paper_type/research.md
- paper_type/review → static/fragments/paper_type/review.md

### 3.5 civil-materials-pptx

New template fragments:
- template/academic → static/fragments/template/academic.md
- template/defense → static/fragments/template/defense.md
- template/journal-club → static/fragments/template/journal-club.md

### 3.6 civil-materials-response

New tone axis fragments (extracted from SKILL.md):
- tone/academic → static/fragments/tone/academic.md
- tone/firm → static/fragments/tone/firm.md

response_task axis values stay in references/.

### 3.7 civil-materials-reviewer

New review_scope axis fragments (extracted from SKILL.md):
- review_scope/full-manuscript → static/fragments/review_scope/full-manuscript.md
- review_scope/figures-tables → static/fragments/review_scope/figures-tables.md
- review_scope/methodology → static/fragments/review_scope/methodology.md

review_depth axis values stay in references/.

## 4. SKILL.md Template (<=40 lines)

```markdown
---
name: civil-materials-<name>
version: "x.y.z"
description: One-line purpose
---

# Civil Materials <Name>

<One-paragraph role statement.>

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `task`, `journal_family`, and `material_domain` from user input.
3. Load only the matching fragments from `static/fragments/`.
4. Follow the contract in `static/core/<name>-contract.md`.
5. <Skill-specific protocol steps — only the load-bearing gates.>

## Gates

- <Critical rules — <=3 items>
```

## 5. SKILL.md Slimming Plan

| Skill | Current | Target | What moves |
|---|---|---|---|
| reader | 152 | <=35 | Source format rules, output type rules, examples |
| research | 135 | <=40 | Task routing details, protocol steps |
| figure | 88 | <=30 | Backend selection rules, figure type rules |
| reviewer | 64 | <=30 | Review scope rules |
| response | 61 | <=30 | Tone rules |
| data | 55 | <=30 | Data task rules, domain rules |
| writing | 50 | <=30 | Section rules, language/journal rules |
| citation | 47 | <=25 | Domain rules, protocol details |
| pptx | 39 | <=25 | Template rules |
| polishing | 31 | <=20 | Language/paper type rules |
| paper2ppt | 25 | <=20 | Task rules |

## 6. No-Break Guarantee

Migration is **structure-only**: every rule that exists today stays in the system, just moved from SKILL.md to a fragment or reference.

Exception: tests that grep SKILL.md for specific phrases may break. Will audit and fix.

## 7. Verification Gate

After migration:
1. `python scripts/run_release_checks.py --json` — must pass
2. ALL 194 tests — must pass
3. Quick manual: 3 migrated SKILL.md files <=40 lines, readable

## 8. Roadmap

```
Round 1 (now):     Fragment architecture migration + SKILL.md slimming
Round 2 (next):    Contract-Gated Handoff — typed handoff schemas + validators
Round 3 (future):  Manifest validation CLI + routing tests + release check hardening
```
