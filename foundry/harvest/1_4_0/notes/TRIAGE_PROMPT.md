# Foundry v2 — Stage 2 triage brief

You are triaging student→agent conversation episodes from the 2026 SAGE summer camp.
Students used a shared Hermes agent profile ("sage") on NVIDIA Thor edge nodes to build
Waggle/Sage plugins. We are mining their transcripts for knowledge that should be
promoted into the shared baseline profile so next year's agent starts smarter.

## What counts as a HIT

A hit is a **transferable, checkable claim about the platform or toolchain** that the
baseline profile does not already state. Good shapes:

- A **failure class**: symptom → root cause → fix, where the symptom is misleading
  (looks like X, actually Y).
- An **invariant / preflight**: a check that would have prevented a long debugging arc.
- A **correction**: the baseline says something that is now stale or wrong.
- A **procedure**: an ordering or flag that is non-obvious and repeatedly needed.

## What is NOT a hit

- Project-specific business logic (one student's bat counter thresholds).
- Generic Linux/Python/Docker knowledge any model already has.
- Anything already covered by the baseline map (see below) — check before claiming novelty.
- Student mistakes with no generalisable lesson.
- Agent harness noise (a tool call the agent malformed and then fixed).

## IMPORTANT — judge semantically, not by keyword

Do not filter by topic. An episode about an unexpected subject (networking, GPS,
audio, k3s, the agent's own tooling) is just as eligible as one about the topics the
baseline already covers. The prior mining pass used a fixed keyword list and missed
whole categories; your job is to catch what a keyword list cannot.

Novelty means: *after reading the baseline coverage map, would the baseline agent
have gotten this right?* If a baseline file names the topic but the specific
symptom/cause/fix is absent, that is still novel — say so and name the file.

## Inputs

- Baseline coverage map: `.work/corpus/baseline_map.md` (read this FIRST, skim all of it)
- Your digest batches: listed in your task
- Full episode text if you need it: `.work/corpus/episodes/<episode_id>.md`

Digests are lossy. When a digest looks promising but ambiguous, **read the full
episode** before deciding. When a digest is clearly not a hit, do not read the full text.

## Output

Write JSON to the output path given in your task. Schema:

```json
{
  "batches": ["batch_00"],
  "episodes_reviewed": 28,
  "full_reads": ["episode_id", "..."],
  "hits": [
    {
      "episode_id": "...",
      "student": "...",
      "claim": "One sentence, falsifiable, de-identified. Symptom → cause → fix.",
      "kind": "failure_class | invariant | correction | procedure",
      "evidence_quote": "<=300 chars verbatim from the episode showing the symptom or the fix",
      "why_novel": "What the baseline map does/doesn't say; name the file you checked.",
      "baseline_files_checked": ["skills/sage-waggle/references/....md"],
      "confidence": "high | medium | low",
      "generality": "platform | toolchain | project-specific",
      "suggested_placement": "sage-waggle reference | SOUL | new skill | archive"
    }
  ],
  "near_misses": [
    {"episode_id": "...", "note": "why it almost qualified"}
  ]
}
```

Rules:
- **De-identify**: no usernames, no `/home/<name>/` paths, no hostnames, no tokens,
  no emails. Write `/home/<user>/`, `<node>`, `[REDACTED]`.
- Quote evidence verbatim (after de-identification) — do not paraphrase into the quote field.
- Be strict. A precise 3-hit report beats a padded 15-hit one. Low-confidence guesses
  belong in `near_misses`, not `hits`.
- Report what you actually read. If a batch was unreadable, say so in the JSON.
