# Contributing

Two ways in. Open an issue with a link and I'll do the rest, or send a PR that touches
`data/` only.

**Never edit `README.md`.** It's generated from `data/` and rebuilt automatically after
every merge. Edit it and the next build overwrites you, and your PR conflicts with every
other open PR for no reason at all.

## Open an issue

[Use the form](../../issues/new?template=submit-resource.yml). Paste a link, answer four
questions. You don't need git, Python, or to know what a slug is.

## Or send a PR

1. Pick the folder: `data/platforms/`, `data/sources/` or `data/tools/`.
2. Copy the nearest existing file. [`data/platforms/polymarket.yaml`](data/platforms/polymarket.yaml)
   is the annotated one. The filename has to match the `slug`.
3. Leave `metrics:`, `github:` and `last_post:` as `null`. The refresh bot owns those and
   will overwrite anything you put there.
4. Check it before you push:

   ```sh
   pip install -r requirements.txt
   python scripts/build.py --validate
   ```

5. Open the PR with data files only. No `README.md` in the diff. CI runs the same
   `--validate` and nothing else.

## What gets an entry

Concrete rules per section, so nobody has to guess what I'll say no to.

### Platforms

It trades contracts on the outcome of a real event, and it settles them. Order books
preferred, AMMs fine.

Sportsbooks and casinos are out, even on-chain. If there's a house on the other side of
your bet, this isn't the list. Exchanges retail can't reach directly are also out: those
belong inside the broker's entry, not their own row.

Dead venues keep their file with `status: dead` and stop rendering. Don't delete them,
other entries cross-link them.

### Datasets

History you can backtest on, that you can download or query.

It has to beat the venue's own live endpoints. Every exchange has an API for its own
book and a row saying so helps nobody. State the licence. No licence means default
copyright, so you can't build a business on it, and I'd rather that sat in the table
than have you find out afterwards.

### Odds and reference feeds

Something you can turn into a fair probability and then hold up against a market price.
Sportsbook odds, weather ensembles, whatever the contract actually resolves on.

Free, or with a free tier you can really build on.

### Tools: trading bots, agents and execution

Working strategy or execution code, with a licence file, pointed at a venue on this list.

Out: tutorials, scrapers with no strategy, and anything whose README promises returns.
Stars get gamed hard in this niche. A repo with 200 stars and four commits is an advert,
not a tool.

### Tools: cross-venue search and arbitrage

It compares the same event across at least two listed venues and shows you the gap.

### Tools: dashboards and market data

It loads, it shows live data, and it doesn't hide everything behind a signup. Freemium
is fine as long as the entry says so.

### Tools: data tooling

Paid is allowed here, but only if it does something nothing free on the page can. There
is exactly one entry in that section, which should tell you how narrow the gate is.

### Research

Free to read, at a URL that will still work next year, with a finding you could act on.

A survey of the field isn't enough. "Political markets sit compressed toward 50%" is a
finding. "Prediction markets aggregate information" is a citation.

### Blogs

It has a feed. No feed, no entry, because `last_post` is measured rather than claimed
and a blog I can't measure will quietly rot in the table.

Free, still posting within the last three months, not owned by an exchange.

### X accounts

The bar is highest here, because nothing checks these. X ended its free API tier in
February 2026, so I can't confirm an account is even still alive. That means outside
coverage, or a track record somebody else has written about. Follower counts prove
nothing.

## Submitting your own work

Encouraged. Tick the box on the form so it's on the record. The bar doesn't move: it has
to be real, work today, and do something the list doesn't already cover.

## House style

- **Descriptions:** one sentence, 200 characters, factual. No superlative you can't
  measure. "Largest by volume" only if it is.
- **`geo`:** what the platform's own terms say about who may trade, with a `source` link
  and an `as_of` date. Never workarounds or evasion.
- **`known_gaps`:** the most useful field in the repo. "No bulk trade endpoint, and
  third-party archives drop whole weeks" beats "limited data".
- **Punctuation:** plain hyphens and straight quotes. No em dashes anywhere.

If you think something already in [`data/excluded.yml`](data/excluded.yml) deserves a
place after all, say so in an issue. Changing my mind is a one-line edit.
