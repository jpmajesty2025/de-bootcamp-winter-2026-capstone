# D1 Two-Lane Demo Runbook (Genie + Knowledge Assistant)

**Date:** 2026-03-29  
**POC:** Capstone Student  
**TL;DR:** Run Q1/Q2 in Genie (structured Gold data) and Q3 in Knowledge Assistant (CDC/WHO docs with citations), then capture screenshots and mark D1 complete.

---

## 1) Lane Mapping (Required)

| Demo Question | Lane | System |
|---|---|---|
| Q1. Which counties show the worst diabetes burden, and what social factors are most associated with those outcomes? | Structured | Genie (text-to-SQL on Gold) |
| Q2. Compare rural vs urban patterns for obesity and heart disease in [state/region], and explain likely drivers. | Structured (proxy-based) | Genie (Gold + poverty/income proxy interpretation) |
| Q3. What evidence-based interventions do CDC/WHO sources recommend for high-burden communities? | Document evidence | Knowledge Assistant (`health-equity-assistant`) |

---

## 2) Preconditions

- Gold table available: `bootcamp_students.health_equity_capstone_jpmajesty2019.gold_health_equity_stats`
- KA deployed: `health-equity-assistant` (endpoint: `ka-37b81bfb-endpoint`)
- Vector index online: `bootcamp_students.health_equity_capstone_jpmajesty2019.cdc_who_docs_index`
- Dashboard C3 reconciliation completed (no major contradictions)

---

## 3) Execution Steps

### Step A — Genie (Q1, Q2)
1. Open Genie space connected to Gold analytics table(s).
2. Ask Q1 exactly.
3. Ask Q2 exactly (or with specific state/region).
4. Confirm generated SQL references expected Gold fields (`measure_id`, `data_value`, `poverty_pct`, `median_household_income`, `county_name`, `state_abbr`).
5. Cross-check outputs with dashboard visuals/KPIs for consistency.

### Step B — Knowledge Assistant (Q3)
1. Open `health-equity-assistant`.
2. Ask Q3 using self-contained wording:
   - “According to the CDC and WHO sources in this assistant, what evidence-based interventions are recommended to reduce health inequities in high-burden communities?”
3. Confirm citations appear and are relevant to source passages.

---

## 4) Pass Criteria (D1)

- Q1/Q2 answers are consistent with Gold/dashboard data.
- Q3 answer is citation-grounded in CDC/WHO corpus.
- No fabricated citations.
- Routing behavior is clear:
  - structured analytics questions → Genie
  - document evidence/intervention questions → KA

---

## 5) Evidence to Capture

1. Screenshot: Genie Q1/Q2 response + SQL trace (or SQL preview)
2. Screenshot: KA Q3 response with citations visible
3. Optional note: any lane-routing caveat observed

Save under `docs/` (timestamped filenames).

---

## 6) Completion Update

After evidence capture:
- Set `D1` to `DONE` in `docs/execution_checklist.md`
- Append D1 evidence summary in `docs/session_notes.md`
- Set `D2` to `IP`
