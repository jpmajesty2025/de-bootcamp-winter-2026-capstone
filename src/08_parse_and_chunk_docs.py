# Databricks notebook source
# MAGIC %md
# MAGIC # 08 - Parse and Chunk Locked CDC/WHO Docs
# MAGIC Reads landed docs from UC Volume, parses full text, and writes:
# MAGIC - raw_docs (document-level text)
# MAGIC - chunked_docs (chunk-level records for vector indexing)

# COMMAND ----------

from __future__ import annotations

import csv
import html
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from config import CHUNKED_DOCS_TABLE, DOCS_SOURCE_PATH, RAW_DOCS_TABLE


CHUNK_SIZE = 400
CHUNK_OVERLAP = 60
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


spark = SparkSession.builder.getOrCreate()


def strip_html_to_text(html_content: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\\1>", " ", html_content)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text


def split_chunks(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
    separators: List[str] = CHUNK_SEPARATORS,
) -> List[str]:
    if not text:
        return []

    overlap = max(0, min(overlap, chunk_size - 1))

    def fixed_window_chunks(segment: str) -> List[str]:
        segment = segment.strip()
        if not segment:
            return []
        if len(segment) <= chunk_size:
            return [segment]

        chunks: List[str] = []
        step = chunk_size - overlap
        start = 0
        while start < len(segment):
            end = min(start + chunk_size, len(segment))
            chunk = segment[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end == len(segment):
                break
            start += step
        return chunks

    def merge_splits(splits: List[str], separator: str) -> List[str]:
        from collections import deque

        docs: List[str] = []
        window = deque()
        window_len = 0
        sep_len = len(separator)

        def append_window() -> None:
            if not window:
                return
            chunk = separator.join(window).strip()
            if chunk:
                docs.append(chunk)

        for split in splits:
            split = split.strip()
            if not split:
                continue

            add_len = len(split) if not window else sep_len + len(split)

            if window and (window_len + add_len) > chunk_size:
                append_window()

                while window and window_len > overlap:
                    removed = window.popleft()
                    window_len -= len(removed)
                    if window:
                        window_len -= sep_len

                add_len = len(split) if not window else sep_len + len(split)

            window.append(split)
            window_len += add_len

        append_window()
        return docs

    def recursive_split(segment: str, active_separators: List[str]) -> List[str]:
        segment = segment.strip()
        if not segment:
            return []
        if len(segment) <= chunk_size:
            return [segment]

        separator = ""
        next_separators: List[str] = []

        for idx, candidate in enumerate(active_separators):
            if candidate == "":
                separator = ""
                next_separators = []
                break
            if candidate in segment:
                separator = candidate
                next_separators = active_separators[idx + 1 :]
                break

        if separator == "":
            return fixed_window_chunks(segment)

        pieces = [p.strip() for p in segment.split(separator) if p and p.strip()]
        short_pieces: List[str] = []
        chunks: List[str] = []

        for piece in pieces:
            if len(piece) <= chunk_size:
                short_pieces.append(piece)
                continue

            if short_pieces:
                chunks.extend(merge_splits(short_pieces, separator))
                short_pieces = []

            if next_separators:
                chunks.extend(recursive_split(piece, next_separators))
            else:
                chunks.extend(fixed_window_chunks(piece))

        if short_pieces:
            chunks.extend(merge_splits(short_pieces, separator))

        return chunks

    return recursive_split(text, separators)


def parse_pdf_with_ai(path: str) -> str:
    # Preferred Databricks path (layout-aware) used in labs.
    try:
        parsed_df = (
            spark.read
            .format("binaryFile")
            .load(path)
            .selectExpr("CAST(ai_parse_document(content) AS STRING) AS parsed")
        )
        rows = parsed_df.collect()
        if rows and rows[0]["parsed"]:
            return rows[0]["parsed"]
    except Exception:
        pass

    # Fallback: decode bytes as text (best-effort).
    raw_bytes = Path(path).read_bytes()
    return raw_bytes.decode("utf-8", errors="ignore")


def parse_html_file(path: str) -> str:
    raw_text = Path(path).read_text(encoding="utf-8", errors="ignore")
    return strip_html_to_text(raw_text)


def main() -> None:
    docs_dir = Path(DOCS_SOURCE_PATH)
    manifest_path = docs_dir / "locked_doc_manifest.csv"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}. Run src/07_ingest_cdc_who_docs.py first.")

    with manifest_path.open("r", encoding="utf-8", newline="") as f:
        manifest_rows = list(csv.DictReader(f))

    success_rows = [r for r in manifest_rows if r.get("status") == "success"]
    if len(success_rows) == 0:
        raise ValueError("No successful landed docs found in manifest.")

    run_ts = datetime.now(timezone.utc).isoformat()
    raw_records = []
    chunk_records = []

    for row in success_rows:
        filename = row["filename"]
        source_url = row["url"]
        source_path = row["local_path"]
        suffix = Path(filename).suffix.lower()

        if suffix == ".pdf":
            content = parse_pdf_with_ai(source_path)
            source_type = "pdf"
        else:
            content = parse_html_file(source_path)
            source_type = "html"

        content = (content or "").strip()
        if content == "":
            raise ValueError(f"Parsed empty content for {filename}")

        doc_id = str(uuid.uuid4())
        raw_records.append(
            {
                "doc_id": doc_id,
                "filename": filename,
                "source_url": source_url,
                "source_path": source_path,
                "source_type": source_type,
                "content": content,
                "content_length": len(content),
                "ingested_at_utc": run_ts,
            }
        )

        chunks = split_chunks(content)
        if not chunks:
            raise ValueError(f"No chunks generated for {filename}")

        for idx, chunk_text in enumerate(chunks):
            chunk_records.append(
                {
                    "chunk_id": str(uuid.uuid4()),
                    "doc_id": doc_id,
                    "chunk_index": idx,
                    "chunk_text": chunk_text,
                    "chunk_char_count": len(chunk_text),
                    "source_url": source_url,
                    "source_path": source_path,
                    "chunked_at_utc": run_ts,
                }
            )

    raw_schema = StructType(
        [
            StructField("doc_id", StringType(), False),
            StructField("filename", StringType(), False),
            StructField("source_url", StringType(), True),
            StructField("source_path", StringType(), False),
            StructField("source_type", StringType(), False),
            StructField("content", StringType(), False),
            StructField("content_length", IntegerType(), False),
            StructField("ingested_at_utc", StringType(), False),
        ]
    )

    chunk_schema = StructType(
        [
            StructField("chunk_id", StringType(), False),
            StructField("doc_id", StringType(), False),
            StructField("chunk_index", IntegerType(), False),
            StructField("chunk_text", StringType(), False),
            StructField("chunk_char_count", IntegerType(), False),
            StructField("source_url", StringType(), True),
            StructField("source_path", StringType(), False),
            StructField("chunked_at_utc", StringType(), False),
        ]
    )

    raw_df = spark.createDataFrame(raw_records, schema=raw_schema)
    chunk_df = spark.createDataFrame(chunk_records, schema=chunk_schema)

    (
        raw_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(RAW_DOCS_TABLE)
    )

    (
        chunk_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(CHUNKED_DOCS_TABLE)
    )

    print(f"Manifest read: {manifest_path}")
    print(f"Successful landed docs in manifest: {len(success_rows)}")
    print(f"Raw docs rows written: {raw_df.count()} -> {RAW_DOCS_TABLE}")
    print(f"Chunked docs rows written: {chunk_df.count()} -> {CHUNKED_DOCS_TABLE}")
    print(f"Distinct docs in chunks: {chunk_df.select('doc_id').distinct().count()}")


if __name__ == "__main__":
    main()
