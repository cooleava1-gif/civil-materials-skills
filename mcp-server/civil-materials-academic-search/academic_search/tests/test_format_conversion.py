import json
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.export.formats import export_citations
from academic_search.service import AcademicSearchService


SAMPLE_RECORD = {
    "title": "Waterborne epoxy modified emulsified asphalt bonding",
    "authors": ["Alice Chen", "Bo Wang"],
    "journal": "Construction and Building Materials",
    "year": 2025,
    "doi": "10.1016/j.conbuildmat.2025.01.001",
}


class FormatConversionTest(unittest.TestCase):
    def test_export_csl_json(self):
        content = export_citations([SAMPLE_RECORD], "csl-json")
        payload = json.loads(content)

        self.assertEqual(payload[0]["type"], "article-journal")
        self.assertEqual(payload[0]["DOI"], SAMPLE_RECORD["doi"])
        self.assertEqual(payload[0]["author"][0]["literal"], "Alice Chen")

    def test_export_jsonl(self):
        content = export_citations([SAMPLE_RECORD], "jsonl")
        lines = content.strip().splitlines()

        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["title"], SAMPLE_RECORD["title"])

    def test_service_convert_citation_records_imports_and_exports(self):
        service = AcademicSearchService(adapters=[])

        result = service.convert_citation_records(
            {
                "content": "title,authors,doi,year\nWaterborne epoxy,Alice Chen,10.1000/example,2025\n",
                "input_format": "csv",
                "output_format": "csl-json",
            }
        )

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["output_format"], "csl-json")
        self.assertIn('"DOI": "10.1000/example"', result["content"])


if __name__ == "__main__":
    unittest.main()
