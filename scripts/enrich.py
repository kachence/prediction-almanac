"""HTTP helpers shared by refresh.py and (later) intake.py."""

import httpx

USER_AGENT = "prediction-almanac/1.0 (+https://github.com/kachence/prediction-almanac)"
TIMEOUT = httpx.Timeout(30.0, connect=10.0)


def client():
    return httpx.Client(
        timeout=TIMEOUT,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        follow_redirects=True,
    )


def get_json(http, url, params=None, attempts=3, headers=None):
    """GET returning parsed JSON, retrying transient failures; None if it never works."""
    for attempt in range(attempts):
        try:
            response = http.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            if attempt == attempts - 1:
                return None
    return None


def post_json(http, url, payload, attempts=3):
    for attempt in range(attempts):
        try:
            response = http.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception:
            if attempt == attempts - 1:
                return None
    return None


def secret(name):
    """Env var first (CI), then .env.local (local dev). None if neither has it."""
    import os
    from pathlib import Path

    if os.environ.get(name):
        return os.environ[name]
    env_file = Path(__file__).resolve().parents[1] / ".env.local"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def as_float(value):
    """APIs mix numbers and numeric strings; anything unparseable counts as zero."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
