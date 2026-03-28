# A6 End-to-End Validation Report

**Date:** YYYY-MM-DD  
**POC:** Capstone Student  
**Environment:** Databricks (Catalog: `bootcamp_students`, Schema: `health_equity_capstone_jpmajesty2019`)  
**Job Name:** DE Winter 2026 Bootcamp Capstone DAG  
**Run ID:** 696785468775406  
**Run Start / End:** Mar 28, 2026, 04:10 PM \ Mar 28, 2026, 04:13 PM
**Overall Result:** PASS

---

## 1) DAG Execution Summary

### Task Flow
`00_setup_env -> (00a_download_cdc, 00b_download_acs) -> (01_ingest_cdc, 02_ingest_acs) -> 03_validate_bronze -> 04_conformed_silver -> 05_build_gold -> 06_validate_gold`

### Run Outcome
- All tasks green: Yes
- Retries triggered: No
- Duration warnings triggered: No
- Failures: none

### Evidence
- DAG graph screenshot: `docs/evidence/696785468775406/01_dag_graph.png`
- DAG timeline screenshot: `docs/evidence/696785468775406/02_dag_timeline.png`

---

## 2) Bronze Validation (Task 03)

### Output Snapshot
- CDC Bronze row count: 229298
- ACS Bronze row count: 3222
- Null metadata rows (CDC): 0
- Null metadata rows (ACS): 0
- Validation status: PASS

### Evidence
- Output/log screenshot or text: `docs/evidence/696785468775406/03_bronze_validation_output.txt`

---

## 3) Silver Conformance + Quarantine (Task 04)

### Output Snapshot
- CDC clean rows: 229232 
- CDC quarantine rows: 66
- ACS clean rows: 3220
- ACS quarantine rows: 2
- DQ monitoring rows appended: 2

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
- `silver_health_null_data_value`: 0
- `cdc_quarantine_rows`: 66
- `acs_quarantine_rows`: 2

### Evidence
- Output/log screenshot or text: `docs/evidence/696785468775406/04_silver_output.txt`

---

## 4) Gold Build + Validation (Tasks 05/06)

### Output Snapshot (Task 05)
- Gold row count: 229006 
- Distinct counties: 3141
- Distinct measures: 40

### Output Snapshot (Task 06)
- Gold row count: 229006
- Rows with null key metrics: 0
- Gold DIABETES avg: 12.400982
- Silver DIABETES avg (join-aligned): 12.400982
- DIABETES avg diff: 0.0
- DQ gold summary rows appended: 1
- Validation status: PASS

### Post-run SQL Checks
```sql
SELECT COUNT(*) AS gold_null_data_value
FROM bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats
WHERE data_value IS NULL;
```

### Result
- `gold_null_data_value`: 0

### Evidence
- Output/log screenshot or text: `docs/evidence/696785468775406/05_gold_output.txt`
- Output/log screenshot or text: `docs/evidence/696785468775406/06_gold_validation_output.txt`

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
- Silver monitoring latest status: WARN/PASS
- Gold monitoring latest status: PASS

### Evidence
- Query result screenshot/text: `docs/evidence/696785468775406/07_dq_monitoring_runs.csv, */08_dq_gold_validation_summary.csv`

---

## 6) Idempotency Verification

### Rerun Scope
- Full DAG rerun or partial rerun (`04 -> 05 -> 06`): Full DAG run

### Expected vs Observed
- Snapshot tables (`bronze_*`, `silver_*`, `gold_*`) overwrite without duplicates: Yes
- History tables (`dq_monitoring_runs`, `dq_gold_validation_summary`) append per run: Yes

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
