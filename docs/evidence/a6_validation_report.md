# A6 End-to-End Validation Report

**Date:** YYYY-MM-DD  
**POC:** Capstone Student  
**Environment:** Databricks (Catalog: `bootcamp_students`, Schema: `health_equity_capstone_jpmajesty2019`)  
**Job Name:** DE Winter 2026 Bootcamp Capstone DAG  
**Run ID:** `<fill>`  
**Run Start / End:** `<fill>`  
**Overall Result:** PASS / FAIL

---

## 1) DAG Execution Summary

### Task Flow
`00_setup_env -> (00a_download_cdc, 00b_download_acs) -> (01_ingest_cdc, 02_ingest_acs) -> 03_validate_bronze -> 04_conformed_silver -> 05_build_gold -> 06_validate_gold`

### Run Outcome
- All tasks green: Yes / No
- Retries triggered: Yes / No
- Duration warnings triggered: Yes / No
- Failures: `<fill or none>`

### Evidence
- DAG graph screenshot: `docs/evidence/<run_folder>/01_dag_graph.png`
- DAG timeline screenshot: `docs/evidence/<run_folder>/02_dag_timeline.png`

---

## 2) Bronze Validation (Task 03)

### Output Snapshot
- CDC Bronze row count: `<fill>`
- ACS Bronze row count: `<fill>`
- Null metadata rows (CDC): `<fill>`
- Null metadata rows (ACS): `<fill>`
- Validation status: PASS / FAIL

### Evidence
- Output/log screenshot or text: `docs/evidence/<run_folder>/03_bronze_validation_output.txt`

---

## 3) Silver Conformance + Quarantine (Task 04)

### Output Snapshot
- CDC clean rows: `<fill>`
- CDC quarantine rows: `<fill>`
- ACS clean rows: `<fill>`
- ACS quarantine rows: `<fill>`
- DQ monitoring rows appended: `<fill>`

### Post-run SQL Checks
```sql
SELECT COUNT(*) AS silver_health_null_data_value
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.silver_health_outcomes_clean
WHERE data_value IS NULL;

SELECT COUNT(*) AS cdc_quarantine_rows
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.silver_health_outcomes_quarantine;

SELECT COUNT(*) AS acs_quarantine_rows
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.silver_socioeconomic_quarantine;
```

### Results
- `silver_health_null_data_value`: `<fill>`
- `cdc_quarantine_rows`: `<fill>`
- `acs_quarantine_rows`: `<fill>`

### Evidence
- Output/log screenshot or text: `docs/evidence/<run_folder>/04_silver_output.txt`

---

## 4) Gold Build + Validation (Tasks 05/06)

### Output Snapshot (Task 05)
- Gold row count: `<fill>`
- Distinct counties: `<fill>`
- Distinct measures: `<fill>`

### Output Snapshot (Task 06)
- Gold row count: `<fill>`
- Rows with null key metrics: `<fill>`
- Gold DIABETES avg: `<fill>`
- Silver DIABETES avg (join-aligned): `<fill>`
- DIABETES avg diff: `<fill>`
- DQ gold summary rows appended: `<fill>`
- Validation status: PASS / FAIL

### Post-run SQL Checks
```sql
SELECT COUNT(*) AS gold_null_data_value
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE data_value IS NULL;
```

### Result
- `gold_null_data_value`: `<fill>`

### Evidence
- Output/log screenshot or text: `docs/evidence/<run_folder>/05_gold_output.txt`
- Output/log screenshot or text: `docs/evidence/<run_folder>/06_gold_validation_output.txt`

---

## 5) DQ Monitoring Tables

### Latest Monitoring Rows
```sql
SELECT *
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.dq_monitoring_runs
ORDER BY run_ts DESC
LIMIT 10;

SELECT *
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.dq_gold_validation_summary
ORDER BY run_ts DESC
LIMIT 10;
```

### Observed Status
- Silver monitoring latest status: `<fill>`
- Gold monitoring latest status: `<fill>`

### Evidence
- Query result screenshot/text: `docs/evidence/<run_folder>/07_dq_monitoring_queries.md`

---

## 6) Idempotency Verification

### Rerun Scope
- Full DAG rerun or partial rerun (`04 -> 05 -> 06`): `<fill>`

### Expected vs Observed
- Snapshot tables (`bronze_*`, `silver_*`, `gold_*`) overwrite without duplicates: Yes / No
- History tables (`dq_monitoring_runs`, `dq_gold_validation_summary`) append per run: Yes / No

### Notes
`<fill>`

---

## 7) Submission/Review Notes

- Key risk(s) observed in run: `<fill>`
- Mitigation(s) applied: `<fill>`
- Ready for demo/submission: Yes / No

---

## 8) Artifact Index

- `01_dag_graph.png`
- `02_dag_timeline.png`
- `03_bronze_validation_output.txt`
- `04_silver_output.txt`
- `05_gold_output.txt`
- `06_gold_validation_output.txt`
- `07_dq_monitoring_queries.md`

(Replace `<run_folder>` with your actual run artifact directory, e.g. `a6_run_20260328_1205`.)
