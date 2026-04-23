from __future__ import annotations

from dataclasses import dataclass, field


AVAILABLE_COUNTRIES = ("denmark", "sweden", "norway")


@dataclass(frozen=True)
class PairSpec:
    pair_id: str
    countries: tuple[str, str]
    reference_year: int
    factor_keys: tuple[str, ...]
    labels: dict[str, str]
    method_note_key: str
    factor_year_overrides: dict[str, int] = field(default_factory=dict)
    country_factor_year_overrides: dict[str, dict[str, int]] = field(default_factory=dict)
    active: bool = True
    blocked_reason_key: str | None = None

    def factor_year(self, country_id: str, factor_key: str) -> int:
        country_overrides = self.country_factor_year_overrides.get(country_id, {})
        if factor_key in country_overrides:
            return country_overrides[factor_key]
        return self.factor_year_overrides.get(factor_key, self.reference_year)


PAIR_SPECS = {
    "dk_se": PairSpec(
        pair_id="dk_se",
        countries=("denmark", "sweden"),
        reference_year=2022,
        factor_keys=("population", "age65", "education", "income", "turnout", "density", "cars"),
        factor_year_overrides={},
        country_factor_year_overrides={},
        labels={"en": "Denmark ↔ Sweden", "da": "Danmark ↔ Sverige", "sv": "Danmark ↔ Sverige", "no": "Danmark ↔ Sverige"},
        method_note_key="dk_se_v1",
        active=True,
    ),
    "dk_no": PairSpec(
        pair_id="dk_no",
        countries=("denmark", "norway"),
        reference_year=2024,
        factor_keys=("population", "income", "density"),
        factor_year_overrides={},
        country_factor_year_overrides={},
        labels={"en": "Denmark ↔ Norway", "da": "Danmark ↔ Norge", "sv": "Danmark ↔ Norge", "no": "Danmark ↔ Norge"},
        method_note_key="dk_no_2024_beta",
        active=True,
    ),
    "se_no": PairSpec(
        pair_id="se_no",
        countries=("sweden", "norway"),
        reference_year=2024,
        factor_keys=("population", "age65", "education", "income", "density"),
        factor_year_overrides={},
        country_factor_year_overrides={"sweden": {"income": 2023}},
        labels={"en": "Sweden ↔ Norway", "da": "Sverige ↔ Norge", "sv": "Sverige ↔ Norge", "no": "Sverige ↔ Norge"},
        method_note_key="se_no_2024_beta",
        active=True,
    ),
}


def get_pair_spec(pair_id: str) -> PairSpec:
    try:
        return PAIR_SPECS[pair_id]
    except KeyError as exc:
        raise KeyError(f"Unsupported pair: {pair_id}") from exc


def list_pair_specs(*, active_only: bool = False) -> list[PairSpec]:
    specs = list(PAIR_SPECS.values())
    if active_only:
        specs = [spec for spec in specs if spec.active]
    return specs


def pair_label(language: str, pair_id: str) -> str:
    spec = get_pair_spec(pair_id)
    return spec.labels.get(language, spec.labels["en"])


def get_target_country_id(pair_spec: PairSpec, source_country_id: str) -> str:
    if source_country_id not in pair_spec.countries:
        raise KeyError(f"{source_country_id} is not in pair {pair_spec.pair_id}")
    return pair_spec.countries[1] if pair_spec.countries[0] == source_country_id else pair_spec.countries[0]
