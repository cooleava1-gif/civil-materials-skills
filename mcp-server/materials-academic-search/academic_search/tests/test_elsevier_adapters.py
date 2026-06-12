import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.adapters import AdapterDisabled, AdapterError
from academic_search.adapters.sciencedirect import ScienceDirectAdapter
from academic_search.adapters.scopus import ScopusAdapter


class FakeJsonResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.request = httpx.Request("GET", "https://api.elsevier.test")
        self.response = httpx.Response(status_code, request=self.request)

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("elsevier error", request=self.request, response=self.response)


class ElsevierAdapterTest(unittest.TestCase):
    def test_scopus_disabled_without_key(self):
        with patch.dict(os.environ, {"SCOPUS_API_KEY": ""}, clear=False):
            with self.assertRaises(AdapterDisabled) as captured:
                ScopusAdapter()

        self.assertIn("SCOPUS_API_KEY", str(captured.exception))

    def test_scopus_search_parses_mock_entries(self):
        payload = {
            "search-results": {
                "entry": [
                    {
                        "dc:title": "Waterborne epoxy asphalt bonding",
                        "dc:identifier": "SCOPUS_ID:85123456789",
                        "eid": "2-s2.0-85123456789",
                        "prism:doi": "10.1016/j.conbuildmat.2025.01.001",
                        "prism:publicationName": "Construction and Building Materials",
                        "prism:coverDate": "2025-01-15",
                        "dc:creator": "Chen, Alice",
                        "citedby-count": "7",
                        "prism:url": "https://api.elsevier.com/content/abstract/scopus_id/85123456789",
                    }
                ]
            }
        }

        def getter(url, **kwargs):
            return FakeJsonResponse(payload)

        with patch.dict(os.environ, {"SCOPUS_API_KEY": "test-key"}, clear=False):
            records = ScopusAdapter(getter=getter).search("waterborne epoxy asphalt", limit=1)

        self.assertEqual(records[0]["source"], "scopus")
        self.assertEqual(records[0]["external_ids"]["scopus_eid"], "2-s2.0-85123456789")
        self.assertEqual(records[0]["doi"], "10.1016/j.conbuildmat.2025.01.001")
        self.assertEqual(records[0]["citation_count"], 7)

    def test_scopus_unauthorized_status_has_clear_error(self):
        with patch.dict(os.environ, {"SCOPUS_API_KEY": "test-key"}, clear=False):
            adapter = ScopusAdapter(getter=lambda url, **kwargs: FakeJsonResponse({}, status_code=403))
            with self.assertRaises(AdapterError) as captured:
                adapter.search("asphalt")

        self.assertIn("Scopus returned 403", str(captured.exception))

    def test_sciencedirect_disabled_without_key(self):
        with patch.dict(os.environ, {"ELSEVIER_API_KEY": ""}, clear=False):
            with self.assertRaises(AdapterDisabled) as captured:
                ScienceDirectAdapter()

        self.assertIn("ELSEVIER_API_KEY", str(captured.exception))

    def test_sciencedirect_fetch_parses_mock_coredata(self):
        payload = {
            "full-text-retrieval-response": {
                "coredata": {
                    "dc:title": "Article metadata for waterborne epoxy asphalt",
                    "prism:doi": "10.1016/j.conbuildmat.2024.12.345",
                    "prism:publicationName": "Construction and Building Materials",
                    "prism:coverDate": "2024-12-01",
                    "dc:creator": [{"$": "Alice Chen"}, {"$": "Bo Wang"}],
                    "prism:url": "https://linkinghub.elsevier.com/retrieve/pii/S0950061824012345",
                    "pii": "S0950061824012345",
                    "dc:description": "Bonding performance abstract.",
                }
            }
        }

        def getter(url, **kwargs):
            return FakeJsonResponse(payload)

        with patch.dict(os.environ, {"ELSEVIER_API_KEY": "test-key"}, clear=False):
            record = ScienceDirectAdapter(getter=getter).fetch(doi="10.1016/j.conbuildmat.2024.12.345")

        self.assertEqual(record["source"], "sciencedirect")
        self.assertEqual(record["external_ids"]["pii"], "S0950061824012345")
        self.assertEqual(record["year"], 2024)
        self.assertEqual(record["authors"], ["Alice Chen", "Bo Wang"])

    def test_sciencedirect_rate_limit_status_has_clear_error(self):
        with patch.dict(os.environ, {"ELSEVIER_API_KEY": "test-key"}, clear=False):
            adapter = ScienceDirectAdapter(getter=lambda url, **kwargs: FakeJsonResponse({}, status_code=429))
            with self.assertRaises(AdapterError) as captured:
                adapter.fetch(pii="S0950061824012345")

        self.assertIn("ScienceDirect returned 429", str(captured.exception))


if __name__ == "__main__":
    unittest.main()
