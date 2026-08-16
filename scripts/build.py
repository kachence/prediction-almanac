#!/usr/bin/env python3
"""Generate README.md from data/*.yaml.

Data is the source of truth; README.md is a build artifact. CI runs
`build.py --check` to reject hand-edited or stale READMEs.
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import pycountry
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jsonschema import Draft202012Validator
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"platforms": "platform", "tools": "tool", "sources": "source"}
MECH_LABEL = {
    "onchain-clob": "CLOB",
    "onchain-amm": "AMM",
    "regulated-exchange": "Regulated exchange",
    "broker": "Broker",
    "play-money": "Play-money",
    "forecasting": "Forecasting",
}
# Dates are normalized away before --check comparison so a rebuild on a later
# day doesn't read as "stale".
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

_yaml = YAML(typ="safe")


def fail(errors):
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)


def load_yaml(path):
    with open(path) as f:
        return _yaml.load(f)


def load_entries(kind):
    entries = []
    for path in sorted((ROOT / "data" / kind).glob("*.yaml")):
        entry = load_yaml(path)
        entry["_file"] = str(path.relative_to(ROOT))
        entries.append(entry)
    return entries


def validate(kind, entries):
    schema = json.loads((ROOT / "schema" / f"{KINDS[kind]}.schema.json").read_text())
    validator = Draft202012Validator(schema)
    errors = []
    for entry in entries:
        bare = {k: v for k, v in entry.items() if not k.startswith("_")}
        for err in validator.iter_errors(bare):
            where = "/".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{entry['_file']}: {where}: {err.message}")
        stem = Path(entry["_file"]).stem
        if entry.get("slug") != stem:
            errors.append(f"{entry['_file']}: slug '{entry.get('slug')}' != filename '{stem}'")
    return errors


def check_country_codes(platforms):
    """Catch typos like 'uk' (the ISO code for the United Kingdom is 'gb')."""
    errors = []
    for p in platforms:
        geo = p.get("geo") or {}
        for field in ("restricted", "allowed"):
            for code in geo.get(field) or []:
                if not pycountry.countries.get(alpha_2=code.upper()):
                    errors.append(f"{p['_file']}: geo.{field}: '{code}' is not an ISO 3166-1 alpha-2 code")
    return errors


def cross_check(platforms, tools, sources):
    """Referential integrity: every cross-reference must resolve to a real slug."""
    errors = []
    platform_slugs = {p["slug"] for p in platforms}
    source_slugs = {s["slug"] for s in sources}
    for group, entries in (("tools", tools), ("sources", sources)):
        for e in entries:
            for ref in e.get("platforms") or []:
                if ref not in platform_slugs:
                    errors.append(f"{e['_file']}: unknown platform slug '{ref}'")
    for p in platforms:
        archive = (p.get("data") or {}).get("free_archive")
        if archive and archive not in source_slugs:
            errors.append(f"{p['_file']}: free_archive '{archive}' is not a data/sources/ slug")
    for kind, entries in (("platforms", platforms), ("tools", tools), ("sources", sources)):
        slugs = [e["slug"] for e in entries]
        for dup in {s for s in slugs if slugs.count(s) > 1}:
            errors.append(f"data/{kind}: duplicate slug '{dup}'")
    return errors


# ---- jinja filters ---------------------------------------------------------

def md(text):
    """Make a value safe inside a markdown table cell."""
    if text is None or text == "":
        return "-"
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def usd(value):
    if value is None:
        return "-"
    for cut, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if value >= cut:
            text = f"{value / cut:.1f}".rstrip("0").rstrip(".")
            return f"${text}{suffix}"
    return f"${value:,.0f}"


def num(value):
    return "-" if value is None else f"{value:,}"


def mark(value):
    return "✓" if value else "-"


def flags(codes):
    """ISO 3166-1 alpha-2 codes -> regional-indicator emoji."""
    return "".join(
        "".join(chr(0x1F1E6 + ord(c) - ord("a")) for c in code) for code in codes
    )


# pycountry's common_name covers most awkward official titles ("Iran, Islamic Republic
# of" -> "Iran"); these three have no common_name and read badly in a tooltip.
COUNTRY_ALIASES = {
    "cd": "DR Congo",
    "ru": "Russia",
    "um": "US Minor Outlying Islands",
}


def country_name(code):
    if code in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[code]
    country = pycountry.countries.get(alpha_2=code.upper())
    if not country:
        return code.upper()
    return getattr(country, "common_name", None) or country.name


TOOLTIP_NAMES = 15  # keep the hover text readable; the source link has the full list


def _tooltip(label, codes):
    shown = [country_name(c) for c in codes[:TOOLTIP_NAMES]]
    if len(codes) > TOOLTIP_NAMES:
        shown.append(f"+{len(codes) - TOOLTIP_NAMES} more")
    return f"{label}: {', '.join(shown)}"


def _ordered(codes, notable):
    """Notable countries first (readers scan for their own), then the rest."""
    ranked = sorted(codes, key=lambda c: (notable.index(c) if c in notable else len(notable), c))
    return ranked


def geo_parts(platform, config):
    """Structured 'who may trade': {text, title, source} or None. Both the README cell
    and the JSON export are built from this, so the branching lives in exactly one place."""
    geo = platform.get("geo")
    if not geo:
        return None
    display = config["geo_display"]
    max_flags, lead, notable = display["max_flags"], display["lead_flags"], display["notable"]
    model = geo["model"]
    title = None
    if model == "everyone":
        text = "🌍 everyone"
    elif model == "permissionless":
        text = "🌐 permissionless"
    elif model == "unknown":
        # We looked and couldn't establish it — better stated than implied.
        text = "❔ unverified"
    elif model == "global-restrictions":
        excluded = _ordered(geo.get("restricted") or [], notable)
        if not excluded:
            # the model asserts restrictions exist; the list just isn't public
            text = "🌍 exc. an undisclosed list"
        elif len(excluded) <= max_flags:
            text = f"🌍 exc. {flags(excluded)}"
            title = _tooltip("Cannot trade", excluded)
        else:
            text = f"🌍 exc. {flags(excluded[:lead])} +{len(excluded) - lead}"
            title = _tooltip("Cannot trade", excluded)
    elif model == "allowlist":
        allowed = _ordered(geo.get("allowed") or [], notable)
        if not allowed:
            text = "licensed countries only"
        elif len(allowed) <= max_flags:
            text = f"only {flags(allowed)}"
            title = _tooltip("Can trade", allowed)
        else:
            text = f"only {len(allowed)} countries"
            title = _tooltip("Can trade", allowed)
    else:  # unreachable while the schema enum holds
        return None
    return {"text": text, "title": title, "source": geo.get("source")}


def make_geo_cell(config):
    """Compact 'who may trade' cell for the markdown table, linked to the terms page."""

    def geo_cell(platform):
        parts = geo_parts(platform, config)
        if parts is None:
            return "-"
        text, title, source = parts["text"], parts["title"], parts["source"]
        if not source:
            return text
        return f'[{text}]({source} "{title}")' if title else f"[{text}]({source})"

    return geo_cell


def vol(platform):
    metrics = platform.get("metrics") or {}
    volume = metrics.get("volume_usd")
    if volume is None:
        return "-"
    period = metrics.get("period")
    return f"{usd(volume)}/{period}" if period else usd(volume)


def tool_name(tool):
    return f"**[{md(tool['name'])}]({tool['url']})**"


def status(tool):
    """Repos live or die by their last commit; stars say whether anyone else agrees."""
    github = tool.get("github") or {}
    date, stars = github.get("last_commit"), github.get("stars")
    if not date:
        return "-"
    health = github.get("health")
    cell = f"{stars:,}★ · {date}" if stars is not None else date
    return f"{cell} · {health}" if health in ("archived", "stale") else cell


def commit(github):
    """Last commit, flagged when the repo is archived or has gone quiet — the date
    alone doesn't tell a reader the project was retired."""
    github = github or {}
    date = github.get("last_commit")
    if not date:
        return "-"
    health = github.get("health")
    return f"{date} · {health}" if health in ("archived", "stale") else date


def ptype(platform):
    label = MECH_LABEL[platform["mechanism"]]
    if platform.get("chain"):
        label = f"{label}, {platform['chain']}"
    if platform.get("routes_to"):
        # a broker's real semantics are where its orders match, not its own name
        label = f"{label} → {', '.join(platform['routes_to'])}"
    return label


# ---- assembly --------------------------------------------------------------

PERIOD_DAYS = {"24h": 1, "30d": 30}


def volume_key(p):
    """Rank on a per-day rate so a 24h figure isn't sorted against 30d ones as if
    they were the same quantity. The table still shows each figure as reported."""
    metrics = p.get("metrics") or {}
    volume = metrics.get("volume_usd")
    if volume is None:
        return (True, 0, p["name"].lower())
    daily = volume / PERIOD_DAYS.get(metrics.get("period"), 1)
    return (False, -daily, p["name"].lower())


def group_platforms(platforms, config):
    covered = {m for g in config["platform_groups"] for m in g["mechanisms"]}
    stray = sorted(p["slug"] for p in platforms if p["mechanism"] not in covered)
    if stray:
        fail([f"config.yml platform_groups covers no mechanism for: {', '.join(stray)}"])
    groups = []
    for g in config["platform_groups"]:
        members = sorted(
            (p for p in platforms if p["mechanism"] in g["mechanisms"]), key=volume_key
        )
        if members:
            groups.append(
                {
                    "title": g["title"],
                    "platforms": members,
                    "show_volume": g.get("show_volume", True),
                    "note": g.get("note"),
                }
            )
    return groups


def group_tools(tools, config):
    """Active projects lead each section: a retired repo shouldn't head the list
    just because it collected stars before it was archived."""
    order = {"active": 0, None: 1, "stale": 2, "archived": 3}
    groups = []
    for spec in config["tool_categories"]:
        members = sorted(
            (t for t in tools if t["category"] in spec["keys"]),
            key=lambda t: (
                t.get("rank") or 99,
                order.get((t.get("github") or {}).get("health"), 1),
                (t.get("github") or {}).get("stars") is None,
                -((t.get("github") or {}).get("stars") or 0),
                t["name"].lower(),
            ),
        )
        if members:
            groups.append({
                "title": spec["title"],
                "note": spec.get("note"),
                "extra": spec.get("extra"),
                "parent": spec.get("parent", "tools"),
                "item_label": spec.get("item_label", "Tool"),
                "covers": spec.get("covers", True),
                "covers_default": spec.get("covers_default"),
                "tools": members,
            })
    return groups


def render(config, platforms, tools, sources, excluded, generated_on):
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    env.filters.update(
        md=md, usd=usd, num=num, mark=mark, ptype=ptype, geo=make_geo_cell(config), vol=vol, commit=commit, tname=tool_name, status=status
    )
    # dead/deprecated entries stay in data/ (cross-links, history) but aren't rendered
    platforms = [p for p in platforms if p["status"] not in ("dead", "deprecated")]
    return env.get_template("README.md.j2").render(
        config=config,
        platforms=platforms,
        excluded=excluded,
        tools=tools,
        sources=sorted(
            sources,
            key=lambda s: (
                ["dataset", "odds-feed"].index(s["kind"]),
                s["name"].lower(),
            ),
        ),
        sources_by_slug={s["slug"]: s for s in sources},
        platform_groups=group_platforms(platforms, config),
        tool_groups=group_tools(tools, config),
        generated_on=generated_on,
    )


# ---- JSON export -----------------------------------------------------------
# A hosted front end (kacho.io) renders the same directory. Rather than have it
# re-implement the grouping, sorting, geo and volume logic and drift, we emit a
# display-ready view model here — the single place that logic lives — and it just
# paints the result. Same helpers as render(), decomposed into JSON instead of
# markdown cells.

EXTRA_LABELS = {
    "status": "Status", "access": "Access", "year": "Year",
    "cadence": "Cadence", "kind": "Medium", "last_post": "Last post",
}


def _platform_view(p, config):
    v = vol(p)
    return {
        "name": p["name"],
        "url": p["url"],
        "type": ptype(p),
        "launched": p.get("launched"),
        "volume": None if v == "-" else v,
        "geo": geo_parts(p, config),
        "description": p.get("description"),
    }


def _source_view(s):
    cov = s.get("coverage") or {}
    return {
        "name": s["name"],
        "url": s["url"],
        "covers": ", ".join(s.get("platforms") or []) or None,
        "prices": s.get("prices"),
        "format": s.get("format"),
        "granularity": s.get("granularity"),
        "coverage": {
            "range": cov.get("range"),
            "completeness": cov.get("completeness"),
            "known_gaps": cov.get("known_gaps"),
        },
        "access": s.get("access"),
        "description": s.get("description"),
    }


def _tool_view(t, group):
    gh = t.get("github") or {}
    key = group.get("extra")
    raw = {
        "status": lambda: (None if status(t) == "-" else status(t)),
        "access": lambda: t.get("access") or "free",
        "year": lambda: t.get("year"),
        "cadence": lambda: t.get("cadence"),
        "kind": lambda: t.get("kind"),
        "last_post": lambda: t.get("last_post"),
    }.get(key, lambda: None)()
    covers = None
    if group.get("covers", True):
        covers = ", ".join(t.get("platforms") or []) or group.get("covers_default")
    return {
        "name": t["name"],
        "url": t["url"],
        "description": t.get("description"),
        "covers": covers,
        "extra": None if raw in (None, "") else str(raw),
        # structured extras, so the front end can render a richer cell than the string:
        "stars": gh.get("stars"),
        "last_commit": gh.get("last_commit"),
        "health": gh.get("health"),
        "access": t.get("access"),
    }


def build_data(config, platforms, tools, sources, excluded, generated_on):
    live = [p for p in platforms if p["status"] not in ("dead", "deprecated")]
    sorted_sources = sorted(
        sources, key=lambda s: (["dataset", "odds-feed"].index(s["kind"]), s["name"].lower())
    )
    return {
        "generated_on": generated_on,
        "site": {
            "title": config["site"]["title"],
            "repo": config["site"]["repo"],
            "tagline": config["site"]["tagline"],
        },
        "counts": {"platforms": len(live), "sources": len(sources), "tools": len(tools)},
        "platform_groups": [
            {
                "title": g["title"],
                "note": g.get("note"),
                "show_volume": g["show_volume"],
                "platforms": [_platform_view(p, config) for p in g["platforms"]],
            }
            for g in group_platforms(live, config)
        ],
        "sources": {
            "datasets": [_source_view(s) for s in sorted_sources if s["kind"] == "dataset"],
            "feeds": [_source_view(s) for s in sorted_sources if s["kind"] == "odds-feed"],
        },
        "tool_groups": [
            {
                "parent": g.get("parent", "tools"),
                "title": g["title"],
                "note": g.get("note"),
                "item_label": g.get("item_label", "Tool"),
                "covers": g.get("covers", True),
                "extra": {"key": g["extra"], "label": EXTRA_LABELS.get(g["extra"], g["extra"])}
                if g.get("extra")
                else None,
                "tools": [_tool_view(t, g) for t in g["tools"]],
            }
            for g in group_tools(tools, config)
        ],
        "excluded": [
            {"name": e.get("name"), "url": e.get("url"), "reason": e.get("reason")}
            for e in (excluded or [])
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate data and verify README.md is up to date; write nothing",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="validate data only; ignore README.md entirely (what PR CI runs)",
    )
    args = parser.parse_args()

    config = load_yaml(ROOT / "config.yml")
    platforms = load_entries("platforms")
    tools = load_entries("tools")
    sources = load_entries("sources")
    excluded = load_yaml(ROOT / "data" / "excluded.yml") or []

    errors = []
    for kind, entries in (("platforms", platforms), ("tools", tools), ("sources", sources)):
        errors += validate(kind, entries)
    errors += check_country_codes(platforms)
    errors += cross_check(platforms, tools, sources)
    excluded_schema = json.loads((ROOT / "schema" / "excluded.schema.json").read_text())
    for err in Draft202012Validator(excluded_schema).iter_errors(excluded):
        where = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"data/excluded.yml: {where}: {err.message}")
    if errors:
        fail(errors)

    if args.validate:
        print(f"OK: data valid ({len(platforms)} platforms, {len(sources)} sources, {len(tools)} tools).")
        return

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    output = render(config, platforms, tools, sources, excluded, today)
    readme = ROOT / "README.md"
    hidden = sum(1 for p in platforms if p["status"] in ("dead", "deprecated"))
    summary = (
        f"{len(platforms) - hidden} platforms ({hidden} dead/deprecated kept in data/), "
        f"{len(sources)} sources, {len(tools)} tools"
    )

    if args.check:
        current = readme.read_text() if readme.exists() else ""
        if DATE_RE.sub("<date>", current) != DATE_RE.sub("<date>", output):
            fail(["README.md is stale or was hand-edited. Run `python scripts/build.py`."])
        print(f"OK: {summary}; README.md up to date.")
        return

    readme.write_text(output)
    data = build_data(config, platforms, tools, sources, excluded, today)
    (ROOT / "almanac.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote README.md and almanac.json: {summary}.")


if __name__ == "__main__":
    main()
