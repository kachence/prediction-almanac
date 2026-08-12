#!/usr/bin/env python3
"""Refresh live metrics in data/platforms/*.yaml, then rebuild with build.py.

Volume only for now (build-order step 3). DefiLlama is the primary source: it tracks
most of these venues under one methodology, which is what makes the column comparable
across platforms, and it counts markets that settled during the window — summing a
platform's own "open markets" endpoint misses those and undercounts badly (Polymarket
by ~2.4x, Kalshi by ~14x). Per-platform APIs are only used where DefiLlama has no
adapter. Anything neither covers stays null on purpose: a missing number is
information, a wrong one is worse than none.

    python scripts/refresh.py                 # fetch everything and write back
    python scripts/refresh.py --dry-run       # fetch and report, write nothing
    python scripts/refresh.py --only kalshi   # one platform (repeatable)
"""

import argparse
import datetime as dt
import sys
from pathlib import Path
from urllib.parse import urlparse

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from enrich import as_float, client, dune_run, get_json, secret

ROOT = Path(__file__).resolve().parents[1]
DEFILLAMA_DEXS = "https://api.llama.fi/overview/dexs"
DEFILLAMA_PROTOCOLS = "https://api.llama.fi/protocols"
# 30d rather than 24h: a quiet day makes a working venue look dead (Rain reports $0 on
# some days), and this column exists to tell real venues from ghost towns.
PERIOD = "30d"

# Stablecoins whose units we can treat as USD 1:1. A market denominated in anything
# else is skipped rather than silently mis-summed.
USD_TOKENS = {"USDC", "USDC.E", "USDT", "USDT0", "USD1", "USDB", "DAI", "USD"}


def fetch_defillama(http):
    """One request covers every venue DefiLlama has an adapter for."""
    data = get_json(
        http,
        DEFILLAMA_DEXS,
        params={"excludeTotalDataChart": "true", "excludeTotalDataChartBreakdown": "true"},
    )
    if not data:
        return {}
    return {
        p["slug"]: p.get("total30d")
        for p in data.get("protocols") or []
        if p.get("slug")
    }


def registrable(url):
    """example.co.uk-style suffixes aren't handled; the last two labels are enough
    to catch the mistake this guards against (rain.one vs rain.trade)."""
    host = urlparse(url or "").hostname or ""
    return ".".join(host.lower().lstrip("www.").split(".")[-2:])


def fetch_defillama_urls(http):
    """slug -> homepage, so a slug can be checked against the platform it claims to be."""
    data = get_json(http, DEFILLAMA_PROTOCOLS)
    return {p["slug"]: p.get("url") for p in data or [] if p.get("slug")}


def fetch_gemini(http):
    """Gemini's documented per-day volume endpoint, summed over 30 complete UTC days.

    Not the events list: expired short-dated markets drop out of it, which undercounts
    by roughly 6.5x. Rows nest by category and a child's volume is included in its
    parent's, so only top-level rows are summed — adding every row would more than
    double the total. Today's date is rejected by the API, so the window is T-1 back.

    Units are contracts, which Gemini reports as USD on a $1 face value. That is
    notional, not cash exchanged; at the ~$0.41 blended price contracts actually
    trade at, cash turnover is far lower.
    """
    today = dt.datetime.now(dt.timezone.utc).date()
    total, days = 0.0, 0
    for offset in range(1, 31):
        rows = get_json(
            http,
            f"https://api.gemini.com/v1/prediction-markets/volume/{today - dt.timedelta(days=offset)}",
        )
        if not rows:
            continue
        total += sum(
            as_float(r.get("volume")) for r in rows if len(r.get("categoryPath") or []) == 1
        )
        days += 1
    if not total:
        return None, PERIOD, "gemini volume endpoint returned nothing"
    return total, PERIOD, f"gemini-api (Σ {days} daily totals, contracts at $1 face)"


def fetch_rain(http, query_id):
    """On-chain fills, because no aggregator measures the live deployment correctly.

    Self-trades are excluded: one address is maker on over half of Rain's all-time
    volume and has traded with itself. See scripts/queries/rain_volume.sql.
    """
    api_key = secret("DUNE_API_KEY")
    if not api_key:
        return None, PERIOD, "needs DUNE_API_KEY"
    rows = dune_run(query_id, api_key)
    if not rows:
        return None, PERIOD, "Dune query failed"
    volume = as_float(rows[0].get("volume_usd"))
    return volume or None, PERIOD, f"dune query {query_id} (pool fills, excl. self-trades)"


# Venues with no DefiLlama adapter but their own usable endpoint.
FETCHERS = {"gemini-predictions": fetch_gemini}

# Venues needing a saved Dune query; ids live in config.yml under `dune`.
DUNE_FETCHERS = {"rain": fetch_rain}

# Platforms with no free volume anywhere, and why. Shown in the run report so the
# gaps stay visible instead of looking like an oversight.
NO_SOURCE = {
    "manifold": "play-money (mana), not USD",
    "betfair": "free key omits totalMatched; the paid key forbids data-only use",
    "smarkets": "endpoint exists but their API terms prohibit extraction and benchmarking",
    "predictit": "per-market volume needs US egress, 15 req/min, and non-commercial terms",
    "robinhood": "discloses contracts traded, not USD; its routed flow is counted inside Kalshi and ForecastEx",
    "ibkr": "no free volume anywhere — event contracts are absent from IBKR's monthly metrics",
    "hypermind": "no public API",
    "futuur": "no historical/aggregate volume endpoint",
    "metaculus": "forecasting, no trading volume",
    "good-judgment-open": "forecasting, no trading volume",
}


def fetch_github(http, repo_url, token):
    """stars, last commit, licence and archived flag for one repo."""
    slug = repo_url.rstrip("/").removeprefix("https://github.com/")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = get_json(http, f"https://api.github.com/repos/{slug}", headers=headers)
    if not data:
        return None
    licence = (data.get("license") or {}).get("spdx_id")
    return {
        "stars": data.get("stargazers_count"),
        "last_commit": (data.get("pushed_at") or "")[:10] or None,
        "license": None if licence in (None, "NOASSERTION") else licence,
        "archived": bool(data.get("archived")),
    }


def derive_health(github, stale_days):
    """archived beats stale beats active — readers filter on this, it isn't a gate."""
    if github.get("archived"):
        return "archived"
    last = github.get("last_commit")
    if not last:
        return None
    age = (dt.date.today() - dt.date.fromisoformat(last)).days
    return "stale" if age > stale_days else "active"


def refresh_tools(http, config, dry_run):
    """Fill the github block for every tool that names a repo."""
    token = secret("GITHUB_TOKEN")
    stale_days = (config.get("thresholds") or {}).get("stale_days", 365)
    yaml = YAML(typ="safe")
    updated = 0
    print(f"\nGitHub ({'authenticated' if token else 'anonymous, 60 req/h'}):")
    for path in sorted((ROOT / "data" / "tools").glob("*.yaml")):
        with open(path) as f:
            entry = yaml.load(f)
        repo_url = entry.get("repo")
        if not repo_url:
            continue
        github = fetch_github(http, repo_url, token)
        if not github:
            print(f"  {entry['slug']:34} unreachable")
            continue
        github["health"] = derive_health(github, stale_days)
        print(
            f"  {entry['slug']:34} {github['stars'] or 0:>7,} stars  "
            f"{github['last_commit'] or '—':>10}  {github['health'] or '—'}"
        )
        if not dry_run and write_block(path, "github", github):
            updated += 1
    return updated


def _represent_none(representer, _data):
    """Keep `null` explicit; ruamel's default writes an empty value."""
    return representer.represent_scalar("tag:yaml.org,2002:null", "null")


def load_yaml(path):
    with open(path) as f:
        return YAML(typ="safe").load(f)


def load_platforms():
    """slug -> (defillama slug or None, domains), for live platforms only."""
    yaml = YAML(typ="safe")
    platforms = {}
    for path in sorted((ROOT / "data" / "platforms").glob("*.yaml")):
        with open(path) as f:
            entry = yaml.load(f)
        if entry.get("status") in ("dead", "deprecated"):
            continue
        domains = {registrable(entry.get("url"))}
        domains |= {registrable(f"https://{a}") for a in entry.get("aliases") or []}
        platforms[entry["slug"]] = (entry.get("defillama"), domains)
    return platforms


def write_block(path, block, values):
    """Round-trip YAML so comments, key order, and layout survive the write.

    A daily job touching these files must not reflow unrelated lines, or every
    refresh commit buries its one real change in whitespace noise.
    """
    yaml = YAML()  # round-trip mode
    yaml.preserve_quotes = True
    yaml.width = 4096  # never re-wrap long flow lists or folded strings
    yaml.representer.add_representer(type(None), _represent_none)
    data = yaml.load(path)
    target = data.get(block)
    if target is None:
        return False
    for key, value in values.items():
        target[key] = value
    yaml.dump(data, path)
    return True


def write_back(slug, volume, period, source, as_of):
    return write_block(
        ROOT / "data" / "platforms" / f"{slug}.yaml",
        "metrics",
        {
            "volume_usd": round(volume, 2),
            "period": period,
            "source": source,
            "as_of": DoubleQuotedScalarString(as_of),  # match the hand-written style
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="fetch and report, write nothing")
    parser.add_argument("--only", action="append", help="limit to these platform slugs")
    parser.add_argument("--skip-tools", action="store_true", help="don't refresh tool health")
    args = parser.parse_args()

    config = load_yaml(ROOT / "config.yml")
    platforms = load_platforms()
    targets = args.only or list(platforms)
    unknown = [t for t in targets if t not in platforms]
    if unknown:
        print(f"Not a live platform: {', '.join(unknown)}", file=sys.stderr)
        return 1

    as_of = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    written, skipped = 0, []
    with client() as http:
        llama = fetch_defillama(http)
        llama_urls = fetch_defillama_urls(http)
        print(f"DefiLlama: {len(llama)} protocols with volume\n")
        for slug in sorted(targets):
            dl_slug, domains = platforms[slug]
            if dl_slug:
                # A slug matched by name alone can point at an unrelated protocol, so
                # check the homepage domain against the platform's own and its declared
                # aliases (a venue may legitimately be listed under an older host).
                dl_url = llama_urls.get(dl_slug)
                if dl_url and registrable(dl_url) not in domains:
                    skipped.append(
                        (slug, f"REFUSED: '{dl_slug}' is {registrable(dl_url)}, not {'/'.join(sorted(domains))}")
                    )
                    continue
                volume = llama.get(dl_slug)
                period, source = PERIOD, f"defillama ({dl_slug})"
                if volume is None:
                    skipped.append((slug, f"no DefiLlama data for '{dl_slug}'"))
                    continue
            elif slug in DUNE_FETCHERS:
                query_id = (config.get("dune") or {}).get(slug)
                if not query_id:
                    skipped.append((slug, f"no dune query id in config.yml for '{slug}'"))
                    continue
                volume, period, source = DUNE_FETCHERS[slug](http, query_id)
                if volume is None:
                    skipped.append((slug, source))
                    continue
            elif slug in FETCHERS:
                volume, period, source = FETCHERS[slug](http)
                if volume is None:
                    skipped.append((slug, source))
                    continue
            else:
                skipped.append((slug, NO_SOURCE.get(slug, "no known free volume source")))
                continue
            print(f"  {slug:24} ${volume:>16,.0f}  {period}  {source}")
            if not args.dry_run and write_back(slug, volume, period, source, as_of):
                written += 1

        if not args.only and not args.skip_tools:
            written += refresh_tools(http, config, args.dry_run)

    print()
    for slug, reason in sorted(skipped):
        print(f"  {slug:24} {'—':>17}       ({reason})")

    if args.dry_run:
        print("\nDry run — nothing written.")
    else:
        print(f"\nUpdated {written} platform file(s). Run `python scripts/build.py` to regenerate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
