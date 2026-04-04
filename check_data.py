from __future__ import annotations

from data_loader import MATCHER_REFERENCE_YEAR, summarize_all_coverage


def main() -> None:
    summaries = summarize_all_coverage(reference_year=MATCHER_REFERENCE_YEAR)
    print(f"reference_year={MATCHER_REFERENCE_YEAR}")
    for country_id, summary in summaries.items():
        print(
            f"{country_id}: municipalities={summary.municipality_count}, "
            f"dropped={summary.dropped_municipalities}, factors={summary.factor_count}"
        )


if __name__ == "__main__":
    main()
