from __future__ import annotations

import math
from dataclasses import dataclass

from data_loader import FACTOR_LABELS, MATCHER_FACTOR_KEYS, MunicipalityVector, load_vectors_by_country
from income_conversion import income_to_match_currency_dkk


@dataclass(frozen=True)
class CrossBorderMatch:
    municipality: str
    country_id: str
    distance: float
    score: float
    similar_factors: tuple[str, ...]
    different_factors: tuple[str, ...]
    factor_details: tuple["FactorDetail", ...]


@dataclass(frozen=True)
class StandardizedMunicipalityVector:
    country_id: str
    municipality: str
    values: dict[str, float]


@dataclass(frozen=True)
class FactorDetail:
    factor_key: str
    label: str
    source_value: float
    target_value: float
    source_standardized: float
    target_standardized: float
    standardized_gap: float


@dataclass(frozen=True)
class MatcherState:
    raw_vectors: dict[str, list[MunicipalityVector]]
    standardized_vectors: dict[str, list[StandardizedMunicipalityVector]]


def get_matching_value(vector: MunicipalityVector, factor_key: str) -> float:
    if factor_key == "income":
        return income_to_match_currency_dkk(vector.country_id, vector.values[factor_key])
    return vector.values[factor_key]


def build_standardized_vectors(
    vectors_by_country: dict[str, list[MunicipalityVector]],
) -> dict[str, list[StandardizedMunicipalityVector]]:
    factor_values: dict[str, list[float]] = {factor_key: [] for factor_key in MATCHER_FACTOR_KEYS}
    for country_vectors in vectors_by_country.values():
        for vector in country_vectors:
            for factor_key in MATCHER_FACTOR_KEYS:
                factor_values[factor_key].append(get_matching_value(vector, factor_key))

    stats: dict[str, tuple[float, float]] = {}
    for factor_key, values in factor_values.items():
        if not values:
            stats[factor_key] = (0.0, 1.0)
            continue
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        std = math.sqrt(variance) or 1.0
        stats[factor_key] = (mean, std)

    standardized: dict[str, list[StandardizedMunicipalityVector]] = {}
    for country_id, vectors in vectors_by_country.items():
        standardized[country_id] = []
        for vector in vectors:
            values = {}
            for factor_key in MATCHER_FACTOR_KEYS:
                mean, std = stats[factor_key]
                values[factor_key] = (get_matching_value(vector, factor_key) - mean) / std
            standardized[country_id].append(
                StandardizedMunicipalityVector(
                    country_id=country_id,
                    municipality=vector.municipality,
                    values=values,
                )
            )
    return standardized


def compute_cross_border_matches(
    source_country_id: str,
    source_municipality: str,
    matcher_state: MatcherState,
    top_n: int = 5,
) -> list[CrossBorderMatch]:
    standardized_vectors = matcher_state.standardized_vectors
    if source_country_id not in standardized_vectors:
        raise KeyError(f"Unknown source country: {source_country_id}")

    target_country_id = next(country_id for country_id in standardized_vectors if country_id != source_country_id)
    source_vector = next(
        (vector for vector in standardized_vectors[source_country_id] if vector.municipality == source_municipality),
        None,
    )
    if source_vector is None:
        raise KeyError(f"Unknown municipality in {source_country_id}: {source_municipality}")

    raw_source_vector = next(
        (
            vector
            for vector in matcher_state.raw_vectors[source_country_id]
            if vector.municipality == source_municipality
        ),
        None,
    )
    if raw_source_vector is None:
        raise KeyError(f"Missing raw municipality in {source_country_id}: {source_municipality}")

    matches: list[CrossBorderMatch] = []
    for target_vector in standardized_vectors[target_country_id]:
        raw_target_vector = next(
            (
                vector
                for vector in matcher_state.raw_vectors[target_country_id]
                if vector.municipality == target_vector.municipality
            ),
            None,
        )
        if raw_target_vector is None:
            continue
        deltas = {
            factor_key: abs(source_vector.values[factor_key] - target_vector.values[factor_key])
            for factor_key in MATCHER_FACTOR_KEYS
        }
        distance = math.sqrt(sum(delta**2 for delta in deltas.values()))
        score = round(100.0 / (1.0 + distance), 1)
        ranked = sorted(deltas.items(), key=lambda item: item[1])
        similar = tuple(FACTOR_LABELS[key] for key, _ in ranked[:3])
        different = tuple(FACTOR_LABELS[key] for key, _ in ranked[-3:])
        factor_details = tuple(
            FactorDetail(
                factor_key=factor_key,
                label=FACTOR_LABELS[factor_key],
                source_value=raw_source_vector.values[factor_key],
                target_value=raw_target_vector.values[factor_key],
                source_standardized=source_vector.values[factor_key],
                target_standardized=target_vector.values[factor_key],
                standardized_gap=deltas[factor_key],
            )
            for factor_key in MATCHER_FACTOR_KEYS
        )
        matches.append(
            CrossBorderMatch(
                municipality=target_vector.municipality,
                country_id=target_country_id,
                distance=distance,
                score=score,
                similar_factors=similar,
                different_factors=different,
                factor_details=factor_details,
            )
        )
    return sorted(matches, key=lambda match: match.distance)[:top_n]


def get_available_municipalities(
    country_id: str,
    matcher_state: MatcherState,
) -> list[str]:
    if country_id not in matcher_state.standardized_vectors:
        raise KeyError(f"Unknown country: {country_id}")
    return sorted(vector.municipality for vector in matcher_state.standardized_vectors[country_id])


def build_default_matcher_state() -> MatcherState:
    raw_vectors = load_vectors_by_country()
    return MatcherState(
        raw_vectors=raw_vectors,
        standardized_vectors=build_standardized_vectors(raw_vectors),
    )
