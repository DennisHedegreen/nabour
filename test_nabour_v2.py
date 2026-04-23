from __future__ import annotations

import unittest

from cross_border_matcher import build_matcher_state, compute_cross_border_matches
from data_loader import FACTOR_LABELS, load_vectors_by_country_for_pair, summarize_pair_coverage
from info_content import get_info
from pair_registry import get_pair_spec, list_pair_specs
from region_metadata import get_region_navigation


class NabourV2Tests(unittest.TestCase):
    def test_pair_registry_keeps_three_live_pairs(self):
        specs = {spec.pair_id: spec for spec in list_pair_specs()}
        self.assertEqual(set(specs), {"dk_se", "dk_no", "se_no"})
        self.assertTrue(specs["dk_se"].active)
        self.assertTrue(specs["dk_no"].active)
        self.assertTrue(specs["se_no"].active)

    def test_loader_returns_expected_shape_for_active_pair(self):
        pair_spec = get_pair_spec("dk_se")
        vectors = load_vectors_by_country_for_pair(pair_spec)
        self.assertEqual(set(vectors), {"denmark", "sweden"})
        self.assertTrue(vectors["denmark"])
        self.assertTrue(vectors["sweden"])
        self.assertEqual(set(vectors["denmark"][0].values), set(pair_spec.factor_keys))

    def test_dk_no_loader_returns_expected_shape(self):
        pair_spec = get_pair_spec("dk_no")
        summaries = summarize_pair_coverage(pair_spec)
        self.assertEqual(summaries["denmark"].municipality_count, 98)
        self.assertEqual(summaries["norway"].municipality_count, 357)
        vectors = load_vectors_by_country_for_pair(pair_spec)
        self.assertEqual(set(vectors), {"denmark", "norway"})
        self.assertEqual(set(vectors["denmark"][0].values), set(pair_spec.factor_keys))

    def test_se_no_loader_returns_expected_shape(self):
        pair_spec = get_pair_spec("se_no")
        summaries = summarize_pair_coverage(pair_spec)
        self.assertEqual(summaries["sweden"].municipality_count, 290)
        self.assertEqual(summaries["norway"].municipality_count, 357)
        vectors = load_vectors_by_country_for_pair(pair_spec)
        self.assertEqual(set(vectors), {"sweden", "norway"})
        self.assertEqual(set(vectors["sweden"][0].values), set(pair_spec.factor_keys))

    def test_matcher_works_both_directions_for_active_pair(self):
        matcher_state = build_matcher_state("dk_se")
        dk_matches = compute_cross_border_matches("denmark", "Aarhus", matcher_state, top_n=3)
        se_matches = compute_cross_border_matches("sweden", "Stockholm", matcher_state, top_n=3)
        self.assertEqual(len(dk_matches), 3)
        self.assertEqual(len(se_matches), 3)
        self.assertTrue(all(match.country_id == "sweden" for match in dk_matches))
        self.assertTrue(all(match.country_id == "denmark" for match in se_matches))

    def test_matcher_works_both_directions_for_dk_no(self):
        matcher_state = build_matcher_state("dk_no")
        dk_matches = compute_cross_border_matches("denmark", "Aarhus", matcher_state, top_n=3)
        no_matches = compute_cross_border_matches("norway", "Oslo - Oslove", matcher_state, top_n=3)
        self.assertEqual(len(dk_matches), 3)
        self.assertEqual(len(no_matches), 3)
        self.assertTrue(all(match.country_id == "norway" for match in dk_matches))
        self.assertTrue(all(match.country_id == "denmark" for match in no_matches))

    def test_matcher_works_both_directions_for_se_no(self):
        matcher_state = build_matcher_state("se_no")
        se_matches = compute_cross_border_matches("sweden", "Stockholm", matcher_state, top_n=3)
        no_matches = compute_cross_border_matches("norway", "Oslo - Oslove", matcher_state, top_n=3)
        self.assertEqual(len(se_matches), 3)
        self.assertEqual(len(no_matches), 3)
        self.assertTrue(all(match.country_id == "norway" for match in se_matches))
        self.assertTrue(all(match.country_id == "sweden" for match in no_matches))

    def test_region_navigation_supports_norway_when_data_is_ready(self):
        norway_regions = get_region_navigation(
            "norway",
            reference_year=2024,
            factor_keys=("population", "age65", "education", "income", "density"),
        )
        self.assertIn("Oslo", norway_regions)
        self.assertIn("Oslo - Oslove", norway_regions["Oslo"])

    def test_info_content_tracks_pair_specific_factor_sets(self):
        dk_se_info = get_info("en", "dk_se")
        dk_no_info = get_info("en", "dk_no")
        se_no_info = get_info("en", "se_no")
        self.assertEqual(set(dk_se_info["factors"]), {FACTOR_LABELS[key] for key in get_pair_spec("dk_se").factor_keys})
        self.assertEqual(set(dk_no_info["factors"]), {FACTOR_LABELS[key] for key in get_pair_spec("dk_no").factor_keys})
        self.assertEqual(set(se_no_info["factors"]), {FACTOR_LABELS[key] for key in get_pair_spec("se_no").factor_keys})
        self.assertTrue(any("narrower 2024 beta layer" in line for line in dk_no_info["method"]))
        self.assertTrue(any("Income is temporarily" in line for line in se_no_info["method"]))


if __name__ == "__main__":
    unittest.main()
