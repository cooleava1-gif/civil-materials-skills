import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.domain.identifiers import (
    deduplicate_records,
    merge_external_ids,
    normalize_arxiv_id,
    normalize_doi,
    normalize_openalex_id,
    normalize_pii,
    normalize_pmcid,
    normalize_pmid,
    normalize_scopus_eid,
    normalize_semantic_scholar_id,
)


class IdentifierTest(unittest.TestCase):
    def test_identifier_normalizers_handle_urls_and_prefixed_ids(self):
        self.assertEqual(normalize_doi("https://doi.org/10.1016/J.CBM.2025.01.001"), "10.1016/j.cbm.2025.01.001")
        self.assertEqual(normalize_pmid("PMID: 12345678"), "12345678")
        self.assertEqual(normalize_pmcid("pmc1234567"), "PMC1234567")
        self.assertEqual(normalize_arxiv_id("https://arxiv.org/abs/2401.12345v2"), "2401.12345v2")
        self.assertEqual(normalize_openalex_id("https://openalex.org/W12345"), "W12345")
        self.assertEqual(normalize_semantic_scholar_id("SemanticScholar:ABCDEF"), "ABCDEF")
        self.assertEqual(normalize_scopus_eid("eid:2-s2.0-85123456789"), "2-s2.0-85123456789")
        self.assertEqual(normalize_pii("pii:S0950061824012345"), "S0950061824012345")

    def test_merge_external_ids_normalizes_known_id_fields(self):
        ids = merge_external_ids(
            [
                {"doi": "10.1000/ABC", "external_ids": {"PMID": "PMID: 123", "arxiv": "arXiv:2401.12345v1"}},
                {"external_ids": {"OpenAlex": "https://openalex.org/W123", "ScopusEID": "2-s2.0-123"}},
                {"external_ids": {"PII": "S0950061824012345", "SemanticScholar": "abc"}},
            ]
        )

        self.assertEqual(ids["doi"], "10.1000/abc")
        self.assertEqual(ids["pmid"], "123")
        self.assertEqual(ids["arxiv"], "2401.12345v1")
        self.assertEqual(ids["openalex"], "W123")
        self.assertEqual(ids["semantic_scholar"], "abc")
        self.assertEqual(ids["scopus_eid"], "2-s2.0-123")
        self.assertEqual(ids["pii"], "S0950061824012345")

    def test_deduplicate_records_prefers_doi_then_external_ids(self):
        records = deduplicate_records(
            [
                {
                    "title": "Waterborne epoxy asphalt",
                    "doi": "10.1000/ABC",
                    "source": "Crossref",
                    "external_ids": {"doi": "10.1000/ABC"},
                },
                {
                    "title": "Waterborne epoxy asphalt",
                    "doi": "https://doi.org/10.1000/abc",
                    "source": "scopus",
                    "external_ids": {"scopus_eid": "2-s2.0-123"},
                },
            ]
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["external_ids"]["doi"], "10.1000/abc")
        self.assertEqual(records[0]["external_ids"]["scopus_eid"], "2-s2.0-123")
        self.assertEqual(records[0]["sources"], ["Crossref", "scopus"])

    def test_deduplicate_records_uses_normalized_title_and_year_when_no_doi(self):
        records = deduplicate_records(
            [
                {"title": "Waterborne-epoxy asphalt bonding!", "year": 2024, "source": "arxiv"},
                {"title": "Waterborne epoxy asphalt bonding", "year": "2024", "source": "Semantic Scholar"},
            ]
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["sources"], ["arxiv", "Semantic Scholar"])

    def test_deduplicate_records_keeps_different_year_records_separate(self):
        records = deduplicate_records(
            [
                {"title": "Waterborne epoxy asphalt bonding", "year": 2023, "source": "A"},
                {"title": "Waterborne epoxy asphalt bonding", "year": 2024, "source": "B"},
            ]
        )

        self.assertEqual(len(records), 2)


if __name__ == "__main__":
    unittest.main()
