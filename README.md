# DE Bootcamp Winter 2026 Capstone

## Current MVP Focus (2026-03-26)
Workstream A — Data Pipeline (A1/A2): validate Bronze ingestion for CDC PLACES and Census ACS in Databricks.

## Repository Structure
- `docs/` — planning docs, execution checklist, session notes
- `src/00_setup_env.py` — creates/validates catalog+schema and table names
- `src/01_ingest_cdc_places.py` — CDC PLACES Bronze ingestion
- `src/02_ingest_census_acs.py` — Census ACS Bronze ingestion
- `src/config.py` — shared catalog/schema/table/source path config

## A1/A2 Run Validation (Databricks)
1. In Databricks, upload raw source files to:
   - `dbfs:/FileStore/capstone/raw/cdc_places.csv`
   - `dbfs:/FileStore/capstone/raw/census_acs.csv`
2. Sync/pull latest repo changes in your Databricks Git Folder.
3. Run scripts in order:
   1. `src/00_setup_env.py`
   2. `src/01_ingest_cdc_places.py`
   3. `src/02_ingest_census_acs.py`
   4. `src/03_validate_bronze.py`
4. Validate table writes:
   - `main.health_equity_capstone.bronze_cdc_places`
   - `main.health_equity_capstone.bronze_census_acs`
   - validation output shows non-zero rows and no null ingestion metadata

## Notes
- If catalog/schema/path differs in your workspace, update `src/config.py` before running.
- Once both ingestions write rows successfully with `ingestion_ts`, A1/A2 can move to DONE in `docs/execution_checklist.md`.
