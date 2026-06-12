# Materials Science Paper Production System PRD

**Date:** 2026-06-09  
**Owner:** materials-skills  
**Status:** Draft for detailed design  
**Source inspirations:** `nature-skills` static/dynamic skill architecture and the AutoResearch scientific paper writing skill group.

## 1. Purpose

Upgrade `materials-skills` from a set of specialized research skills into
a coordinated materials paper production system.

The system should help a civil engineering materials researcher move from a
rough research idea to a review-ready manuscript package through routed,
evidence-grounded, testable skill workflows. The first priority domain remains
waterborne epoxy modified emulsified asphalt (WER-EA) and related modified
emulsified asphalt bonding-performance research, while keeping the architecture
general enough for cement/concrete, construction materials, durability, and
pavement-materials topics.

This PRD is a top-level product and system description. It intentionally does
not define implementation tasks yet. Detailed design documents and execution
plans will be created after this PRD is reviewed.

## 2. Background

The current `materials-skills` package already contains specialized
modules for research routing, paper reading, citation mapping, writing,
polishing, reviewer response, simulated review, figures, PPT/PPTX, and data
packaging. Recent upgrades also introduced a stronger static/dynamic
architecture, reader standard output package, expanded citation search tooling,
and a WER-EA figure atlas.

Two external patterns are worth absorbing:

1. `nature-skills`: a skill-engineering pattern based on short routers,
   declarative manifests, static core rules, lazy fragments, references,
   templates, scripts, tests, and shared resources.
2. AutoResearch paper-writing skill group: a paper-production pattern based on
   sub-skill division of labor, phase routing, quality gates, weakness routing,
   peer-review loops, and score progression.

The target upgrade combines these two ideas:

- Use `nature-skills` as the engineering skeleton.
- Use paper-writing as the research-production control loop.
- Adapt both to materials evidence, journal expectations, laboratory
  constraints, standards, and WER-EA manuscript needs.

## 3. Product Vision

`materials-skills` should behave like a research co-pilot for civil
materials papers, not just like a collection of independent prompts.

The user should be able to ask for high-level outcomes such as:

- "Help me write a WER-EA mini-review."
- "Turn these 30 papers into a review argument."
- "Check whether this manuscript can target CBM Transportation."
- "Find what evidence is missing before I draft the discussion."
- "Audit this figure package for reviewer risk."
- "Route the simulated reviewer comments to the right skills."

The system should then route the work across reader, citation, writing,
figure, data, polishing, reviewer, and response modules with explicit
handoffs, evidence boundaries, and quality gates.

## 4. Goals

1. Turn `materials-research` into a paper-production orchestrator.
2. Add a materials paper-production reference layer that explains
   workflows, phases, weakness routing, quality gates, and score progression.
3. Standardize weakness routing across skills so review findings automatically
   map to the responsible module.
4. Extend manifest axes so skills can reason about paper stage, evidence level,
   and package type, not only task/domain/journal.
5. Add paper-level quality gates that complement code-level release checks.
6. Make writing, polishing, reviewer, and response skills consume standard
   intermediate artifacts instead of drafting from loose context.

## 5. Non-Goals

- This PRD does not implement the upgrade.
- This PRD does not rewrite all skills immediately.
- This PRD does not replace human supervisor, co-author, or journal decisions.
- This PRD does not claim live journal facts without browsing official sources.
- This PRD does not guarantee publishability; it creates a stronger workflow
  for evidence, structure, and reviewer-risk control.

## 6. Users And Use Cases

### Primary User

A civil engineering materials graduate researcher preparing review papers,
experimental manuscripts, presentation materials, and submission packages.

### Primary Use Cases

1. WER-EA mini-review production.
2. Experimental WER-EA bonding-performance manuscript planning.
3. Literature screening and claim-source mapping.
4. Full-paper reading and source-grounded note packaging.
5. Mechanism-evidence-boundary extraction.
6. Figure and table package planning.
7. Reviewer-risk audit and revision routing.
8. Journal targeting and submission package preparation.

## 7. Six Upgrade Points

### 7.1 Upgrade Point 1: `materials-research` As Orchestrator

`materials-research` should become the main paper-production controller.
It should still route by task, domain, and journal, but it should also manage
multi-skill workflows.

Expected orchestration routes:

- Idea route: topic positioning -> gap -> research question -> paper angle.
- Literature route: search strategy -> screening -> citation matrix -> source
  quality audit.
- Reading route: source-grounded reader package -> claim/evidence/mechanism
  extraction -> handoff to writing and figure skills.
- Writing route: argument chain -> section draft -> claim-strength audit.
- Figure route: figure contract -> WER-EA atlas selection -> visual QA.
- Review route: simulated reviewer report -> weakness routing -> targeted
  fixes -> regression check.
- Submission route: journal fit -> cover letter/highlights/graphical abstract
  -> final risk audit.

The orchestrator should not duplicate every companion skill. It should decide
the route, load the minimum needed guidance, request or consume handoff
artifacts, and return a clear next-action package.

### 7.2 Upgrade Point 2: Paper-Production Orchestrator Reference

Add a top-level reference document under `materials-research`:

`skills/materials-research/references/paper-production-orchestrator.md`

This document should define:

- WER-EA mini-review production route.
- Experimental manuscript production route.
- Submission-package route.
- Phase routing from early idea to final review.
- Required handoff artifacts between modules.
- Quality gates and stop/go criteria.
- Weakness routing table.
- Score progression path.
- Reviewer-risk regression loop.

The document should be concise enough to load when needed, but detailed enough
that another agent can follow the system without relying on hidden context.

### 7.3 Upgrade Point 3: Civil-Materials Weakness Routing

Introduce a shared weakness-routing table that maps reviewer comments,
self-review findings, or quality-gate failures to the skill responsible for
repair.

Initial routing examples:

| Weakness | Route To | Expected Fix |
|---|---|---|
| Mechanism evidence is too speculative | `materials-reader` + `materials-citation` | Rebuild claim-evidence-mechanism-boundary rows and mark missing evidence. |
| Citation coverage is too narrow | `materials-citation` | Run targeted search, source quality audit, and citation matrix update. |
| Recent WER-EA literature is missing | `materials-citation` | Run recent-year search and update screening criteria. |
| Claim strength exceeds evidence | `materials-polishing` + `materials-reviewer` | Downgrade causal wording and add reviewer-risk note. |
| Figure caption overclaims mechanism | `materials-figure` | Rewrite caption boundary and link figure panels to evidence anchors. |
| Experimental variables are unclear | `materials-research` + `materials-data` | Rebuild test matrix, variables, controls, and metadata. |
| Standards or test conditions are missing | `materials-reader` + `materials-writing` | Extract test conditions and update method/reporting text. |
| Manuscript structure reads like a paper list | `materials-writing` | Rebuild section logic around evidence roles and review questions. |
| Reviewer response lacks proof of change | `materials-response` | Add location, revision evidence, and response status. |

The weakness router should become a reusable artifact consumed by reviewer,
response, writing, polishing, and research orchestration workflows.

### 7.4 Upgrade Point 4: More Expressive Manifest Axes

The current manifest axes such as `task`, `domain`, and `journal` are useful
but not enough for a full paper-production workflow.

Add or standardize new axes where appropriate:

| Axis | Purpose | Example Values |
|---|---|---|
| `paper_stage` | Identify where the user is in the manuscript lifecycle. | `idea`, `screening`, `reading`, `drafting`, `revision`, `submission` |
| `evidence_level` | Express how strong the current support is. | `performance-only`, `mechanism-supported`, `durability-supported`, `field-validated` |
| `output_package` | Choose the concrete deliverable shape. | `note`, `matrix`, `reader-package`, `manuscript`, `figure-package`, `submission-package` |
| `workflow_mode` | Distinguish one-shot output from iterative production. | `single-task`, `pipeline`, `review-loop` |

These axes should not be added mechanically to every skill. They should be
introduced where they change routing, loading, output contracts, or quality
gates.

### 7.5 Upgrade Point 5: Paper-Level Quality Gates

Add paper-level quality gates that complement repository release checks.

Proposed gates:

| Gate | Name | What It Checks |
|---|---|---|
| Gate 1 | Literature Coverage | Search strategy, screening criteria, source quality, recent literature, citation roles. |
| Gate 2 | Source Anchoring | Every major claim has a source anchor, page/figure/table location, and evidence type. |
| Gate 3 | Mechanism Boundary | Mechanism claims are separated into measured, inferred, speculative, and missing. |
| Gate 4 | Figure And Table Integrity | Figures/tables have evidence links, caption boundaries, readable exports, and text references. |
| Gate 5 | Manuscript Logic | Argument chain, section transitions, contribution/gap alignment, and missing-evidence flags. |
| Gate 6 | Reviewer Simulation | Reviewer risks are prioritized, routed, fixed, and regression-checked. |
| Gate 7 | Submission Fit | Journal scope, article type, formatting, cover letter, highlights, and declarations are checked. |

Each gate should produce a machine-readable or table-structured report so later
skills can consume it instead of relying on prose memory.

### 7.6 Upgrade Point 6: Standard Intermediate Artifacts

Writing, polishing, reviewer, response, figure, and submission workflows should
consume standard intermediate artifacts whenever available.

Priority artifacts:

- `reader-package/package_manifest.json`
- `reader-package/source_map.json`
- `reader-package/citation_handoff.csv`
- `reader-package/figure_handoff.csv`
- `reader-package/review_handoff.md`
- `claim-evidence-boundary table`
- `mechanism-evidence table`
- `weakness-routing report`
- `figure-contract`
- `data/FAIR package manifest`
- `submission checklist`

Expected behavior:

- `materials-writing` drafts from evidence artifacts, not loose claims.
- `materials-polishing` downgrades or strengthens claims based on the
  evidence-level field.
- `materials-reviewer` emits weakness routes, not only comments.
- `materials-response` uses routed weaknesses to build point-by-point
  replies and revision proof.
- `materials-figure` consumes source anchors and caption boundaries.
- `materials-research` tracks which gates are passed, failed, or blocked.

## 8. Target Workflow

### 8.1 WER-EA Mini-Review Workflow

1. Topic framing:
   - Define scope, angle, audience, and target journal family.
2. Literature screening:
   - Use `materials-citation` for WER-EA query strategy, source quality,
     recent-year coverage, and citation matrix.
3. Source-grounded reading:
   - Use `materials-reader` to build reader packages and extract
     claim/evidence/mechanism/boundary rows.
4. Review architecture:
   - Use `materials-writing` to build evidence-role-based sections,
     not paper-title-based sections.
5. Figure planning:
   - Use `materials-figure` to create study selection flow, mechanism
     map, evidence heatmap, dosage window, and reviewer-safe caption boundaries.
6. Quality gates:
   - Run literature, source anchoring, mechanism boundary, figure/table, and
     manuscript logic gates.
7. Simulated review:
   - Use `materials-reviewer` to identify major/minor weaknesses.
8. Weakness routing:
   - Route each weakness to reader, citation, writing, polishing, figure, data,
     or response modules.
9. Revision loop:
   - Fix routed weaknesses and run regression checks.
10. Submission planning:
   - Verify journal facts live when needed and build final package.

### 8.2 Experimental Manuscript Workflow

1. Define research question and hypothesis.
2. Build test matrix and standards map.
3. Connect each experiment to a manuscript claim.
4. Prepare data/FAIR package and source metadata.
5. Draft results/discussion only from supplied evidence.
6. Build figures/tables with uncertainty, conditions, and caption boundaries.
7. Run reviewer-risk and claim-strength audits.
8. Prepare submission package.

## 9. Acceptance Criteria

This PRD will be considered implemented when:

1. `materials-research` can route paper-production workflows by stage,
   evidence level, output package, task, domain, and journal.
2. `paper-production-orchestrator.md` exists and is referenced by the research
   skill manifest.
3. A weakness-routing table exists and is consumed by reviewer/response or
   research workflows.
4. Paper-level quality gates are documented and at least partially automated or
   template-backed.
5. Writing, polishing, reviewer, response, and figure skills document how they
   consume standard intermediate artifacts.
6. Release checks verify that new manifest paths, templates, and references
   exist and that root/plugin mirrors remain aligned.
7. WER-EA mini-review and experimental-manuscript workflows can be followed
   without relying on unstated memory.

## 10. Risks And Controls

| Risk | Control |
|---|---|
| The orchestrator becomes too large and duplicates companion skills. | Keep `SKILL.md` short; move details into references and route to companion modules. |
| Paper gates become vague checklists. | Use structured templates and required fields. |
| The system overclaims publishability. | Use evidence-level and reviewer-risk fields; require live verification for journal facts. |
| WER-EA logic overfits one topic. | Put WER-EA as the first-class route, but keep generic materials axes. |
| Agents ignore artifacts and draft from memory. | Require artifact-first behavior in writing, polishing, reviewer, and response contracts. |
| Root and plugin mirror drift. | Keep release checks and mirror identity gates. |

## 11. Proposed Document And File Map For Later Design

Likely files to create or update in later implementation:

- `skills/materials-research/references/paper-production-orchestrator.md`
- `skills/materials-research/assets/templates/weakness-routing-template.csv`
- `skills/materials-research/assets/templates/paper-gate-report-template.md`
- `skills/materials-research/manifest.yaml`
- `skills/materials-research/SKILL.md`
- `skills/materials-writing/static/core/contract.md`
- `skills/materials-polishing/static/core/contract.md`
- `skills/materials-reviewer/static/core/contract.md`
- `skills/materials-response/static/core/contract.md`
- `skills/materials-figure/static/core/contract.md`
- `scripts/check_skill_architecture.py`
- `scripts/run_release_checks.py`
- Matching files under `plugins/materials-skills/skills/`

This list is intentionally provisional. The detailed design should decide which
files are necessary and how much automation belongs in phase one.

## 12. Open Design Questions

1. Should paper-level quality gates be implemented first as templates, Python
   scripts, or both?
2. Should weakness routing live only in `materials-research`, or should
   it be promoted into `_shared` for all skills?
3. Should the first implementation target only the WER-EA mini-review route, or
   also the experimental manuscript route?
4. Should score progression use numerical scores, maturity levels, or both?
5. Should reviewer simulation output a CSV/JSON route report in addition to
   Markdown?

## 13. Recommended Next Step

Create a detailed design document that turns this PRD into concrete module
boundaries, artifact schemas, routing contracts, and validation rules.

After the design is approved, create an implementation plan with staged tasks:

1. Orchestrator reference and manifest routing.
2. Weakness-routing templates.
3. Paper-level gate templates.
4. Writing/reviewer/response artifact-consumption contracts.
5. Release-check integration.
6. WER-EA mini-review workflow smoke test.

