import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.adapters.arxiv import ArxivAdapter


ATOM_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2401.12345v2</id>
    <updated>2024-01-20T00:00:00Z</updated>
    <published>2024-01-15T00:00:00Z</published>
    <title>Waterborne epoxy asphalt interface learning</title>
    <summary>Machine learning for asphalt interface behavior.</summary>
    <author><name>Alice Chen</name></author>
    <author><name>Bo Wang</name></author>
    <arxiv:doi>10.48550/arXiv.2401.12345</arxiv:doi>
    <link href="http://arxiv.org/abs/2401.12345v2" rel="alternate" type="text/html"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/cs/9901001</id>
    <published>1999-01-01T00:00:00Z</published>
    <title>Legacy arXiv identifier parsing</title>
    <summary>Legacy category identifiers should survive parsing.</summary>
    <author><name>Casey Doe</name></author>
  </entry>
</feed>
"""


class FakeResponse:
    status_code = 200
    text = ATOM_FEED

    def raise_for_status(self):
        return None


class ArxivAdapterTest(unittest.TestCase):
    def test_arxiv_search_parses_atom_feed(self):
        calls = []

        def getter(url, **kwargs):
            calls.append({"url": url, "params": kwargs.get("params")})
            return FakeResponse()

        adapter = ArxivAdapter(getter=getter)

        records = adapter.search("waterborne epoxy asphalt", year_range="2024-2026", limit=2)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["title"], "Waterborne epoxy asphalt interface learning")
        self.assertEqual(records[0]["authors"], ["Alice Chen", "Bo Wang"])
        self.assertEqual(records[0]["year"], 2024)
        self.assertEqual(records[0]["external_ids"]["arxiv"], "2401.12345v2")
        self.assertEqual(records[0]["external_ids"]["arxiv_canonical"], "2401.12345")
        self.assertEqual(records[0]["source"], "arxiv")
        self.assertIn("submittedDate:[202401010000 TO 202612312359]", calls[0]["params"]["search_query"])

    def test_arxiv_fetch_accepts_versioned_id(self):
        adapter = ArxivAdapter(getter=lambda url, **kwargs: FakeResponse())

        record = adapter.fetch(external_id="https://arxiv.org/abs/2401.12345v2")

        self.assertIsNotNone(record)
        self.assertEqual(record["external_ids"]["arxiv"], "2401.12345v2")
        self.assertEqual(record["external_ids"]["arxiv_canonical"], "2401.12345")

    def test_arxiv_adapter_never_requires_api_key(self):
        adapter = ArxivAdapter(getter=lambda url, **kwargs: FakeResponse())

        records = adapter.search("asphalt", limit=1)

        self.assertEqual(records[0]["source"], "arxiv")


if __name__ == "__main__":
    unittest.main()
