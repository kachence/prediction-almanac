<!-- ⚠️ GENERATED FILE — do not edit by hand. -->
<!-- Edit data/*.yaml and run `python scripts/build.py`. CI rejects hand edits. -->

# Prediction Almanac

[![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)
[![README: generated](https://img.shields.io/badge/README-generated_from_data%2F-blue)](SPEC.md)

> The self-updating almanac of prediction markets — every platform, the data you can actually get out of it, and the tools around them.

**15 platforms · 13 data sources · 58 tools** — generated 2026-08-12 by [`scripts/build.py`](scripts/build.py)

Every entry is a YAML file under [`data/`](data/); this page is a build artifact.
Volume, stars, and repo health are measured, not asserted — a “—” means no free,
comparable figure exists, and the entry says why. Link-rot sweeps and the
contribution bot are still to come ([roadmap](SPEC.md#7-build-order-each-step-ships-something)).

## Contents

- [Platforms](#platforms)
- [Data sources](#data-sources) — *archives and feeds worth building on*
- [Tools](#tools)
- [Contributing](#contributing)
- [Related](#related)

## Platforms

### On-chain markets

| Platform | Type | Since | Volume | Who can trade | Description |
|---|---|---|---|---|---|
| **[Polymarket](https://polymarket.com)** | CLOB, Polygon | 2020 | $2.5B/30d | [🌍 exc. 🇺🇸🇬🇧🇨🇦🇦🇺 +39](https://polymarket.com/tos "Cannot trade: United States, United Kingdom, Canada, Australia, Germany, France, Netherlands, Italy, Japan, Singapore, Brazil, Belgium, Burundi, Belarus, DR Congo, +28 more") | Largest on-chain prediction market; USDC-settled CLOB on Polygon. |
| **[predict.fun](https://predict.fun)** | CLOB, Blast | 2024 | $225.7M/30d | [🌍 exc. 🇺🇸🇬🇧🇦🇺🇫🇷 +9](https://docs.predict.fun/terms-of-service "Cannot trade: United States, United Kingdom, Australia, France, Singapore, Belgium, Cuba, Iran, North Korea, Poland, Syria, Thailand, Taiwan") | Polymarket-style on-chain CLOB prediction market on Blast. |
| **[SX Bet](https://sx.bet)** | CLOB, SX Rollup | 2019 | $58.2M/30d | [🌍 exc. 🇺🇸🇬🇧🇦🇺🇩🇪 +19](https://help.sx.bet/en/articles/3613372-terms-and-conditions "Cannot trade: United States, United Kingdom, Australia, Germany, France, Netherlands, Spain, Afghanistan, Austria, Belarus, Cuba, Iraq, Iran, Comoros, North Korea, +8 more") | Peer-to-peer betting exchange with a genuine order book on its own Arbitrum Orbit L2; no house or vig, but every currently active market is sports. |
| **[Limitless](https://limitless.exchange)** | CLOB, Base | 2024 | $48.9M/30d | [🌍 exc. 🇺🇸🇧🇾🇨🇺🇮🇷🇰🇵🇷🇺🇸🇾](https://docs.limitless.exchange/user-guide/terms-of-service#1-eligibility "Cannot trade: United States, Belarus, Cuba, Iran, North Korea, Russia, Syria") | Fast-cycle (hourly/daily/weekly) prediction markets on Base, aimed at traders. |
| **[Myriad](https://myriad.markets)** | CLOB, BNB Chain +3 | 2025 | $2M/30d | [🌍 exc. 🇺🇸🇫🇷🇸🇬🇧🇸 +14](https://help.myriad.markets/myriad-terms-of-use "Cannot trade: United States, France, Singapore, Bahamas, Botswana, Switzerland, Iran, Cambodia, North Korea, Cayman Islands, Libya, Malta, Sudan, Somalia, Syria, +3 more") | Prediction market from Dastan (Decrypt, Rug Radio): an off-chain-matched, on-chain-settled order book on BNB Chain, plus AMM markets on Abstract, Celo, and Linea. |
| **[Rain](https://www.rain.trade)** | CLOB, Arbitrum | 2026 | $815.3k/30d | [❔ unverified](https://www.rain.trade/terms-and-conditions) | Permissionless event markets on Arbitrum settled in USDT0 and matched by on-chain order books, where users create their own politics, sports, and crypto markets. |

### Regulated exchanges & brokers

| Platform | Type | Since | Volume | Who can trade | Description |
|---|---|---|---|---|---|
| **[Kalshi](https://kalshi.com)** | Regulated exchange | 2021 | $10.9B/30d | [🌍 exc. 🇬🇧🇨🇦🇦🇺🇫🇷 +51](https://kalshi.com/docs/kalshi-member-agreement.pdf "Cannot trade: United Kingdom, Canada, Australia, France, Italy, China, India, Singapore, United Arab Emirates, Afghanistan, Angola, Belgium, Burkina Faso, Bulgaria, Bolivia, +40 more") | CFTC-regulated US event-contract exchange spanning politics, economics, weather, and sports. |
| **[Gemini Predictions](https://www.gemini.com/predictions)** | Regulated exchange | 2025 | $38.1M/30d | [only 🇺🇸](https://www.gemini.com/legal/predictions-user-agreement "Can trade: United States") | CFTC-regulated event contracts from Gemini's own DCM affiliate; yes/no and categorical markets on a central limit order book, settled in USD. |
| **[Betfair Exchange](https://www.betfair.com/exchange)** | Regulated exchange | 2000 | — | [🌍 exc. an undisclosed list](https://www.sec.gov/Archives/edgar/data/1635327/000163532726000005/flut-20251231.htm) | The largest betting exchange; politics and current-affairs markets alongside sports. |
| **[IBKR Prediction Markets](https://www.interactivebrokers.com/predictionmarkets/en/home.php)** | Broker → ForecastEx, Kalshi, CME | 2024 | — | [only 🇺🇸🇨🇦🇸🇬🇭🇰](https://www.interactivebrokers.ie/predictionmarkets/en/home.php "Can trade: United States, Canada, Singapore, Hong Kong") | Interactive Brokers' front-end for binary event contracts, routing to its wholly-owned ForecastEx plus Kalshi and CME; the EEA offering is ForecastEx-only and professional-clients-only. |
| **[PredictIt](https://www.predictit.org)** | Regulated exchange | 2014 | — | [only 🇺🇸](https://www.predictit.org/terms-and-conditions "Can trade: United States") | Long-running US political research market; capped stakes and a small contract universe. |
| **[Robinhood Prediction Markets](https://robinhood.com/us/en/prediction-markets/)** | Broker → Kalshi, ForecastEx, Rothera | 2024 | — | [only 🇺🇸](https://robinhood.com/us/en/support/articles/event-contracts-restrictions/ "Can trade: United States") | Robinhood Derivatives, a CFTC-registered FCM, sells binary event contracts in-app and routes the orders to the Kalshi, ForecastEx, and Rothera exchanges. |
| **[Smarkets](https://smarkets.com)** | Regulated exchange | 2008 | — | [🌍 exc. 🇺🇸🇦🇺🇫🇷🇳🇱 +15](https://help.smarkets.com/hc/en-gb/articles/213469085-Smarkets-Terms-and-Conditions "Cannot trade: United States, Australia, France, Netherlands, Italy, China, Belgium, Belarus, Switzerland, Czechia, Denmark, Hong Kong, Kazakhstan, Norway, Portugal, +4 more") | UK-licensed betting exchange with notably deep political markets. |

### Research & play-money venues

*Listed for their data, not for trading. These are the only platforms here with complete, free, public history, which is what you backtest and calibrate against before risking money on the venues above.*

| Platform | Type | Since | Who can trade | Description |
|---|---|---|---|---|
| **[Manifold](https://manifold.markets)** | Play-money | 2021 | [🌍 everyone](https://docs.manifold.markets/terms) | Play-money markets anyone can create; the most open API and data of any platform. |
| **[Metaculus](https://www.metaculus.com)** | Forecasting | 2015 | [🌍 everyone](https://www.metaculus.com/terms-of-use/) | Long-horizon forecasting community with tournaments and track records; aggregates probabilistic forecasts rather than trading. |

*“Who can trade” is factual, per each platform’s own terms — not advice, and never
guidance around restrictions. Hover a cell to name the countries; click it for the terms
it was read from. 🌐 permissionless = the protocol enforces nothing, though official
frontends may still geoblock.*

*Volume is notional USD over the stated period, and a blank means no free, comparable
figure exists — each entry’s known-gaps note says why, since several venues publish only
commission revenue or contract counts, which are not volume. **Don’t total the column:**
brokers route their flow into exchanges listed in the same table, so it would be counted
twice. Dead or deprecated platforms keep their entry in [`data/`](data/) but aren’t
listed here.*

<details>
<summary><b>Considered and not listed</b> — this is a prediction-market directory, so adjacent venues are deliberately out of scope</summary>

| Resource | Why not |
|---|---|
| [Azuro](https://azuro.org) | Sports-betting liquidity protocol powering third-party sportsbooks, not a prediction market venue in its own right. |
| [Overtime](https://overtimemarkets.xyz) | Sports betting (Thales protocol family) with an AMM, not event-outcome prediction markets. |
| [Hyperliquid Outcomes (HIP-4)](https://app.hyperliquid.xyz/outcomes) | Exchange infrastructure rather than a venue in its own right — HIP-4 is an order-book primitive that front-ends build on, and mainnet inventory is a handful of recurring crypto price binaries. |
| [ForecastEx](https://forecastex.com) | A CFTC-licensed exchange that retail cannot access directly; it is the matching venue behind broker front-ends such as IBKR ForecastTrader, which are listed instead. |
| [Iowa Electronic Markets](https://iem.uiowa.edu) | Academic research market with $500 account caps, no API, and negligible volume; of historical interest rather than practical use. |
| [Futuur](https://futuur.com) | Play-money side adds no data or liquidity, and the real-money side is offshore-licensed with 39 countries blocked and no historical API. Nothing in the directory references it. |
| [Hypermind](https://www.hypermind.com) | Prize-based forecasting with no public API and no exportable data, so it offers nothing to a trader or a builder. |
| [Good Judgment Open](https://www.gjopen.com) | No API and no data export. Metaculus covers the same ground with full public forecast history. |

Disagree? [Open an issue](https://github.com/kachence/prediction-almanac/issues) — the reasons live in [`data/excluded.yml`](data/excluded.yml), so changing our mind is a one-line edit.
</details>

## Data sources

Every venue has a live API for its own book — that part is unremarkable. What is worth
tracking is where you get **history you can backtest on**, and the **cross-platform odds
feeds** worth pricing against. A platform missing from this table has nothing better than
its own live endpoints.


| Source | Covers | Kind | Format · granularity | Coverage | Access | Known gaps |
|---|---|---|---|---|---|---|
| **[Betfair Historical Data](https://historicdata.betfair.com)** | betfair | historical-archive | compressed JSON (market ticks) · odds ticks + book | varies by sport/tier (full) | paid | Politics/specials coverage thinner than sports. |
| **[pmxt](https://pmxt.dev)** | polymarket, kalshi, limitless, gemini-predictions, myriad | historical-archive | parquet · trade+book | 2024–present (partial) | free | Multi-day gaps on some markets. Also archives Opinion, which this directory does not yet list. |
| **[Dune (decoded on-chain tables)](https://dune.com)** | polymarket | dataset | SQL over decoded Polygon tables · on-chain events | 2020–present (full) | gated | Requires writing SQL against raw/decoded contract tables; API export is metered. |
| **[prediction-market-analysis](https://github.com/jon-becker/prediction-market-analysis)** | polymarket, kalshi | dataset | compressed bulk dataset (~36GB) · trade | through 2025 (partial) | free | A research framework as much as a dataset — it ships indexers for collecting new data, so freshness depends on running them yourself. |
| **[Betfair Exchange API](https://developer.betfair.com)** | betfair | odds-feed | JSON-RPC / REST · prices and market book | live only (partial) | gated | Needs an account and app key. The free Delayed key omits traded volume entirely, and the GBP 499 Live key forbids read-only data collection. |
| **[ElectionBettingOdds](https://electionbettingodds.com)** | polymarket, kalshi, predictit, betfair, smarkets | odds-feed | HTML (no API) · per-market odds and cumulative matched USD, by venue | election markets only (partial) | free | Scraped from the page, with no API and no time series — figures are cumulative per market rather than per period, and only election markets are covered. |
| **[Pinnacle API](https://github.com/pinnacleapi)** | — | odds-feed | JSON REST · pre-match and live odds, lines, limits | live only (partial) | gated | Account credentials required and no history — Pinnacle is a sharp sportsbook, so this is a pricing benchmark rather than a dataset. |
| **[The Odds API](https://the-odds-api.com)** | — | odds-feed | JSON REST · odds by bookmaker, per market | live + limited history (partial) | free | Free tier is request-capped and historical odds sit behind a paid plan; bookmaker coverage varies by region. |
| **[Polymarket subgraph](https://github.com/Polymarket/polymarket-subgraph)** | polymarket | subgraph | GraphQL · on-chain events (trades, positions, redemptions) | 2020–present (full) | free | Requires a hosted indexer (Goldsky) or self-indexing; schemas shift between versions. |
| **[Gemini Predictions API](https://api.gemini.com/v1/prediction-markets/events)** | gemini-predictions | live-api | JSON REST + WebSocket · daily volume by category; prices, per-event volume; L2 depth over WebSocket | 2025–present (partial) | free | Daily volume is T-1 only and counted in contracts at $1 face; category rows nest, so only top-level rows may be summed. No REST depth snapshot. |
| **[Kalshi Trading API](https://docs.kalshi.com)** | kalshi | live-api | JSON REST + WebSocket · trades, candlesticks, order book | 2021–present (full) | free | Per-market pagination; no bulk download. |
| **[Manifold API](https://docs.manifold.markets/api)** | manifold | live-api | JSON REST · bet-level | 2021–present (full) | free | Rate limits make whole-site pulls slow. |
| **[Metaculus API](https://www.metaculus.com/api/)** | metaculus | live-api | JSON REST · question + aggregate forecast history | 2015–present (full) | free | Individual forecasts mostly private; aggregates and resolutions are public. |

## Tools

### Trading bots & agents

*Running strategies against these venues: market making, arbitrage, and autonomous agents. Read the licence and the code before pointing anything at real money — none of this is audited, and a stale repo is a liability.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[poly-maker](https://github.com/warproxxx/poly-maker)** | polymarket | 1,448 | 2026-07-09 | Maker-only market making on Polymarket CLOB V2: depth-weighted microprice fair value, inventory skew, volatility-widened spreads and a regime state machine. |
| **[CloddsBot](https://github.com/alsk1992/CloddsBot)** | polymarket, kalshi, manifold, metaculus, predict-fun | 663 | 2026-06-26 | Self-hosted autonomous agent spanning prediction markets, perps and DEXs, with Kelly sizing, VaR and CVaR limits and circuit breakers. |
| **[kalshi-ai-trading-bot](https://github.com/ryanfrigo/kalshi-ai-trading-bot)** | kalshi | 569 | 2026-07-06 | Kalshi strategy toolkit with authenticated client, position tracking, paper mode and example strategies whose losing periods the README documents. |
| **[Kalshi Trading Bot CLI](https://github.com/OctagonAI/kalshi-trading-bot-cli)** | kalshi | 369 | 2026-06-25 | CLI that researches a question, forms an independent probability, computes edge against the live book and sizes with Kelly — with a demo mode. |
| **[PolyClaw](https://github.com/chainstacklabs/polyclaw)** | polymarket | 357 | 2026-04-28 | Polymarket agent skill that browses markets and executes on-chain via split plus CLOB, showing the mint path rather than naive taking. |
| **[KalshiMarketMaker](https://github.com/rodlaf/KalshiMarketMaker)** | kalshi | 227 | 2026-04-14 | Avellaneda-Stoikov market making on Kalshi — reservation price, asymmetric quotes and inventory-risk-adjusted sizing, with portfolio caps and Docker deployment. |
| **[Homerun](https://github.com/braedonsaunders/homerun)** | polymarket, kalshi | 168 | 2026-07-04 | Write Python strategies, backtest them on L2 book replay with Cox hazard fill modelling, then run the same code in shadow or live mode. |
| **[Olas Predict trader](https://github.com/valory-xyz/trader)** | omen | 72 | 2026-08-12 | Autonomous prediction-market trading agent that runs as an on-chain Olas service. |
| **[polymm](https://github.com/kachence/polymm)** | polymarket | 72 | 2026-07-22 | Sports market-making and arbitrage bot for Polymarket: de-vigs sportsbook odds, quotes both sides, and hedges the fills. |
| **[poly-market-maker](https://github.com/Polymarket/poly-market-maker)** | polymarket | 321 | 2024-07-05 · stale | Reference market-making bot for the Polymarket CLOB. |
| **[Polymarket Agents](https://github.com/Polymarket/agents)** | polymarket | 3,767 | 2024-11-05 · archived | Official framework for building LLM trading agents on Polymarket. |

### Cross-venue search & arbitrage

*Finding where an event trades at all, and where it trades at a different price — which is where most of the edge in this space actually lives.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Polymarket Alpha Bot](https://github.com/chainstacklabs/polymarket-alpha-bot)** | polymarket | 169 | 2026-08-05 | Finds covering portfolios across logically related markets by extracting implications, validating them, then pricing the trade on live quotes. |
| **[Adjacent News](https://adj.news)** | polymarket, kalshi, manifold, metaculus | — | — | News and research terminal built around prediction-market data, with a market-data API. |
| **[Chironus Scanner](https://chironus.com/scanner)** · freemium | polymarket, kalshi | — | — | Scanner across all live Polymarket and Kalshi markets with category, volume, price-band and time-to-close filters; free tier serves delayed prices. |
| **[ElectionBettingOdds](https://electionbettingodds.com)** | polymarket, kalshi, predictit, betfair | — | — | Long-running site charting election odds averaged across real-money markets. |
| **[Prediction Market News](https://predictionmarketnews.org)** | polymarket, kalshi | — | — | Cross-venue screener over 10,752 matched Polymarket and Kalshi markets, showing consensus odds, per-venue spread, open interest, depth and resolution rules. |
| **[Predicts.guru](https://www.predicts.guru)** | polymarket, kalshi, limitless | — | — | No-login wallet checker, smart-money radar and live trade feed, plus an arbitrage scanner matching Polymarket against Kalshi and Limitless. |
| **[Metaforecast](https://metaforecast.org)** | polymarket, kalshi, manifold, metaculus, predictit, smarkets, betfair, infer | 68 | 2025-02-09 · archived | Meta search engine aggregating forecasts and odds across platforms. |

### Dashboards & market data

*Watching flow, positions, and volume without building your own pipeline.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Dune: Kalshi Overview](https://dune.com/datadashboards/kalshi-overview)** | kalshi | — | — | Dedicated Kalshi dashboard covering exchange volume, trade counts and activity trends, without a research-platform subscription. |
| **[Dune: Prediction Markets](https://dune.com/datadashboards/prediction-markets)** | polymarket, kalshi, limitless, myriad, predict-fun | — | — | Multi-venue on-chain dashboard covering weekly volume, trade counts, open interest and unique users across seven venues — the broadest free venue-share view. |
| **[Polyguana](https://polyguana.com)** | polymarket | — | — | Live rankings across 157k Polymarket markets with 24h movers, a category heatmap, watchlist alerts and a resolved-market archive. |
| **[Polymarket on Dune](https://dune.com/rchen8/polymarket)** | polymarket | — | — | Community Dune dashboard tracking Polymarket volume, users, and market activity on-chain. |
| **[Resolve Markets](https://resolvemarkets.com)** · freemium | polymarket, kalshi, predict-fun, predictit, manifold | — | — | Multi-venue suite with separate Kalshi, Polymarket and predict.fun dashboards, whale watch, contract comparison and a purpose-built negative-risk tool. |

### Analytics & calibration

*Judging whether prices are any good — accuracy scoring, calibration curves, and personal forecast tracking.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Squiggle](https://www.squiggle-language.com)** | — | 218 | 2026-08-11 | Probabilistic estimation language for building and sanity-checking forecasts. |
| **[Fatebook](https://fatebook.io)** | — | 60 | 2026-06-12 | Quick personal forecast logging and calibration tracking, from Sage. |
| **[Calibration City](https://calibration.city)** | polymarket, kalshi, manifold, metaculus | — | — | Cross-platform calibration explorer scoring how well market prices predict real outcomes. |
| **[Dune: How Accurate Is Polymarket](https://dune.com/alexmccullough/how-accurate-is-polymarket)** | polymarket | — | — | Dune dashboard measuring Polymarket's realised accuracy, bias and outcome distribution against resolved markets — forkable and re-queryable. |
| **[OVERROUND](https://www.overround.pro)** · freemium | polymarket | — | — | Skill-adjusted forecaster leaderboard scoring every on-chain fill against the price paid, with a free public calibration page over 8.9M scored fills. |
| **[Polysights](https://www.polysights.xyz)** · freemium | polymarket | — | — | Polymarket analytics suite: market screener, trader and portfolio analytics, a sharp-wallet scanner, and API, MCP and CLI access. |

### Data tooling

*Paid research infrastructure. Listed because reconstructing historical book depth is the one thing no free source in this directory does.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Probalytics](https://probalytics.io)** · paid | polymarket | — | — | Millisecond-granularity Polymarket history — full orderbook snapshots, fills and metadata via ClickHouse SQL, REST or Parquet export. From $39/mo. |

### APIs, SDKs & CLIs

*The connection layer. Only current, maintained clients are listed — a superseded SDK costs more time than it saves.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[CCXT](https://github.com/ccxt/ccxt)** | polymarket, kalshi, limitless, myriad | 43,609 | 2026-08-12 | The long-established unified trading library, which now lists Polymarket, Kalshi, Limitless and Myriad alongside 100+ crypto exchanges across seven languages. |
| **[polymarket-cli](https://github.com/Polymarket/polymarket-cli)** | polymarket | 2,847 | 2026-05-26 | Official Rust CLI to browse markets, place orders and manage positions from a terminal, or drive them as a JSON API from scripts and agents. |
| **[PMXT SDK](https://github.com/pmxt-dev/pmxt)** | polymarket, kalshi, limitless, myriad, metaculus, gemini-predictions | 2,077 | 2026-07-18 | CCXT-style unified API across 14+ prediction markets, with Python and TypeScript SDKs, a CLI, and MCP integration — one integration instead of fourteen. |
| **[pykalshi](https://github.com/arshka/pykalshi)** | kalshi | 120 | 2026-07-29 | Unofficial Kalshi client with order amend/cancel, WebSocket book and trade feeds, Pydantic models, typed errors and pandas integration. |
| **[Polymarket py-sdk](https://github.com/Polymarket/py-sdk)** | polymarket | 95 | 2026-08-12 | Official unified Python SDK — public data, authenticated account, trading, builder attribution and wallet workflows in one package. |
| **[forecasting-tools](https://github.com/Metaculus/forecasting-tools)** | metaculus | 76 | 2026-08-09 | Python framework for building LLM forecasting bots, used in Metaculus AI tournaments. |
| **[prediction-market-agent-tooling](https://github.com/gnosis/prediction-market-agent-tooling)** | polymarket, manifold, omen | 58 | 2026-04-22 | Gnosis toolkit for building AI agents that trade on prediction markets. |
| **[manifoldpy](https://github.com/vluzko/manifoldpy)** | manifold | 41 | 2026-07-10 | Community Python wrapper for the Manifold API. |
| **[Polymarket ts-sdk](https://github.com/Polymarket/ts-sdk)** | polymarket | 29 | 2026-08-12 | Official unified TypeScript SDK, the JS counterpart to py-sdk and the current replacement for the archived clob-client. |
| **[kalshi-python](https://pypi.org/project/kalshi-python/)** | kalshi | — | — | Official Python SDK for Kalshi's trading API. |

### Protocol internals

*Settlement mechanics rather than convenience tooling. Relevant if you hedge by splitting and merging outcome tokens, or you are building execution that touches the contracts directly.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[ctf-exchange-v2](https://github.com/Polymarket/ctf-exchange-v2)** | polymarket | 75 | 2026-08-03 | Polymarket's current core contracts: operator-driven order matching over Conditional Token Framework assets, superseding the archived v1. |
| **[Conditional Token Framework](https://github.com/gnosis/conditional-tokens-contracts)** | polymarket, omen | 305 | 2023-01-24 · stale | Gnosis' ERC-1155 outcome-token standard Polymarket settles on — the split and merge mechanics you use to hedge or construct a position from collateral. |

### Research

*Mostly papers, because that is the actual shape of this field: the 2026 academic output is free, unusually trader-relevant, and better than any venue's "learn" page. Order-book microstructure, maker-versus-taker returns, calibration by domain and horizon, and measured arbitrage capacity.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Arbitrage Analysis in Polymarket NBA Markets](https://arxiv.org/abs/2605.00864)** | polymarket | — | — | 75M book snapshots over 173 NBA games: only 7 executable single-market arbs with a median 3.6s life, and combinatorial episodes mostly capped near 15 shares. |
| **[Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics](https://arxiv.org/abs/2602.19520)** | kalshi, polymarket | — | — | 353M trades across 429k Kalshi and Polymarket contracts, mapping where prices are systematically wrong — political markets stay compressed toward 50%. |
| **[Interpreting Prediction Market Prices as Probabilities](https://www.nber.org/system/files/working_papers/w12200/w12200.pdf)** | — | — | — | Derives when a market price equals mean belief, and the wedge that risk aversion and belief heterogeneity create — that is, when 60c is not 60%. |
| **[Logarithmic Market Scoring Rules](https://mason.gmu.edu/~rhanson/mktscore.pdf)** | — | — | — | Hanson's LMSR — a scoring rule doubling as a bounded-loss automated market maker, and the pricing engine behind most subsidised event markets. |
| **[Makers and Takers: The Economics of the Kalshi Prediction Market](https://www2.gwu.edu/~forcpgm/2026-001.pdf)** | kalshi | — | — | Transaction-level study of 300k+ Kalshi contracts: a strong favorite-longshot bias after fees, and higher realised returns for makers than for takers. |
| **[Optimal Market Making in Prediction Markets](https://arxiv.org/abs/2607.17991)** | — | — | — | Derives optimal bid and ask quotes for binary event contracts via an HJB equation, handling inventory and terminal settlement risk — the binary analogue of Avellaneda-Stoikov. |
| **[Prediction Markets (Wolfers & Zitzewitz, JEP 2004)](https://www.nber.org/system/files/working_papers/w10504/w10504.pdf)** | — | — | — | The founding survey: how markets aggregate dispersed information, and which contract design extracts a probability versus a mean versus a median. |
| **[Price Discovery Across Political Prediction Markets](https://web.bogazici.edu.tr/torul/pridis.pdf)** | polymarket, kalshi, betfair, predictit | — | — | Information shares across nine venues trading the 2024 US presidential outcome: Polymarket and Betfair hold ~85%, and the consensus led S&P 500 futures on election night. |
| **[Prices, Probabilities, and Parlays: Systematic Bias in Sports Prediction Markets](https://arxiv.org/abs/2607.14430)** | kalshi | — | — | 23M Kalshi moneyline trades: calibration holds mid-contract but breaks in the final ten minutes, and cross-game parlays are overpriced relative to their legs. |
| **[SoK: Market Microstructure for Decentralized Prediction Markets](https://arxiv.org/abs/2510.15612)** | — | — | — | Systematization of prediction-market design: CLOB versus AMM and LMSR mechanics, and which design stage introduces resolution risk. |
| **[Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf)** | — | — | — | The canonical treatment of strictly proper scoring rules — logarithmic, Brier, spherical, CRPS — and the mathematical parent of the LMSR. |
| **[The Anatomy of a Decentralized Prediction Market](https://arxiv.org/abs/2604.24366)** | polymarket | — | — | Microstructure of 30bn Polymarket book events — longshot spread premium, ~1% wash trading, and a warning that trade direction inferred from the public book is only ~59% accurate. |

### Docs & training

*Platform documentation worth reading and the two calibration-practice sites that exist. We looked for newsletters and podcasts and found none current enough to list, which is itself worth knowing.*

| Tool | Covers | Stars | Last commit | Description |
|---|---|---|---|---|
| **[Forecasting Wiki](https://forecasting.wiki)** | — | — | — | Community wiki collecting forecasting concepts, techniques, and platform know-how. |
| **[IBKR Campus: Predictive Markets](https://www.interactivebrokers.com/campus/traders-academy/predict-market/)** | ibkr | — | — | Two free CFA-accredited courses on event contracts and how they settle — genuinely structured, but explicitly beginner level. |
| **[Polymarket Documentation](https://docs.polymarket.com)** | polymarket | — | — | Order-book mechanics, fees and market-making operations — and the only platform-native page teaching resolution risk: bond sizes, dispute windows and 50/50 fallbacks. |
| **[Quantified Intuitions](https://www.quantifiedintuitions.org)** | — | — | — | Calibration-training games (estimation, pastcasting) from Sage. |

## Contributing

Entries are one YAML file each under [`data/`](data/), validated against
[`schema/`](schema/) — **edit data, never this README**. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the two-minute guide. An issue-form intake bot
(deterministic checks + LLM vetting + auto-merge) is on the
[roadmap](SPEC.md#7-build-order-each-step-ships-something).

## Related

- [PM Atlas](https://pmatlas.xyz) — hosted dashboard mapping the platform landscape.
- [jon-becker/prediction-market-analysis](https://github.com/jon-becker/prediction-market-analysis) — large public Polymarket + Kalshi trade dataset (also listed under [Data sources](#data-sources)).
- [sindresorhus/awesome](https://github.com/sindresorhus/awesome) — the genre this almanac grew out of.

---

_Generated 2026-08-12 from [`data/`](data/). Found something stale or dead? The
refresh bot will too — but [issues](https://github.com/kachence/prediction-almanac/issues) are welcome._
