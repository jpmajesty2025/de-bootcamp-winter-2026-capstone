"""
Small utility script to download county-level Census ACS indicators to a CSV snapshot.

Usage:
    python src/00b_download_census_acs.py
    python src/00b_download_census_acs.py --year 2023 --out /Volumes/<catalog>/<schema>/census_acs/census_acs.csv
    python src/00b_download_census_acs.py --api-key YOUR_KEY
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import ACS_SOURCE_FILE, ACS_SOURCE_PATH

DEFAULT_YEAR = 2023
DEFAULT_OUT = f"{ACS_SOURCE_PATH}{ACS_SOURCE_FILE}"

# Optional Databricks secret lookup defaults (used only if dbutils is available)
DEFAULT_SECRET_SCOPE = "health_equity"
DEFAULT_SECRET_KEY = "census_api_key"

# ACS Subject Tables (county-level), selected SDOH indicators:
# - S1701_C03_001E: Poverty percent estimate
# - S1901_C01_012E: Median household income estimate
ACS_VARS = [
    "NAME",
    "S1701_C03_001E",
    "S1901_C01_012E",
]


def build_url(year: int, api_key: str | None) -> str:
    base = f"https://api.census.gov/data/{year}/acs/acs5/subject"
    params = {
        "get": ",".join(ACS_VARS),
        "for": "county:*",
    }
    if api_key:
        params["key"] = api_key
    return f"{base}?{urlencode(params)}"


def fetch_acs_rows(url: str) -> list[list[str]]:
    req = Request(
        url,
        headers={
            "User-Agent": "de-bootcamp-capstone/1.0",
            "Accept": "application/json",
        },
    )
    with urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    if not payload or len(payload) < 2:
        raise ValueError("ACS API returned no data rows.")

    return payload


def write_csv(payload: list[list[str]], out_path: Path, year: int, source_url: str) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    header = payload[0]
    rows = payload[1:]

    # API returns state + county separately; add concatenated 5-digit county FIPS
    output_header = header + ["county_fips", "acs_year", "source_url"]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(output_header)

        for row in rows:
            row_map = dict(zip(header, row))
            state = row_map.get("state", "").zfill(2)
            county = row_map.get("county", "").zfill(3)
            county_fips = f"{state}{county}"
            writer.writerow(row + [county_fips, str(year), source_url])

    return len(rows)


def resolve_api_key(cli_api_key: str | None) -> str | None:
    if cli_api_key:
        return cli_api_key

    env_key = os.getenv("CENSUS_API_KEY")
    if env_key:
        return env_key

    dbutils_obj = globals().get("dbutils")
    if dbutils_obj is None:
        return None

    secret_scope = os.getenv("CENSUS_API_SECRET_SCOPE", DEFAULT_SECRET_SCOPE)
    secret_key = os.getenv("CENSUS_API_SECRET_KEY", DEFAULT_SECRET_KEY)

    try:
        secret_value = dbutils_obj.secrets.get(scope=secret_scope, key=secret_key)
        return secret_value or None
    except Exception:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Census ACS county indicators to CSV.")
    parser.add_argument("--year", type=int, default=DEFAULT_YEAR, help=f"ACS year (default: {DEFAULT_YEAR})")
    parser.add_argument("--out", default=DEFAULT_OUT, help=f"Output path (default: {DEFAULT_OUT})")
    parser.add_argument("--api-key", default=None, help="Optional Census API key")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_path = Path(args.out)
    api_key = resolve_api_key(args.api_key)

    source_url = build_url(args.year, api_key)
    print(f"Downloading from: {source_url}")
    print(f"Using API key: {'yes' if api_key else 'no'}")

    payload = fetch_acs_rows(source_url)
    row_count = write_csv(payload, out_path, args.year, source_url)

    print(f"Saved to: {out_path.resolve()}")
    print(f"Rows written: {row_count}")


if __name__ == "__main__":
    main()
