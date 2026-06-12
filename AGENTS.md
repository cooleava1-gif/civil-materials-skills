# Materials Science Skills

Full-cycle Codex skill bundle for civil engineering and construction-materials research. Routes work across research, citation, reader, writing, figure, data, polishing, reviewer, response, paper-to-PPT, and PPTX generation.

## Project

- **Stack**: Python 3.11+, skill manifests in YAML, tests with `unittest`
- **Entry**: any of 11 `materials-*` skills; start with `materials-research` for workflow routing
- **Plugin mirror**: `plugins/materials-skills/` — installed package mirrored from `skills/`

## Commands

| Purpose | Command |
|---|---|
| **All skill tests** | `python -m unittest discover -s skills/<skill>/tests -p "test_*.py" -v` |
| **Citation MCP tests** | `python -m unittest discover -s skills/materials-citation/mcp/academic_search/tests -p "test_*.py" -v` |
| **Root contract tests** | `python -m unittest discover -s tests -p "test_*.py" -v` |
| **Full suite** | iterate 11 skills + citation MCP + root tests (201 tests total) |
| **Release checks** | `python scripts/run_release_checks.py --json` |
| **Install** | `.\scripts\install.ps1` (Windows PowerShell) |

## Architecture

- **11 skill modules** under `skills/materials-*/`, each with `SKILL.md`, `manifest.yaml`, `tests/`, and `scripts/`
- **_shared/** — cross-skill assets: `core/` (stance, contract, ethics), `journal-formats/` (CBM, CCC, JBE, RMPD), `paper-production/` (routing, gate report, weakness templates)
- **`manifest.yaml`** — skill's routing axes with `always_load`, `detect` triggers, and fragment paths
- **Output handoffs** — standardized CSV/MD artifacts: `reader-package`, `citation_handoff.csv`, `figure_handoff.csv`, gate reports, review assets
- **scripts/** — `run_release_checks.py`, `install.ps1`, figure generators, pressure tests
- **docs/** — workflow demos (4 routes), gallery, showcases, architecture docs
- **plugins/** — Codex plugin mirror of the source tree

## Conventions

- Each skill has a `manifest.yaml` (routing axes + `always_load` + `value` groups) and `SKILL.md` (trigger + protocol + gates)
- Test files: `test_*.py` in `tests/` per skill, using `unittest.TestCase`
- Citation MCP tests live under `mcp/academic_search/tests/` — separate discovery path
- Handoff contract references: `static/core/contract.md` defines output fields and QA gates
- No data files committed for real papers — use synthetic/example data
- Paths in scripts use `pathlib.Path`; prefer relative to repo root

## Notes

- 201 tests total: 107 skill tests + 77 citation MCP tests — all pass
- Dependencies: `httpx`, `matplotlib`, `numpy`, `pillow`, `pymupdf`
- Latest commit: `b62df97` — feat: nature-skills alignment
- Release checks validate: file presence, manifest validity, figure packages, paper-production templates
