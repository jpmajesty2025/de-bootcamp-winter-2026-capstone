# Execution Checklist — Capstone MVP Sprint

**Date:** 2026-03-26  
**POC:** Capstone Student  
**TL;DR:** Execute protected-core MVP by 2026-03-28: reliable medallion pipeline, dashboard-first demo, citation-grounded agent workflow, lean eval gate, and cloud runbook.

---

## Status Legend
- **NS** = Not Started
- **IP** = In Progress
- **BLK** = Blocked
- **DONE** = Complete

---

## MVP Non-Negotiables (Q10 Protected Core)
- [ ] **P0** Running Bronze/Silver/Gold pipeline for CDC PLACES + ACS with data quality checks
- [ ] **P0** Gold-layer dashboard answers required demo analytics questions
- [ ] **P0** Citation-grounded agent workflow over locked 5-collection CDC/WHO corpus
- [ ] **P0** Lean MVP evaluation gate (15–25 questions + threshold checks)
- [ ] **P0** Cloud-running deployment + concise runbook

---

## Agentic Implementation Boundary (Explicit)

**In MVP (yes):**
1. **Structured analytics lane:** Databricks **Genie** for text→SQL over governed Gold tables.
2. **Document evidence lane (primary):** Databricks **Agent Bricks Knowledge Assistant** over the locked 5 CDC/WHO collections (docs landed to UC Volume, managed citations/guardrails).
3. **Document evidence lane (fallback):** notebook-based citation RAG over Vector Search if Agent Bricks is temporarily unavailable.

**Not in MVP core (defer):**
- Supervisor Agent patterns
- Custom multi-agent orchestration via LangChain/LangGraph

**Why:** protect 2026-03-28 MVP reliability and keep execution aligned to DE-first capstone grading while using Databricks-managed agentic capability where it is lowest risk and fastest to ship.

---

## Workstream Board

## A) Data Pipeline (P0)

| ID | Task | Priority | Status | Owner | Estimate | Depends On | Done Criteria |
|---|---|---|---|---|---|---|---|
| A1 | CDC PLACES Bronze ingestion operational | P0 | NS | You | 1–2h | None | Raw ingest runs successfully with ingestion metadata |
| A2 | ACS Bronze ingestion operational | P0 | NS | You | 1–2h | None | Raw ingest runs successfully with ingestion metadata |
| A3 | Silver conformance (FIPS/schema/date normalization) | P0 | NS | You | 2–3h | A1, A2 | Conformed Silver tables queryable and keyed consistently |
| A4 | Gold fact tables (county burden + SDOH joins) | P0 | NS | You | 2–3h | A3 | Gold marts populated and dashboard-ready |
| A5 | Data quality checks (schema/null/unique/range/ref/freshness) | P0 | NS | You | 2h | A3, A4 | DQ checks pass or exceptions documented with rationale |
| A6 | End-to-end scheduled run validated | P0 | NS | You | 1h | A1–A5 | One full run completes reproducibly |

---

## B) Document/RAG Ingestion (P0)

| ID | Task | Priority | Status | Owner | Estimate | Depends On | Done Criteria |
|---|---|---|---|---|---|---|---|
| B1 | Land locked 5 CDC/WHO source docs into Unity Catalog Volume (with fallbacks) | P0 | NS | You | 2–3h | None | All 5 sources landed and tracked in UC Volume |
| B2 | Configure Agent Bricks Knowledge Assistant source and build | P0 | NS | You | 1–2h | B1 | KA build completes successfully for selected corpus |
| B3 | Deploy/verify KA serving endpoint for document Q&A | P0 | NS | You | 1–2h | B2 | Endpoint is queryable and returns grounded responses |
| B4 | Validate citations/guardrails on KA responses | P0 | NS | You | 1h | B3 | Citations are human-verifiable and guardrails behave as expected |
| B5 | Fallback path smoke test: notebook-based citation RAG over Vector Search | P1 | NS | You | 1h | B1 | Fallback path documented and minimally validated |

---

## C) Dashboard (P0)

| ID | Task | Priority | Status | Owner | Estimate | Depends On | Done Criteria |
|---|---|---|---|---|---|---|---|
| C1 | Final KPI/visual shortlist mapped to 3 demo questions | P0 | NS | You | 45m | A4 | KPI list approved and query-backed |
| C2 | Build dashboard views (burden, SDOH association, rural/urban) | P0 | NS | You | 2–3h | C1 | Core views implemented and filterable |
| C3 | Reconcile dashboard numbers vs gold tables | P0 | NS | You | 1h | C2 | No major contradictions |
| C4 | Demo-ready polish (labels, filters, readability) | P1 | NS | You | 45m | C3 | Dashboard understandable in <2 min walkthrough |

---

## D) Agentic Workflow (P0)

| ID | Task | Priority | Status | Owner | Estimate | Depends On | Done Criteria |
|---|---|---|---|---|---|---|---|
| D1 | Implement two-lane query path (Genie for structured, KA for document evidence) | P0 | NS | You | 1–2h | B3, C3 | Routing/usage pattern is clear and testable in demo flow |
| D2 | Enforce citation-grounded document answers via KA | P0 | NS | You | 1h | D1, B4 | Document-lane responses include relevant citations |
| D3 | 3 demo questions + paraphrase test pass across lanes | P0 | NS | You | 1h | D2, C3 | Acceptable answer quality across variants and both lanes |
| D4 | Verify abstention behavior for weak/unsupported evidence | P1 | NS | You | 45m | D2 | System clearly abstains when support is insufficient |

---

## E) Evaluation (P0)

| ID | Task | Priority | Status | Owner | Estimate | Depends On | Done Criteria |
|---|---|---|---|---|---|---|---|
| E1 | Build 15–25 question eval set | P0 | NS | You | 1–2h | D1 | Eval set covers factual/synthesis/equity questions |
| E2 | Run eval and score core metrics | P0 | NS | You | 1–2h | E1, D2 | Metrics computed and saved |
| E3 | Threshold check + remediation pass | P0 | NS | You | 1–2h | E2 | Meets target bars or mitigation documented/re-run done |
| E4 | Log baseline comparison in MLflow | P1 | NS | You | 45m | E2 | One comparative experiment logged |
| E5 | Eval summary artifact for demo/proposal | P0 | NS | You | 45m | E3 | Summary ready for presentation |

**Target thresholds (MVP):**
- Groundedness/Faithfulness: **>= 80%**
- Citation correctness: **>= 85%**
- Relevance: **>= 80%**
- Failure rate: **< 10%**
- Latency: **p95 ~10–15s target**
- Demo reliability: **>= 80% pass/question**, **0 fabricated citations**

---

## F) Demo & Delivery (P0)

| ID | Task | Priority | Status | Owner | Estimate | Depends On | Done Criteria |
|---|---|---|---|---|---|---|---|
| F1 | 5–7 minute demo script (dashboard-first, agent-second) | P0 | NS | You | 1h | C4, D3 | Script clear and timed |
| F2 | Backup artifacts (screenshots, fallback queries) | P1 | NS | You | 45m | C4, D3 | Recovery path exists if live issue occurs |
| F3 | Concise runbook (pipeline, dashboard refresh, eval run) | P0 | NS | You | 1h | A6, E3 | Another reviewer could follow steps |
| F4 | Full timed dry run | P0 | NS | You | 1h | F1–F3 | Uninterrupted dry run completed |

---

## Daily Gates (Timeline Reset: start 2026-03-26)

### Thu 2026-03-26
- Focus: A1–A5, B1–B2
- Gate: Bronze/Silver stable + initial Gold draft queryable

### Fri 2026-03-27
- Focus: A6, B3–B5, C1–C3
- Gate: Dashboard answers demo analytics questions from Gold data + KA endpoint returns cited responses

### Sat 2026-03-28
- Focus: D1–D4, E1–E4, F1
- Gate: Agent quality near/at thresholds with remediation list closed or minor-only

### Sun 2026-03-29 (MVP Functional Target)
- Focus: E5, F2–F4
- Gate: End-to-end demo-ready system + runbook + eval evidence

---

## Scope-Cut Defer Order (If Needed)
1. DAB packaging/environment promotion automation  
2. Eval depth beyond lean MVP gate  
3. Corpus expansion beyond locked 5 collections  
4. Extra UX polish beyond required dashboard + agent path  
5. Graph RAG / streaming work (Phase 2)

---

## Blockers / Notes Log

| Date | Workstream | Blocker | Impact | Mitigation | Status |
|---|---|---|---|---|---|
| 2026-03-26 | — | Timeline reset: execution starts from A) Data Pipeline with all tasks at NS | 1-day schedule compression | Prioritize P0 tasks only; defer all P1 unless ahead of schedule | Open |

---

## End-of-Day Update Template
- **Date:** YYYY-MM-DD
- **Completed:**  
- **In Progress:**  
- **Blocked:**  
- **Metrics snapshot:**  
- **Plan tomorrow:**