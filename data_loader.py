from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from pair_registry import AVAILABLE_COUNTRIES, PairSpec

MATCHER_REFERENCE_YEAR = 2022

FACTOR_LABELS = {
    "population": "Population",
    "age65": "Age 65+",
    "education": "Education",
    "income": "Income",
    "turnout": "Turnout",
    "density": "Population density",
    "cars": "Cars",
}

FACTOR_FILE_NAMES = {
    "population": "population.csv",
    "age65": "age65_pct.csv",
    "education": "education.csv",
    "income": "income.csv",
    "turnout": "turnout_pct.csv",
    "density": "population_density.csv",
    "cars": "cars_per_1000.csv",
}


@dataclass(frozen=True)
class MunicipalityVector:
    country_id: str
    municipality: str
    year: int
    values: dict[str, float]


@dataclass(frozen=True)
class CoverageSummary:
    country_id: str
    reference_year: int
    factor_count: int
    municipality_count: int
    dropped_municipalities: int


def get_data_root() -> Path:
    return Path(__file__).resolve().parent / "data"


def get_factor_path(country_id: str, factor_key: str, data_root: Path | None = None) -> Path:
    if country_id not in AVAILABLE_COUNTRIES:
        raise KeyError(f"Unsupported country: {country_id}")
    if factor_key not in FACTOR_FILE_NAMES:
        raise KeyError(f"Unsupported factor: {factor_key}")
    root = data_root or get_data_root()
    return root / country_id / "factors" / FACTOR_FILE_NAMES[factor_key]


def load_factor_values(
    country_id: str,
    factor_key: str,
    reference_year: int = MATCHER_REFERENCE_YEAR,
    data_root: Path | None = None,
) -> dict[str, float]:
    path = get_factor_path(country_id, factor_key, data_root=data_root)
    values: dict[str, float] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            year_raw = row.get("year")
            municipality = (row.get("municipality") or "").strip()
            value_raw = row.get("value")
            if not year_raw or not municipality or not value_raw:
                continue
            if int(year_raw) != reference_year:
                continue
            values[municipality] = float(value_raw)
    return values


def load_country_vectors(
    country_id: str,
    factor_years: dict[str, int],
    reference_year: int,
    data_root: Path | None = None,
) -> list[MunicipalityVector]:
    factor_maps = {
        factor_key: load_factor_values(
            country_id=country_id,
            factor_key=factor_key,
            reference_year=factor_year,
            data_root=data_root,
        )
        for factor_key, factor_year in factor_years.items()
    }
    municipality_sets = [set(values.keys()) for values in factor_maps.values()]
    if not municipality_sets:
        return []

    shared_municipalities = set.intersection(*municipality_sets)
    vectors: list[MunicipalityVector] = []
    for municipality in sorted(shared_municipalities):
        values = {factor_key: factor_maps[factor_key][municipality] for factor_key in factor_years}
        vectors.append(
            MunicipalityVector(
                country_id=country_id,
                municipality=municipality,
                year=reference_year,
                values=values,
            )
        )
    return vectors


def load_vectors_by_country_for_pair(
    pair_spec: PairSpec,
    data_root: Path | None = None,
) -> dict[str, list[MunicipalityVector]]:
    return {
        country_id: load_country_vectors(
            country_id=country_id,
            factor_years={factor_key: pair_spec.factor_year(country_id, factor_key) for factor_key in pair_spec.factor_keys},
            reference_year=pair_spec.reference_year,
            data_root=data_root,
        )
        for country_id in pair_spec.countries
    }


def summarize_country_coverage(
    pair_spec: PairSpec,
    country_id: str,
    data_root: Path | None = None,
) -> CoverageSummary:
    factor_maps = {
        factor_key: load_factor_values(
            country_id=country_id,
            factor_key=factor_key,
            reference_year=pair_spec.factor_year(country_id, factor_key),
            data_root=data_root,
        )
        for factor_key in pair_spec.factor_keys
    }
    all_municipalities = set().union(*(values.keys() for values in factor_maps.values())) if factor_maps else set()
    shared_municipalities = set.intersection(*(set(values.keys()) for values in factor_maps.values())) if factor_maps else set()
    return CoverageSummary(
        country_id=country_id,
        reference_year=pair_spec.reference_year,
        factor_count=len(pair_spec.factor_keys),
        municipality_count=len(shared_municipalities),
        dropped_municipalities=len(all_municipalities - shared_municipalities),
    )


def summarize_pair_coverage(
    pair_spec: PairSpec,
    data_root: Path | None = None,
) -> dict[str, CoverageSummary]:
    return {
        country_id: summarize_country_coverage(
            pair_spec=pair_spec,
            country_id=country_id,
            data_root=data_root,
        )
        for country_id in pair_spec.countries
    }


def vectors_to_rows(vectors: list[MunicipalityVector]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for vector in vectors:
        row: dict[str, object] = {
            "country_id": vector.country_id,
            "municipality": vector.municipality,
            "year": vector.year,
        }
        row.update(vector.values)
        rows.append(row)
    return rows
