# HV2-0004 — human review

- [ ] Claim is accurate and de-identified
- [ ] Placement is right (reference vs SOUL vs new skill)
- [ ] Does not duplicate existing baseline content
- [ ] Cross-links name neighbouring pages without importing their error strings
      (see findings log F12 — quoting a neighbour's symptom text distorts retrieval)
- [ ] **Correction**: confirm the baseline text it contradicts is genuinely wrong on current fleet state

**Reviewer:** _unassigned_
**Decision:** _pending_

## Verification status

Deterministic retrieval A/B only. No live Thor canary was run in this pass.
**This candidate contradicts shipped guidance** — a stale correction is worse than none. Verify on a current node before merging.
