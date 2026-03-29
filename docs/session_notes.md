# Capstone Project Session Notes
**Project:** Winter 2026 DE Bootcamp Capstone
**Last Updated:** 2026-03-28

---

## Purpose
Running log of decisions, answers to clarifying questions, and next steps. Updated each session to survive context resets.

---

## Project Background
- **Bootcamp:** 5-week Data Engineering Bootcamp (Databricks-heavy) + Analytics Engineering Bootcamp
- **Timeline:** Today is Week 1, last day (as of ~2026-02-20 brainstorm session)
- **Requirements:** Pipeline, data quality controls, documentation/visualization, deployed in cloud, conceptual data model due end of Week 3

## Theme
Health-related data: CDC, WHO, and related public health APIs/datasets.

## Candidate Ideas (from brainstorm doc)
1. **Public Health Intelligence Platform** — multi-layered pipeline, structured + unstructured, AI agent *(recommended)*
2. **Chronic Disease & Social Determinants Correlator** — CDC PLACES + Census ACS, analytics-heavy *(more tractable)*
3. **Vaccine Coverage vs. Disease Outbreak Tracker** — streaming-forward, Kafka-centric
4. **Health Document RAG Pipeline** — AI/unstructured-forward, Cortex AI + Databricks agent

---

## Clarifying Questions & Decisions
*(5 hypothesized questions from lost session — awaiting user confirmation)*

- [x] Q1: **Platform confirmed: Databricks workspace (bootcamp-provided) + S3 cloud storage.** Stack is Databricks-native (Delta Lake on S3). Snowflake not required (AE bootcamp tools optional).
- [x] Q2: **Scope of pipeline.** Expand beyond unstructured CDC docs. Two confirmed sources: CDC PLACES (structured, county-level chronic disease metrics) + CDC/WHO PDFs (unstructured). Both Vector RAG and Graph RAG included. User has Neo4j Academy background — graph layer is a key differentiator.
- [x] Q3: **Frontend / Visualization.** *(Discussed 2026-03-14, PDT)* Capstone requires a visualization (per Zach Wilson). 

  **Decision: Keep VitalDocs AI and the DE capstone pipeline decoupled.** Focus capstone effort on building a robust Databricks DE workflow. VitalDocs AI appears in the demo as narrative context — "the future product this pipeline will power" — not as a capstone deliverable.

  **Visualization options considered:**
  - **Option A (chosen for capstone):** Databricks SQL Dashboard — native, zero extra infra, directly queries gold Delta tables. The capstone visualization deliverable.
  - **Option B (product roadmap):** Add `/analytics` route to VitalDocs AI — pulls from Databricks SQL REST API, embedded charts/maps. More cohesive product but additive scope post-capstone.
  - **Option C:** Streamlit on Databricks — more interactive than SQL Dashboard, still no extra infra.
  - **Option D:** External BI (Tableau, Power BI) — overkill, adds infra complexity for no capstone credit.

  **Light pointer:** A link/button in VitalDocs AI pointing to the Databricks SQL Dashboard is ~10 min of work and tells a great demo story. ✅ Include this.

  **Backend swap (Supabase pgvector → Databricks Vector Search) is explicitly OUT of capstone scope.** That is a post-capstone product evolution. Supabase/OpenAI chat backend stays as-is for now.

  **Product vision (post-capstone):** Combined Chat + Analytics SaaS is a valid and forward-looking product direction (consistent with Databricks Genie, Tableau Pulse, Snowflake Cortex Analyst positioning). VitalDocs AI evolution: (1) `/analytics` route added, (2) chat backend swapped to Databricks Model Serving. Design system ("Clinical SaaS" aesthetic) requires no changes. Navigation: add "Search" + "Analytics" tabs.

  Sub-questions answered *(2026-03-14)*:
  - (a) **Post-capstone plans:** User is actively job-seeking (laid off ~1 year). Continuing to build VitalDocs AI is career-relevant. Backend swap (Supabase → Databricks) is a meaningful post-capstone milestone.
  - (b) **Review format:** AI auto-grader first, then human review by TAs and/or Zach Wilson.
  - (c) **Data strategy / health topic:** See Data Strategy section below.

---

## Data Strategy *(2026-03-14)*

The capstone pipeline has two outputs: (1) **Analytics dashboard** — structured data visualized; (2) **RAG agent** — NL Q&A over documents. Structured data and unstructured docs must tell the same health story.

**Three options considered:**

| Option | Structured Data | Unstructured Docs | Story |
|---|---|---|---|
| A) Chronic Disease | CDC PLACES (county-level: diabetes, obesity, heart disease, mental health) | CDC chronic disease guidelines + WHO prevention reports | "Where are Americans sickest, and what do guidelines recommend?" |
| B) Infectious Disease | CDC NIS (vaccine coverage) + CDC Wonder API (disease incidence) | CDC/WHO immunization guidelines, outbreak reports | Closest to VitalDocs AI original focus |
| C) Health Equity *(recommended)* | CDC PLACES + Census ACS (income, education, food access by county) | CDC health equity reports, WHO social determinants docs | "Which communities face worst health outcomes, and why?" |

**Option C recommended** — most analytically rich, strongest joins story (CDC PLACES + Census ACS = two clean structured sources), most visually compelling dashboard, resonates with hiring audience.

**VitalDocs AI tie-in with Option C:** Architectural, not thematic. VitalDocs AI's value is the pattern ("NL questions over health docs → cited answers"), not the specific topic. Story: *"Vibe Coding bootcamp → VitalDocs AI MVP in 48hrs using off-the-shelf components. DE capstone → production data platform powering same product vision: medallion pipeline, structured analytics, graph RAG, LLMOps."* Topic shift from infectious disease to health equity is a non-issue in this framing.

**Decision: Option C confirmed. *(2026-03-14)***

---

## Out-of-Scope Query Handling *(2026-03-14)*

**Context:** VitalDocs AI currently fails gracefully (low retrieval confidence) on topics outside its corpus. This is the product motivation for the DE capstone. A richer handling strategy was discussed — likely MVP++ tier or post-capstone, since MVP++ has plenty of DE workflow work without touching VitalDocs AI. Still a compelling demo story regardless of current VitalDocs AI behavior.

**Actions identified when a user asks an out-of-scope question:**

| Action | Value | Tier |
|---|---|---|
| Log query + user + timestamp to `failed_queries` table | Corpus gap analysis | MVP+ |
| Auto-classify query into health topic taxonomy (LLM call) | Structured demand signals, not just raw text | MVP+ |
| Track query frequency by topic cluster | High-demand topics bubble up automatically | MVP+ |
| Track per-user query history | Personalization, user-level demand signals | MVP+ |
| Return "notify me" CTA — user opts in for alerts when topic available | Demand validation + retention | MVP+ |
| Feed `failed_queries` back into Databricks pipeline as corpus expansion signal | Closes the loop — user demand drives ingestion | MVP++ |
| Admin dashboard showing top unmet topics | Product/operator visibility | MVP++ |
| A/B test graceful degradation messages | Optimize "notify me" CTA conversion | MVP++ |

**The closed loop (MVP++):** VitalDocs AI failures → `failed_queries` table → Databricks pipeline prioritization → new gold data → expanded RAG corpus → VitalDocs AI answers those questions. A genuine product feedback loop.

**VitalDocs AI changes required (when pursued):**
1. Expose retrieval confidence score; add threshold check for out-of-scope detection
2. API route: write to `failed_queries` table (Supabase now, Databricks REST API post-capstone)
3. Response logic: graceful degradation message + optional "notify me" button
4. New Supabase table: `failed_queries` (query_text, user_id, timestamp, auto_classified_topic, confidence_score)

**Capstone scope ruling:** MVP++ or post-capstone. DE workflow itself has sufficient depth to fulfill MVP++ without touching VitalDocs AI. Demo story works regardless of current VitalDocs AI out-of-scope behavior.



**Product motivation framing (locked):** The thematic disconnect between VitalDocs AI's current corpus (infectious disease/immunization) and Option C (chronic disease + health equity) is not a weakness — it's the product narrative. Current VitalDocs AI gracefully fails on out-of-scope questions (e.g., diabetes management, county health outcomes). The DE capstone is the infrastructure that closes that gap. Demo moment: show VitalDocs AI failing on a chronic disease question today → show the capstone pipeline answering it.

> *"VitalDocs AI launched with a narrow corpus. Real users immediately asked questions it couldn't answer. The DE capstone builds the data infrastructure that closes that gap — medallion pipeline, CDC PLACES + Census ACS structured data, broadened document corpus, graph-enriched retrieval, production-grade RAG agent. Same product vision, dramatically expanded scope."*
- [x] Q4: **Streaming.** *(Decided 2026-03-14)* **Not included — no legitimate business case.** CDC PLACES, Census ACS, and CDC/WHO PDFs all publish on annual/periodic cycles with no sub-hour latency requirements. Batch ingestion (Airflow/scheduled Databricks jobs) is the correct pattern. Streaming is not a capstone requirement. Simulating Kafka just to check a box would be the wrong call. Proposal will include explicit rationale: *"Streaming evaluated and ruled out — data sources publish periodically with no sub-hour latency requirements. Batch ingestion is the appropriate pattern."* Demonstrates stronger engineering judgment than a forced streaming implementation.
- [x] Q5: **Timeline.** *(Decided 2026-03-14)* Week 5 begins 2026-03-16. No official due date listed yet — based on prior bootcamp experience, likely 2026-03-29 11:59pm (week after classes end), possibly 2026-03-22 11:59pm if earlier. **Working assumption: target MNVP by 2026-03-22 (hard internal deadline), full MVP by 2026-03-29.** Week 5 covers AI agent components — designing around them is fully justified given Week 5 starts in 2 days.

---

## Reconstructed Plan (from prior lost session + 3/14 reconstruction)
- Direction confirmed: **use VitalDocs AI MVP as jumping-off point** for DE capstone
- 3-tier plan fully reconstructed below

---

## 3-Tier Capstone Plan

### MNVP — Vector RAG + Medallion Pipeline
- Ingest CDC PLACES (structured) + CDC/WHO PDFs (unstructured) → bronze/silver/gold on Delta Lake/S3
- Vector embeddings of PDF chunks → Databricks Vector Search
- Basic Databricks AI agent: natural language → vector retrieval → cited answers
- Joins requirement met: CDC PLACES county metrics + WHO document context joined at query time
- **LLMOps (MNVP):** MLflow experiment tracking — log prompt templates, chunk size, embedding model, top-k, latency as artifacts/metrics; **Prompt Registry** (MLflow 2.4+) for versioned prompt management; **Unity Catalog** from day one — register vector indexes, models, and gold tables as governed assets; **`mlflow.evaluate()`** for hallucination detection and RAG quality scoring

### MVP+ — Graph RAG Layer (Neo4j)
- Entity extraction from ingested documents: diseases, conditions, risk factors, interventions, geographic entities, medications
- Knowledge graph in **Neo4j Aura** (hosted, accessible from Databricks)
  - Nodes: Disease, Condition, RiskFactor, Intervention, County, Document
  - Relationships: `ASSOCIATED_WITH`, `INCREASES_RISK_OF`, `RECOMMENDED_FOR`, `LOCATED_IN`, `CITED_BY`
- Upgraded agent: queries both vector index AND graph (graph for multi-hop, vector for semantic)
- Example power query: *"Which counties have high diabetes prevalence AND low fruit/vegetable access, and what do CDC guidelines recommend?"*
- **LLMOps (MVP+):** `mlflow.evaluate()` for hallucination detection, relevance, faithfulness, completeness scoring; retrieval quality metrics (precision@k, context recall); compare vector-only vs graph+vector as MLflow experiments; **AI Gateway** — centralized access control, rate limiting, and cost tracking for external model endpoints (OpenAI/Anthropic)

### MVP++ — Hybrid RAG + Streaming + Production LLMOps
- **Hybrid retrieval**: dynamic routing — graph-first for relational/multi-hop, vector-first for semantic, fused for complex queries
- **Streaming layer**: Kafka → Delta Live Tables for simulated real-time health surveillance events (new incidence reports trigger graph/pipeline updates)
- **Agentic reasoning loop**: agent autonomously chooses graph traversal, vector search, structured gold table query, or combination
- **Dashboard**: Databricks SQL + Neo4j Bloom graph visualization
- **LLMOps (MVP++):** Monitoring dashboard (latency, token cost, hallucination rate, retrieval relevance trends); A/B testing of retrieval strategies; automated quality alerts if relevance drops; streaming events → pipeline reruns → LLMOps monitors impact of new data on answer quality; **Databricks Model Serving** — serverless GPU hosting for custom embedding or fine-tuned models; **Databricks Asset Bundles (DABs)** — infrastructure-as-code for full pipeline deployment (dev → staging → production); **CI/CD via Databricks Git folders + MLOps Stacks** — automated environment promotion for pipeline and agent changes

---

## How Capstone Requirements Are Met

| Requirement | How It's Met |
|---|---|
| Pipeline | Bronze→Silver→Gold medallion + entity extraction pipeline |
| Two+ data sources with joins | CDC PLACES (structured) + WHO/CDC PDFs (unstructured) — joined via graph and at query time |
| Data quality controls | Delta Live Table expectations |
| Agentic action | Hybrid RAG agent with graph + vector + structured retrieval |
| Cloud deployed | Databricks on S3 + Neo4j Aura |
| Weeks 3–5 coverage | Unstructured (Wk3) + Streaming (Wk4) + AI Agent (Wk5) |
| LLMOps | MLflow throughout all tiers — experiment tracking → evaluation → production monitoring |

---

## Proposal Sections Required (per TA)
1. Project Description / Scope
2. Conceptual Data Model & Diagram
3. Tools, Data Sources and Formats
4. Ingestion Strategy, Data Quality Checks
5. Success Metrics, Stakeholder Value

## Capstone Technical Requirements
- One or more pipelines
- Data quality controls
- Deployed and running in the cloud
- Must have agentic action(s)
- At least two data inputs with meaningful joins, aggregations, gold-standard output (medallion architecture)

---

## Open Items
- [x] User to confirm/correct the 5 clarifying questions and their answers
- [x] Reconstruct 3-tier MNVP/MVP+/MVP++ plan
- [x] Draft capstone proposal: `docs/de_capstone_proposal_draft_1.md`

---

## Session Log
| Date | Summary |
|------|---------|
| ~2026-02-20 | Initial brainstorm — 4 ideas generated, saved to `docs/winter_2026_de_bootcamp_capstone_brainstorm_1.md` |
| ~2026-02-22 | Vibe Coding bootcamp brainstorm → VitalDocs AI proposal created (`PROPOSAL.md`) |
| 2026-03-13 AM | Multi-hour session: reviewed all docs, developed 3-tier plan, was about to draft proposal — lost to API timeout |
| 2026-03-13 PM | Session recovery. Read all available docs. Reconstructed context. Identified 5 missing clarifying Q&A. User confirmed: update session notes after every exchange. |

---

## Planning Resumption Questions *(2026-03-25)*

In light of `docs/de_capstone_proposal_draft_1.md` and `docs/resumption_of_planning.md`, these are the 10 questions to finalize scope and execution.

### Critical decisions
1. **Primary demo experience:** Should the capstone front door be Dashboard-first (gold tables + BI) or Agent-first (chat/Genie + tools), with the other secondary?
2. **Graph RAG direction:** Keep Neo4j Graph RAG as core scope, or pivot to a Databricks-native supervisor pattern (Genie + Knowledge Assistant) and treat graph as Phase 2?
3. **RAG corpus scope:** Which exact 3–5 CDC/WHO document collections are in MVP scope?
4. **Deployment target:** DAB-based deployment (production-grade) or notebook/manual deployment (faster, lower risk) for submission?

### Execution constraints
5. **Deadline + grading emphasis:** For evaluation, what matters most—architecture completeness, demo polish, or measurable LLM eval quality?
6. **Workspace limits:** Any constraints on Databricks compute, serving endpoints, Vector Search, or external services?
7. **Freshness expectations:** Is batch-only ingestion acceptable for MVP, with streaming/Kafka-DLT as future extension?

### Success criteria
8. **Must-answer demo questions:** What are the top 3 user questions the system must answer reliably?
9. **Agent quality bar:** Do we require explicit eval thresholds (e.g., groundedness/faithfulness), or a qualitative rubric only?
10. **Scope guardrails:** If we cut 20–30% scope, which features are non-negotiable?

**Status:** Q1–Q9 decided (below). Q10 pending; once answered, produce finalized implementation plan and execution timeline.

### Q1 Decision Memo *(2026-03-25)*
**Question:** Should the capstone primary demo be Dashboard-first or Agent-first?

**Context:** This is a Data Engineering bootcamp with a Databricks-first expectation. Agentic workflow is required, but not the core instructional focus.

**Options considered:**
- **Dashboard-first (Agent secondary):**
  - **Pros:** Strongest alignment to DE grading criteria (medallion outputs, joins, data quality, gold-layer analytics), lower live-demo risk, clearer stakeholder value for health equity.
  - **Cons:** Less “AI wow” if agent integration is weak.
- **Agent-first (Dashboard secondary):**
  - **Pros:** Strong Week 5 AI narrative, compelling conversational UX, clear product-forward story.
  - **Cons:** Higher demo fragility and risk of under-emphasizing DE rigor.

**Final recommendation (accepted):**
- **Choose Dashboard-first as primary demo spine.**
- **Include agentic workflow as a required, prominent secondary layer** (not optional), demonstrating natural-language Q&A with citations over the same governed data foundation.

**Narrative to use in proposal/demo:**
> “Trusted data engineering foundation first, intelligent access second.  
> We built reliable Databricks medallion pipelines and analytics outputs, then added an agentic interface to make those insights conversational and evidence-backed.”

**Implementation implication:** All milestone planning should optimize first for DE reliability/completeness, while ensuring agentic action is clearly implemented and demonstrable for capstone requirements.

### Q2 Decision Memo *(2026-03-25)*
**Question:** Should Neo4j Graph RAG remain core MVP scope, or move to Phase 2?

**Decision (accepted):**
- **Move Graph RAG to Phase 2** (post-MVP scope) due to time constraints.
- Keep MVP focused on Databricks-native DE deliverables + required agentic workflow.

**Rationale:**
- Current date is **2026-03-25** with due date **2026-03-29**.
- Team target is **fully deployed, running MVP by 2026-03-28**, reserving **2026-03-29** for polish and selective low-hanging enhancements.
- Graph RAG adds significant integration and evaluation overhead that increases delivery risk under current timeline.

**Timeline lock:**
- **MVP functional deadline:** 2026-03-28
- **Polish/buffer day:** 2026-03-29
- **Graph RAG:** explicitly deferred to Phase 2 / stretch work only if schedule permits after MVP hardening.

**Implementation implication:** Planning should prioritize deterministic pipeline reliability, gold-layer dashboard quality, and a clear/working agentic action path before any graph expansion.

### Q3 Decision Memo *(2026-03-25)*
**Question:** Which exact 3–5 CDC/WHO document collections are in MVP scope?

**Decision (accepted):**
- **Adopt Option B (5 collections)** as the MVP RAG corpus scope.

**Confirmed collections (verified available):**
1. **CDC Advancing Health Equity Collection**  
   - Primary: https://www.cdc.gov/pcd/collections/Advancing_Health_Collection.htm  
   - Fallback PDF: https://www.cdc.gov/pcd/collections/pdf/health-disparities-collection_508.pdf
2. **CDC Mapping Chronic Disease Collection**  
   - Primary: https://www.cdc.gov/pcd/collections/Mapping_Chronic_Disease.htm  
   - Fallback PDF: https://www.cdc.gov/pcd/collections/pdf/gis_collection.pdf
3. **CDC Rural Health Disparities (2025)**  
   - Primary: https://www.cdc.gov/pcd/issues/2025/25_0202.htm  
   - Fallback PDF: https://www.cdc.gov/pcd/issues/2025/pdf/25_0202.pdf
4. **CDC Health Equity Science / SDOH Documentation**  
   - Primary: https://www.cdc.gov/health-equity-chronic-disease/hcp/health-equity-science/index.html  
   - Fallback PDF: https://www.cdc.gov/cardiovascular-resources/media/pdfs/surveillance_evaluation_guide-508.pdf
5. **WHO World Health Statistics 2025**  
   - Primary: https://www.who.int/publications/b/78420  
   - Fallback direct PDF: https://iris.who.int/server/api/core/bitstreams/c992fbdc-11ef-43db-a478-7e7a195403ae/content

**Availability confirmation:** All five primary sources were validated as currently accessible.

**Implementation implication:** Start ingestion with stable consolidated PDFs first (WHO + CDC collection PDFs), then layer web-first pages with PDF fallbacks to reduce delivery risk before 2026-03-28.

### Q4 Decision Memo *(2026-03-25)*
**Question:** Should deployment target be DAB-based now, or notebook/manual first?

**Decision (accepted):**
- **Use notebook/manual Databricks deployment for MVP (by 2026-03-28).**
- **Treat DAB as post-MVP hardening** for 2026-03-29 (time permitting) or immediate next iteration.

**Clarification:**
- Notebook/manual deployment in Databricks **still satisfies “deployed in the cloud”** for capstone requirements.
- DAB is an advanced packaging/deployment workflow introduced in Week 5, valuable but not required to prove cloud deployment.

**Transition difficulty (manual → DAB):**
- **Moderate but manageable** if MVP is structured cleanly.
- Expected effort is low-friction when assets are already organized (jobs/pipelines/notebooks, parameters, env-specific configs).

**Low-friction migration path:**
1. Keep notebooks modular by layer/use case (bronze, silver, gold, rag_ingest, eval).
2. Centralize parameters (catalog/schema, paths, table names) instead of hardcoding.
3. Capture execution order as jobs/workflows in Databricks.
4. Add DAB scaffolding after MVP to package same assets and promote across environments.

**Implementation implication:** Prioritize reliable cloud-running MVP first; add DAB only after core functionality, demo flow, and validation checks are stable.

### Q5 Decision Memo *(2026-03-25)*
**Question:** For grading and execution, what should be prioritized: architecture completeness, demo polish, or LLM eval depth?

**Decision (accepted):**
- Prioritize in this order:
  1. **Architecture completeness** (must meet and modestly exceed minimum requirements)
  2. **Demo polish** (clear, credible, stakeholder-friendly)
  3. **LLM eval depth** (lean MVP set now; deeper robustness later)

**Rationale:**
- Timeline is constrained (MVP running by 2026-03-28, polish on 2026-03-29).
- Strong DE fundamentals and a reliable demo are the highest-value grading and delivery levers.
- LLM evaluation remains required, but should be right-sized for schedule.

**Lean MVP LLM eval plan (in scope):**
1. Build a **small gold eval set (15–25 questions)**:
   - factual lookup,
   - synthesis/comparison,
   - county/equity interpretation,
   - optional out-of-scope checks.
2. Score 3 core quality dimensions:
   - **Groundedness/Faithfulness** (supported by retrieved context),
   - **Citation correctness** (source exists and is relevant),
   - **Answer relevance** (answers the asked question).
3. Track minimal operational metrics:
   - latency,
   - failure/error rate,
   - token/cost if easy to capture.
4. Run at least one simple baseline comparison (e.g., top-k or prompt version), logged in MLflow.

**MVP acceptance thresholds (target):**
- Groundedness/Faithfulness: **>= 80%**
- Citation correctness: **>= 85%**
- Relevance: **>= 80%**
- Failure rate: **< 10%**
- Latency: acceptable demo responsiveness (practical target: p95 under ~10–15s)

**Phase-2 hardening (deferred):**
- Larger eval set,
- richer retrieval metrics (precision@k/context recall),
- stronger comparative experiments,
- expanded tracing/monitoring and alerting.

### Q6 Decision Memo *(2026-03-25)*
**Question:** Are there known Databricks workspace constraints (compute/model/vector/external access) that affect scope?

**Decision (accepted):**
- **No known workspace constraints at this time.**
- Proceed with standard bootcamp workspace assumptions and right-sized resource usage.

**Rationale:**
- No explicit limits were communicated during bootcamp.
- Planned MVP workload is moderate (not large-scale or unusually compute-intensive).
- Current scope is practical for capstone scale and timeline.

**Operational assumption:**
- Use conservative/default cluster sizing and avoid over-provisioning.
- If an unexpected quota/permission limit appears, treat as execution risk and pivot to lower-cost fallback settings (smaller batches, fewer docs per run, reduced concurrency).

**Implementation implication:** Continue planning as unconstrained-by-default, while keeping lightweight fallback knobs ready to preserve the 2026-03-28 MVP deadline.

### Q7 Decision Memo *(2026-03-25)*
**Question:** Is batch-only ingestion acceptable for MVP, with streaming/Kafka-DLT deferred?

**Decision (accepted):**
- **Yes — batch-only ingestion is acceptable for MVP.**
- **Streaming capabilities are explicitly deferred** to a later iteration.

**Rationale:**
- Current sources and use case do not require real-time latency.
- Streaming would add complexity without clear MVP value.
- Deferring streaming protects timeline and increases likelihood of a stable deployed MVP by 2026-03-28.

**Implementation implication:** Build and harden scheduled batch ingestion/orchestration now; document streaming as a future enhancement path, not MVP scope.

### Q8 Decision Memo *(2026-03-25)*
**Question:** What are the top 3 demo questions the system must answer reliably?

**Decision (accepted):**
Use the following 3-question demo set:
1. **“Which counties show the worst diabetes burden, and what social factors are most associated with those outcomes?”**
2. **“Compare rural vs urban patterns for obesity and heart disease in [state/region], and explain likely drivers.”**
3. **“Given these disparities, what evidence-based interventions do CDC/WHO sources recommend for similar communities?”**

**Why this set:**
- Covers structured joins and gold-layer analytics (PLACES + ACS),
- demonstrates health equity framing and segmentation,
- proves required agentic workflow with cited unstructured evidence.

**Reliability evaluation protocol (MVP):**
1. For each demo question, create **1 canonical prompt + 2 paraphrases** (9 prompts total).
2. Run each prompt **at least twice** (18 total responses) to test consistency.
3. Score each response on:
   - **Relevance** (answers the actual question),
   - **Groundedness/Faithfulness** (supported by retrieved context),
   - **Citation correctness** (real, relevant source support),
   - **Data consistency** (matches dashboard/gold-table values).

**Pass criteria (MVP):**
- **>= 80% pass rate per demo question** across variants/reruns,
- **>= 85% citation correctness** overall,
- **0 fabricated citations** for demo questions,
- **No major contradictions** with dashboard metrics.

**Implementation implication:** Demo readiness is defined by measurable reliability on these 3 stakeholder questions, not only by successful one-off responses.

### Q9 Decision Memo *(2026-03-25)*
**Question:** Should agent quality be evaluated with explicit numeric thresholds, qualitative rubric, or both?

**Decision (accepted):**
- Use a **hybrid quality model**:
  1. **Numeric thresholds** as internal acceptance gates for MVP readiness.
  2. **Qualitative rubric** for final demo/readability and evaluator-facing quality judgment.

**Where numeric thresholds are already defined:**
- In **Q5 Decision Memo** (overall MVP eval targets).
- In **Q8 Decision Memo** (demo-question reliability protocol).

**Numeric quality checks (MVP):**
- Groundedness/Faithfulness: **>= 80%**
- Citation correctness: **>= 85%**
- Relevance: **>= 80%**
- Failure rate: **< 10%**
- Latency: **p95 under ~10–15s** (practical target)
- Demo reliability: **>= 80% pass per demo question** across variants/reruns; **0 fabricated citations**; no major dashboard contradictions

**Qualitative quality checks (MVP):**
1. **Abstention behavior:** Clearly indicates insufficient evidence when retrieval context is weak.
2. **Citation usability:** Sources are specific and human-verifiable.
3. **Analyst readability:** Response is concise, structured, and decision-useful.
4. **Data consistency narrative:** Textual conclusions align with dashboard/gold metrics.
5. **Transparency:** Assumptions/limitations are stated when applicable.

**Implementation implication:** Treat numeric thresholds as go/no-go release criteria, and qualitative rubric as presentation and trustworthiness criteria for capstone review.

### Q10 Decision Memo *(2026-03-25)*
**Question:** If we cut 20–30% scope, which features are non-negotiable?

**Decision (accepted):**
Define a **Protected Core Scope** that must survive any scope cut before 2026-03-28:
1. **Running medallion pipeline (Bronze/Silver/Gold)** for core structured sources (**CDC PLACES + Census ACS**) with documented data quality checks.
2. **Gold-layer dashboard** that reliably answers the analytics demo questions (county burden + social determinant interpretation).
3. **Agentic workflow with citations** over the locked 5-collection CDC/WHO corpus, capable of answering intervention/evidence questions.
4. **Lean MVP evaluation gate** (15–25 gold questions + numeric pass thresholds from Q5/Q8/Q9).
5. **Cloud-running deployment + runbook** (manual/notebook deployment acceptable for MVP).

**First items to cut/defer if schedule compresses:**
- DAB packaging and environment promotion automation.
- Expanded eval depth beyond lean MVP metrics.
- Corpus expansion beyond the 5 locked collections.
- Extra UX polish/integration beyond required dashboard + working agent path.
- Any Graph RAG and streaming work (already Phase 2).

**Minimum “done” definition under constrained scope:**
- End-to-end pipeline runs in Databricks.
- Gold tables + dashboard are demo-ready and internally consistent.
- Agent answers the 3 required demo questions with verifiable citations at target quality bars.
- Evaluation results are captured and presentable.

**Implementation implication:** Execution planning now optimizes for protected-core completion first, with all stretch work explicitly deprioritized until after MVP stability is confirmed.

---

## Execution Progress Log *(2026-03-26)*

- **Timeline reset confirmed:** execution starts from Workstream A (Data Pipeline), all tasks at NS at start of day.
- **Agentic boundary clarified and locked in docs:**
  - Structured lane: Databricks Genie (text→SQL over Gold tables)
  - Document lane: Agent Bricks Knowledge Assistant (primary) with notebook/vector fallback
- **Pipeline scaffold progress:**
  - Verified existing `src/00_setup_env.py` (catalog/schema + Bronze table constants)
  - Verified existing `src/01_ingest_cdc_places.py` (CDC Bronze ingest scaffold with ingestion metadata)
  - Created `src/02_ingest_census_acs.py` (ACS Bronze ingest scaffold with ingestion metadata)
- **Current focus:** continue Workstream A by wiring real source paths/config and preparing Databricks run validation for A1/A2.
- **Config centralization completed:**
  - Created `src/config.py` for shared catalog/schema, Bronze table names, and source paths.
  - Updated `src/01_ingest_cdc_places.py` to import table/path settings from `config.py`.
  - Updated `src/02_ingest_census_acs.py` to import table/path settings from `config.py`.
- **Checklist tracking updated:** A1 and A2 moved from `NS` to `IP` in `docs/execution_checklist.md` pending Databricks run validation.
- **Checkpoint commit created:** `44e1960` — scaffolded `src/` pipeline files (`00_setup_env.py`, `01_ingest_cdc_places.py`, `02_ingest_census_acs.py`, `config.py`) and synced progress docs.
- **Next step:** run-validate A1/A2 in Databricks by uploading sample CDC/ACS raw files to configured DBFS paths and executing setup + ingestion scripts.
- **Runbook update completed:** expanded `README.md` with A1/A2 Databricks validation instructions (repo structure, run order, target bronze tables, and config override note).
- **Bronze validation script added:** created `src/03_validate_bronze.py` to verify both bronze tables exist, have non-zero rows, and contain non-null ingestion metadata (`ingestion_ts`, `source_path`, `source_system`).
- **Run order updated:** `README.md` now includes `src/03_validate_bronze.py` after CDC/ACS ingestion scripts.
- **CDC raw acquisition test passed (local):**
  - Added `src/00a_download_cdc_places_bulk.py` (bulk CSV snapshot downloader).
  - Verified source URL `https://data.cdc.gov/api/views/swc5-untb/rows.csv?accessType=DOWNLOAD`.
  - Download succeeded to `data/raw/cdc_places.csv` (~53 MB); schema preview confirms expected PLACES columns including `LocationID`, `MeasureId`, `Data_Value`.
- **ACS raw acquisition test passed (local):**
  - Added `src/00b_download_census_acs.py` (county-level ACS subject-table pull to CSV with `county_fips` enrichment).
  - Default test run succeeded to `data/raw/census_acs.csv` with 3,222 county rows.
  - Header/sample validation confirms expected fields: `NAME`, poverty %, median income, `state`, `county`, `county_fips`, `acs_year`, `source_url`.
- **Decisions confirmed (2026-03-27):**
  - Use **managed UC Volumes** for MVP (external volumes deferred).
  - Add **optional** Census API key support (CLI arg / env var / Databricks secret), but keep no-key path functional by default.
  - Treat execution as **Databricks-first**; no local fallback required for core workflow.
- **Cleanup patch progress:**
  - Tightened run-order docs to `00 -> 00a/00b -> 01 -> 02 -> 03`.
  - Added managed-vs-external volume guidance in `src/config.py` and `README.md`.
  - Refined A-workstream dependencies in `docs/execution_checklist.md` with explicit Bronze validation gate (`A2c`).
  - Ran syntax sanity check via `python -m py_compile` for pipeline scripts (pass).
- **Databricks runtime compatibility fix applied (2026-03-28):**
  - Updated `src/00a_download_cdc_places_bulk.py` and `src/00b_download_census_acs.py` argparse handling for Databricks REPL context (avoids `SystemExit: 2` from notebook-injected args).
  - Verified both download scripts run successfully after the fix.
- **A-workstream Bronze validation result (Databricks run):**
  - CDC Bronze table: `bootcamp_students.health_equity_capstone_jpmajesty2019.bronze_cdc_places` → **229,298 rows**, **0 null metadata rows**, PASS.
  - ACS Bronze table: `bootcamp_students.health_equity_capstone_jpmajesty2019.bronze_census_acs` → **3,222 rows**, **0 null metadata rows**, PASS.
  - Final output: **All Bronze validations passed.**
- **Execution status update:** A0, A1a, A1b, A2a, A2b, A2c are now completed in practice; next focus is A3 (Silver conformance).
- **Idempotency hardening (Bronze ingestion):**
  - Updated `src/01_ingest_cdc_places.py` and `src/02_ingest_census_acs.py` write mode from `append` to `overwrite`.
  - Rationale: rerunning ingestion should not duplicate Bronze rows for full-snapshot source loads.
- **Orchestration decision (2026-03-28):**
  - Use a **single Databricks Job (multi-task DAG)** for MVP orchestration.
  - Planned task flow: `00_setup_env` → (`00a_download_cdc`, `00b_download_acs`) → (`01_ingest_cdc`, `02_ingest_acs`) → `03_validate_bronze` → `04_conformed_silver`.
  - Rationale: lowest infrastructure risk, easiest retries/scheduling/alerts, and aligned to current notebook/script assets.
- **DLT status:**
  - Full DLT migration deferred for MVP timeline protection.
  - DLT-lite quality layer (expectation-like checks/quarantine equivalent) remains an optional post-core enhancement.
- **A3 Silver kickoff (2026-03-28):**
  - Added Silver table targets to `src/config.py`, including clean/quarantine outputs and `dq_monitoring_runs`.
  - Created `src/04_conformed_silver.py` with non-DLT conformance flow:
    - FIPS normalization and schema standardization for CDC/ACS.
    - Clean vs quarantine split via rule flags (`dq_failed_rules`).
    - Run-level DQ monitoring metrics appended to `dq_monitoring_runs`.
    - Idempotent writes (`overwrite`) for Silver clean/quarantine outputs.
  - Updated `docs/execution_checklist.md`: A3 moved to `IP`.
  - Syntax check passed for `src/04_conformed_silver.py` and `src/config.py`.
- **Databricks DAG Run 1 (all green) — 2026-03-28:**
  - `Conformed_silver_tables` output:
    - CDC clean: **229,298**
    - CDC quarantine: **0**
    - ACS clean: **3,222**
    - ACS quarantine: **0**
    - DQ monitoring rows appended: **2** (`dq_monitoring_runs`)
  - DAG timeline screenshot captured: `docs/dag_run_1_2026-03-28 115451.png`.
- **A4/A5 implementation checkpoint (2026-03-28):**
  - Added Gold targets to `src/config.py`: `gold_health_equity_stats` and `dq_gold_validation_summary`.
  - Created `src/05_build_gold.py`:
    - Joins `silver_health_outcomes_clean` + `silver_socioeconomic_clean` on `county_fips`.
    - Produces idempotent Gold snapshot (`overwrite`) with derived bands (`health_burden_band`, `poverty_band`).
  - Created `src/06_validate_gold.py`:
    - Validates Gold non-empty rowset and key metric non-null checks.
    - Cross-checks DIABETES average between Gold and Silver health outputs.
    - Appends run summary metrics to `dq_gold_validation_summary`.
  - Updated `docs/execution_checklist.md`: A4 and A5 moved to `IP`.
  - Syntax check passed for `src/05_build_gold.py`, `src/06_validate_gold.py`, and `src/config.py`.
- **Silver quarantine + Gold validation hardening (2026-03-28):**
  - Identified validation failure cause: **66 null `data_value`** rows in Gold inherited from Silver clean CDC output.
  - Root-cause diagnostics confirmed:
    - `silver_health_null_data_value = 66`
    - `cdc_quarantine_rows = 0` (pre-fix)
    - `gold_null_data_value = 66` (pre-fix)
  - Updated `src/04_conformed_silver.py`:
    - Added explicit boolean rule flags and `dq_any_failure` gating.
    - Ensured clean-table writes project only stable/base columns to avoid Delta schema mismatch.
    - Routed failed rows to quarantine outputs with `dq_failed_rules` and `dq_run_ts`.
  - Post-fix verification:
    - `silver_health_null_data_value = 0`
    - `cdc_quarantine_rows = 66`
    - `gold_null_data_value = 0`
  - Updated `src/06_validate_gold.py`:
    - Adjusted DIABETES average cross-check to compare Gold against **join-aligned Silver subset** (same county population) instead of full Silver.
- **Gold validation pass (post-fix):**
  - Gold row count: **229,006**
  - Rows with null key metrics: **0**
  - Gold DIABETES avg: **12.400982**
  - Silver DIABETES avg (join-aligned): **12.400982**
  - DIABETES avg diff: **0.0**
  - Validation summary appended to `dq_gold_validation_summary`: **1**
  - **Gold validation status: PASS**
- **Execution status update:** A4, A5, and A6 are complete in practice (full DAG run validated, evidence bundle captured).
- **Next active focus:** Track B (Document/RAG ingestion) starting with B1 (land 5 locked CDC/WHO sources into UC Volume).
- **Track B kickoff progress (2026-03-28):**
  - Added document-lane config in `src/config.py`:
    - `DOCS_SOURCE_PATH` for UC docs volume
    - `LOCKED_DOC_SOURCES` map for the 5 locked CDC/WHO sources
  - Updated `src/00_setup_env.py` to create managed docs volume: `cdc_who_docs`.
  - Created `src/07_ingest_cdc_who_docs.py` to download locked sources and write `locked_doc_manifest.csv` for landing tracking.
  - Syntax sanity check passed for `src/07_ingest_cdc_who_docs.py`, `src/00_setup_env.py`, and `src/config.py`.
  - Updated `docs/execution_checklist.md`: B1 moved from `NS` to `IP`.
- **Track B Run 1 (separate DAG) — B1 landing success:**
  - Docs volume path: `/Volumes/bootcamp_students/health_equity_capstone_jpmajesty2019/cdc_who_docs`
  - Manifest written: `/Volumes/bootcamp_students/health_equity_capstone_jpmajesty2019/cdc_who_docs/locked_doc_manifest.csv`
  - Sources attempted: **5**
  - Successful downloads: **5**
  - Failed downloads: **0**
- **Execution status update:** B1 is complete in practice; next focus is B2 (parse/chunk docs for Vector Search index preparation).
- **B2 kickoff progress (2026-03-28):**
  - Added `src/08_parse_and_chunk_docs.py` to parse landed docs and produce:
    - `raw_docs` (document-level parsed text)
    - `chunked_docs` (chunk-level records for vector indexing)
  - Added table constants in `src/config.py`: `RAW_DOCS_TABLE`, `CHUNKED_DOCS_TABLE`.
  - Script supports PDF parsing via `ai_parse_document` with fallback and HTML text extraction.
  - Idempotent write strategy: overwrite snapshots for both raw/chunked tables.
  - Updated `docs/execution_checklist.md`: B2 moved from `NS` to `IP`.
  - Local syntax check passed for `src/08_parse_and_chunk_docs.py`.


