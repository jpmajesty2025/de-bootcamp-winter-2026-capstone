# Databricks notebook source
# MAGIC %md
# MAGIC # 07 - Ingest Locked CDC/WHO Document Sources to UC Volume
# MAGIC Downloads the locked 5 document sources and writes a landing manifest for B1 tracking.

# COMMAND ----------

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from config import DOCS_SOURCE_PATH, LOCKED_DOC_SOURCES


def download_url_to_path(url: str, out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = Request(
        url,
        headers={
            "User-Agent": "de-bootcamp-capstone/1.0",
            "Accept": "*/*",
        },
    )
    with urlopen(req, timeout=180) as resp:
        content = resp.read()

    out_path.write_bytes(content)
    return len(content)


def main() -> None:
    docs_dir = Path(DOCS_SOURCE_PATH)
    docs_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = docs_dir / "locked_doc_manifest.csv"
    run_ts = datetime.now(timezone.utc).isoformat()

    rows = []
    for filename, url in LOCKED_DOC_SOURCES.items():
        out_path = docs_dir / filename
        try:
            file_size = download_url_to_path(url, out_path)
            status = "success"
            error = ""
        except Exception as exc:
            file_size = 0
            status = "error"
            error = str(exc)

        rows.append(
            {
                "run_ts_utc": run_ts,
                "filename": filename,
                "url": url,
                "local_path": str(out_path),
                "status": status,
                "file_size_bytes": file_size,
                "error": error,
            }
        )

    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_ts_utc",
                "filename",
                "url",
                "local_path",
                "status",
                "file_size_bytes",
                "error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    success_count = sum(1 for r in rows if r["status"] == "success")
    error_count = sum(1 for r in rows if r["status"] == "error")

    print(f"Docs volume path: {docs_dir}")
    print(f"Manifest written: {manifest_path}")
    print(f"Sources attempted: {len(rows)}")
    print(f"Successful downloads: {success_count}")
    print(f"Failed downloads: {error_count}")

    if error_count > 0:
        print("Failures:")
        for r in rows:
            if r["status"] == "error":
                print(f"- {r['filename']}: {r['error']}")

    if error_count > 0:
        raise ValueError("One or more locked document sources failed to download.")


if __name__ == "__main__":
    main()
