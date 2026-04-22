# nabour

A pair-based Nordic municipality matcher from Hedegreen Research.

This repo is a small public-style tool room. It is being reshaped from one hardcoded Denmark ↔ Sweden matcher into a country-pair matcher with explicit pair-specific specs.

## Current scope

- Geography: `municipality`
- Result shape: top `5` matches in the other country of the active pair
- Active pair now:
  - `dk_se`
    - countries: `Denmark` and `Sweden`
    - reference year: `2022`
    - factors: `population`, `age65`, `education`, `income`, `turnout`, `population density`, `cars`
  - `dk_no`
    - countries: `Denmark` and `Norway`
    - reference year: `2024`
    - factors: `population`, `income`, `population density`
    - status: live beta pair built on the narrow Denmark-Norway overlap that is actually real today
- Planned but blocked pairs:
  - `se_no`
  - Norway data is staged locally, and `se_no` stays blocked because Sweden does not currently provide the 2024 municipal rows needed for an honest aligned release.

## What it does

- lets the user choose a country pair
- lets the user choose a source country inside that pair
- lets the user choose a region and municipality
- returns the closest structural municipality matches in the other country
- shows which factors are closest and which still differ

## What it is not

- not a politics ranking
- not a lifestyle recommender
- not a map of culture, language, architecture, or feeling at home
- not a claim that Denmark and Sweden are fully comparable beyond the declared factor layer
- not a weighted personal preference engine

## Data

`nabour` uses a reduced per-pair factor layer in `data/`.

Current factor files:

- `data/denmark/factors/population.csv`
- `data/denmark/factors/age65_pct.csv`
- `data/denmark/factors/education.csv`
- `data/denmark/factors/income.csv`
- `data/denmark/factors/turnout_pct.csv`
- `data/denmark/factors/population_density.csv`
- `data/denmark/factors/cars_per_1000.csv`
- `data/sweden/factors/population.csv`
- `data/sweden/factors/age65_pct.csv`
- `data/sweden/factors/education.csv`
- `data/sweden/factors/income.csv`
- `data/sweden/factors/turnout_pct.csv`
- `data/sweden/factors/population_density.csv`
- `data/sweden/factors/cars_per_1000.csv`
- `data/norway/factors/population.csv`
- `data/norway/factors/age65_pct.csv`
- `data/norway/factors/education.csv`
- `data/norway/factors/income.csv`
- `data/norway/factors/population_density.csv`
- `data/norway/factors/turnout_pct.csv`
- `data/norway/factors/cars_per_1000.csv`

Current active matcher rule:

- `dk_se` uses `2022` as the last clean common full reference year.
- `dk_no` uses a narrower `2024` beta layer built from the real Denmark-Norway overlap: `population`, `income`, `population density`.

Current blocked pair rule:

- `se_no` is still planned around a wider `2024` structural layer, but stays disabled until Sweden exposes the missing annual rows needed to make that pair spec real.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

CLI example:

```bash
python run_match.py --pair dk_se --country denmark --municipality Aarhus
```

## Repo structure

```text
app.py                   Streamlit interface
cross_border_matcher.py  Matching core
data_loader.py           Shared factor normalization layer
income_conversion.py     Sweden ↔ Denmark income harmonization
region_metadata.py       Denmark / Sweden region navigation layer
translations.py          English / Dansk / Svenska text layer
info_content.py          Method and factor notes for the settings menu
run_match.py             Small CLI entrypoint
check_data.py            Coverage check for the locked reference year
check_regions.py         Region navigation sanity check
check_income_conversion.py  Income conversion sanity check
data/                    Local Denmark / Sweden factor layer for this tool
```

## Method guardrails

- This is a structural similarity tool.
- It uses one locked pair spec at a time rather than pretending all Nordic countries are already cleanly comparable.
- Income is harmonized internally for matching, but the UI stays explicit about unit limits.
- The score is an internal distance-based helper, not a claim of objective sameness.

## About

Small cross-border municipality matcher from Hedegreen Research.
