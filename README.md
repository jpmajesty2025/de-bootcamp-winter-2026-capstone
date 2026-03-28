# DE Bootcamp Winter 2026 Capstone

## Current MVP Focus (2026-03-26)
Workstream A — Data Pipeline (A1/A2): validate Bronze ingestion for CDC PLACES and Census ACS in Databricks.

## Repository Structure
- `docs/` — planning docs, execution checklist, session notes
- `src/00_setup_env.py` — creates/validates catalog+schema and Volumes
- `src/00a_download_cdc_places_bulk.py` — downloads raw CDC to Volume
- `src/00b_download_census_acs.py` — downloads raw ACS to Volume
- `src/01_ingest_cdc_places.py` — CDC PLACES Bronze table ingestion
- `src/02_ingest_census_acs.py` — Census ACS Bronze table ingestion
- `src/config.py` — shared catalog/schema/table/source path config

## A1/A2 Run Validation (Databricks)
1. Sync/pull latest repo changes in your Databricks Git Folder.
2. Run scripts in order:
   1. `src/00_setup_env.py` (Creates schema + managed UC Volumes by default)
   2. `src/00a_download_cdc_places_bulk.py` (Lands raw CDC CSV to Volume)
   3. `src/00b_download_census_acs.py` (Lands raw ACS CSV to Volume)
   4. `src/01_ingest_cdc_places.py` (Bronze Table: CDC)
   5. `src/02_ingest_census_acs.py` (Bronze Table: ACS)
   6. `src/03_validate_bronze.py` (Validation gate for A1/A2 completion)
3. Validate table writes:
   - `{CATALOG}.{SCHEMA}.bronze_cdc_places`
   - `{CATALOG}.{SCHEMA}.bronze_census_acs`
   - Validation script confirms non-zero rows and non-null ingestion metadata (`ingestion_ts`, `source_path`, `source_system`).

## Notes
- Default setup uses **managed UC Volumes**. External volume locations can be added later in `src/00_setup_env.py`.
- If catalog/schema differs in your workspace, update `src/config.py` before running.
