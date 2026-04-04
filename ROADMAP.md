# nabour roadmap

## v0.1 goal

Ship a small, honest Denmark <-> Sweden municipality matcher based on shared
structural indicators only.

The tool should:

- let the user choose source country
- let the user choose source municipality
- return the top 5 closest municipalities in the other country
- explain each match with similar and different factors

This is not a politics ranking and not a lifestyle recommender.

`nabour` should be treated as its own tool, not as a feature branch inside
another project.

## Locked v0.1 scope

- Denmark <-> Sweden only
- municipality-level matching only
- 7 shared factors only:
  - population
  - age65
  - education
  - income
  - turnout
  - population density
  - cars
- simple explainable normalization
- distance-based matching
- no sliders
- no user weighting
- no advanced filtering

## Locked v0.1 interaction flow

The front flow should stay as simple as possible:

1. choose source country
2. choose region and municipality
3. see the top 5 closest structural matches in the other country
4. open any match to inspect all 7 factors

Rules:

- the first screen should be minimal
- no long explanation on entry
- region is navigation help only, not part of the matching method
- full factor visibility should exist in the detail layer
- nothing important should be hidden behind a fake smart score

## Active UI direction

- `nabour` should read as a quiet Hedegreen tool
- the first screen should stay centered and almost empty
- the public surface should use ordinary language before method language
- the technical method layer should live in one small global settings menu
- the app should carry one shared language switch:
  - English
  - Dansk
  - Svenska

## Proposed method

1. Load the Denmark and Sweden factor files from `data/`.
2. Normalize both countries into one shared municipality-vector shape.
3. Pick one common reference year for v0.1.
4. Standardize the shared factors.
5. Harmonize Sweden `income` into a real money scale before standardization:
   - `price-base-amounts -> SEK`
   - `SEK -> locked 2022 DKK motor scale`
6. Compute cross-border similarity with Euclidean distance.
7. Convert distance into one simple internal score for display.
8. Derive:
   - top 3 most similar factors
   - top 3 most different factors

## v0.1 build order

### 1. Data normalization

Goal:
- turn the factor CSVs into one clean shared table per country

Tasks:
- map Denmark raw factor files into canonical factor ids
- map Sweden raw factor files into canonical factor ids
- choose the shared reference year
- add one small local region metadata layer for Denmark and Sweden
- confirm municipality naming is stable enough for matching output
- document any dropped rows or missing values

Deliverable:
- one transformation layer producing municipality vectors for both countries
- one region -> municipality navigation layer for the UI

### 2. Matching core

Goal:
- make the similarity calculation reliable and reusable

Tasks:
- clean up `cross_border_matcher.py`
- standardize vectors across the shared cross-border pool
- compute distances
- return sorted top 5 matches
- generate:
  - score
  - similar factors
  - different factors

Deliverable:
- one matcher function that works Denmark -> Sweden and Sweden -> Denmark

### 3. Sanity checks

Goal:
- catch obviously broken results before any UI

Tasks:
- verify both directions work
- test a few obvious urban cases
- test a few more rural cases
- inspect suspicious outputs manually

Deliverable:
- small validation script or tests

### 4. Minimal interface

Goal:
- make the matcher usable without redesigning a whole app

Tasks:
- choose a tiny shell:
  - CLI first, or
  - very small Streamlit page
- add:
  - source country screen
  - region + municipality selection screen
  - results screen
  - expandable or drill-in factor details
- keep the first screen almost empty
- keep explanation secondary, not front-loaded

Deliverable:
- first usable v0.1 interface

### 5. Trust pass

Goal:
- make sure the tool does not overclaim

Tasks:
- review labels and copy
- remove misleading phrasing
- explain what the score is and what it is not
- note the limits of structural matching

Deliverable:
- v0.1 that is honest enough to show someone else

## Out of scope for v0.1

- Norway, Finland, or more countries
- politics-based matching
- personal preference matching
- maps
- user-adjusted weights
- saved comparisons
- recommendation language like "best place for you"
- deeper causal interpretation

## Definition of done for v0.1

`nabour` is at v0.1 when:

- the local data is transformed into shared municipality vectors
- the matcher returns plausible top 5 results both ways
- the explanation layer works
- the UI is simple and usable
- the copy stays structurally honest
