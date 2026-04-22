from __future__ import annotations

from pair_registry import list_pair_specs
from region_metadata import get_region_navigation


def main() -> None:
    seen: set[tuple[str, int, tuple[str, ...]]] = set()
    for pair_spec in list_pair_specs():
        for country_id in pair_spec.countries:
            key = (country_id, pair_spec.reference_year, pair_spec.factor_keys)
            if key in seen:
                continue
            seen.add(key)
            grouped = get_region_navigation(
                country_id,
                reference_year=pair_spec.reference_year,
                factor_keys=pair_spec.factor_keys,
            )
            municipality_count = sum(len(municipalities) for municipalities in grouped.values())
            print(f"{country_id}: regions={len(grouped)}, municipalities={municipality_count}")
            for region_name, municipalities in grouped.items():
                print(f"  - {region_name}: {len(municipalities)}")


if __name__ == "__main__":
    main()
