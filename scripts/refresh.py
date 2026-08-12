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

from enrich import as_float, client, get_json, post_json

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
    total, offset = 0.0, 0
    for _ in range(20):
        page = get_json(
            http,
            "https://api.gemini.com/v1/prediction-markets/events",
            params={"limit": 200, "offset": offset},
        )
        events = (page or {}).get("data") or []
        if not events:
            break
        total += sum(as_float(e.get("volume24h")) for e in events)
        if len(events) < 200:
            break
        offset += 200
    # Gemini publishes cumulative and 24h only — no 30d — so this one cell is a
    # different period, which is why the column labels each figure.
    return (total or None, "24h", "gemini-api (Σ event volume24h)")


def fetch_hyperliquid(http):
    """HIP-4 outcome markets, via a third party — Hyperliquid's own API cannot do it.

    Expired outcome coins are fully delisted (candleSnapshot, l2Book and allMids all
    return null for them), so nothing official reaches back beyond the current
    contract day, and DefiLlama only has builder-code adapters covering ~10% of the
    market. stats.outcome.xyz publishes network-wide daily volume back to launch.

    Its figure is collateral notional (contracts × $1, i.e. both legs summed), which
    runs ~1.8x a price-weighted figure like Polymarket's — noted in `source` so the
    column doesn't imply a like-for-like comparison it can't make.
    """
    start = (dt.date.today() - dt.timedelta(days=30)).isoformat()
    data = get_json(
        http,
        "https://stats.outcome.xyz/api/builder/volume-daily",
        params={"startDate": start, "limitBuilders": 500, "format": "rows"},
    )
    rows = (data or {}).get("days") or []
    if not rows:
        return None, PERIOD, "stats.outcome.xyz unreachable or empty"
    total = sum(as_float(r.get("volume")) for r in rows)
    return total or None, PERIOD, "stats.outcome.xyz (network HIP-4, collateral notional)"


# Venues with no DefiLlama adapter but their own usable endpoint.
FETCHERS = {
    "gemini-predictions": fetch_gemini,
    "hyperliquid-outcomes": fetch_hyperliquid,
}

# Platforms with no free volume anywhere, and why. Shown in the run report so the
# gaps stay visible instead of looking like an oversight.
NO_SOURCE = {
    "manifold": "play-money (mana), not USD",
    "betfair": "no free aggregate volume",
    "smarkets": "no free aggregate volume",
    "predictit": "snapshot API only, no volume",
    "forecastex": "no public data API",
    "iowa-electronic-markets": "no API",
    "hypermind": "no public API",
    "futuur": "no historical/aggregate volume endpoint",
    "metaculus": "forecasting, no trading volume",
    "good-judgment-open": "forecasting, no trading volume",
}


def _represent_none(representer, _data):
    """Keep `null` explicit; ruamel's default writes an empty value."""
    return representer.represent_scalar("tag:yaml.org,2002:null", "null")


def load_platforms():
    """slug -> (defillama slug or None, homepage), for live platforms only."""
    yaml = YAML(typ="safe")
    platforms = {}
    for path in sorted((ROOT / "data" / "platforms").glob("*.yaml")):
        with open(path) as f:
            entry = yaml.load(f)
        if entry.get("status") in ("dead", "deprecated"):
            continue
        platforms[entry["slug"]] = (entry.get("defillama"), entry.get("url"))
    return platforms


def write_back(slug, volume, period, source, as_of):
    """Round-trip YAML so comments, key order, and layout survive the write.

    A daily job touching these files must not reflow unrelated lines, or every
    refresh commit buries its one real change in whitespace noise.
    """
    yaml = YAML()  # round-trip mode
    yaml.preserve_quotes = True
    yaml.width = 4096  # never re-wrap long flow lists or folded strings
    yaml.representer.add_representer(type(None), _represent_none)
    path = ROOT / "data" / "platforms" / f"{slug}.yaml"
    data = yaml.load(path)
    metrics = data.get("metrics")
    if metrics is None:
        return False
    metrics["volume_usd"] = round(volume, 2)
    metrics["period"] = period
    metrics["source"] = source
    metrics["as_of"] = DoubleQuotedScalarString(as_of)  # match the hand-written style
    yaml.dump(data, path)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="fetch and report, write nothing")
    parser.add_argument("--only", action="append", help="limit to these platform slugs")
    args = parser.parse_args()

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
            dl_slug, url = platforms[slug]
            if dl_slug:
                # A slug matched by name alone can point at an unrelated protocol —
                # DefiLlama's `rain` is rain.one, not rain.trade. Refuse the mismatch
                # rather than publish another venue's numbers under this name.
                dl_url = llama_urls.get(dl_slug)
                if dl_url and registrable(dl_url) != registrable(url):
                    skipped.append(
                        (slug, f"REFUSED: '{dl_slug}' is {registrable(dl_url)}, not {registrable(url)}")
                    )
                    continue
                volume = llama.get(dl_slug)
                period, source = PERIOD, f"defillama ({dl_slug})"
                if volume is None:
                    skipped.append((slug, f"no DefiLlama data for '{dl_slug}'"))
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
