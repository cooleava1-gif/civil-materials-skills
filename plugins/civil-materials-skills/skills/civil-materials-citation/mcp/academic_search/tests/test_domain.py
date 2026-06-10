import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.domain.classifier import classify_evidence_layers, evidence_type_for_claim
from academic_search.domain.journals import JOURNAL_FAMILIES, canonical_journal_family, expand_journal_terms
from academic_search.domain.queries import build_pubmed_query, suggest_queries


class DomainRulesTest(unittest.TestCase):
    def test_classifies_waterborne_epoxy_asphalt_evidence_layers(self):
        text = (
            "Waterborne epoxy modified emulsified asphalt showed improved pull-off "
            "bonding strength after demulsification. FTIR and fluorescence microscopy "
            "confirmed curing and phase compatibility under moisture aging."
        )

        layers = classify_evidence_layers(text)

        self.assertIn("curing_demulsification", layers)
        self.assertIn("microstructure_chemistry", layers)
        self.assertIn("bonding_interface_performance", layers)
        self.assertIn("moisture_aging_durability", layers)

    def test_classifies_full_wer_ea_screening_taxonomy(self):
        text = (
            "A waterborne epoxy resin dosage and emulsifier formulation study measured "
            "storage stability, particle size, pull-off bonding interface performance, "
            "Brookfield viscosity, demulsification and epoxy curing, FTIR/SEM chemistry, "
            "moisture aging durability, field trial traffic relevance, and review gaps."
        )

        layers = classify_evidence_layers(text)

        self.assertEqual(
            [
                "material_formulation",
                "emulsion_stability",
                "bonding_interface_performance",
                "rheology",
                "curing_demulsification",
                "microstructure_chemistry",
                "moisture_aging_durability",
                "service_field_relevance",
                "review_background",
            ],
            layers,
        )

    def test_claim_evidence_type_separates_mechanism_performance_and_durability(self):
        self.assertEqual(evidence_type_for_claim("FTIR explains the curing mechanism"), "mechanism")
        self.assertEqual(evidence_type_for_claim("bond strength increased after modification"), "performance")
        self.assertEqual(evidence_type_for_claim("moisture aging durability should be improved"), "durability")
        self.assertEqual(evidence_type_for_claim("recent progress and research gap"), "review/positioning")

    def test_journal_alias_expansion_supports_civil_materials_targets(self):
        self.assertEqual(canonical_journal_family("CBM"), "Construction and Building Materials")
        self.assertEqual(canonical_journal_family("ccc"), "Cement and Concrete Composites")
        self.assertNotIn("CCS", JOURNAL_FAMILIES)

        terms = expand_journal_terms(["CBM", "CCR", "JMCE", "MAS", "JCP", "RCR", "RMPD", "IJPE", "JRE", "CSCM"])

        self.assertIn("Construction and Building Materials", terms)
        self.assertIn("Cement and Concrete Research", terms)
        self.assertIn("Journal of Materials in Civil Engineering", terms)
        self.assertIn("Materials and Structures", terms)
        self.assertIn("Journal of Cleaner Production", terms)
        self.assertIn("Resources, Conservation and Recycling", terms)
        self.assertIn("Road Materials and Pavement Design", terms)
        self.assertIn("International Journal of Pavement Engineering", terms)
        self.assertIn("Journal of Road Engineering", terms)
        self.assertIn("Case Studies in Construction Materials", terms)

    def test_evidence_classifier_uses_word_boundaries_for_short_terms(self):
        text = (
            "Managing semantic packaging during a semester seminar and reporting a "
            "short-term 24 h strength value alone should remain a screening note, "
            "not proof of chemistry, weather exposure, or road use."
        )

        layers = classify_evidence_layers(text)

        self.assertNotIn("moisture_aging_durability", layers)
        self.assertNotIn("microstructure_chemistry", layers)
        self.assertNotIn("service_field_relevance", layers)

    def test_construction_materials_phrase_does_not_imply_field_service(self):
        layers = classify_evidence_layers(
            "Construction materials review for laboratory emulsified asphalt bonding tests."
        )

        self.assertNotIn("service_field_relevance", layers)

    def test_query_suggestions_include_topic_evidence_and_journal_terms(self):
        queries = suggest_queries(
            topic="waterborne epoxy modified emulsified asphalt",
            journal_family=["CBM", "RMPD"],
            evidence_layer="bonding_interface_performance",
            year_range="2020-2026",
        )

        self.assertTrue(queries)
        query = queries[0]["query"]
        self.assertIn('"waterborne epoxy modified emulsified asphalt"', query)
        self.assertIn("bonding", query)
        self.assertIn("Construction and Building Materials", query)
        self.assertIn("Road Materials and Pavement Design", query)
        self.assertEqual(queries[0]["year_range"], "2020-2026")

    def test_query_suggestions_escape_quotes_inside_topic(self):
        queries = suggest_queries(
            topic='waterborne epoxy "fast setting" OR fabricated',
            journal_family=["CBM"],
            evidence_layer="bonding_interface",
        )

        query = queries[0]["query"]

        self.assertIn('"waterborne epoxy \\"fast setting\\" OR fabricated"', query)
        self.assertEqual(queries[0]["evidence_layer"], "bonding_interface_performance")

    def test_build_pubmed_query_adds_journal_and_publication_date_filters(self):
        query = build_pubmed_query(
            '"waterborne epoxy" AND bonding',
            journals=["Construction and Building Materials", "Road Materials and Pavement Design"],
            year_range="2020-2026",
        )

        self.assertIn('("waterborne epoxy" AND bonding)', query)
        self.assertIn('"Construction and Building Materials"[Journal]', query)
        self.assertIn('"Road Materials and Pavement Design"[Journal]', query)
        self.assertIn("2020:2026[pdat]", query)


if __name__ == "__main__":
    unittest.main()
