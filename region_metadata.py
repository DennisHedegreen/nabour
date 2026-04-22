from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from data_loader import MATCHER_REFERENCE_YEAR, load_country_vectors


DENMARK_REGION_BY_MUNICIPALITY = {
    "Aabenraa": "Region Syddanmark",
    "Aalborg": "Region Nordjylland",
    "Aarhus": "Region Midtjylland",
    "Albertslund": "Region Hovedstaden",
    "Allerød": "Region Hovedstaden",
    "Assens": "Region Syddanmark",
    "Ballerup": "Region Hovedstaden",
    "Billund": "Region Syddanmark",
    "Bornholm": "Region Hovedstaden",
    "Brøndby": "Region Hovedstaden",
    "Brønderslev": "Region Nordjylland",
    "Copenhagen": "Region Hovedstaden",
    "Dragør": "Region Hovedstaden",
    "Egedal": "Region Hovedstaden",
    "Esbjerg": "Region Syddanmark",
    "Faaborg-Midtfyn": "Region Syddanmark",
    "Fanø": "Region Syddanmark",
    "Favrskov": "Region Midtjylland",
    "Faxe": "Region Sjælland",
    "Fredensborg": "Region Hovedstaden",
    "Fredericia": "Region Syddanmark",
    "Frederiksberg": "Region Hovedstaden",
    "Frederikshavn": "Region Nordjylland",
    "Frederikssund": "Region Hovedstaden",
    "Furesø": "Region Hovedstaden",
    "Gentofte": "Region Hovedstaden",
    "Gladsaxe": "Region Hovedstaden",
    "Glostrup": "Region Hovedstaden",
    "Greve": "Region Sjælland",
    "Gribskov": "Region Hovedstaden",
    "Guldborgsund": "Region Sjælland",
    "Haderslev": "Region Syddanmark",
    "Halsnæs": "Region Hovedstaden",
    "Hedensted": "Region Midtjylland",
    "Helsingør": "Region Hovedstaden",
    "Herlev": "Region Hovedstaden",
    "Herning": "Region Midtjylland",
    "Hillerød": "Region Hovedstaden",
    "Hjørring": "Region Nordjylland",
    "Holbæk": "Region Sjælland",
    "Holstebro": "Region Midtjylland",
    "Horsens": "Region Midtjylland",
    "Hvidovre": "Region Hovedstaden",
    "Høje-Taastrup": "Region Hovedstaden",
    "Hørsholm": "Region Hovedstaden",
    "Ikast-Brande": "Region Midtjylland",
    "Ishøj": "Region Hovedstaden",
    "Jammerbugt": "Region Nordjylland",
    "Kalundborg": "Region Sjælland",
    "Kerteminde": "Region Syddanmark",
    "Kolding": "Region Syddanmark",
    "Køge": "Region Sjælland",
    "Langeland": "Region Syddanmark",
    "Lejre": "Region Sjælland",
    "Lemvig": "Region Midtjylland",
    "Lolland": "Region Sjælland",
    "Lyngby-Taarbæk": "Region Hovedstaden",
    "Læsø": "Region Nordjylland",
    "Mariagerfjord": "Region Nordjylland",
    "Middelfart": "Region Syddanmark",
    "Morsø": "Region Nordjylland",
    "Norddjurs": "Region Midtjylland",
    "Nordfyns": "Region Syddanmark",
    "Nyborg": "Region Syddanmark",
    "Næstved": "Region Sjælland",
    "Odder": "Region Midtjylland",
    "Odense": "Region Syddanmark",
    "Odsherred": "Region Sjælland",
    "Randers": "Region Midtjylland",
    "Rebild": "Region Nordjylland",
    "Ringkøbing-Skjern": "Region Midtjylland",
    "Ringsted": "Region Sjælland",
    "Roskilde": "Region Sjælland",
    "Rudersdal": "Region Hovedstaden",
    "Rødovre": "Region Hovedstaden",
    "Samsø": "Region Midtjylland",
    "Silkeborg": "Region Midtjylland",
    "Skanderborg": "Region Midtjylland",
    "Skive": "Region Midtjylland",
    "Slagelse": "Region Sjælland",
    "Solrød": "Region Sjælland",
    "Sorø": "Region Sjælland",
    "Stevns": "Region Sjælland",
    "Struer": "Region Midtjylland",
    "Svendborg": "Region Syddanmark",
    "Syddjurs": "Region Midtjylland",
    "Sønderborg": "Region Syddanmark",
    "Thisted": "Region Nordjylland",
    "Tårnby": "Region Hovedstaden",
    "Tønder": "Region Syddanmark",
    "Vallensbæk": "Region Hovedstaden",
    "Varde": "Region Syddanmark",
    "Vejen": "Region Syddanmark",
    "Vejle": "Region Syddanmark",
    "Vesthimmerlands": "Region Nordjylland",
    "Viborg": "Region Midtjylland",
    "Vordingborg": "Region Sjælland",
    "Ærø": "Region Syddanmark",
}

SWEDEN_COUNTY_BY_PREFIX = {
    "01": "Stockholms län",
    "03": "Uppsala län",
    "04": "Södermanlands län",
    "05": "Östergötlands län",
    "06": "Jönköpings län",
    "07": "Kronobergs län",
    "08": "Kalmar län",
    "09": "Gotlands län",
    "10": "Blekinge län",
    "12": "Skåne län",
    "13": "Hallands län",
    "14": "Västra Götalands län",
    "17": "Värmlands län",
    "18": "Örebro län",
    "19": "Västmanlands län",
    "20": "Dalarnas län",
    "21": "Gävleborgs län",
    "22": "Västernorrlands län",
    "23": "Jämtlands län",
    "24": "Västerbottens län",
    "25": "Norrbottens län",
}

NORWAY_COUNTY_BY_PREFIX = {
    "03": "Oslo",
    "11": "Rogaland",
    "15": "Møre og Romsdal",
    "18": "Nordland",
    "31": "Østfold",
    "32": "Akershus",
    "33": "Buskerud",
    "34": "Innlandet",
    "39": "Vestfold",
    "40": "Telemark",
    "42": "Agder",
    "46": "Vestland",
    "50": "Trøndelag",
    "55": "Troms",
    "56": "Finnmark",
}


def get_sweden_population_path(data_root: Path | None = None) -> Path:
    root = data_root or (Path(__file__).resolve().parent / "data")
    return root / "sweden" / "factors" / "population.csv"


def load_sweden_region_by_municipality(
    reference_year: int = MATCHER_REFERENCE_YEAR,
    data_root: Path | None = None,
) -> dict[str, str]:
    region_by_municipality: dict[str, str] = {}
    with get_sweden_population_path(data_root=data_root).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if int(row["year"]) != reference_year:
                continue
            municipality = row["municipality"].strip()
            code_prefix = row["public_geography_id"][:2]
            region_by_municipality[municipality] = SWEDEN_COUNTY_BY_PREFIX[code_prefix]
    return region_by_municipality


def get_norway_population_path(data_root: Path | None = None) -> Path:
    root = data_root or (Path(__file__).resolve().parent / "data")
    return root / "norway" / "factors" / "population.csv"


def load_norway_region_by_municipality(
    reference_year: int = MATCHER_REFERENCE_YEAR,
    data_root: Path | None = None,
) -> dict[str, str]:
    region_by_municipality: dict[str, str] = {}
    with get_norway_population_path(data_root=data_root).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if int(row["year"]) != reference_year:
                continue
            municipality = row["municipality"].strip()
            code_prefix = row["public_geography_id"][:2]
            region_by_municipality[municipality] = NORWAY_COUNTY_BY_PREFIX[code_prefix]
    return region_by_municipality


def get_region_by_municipality(
    country_id: str,
    reference_year: int = MATCHER_REFERENCE_YEAR,
    data_root: Path | None = None,
) -> dict[str, str]:
    if country_id == "denmark":
        return DENMARK_REGION_BY_MUNICIPALITY.copy()
    if country_id == "sweden":
        return load_sweden_region_by_municipality(reference_year=reference_year, data_root=data_root)
    if country_id == "norway":
        return load_norway_region_by_municipality(reference_year=reference_year, data_root=data_root)
    raise KeyError(f"Unsupported country: {country_id}")


def get_region_navigation(
    country_id: str,
    reference_year: int = MATCHER_REFERENCE_YEAR,
    factor_keys: tuple[str, ...] | None = None,
    data_root: Path | None = None,
) -> dict[str, list[str]]:
    active_factor_keys = factor_keys or ("population",)
    available = {
        vector.municipality
        for vector in load_country_vectors(country_id, active_factor_keys, reference_year, data_root)
    }
    region_by_municipality = get_region_by_municipality(
        country_id=country_id,
        reference_year=reference_year,
        data_root=data_root,
    )

    missing = sorted(available - set(region_by_municipality))
    if missing:
        raise KeyError(f"Missing region metadata for {country_id}: {', '.join(missing[:5])}")

    grouped: dict[str, list[str]] = defaultdict(list)
    for municipality in sorted(available):
        grouped[region_by_municipality[municipality]].append(municipality)
    return dict(grouped)
