# Contributing

Thanks for adding to the almanac. One rule above all: **the README is generated — edit
`data/`, never `README.md`.** CI rejects hand-edited READMEs.

## Add or fix an entry (the two-minute version)

1. Pick the type: `data/platforms/` (somewhere people trade/forecast),
   `data/tools/` (built on top), or `data/sources/` (a way to get data out).
2. Copy the closest existing file — [`data/platforms/polymarket.yaml`](data/platforms/polymarket.yaml)
   is the annotated exemplar. Filename must equal the `slug`.
3. Leave every field under `metrics:` / `github:` as `null` — the refresh bot owns those.
4. Rebuild and validate:

   ```sh
   pip install -r requirements.txt
   python scripts/build.py          # regenerates README.md
   python scripts/build.py --check  # what CI runs
   ```

5. Open a PR containing the data file **and** the regenerated `README.md`.

An issue-form submission flow (bot-vetted, auto-merged) is coming — see
[SPEC.md](SPEC.md). Until then, direct PRs are the path.

## House style

- **Descriptions:** one factual sentence, ≤200 chars, no marketing superlatives unless
  measurable ("largest by volume" only if it is).
- **`geo.us_access`:** factual "who may trade" per the platform's own terms —
  never workarounds or evasion guidance.
- **`data.known_gaps`:** be specific ("no bulk trade endpoint; archives have week-long
  gaps"), it's the most valuable field in the repo.
- **Dead things stay listed** (status `deprecated`/`dead`) when historically relevant —
  point `url` somewhere durable, e.g. the GitHub org.

## What gets an entry

Platforms with real usage (any mechanism, including play-money and forecasting sites);
tools that work today against a listed platform; sources that a stranger can actually
access. Broken links, pure marketing pages, and copies of existing entries get pruned.
