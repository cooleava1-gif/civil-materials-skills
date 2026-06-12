# Materials Science P2 Outcome Showcase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the current demo and gallery entry surface into outcome-level showcase pages for submission packages, reviewer responses, and FAIR data packages.

**Architecture:** Build a new `docs/showcases/` layer that sits between the workflow demos and the deep skill docs. Each showcase page should feel like a concrete result entry point: what the deliverable is, which assets prove it, which prompt starts it, and which repo files exemplify it. Then wire these pages into the root README, install guide, gallery, and release checks.

**Tech Stack:** Markdown, Python `unittest`, existing release-check scripts

---

### Task 1: Add Failing Outcome Showcase Contract Tests

**Files:**
- Modify: `tests/test_product_docs_contract.py`

- [ ] **Step 1: Add showcase hub assertions**

```python
self.assertTrue((ROOT / "docs" / "showcases" / "README.md").is_file())
```

- [ ] **Step 2: Add three outcome-page assertions**

```python
for slug in ["submission-package", "reviewer-response", "fair-data-package"]:
    self.assertTrue((ROOT / "docs" / "showcases" / f"{slug}.md").is_file())
```

- [ ] **Step 3: Re-run the test and verify it fails**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: FAIL because the showcase docs do not exist yet.

- [ ] **Step 4: Keep the assertions concrete**

```python
required_sections = ["## Outcome Snapshot", "## Demo Prompt", "## Proof Assets", "## When To Use This Route"]
```

- [ ] **Step 5: Commit**

```bash
git add tests/test_product_docs_contract.py
git commit -m "test: require outcome showcase docs"
```

### Task 2: Create Outcome Showcase Pages

**Files:**
- Create: `docs/showcases/README.md`
- Create: `docs/showcases/submission-package.md`
- Create: `docs/showcases/reviewer-response.md`
- Create: `docs/showcases/fair-data-package.md`

- [ ] **Step 1: Add the showcase hub**

```markdown
## Outcome Index

1. Submission package
2. Reviewer response
3. FAIR data package
```

- [ ] **Step 2: Give each outcome page the same structure**

```markdown
## Outcome Snapshot
## Demo Prompt
## Proof Assets
## Build Path
## When To Use This Route
```

- [ ] **Step 3: Use real repo assets and examples**

```markdown
- `skills/materials-response/examples/cbm-major-revision-response-example.md`
```

- [ ] **Step 4: Re-run the product docs contract test**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: showcase assertions pass; README/gallery linkage assertions may still need updates.

- [ ] **Step 5: Commit**

```bash
git add docs/showcases
git commit -m "docs: add outcome showcase pages"
```

### Task 3: Wire Showcases Into The Front Door

**Files:**
- Modify: `README.md`
- Modify: `install.md`
- Modify: `docs/gallery/README.md`

- [ ] **Step 1: Add root-level outcome links**

```markdown
## Outcome Showcases
```

- [ ] **Step 2: Add install guide pointers**

```markdown
## Showcase Shortcuts
```

- [ ] **Step 3: Add gallery links for the three outcomes**

```markdown
## Outcome Showcases
```

- [ ] **Step 4: Re-run the product docs contract test**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add README.md install.md docs/gallery/README.md
git commit -m "docs: link outcome showcases from the front door"
```

### Task 4: Lock It Into Release Checks And Verify

**Files:**
- Modify: `scripts/run_release_checks.py`

- [ ] **Step 1: Add release markers for showcase docs**

```python
if "## Outcome Showcases" not in readme_text:
    issues["skills_index"].append("README.md missing outcome showcases section")
```

- [ ] **Step 2: Re-run targeted tests**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: PASS

- [ ] **Step 3: Run full verification in the dependency-complete environment**

Run: `python .\scripts\run_release_checks.py --json`
Expected: final JSON `status` is `pass`.

- [ ] **Step 4: Check git status**

Run: `git status --short --branch`
Expected: only intended showcase changes are present before commit, then clean after commit.

- [ ] **Step 5: Commit**

```bash
git add scripts/run_release_checks.py
git commit -m "test: lock outcome showcase release surface"
```
