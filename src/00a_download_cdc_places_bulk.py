"""
Small utility script to download CDC PLACES county data as a bulk CSV snapshot.

Usage:
    python src/00a_download_cdc_places_bulk.py
    python src/00a_download_cdc_places_bulk.py --out data/raw/cdc_places.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import Request, urlopen

CDC_PLACES_BULK_CSV_URL = "https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD"


def download_file(url: str, out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    req = Request(
        url,
        headers={
            "User-Agent": "de-bootcamp-capstone/1.0",
            "Accept": "text/csv,*/*",
        },
    )

    with urlopen(req, timeout=120) as resp:
        content = resp.read()

    out_path.write_bytes(content)
    return len(content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download CDC PLACES bulk CSV.")
    parser.add_argument(
        "--out",
        default="data/raw/cdc_places.csv",
        help="Output file path (default: data/raw/cdc_places.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_path = Path(args.out)

    print(f"Downloading from: {CDC_PLACES_BULK_CSV_URL}")
    size = download_file(CDC_PLACES_BULK_CSV_URL, out_path)
    print(f"Saved to: {out_path.resolve()}")
    print(f"Downloaded bytes: {size}")


if __name__ == "__main__":
    main()
