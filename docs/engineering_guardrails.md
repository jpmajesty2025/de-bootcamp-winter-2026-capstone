# Engineering Guardrails (Default Operating Standard)

**Date:** 2026-03-29  
**POC:** Capstone Student + AdaL  
**TL;DR:** Default to idempotent, retry-safe, test-backed changes with minimal blast radius. If behavior is non-idempotent, it must be intentional, documented, and validated.

---

## 1) Idempotency-By-Default (All Pipeline/Backend Work)

### Required defaults
1. **Writes:** Use `overwrite`, `merge/upsert`, or deterministic replace semantics for scheduled batch jobs.  
2. **No blind append:** `append` only for intentional immutable event logs.  
3. **Deterministic keys:** Prefer business/hash keys over random UUIDs when run-to-run key stability matters.  
4. **Create-if-missing infra:** Endpoints/indexes/schemas/volumes must be safe on rerun (`already exists` handling).  
5. **Retry-safe external effects:** Notifications/webhooks/API side effects need idempotency keys or dedupe checks.

### Required per-task declaration
Every new task/script should state:
- **Input contract**
- **Output contract**
- **Write mode**
- **Idempotency behavior on rerun**
- **Expected retry behavior**

---

## 2) Senior Engineering Standards (General)

1. **Surgical changes only:** Modify only what the task requires; avoid unrelated refactors.
2. **Test before done:** Add/adjust tests for behavior changes and run validations.
3. **Fail loud, fail useful:** Clear errors with actionable context (what failed, where, why).
4. **No hidden coupling:** Centralize shared constants/config; avoid magic literals.
5. **Observability first:** Emit key row counts, statuses, and checkpoint logs for every stage.
6. **Rollback mindset:** Changes should be reversible and safe under partial failure.
7. **Security hygiene:** No secrets in code/logs/commits; principle of least privilege.
8. **Docs stay current:** Update checklist/session notes in the same change set as implementation.

---

## 3) Data Engineering-Specific Rules

1. **Schema discipline:** Explicit schemas for core tables; avoid accidental schema drift.
2. **DQ gates:** Null/key/range/ref checks with quarantine or documented exception path.
3. **Reconciliation checks:** Validate output aggregates against trusted upstream subsets.
4. **CDF + index prerequisites:** Ensure table properties and prerequisites before index build/sync.
5. **Runtime guardrails:** Add timeout/polling behavior for long async operations.

---

## 4) Backend/Software Engineering-Specific Rules

1. **Deterministic APIs:** Repeated requests with same intent should yield stable outcomes.
2. **Idempotent mutations:** PUT/PATCH/POST behaviors must define dedupe/upsert semantics.
3. **Contract clarity:** Versioned interfaces and explicit payload validation.
4. **Resilience:** Retries with bounded backoff for transient failures; no infinite retry loops.
5. **Feature flags over risky toggles:** Use safe rollout patterns for behavior changes.

---

## 5) Practical “Definition of Done” Gate

A change is not done unless:
- [ ] Idempotency behavior is explicit and validated
- [ ] Tests/validation queries pass
- [ ] Observability outputs are present
- [ ] Checklist/session notes updated
- [ ] Non-idempotent behavior (if any) is documented with rationale

---

## 6) Current Capstone Application (Track B)

- `raw_docs` and `chunked_docs` use full-refresh `overwrite` writes (rerun-safe).
- Vector endpoint/index setup uses rerun-safe create/check patterns.
- Known nuance: UUID-based IDs are not run-stable across full refreshes unless replaced by deterministic keys.

