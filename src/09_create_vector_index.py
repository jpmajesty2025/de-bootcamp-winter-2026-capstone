# Databricks notebook source
# MAGIC %md
# MAGIC # 09 - Create Delta Sync Vector Search Index
# MAGIC Creates/validates the Vector Search endpoint and index for `chunked_docs`.

from __future__ import annotations

import time
from urllib.parse import quote

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.vectorsearch import EndpointType
from pyspark.sql import SparkSession

from config import (
    CHUNKED_DOCS_TABLE,
    VS_EMBEDDING_MODEL_ENDPOINT,
    VS_ENDPOINT_NAME,
    VS_INDEX_NAME,
)


spark = SparkSession.builder.getOrCreate()
w = WorkspaceClient()


def ensure_cdf_enabled(table_name: str) -> None:
    spark.sql(
        f"""
        ALTER TABLE {table_name}
        SET TBLPROPERTIES (delta.enableChangeDataFeed = true)
        """
    )
    print(f"CDF enabled on source table: {table_name}")


def ensure_vs_endpoint(endpoint_name: str) -> None:
    print(f"Ensuring Vector Search endpoint exists: {endpoint_name}")
    try:
        w.vector_search_endpoints.create_endpoint(
            name=endpoint_name,
            endpoint_type=EndpointType.STANDARD,
        ).result()
        print(f"Endpoint created: {endpoint_name}")
    except Exception as exc:
        msg = str(exc).upper()
        if "ALREADY_EXISTS" in msg or "RESOURCE_ALREADY_EXISTS" in msg:
            print(f"Endpoint already exists: {endpoint_name}")
        else:
            raise


def ensure_delta_sync_index() -> None:
    print(f"Ensuring Delta Sync index exists: {VS_INDEX_NAME}")
    body = {
        "name": VS_INDEX_NAME,
        "endpoint_name": VS_ENDPOINT_NAME,
        "primary_key": "chunk_id",
        "index_type": "DELTA_SYNC",
        "delta_sync_index_spec": {
            "source_table": CHUNKED_DOCS_TABLE,
            "pipeline_type": "TRIGGERED",
            "embedding_source_columns": [
                {
                    "name": "chunk_text",
                    "embedding_model_endpoint_name": VS_EMBEDDING_MODEL_ENDPOINT,
                }
            ],
        },
    }

    try:
        w.api_client.do("POST", "/api/2.0/vector-search/indexes", body=body)
        print(f"Index creation requested: {VS_INDEX_NAME}")
    except Exception as exc:
        msg = str(exc).upper()
        if "ALREADY_EXISTS" in msg or "RESOURCE_ALREADY_EXISTS" in msg:
            print(f"Index already exists: {VS_INDEX_NAME}")
        else:
            raise


def wait_for_index_not_provisioning(timeout_seconds: int = 900, poll_seconds: int = 15) -> None:
    encoded_name = quote(VS_INDEX_NAME, safe="")
    path = f"/api/2.0/vector-search/indexes/{encoded_name}"

    deadline = time.time() + timeout_seconds
    last_state = None

    while time.time() < deadline:
        details = w.api_client.do("GET", path)
        status = details.get("status", {})
        detailed_state = status.get("detailed_state", "UNKNOWN")
        index_url = status.get("index_url", "")

        if detailed_state != last_state:
            print(f"Index state: {detailed_state}")
            if index_url:
                print(f"Index URL: {index_url}")
            last_state = detailed_state

        if detailed_state not in {"PROVISIONING", "INDEX_BUILDING", "TRIGGERING_PIPELINE"}:
            print("Index is no longer provisioning/building.")
            return

        time.sleep(poll_seconds)

    print("Timed out waiting for index readiness window. Check index status in Databricks UI.")


def main() -> None:
    ensure_cdf_enabled(CHUNKED_DOCS_TABLE)
    ensure_vs_endpoint(VS_ENDPOINT_NAME)
    ensure_delta_sync_index()
    wait_for_index_not_provisioning()

    print("B3 setup step complete.")
    print(f"Endpoint: {VS_ENDPOINT_NAME}")
    print(f"Index: {VS_INDEX_NAME}")
    print(f"Source table: {CHUNKED_DOCS_TABLE}")
    print(f"Embedding model endpoint: {VS_EMBEDDING_MODEL_ENDPOINT}")


if __name__ == "__main__":
    main()
