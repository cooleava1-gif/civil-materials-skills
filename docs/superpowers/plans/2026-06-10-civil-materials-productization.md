# Civil Materials Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current civil-materials skill bundle into a more polished, nature-style product surface without weakening the existing paper-production architecture.

**Architecture:** Keep the research and release-check core intact, then add a stronger presentation layer around it: a sharper root README, a dedicated install guide, consistent per-skill README files, and plugin metadata that showcases real generated assets. Lock the new documentation surface with lightweight repository contract tests so future upgrades do not regress back into an internal-only bundle.

**Tech Stack:** Markdown, JSON, Python `unittest`, existing release-check scripts

---

### Task 1: Add Failing Product-Surface Contract Tests

**Files:**
- Create: `tests/test_product_docs_contract.py`

- [ ] **Step 1: Write the failing test**

```python
def test_every_skill_has_readme():
    self.assertTrue((ROOT / "skills" / "civil-materials-research" / "README.md").is_file())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: FAIL because `install.md`, skill README files, and screenshot metadata are incomplete or missing.

- [ ] **Step 3: Keep tests focused on productization contracts**

```python
required_sections = [
    "## When To Use",
    "## Inputs",
    "## Outputs",
    "## Example",
    "## Validation",
    "## Boundaries",
]
```

- [ ] **Step 4: Re-run the same test target**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: FAIL with only product-surface gaps, not syntax or import errors.

- [ ] **Step 5: Commit**

```bash
git add tests/test_product_docs_contract.py
git commit -m "test: add product docs contract coverage"
```

### Task 2: Rebuild Root Product Entry Surfaces

**Files:**
- Modify: `README.md`
- Create: `install.md`

- [ ] **Step 1: Rewrite the root README around workflow entry points**

```markdown
## Four Workflow Entry Points

| Workflow | Start With | Core Handoffs | Final Product |
|---|---|---|---|
| WER-EA mini-review | `civil-materials-research` | citation -> reader -> writing -> figure -> reviewer | Review-ready package |
```

- [ ] **Step 2: Add a dedicated installation guide**

```markdown
## Option 1: Codex Plugin

codex plugin marketplace add https://github.com/cooleava1-gif/civil-materials-skills.git --ref main
codex plugin add civil-materials-skills@civil-materials-skills
```

- [ ] **Step 3: Add a five-minute walkthrough**

```markdown
1. Route a WER-EA review question.
2. Build the citation matrix.
3. Extract a reader package.
4. Draft the review outline.
```

- [ ] **Step 4: Re-run the product docs contract test**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: root README and install guide assertions pass; skill README and plugin screenshot assertions may still fail.

- [ ] **Step 5: Commit**

```bash
git add README.md install.md
git commit -m "docs: rebuild civil materials product entry surfaces"
```

### Task 3: Add Consistent README Files For Every Skill

**Files:**
- Create: `skills/civil-materials-citation/README.md`
- Create: `skills/civil-materials-data/README.md`
- Modify: `skills/civil-materials-figure/README.md`
- Create: `skills/civil-materials-paper2ppt/README.md`
- Create: `skills/civil-materials-polishing/README.md`
- Create: `skills/civil-materials-pptx/README.md`
- Create: `skills/civil-materials-reader/README.md`
- Create: `skills/civil-materials-research/README.md`
- Create: `skills/civil-materials-response/README.md`
- Create: `skills/civil-materials-reviewer/README.md`
- Create: `skills/civil-materials-writing/README.md`
- Modify: `plugins/civil-materials-skills/skills/<same skill>/README.md` via mirror sync

- [ ] **Step 1: Use one shared README structure**

```markdown
## When To Use
## Inputs
## Outputs
## Example
## Validation
## Boundaries
```

- [ ] **Step 2: Make each README workflow-specific**

```markdown
Use this skill when the deliverable is a screened citation matrix with evidence-layer fields and reviewer-safe handoff columns.
```

- [ ] **Step 3: Sync the new README files into the plugin mirror**

```powershell
Copy-Item -Force .\skills\civil-materials-*\README.md .\plugins\civil-materials-skills\skills\ -Container
```

- [ ] **Step 4: Re-run the product docs contract test**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: skill README assertions pass; plugin screenshot assertions may still fail.

- [ ] **Step 5: Commit**

```bash
git add skills plugins/civil-materials-skills/skills
git commit -m "docs: add skill-level product readmes"
```

### Task 4: Upgrade Plugin Showcase Metadata And Release Checks

**Files:**
- Modify: `plugins/civil-materials-skills/.codex-plugin/plugin.json`
- Modify: `scripts/run_release_checks.py`

- [ ] **Step 1: Point plugin screenshots at real generated assets**

```json
"screenshots": [
  "./skills/civil-materials-figure/assets/wer-ea-atlas/generated/wer_ea_mechanism_map.png"
]
```

- [ ] **Step 2: Teach release checks to verify screenshot existence and install guide presence**

```python
if not (root / "install.md").is_file():
    issues["skills_index"].append("install.md is missing")
```

- [ ] **Step 3: Re-run the targeted tests**

Run: `python -m unittest discover -s tests -p "test_product_docs_contract.py" -v`
Expected: PASS

- [ ] **Step 4: Run the release checks**

Run: `python .\scripts\run_release_checks.py --json`
Expected: PASS or only known non-productization warnings.

- [ ] **Step 5: Commit**

```bash
git add plugins/civil-materials-skills/.codex-plugin/plugin.json scripts/run_release_checks.py
git commit -m "feat: productize plugin showcase metadata"
```

### Task 5: Final Verification And Installed-State Sync

**Files:**
- Modify: installed skill copies under `%CODEX_HOME%\skills` or `~\.codex\skills` via installer

- [ ] **Step 1: Reinstall the skills**

Run: `.\scripts\install.ps1`
Expected: updated `civil-materials-*` skills and `_shared` copied into the installed skill directory.

- [ ] **Step 2: Run the main release verification**

Run: `python .\scripts\run_release_checks.py --json`
Expected: top-level `status` is `pass`.

- [ ] **Step 3: Check git status**

Run: `git status --short --branch`
Expected: only intended tracked changes remain before commit, then clean after commit.

- [ ] **Step 4: Create the final commit**

```bash
git add README.md install.md tests/test_product_docs_contract.py scripts/run_release_checks.py skills plugins/civil-materials-skills
git commit -m "feat: productize civil materials skill entry experience"
```

- [ ] **Step 5: Report verification evidence**

```text
Report the exact test command, release check command, and git status result before claiming completion.
```
