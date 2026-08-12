<!-- ⚠️ GENERATED FILE — do not edit by hand. -->
<!-- Edit data/*.yaml and run `python scripts/build.py`. CI rejects hand edits. -->

# Prediction Almanac

[![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)
[![README: generated](https://img.shields.io/badge/README-generated_from_data%2F-blue)](SPEC.md)

> The self-updating almanac of prediction markets — every platform, the data you can actually get out of it, and the tools around them.

**17 platforms · 11 data sources · 20 tools** — generated 2026-08-12 by [`scripts/build.py`](scripts/build.py)

Every entry is a YAML file under [`data/`](data/); this page is a build artifact.
Live columns (volume, stars, health, link liveness) refresh on a schedule — nulls
show as “—” until their refresh pipeline lands ([roadmap](SPEC.md#7-build-order-each-step-ships-something)).

## Contents

- [Platforms](#platforms)
- [Data coverage](#data-coverage) — *which markets you can actually get data out of*
- [Tools](#tools)
- [Contributing](#contributing)
- [Related](#related)

## Platforms

### On-chain markets

| Platform | Type | Since | Volume | Who can trade | Description |
|---|---|---|---|---|---|
| **[Azuro](https://azuro.org)** | AMM · Polygon, Gnosis + | 2022 | — | [🌍 exc. 26 countries](https://gem.azuro.org/terms-of-use) | On-chain betting liquidity protocol that powers third-party sportsbook and prediction frontends. |
| **[Limitless](https://limitless.exchange)** | CLOB · Base | 2024 | — | [🌍 exc. 7 countries](https://docs.limitless.exchange/user-guide/terms-of-service) | Fast-cycle (hourly/daily/weekly) prediction markets on Base, aimed at traders. |
| **[Overtime](https://overtimemarkets.xyz)** | AMM · Optimism, Arbitrum, Base | 2022 | — | [🌍 exc. 13 countries](https://docs.overtime.io/resources/terms-of-use) | Sports-focused on-chain AMM markets from the Thales protocol family. |
| **[Polymarket](https://polymarket.com)** | CLOB · Polygon | 2020 | — | [🌍 exc. 43 countries](https://polymarket.com/tos) | Largest on-chain prediction market; USDC-settled CLOB on Polygon. |
| **[predict.fun](https://predict.fun)** | CLOB · Blast | 2024 | — | [🌍 exc. 13 countries](https://docs.predict.fun/terms-of-service) | Polymarket-style on-chain CLOB prediction market on Blast. |
| **[Zeitgeist](https://zeitgeist.pm)** | AMM · Polkadot parachain | 2022 | — | [🌍 exc. 🇺🇸](https://app.zeitgeist.pm/terms) | Prediction-market parachain in the Polkadot ecosystem with on-chain market governance. |

### Regulated & traditional exchanges

| Platform | Type | Since | Volume | Who can trade | Description |
|---|---|---|---|---|---|
| **[Betfair Exchange](https://www.betfair.com/exchange)** | Regulated exchange | 2000 | — | [licensed countries only](https://support.betfair.com/app/answers/detail/betfair-general-terms-and-conditions/) | The largest betting exchange; politics and current-affairs markets alongside sports. |
| **[ForecastEx](https://forecastex.com)** | Regulated exchange | 2024 | — | [only 🇺🇸🇨🇦🇭🇰🇮🇪](https://www.interactivebrokers.com/en/general/about/mediaRelations/4-1-25.php) | Interactive Brokers' CFTC-regulated event exchange; yes/no contracts on economics and climate. |
| **[Iowa Electronic Markets](https://iem.uiowa.edu)** | Regulated exchange | 1988 | — | [🌍 everyone](https://iemweb.biz.uiowa.edu/faq/) | The original academic real-money market, run by the University of Iowa since 1988. |
| **[Kalshi](https://kalshi.com)** | Regulated exchange | 2021 | — | [🌍 exc. 55 countries](https://kalshi.com/docs/kalshi-member-agreement.pdf) | CFTC-regulated US event-contract exchange spanning politics, economics, weather, and sports. |
| **[PredictIt](https://www.predictit.org)** | Regulated exchange | 2014 | — | [only 🇺🇸](https://www.predictit.org/terms-and-conditions) | Long-running US political research market; capped stakes and a small contract universe. |
| **[Smarkets](https://smarkets.com)** | Regulated exchange | 2008 | — | [🌍 exc. 19 countries](https://help.smarkets.com/hc/en-gb/articles/213469085-Smarkets-Terms-and-Conditions) | UK-licensed betting exchange with notably deep political markets. |

### Play-money markets

| Platform | Type | Since | Who can trade | Description |
|---|---|---|---|---|
| **[Futuur](https://futuur.com)** | Play-money | 2017 | [🌍 exc. 39 countries](https://help.futuur.com/Terms-of-Service-a2f757178971446cba1402b3cdc9a799) | Social prediction markets in play-money and real-money (crypto) flavors. |
| **[Hypermind](https://www.hypermind.com)** | Play-money | 2014 | [🌍 everyone](https://predict.hypermind.com/hypermind/RulesTextPage.html) | Prize-based prediction market and forecasting panel; long-running French-American operation. |
| **[Manifold](https://manifold.markets)** | Play-money | 2021 | [🌍 everyone](https://docs.manifold.markets/terms) | Play-money markets anyone can create; the most open API and data of any platform. |

### Forecasting platforms

| Platform | Type | Since | Who can trade | Description |
|---|---|---|---|---|
| **[Good Judgment Open](https://www.gjopen.com)** | Forecasting | 2015 | [🌍 everyone](https://www.gjopen.com/terms) | Public forecasting tournament from Good Judgment, of Superforecasting fame. |
| **[Metaculus](https://www.metaculus.com)** | Forecasting | 2015 | [🌍 everyone](https://www.metaculus.com/terms-of-use/) | Long-horizon forecasting community with tournaments and track records; aggregates probabilistic forecasts rather than trading. |

*“Who can trade” is factual, per each platform’s own terms (each cell links to its
source; 🌐 permissionless = protocol enforces nothing, official frontends may geoblock) —
not advice, and never guidance around restrictions. Volume is notional USD over the
stated period. Dead or deprecated platforms keep their entry in [`data/`](data/) but
aren’t listed here.*

## Data coverage

What nobody else tracks: whether you can actually **get the data out** — for research,
backtesting, or building. Per platform first, then the concrete sources.

| Platform | Public API | Live book | Historical | Granularity | Free archive | Known gaps |
|---|---|---|---|---|---|---|
| [Azuro](https://azuro.org) | ✓ | — | partial | on-chain (subgraph) | — | Data via subgraphs per chain; no unified archive. |
| [Betfair Exchange](https://www.betfair.com/exchange) | ✓ | ✓ | partial | odds ticks+book | — | Historical exchange data is a separate paid product (historicdata.betfair.com). |
| [ForecastEx](https://forecastex.com) | — | — | none | — | — | Market data flows through Interactive Brokers platforms/APIs; no standalone public data API. |
| [Futuur](https://futuur.com) | ✓ | — | none | current odds | — | API serves current markets/odds; no historical endpoint. |
| [Good Judgment Open](https://www.gjopen.com) | — | — | none | — | — | No public API; forecast data is not exported. |
| [Hypermind](https://www.hypermind.com) | — | — | none | — | — | No public API. |
| [Iowa Electronic Markets](https://iem.uiowa.edu) | — | — | full | daily prices | — | History published as per-market files on the site; no API. |
| [Kalshi](https://kalshi.com) | ✓ | ✓ | partial | trade+candlestick | [prediction-market-analysis](https://github.com/jon-becker/prediction-market-analysis) | History served per-market via API (trades, candlesticks); no official bulk archive. |
| [Limitless](https://limitless.exchange) | ✓ | ✓ | none | live markets+book | — | No historical archive; markets are short-lived by design. |
| [Manifold](https://manifold.markets) | ✓ | — | full | bet-level | — | Full history only via paginated API; rate limits make whole-site pulls slow. |
| [Metaculus](https://www.metaculus.com) | ✓ | — | full | aggregate forecast history | — | Individual forecasts mostly private; aggregates and resolutions are public via API. |
| [Overtime](https://overtimemarkets.xyz) | ✓ | — | partial | on-chain (subgraph) | — | Data via per-chain subgraphs. |
| [Polymarket](https://polymarket.com) | ✓ | ✓ | partial | trade+book | [pmxt](https://pmxt.dev) | No official bulk historical-trade endpoint; third-party archives have day/week gaps on some markets. |
| [predict.fun](https://predict.fun) | ✓ | ✓ | none | live markets+book | — | No historical archive. |
| [PredictIt](https://www.predictit.org) | ✓ | — | none | snapshot quotes | — | Official API is a current-price snapshot only; no historical endpoint. |
| [Smarkets](https://smarkets.com) | ✓ | ✓ | none | live odds+book | — | Trading API requires an account; no public historical archive. |
| [Zeitgeist](https://zeitgeist.pm) | ✓ | — | partial | on-chain (indexer) | — | Data via its own indexer/SDK; no simple REST archive. |

### Sources

| Source | Covers | Kind | Format · granularity | Coverage | Access | Known gaps |
|---|---|---|---|---|---|---|
| **[Betfair Historical Data](https://historicdata.betfair.com)** | betfair | historical-archive | compressed JSON (market ticks) · odds ticks + book | varies by sport/tier (full) | paid | Politics/specials coverage thinner than sports. |
| **[Dune (decoded on-chain tables)](https://dune.com)** | polymarket | dataset | SQL over decoded Polygon tables · on-chain events | 2020–present (full) | gated | Requires writing SQL against raw/decoded contract tables; API export is metered. |
| **[Kalshi Trading API](https://docs.kalshi.com)** | kalshi | live-api | JSON REST + WebSocket · trades, candlesticks, order book | 2021–present (full) | free | Per-market pagination; no bulk download. |
| **[Manifold API](https://docs.manifold.markets/api)** | manifold | live-api | JSON REST · bet-level | 2021–present (full) | free | Rate limits make whole-site pulls slow. |
| **[Metaculus API](https://www.metaculus.com/api/)** | metaculus | live-api | JSON REST · question + aggregate forecast history | 2015–present (full) | free | Individual forecasts mostly private; aggregates and resolutions are public. |
| **[pmxt](https://pmxt.dev)** | polymarket | historical-archive | parquet (hourly) · trade+book | 2024–present (partial) | free | Multi-day/week gaps on some markets. |
| **[Polymarket CLOB API](https://docs.polymarket.com)** | polymarket | live-api | JSON REST + WebSocket · L2 order book, prices, recent trades | live (partial) | free | Live and recent data; not a bulk historical source. |
| **[Polymarket Gamma API](https://gamma-api.polymarket.com)** | polymarket | live-api | JSON REST · markets/events metadata + volumes | 2020–present (full) | free | Metadata and aggregates only — not a trade tape. |
| **[Polymarket subgraph](https://github.com/Polymarket/polymarket-subgraph)** | polymarket | subgraph | GraphQL · on-chain events (trades, positions, redemptions) | 2020–present (full) | free | Requires a hosted indexer (Goldsky) or self-indexing; schemas shift between versions. |
| **[prediction-market-analysis](https://github.com/jon-becker/prediction-market-analysis)** | polymarket, kalshi | dataset | bulk files (see repo) · trade | through 2025 (partial) | free | Point-in-time snapshots; check the repo for freshness. |
| **[PredictIt market data API](https://www.predictit.org/api/marketdata/all/)** | predictit | live-api | JSON (single snapshot endpoint) · current quotes | live snapshot only (partial) | free | No history; unofficial and lightly documented. |

## Tools

### Aggregators

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Adjacent News](https://adj.news)** | polymarket, kalshi, manifold, metaculus | — | — | News and research terminal built around prediction-market data, with a market-data API. |
| **[ElectionBettingOdds](https://electionbettingodds.com)** | polymarket, kalshi, predictit, betfair | — | — | Long-running site charting election odds averaged across real-money markets. |
| **[Metaforecast](https://metaforecast.org)** | polymarket, kalshi, manifold, metaculus, predictit, smarkets, betfair, good-judgment-open, infer | — | — | Meta search engine aggregating forecasts and odds across platforms. |

### Analytics & calibration

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Calibration City](https://calibration.city)** | polymarket, kalshi, manifold, metaculus | — | — | Cross-platform calibration explorer scoring how well market prices predict real outcomes. |
| **[Fatebook](https://fatebook.io)** | — | — | — | Quick personal forecast logging and calibration tracking, from Sage. |

### APIs & SDKs

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[clob-client](https://github.com/Polymarket/clob-client)** | polymarket | — | — | Official TypeScript client for the Polymarket CLOB API. |
| **[forecasting-tools](https://github.com/Metaculus/forecasting-tools)** | metaculus | — | — | Python framework for building LLM forecasting bots, used in Metaculus AI tournaments. |
| **[kalshi-python](https://pypi.org/project/kalshi-python/)** | kalshi | — | — | Official Python SDK for Kalshi's trading API. |
| **[manifoldpy](https://github.com/vluzko/manifoldpy)** | manifold | — | — | Community Python wrapper for the Manifold API. |
| **[prediction-market-agent-tooling](https://github.com/gnosis/prediction-market-agent-tooling)** | polymarket, manifold, omen | — | — | Gnosis toolkit for building AI agents that trade on prediction markets. |
| **[py-clob-client](https://github.com/Polymarket/py-clob-client)** | polymarket | — | — | Official Python client for the Polymarket CLOB API. |

### Bots & agents

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Olas Predict trader](https://github.com/valory-xyz/trader)** | omen | — | — | Autonomous prediction-market trading agent that runs as an on-chain Olas service. |
| **[poly-market-maker](https://github.com/Polymarket/poly-market-maker)** | polymarket | — | — | Reference market-making bot for the Polymarket CLOB. |
| **[Polymarket Agents](https://github.com/Polymarket/agents)** | polymarket | — | — | Official framework for building LLM trading agents on Polymarket. |

### Dashboards

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Polymarket on Dune](https://dune.com/rchen8/polymarket)** | polymarket | — | — | Community Dune dashboard tracking Polymarket volume, users, and market activity on-chain. |

### Infrastructure

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Conditional Token Framework](https://github.com/gnosis/conditional-tokens-contracts)** | polymarket, omen | — | — | Gnosis' ERC-1155 outcome-token standard that Polymarket and Omen settle on. |
| **[ctf-exchange](https://github.com/Polymarket/ctf-exchange)** | polymarket | — | — | Polymarket's audited on-chain exchange contracts for settling CTF outcome tokens. |
| **[Squiggle](https://www.squiggle-language.com)** | — | — | — | Probabilistic estimation language for building and sanity-checking forecasts. |

### Education

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Forecasting Wiki](https://forecasting.wiki)** | — | — | — | Community wiki collecting forecasting concepts, techniques, and platform know-how. |
| **[Quantified Intuitions](https://www.quantifiedintuitions.org)** | — | — | — | Calibration-training games (estimation, pastcasting) from Sage. |

## Contributing

Entries are one YAML file each under [`data/`](data/), validated against
[`schema/`](schema/) — **edit data, never this README**. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the two-minute guide. An issue-form intake bot
(deterministic checks + LLM vetting + auto-merge) is on the
[roadmap](SPEC.md#7-build-order-each-step-ships-something).

## Related

- [PM Atlas](https://pmatlas.xyz) — hosted dashboard mapping the platform landscape.
- [jon-becker/prediction-market-analysis](https://github.com/jon-becker/prediction-market-analysis) — large public Polymarket + Kalshi trade dataset (also listed in [Sources](#sources)).
- [sindresorhus/awesome](https://github.com/sindresorhus/awesome) — the genre this almanac grew out of.

---

_Generated 2026-08-12 from [`data/`](data/). Found something stale or dead? The
refresh bot will too — but [issues](https://github.com/kachence/prediction-almanac/issues) are welcome._
