from __future__ import annotations

from region_metadata import get_region_navigation


def main() -> None:
    for country_id in ("denmark", "sweden"):
        grouped = get_region_navigation(country_id)
        municipality_count = sum(len(municipalities) for municipalities in grouped.values())
        print(f"{country_id}: regions={len(grouped)}, municipalities={municipality_count}")
        for region_name, municipalities in grouped.items():
            print(f"  - {region_name}: {len(municipalities)}")


if __name__ == "__main__":
    main()
