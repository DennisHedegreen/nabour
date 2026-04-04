from __future__ import annotations

import csv
from pathlib import Path

from income_conversion import (
    get_income_conversion_meta,
    income_to_home_currency_display,
    income_to_local_currency,
    income_to_match_currency_dkk,
)


ROOT = Path(__file__).resolve().parent


def load_income(country_id: str, municipality: str, year: int = 2022) -> float:
    path = ROOT / "data" / country_id / "factors" / "income.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["municipality"] == municipality and int(row["year"]) == year:
                return float(row["value"])
    raise KeyError(f"Missing income value for {country_id}/{municipality}/{year}")


def print_example(country_id: str, municipality: str, home_country_id: str) -> None:
    raw_value = load_income(country_id, municipality)
    local_currency, local_value = income_to_local_currency(country_id, raw_value)
    home_currency, home_value = income_to_home_currency_display(country_id, raw_value, home_country_id)
    match_value_dkk = income_to_match_currency_dkk(country_id, raw_value)
    print(
        f"{municipality} ({country_id}) -> local {local_value:,.0f} {local_currency}, "
        f"match motor {match_value_dkk:,.0f} DKK_2022, "
        f"display for {home_country_id}: {home_value:,.0f} {home_currency}"
    )


def main() -> None:
    meta = get_income_conversion_meta()
    print(
        "income motor:",
        f"pba_2022={meta.sweden_price_base_amount_2022_sek:,.0f} SEK,",
        f"match_ref={meta.match_reference_date} SEK->DKK={meta.match_reference_sek_to_dkk:.4f},",
        f"display_ref={meta.display_reference_date} SEK->DKK={meta.display_reference_sek_to_dkk:.4f}",
    )
    print_example("denmark", "Albertslund", "sweden")
    print_example("sweden", "Landskrona", "denmark")


if __name__ == "__main__":
    main()
