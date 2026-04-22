from __future__ import annotations

from dataclasses import dataclass


MATCH_REFERENCE_YEAR = 2022
SWEDEN_PRICE_BASE_AMOUNT_2022_SEK = 48_300.0

# Source: ECB euro reference rates, 30 December 2022.
MATCH_REFERENCE_DATE = "2022-12-30"
MATCH_REFERENCE_EUR_DKK = 7.4365
MATCH_REFERENCE_EUR_SEK = 11.1218

# Source: ECB euro reference rates, 31 December 2024.
MATCH_REFERENCE_2024_DATE = "2024-12-31"
MATCH_REFERENCE_2024_EUR_DKK = 7.4578
MATCH_REFERENCE_2024_EUR_SEK = 11.4590
MATCH_REFERENCE_2024_EUR_NOK = 11.7950

# Source: ECB euro reference rates, 2 April 2026.
DISPLAY_REFERENCE_DATE = "2026-04-02"
DISPLAY_REFERENCE_EUR_DKK = 7.4722
DISPLAY_REFERENCE_EUR_SEK = 10.9480
DISPLAY_REFERENCE_EUR_NOK = 11.2285


@dataclass(frozen=True)
class IncomeConversionMeta:
    sweden_price_base_amount_2022_sek: float
    match_reference_date: str
    match_reference_sek_to_dkk: float
    match_reference_dkk_to_sek: float
    display_reference_date: str
    display_reference_sek_to_dkk: float
    display_reference_dkk_to_sek: float


def derive_cross_rate(base_a_per_eur: float, base_b_per_eur: float) -> float:
    return base_b_per_eur / base_a_per_eur


MATCH_REFERENCE_SEK_TO_DKK = derive_cross_rate(MATCH_REFERENCE_EUR_SEK, MATCH_REFERENCE_EUR_DKK)
MATCH_REFERENCE_DKK_TO_SEK = derive_cross_rate(MATCH_REFERENCE_EUR_DKK, MATCH_REFERENCE_EUR_SEK)
MATCH_REFERENCE_2024_NOK_TO_DKK = derive_cross_rate(MATCH_REFERENCE_2024_EUR_NOK, MATCH_REFERENCE_2024_EUR_DKK)
DISPLAY_REFERENCE_SEK_TO_DKK = derive_cross_rate(DISPLAY_REFERENCE_EUR_SEK, DISPLAY_REFERENCE_EUR_DKK)
DISPLAY_REFERENCE_DKK_TO_SEK = derive_cross_rate(DISPLAY_REFERENCE_EUR_DKK, DISPLAY_REFERENCE_EUR_SEK)

def get_income_conversion_meta() -> IncomeConversionMeta:
    return IncomeConversionMeta(
        sweden_price_base_amount_2022_sek=SWEDEN_PRICE_BASE_AMOUNT_2022_SEK,
        match_reference_date=MATCH_REFERENCE_DATE,
        match_reference_sek_to_dkk=MATCH_REFERENCE_SEK_TO_DKK,
        match_reference_dkk_to_sek=MATCH_REFERENCE_DKK_TO_SEK,
        display_reference_date=DISPLAY_REFERENCE_DATE,
        display_reference_sek_to_dkk=DISPLAY_REFERENCE_SEK_TO_DKK,
        display_reference_dkk_to_sek=DISPLAY_REFERENCE_DKK_TO_SEK,
    )


def sweden_price_base_amounts_to_sek(raw_value: float) -> float:
    return raw_value * SWEDEN_PRICE_BASE_AMOUNT_2022_SEK


def income_to_local_currency(country_id: str, raw_value: float) -> tuple[str, float]:
    if country_id == "denmark":
        return ("DKK", raw_value)
    if country_id == "sweden":
        return ("SEK", sweden_price_base_amounts_to_sek(raw_value))
    if country_id == "norway":
        return ("NOK", raw_value)
    raise KeyError(f"Unsupported country: {country_id}")


DISPLAY_REFERENCE_NOK_TO_DKK = derive_cross_rate(DISPLAY_REFERENCE_EUR_NOK, DISPLAY_REFERENCE_EUR_DKK)
DISPLAY_REFERENCE_DKK_TO_NOK = derive_cross_rate(DISPLAY_REFERENCE_EUR_DKK, DISPLAY_REFERENCE_EUR_NOK)
DISPLAY_REFERENCE_SEK_TO_NOK = derive_cross_rate(DISPLAY_REFERENCE_EUR_SEK, DISPLAY_REFERENCE_EUR_NOK)
DISPLAY_REFERENCE_NOK_TO_SEK = derive_cross_rate(DISPLAY_REFERENCE_EUR_NOK, DISPLAY_REFERENCE_EUR_SEK)


def income_to_match_currency_dkk(country_id: str, raw_value: float, *, reference_year: int) -> float:
    if country_id == "denmark":
        return raw_value
    if country_id == "sweden" and reference_year == 2022:
        return sweden_price_base_amounts_to_sek(raw_value) * MATCH_REFERENCE_SEK_TO_DKK
    if country_id == "norway" and reference_year == 2024:
        return raw_value * MATCH_REFERENCE_2024_NOK_TO_DKK
    raise KeyError(f"Unsupported country: {country_id}")


def income_to_home_currency_display(country_id: str, raw_value: float, home_country_id: str) -> tuple[str, float]:
    local_currency, local_value = income_to_local_currency(country_id, raw_value)

    if home_country_id == "denmark":
        if local_currency == "DKK":
            return ("DKK", local_value)
        if local_currency == "SEK":
            return ("DKK", local_value * DISPLAY_REFERENCE_SEK_TO_DKK)
        return ("DKK", local_value * DISPLAY_REFERENCE_NOK_TO_DKK)

    if home_country_id == "sweden":
        if local_currency == "SEK":
            return ("SEK", local_value)
        if local_currency == "DKK":
            return ("SEK", local_value * DISPLAY_REFERENCE_DKK_TO_SEK)
        return ("SEK", local_value * DISPLAY_REFERENCE_NOK_TO_SEK)

    if home_country_id == "norway":
        if local_currency == "NOK":
            return ("NOK", local_value)
        if local_currency == "DKK":
            return ("NOK", local_value * DISPLAY_REFERENCE_DKK_TO_NOK)
        return ("NOK", local_value * DISPLAY_REFERENCE_SEK_TO_NOK)

    raise KeyError(f"Unsupported home country: {home_country_id}")
