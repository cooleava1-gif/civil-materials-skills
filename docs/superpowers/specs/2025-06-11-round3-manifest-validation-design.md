# Round 3: Manifest Validation CLI + Release Check Hardening

**Date:** 2025-06-11
**Based on:** Round 1 (fragment architecture) + Round 2 (handoff contracts)

## 1. What & Why

**Problem:** Manifests can silently rot — fragment files get renamed but manifest paths don't update, triggers become stale, fragments become orphaned.

**Solution:** A deterministic validation CLI that checks every manifest.yaml for structural integrity, plus integration into release checks.

## 2. Validation CLI (`scripts/validate_manifest.py`)

```bash
python scripts/validate_manifest.py                    # all skills
python scripts/validate_manifest.py --skill reader     # one skill
python scripts/validate_manifest.py --json             # JSON output
```

### Checks

| # | Check | What it validates |
|---|---|---|
| 1 | **Path existence** | Every `path:` in axes.values, always_load, references.on_demand, assets, scripts exists |
| 2 | **No orphan fragments** | Every file under `static/fragments/` is referenced by at least one axis value |
| 3 | **Trigger non-empty** | Every axis value has >=2 trigger words/phrases |
| 4 | **Trigger collision** | No two values in the same axis share the same trigger word |
| 5 | **Contract reference** | Every `contract:` path in handoffs.provides exists |
| 6 | **Template existence** | Every template listed in handoff contracts exists |
| 7 | **No dangling references** | Every `references/` file listed in manifest is referenced by an axis or on_demand |

## 3. Integration

`run_release_checks.py --json` calls `validate_manifest.py` for all skills.

## 4. Scope

- 1 new script: `scripts/validate_manifest.py`
- Integration in `run_release_checks.py`
- Tests for the validator
- Optionally: fix any existing issues found by the validator
