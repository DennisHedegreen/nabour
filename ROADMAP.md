# nabour roadmap

## Current product read

`nabour` is no longer only a Denmark ↔ Sweden experiment.

It is now being shaped as a Nordic `country-pair matcher`.

That means:

- one pair at a time
- one locked factor set per pair
- one locked reference year per pair
- no fake all-Nordics layer before the data actually supports it

## Active release state

Live now:

- `dk_se`
  - year: `2022`
  - 7 shared factors
- `dk_no`
  - year: `2024`
  - 3 shared factors: `population`, `income`, `population density`
  - explicit beta pair built on the narrow Denmark-Norway overlap that is actually real today
- `se_no`
  - structural year: `2024`
  - factors: `population`, `age65`, `education`, `income`, `population density`
  - live beta with explicit mixed-year note: Sweden `income` uses `2023` latest municipal row while remaining factors stay `2024`

## Next useful pass

v0.2 should:

- lock the pair architecture in code
- keep `dk_se` stable as the broad baseline pair
- carry `dk_no` as a narrower live beta pair instead of leaving Norway fully outside
- carry `se_no` as a live beta with explicit year-mismatch disclosure
- make pair-specific method notes visible in the app

## Non-goals

- one giant Nordic normalization regime
- maps
- user weighting
- lifestyle or politics recommendation language
