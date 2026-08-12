#!/usr/bin/env python3
"""Refresh live metrics in data/platforms/*.yaml, then rebuild with build.py.

Only 24h notional USD volume for now (build-order step 3). Platforms without a free,
unambiguous volume endpoint are left null on purpose — a missing number is information,
and a wrong one is worse than none.

    python scripts/refresh.py                 # fetch everything and write back
    python scripts/refresh.py --dry-run       # fetch and report, write nothing
    python scripts/refresh.py --only kalshi   # one platform (repeatable)
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from enrich import as_float, client, get_json, post_json

ROOT = Path(__file__).resolve().parents[1]
PERIOD = "24h"

# Stablecoins whose units we can treat as USD 1:1. A market denominated in anything
# else is skipped rather than silently mis-summed.
USD_TOKENS = {"USDC", "USDC.E", "USDT", "USDT0", "USD1", "USDB", "DAI", "USD"}


def fetch_polymarket(http):
    """Gamma exposes per-market volume24hr; sorted desc, the tail rounds to nothing."""
    total, offset = 0.0, 0
    for _ in range(40):
        page = get_json(
            http,
            "https://gamma-api.polymarket.com/markets",
            params={
                "closed": "false",
                "limit": 500,
                "offset": offset,
                "order": "volume24hr",
                "ascending": "false",
            },
        )
        if not page:
            break
        page_total = sum(as_float(m.get("volume24hr")) for m in page)
        total += page_total
        # sorted descending, so once a whole page is dust the rest is too
        if len(page) < 500 or page_total < 100:
            break
        offset += 500
    return total or None, "gamma-api (Σ open-market volume24hr)"


def fetch_kalshi(http):
    """Kalshi reports volume in contracts, so notional ≈ contracts × last price.

    Nested markets under /events, not /markets: the market list is dominated by
    ~200k dormant strikes, and its `status` filter has no value matching the
    `active` state that traded markets actually report.
    """
    total, cursor = 0.0, None
    for _ in range(200):
        params = {"limit": 200, "status": "open", "with_nested_markets": "true"}
        if cursor:
            params["cursor"] = cursor
        page = get_json(http, "https://api.elections.kalshi.com/trade-api/v2/events", params=params)
        events = (page or {}).get("events")
        if not events:
            break
        for event in events:
            for market in event.get("markets") or []:
                contracts = as_float(market.get("volume_24h_fp"))
                if contracts:
                    total += contracts * as_float(market.get("last_price_dollars"))
        cursor = page.get("cursor")
        if not cursor:
            break
    return total or None, "kalshi-api (Σ 24h contracts × last price)"


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
    return total or None, "gemini-api (Σ event volume24h)"


def fetch_myriad(http):
    """Paginates by page, not offset; collateral varies per market, so points- and
    other non-USD-denominated markets are excluded rather than summed as dollars."""
    total, skipped = 0.0, 0
    for model in ("ob", "amm"):
        page_num = 1
        while page_num <= 20:
            page = get_json(
                http,
                "https://api-v2.myriadprotocol.com/markets",
                params={"trading_model": model, "state": "open", "limit": 100, "page": page_num},
            )
            markets = (page or {}).get("data") or []
            if not markets:
                break
            for market in markets:
                symbol = ((market.get("token") or {}).get("symbol") or "").upper()
                if symbol in USD_TOKENS:
                    total += as_float(market.get("volume24h"))
                else:
                    skipped += 1
            if not ((page or {}).get("pagination") or {}).get("hasNext"):
                break
            page_num += 1
    note = f"; {skipped} non-USD markets excluded" if skipped else ""
    return total or None, f"myriad-api (Σ open-market volume24h{note})"


def fetch_hyperliquid(http):
    """No volume field on outcome metadata today; recorded so the gap is visible."""
    meta = post_json(http, "https://api.hyperliquid.xyz/info", {"type": "outcomeMeta"})
    if meta is None:
        return None, "unreachable"
    return None, "no volume field on outcomeMeta"


FETCHERS = {
    "polymarket": fetch_polymarket,
    "kalshi": fetch_kalshi,
    "gemini-predictions": fetch_gemini,
    "myriad": fetch_myriad,
    "hyperliquid-outcomes": fetch_hyperliquid,
}

# Platforms deliberately left null, with the reason shown in the run report.
NO_SOURCE = {
    "limitless": "only cumulative per-market volume; no 24h or 30d field",
    "predict-fun": "no public volume endpoint found",
    "sxbet": "no aggregate endpoint; /trades requires a filter",
    "rain": "API exposes cumulative volume only",
    "betfair": "no free aggregate volume",
    "smarkets": "no free aggregate volume",
    "predictit": "snapshot API only, no volume",
    "forecastex": "no public data API",
    "iowa-electronic-markets": "no API",
}


def _represent_none(representer, _data):
    """Keep `null` explicit; ruamel's default writes an empty value."""
    return representer.represent_scalar("tag:yaml.org,2002:null", "null")


def write_back(slug, volume, source, as_of):
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
    metrics["period"] = PERIOD
    metrics["source"] = source
    metrics["as_of"] = DoubleQuotedScalarString(as_of)  # match the hand-written style
    yaml.dump(data, path)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="fetch and report, write nothing")
    parser.add_argument("--only", action="append", help="limit to these platform slugs")
    args = parser.parse_args()

    targets = args.only or list(FETCHERS)
    unknown = [t for t in targets if t not in FETCHERS]
    if unknown:
        print(f"No fetcher for: {', '.join(unknown)}", file=sys.stderr)
        return 1

    as_of = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    written = 0
    with client() as http:
        for slug in targets:
            volume, source = FETCHERS[slug](http)
            if volume is None:
                print(f"  {slug:24} —            ({source})")
                continue
            print(f"  {slug:24} ${volume:>14,.0f}  {PERIOD}  {source}")
            if not args.dry_run and write_back(slug, volume, source, as_of):
                written += 1

    for slug, reason in sorted(NO_SOURCE.items()):
        print(f"  {slug:24} —            (skipped: {reason})")

    if args.dry_run:
        print("\nDry run — nothing written.")
    else:
        print(f"\nUpdated {written} platform file(s). Run `python scripts/build.py` to regenerate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
