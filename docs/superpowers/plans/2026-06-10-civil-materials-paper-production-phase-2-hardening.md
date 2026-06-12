# Materials Science Paper Production Phase 2 Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden the already-landed paper-production orchestrator so the WER-EA mini-review route is provable from repository artifacts, explicit handoffs, and release gates rather than unstated memory.

**Architecture:** Keep `materials-research` as the thin front door and keep shared paper-production contracts under `skills/_shared/paper-production/`. Phase 2 adds three things around the existing slice: route-smoke examples, filled handoff artifacts that can be audited, and release checks that prove those artifacts stay mirrored and coherent. Full end-to-end rehearsal and broader route expansion stay out of this pass.

**Tech Stack:** Markdown, YAML, CSV, Python `unittest`, existing release-check scripts, PowerShell installer

---

## File Map

- `skills/materials-research/tests/test_paper_production_route_smoke.py`
  - New smoke-contract test for the WER-EA mini-review route and the orchestrator output shape.
- `skills/materials-research/examples/library/paper-production-mini-review-example.md`
  - New concrete example showing the orchestrator response for a blocked WER-EA mini-review workflow.
- `skills/materials-research/examples/library/library-index.md`
  - Add the new paper-production example to the example catalog.
- `skills/materials-research/references/paper-production-orchestrator.md`
  - Link the route to the new concrete example and filled proof artifacts.
- `skills/_shared/paper-production/examples/wer-ea-mini-review-weakness-routing.csv`
  - New filled weakness-routing sample with realistic open, fixed, and regression-checked rows.
- `skills/_shared/paper-production/examples/wer-ea-mini-review-gate-report.md`
  - New filled gate report sample that cross-links to the weakness rows.
- `skills/_shared/paper-production/audit_paper_production.py`
  - Extend the audit from header-only checks to row-level and cross-link validation.
- `skills/materials-research/tests/test_paper_production_orchestrator.py`
  - Add regression coverage for the stronger audit and the filled examples.
- `scripts/run_release_checks.py`
  - Verify the new example artifacts, run the stronger audit, and keep root/plugin mirrors aligned.
- `plugins/materials-skills/skills/_shared/paper-production/examples/wer-ea-mini-review-weakness-routing.csv`
  - Mirror copy of the filled weakness-routing sample.
- `plugins/materials-skills/skills/_shared/paper-production/examples/wer-ea-mini-review-gate-report.md`
  - Mirror copy of the filled gate report sample.
- `plugins/materials-skills/skills/materials-research/examples/library/paper-production-mini-review-example.md`
  - Mirror copy of the route-smoke example.
- `plugins/materials-skills/skills/materials-research/examples/library/library-index.md`
  - Mirror copy of the updated example index.
- `plugins/materials-skills/skills/materials-research/references/paper-production-orchestrator.md`
  - Mirror copy of the updated orchestrator reference.

## Out Of Scope

- Full end-to-end rehearsal across live multi-skill execution
- A new orchestrator for domains beyond the current WER-EA-first slice
- Large manifest refactors unrelated to route hardening
- Reworking unrelated dirty files already present in the worktree

### Task 1: Add Failing WER-EA Route Smoke Coverage

**Files:**
- Create: `skills/materials-research/tests/test_paper_production_route_smoke.py`
- Create: `skills/materials-research/examples/library/paper-production-mini-review-example.md`
- Modify: `skills/materials-research/examples/library/library-index.md`

- [ ] **Step 1: Write the failing smoke test**

```python
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "skills" / "materials-research" / "examples" / "library" / "paper-production-mini-review-example.md"


class PaperProductionRouteSmokeTests(unittest.TestCase):
    def test_wer_ea_mini_review_example_exposes_route_shape(self):
        self.assertTrue(EXAMPLE.is_file(), "paper-production example must exist")
```

- [ ] **Step 2: Run the new test target to verify it fails**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production_route_smoke.py" -v`
Expected: FAIL because the example file and route markers do not exist yet.

- [ ] **Step 3: Add the concrete route example and index link**

```markdown
# Paper Production Mini-Review Example

Route: literature-review / asphalt-pavement / generic.

- `paper_stage`: screening
- `workflow_mode`: paper-production
- `output_package`: reader-package

## Available Artifacts
- `citation_handoff.csv`

## Blocked Gates
- `G2 Source Anchoring` -> next skill `materials-reader` -> expected artifact `reader-package/source_map.json`

## Weakness Routing Rows To Update
- `W-G2-001`

## Reviewer-Risk Note
- Mechanism wording is blocked until page-level anchors are restored.
```

- [ ] **Step 4: Expand the smoke assertions to cover the required route markers**

```python
for marker in [
    "Route: literature-review / asphalt-pavement / generic.",
    "`paper_stage`: screening",
    "`workflow_mode`: paper-production",
    "`output_package`: reader-package",
    "## Available Artifacts",
    "## Blocked Gates",
    "materials-reader",
    "reader-package/source_map.json",
    "## Weakness Routing Rows To Update",
    "## Reviewer-Risk Note",
]:
    self.assertIn(marker, EXAMPLE.read_text(encoding="utf-8"))
```

- [ ] **Step 5: Re-run the smoke test and commit**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production_route_smoke.py" -v`
Expected: PASS

```bash
git add skills/materials-research/tests/test_paper_production_route_smoke.py skills/materials-research/examples/library/paper-production-mini-review-example.md skills/materials-research/examples/library/library-index.md
git commit -m "test: add paper-production route smoke coverage"
```

### Task 2: Add Filled Handoff Artifacts For The Revision Loop

**Files:**
- Create: `skills/_shared/paper-production/examples/wer-ea-mini-review-weakness-routing.csv`
- Create: `skills/_shared/paper-production/examples/wer-ea-mini-review-gate-report.md`
- Modify: `skills/materials-research/references/paper-production-orchestrator.md`

- [ ] **Step 1: Write a failing test that expects filled proof artifacts**

```python
WEAKNESS_EXAMPLE = ROOT / "skills" / "_shared" / "paper-production" / "examples" / "wer-ea-mini-review-weakness-routing.csv"
GATE_EXAMPLE = ROOT / "skills" / "_shared" / "paper-production" / "examples" / "wer-ea-mini-review-gate-report.md"

self.assertTrue(WEAKNESS_EXAMPLE.is_file())
self.assertTrue(GATE_EXAMPLE.is_file())
```

- [ ] **Step 2: Run the orchestrator contract tests to verify the new assertions fail**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production_orchestrator.py" -v`
Expected: FAIL because the filled example artifacts do not exist yet.

- [ ] **Step 3: Create the filled weakness-routing sample**

```csv
weakness_id,source,severity,weakness_type,evidence_gap,route_to,required_fix,expected_artifact,status,regression_check
W-G2-001,gate:G2,major,source_anchor_missing,"FTIR and pull-off evidence are unanchored",materials-reader,"Rebuild page/table anchors for mechanism claims",reader-package/source_map.json,open,pending
W-G4-001,gate:G4,major,figure_caption_boundary,"Figure caption still overclaims chemical mechanism",materials-figure,"Rewrite caption boundary and relink source anchors",figure_handoff.csv,fixed,pending
W-G6-001,reviewer:R1,minor,claim_strength,"Reviewer flagged causal wording beyond available evidence",materials-polishing,"Downgrade wording and add reviewer-risk note",claim-strength-audit.md,regression-checked,pass
```

- [ ] **Step 4: Create the filled gate report sample and link it from the route doc**

```markdown
| gate_id | gate_name | status | evidence_checked | missing_inputs | routed_weakness_ids | next_skill | reviewer_risk |
|---|---|---|---|---|---|---|---|
| G2 | Source Anchoring | blocked | 18 anchored papers; 12 missing page-level anchors | `source_map.json` updates for 12 papers | W-G2-001 | materials-reader | unsupported mechanism synthesis |
| G4 | Figure And Table Integrity | fail | figure intake exists but caption boundary still overclaims | caption rewrite with source anchors | W-G4-001 | materials-figure | reviewer may reject mechanism figure |
| G6 | Reviewer Simulation | pass | routed reviewer fix rechecked | none | W-G6-001 | materials-polishing | residual wording risk is controlled |
```

- [ ] **Step 5: Re-run the orchestrator contract tests and commit**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production_orchestrator.py" -v`
Expected: PASS for the new file-existence and phrase checks; later audit-link checks may still fail.

```bash
git add skills/_shared/paper-production/examples skills/materials-research/references/paper-production-orchestrator.md skills/materials-research/tests/test_paper_production_orchestrator.py
git commit -m "docs: add paper-production proof artifacts"
```

### Task 3: Harden The Audit With Row-Level And Cross-Link Validation

**Files:**
- Modify: `skills/_shared/paper-production/audit_paper_production.py`
- Modify: `skills/materials-research/tests/test_paper_production_orchestrator.py`

- [ ] **Step 1: Add a failing regression test for invalid row values**

```python
with tempfile.TemporaryDirectory() as tmp:
    bad_weakness = Path(tmp) / "weakness.csv"
    bad_gate = Path(tmp) / "gate.md"
    bad_weakness.write_text(
        "weakness_id,source,severity,weakness_type,evidence_gap,route_to,required_fix,expected_artifact,status,regression_check\n"
        "W-G2-001,gate:G2,major,source_anchor_missing,gap,materials-reader,fix,reader-package/source_map.json,done,maybe\n",
        encoding="utf-8",
    )
    bad_gate.write_text(
        "| gate_id | gate_name | status | evidence_checked | missing_inputs | routed_weakness_ids | next_skill | reviewer_risk |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| G2 | Source Anchoring | blocked | anchors missing | source_map.json | W-G2-404 | materials-reader | unsupported claim |\n",
        encoding="utf-8",
    )
    report = audit.audit_files(bad_weakness, bad_gate)
    self.assertEqual(report["status"], "fail")
```

- [ ] **Step 2: Run the targeted test to verify the new regression fails**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production_orchestrator.py" -v`
Expected: FAIL because the audit currently checks only headers and gate names.

- [ ] **Step 3: Extend the audit to validate allowed values and cross-links**

```python
ALLOWED_WEAKNESS_STATUS = {"open", "fixed", "regression-checked"}
ALLOWED_REGRESSION_STATUS = {"pending", "pass", "fail", "not_applicable"}
ALLOWED_GATE_STATUS = {"pass", "fail", "blocked", "not_applicable"}
```

```python
if row["status"] not in ALLOWED_WEAKNESS_STATUS:
    issues.append(f"{path.as_posix()} row {row['weakness_id']} has invalid status {row['status']!r}")
if row["regression_check"] not in ALLOWED_REGRESSION_STATUS:
    issues.append(f"{path.as_posix()} row {row['weakness_id']} has invalid regression_check {row['regression_check']!r}")
if weakness_id not in routed_ids_from_gate_rows:
    issues.append(f"{gate_path.as_posix()} references unknown weakness id {weakness_id}")
```

- [ ] **Step 4: Add a passing assertion for the filled WER-EA proof artifacts**

```python
report = audit.audit_files(WEAKNESS_EXAMPLE, GATE_EXAMPLE)
self.assertEqual(report["status"], "pass", report)
```

- [ ] **Step 5: Re-run the targeted tests and commit**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production_orchestrator.py" -v`
Expected: PASS

```bash
git add skills/_shared/paper-production/audit_paper_production.py skills/materials-research/tests/test_paper_production_orchestrator.py
git commit -m "feat: harden paper-production audit regression checks"
```

### Task 4: Extend Release Checks To Prove The New Artifacts

**Files:**
- Modify: `scripts/run_release_checks.py`
- Create: `plugins/materials-skills/skills/_shared/paper-production/examples/wer-ea-mini-review-weakness-routing.csv`
- Create: `plugins/materials-skills/skills/_shared/paper-production/examples/wer-ea-mini-review-gate-report.md`
- Create: `plugins/materials-skills/skills/materials-research/examples/library/paper-production-mini-review-example.md`
- Modify: `plugins/materials-skills/skills/materials-research/examples/library/library-index.md`
- Modify: `plugins/materials-skills/skills/materials-research/references/paper-production-orchestrator.md`

- [ ] **Step 1: Add a failing release-check assertion for the new proof artifacts**

```python
PAPER_PRODUCTION_PROOF_FILES = [
    Path("materials-research") / "examples" / "library" / "paper-production-mini-review-example.md",
    Path("_shared") / "paper-production" / "examples" / "wer-ea-mini-review-weakness-routing.csv",
    Path("_shared") / "paper-production" / "examples" / "wer-ea-mini-review-gate-report.md",
]
```

- [ ] **Step 2: Run the release checks to verify the new bucket fails before implementation**

Run: `python .\scripts\run_release_checks.py --json`
Expected: FAIL in the `paper_production_orchestrator` bucket until the new files and mirror sync logic are wired in.

- [ ] **Step 3: Reuse the stronger audit inside `collect_paper_production_orchestrator_issues`**

```python
example_result = subprocess.run(
    [
        sys.executable,
        str(script),
        "--weakness-routing",
        str(shared_root / "examples" / "wer-ea-mini-review-weakness-routing.csv"),
        "--gate-report",
        str(shared_root / "examples" / "wer-ea-mini-review-gate-report.md"),
        "--json",
    ],
    check=False,
    capture_output=True,
    text=True,
)
example_report = json.loads(example_result.stdout)
if example_report["status"] != "pass":
    issue_list.append(f"{label}: paper-production example audit failed: {example_report['issues']}")
```

- [ ] **Step 4: Mirror the new example assets and verify the route example is indexed**

```python
collect_required_file_terms(
    root,
    label,
    skills_root,
    [Path("materials-research") / "examples" / "library" / "paper-production-mini-review-example.md"],
    ["Route:", "## Blocked Gates", "## Reviewer-Risk Note"],
    issues["paper_production_orchestrator"],
)
```

- [ ] **Step 5: Re-run release checks and commit**

Run: `python .\scripts\run_release_checks.py --json`
Expected: PASS or only previously accepted non-paper-production warnings.

```bash
git add scripts/run_release_checks.py plugins/materials-skills/skills/_shared/paper-production/examples plugins/materials-skills/skills/materials-research/examples/library plugins/materials-skills/skills/materials-research/references/paper-production-orchestrator.md
git commit -m "test: wire paper-production proof assets into release checks"
```

### Task 5: Final Verification, Install Sync, And Closeout

**Files:**
- Modify: installed skill copies under `%CODEX_HOME%\skills` or `%USERPROFILE%\.codex\skills` via installer

- [ ] **Step 1: Run the targeted paper-production tests**

Run: `python -m unittest discover -s skills/materials-research/tests -p "test_paper_production*.py" -v`
Expected: PASS

- [ ] **Step 2: Run release and architecture verification**

Run: `python .\scripts\run_release_checks.py --json`
Expected: top-level `status` is `pass`

Run: `python .\scripts\check_skill_architecture.py --json`
Expected: root/plugin mirror diff is empty or only an already-whitelisted exception

- [ ] **Step 3: Reinstall the skills**

Run: `.\scripts\install.ps1`
Expected: updated `materials-*` skills and `_shared` copied into the installed skills directory

- [ ] **Step 4: Confirm the working tree and stage only intended files**

Run: `git status --short --branch`
Expected: only the paper-production hardening files are staged for the final feature commit; unrelated pre-existing dirty files stay untouched

- [ ] **Step 5: Create the final feature commit and record the verification evidence**

```bash
git add skills/materials-research/tests/test_paper_production_route_smoke.py skills/materials-research/examples/library/paper-production-mini-review-example.md skills/materials-research/examples/library/library-index.md skills/materials-research/references/paper-production-orchestrator.md skills/_shared/paper-production/examples skills/_shared/paper-production/audit_paper_production.py skills/materials-research/tests/test_paper_production_orchestrator.py scripts/run_release_checks.py plugins/materials-skills/skills/_shared/paper-production/examples plugins/materials-skills/skills/materials-research/examples/library plugins/materials-skills/skills/materials-research/references/paper-production-orchestrator.md
git commit -m "feat: harden materials paper-production proofs"
```

```text
Report the exact unittest command, release-check command, architecture-check command, installer command, and final git status result before claiming the phase complete.
```

## Coverage Check Against The Current Spec

- PRD acceptance criterion 3 is strengthened by the filled weakness-routing sample plus row-level audit coverage.
- PRD acceptance criterion 4 is strengthened by a filled gate report example and stricter audit logic.
- PRD acceptance criterion 6 is strengthened by release checks that validate proof artifacts, not only templates.
- PRD acceptance criterion 7 is strengthened for the WER-EA mini-review route by a smoke example that another agent can follow without hidden memory.
- End-to-end rehearsal is intentionally deferred, matching the current instruction boundary.
