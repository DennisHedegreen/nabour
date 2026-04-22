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

Staged but blocked:

- `se_no`

Why blocked:

- Norway data now exists locally in `nabour/data/norway/factors/`
- `dk_no` became viable only after rebuilding Danish `2024` population and density from official municipality rows
- `se_no` is still blocked because Sweden does not yet expose the matching `2024` municipal rows needed for an honest pair

## Next useful pass

v0.2 should:

- lock the pair architecture in code
- keep `dk_se` stable as the broad baseline pair
- carry `dk_no` as a narrower live beta pair instead of leaving Norway fully outside
- carry `se_no` as an explicit blocked spec instead of a vague future idea
- make pair-specific method notes visible in the app
- keep `se_no` out of the public matcher until the missing Sweden rows are solved
## Non-goals

- fake `se_no` results built on non-aligned years
- one giant Nordic normalization regime
- maps
- user weighting
- lifestyle or politics recommendation language
