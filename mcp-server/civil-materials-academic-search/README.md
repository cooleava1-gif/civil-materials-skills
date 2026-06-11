# Civil Materials Academic Search — MCP Server

FastMCP-based MCP server for civil engineering and construction-materials literature search.

## Tools (12)

| Tool | Description |
|---|---|
| `list_academic_sources` | List enabled/disabled sources (CrossRef, PubMed, arXiv, Scopus, etc.) |
| `search_civil_materials` | Search for papers with journal family and material domain filters |
| `fetch_paper_metadata` | Resolve DOI/title to full metadata |
| `resolve_paper_ids` | Normalize identifiers across all supported sources |
| `suggest_search_queries` | Generate CBM/CCC/JBE/RMPD-aware Boolean search queries |
| `lookup_mesh` | Look up PubMed MeSH terms for civil-materials topics |
| `convert_citation_records` | Convert between RIS, BibTeX, CSL JSON, GB/T 7714 formats |
| `deduplicate_citation_records` | Deduplicate records by DOI and title |
| `build_claim_source_map` | Map manuscript claims to evidence sources |
| `audit_reference_gaps` | Flag missing evidence types |
| `export_citation_matrix` | Export rows compatible with citation matrix template |
| `get_formatted_citation` | Generate formatted citations (APA/Nature/IEEE/RIS/BibTeX) |

## Sources

- **CrossRef** — open metadata (no API key needed)
- **PubMed / MeSH** — biomedical and chemistry-adjacent (no API key needed)
- **arXiv** — open e-prints (no API key needed)
- **OpenAlex** — open scholarly index (no API key needed)
- **Semantic Scholar** — AI-powered academic search (optional API key for higher rate limits)
- **Scopus** — Elsevier abstract database (optional API key)
- **ScienceDirect** — Elsevier full-text platform (optional API key)

## Quick Start

### Register with Claude Code or Codex

The `.mcp.json` at the repo root registers this server automatically.

### Manual test

```powershell
python server.py
```

Then send from another terminal:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"0.1.0"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

### Run tests

```bash
python -m unittest discover -s academic_search/tests -p "test_*.py" -v
```

## Environment Variables (all optional)

- `OPENALEX_API_KEY` — enables OpenAlex searches
- `SEMANTIC_SCHOLAR_API_KEY` — higher rate limits for Semantic Scholar
- `CIVIL_MATERIALS_CONTACT_EMAIL` — polite Crossref requests
- `NCBI_API_KEY` — higher PubMed E-utilities rate limits
