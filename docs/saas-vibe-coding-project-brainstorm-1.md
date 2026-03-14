# SaaS Vibe Coding Project Brainstorm — Session 1
**Date:** 2026-02-22

---

## Assignment Context

**Theme:** Build a Real SaaS Product in 48 Hours

**Tech Requirements:**
- Framework: Next.js (v14+, App Router preferred)
- Styling: Any (Tailwind CSS, Shadcn/ui, etc.)
- Backend: Next.js API Routes or Server Actions
- Database: Optional but encouraged (Supabase, Neon, etc.)
- Auth: Optional but encouraged (NextAuth, Clerk, etc.)
- Deployment: Required — must be publicly accessible (Vercel recommended)

**Submission Requirements:**
1. Landing page screenshot (product name, tagline, value proposition, visible CTA)
2. Next.js Routes Export
3. Submission form (product name, description, team, live URL, GitHub URL, 2–3 sentence problem description)

**What Makes a Great Submission:**
- Clear Value Proposition
- Working Core Feature (end-to-end)
- Clean UI/UX
- Logical Route Structure
- Live Deployment

---

## Source Material

Ideas drawn from the Winter 2026 DE Bootcamp capstone brainstorm (`winter_2026_de_bootcamp_capstone_brainstorm_1.md`), which explored a public health data domain using Databricks, Kafka, Delta Lake, dbt, and Snowflake.

---

## Analysis: Can DE Bootcamp Ideas Become a Vibe Coding SaaS?

### Why the Ideas Don't Transfer Directly

The DE brainstorm is built around enterprise data engineering infrastructure (Databricks, Kafka, Delta Lake, dbt, Snowflake) with a pipeline-first architecture and multi-week scope. The Vibe Coding project needs a Next.js web product with a working core feature deployable in 48 hours.

### Idea Viability Summary

| Idea | Viability | Notes |
|---|---|---|
| Idea 1 — Public Health Intelligence Platform | ❌ | Way too complex, wrong stack |
| Idea 2 — Chronic Disease & Social Determinants Correlator | ⚠️ | Dashboard/viz tool, not SaaS-feeling |
| Idea 3 — Vaccine Coverage vs. Disease Outbreak Tracker | ⚠️ | Data sourcing is the hard part |
| **Idea 4 — Health Document RAG Pipeline** | **✅** | **Cleanest SaaS fit** |

---

## Recommended Direction: Health Document RAG SaaS

### Concept
*"Ask any question about CDC/WHO clinical guidelines in plain English — instant, cited answers for healthcare workers and researchers."*

### How DE Idea 4 Maps to a Next.js SaaS

| DE Bootcamp Version | Vibe Coding SaaS Version |
|---|---|
| Spark + Cortex `AI_PARSE_DOCUMENT` | Pre-process CDC/WHO docs offline |
| `AI_EMBED` on Snowflake | Supabase `pgvector` or OpenAI embeddings |
| Databricks AI Agent | Next.js API route → OpenAI |
| Airflow nightly ingestion | Static/seeded vector DB at launch |

### 48-Hour MVP Architecture

```
Landing page (Next.js)
  ↓
Sign up / Login (Clerk — ~30 min setup)
  ↓
Dashboard: Chat interface
  ↓
API Route: query → OpenAI embeddings → Supabase pgvector → GPT-4o answer + source citations
  ↓
Deploy: Vercel (one command)
```

Pre-seed with ~20–50 key CDC/WHO documents. That's the entire backend.

---

## Open Questions / Next Steps
- [ ] Confirm target user persona (healthcare worker, researcher, general public?)
- [ ] Decide on document corpus (CDC only? WHO? Both? Specific topics?)
- [ ] Define exact route structure for submission
- [ ] Scaffold Next.js project and confirm tech stack
