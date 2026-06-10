# Civil Materials Skills

Civil Materials Skills is a Codex skill bundle for civil engineering and construction-materials research. It is adapted for asphalt pavement materials, waterborne epoxy modified emulsified asphalt, cement/concrete, durability, sustainability, journal targeting, literature work, manuscript writing, figures, PPTX, data/FAIR packaging, and reviewer responses.

## Included Skills

| Skill | Purpose |
|---|---|
| `civil-materials-research` | Research router, topic positioning, manuscript strategy, journal fit, pressure tests, example library |
| `civil-materials-reader` | Evidence-chain reading, source-map anchors, citation/figure handoffs |
| `civil-materials-citation` | Literature search planning, WER-EA source screening, citation matrices, expanded academic-search MCP |
| `civil-materials-writing` | From-scratch manuscript drafting, argument chains, section writing, and review-paper outlines |
| `civil-materials-polishing` | English polishing, Chinese-to-English academic rewriting, claim-strength control |
| `civil-materials-response` | Reviewer response packages and point-by-point rebuttal drafting |
| `civil-materials-reviewer` | Simulated peer review reports and pre-submission referee-risk audits |
| `civil-materials-paper2ppt` | Paper-to-PPT outlines and slide-ready Markdown |
| `civil-materials-pptx` | Real `.pptx` generation from structured outlines |
| `civil-materials-figure` | Figure planning, review-figure intake, WER-EA atlas, SVG demos, caption boundaries |
| `civil-materials-data` | Dataset packages, metadata, FAIR audits, data availability statements |

## Skill Status Index

For fuller human-readable routing notes, see [docs/skills-index.md](docs/skills-index.md).

| Module | Maturity | Scripts | Tests | Typical input | Typical product |
|---|---|---|---|---|---|
| `civil-materials-research` | Stable router | Yes | Yes | Research idea, journal target, manuscript task | Route, topic angle, risk map, workflow plan |
| `civil-materials-reader` | Stable production skill | Yes | Yes | PDF/text, paper notes, figure caption | Standard reader package, evidence-chain matrix, citation/figure handoff |
| `civil-materials-citation` | Stable MCP-backed skill | Yes | Yes | Topic, claim list, candidate sources | Search plan, screened citation matrix, reference gaps, ID/citation conversion |
| `civil-materials-writing` | Stable production skill | Yes | Yes | Claims, results, outline, Chinese draft | Manuscript section, review outline, argument chain |
| `civil-materials-polishing` | Stable production skill | Yes | Yes | English draft, Chinese academic paragraph | Polished text, claim-strength audit |
| `civil-materials-response` | Stable production skill | Yes | Yes | Reviewer comments, revision notes | Point-by-point response, rebuttal package |
| `civil-materials-reviewer` | Stable audit skill | Yes | Yes | Manuscript draft, abstract, figures | Simulated review, desk-reject risk report |
| `civil-materials-paper2ppt` | Stable handoff skill | Yes | Yes | Paper notes, review matrix, outline | Slide-ready Markdown, talk structure |
| `civil-materials-pptx` | Stable generation skill | Yes | Yes | PPTX-ready Markdown or JSON | Real `.pptx` deck |
| `civil-materials-figure` | Stable production skill | Yes | Yes | Data table, reader/citation handoff, figure idea | Figure plan, review-figure intake, WER-EA atlas, SVG/PNG package, caption boundary |
| `civil-materials-data` | Stable FAIR skill | Yes | Yes | Raw/processed data, metadata needs | FAIR package, data availability statement |

## Install

### Codex plugin

Install the repo-local marketplace:

```powershell
codex plugin marketplace add https://github.com/cooleava1-gif/civil-materials-skills.git --ref main
codex plugin add civil-materials-skills@civil-materials-skills
```

The plugin package includes the `civil-materials-*` skills, the required `_shared` folder, and the academic-search MCP config.

### Manual skills install

Run the local installer:

```powershell
.\scripts\install.ps1
```

The installer copies both the `civil-materials-*` skill folders and the required `_shared` folder. If `CODEX_HOME` is not set, it installs to `~\.codex\skills`.

Manual install:

```powershell
$skillsDir = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex\skills" }
New-Item -ItemType Directory -Force $skillsDir | Out-Null
Copy-Item -Recurse -Force .\skills\civil-materials-* $skillsDir
Copy-Item -Recurse -Force .\skills\_shared $skillsDir
```

The `_shared` directory is required because multiple skill manifests load shared stance, ethics, evidence-contract, claim-strength, terminology, and journal-format files through `../_shared/...` paths.

## Optional Academic Search MCP

The citation skill includes a local academic-search MCP server.

Install the Python dependency first:

```powershell
python -m pip install -r .\requirements.txt
```

Example Codex config:

```toml
[mcp_servers."civil-materials-academic-search"]
command = "python"
args = ["$CODEX_HOME/skills/civil-materials-citation/mcp/academic_search/server.py"]
```

Optional environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `CIVIL_MATERIALS_CONTACT_EMAIL`
- `NCBI_API_KEY`

The MCP can search Crossref, PubMed, OpenAlex, and Semantic Scholar. It also exposes `lookup_mesh` for PubMed MeSH term checks.

The expanded MCP layer also includes optional arXiv, Scopus, and ScienceDirect adapters, plus DOI/PMID/PMCID/arXiv/OpenAlex/Semantic Scholar/Scopus EID/PII normalization and RIS/BibTeX/NBIB/CSV conversion to RIS, BibTeX, GB/T 7714, CSL JSON, or JSONL. Scopus and ScienceDirect are disabled with warnings unless the relevant API keys are configured.

## Architecture

The final skill architecture is documented in [docs/architecture/skill-architecture.md](docs/architecture/skill-architecture.md), and release gate coverage is documented in [docs/architecture/release-gate-contract.md](docs/architecture/release-gate-contract.md).

## Evidence-To-Review Pipeline

The upgraded reader-citation-figure path supports WER-EA mini-review work:

1. `civil-materials-reader` creates a standard reader package with source anchors, citation handoff rows, figure handoff rows, QA report, and optional Obsidian note.
2. `civil-materials-citation` screens candidate sources by WER-EA evidence layer, source role, source quality, reviewer risk, and normalized scholarly IDs.
3. `civil-materials-figure` consumes handoff rows for review-figure intake and WER-EA atlas templates, keeping measured, inferred, speculative, and missing evidence visually separate.

No secrets or local Codex config files are included in this repository.

## Verify

Run the release check script:

```powershell
python .\scripts\run_release_checks.py
```

The script checks core tests, pressure-test coverage, generated-artifact cleanup, and accidental local-path or secret leakage.

## Scope

This bundle helps structure research work. It does not replace deep reading, experimental evidence, supervisor/co-author judgment, official journal instructions, or ethical/institutional requirements.

## License

MIT License. See [LICENSE](LICENSE).
