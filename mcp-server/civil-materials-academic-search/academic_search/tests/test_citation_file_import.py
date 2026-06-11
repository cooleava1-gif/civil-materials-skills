import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.importers.citation_files import parse_citation_records


class CitationFileImportTest(unittest.TestCase):
    def test_parse_minimal_ris(self):
        content = """TY  - JOUR
TI  - Waterborne epoxy asphalt bonding
AU  - Chen, Alice
AU  - Wang, Bo
JO  - Construction and Building Materials
PY  - 2025
DO  - 10.1016/j.conbuildmat.2025.01.001
ER  -
"""

        records = parse_citation_records(content, "ris")

        self.assertEqual(records[0]["title"], "Waterborne epoxy asphalt bonding")
        self.assertEqual(records[0]["authors"], ["Chen, Alice", "Wang, Bo"])
        self.assertEqual(records[0]["doi"], "10.1016/j.conbuildmat.2025.01.001")

    def test_parse_minimal_bibtex(self):
        content = """@article{chen2025,
  title={Waterborne epoxy asphalt bonding},
  author={Alice Chen and Bo Wang},
  journal={Construction and Building Materials},
  year={2025},
  doi={10.1016/j.conbuildmat.2025.01.001}
}
"""

        records = parse_citation_records(content, "bibtex")

        self.assertEqual(records[0]["title"], "Waterborne epoxy asphalt bonding")
        self.assertEqual(records[0]["authors"], ["Alice Chen", "Bo Wang"])
        self.assertEqual(records[0]["year"], 2025)

    def test_parse_minimal_nbib(self):
        content = """PMID- 12345678
TI  - Waterborne epoxy asphalt bonding.
FAU - Chen, Alice
FAU - Wang, Bo
JT  - Construction and Building Materials
DP  - 2025 Jan
AID - 10.1016/j.conbuildmat.2025.01.001 [doi]
"""

        records = parse_citation_records(content, "nbib")

        self.assertEqual(records[0]["external_ids"]["pmid"], "12345678")
        self.assertEqual(records[0]["journal"], "Construction and Building Materials")
        self.assertEqual(records[0]["doi"], "10.1016/j.conbuildmat.2025.01.001")

    def test_parse_minimal_csv(self):
        content = "title,authors,doi,year,journal\nWaterborne epoxy asphalt,Alice Chen; Bo Wang,10.1000/example,2024,CBM\n"

        records = parse_citation_records(content, "csv")

        self.assertEqual(records[0]["authors"], ["Alice Chen", "Bo Wang"])
        self.assertEqual(records[0]["year"], 2024)


if __name__ == "__main__":
    unittest.main()
