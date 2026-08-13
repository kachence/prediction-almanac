<!-- ⚠️ GENERATED FILE — do not edit by hand. -->
<!-- Edit data/*.yaml and run `python scripts/build.py`. CI rejects hand edits. -->

# Prediction Almanac

[![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)
[![README: generated](https://img.shields.io/badge/README-generated_from_data%2F-blue)](SPEC.md)

> The self-updating almanac of prediction markets — where to trade, the datasets and feeds to build against, and the tools people have actually published.

**15 platforms · 10 data sources · 39 tools** — generated 2026-08-13 by [`scripts/build.py`](scripts/build.py)

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

A market maker or informed taker needs three things beyond a venue: **a dataset** to
evaluate a strategy on before risking money, **a feed** to derive a fair probability
from, and the tools below. Platform APIs are deliberately absent — every venue has one
for its own book, and they are linked from the platform tables above.

### Datasets

*History to backtest against.*

| Dataset | Covers | Format · granularity | Coverage | Known gaps |
|---|---|---|---|---|
| **[Kalshi trades (TrevorJS)](https://huggingface.co/datasets/TrevorJS/kalshi-trades)** | kalshi | parquet · trades + market metadata with outcomes | 2021-06–2026-01 (full) | Stops January 2026 and has not been updated since. No order book. |
| **[pmxt archive](https://archive.pmxt.dev/)** | polymarket, kalshi, limitless | parquet · hourly order-book snapshots | 2026–present (partial) | Per-venue start dates differ — Polymarket from February 2026, Kalshi and Limitless from May. Polymarket splits into v1 and v2 across the CLOB migration. Also archives Opinion, a venue this directory does not list. |
| **[Polymarket aligned tape (TimeSeventeen)](https://huggingface.co/datasets/TimeSeventeen/Polymarket-v1)** | polymarket | parquet · trades with resolution, fees and event-normalised probability | 2022-11–2026-04, v2 continues to date (full) | Needs the companion v2 repo for coverage past the April 2026 migration. Do not pool binary, up-down and NegRisk markets without checking category. |
| **[Polymarket L2 depth (vpcapitano)](https://huggingface.co/datasets/vpcapitano/polymarket-genesis-liquidity)** | polymarket | parquet · 10-level book depth, spread, best bid/ask | 2025-10–2026-03 (partial) | Six months only, and no resolution column — join outcomes yourself. |
| **[prediction-market-analysis](https://github.com/jon-becker/prediction-market-analysis)** | polymarket, kalshi | compressed bulk dataset (~36GB) · trade | through 2025 (partial) | A research framework as much as a dataset — it ships indexers for collecting new data, so freshness depends on running them yourself. |

### Odds & reference feeds

*Inputs for computing a fair probability, then comparing it against the market's price.*

| Feed | Prices | Format · granularity | Coverage | Known gaps |
|---|---|---|---|---|
| **[Betfair Exchange](https://developer.betfair.com)** | Sports and politics | JSON-RPC / REST · prices and market book; historical as market ticks | live, plus a separate historical archive (partial) | Needs an account and app key. The free Delayed key omits traded volume, and the GBP 499 Live key forbids read-only data collection. History is a separate paid product at historicdata.betfair.com, with politics coverage thinner than sports. |
| **[ElectionBettingOdds](https://electionbettingodds.com)** | Elections | HTML (no API) · per-market odds and cumulative matched USD, by venue | election markets only (partial) | Scraped from the page, with no API and no time series — figures are cumulative per market rather than per period, and only election markets are covered. |
| **[Open-Meteo](https://open-meteo.com)** | Weather | JSON REST · hourly forecast, ensemble members, historical reanalysis | 1940–present, plus forecasts (full) | Non-commercial use is free without a key; commercial use needs a paid plan. Ensembles are raw members, so you compute the probability yourself. |
| **[Pinnacle API](https://github.com/pinnacleapi)** | Sports | JSON REST · pre-match and live odds, lines, limits | live only (partial) | Account credentials required, and no history — Pinnacle is a sharp sportsbook, so this is a pricing benchmark rather than a dataset. |
| **[The Odds API](https://the-odds-api.com)** | Sports | JSON REST · odds by bookmaker, per market | live + limited history (partial) | The free tier is request-capped and keyed; historical odds sit behind a paid plan, and bookmaker coverage varies by region. |

*This list is deliberately short — a directory that lists everything is as useless as one
that lists nothing. But short lists carry the taste of whoever wrote them, so if you price
against something that belongs here,
[suggest it](https://github.com/kachence/prediction-almanac/issues).*

## Tools

### Trading bots, agents & execution

*Running strategies against these venues: market making, arbitrage, autonomous agents, and the cross-venue layers you execute through. Read the licence and the code before pointing anything at real money — none of this is audited, and a stale repo is a liability.*

| Tool | Covers | Status | Description |
|---|---|---|---|
| **[CCXT](https://github.com/ccxt/ccxt)** | polymarket, kalshi, limitless, myriad | 43,615★ · 2026-08-13 | The long-established unified trading library, which now lists Polymarket, Kalshi, Limitless and Myriad alongside 100+ crypto exchanges across seven languages. |
| **[PMXT SDK](https://github.com/pmxt-dev/pmxt)** | polymarket, kalshi, limitless, myriad, metaculus, gemini-predictions | 2,077★ · 2026-07-18 | CCXT-style unified API across 14+ prediction markets, with Python and TypeScript SDKs, a CLI, and MCP integration — one integration instead of fourteen. |
| **[poly-maker](https://github.com/warproxxx/poly-maker)** | polymarket | 1,447★ · 2026-07-09 | Maker-only market making on Polymarket CLOB V2: depth-weighted microprice fair value, inventory skew, volatility-widened spreads and a regime state machine. |
| **[CloddsBot](https://github.com/alsk1992/CloddsBot)** | polymarket, kalshi, manifold, metaculus, predict-fun | 676★ · 2026-06-26 | Self-hosted autonomous agent spanning prediction markets, perps and DEXs, with Kelly sizing, VaR and CVaR limits and circuit breakers. |
| **[kalshi-ai-trading-bot](https://github.com/ryanfrigo/kalshi-ai-trading-bot)** | kalshi | 570★ · 2026-07-06 | Kalshi strategy toolkit with authenticated client, position tracking, paper mode and example strategies whose losing periods the README documents. |
| **[Kalshi Trading Bot CLI](https://github.com/OctagonAI/kalshi-trading-bot-cli)** | kalshi | 369★ · 2026-06-25 | CLI that researches a question, forms an independent probability, computes edge against the live book and sizes with Kelly — with a demo mode. |
| **[PolyClaw](https://github.com/chainstacklabs/polyclaw)** | polymarket | 357★ · 2026-04-28 | Polymarket agent skill that browses markets and executes on-chain via split plus CLOB, showing the mint path rather than naive taking. |
| **[KalshiMarketMaker](https://github.com/rodlaf/KalshiMarketMaker)** | kalshi | 227★ · 2026-04-14 | Avellaneda-Stoikov market making on Kalshi — reservation price, asymmetric quotes and inventory-risk-adjusted sizing, with portfolio caps and Docker deployment. |
| **[Polymarket Alpha Bot](https://github.com/chainstacklabs/polymarket-alpha-bot)** | polymarket | 169★ · 2026-08-05 | Finds covering portfolios across logically related markets by extracting implications, validating them, then pricing the trade on live quotes. |
| **[Homerun](https://github.com/braedonsaunders/homerun)** | polymarket, kalshi | 168★ · 2026-07-04 | Write Python strategies, backtest them on L2 book replay with Cox hazard fill modelling, then run the same code in shadow or live mode. |
| **[Olas Predict trader](https://github.com/valory-xyz/trader)** | polymarket, omen | 72★ · 2026-08-12 | Autonomous trading agent shipped as an on-chain Olas service, with separate strategies for Polymarket on Polygon and Omen on Gnosis. |
| **[polymm](https://github.com/kachence/polymm)** | polymarket | 72★ · 2026-07-22 | Sports market-making and arbitrage bot for Polymarket: de-vigs sportsbook odds, quotes both sides, and hedges the fills. |
| **[prediction-market-agent-tooling](https://github.com/gnosis/prediction-market-agent-tooling)** | polymarket, manifold, omen | 58★ · 2026-04-22 | Gnosis toolkit for building AI agents that trade on prediction markets. |

### Cross-venue search & arbitrage

*Finding where an event trades at all, and where it trades at a different price — which is where most of the edge in this space actually lives.*

| Tool | Covers | Access | Description |
|---|---|---|---|
| **[Prediction Market News](https://predictionmarketnews.org)** | polymarket, kalshi | free | Cross-venue screener over 10,752 matched Polymarket and Kalshi markets, showing consensus odds, per-venue spread, open interest, depth and resolution rules. |
| **[Predicts.guru](https://www.predicts.guru)** | polymarket, kalshi, limitless | free | No-login wallet checker, smart-money radar and live trade feed, plus an arbitrage scanner matching Polymarket against Kalshi and Limitless. |
| **[Chironus Scanner](https://chironus.com/scanner)** | polymarket, kalshi | freemium | Scanner across all live Polymarket and Kalshi markets with category, volume, price-band and time-to-close filters; free tier serves delayed prices. |
| **[Adjacent News](https://adj.news)** | polymarket, kalshi, manifold, metaculus | free | News and research terminal built around prediction-market data, with a market-data API. |

### Dashboards & market data

*Watching flow, positions, and volume without building your own pipeline, including the wallet leaderboards that tell you who is actually sharp.*

| Tool | Covers | Access | Description |
|---|---|---|---|
| **[Dune: Kalshi Overview](https://dune.com/datadashboards/kalshi-overview)** | kalshi | free | Dedicated Kalshi dashboard covering exchange volume, trade counts and activity trends, without a research-platform subscription. |
| **[Dune: Prediction Markets](https://dune.com/datadashboards/prediction-markets)** | polymarket, kalshi, limitless, myriad, predict-fun | free | Multi-venue on-chain dashboard covering weekly volume, trade counts, open interest and unique users across seven venues — the broadest free venue-share view. |
| **[OVERROUND](https://www.overround.pro)** | polymarket | freemium | Skill-adjusted leaderboard scoring every on-chain fill against the price paid, de-correlating events and shrinking small samples so sharp money is defensible. |
| **[Polyguana](https://polyguana.com)** | polymarket | free | Live rankings across 157k Polymarket markets with 24h movers, a category heatmap, watchlist alerts and a resolved-market archive. |
| **[Polysights](https://www.polysights.xyz)** | polymarket | freemium | Polymarket analytics suite: market screener, trader and portfolio analytics, a sharp-wallet scanner, and API, MCP and CLI access. |
| **[Resolve Markets](https://resolvemarkets.com)** | polymarket, kalshi, predict-fun, predictit, manifold | freemium | Multi-venue suite with separate Kalshi, Polymarket and predict.fun dashboards, whale watch, contract comparison and a purpose-built negative-risk tool. |

### Data tooling

*Paid research infrastructure. Listed because reconstructing historical book depth is the one thing no free source in this directory does.*

| Tool | Covers | Access | Description |
|---|---|---|---|
| **[Probalytics](https://probalytics.io)** | polymarket | paid | Millisecond-granularity Polymarket history — full orderbook snapshots, fills and metadata via ClickHouse SQL, REST or Parquet export. From $39/mo. |

### Research

*Mostly papers, because that is the actual shape of this field: the 2026 academic output is free, unusually trader-relevant, and better than any venue's "learn" page. Order-book microstructure, maker-versus-taker returns, calibration by domain and horizon, and measured arbitrage capacity.*

| Tool | Covers | Year | Description |
|---|---|---|---|
| **[Arbitrage Analysis in Polymarket NBA Markets](https://arxiv.org/abs/2605.00864)** | polymarket | 2026 | 75M book snapshots over 173 NBA games: only 7 executable single-market arbs with a median 3.6s life, and combinatorial episodes mostly capped near 15 shares. |
| **[Decomposing Crowd Wisdom: Domain-Specific Calibration Dynamics](https://arxiv.org/abs/2602.19520)** | kalshi, polymarket | 2026 | 353M trades across 429k Kalshi and Polymarket contracts, mapping where prices are systematically wrong — political markets stay compressed toward 50%. |
| **[Logarithmic Market Scoring Rules](https://mason.gmu.edu/~rhanson/mktscore.pdf)** | general | 2002 | Hanson's LMSR — a scoring rule doubling as a bounded-loss automated market maker, and the pricing engine behind most subsidised event markets. |
| **[Makers and Takers: The Economics of the Kalshi Prediction Market](https://www2.gwu.edu/~forcpgm/2026-001.pdf)** | kalshi | 2026 | Transaction-level study of 300k+ Kalshi contracts: a strong favorite-longshot bias after fees, and higher realised returns for makers than for takers. |
| **[Optimal Market Making in Prediction Markets](https://arxiv.org/abs/2607.17991)** | general | 2026 | Derives optimal bid and ask quotes for binary event contracts via an HJB equation, handling inventory and terminal settlement risk — the binary analogue of Avellaneda-Stoikov. |
| **[Prices, Probabilities, and Parlays: Systematic Bias in Sports Prediction Markets](https://arxiv.org/abs/2607.14430)** | kalshi | 2026 | 23M Kalshi moneyline trades: calibration holds mid-contract but breaks in the final ten minutes, and cross-game parlays are overpriced relative to their legs. |
| **[The Anatomy of a Decentralized Prediction Market](https://arxiv.org/abs/2604.24366)** | polymarket | 2026 | Microstructure of 30bn Polymarket book events — longshot spread premium, ~1% wash trading, and a warning that trade direction inferred from the public book is only ~59% accurate. |

### Blogs

*People worth reading on this space — free, current, and not owned by an exchange. Last post is read from each feed, so a blog that goes quiet shows it. Building something here? This is the section to put yourself in.*

| Tool | Last post | Description |
|---|---|---|
| **[Alphanume Research](https://www.alphanume-research.com/)** | 2026-08-12 | Free quant-flavoured writing on actually trading these venues — order-book mechanics, bonding bots, and how platform rule changes hit short-dated markets. |
| **[Imperfect Information](https://rajivsethi.substack.com)** | 2026-08-06 | Rajiv Sethi on prediction-market accuracy, wash trading and market design — the most rigorous writing on when prices beat polls and where they fail. |
| **[Kacho](https://kacho.io)** | 2026-07-29 | Data engineer building side projects in public, including the Polymarket market-making bot polymm, and posting the verified metrics behind them. |
| **[Sentinel Global Risks Watch](https://blog.sentinel-team.org)** | 2026-08-10 | Free weekly global-risk roundup written with elite forecasters, tracking the geopolitical situations that Kalshi and Polymarket list as contracts. |
| **[The Event Horizon](https://nexteventhorizon.substack.com)** | 2026-08-12 | Dustin Gouker's near-daily free trade publication on volume shifts, contract design, exchange litigation and CFTC/state regulation — the structural risk that moves liquidity. |

### X accounts

*The only rows in this directory nothing can verify: X ended its free API tier in February 2026, so confirming an account is still active costs money per lookup. Listed on outside corroboration rather than follower counts, and kept deliberately short. Podcasts were checked and none qualified.*

| Tool | Description |
|---|---|
| **[Domer (@Domahhhh)](https://x.com/Domahhhh)** | Polymarket's number one all-time trader by volume and profit, around $300M across 5,000+ markets, and the most-cited independent voice in the space. |
| **[Esoteric Catboy (@catboyautist)](https://x.com/catboyautist)** | Trader who posts positions and reasoning openly, particularly on Kalshi mention markets; quoted in Bloomberg's 2026 prediction-markets feature. |
| **[Kyle (@KyleDeWriter)](https://x.com/KyleDeWriter)** | Tracks the Polymarket leaderboard and explains platform mechanics, such as what removing the 500ms order delay did to short-dated markets. |

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

_Generated 2026-08-13 from [`data/`](data/). Found something stale or dead? The
refresh bot will too — but [issues](https://github.com/kachence/prediction-almanac/issues) are welcome._
