from __future__ import annotations

from data_loader import summarize_pair_coverage
from pair_registry import list_pair_specs


def main() -> None:
    for pair_spec in list_pair_specs():
        print(
            f"pair={pair_spec.pair_id} active={pair_spec.active} "
            f"reference_year={pair_spec.reference_year} factors={len(pair_spec.factor_keys)}"
        )
        for country_id, summary in summarize_pair_coverage(pair_spec).items():
            print(
                f"  {country_id}: municipalities={summary.municipality_count}, "
                f"dropped={summary.dropped_municipalities}, factors={summary.factor_count}"
            )


if __name__ == "__main__":
    main()
