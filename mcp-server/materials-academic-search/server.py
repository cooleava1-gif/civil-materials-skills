#!/usr/bin/env python3
"""FastMCP-based MCP server for materials academic search."""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

# Ensure package is importable when run directly
if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.fastmcp import FastMCP

from academic_search.service import AcademicSearchService

logger = logging.getLogger("materials-academic-search")
service = AcademicSearchService()
mcp = FastMCP("materials-academic-search")


def _r(service_result: dict[str, Any]) -> str:
    """Wrap service result as JSON string for MCP text content."""
    return json.dumps(service_result, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# Tool: list_academic_sources
# ──────────────────────────────────────────────
@mcp.tool()
def list_academic_sources() -> str:
    """List enabled and disabled academic metadata sources, including optional API-key gated sources."""
    return _r(service.list_academic_sources({}))


# ──────────────────────────────────────────────
# Tool: resolve_paper_ids
# ──────────────────────────────────────────────
@mcp.tool()
def resolve_paper_ids(
    doi: str | None = None,
    pmid: str | None = None,
    pmcid: str | None = None,
    arxiv: str | None = None,
    openalex: str | None = None,
    semantic_scholar: str | None = None,
    scopus_eid: str | None = None,
    pii: str | None = None,
) -> str:
    """Normalize DOI, PMID, PMCID, arXiv, OpenAlex, Semantic Scholar, Scopus EID, or ScienceDirect PII identifiers."""
    return _r(service.resolve_paper_ids({
        k: v for k, v in locals().items() if v is not None
    }))


# ──────────────────────────────────────────────
# Tool: convert_citation_records
# ──────────────────────────────────────────────
@mcp.tool()
def convert_citation_records(
    content: str,
    input_format: str = "ris",
    output_format: str = "csl-json",
    deduplicate: bool = True,
) -> str:
    """Parse RIS, BibTeX, NBIB, or CSV records and export to another format."""
    return _r(service.convert_citation_records({
        "content": content,
        "input_format": input_format,
        "output_format": output_format,
        "deduplicate": deduplicate,
    }))


# ──────────────────────────────────────────────
# Tool: deduplicate_citation_records
# ──────────────────────────────────────────────
@mcp.tool()
def deduplicate_citation_records(
    records: list[dict[str, Any]] | None = None,
    content: str | None = None,
    input_format: str = "ris",
) -> str:
    """Deduplicate citation records by DOI, external IDs, then normalized title and year."""
    args: dict[str, Any] = {"input_format": input_format}
    if records is not None:
        args["records"] = records
    if content is not None:
        args["content"] = content
    return _r(service.deduplicate_citation_records(args))


# ──────────────────────────────────────────────
# Tool: search_civil_materials
# ──────────────────────────────────────────────
@mcp.tool()
def search_civil_materials(
    topic: str,
    journal_family: str | list[str] | None = None,
    material_domain: str = "asphalt",
    evidence_layer: str | None = None,
    year_range: str | None = None,
    limit: int = 10,
) -> str:
    """Search scholarly sources for civil engineering and construction-materials papers."""
    args: dict[str, Any] = {"topic": topic, "material_domain": material_domain, "limit": limit}
    if journal_family:
        args["journal_family"] = journal_family
    if evidence_layer:
        args["evidence_layer"] = evidence_layer
    if year_range:
        args["year_range"] = year_range
    return _r(service.search_civil_materials(args))


# ──────────────────────────────────────────────
# Tool: fetch_paper_metadata
# ──────────────────────────────────────────────
@mcp.tool()
def fetch_paper_metadata(
    doi: str | None = None,
    title: str | None = None,
    external_id: str | None = None,
    openalex_id: str | None = None,
    semantic_scholar_id: str | None = None,
) -> str:
    """Resolve DOI, title, year, journal, author, abstract, and source metadata for one paper."""
    return _r(service.fetch_paper_metadata({
        k: v for k, v in locals().items() if v is not None
    }))


# ──────────────────────────────────────────────
# Tool: suggest_search_queries
# ──────────────────────────────────────────────
@mcp.tool()
def suggest_search_queries(
    topic: str,
    journal_family: str | list[str] | None = None,
    material_domain: str = "asphalt",
    evidence_layer: str | None = None,
    year_range: str | None = None,
    limit: int = 6,
) -> str:
    """Generate CBM/CCC/JBE/RMPD-aware Boolean search queries."""
    args: dict[str, Any] = {"topic": topic, "material_domain": material_domain, "limit": limit}
    if journal_family:
        args["journal_family"] = journal_family
    if evidence_layer:
        args["evidence_layer"] = evidence_layer
    if year_range:
        args["year_range"] = year_range
    return _r(service.suggest_search_queries(args))


# ──────────────────────────────────────────────
# Tool: lookup_mesh
# ──────────────────────────────────────────────
@mcp.tool()
def lookup_mesh(topic: str, limit: int = 10) -> str:
    """Look up PubMed MeSH terms for a materials or chemistry topic."""
    return _r(service.lookup_mesh({"topic": topic, "limit": limit}))


# ──────────────────────────────────────────────
# Tool: build_claim_source_map
# ──────────────────────────────────────────────
@mcp.tool()
def build_claim_source_map(
    topic: str | None = None,
    claims: list[str] | None = None,
    text: str | None = None,
    candidate_records: list[dict[str, Any]] | None = None,
    journal_family: str | list[str] | None = None,
    material_domain: str = "asphalt",
    year_range: str | None = None,
) -> str:
    """Map manuscript claims to evidence type, search query, candidate sources, and reviewer risk."""
    args: dict[str, Any] = {"material_domain": material_domain}
    if topic:
        args["topic"] = topic
    if claims:
        args["claims"] = claims
    if text:
        args["text"] = text
    if candidate_records:
        args["candidate_records"] = candidate_records
    if journal_family:
        args["journal_family"] = journal_family
    if year_range:
        args["year_range"] = year_range
    return _r(service.build_claim_source_map(args))


# ──────────────────────────────────────────────
# Tool: audit_reference_gaps
# ──────────────────────────────────────────────
@mcp.tool()
def audit_reference_gaps(
    claims: list[str] | None = None,
    text: str | None = None,
    claim_source_map: list[dict[str, Any]] | None = None,
    candidate_records: list[dict[str, Any]] | None = None,
) -> str:
    """Flag missing mechanism, performance, durability, and reviewer-safe source evidence."""
    args: dict[str, Any] = {}
    if claims:
        args["claims"] = claims
    if text:
        args["text"] = text
    if claim_source_map:
        args["claim_source_map"] = claim_source_map
    if candidate_records:
        args["candidate_records"] = candidate_records
    return _r(service.audit_reference_gaps(args))


# ──────────────────────────────────────────────
# Tool: export_citation_matrix
# ──────────────────────────────────────────────
@mcp.tool()
def export_citation_matrix(
    topic: str | None = None,
    claims: list[str] | None = None,
    target_journals: str | list[str] | None = None,
    journal_family: str | list[str] | None = None,
    material_domain: str = "asphalt",
    year_range: str | None = None,
    manuscript_location: str | None = None,
) -> str:
    """Export rows compatible with the materials citation matrix template."""
    args: dict[str, Any] = {"material_domain": material_domain}
    if topic:
        args["topic"] = topic
    if claims:
        args["claims"] = claims
    if target_journals:
        args["target_journals"] = target_journals
    if journal_family:
        args["journal_family"] = journal_family
    if year_range:
        args["year_range"] = year_range
    if manuscript_location:
        args["manuscript_location"] = manuscript_location
    return _r(service.export_citation_matrix(args))


# ──────────────────────────────────────────────
# Tool: get_formatted_citation
# ──────────────────────────────────────────────
@mcp.tool()
def get_formatted_citation(
    doi: str | None = None,
    dois: list[str] | None = None,
    format: str = "ris",
    records: list[dict[str, Any]] | None = None,
) -> str:
    """Generate formatted citation strings or export files for papers by DOI."""
    args: dict[str, Any] = {"format": format}
    if doi:
        args["doi"] = doi
    if dois:
        args["dois"] = dois
    if records:
        args["records"] = records
    return _r(service.get_formatted_citation(args))


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
def main() -> int:
    """Run the MCP server over stdio."""
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
