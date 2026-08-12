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

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jsonschema import Draft202012Validator
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"platforms": "platform", "tools": "tool", "sources": "source"}
MECH_LABEL = {
    "onchain-clob": "CLOB",
    "onchain-amm": "AMM",
    "regulated-exchange": "Regulated exchange",
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
        return "—"
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def usd(value):
    if value is None:
        return "—"
    for cut, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "k")):
        if value >= cut:
            text = f"{value / cut:.1f}".rstrip("0").rstrip(".")
            return f"${text}{suffix}"
    return f"${value:,.0f}"


def num(value):
    return "—" if value is None else f"{value:,}"


def mark(value):
    return "✓" if value else "—"


def flags(codes):
    """ISO 3166-1 alpha-2 codes -> regional-indicator emoji."""
    return "".join(
        "".join(chr(0x1F1E6 + ord(c) - ord("a")) for c in code) for code in codes
    )


MAX_FLAGS = 6  # above this, show a count instead of a wall of flags


def geo_cell(platform):
    """Compact 'who may trade' cell; links to the terms page we read it from."""
    geo = platform.get("geo")
    if not geo:
        return "—"
    model = geo["model"]
    if model == "everyone":
        text = "🌍 everyone"
    elif model == "permissionless":
        text = "🌐 permissionless"
    elif model == "global-restrictions":
        excluded = geo.get("restricted") or []
        if not excluded:
            text = "🌍 everyone"
        elif len(excluded) <= MAX_FLAGS:
            text = f"🌍 exc. {flags(excluded)}"
        else:
            text = f"🌍 exc. {len(excluded)} countries"
    elif model == "allowlist":
        allowed = geo.get("allowed") or []
        if allowed and len(allowed) <= MAX_FLAGS:
            text = f"only {flags(allowed)}"
        elif allowed:
            text = f"only {len(allowed)} countries"
        else:
            text = "licensed countries only"
    else:  # unreachable while the schema enum holds
        text = "—"
    source = geo.get("source")
    return f"[{text}]({source})" if source else text


def vol(platform):
    metrics = platform.get("metrics") or {}
    volume = metrics.get("volume_usd")
    if volume is None:
        return "—"
    period = metrics.get("period")
    return f"{usd(volume)}/{period}" if period else usd(volume)


def ptype(platform):
    label = MECH_LABEL[platform["mechanism"]]
    if platform.get("chain"):
        label = f"{label} · {platform['chain']}"
    return label


# ---- assembly --------------------------------------------------------------

def volume_key(p):
    volume = (p.get("metrics") or {}).get("volume_usd")
    return (volume is None, -(volume or 0), p["name"].lower())


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
                }
            )
    return groups


def group_tools(tools, config):
    groups = []
    for key, title in config["tool_categories"].items():
        members = sorted(
            (t for t in tools if t["category"] == key),
            key=lambda t: (
                (t.get("github") or {}).get("stars") is None,
                -((t.get("github") or {}).get("stars") or 0),
                t["name"].lower(),
            ),
        )
        if members:
            groups.append({"title": title, "tools": members})
    return groups


def render(config, platforms, tools, sources, generated_on):
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    env.filters.update(md=md, usd=usd, num=num, mark=mark, ptype=ptype, geo=geo_cell, vol=vol)
    # dead/deprecated entries stay in data/ (cross-links, history) but aren't rendered
    platforms = [p for p in platforms if p["status"] not in ("dead", "deprecated")]
    return env.get_template("README.md.j2").render(
        config=config,
        platforms=platforms,
        tools=tools,
        sources=sorted(sources, key=lambda s: s["name"].lower()),
        sources_by_slug={s["slug"]: s for s in sources},
        platform_groups=group_platforms(platforms, config),
        tool_groups=group_tools(tools, config),
        generated_on=generated_on,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate data and verify README.md is up to date; write nothing",
    )
    args = parser.parse_args()

    config = load_yaml(ROOT / "config.yml")
    platforms = load_entries("platforms")
    tools = load_entries("tools")
    sources = load_entries("sources")

    errors = []
    for kind, entries in (("platforms", platforms), ("tools", tools), ("sources", sources)):
        errors += validate(kind, entries)
    errors += cross_check(platforms, tools, sources)
    if errors:
        fail(errors)

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    output = render(config, platforms, tools, sources, today)
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
    print(f"Wrote README.md: {summary}.")


if __name__ == "__main__":
    main()
