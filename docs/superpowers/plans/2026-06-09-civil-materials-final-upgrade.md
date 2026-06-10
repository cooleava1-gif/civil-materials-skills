# Civil Materials Final Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `civil-materials-skills` to a final-version, non-MVP research workflow by completing four pillars: unified skill architecture, reader standard output packages, expanded academic-search sources, and a WER-EA figure asset library.

**Architecture:** Keep the existing root skill folders as the source of truth and mirror every changed skill file into `plugins/civil-materials-skills/skills/<skill>/`. Standardize skill routing around `SKILL.md`, `manifest.yaml`, `static/core/*`, on-demand `references/*`, templates, scripts, tests, manifest-declared assets/scripts/handoffs, and release gates. Preserve the current evidence-to-review pipeline while adding production-grade package builders, source adapters, visual assets, and verification.

**Tech Stack:** Codex skills, Markdown references/templates, YAML manifests, Python stdlib + `unittest`, optional `httpx`, optional academic API keys, matplotlib/SVG figure scripts, PowerShell verification commands on Windows.

---

## Current State And Non-Negotiable Constraints

- Work from `the repository root`.
- Current branch is expected to be `codex/civil-materials-core-upgrades`.
- There are already uncommitted upgrades for reader/citation/figure. Workers must not revert them.
- `outputs/wer-ea-30-reading-sample/` must stay ignored and must not be staged.
- Root skill folders under `skills/` and plugin mirror folders under `plugins/civil-materials-skills/skills/` must stay byte-identical for changed files, except known generated cache files and the pre-existing figure hard-workflow root-only exception.
- New files should be ASCII unless an existing domain file intentionally contains Chinese trigger text. If Chinese trigger text is changed, validate real UTF-8 bytes with Python, not PowerShell display.
- Every pillar must add or update tests before being called complete.
- The final integration gate is:

```powershell
python -m unittest discover -s skills\civil-materials-reader\tests -v
python -m unittest discover -s skills\civil-materials-figure\tests -v
python -m unittest discover -s skills\civil-materials-citation\mcp\academic_search\tests -v
python scripts\run_release_checks.py --json
git diff --check
git status --short --branch --ignored -- outputs\wer-ea-30-reading-sample
```

Expected final results:

- All targeted tests pass.
- Release check JSON reports top-level `"status": "pass"`.
- `git diff --check` has no whitespace errors. CRLF warnings are acceptable.
- `outputs/wer-ea-30-reading-sample/` appears as ignored, not staged.

---

## Pillar 1: Unified Architecture Final Plan

### Purpose

Make every `civil-materials-*` skill follow one explicit architecture: short router `SKILL.md`, schema-backed `manifest.yaml`, always-loaded `static/core/*`, lazy references/templates/scripts, tests, and release gates. This should make the package closer to the clean nature-skills static/dynamic split while preserving civil-materials domain specificity.

### Final Architecture Contract

Every production skill must have:

- `SKILL.md`: short router with description, protocol, default output, and links to manifest-driven references.
- `manifest.yaml`: `version`, `always_load`, and `axes` with explicit values, paths, and trigger lists.
- `manifest.yaml` standard metadata blocks: `assets`, `scripts`, `tests`, `quality_gates`, `handoffs`, and `release_checks`.
- `agents/openai.yaml`: skill-specific agent metadata.
- `static/core/contract.md`: what the skill promises to produce and what it refuses to invent.
- `static/core/workflow.md`: stepwise workflow used on every invocation.
- `references/`: on-demand workflows and domain guidance.
- `assets/templates/`: reusable output contracts and CSV/Markdown schemas where the skill has deliverables.
- `tests/`: structural tests for key references, templates, routes, and anti-overclaim constraints.
- Plugin mirror under `plugins/civil-materials-skills/skills/<skill>/`.

Skills without scripts are allowed, but the manifest must still say what the skill can produce and how it routes.

### Files

Modify:

- `README.md`
- `docs/skills-index.md`
- `scripts/run_release_checks.py`
- `skills/*/SKILL.md`
- `skills/*/manifest.yaml`
- `skills/*/static/core/*`
- `plugins/civil-materials-skills/skills/*/SKILL.md`
- `plugins/civil-materials-skills/skills/*/manifest.yaml`
- `plugins/civil-materials-skills/skills/*/static/core/*`

Create:

- `docs/architecture/skill-architecture.md`
- `docs/architecture/release-gate-contract.md`
- `scripts/check_skill_architecture.py`
- `tests/test_skill_architecture_contract.py`
- Optional root wrappers if chosen for mirror symmetry:
  - `skills/_shared/SKILL.md`
  - `skills/_shared/agents/openai.yaml`
- Missing `static/core/contract.md` and `static/core/workflow.md` files for any skill lacking them.

### Task 1.1: Add Architecture Documentation

Owned files:

- `docs/architecture/skill-architecture.md`
- `docs/architecture/release-gate-contract.md`

Steps:

- [ ] Create `docs/architecture/skill-architecture.md` describing the required router, manifest, static core, references, templates, scripts, tests, and plugin mirror pattern.
- [ ] Include the final architecture contract table:

```markdown
| Layer | Required files | Responsibility | Release gate |
|---|---|---|---|
| Router | SKILL.md | Trigger and route only | frontmatter + links checked |
| Manifest | manifest.yaml | Axes, always_load, trigger routing, assets, scripts, tests, handoffs, release checks | path, schema, and UTF-8 checks |
| Static core | static/core/contract.md, static/core/workflow.md | Stable promises and base workflow | required terms checked |
| References | references/*.md | Heavy domain guidance | linked paths checked |
| Templates | assets/templates/* | Output schemas | required fields checked |
| Scripts | scripts/*.py | Reusable production helpers | targeted tests |
| Tests | tests/* | Regression and contract checks | release gate |
| Plugin mirror | plugins/civil-materials-skills/skills/<skill>/ | Installed package copy | byte identity check |
```

- [ ] Create `docs/architecture/release-gate-contract.md` listing every release check bucket, what it proves, and what it does not prove.
- [ ] Document the accepted mirror exceptions, including whether `_shared/SKILL.md`, `_shared/agents/openai.yaml`, and `civil-materials-figure/tests/test_figure_hard_workflow.py` are synced or explicitly allowlisted.
- [ ] Update `README.md` and `docs/skills-index.md` with a short "Architecture" section that points to these two docs.

Verification:

```powershell
Select-String -Path docs\architecture\skill-architecture.md -Pattern 'Plugin mirror','manifest.yaml','static/core'
Select-String -Path docs\architecture\release-gate-contract.md -Pattern 'mojibake','generated_artifacts','plugin mirror'
```

### Task 1.2: Add Architecture Checker Script

Owned files:

- `scripts/check_skill_architecture.py`
- `tests/test_skill_architecture_contract.py`

Implement `scripts/check_skill_architecture.py` with these functions:

```python
REQUIRED_CORE_FILES = ("static/core/contract.md", "static/core/workflow.md")
REQUIRED_ROUTER_FILES = ("SKILL.md", "manifest.yaml", "agents/openai.yaml")

def inspect_skill(skill_dir: Path) -> dict[str, object]:
    """Return missing files, missing manifest paths, and invalid trigger encodings."""

def inspect_all(root: Path = Path("skills")) -> dict[str, object]:
    """Inspect every civil-materials-* skill and return a JSON-safe report."""

def main(argv: list[str] | None = None) -> int:
    """Print JSON. Exit 0 only when every required architecture check passes."""
```

Required checks:

- Every `civil-materials-*` skill has `SKILL.md`, `manifest.yaml`, `agents/openai.yaml`.
- Every production skill has `static/core/contract.md` and `static/core/workflow.md`.
- Every `manifest.yaml` has standard blocks: `assets`, `scripts`, `tests`, `quality_gates`, `handoffs`, and `release_checks`.
- Every `always_load` path exists relative to the skill folder.
- Every `axes.*.values.*.path` exists relative to the skill folder.
- Every file listed in `assets`, `scripts`, and `tests` exists, unless listed under a documented exemption.
- Trigger strings do not contain known mojibake markers such as `鏂`, `绮`, `鍥`, `璇`, `浜`, `€`.
- Root and plugin mirror copies of changed architecture files match.

Test cases in `tests/test_skill_architecture_contract.py`:

```python
def test_all_civil_materials_skills_follow_static_dynamic_architecture():
    report = inspect_all(Path("skills"))
    assert report["status"] == "pass", report

def test_architecture_checker_reports_missing_manifest_path(tmp_path):
    # Build a minimal fake skill with a manifest route pointing to a missing file.
    # Assert inspect_skill returns that path under missing_manifest_paths.

def test_architecture_checker_detects_mojibake_trigger(tmp_path):
    # Build a minimal fake manifest with trigger '鏂囩尞PDF'.
    # Assert inspect_skill flags the trigger.

def test_architecture_checker_requires_standard_manifest_blocks(tmp_path):
    # Build a minimal fake skill without assets/scripts/tests/quality_gates/handoffs/release_checks.
    # Assert inspect_skill reports missing_manifest_blocks.
```

Verification:

```powershell
python -m unittest tests\test_skill_architecture_contract.py -v
python scripts\check_skill_architecture.py --json
```

### Task 1.3: Normalize Manifests And Static Core Across Skills

Owned files:

- `skills/<skill>/manifest.yaml`
- `skills/<skill>/static/core/contract.md`
- `skills/<skill>/static/core/workflow.md`
- Matching plugin mirror files.

Per-skill final contract:

- `civil-materials-research`: router and cross-skill planner.
- `civil-materials-reader`: source-grounded reading and standard reader package.
- `civil-materials-citation`: literature search, source screening, citation matrix, MCP.
- `civil-materials-writing`: manuscript and review drafting from evidence.
- `civil-materials-polishing`: language polishing and claim-strength control.
- `civil-materials-response`: reviewer response mapping.
- `civil-materials-reviewer`: simulated peer review and risk audit.
- `civil-materials-paper2ppt`: slide-ready Markdown handoff.
- `civil-materials-pptx`: real PPTX generation.
- `civil-materials-figure`: figure package, visual QA, WER-EA atlas.
- `civil-materials-data`: FAIR data package and data availability.

Steps:

- [ ] For each skill, make `SKILL.md` a router and move long invariant rules into `static/core/contract.md` or `static/core/workflow.md`.
- [ ] Ensure every `manifest.yaml` has `version`, `always_load`, `axes`, `assets`, `scripts`, `tests`, `quality_gates`, `handoffs`, and `release_checks`.
- [ ] Replace mojibake trigger text with valid UTF-8 Chinese trigger text when Chinese triggers are useful.
- [ ] Declare the citation test location as `mcp/academic_search/tests` rather than forcing a root `tests/` directory.
- [ ] Add smoke tests or explicit documented release exemptions for `civil-materials-paper2ppt` and `civil-materials-pptx`.
- [ ] Keep all existing useful references and templates; do not delete domain guidance merely to make files shorter.
- [ ] Mirror all root skill changes into `plugins/civil-materials-skills/skills/<skill>/`.

Verification:

```powershell
python scripts\check_skill_architecture.py --json
python scripts\run_release_checks.py --json
```

### Task 1.4: Harden Release Gate

Owned files:

- `scripts/run_release_checks.py`
- `tests/test_skill_architecture_contract.py`

New release buckets:

- `skill_architecture`
- `manifest_routes`
- `plugin_mirror_identity`
- `all_skill_mojibake`
- `reader_standard_package`
- `academic_search_expanded_sources`
- `wer_ea_asset_library`
- `paper2ppt_pptx_smoke_or_exemption`

Steps:

- [ ] Import or call the checker logic from `scripts/check_skill_architecture.py`.
- [ ] Expand mojibake scanning from selected skills to all `civil-materials-*` skills, root and plugin.
- [ ] Add plugin mirror identity checks for files touched by this final upgrade.
- [ ] Add `--check-only` or `--no-clean` mode so pure audits can avoid deleting `__pycache__` or generated byproducts.
- [ ] Add release checks for reader package scripts and WER-EA atlas required assets.
- [ ] Keep output JSON backward compatible: top-level `status`, `coverage`, `issues`, and test summaries.

Verification:

```powershell
python scripts\run_release_checks.py --json
```

Acceptance criteria for Pillar 1:

- Every skill follows the same static/dynamic router pattern.
- All manifest paths resolve.
- All changed root/plugin mirror files match.
- All mojibake markers are absent from checked triggers.
- Release gate proves the architecture rather than relying on README claims.

---

## Pillar 2: Reader Standard Output Package Final Plan

### Purpose

Turn `civil-materials-reader` into a production package generator for full-paper reading, WER-EA mini-review extraction, citation handoff, figure handoff, and Obsidian handoff. The final output must be a reusable folder, not isolated notes.

### Final Reader Package Contract

Standard package folder:

```text
reader-package/
  package_manifest.json
  source_map.json
  paper.md
  translation_notes.md
  source_anchor_checklist.md
  figure_table_cards.md
  mechanism_evidence_table.csv
  dosage_window_table.csv
  citation_handoff.csv
  figure_handoff.csv
  review_handoff.md
  obsidian_note.md
  qa_report.md
  assets/
    asset_manifest.md
    visual_asset_report.json
    contact_sheet.png
    rendered_pages/
```

Optional, only when requested or supported:

```text
reader-package/
  reader.html
  assets/crops/
  assets/tables/
```

The package must preserve:

- stable source IDs: `S001`, `C001`, `F001`, `T001`;
- page/section/figure/table anchor;
- original excerpt;
- Chinese interpretation when translation is requested;
- claim-evidence-boundary;
- confidence label;
- missing evidence flag;
- citation role and evidence type;
- figure archetype and visual risk boundary.

### Files

Modify:

- `skills/civil-materials-reader/SKILL.md`
- `skills/civil-materials-reader/manifest.yaml`
- `skills/civil-materials-reader/static/core/reader-contract.md`
- `skills/civil-materials-reader/static/core/workflow.md`
- `skills/civil-materials-reader/references/evidence-to-review-handoff.md`
- `skills/civil-materials-reader/references/fulltext-figure-anchored-reading.md`
- `skills/civil-materials-reader/references/wer-ea-intensive-reading-package.md`
- `scripts/run_release_checks.py`
- Matching plugin mirror files.

Create:

- `skills/civil-materials-reader/references/standard-output-package.md`
- `skills/civil-materials-reader/assets/schemas/source-map.schema.json`
- `skills/civil-materials-reader/assets/schemas/visual-asset-spec.schema.json`
- `skills/civil-materials-reader/assets/schemas/visual-asset-report.schema.json`
- `skills/civil-materials-reader/assets/schemas/reader-package-manifest.schema.json`
- `skills/civil-materials-reader/assets/templates/package-manifest-template.json`
- `skills/civil-materials-reader/assets/templates/qa-report-template.md`
- `skills/civil-materials-reader/scripts/build_reader_package.py`
- `skills/civil-materials-reader/scripts/audit_reader_package.py`
- `skills/civil-materials-reader/scripts/validate_reader_package.py`
- `skills/civil-materials-reader/tests/test_reader_package_contract.py`
- `skills/civil-materials-reader/tests/test_reader_package_scripts.py`
- `skills/civil-materials-reader/tests/test_validate_reader_package.py`
- Matching plugin mirror files.

### Task 2.1: Add Standard Package Reference And Templates

Owned files:

- `skills/civil-materials-reader/references/standard-output-package.md`
- `skills/civil-materials-reader/assets/schemas/*.schema.json`
- `skills/civil-materials-reader/assets/templates/package-manifest-template.json`
- `skills/civil-materials-reader/assets/templates/qa-report-template.md`
- Existing reader templates.

Steps:

- [ ] Define every required package file and required field in `standard-output-package.md`.
- [ ] State which files are mandatory for pasted text, DOI/HTML, full PDF, and WER-EA mini-review mode.
- [ ] Add the manifest template:

```json
{
  "package_type": "civil-materials-reader-package",
  "skill_version": "1.2.0",
  "source_type": "",
  "paper_title": "",
  "doi_or_url": "",
  "generated_at": "",
  "required_files": [
    "source_map.json",
    "paper.md",
    "translation_notes.md",
    "source_anchor_checklist.md",
    "figure_table_cards.md",
    "citation_handoff.csv",
    "figure_handoff.csv",
    "review_handoff.md",
    "qa_report.md"
  ],
  "handoff_targets": ["civil-materials-citation", "civil-materials-figure"],
  "evidence_boundary": "No unsupported claim is promoted without a source anchor."
}
```

- [ ] Add `qa-report-template.md` sections for source coverage, figure/table coverage, citation handoff, figure handoff, missing evidence, and overclaim risk.
- [ ] Update existing CSV templates so shared fields are consistent across `citation_handoff.csv`, `figure_handoff.csv`, and citation matrix fields.
- [ ] Add JSON Schemas for `source_map.json`, `visual_asset_spec.json`, `visual_asset_report.json`, and `package_manifest.json`.
- [ ] Treat `outputs/wer-ea-30-reading-sample/` as a local golden fixture for validation only. It remains ignored and is not versioned.

Verification:

```powershell
Select-String -Path skills\civil-materials-reader\references\standard-output-package.md -Pattern 'package_manifest.json','source_map.json','citation_handoff.csv','figure_handoff.csv','qa_report.md'
python - <<'PY'
import json
from pathlib import Path
for path in Path('skills/civil-materials-reader/assets/schemas').glob('*.schema.json'):
    json.loads(path.read_text(encoding='utf-8'))
print('schemas valid')
PY
```

### Task 2.2: Add Reader Package Builder

Owned files:

- `skills/civil-materials-reader/scripts/build_reader_package.py`
- Matching plugin mirror file.

Implement a deterministic builder that creates an empty but valid package scaffold from metadata and optional source-map JSON.

CLI:

```powershell
python skills\civil-materials-reader\scripts\build_reader_package.py --output-dir <dir> --source-type pasted-text --title "Example" --doi "10.x/example" --json
```

Required behavior:

- Create all mandatory package files.
- Copy template headers into Markdown/CSV files.
- Fill `package_manifest.json`.
- Escape CSV cells that begin with Excel formula characters: `=`, `+`, `-`, `@`.
- Never write outside the requested output directory.
- Refuse to overwrite a non-empty directory unless `--force` is passed.
- Print JSON with `status`, `output_dir`, `created_files`, and `warnings`.

Core functions:

```python
def build_reader_package(output_dir: Path, metadata: dict[str, str], *, force: bool = False) -> dict[str, object]:
    """Create a standard reader package and return a JSON-safe report."""

def write_csv_template(path: Path, fields: list[str]) -> None:
    """Write a one-row CSV header using newline='' and utf-8."""

def safe_resolve_output_dir(path: Path) -> Path:
    """Resolve output dir and reject dangerous roots such as drive root or home root."""
```

Verification:

```powershell
python skills\civil-materials-reader\scripts\build_reader_package.py --output-dir $env:TEMP\reader-package-smoke --source-type pasted-text --title "Smoke" --force --json
```

Expected: JSON reports `status: pass` and lists required files.

### Task 2.3: Add Reader Package Auditor

Owned files:

- `skills/civil-materials-reader/scripts/audit_reader_package.py`
- `skills/civil-materials-reader/scripts/validate_reader_package.py`
- Matching plugin mirror file.

Audit rules:

- Required files exist.
- `package_manifest.json` is valid JSON.
- `source_map.json` contains a list or object with stable source IDs when populated.
- CSV files contain required headers:
  - `citation_handoff.csv`: `claim_id`, `source_anchor`, `original_excerpt`, `citation_role`, `evidence_type`, `reviewer_risk`.
  - `figure_handoff.csv`: `claim_id`, `source_anchor`, `figure_archetype`, `certainty_tier`, `caption_boundary`, `reviewer_risk`.
- `qa_report.md` contains source coverage, missing evidence, and handoff status sections.
- `assets/asset_manifest.md` exists when `assets/` contains extracted files.
- `reader.html` is not required unless listed in `package_manifest.json`.
- No local absolute paths, secrets, or raw PDF source files are packaged.
- Obsidian note, when present, contains the validated sections:
  - `1 快读判断`
  - `2 实验证据层`
  - `3 写作转化层`
  - concept links.

CLI:

```powershell
python skills\civil-materials-reader\scripts\audit_reader_package.py --package-dir <dir> --json
python skills\civil-materials-reader\scripts\validate_reader_package.py --package-dir <dir> --json
```

Expected JSON:

```json
{
  "status": "pass",
  "issues": {
    "missing_files": [],
    "invalid_json": [],
    "missing_headers": [],
    "qa_gaps": []
  }
}
```

### Task 2.4: Add Reader Package Tests

Owned files:

- `skills/civil-materials-reader/tests/test_reader_package_contract.py`
- `skills/civil-materials-reader/tests/test_reader_package_scripts.py`
- Matching plugin mirror files.

Test cases:

```python
def test_standard_package_reference_lists_all_required_outputs():
    # Assert reference includes package_manifest.json, source_map.json, paper.md,
    # citation_handoff.csv, figure_handoff.csv, review_handoff.md, qa_report.md.

def test_builder_creates_auditable_package(tmp_path):
    # Run build_reader_package into tmp_path / "pkg".
    # Run audit_reader_package.
    # Assert both return status pass.

def test_builder_refuses_non_empty_directory_without_force(tmp_path):
    # Create tmp_path / "pkg" / "existing.txt".
    # Assert build_reader_package exits non-zero or returns status error.

def test_auditor_reports_missing_citation_handoff_header(tmp_path):
    # Build package, rewrite citation_handoff.csv with incomplete header.
    # Assert audit reports missing_headers.

def test_validate_reader_package_accepts_local_golden_samples_when_present():
    # If outputs/wer-ea-30-reading-sample exists, validate at least three child packages.
    # Skip with a clear message if the ignored local sample directory is absent.

def test_reader_schemas_are_valid_json_and_referenced_by_validator():
    # Assert every schema parses as JSON and validate_reader_package imports their paths.
```

Verification:

```powershell
python -m unittest discover -s skills\civil-materials-reader\tests -v
```

### Task 2.5: Wire Reader Package Into Manifest And Release Gate

Owned files:

- `skills/civil-materials-reader/SKILL.md`
- `skills/civil-materials-reader/manifest.yaml`
- `scripts/run_release_checks.py`
- Matching plugin mirror files.

Steps:

- [ ] Add `standard-output-package` route to `manifest.yaml`.
- [ ] Add valid Chinese trigger text for `标准输出包`, `全文精读包`, `文献精读包`, `综述交接包` after verifying UTF-8.
- [ ] Update `SKILL.md` default output section to require the standard package when the user requests full paper reading, WER-EA intensive reading, or handoff deliverables.
- [ ] Add release check bucket `reader_standard_package` that runs package builder/auditor in a temp directory.

Verification:

```powershell
python -m unittest discover -s skills\civil-materials-reader\tests -v
python scripts\run_release_checks.py --json
```

Acceptance criteria for Pillar 2:

- Reader has a documented standard output package.
- Builder can create a valid package without external dependencies.
- Auditor can fail an incomplete package with actionable JSON.
- Manifest routes full reading and WER-EA handoff requests to the package reference.
- Release gate proves the package scaffold stays functional.

---

## Pillar 3: Academic-Search Expanded Sources Final Plan

### Purpose

Upgrade `civil-materials-citation` from a focused Crossref/PubMed/OpenAlex/Semantic Scholar workflow into a broader academic-search layer comparable to nature-skills breadth, while keeping civil-materials evidence classification as the differentiator.

### Final Source Contract

Required adapters:

- Crossref: default DOI and metadata search.
- PubMed: MeSH and biomedical/chemistry-adjacent source search.
- OpenAlex: broad scholarly graph and open metadata.
- Semantic Scholar: broad citation/abstract enrichment.
- arXiv: methods and AI/materials-adjacent preprints.
- Scopus: optional Elsevier API, disabled without `SCOPUS_API_KEY`.
- ScienceDirect: optional Elsevier API, disabled without `ELSEVIER_API_KEY`.

Required new service capabilities:

- source selection and source warnings;
- DOI/PMID/arXiv/Scopus EID/PII/URL ID conversion;
- RIS/BibTeX/NBIB/CSV import and export helpers;
- CSL JSON, JSONL, and Zotero-friendly RIS/notes export options;
- deduplication by DOI, normalized title, external IDs, and year;
- source provenance fields in every merged record;
- WER-EA evidence-layer classification preserved after merge.

### Files

Modify:

- `skills/civil-materials-citation/SKILL.md`
- `skills/civil-materials-citation/manifest.yaml`
- `skills/civil-materials-citation/mcp/academic_search/README.md`
- `skills/civil-materials-citation/mcp/academic_search/server.py`
- `skills/civil-materials-citation/mcp/academic_search/service.py`
- `skills/civil-materials-citation/mcp/academic_search/adapters/__init__.py`
- `skills/civil-materials-citation/mcp/academic_search/adapters/base.py`
- `skills/civil-materials-citation/mcp/academic_search/tests/*`
- `skills/civil-materials-citation/references/academic-search-mcp.md`
- `scripts/run_release_checks.py`
- Matching plugin mirror files.

Create:

- `skills/civil-materials-citation/mcp/academic_search/adapters/arxiv.py`
- `skills/civil-materials-citation/mcp/academic_search/adapters/elsevier_common.py`
- `skills/civil-materials-citation/mcp/academic_search/adapters/scopus.py`
- `skills/civil-materials-citation/mcp/academic_search/adapters/sciencedirect.py`
- `skills/civil-materials-citation/mcp/academic_search/domain/identifiers.py`
- `skills/civil-materials-citation/mcp/academic_search/importers/citation_files.py`
- `skills/civil-materials-citation/mcp/academic_search/export/csl_json.py`
- `skills/civil-materials-citation/mcp/academic_search/export/jsonl.py`
- `skills/civil-materials-citation/mcp/academic_search/tests/test_arxiv_adapter.py`
- `skills/civil-materials-citation/mcp/academic_search/tests/test_elsevier_adapters.py`
- `skills/civil-materials-citation/mcp/academic_search/tests/test_identifiers.py`
- `skills/civil-materials-citation/mcp/academic_search/tests/test_citation_file_import.py`
- `skills/civil-materials-citation/mcp/academic_search/tests/test_format_conversion.py`
- `skills/civil-materials-citation/references/expanded-academic-search.md`
- Matching plugin mirror files.

### Task 3.1: Add arXiv Adapter

Owned files:

- `adapters/arxiv.py`
- `adapters/__init__.py`
- `tests/test_arxiv_adapter.py`

Behavior:

- Search arXiv API with query, year range, and limit.
- Fetch by arXiv ID or title.
- Normalize into the existing record schema:
  - `title`
  - `authors`
  - `year`
  - `abstract`
  - `doi`
  - `external_ids.arxiv`
  - `source`
  - `source_provenance`
  - `url`

No API key is required.

Test cases:

```python
def test_arxiv_search_parses_atom_feed():
    # Mock HTTP response with two Atom entries.
    # Assert normalized title, authors, year, arxiv ID, and source.

def test_arxiv_fetch_accepts_versioned_id():
    # external_id="2401.12345v2" should preserve version and canonical ID.

def test_arxiv_disabled_never_requires_api_key():
    # Adapter should not raise AdapterDisabled because no key is needed.
```

### Task 3.2: Add Elsevier Common, Scopus, And ScienceDirect Adapters

Owned files:

- `adapters/elsevier_common.py`
- `adapters/scopus.py`
- `adapters/sciencedirect.py`
- `tests/test_elsevier_adapters.py`

Environment variables:

- `SCOPUS_API_KEY`
- `ELSEVIER_API_KEY`
- `ELSEVIER_INSTTOKEN` optional

Behavior:

- Without key, raise `AdapterDisabled` with a clear message.
- With key, build correct request URLs and headers.
- Support mock-tested parsing for:
  - Scopus search result entries,
  - Scopus abstract retrieval by EID or DOI,
  - ScienceDirect article metadata by DOI or PII.
- Do not run live Elsevier tests in release gate.

Test cases:

```python
def test_scopus_disabled_without_key(monkeypatch):
    # Clear SCOPUS_API_KEY and assert AdapterDisabled.

def test_scopus_search_parses_mock_entries(monkeypatch):
    # Mock HTTP response. Assert source='scopus' and external_ids.eid exists.

def test_sciencedirect_disabled_without_key(monkeypatch):
    # Clear ELSEVIER_API_KEY and assert AdapterDisabled.

def test_sciencedirect_fetch_parses_mock_coredata(monkeypatch):
    # Mock metadata response by DOI. Assert DOI/title/journal/year.
```

### Task 3.3: Add ID Conversion And Dedup Domain Layer

Owned files:

- `domain/identifiers.py`
- `service.py`
- `tests/test_identifiers.py`

Functions:

```python
def normalize_arxiv_id(value: str | None) -> str | None:
    """Return canonical arXiv ID with optional version."""

def normalize_scopus_eid(value: str | None) -> str | None:
    """Return normalized Scopus EID."""

def normalize_pii(value: str | None) -> str | None:
    """Return normalized ScienceDirect PII."""

def merge_external_ids(records: list[dict[str, object]]) -> dict[str, str]:
    """Merge DOI, PMID, PMCID, arXiv, OpenAlex, Semantic Scholar, Scopus EID, and PII IDs."""

def deduplicate_records(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Deduplicate by DOI, external IDs, then normalized title + year."""
```

Test cases:

```python
def test_deduplicate_records_prefers_doi_then_external_ids():
    # Same DOI from Crossref and Scopus becomes one record with both sources.

def test_deduplicate_records_uses_normalized_title_and_year_when_no_doi():
    # Minor punctuation differences collapse when year matches.

def test_deduplicate_records_keeps_different_year_records_separate():
    # Avoid over-merging reviews with similar titles.

def test_identifier_normalizers_handle_urls_and_prefixed_ids():
    # DOI URLs, PMID:, PMCID, arXiv v1/v2, Scopus EID, and PII normalize predictably.
```

### Task 3.4: Add Citation File Import And Conversion

Owned files:

- `importers/citation_files.py`
- `export/formats.py`
- `server.py`
- `service.py`
- `tests/test_citation_file_import.py`

Supported inputs:

- RIS
- BibTeX
- NBIB
- CSV with DOI/title/year/journal columns

Supported outputs:

- RIS
- BibTeX
- GB/T 7714
- CSL JSON
- JSONL
- Zotero-friendly RIS with source provenance in notes
- CSV matrix

New MCP tool:

```json
{
  "name": "convert_citation_records",
  "description": "Parse RIS, BibTeX, NBIB, or CSV citation records, deduplicate them, and export a selected citation format."
}
```

Input schema:

- `content`: string
- `input_format`: `ris`, `bibtex`, `nbib`, or `csv`
- `output_format`: `ris`, `bibtex`, `gbt7714`, or `csv`
- `include_provenance`: boolean, default true

Test cases:

```python
def test_parse_ris_to_records():
    # Minimal RIS with DOI and title becomes one record.

def test_parse_bibtex_to_records():
    # Minimal @article becomes one record.

def test_convert_citation_records_deduplicates_before_export():
    # Duplicate DOI in RIS and BibTeX exports once.

def test_convert_citation_records_rejects_unknown_format():
    # Raises ValueError with machine-readable MCP invalid params.

def test_export_csl_json_preserves_doi_title_year_and_source_notes():
    # CSL JSON output keeps core metadata and provenance notes.

def test_export_jsonl_outputs_one_record_per_line():
    # JSONL output is parseable line by line.
```

### Task 3.5: Expand MCP Server Tool Surface

Owned files:

- `server.py`
- `service.py`
- `tests/test_mcp_contract.py`
- `tests/test_service.py`

Add or update tools:

- `search_civil_materials`: keep backward compatible.
- `fetch_paper_metadata`: accept DOI, title, PMID, arXiv ID, Scopus EID, PII.
- `search_academic_sources`: explicit multi-source search with `sources` list.
- `convert_citation_records`: parse, deduplicate, and export.
- `deduplicate_citation_records`: return merged records and duplicate report.
- `resolve_paper_ids`: normalize and merge DOI/PMID/PMCID/arXiv/OpenAlex/S2/Scopus/PII identifiers.
- `list_academic_sources`: return configured, disabled, and key-required source status.
- `lookup_mesh`: unchanged.
- `suggest_search_queries`: unchanged.

Tool notes must say:

- candidate search records are not deep-read evidence;
- disabled optional sources are reported as warnings, not fatal errors;
- Elsevier-backed sources require user-provided API keys;
- WER-EA claims still require reader evidence anchors.

### Task 3.6: Documentation, Manifest, And Release Gate

Owned files:

- `references/expanded-academic-search.md`
- `references/academic-search-mcp.md`
- `mcp/academic_search/README.md`
- `manifest.yaml`
- `SKILL.md`
- `scripts/run_release_checks.py`
- Matching plugin mirror files.

Steps:

- [ ] Document all sources, required keys, disabled-source behavior, ID conversion, and citation file conversion.
- [ ] Add manifest routes for `multi-source-search`, `citation-file-conversion`, `deduplication`, `id-conversion`, and `expanded-source-screening`.
- [ ] Add release check bucket `academic_search_expanded_sources` proving new adapters exist and mocked tests pass.

Verification:

```powershell
python -m unittest discover -s skills\civil-materials-citation\mcp\academic_search\tests -v
python scripts\run_release_checks.py --json
```

Acceptance criteria for Pillar 3:

- arXiv works without keys.
- Scopus and ScienceDirect gracefully disable without keys.
- Mocked Scopus/ScienceDirect tests prove parsing and request construction.
- Service layer can search selected sources and report source warnings.
- Citation file conversion works for RIS/BibTeX/NBIB/CSV.
- Deduplication preserves source provenance and WER-EA evidence classification.

---

## Pillar 4: WER-EA Figure Asset Library Final Plan

### Purpose

Build a domain-specific WER-EA figure atlas that does for waterborne epoxy modified emulsified asphalt what nature-figure does for generic high-impact figures: reusable visual patterns, scripts, templates, example packages, QA rules, and reviewer-safe caption boundaries.

### Final Asset Library Contract

The library must include at least these figure families:

1. WER-EA mechanism map.
2. Evidence heatmap.
3. Material-system/formulation map.
4. Performance-mechanism boundary map.
5. Literature-screening flow.
6. Graphical abstract.
7. Dosage-workability-performance window.
8. Emulsion stability timeline.
9. Curing/demulsification sequence.
10. Bonding performance comparison.
11. Pull-off/shear method comparison.
12. Rheology-performance link.
13. FTIR peak assignment card.
14. SEM/fluorescence image plate.
15. Durability retention map.
16. Water/aging/freeze-thaw challenge map.
17. Test standard and condition card.
18. Construction application workflow.
19. Sustainability/LCA boundary card.
20. Research gap matrix.

Every asset must have:

- `asset_id`
- `family`
- `review_use`
- `panel_structure`
- `required_evidence`
- `claim_boundary`
- `caption_pattern`
- `source_learning_basis`
- `certainty_encoding`
- `source_data_template`
- `script`
- `exports`
- `qa_status`

### Files

Modify:

- `skills/civil-materials-figure/SKILL.md`
- `skills/civil-materials-figure/README.md`
- `skills/civil-materials-figure/manifest.yaml`
- `skills/civil-materials-figure/references/wer-ea-review-figure-contract.md`
- `skills/civil-materials-figure/references/visual-asset-roadmap.md`
- `skills/civil-materials-figure/references/figure-gallery.md`
- `skills/civil-materials-figure/tests/test_review_assets.py`
- `scripts/run_release_checks.py`
- Matching plugin mirror files.

Create:

- `skills/civil-materials-figure/references/wer-ea-figure-atlas.md`
- `skills/civil-materials-figure/assets/wer-ea-atlas/asset-specs.csv`
- `skills/civil-materials-figure/assets/wer-ea-atlas/data/*.csv`
- `skills/civil-materials-figure/assets/wer-ea-atlas/generated/*.svg`
- `skills/civil-materials-figure/assets/wer-ea-atlas/generated/*.png`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/generate_atlas.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_mechanism_map.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_evidence_heatmap.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_material_system_map.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_performance_mechanism_boundary.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_literature_screening_flow.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_graphical_abstract.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_dosage_window.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_durability_retention.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_characterization_panel.py`
- `skills/civil-materials-figure/scripts/wer_ea_atlas/plot_construction_workflow.py`
- `skills/civil-materials-figure/tests/test_wer_ea_atlas.py`
- Matching plugin mirror files.

### Task 4.1: Define Atlas Reference And Asset Spec Schema

Owned files:

- `references/wer-ea-figure-atlas.md`
- `assets/wer-ea-atlas/asset-specs.csv`
- Matching plugin mirror files.

Steps:

- [ ] Write `wer-ea-figure-atlas.md` with one section per figure family.
- [ ] For each family, define scientific purpose, required evidence, visual encoding, caption boundary, and reviewer risk.
- [ ] Create `asset-specs.csv` with the full required schema.
- [ ] Migrate or cross-reference existing `assets/review-first/asset-specs.csv` entries without deleting useful current assets.
- [ ] Mark all example assets as template-only unless source data are provided.

Verification:

```powershell
Select-String -Path skills\civil-materials-figure\references\wer-ea-figure-atlas.md -Pattern 'mechanism map','evidence heatmap','graphical abstract','caption boundary'
```

### Task 4.2: Add Atlas Data Templates

Owned files:

- `assets/wer-ea-atlas/data/*.csv`
- Matching plugin mirror files.

Required data templates:

- `mechanism_edges.csv`: `edge_id,from_node,to_node,evidence_layer,certainty_tier,source_anchor,caption_boundary`
- `evidence_heatmap.csv`: `paper_id,evidence_layer,certainty_tier,source_role,reviewer_risk`
- `material_systems.csv`: `system_id,asphalt_type,emulsifier,epoxy_type,curing_agent,dosage_range,preparation_route`
- `performance_boundary.csv`: `claim_id,performance_metric,mechanism_evidence,certainty_tier,boundary_note`
- `screening_flow.csv`: `stage,input_count,output_count,exclusion_reason,source_anchor`
- `dosage_window.csv`: `formulation_id,wer_dosage,viscosity,bonding_strength,storage_stability,workability_flag`
- `durability_retention.csv`: `condition,baseline_value,conditioned_value,retention_percent,protocol`
- `characterization_panel.csv`: `panel_id,method,signal_or_image,source_anchor,interpretation_boundary`
- `construction_workflow.csv`: `step_id,operation,control_variable,quality_check,field_relevance`
- `lca_boundary.csv`: `boundary_id,functional_unit,system_boundary,inventory_basis,comparison_limit`
- `research_gap_matrix.csv`: `gap_id,evidence_layer,available_evidence,missing_evidence,reviewer_risk`

Verification:

```powershell
Get-ChildItem skills\civil-materials-figure\assets\wer-ea-atlas\data\*.csv | Measure-Object
```

Expected: at least 9 CSV templates.

### Task 4.3: Add Reusable Atlas Plot Scripts

Owned files:

- `scripts/wer_ea_atlas/*.py`
- Matching plugin mirror files.

Shared helper behavior:

- Use deterministic sample data.
- Export SVG and PNG for every plot.
- Keep text editable in SVG when possible.
- Include visual legend for `measured`, `inferred`, `speculative`, `missing`.
- Include caption boundary in generated card metadata, not necessarily in the plotted image.
- Never claim the generated examples are experimental evidence.

Shared CLI:

```powershell
python skills\civil-materials-figure\scripts\wer_ea_atlas\generate_atlas.py --output-dir skills\civil-materials-figure\assets\wer-ea-atlas\generated --json
```

Expected JSON:

```json
{
  "status": "pass",
  "generated": [
    {"asset_id": "wer-ea-mechanism-map", "svg": "...", "png": "..."}
  ],
  "warnings": []
}
```

### Task 4.4: Add Atlas Tests And Visual QA

Owned files:

- `tests/test_wer_ea_atlas.py`
- Matching plugin mirror file.

Test cases:

```python
def test_wer_ea_atlas_spec_contains_required_families():
    # Assert at least 20 rows and all required families exist.

def test_wer_ea_atlas_data_templates_have_required_headers():
    # Assert every data CSV has exact required columns.

def test_generate_atlas_creates_svg_and_png_outputs(tmp_path):
    # Run generate_atlas.py into tmp_path.
    # Assert expected count, non-empty SVG, readable PNG dimensions.

def test_generated_assets_include_certainty_legend(tmp_path):
    # Parse SVG text and assert measured/inferred/speculative/missing appear.

def test_atlas_assets_are_mirrored_into_plugin():
    # Compare root and plugin atlas specs/scripts/generated examples.
```

Verification:

```powershell
python -m unittest skills\civil-materials-figure\tests\test_wer_ea_atlas.py -v
```

### Task 4.5: Wire Atlas Into Figure Skill And Release Gate

Owned files:

- `SKILL.md`
- `README.md`
- `manifest.yaml`
- `references/wer-ea-review-figure-contract.md`
- `scripts/run_release_checks.py`
- Matching plugin mirror files.

Steps:

- [ ] Add `wer-ea-figure-atlas` route to manifest.
- [ ] Add trigger text for WER-EA figure atlas, mechanism map, evidence heatmap, graphical abstract, dosage window, durability map, and review figure library.
- [ ] Update README gallery section with atlas structure and sample command.
- [ ] Add release bucket `wer_ea_asset_library` checking spec rows, required families, generator smoke run, and generated asset readability.

Verification:

```powershell
python -m unittest discover -s skills\civil-materials-figure\tests -v
python scripts\run_release_checks.py --json
```

Acceptance criteria for Pillar 4:

- WER-EA atlas has at least 20 figure families with evidence boundaries.
- Data templates exist for the major figure families.
- Generator creates non-empty SVG and readable PNG outputs.
- Every generated example is marked template-only unless source data are provided.
- Figure skill manifest routes WER-EA atlas requests.
- Release gate proves the atlas remains intact.

---

## Integration And Subagent Execution Map

### Recommended Subagent Split

Run these workers in parallel only after this plan is accepted as the source of truth. Each worker owns disjoint files where possible.

1. **Architecture worker**
   - Owns: `docs/architecture/*`, `scripts/check_skill_architecture.py`, `tests/test_skill_architecture_contract.py`, manifest/static-core normalization.
   - Does not edit: academic-search adapters or figure atlas scripts.

2. **Reader package worker**
   - Owns: `skills/civil-materials-reader/**`, plugin reader mirror, reader-specific release checks.
   - Does not edit: citation MCP or figure atlas scripts except handoff field coordination in docs.

3. **Academic-search worker**
   - Owns: `skills/civil-materials-citation/mcp/academic_search/**`, citation MCP docs, citation-specific release checks.
   - Does not edit: reader package builder or figure atlas scripts.

4. **WER-EA atlas worker**
   - Owns: `skills/civil-materials-figure/assets/wer-ea-atlas/**`, `scripts/wer_ea_atlas/**`, figure atlas docs/tests, plugin mirror.
   - Does not edit: citation MCP internals or reader package scripts.

5. **Integration worker**
   - Owns: `README.md`, `docs/skills-index.md`, `scripts/run_release_checks.py`, root/plugin mirror audit, final test command run.
   - Must wait until the four pillar workers finish.

### Conflict Rules

- If two workers need to touch `scripts/run_release_checks.py`, each should add a local helper function and clearly mark the issue bucket it owns. Integration worker reconciles ordering and JSON shape.
- If two workers need to touch shared handoff field names, use these canonical fields:
  - `claim_id`
  - `source_anchor`
  - `source_location`
  - `original_excerpt`
  - `evidence_layer`
  - `evidence_type`
  - `source_role`
  - `source_quality`
  - `certainty_tier`
  - `caption_boundary`
  - `figure_handoff`
  - `reviewer_risk`
- No worker may delete existing examples, generated gallery assets, or tests to make new tests pass.

### Final Completion Audit

Before marking the upgrade complete, the controller must verify:

- Pillar 1: architecture checker passes and release gate has architecture buckets.
- Pillar 2: reader builder and auditor pass in a temp directory.
- Pillar 3: all citation MCP tests pass with optional sources disabled and mocked source tests passing.
- Pillar 4: WER-EA atlas generator creates SVG/PNG outputs and atlas tests pass.
- Root/plugin mirror identity is checked for all changed files.
- `outputs/wer-ea-30-reading-sample/` remains ignored.
- No new secrets or local absolute paths are introduced.

Final commands:

```powershell
python -m unittest tests\test_skill_architecture_contract.py -v
python -m unittest discover -s skills\civil-materials-reader\tests -v
python -m unittest discover -s skills\civil-materials-citation\mcp\academic_search\tests -v
python -m unittest discover -s skills\civil-materials-figure\tests -v
python scripts\check_skill_architecture.py --json
python scripts\run_release_checks.py --json
git diff --check
git status --short --branch --ignored -- outputs\wer-ea-30-reading-sample
```

---

## Self-Review

Spec coverage:

- Unified architecture: covered by Pillar 1 tasks, checker, docs, release buckets, and manifest/static-core normalization.
- Reader standard output package: covered by Pillar 2 reference, templates, builder, auditor, tests, and release gate.
- Academic-search expansion: covered by Pillar 3 arXiv, Scopus, ScienceDirect, ID conversion, citation file conversion, MCP tools, tests, and disabled-source behavior.
- WER-EA figure asset library: covered by Pillar 4 atlas reference, asset specs, data templates, scripts, generated assets, visual QA tests, and release gate.
- Subagent execution: covered by integration map and conflict rules.

Placeholder scan:

- No `TBD`, `TODO`, `implement later`, or undefined "appropriate tests" placeholders are used.

Type and naming consistency:

- Handoff fields are canonicalized in the integration section.
- Release buckets use stable names: `skill_architecture`, `reader_standard_package`, `academic_search_expanded_sources`, and `wer_ea_asset_library`.

