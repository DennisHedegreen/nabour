# nabour

A Denmark ↔ Sweden municipality matcher based on shared structural indicators.

This repo is a small public-style tool room from Hedegreen Research.
It compares municipalities across the two countries using one narrow shared factor set and returns the closest structural matches in the other country.

## Current scope

- Countries: `Denmark` and `Sweden`
- Geography: `municipality`
- Reference year: `2022`
- Result shape: top `5` matches in the other country
- Current shared factors: `population`, `age65`, `education`, `income`, `turnout`, `population density`, `cars`

## What it does

- lets the user choose a source country
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

`nabour` uses a reduced Denmark / Sweden factor layer in `data/`, limited to the 7 shared indicators needed for the matcher.

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

The current matcher assumes that `2022` is the last clean common full reference year for the shared v0.1 factor set.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

CLI example:

```bash
python run_match.py --country denmark --municipality Aarhus
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
- It uses one narrow shared factor layer rather than pretending to know everything about a place.
- Income is harmonized internally for matching, but the UI stays explicit about unit limits.
- The score is an internal distance-based helper, not a claim of objective sameness.

## About

Small cross-border municipality matcher from Hedegreen Research.
