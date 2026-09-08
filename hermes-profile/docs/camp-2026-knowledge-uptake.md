# Camp 2026 knowledge uptake (Hermes Learning Foundry pilot)

Distribution **1.1.0 → 1.2.0**. Validated deltas only — no student graphs, sessions, or MEMORY.md merges.

| Candidate | Placement | Baseline path | Source (de-identified) |
| --- | --- | --- | --- |
| HERMES-0001 | Core sage-waggle patch + SOUL bullet | `references/thor-host-cpu-dev-first.md` | Agent-created Thor ML skills (one contributor; instructor canary still required for hardware retest) |
| HERMES-0002 | Core sage-waggle patch + SOUL bullet | `references/plugin-verification-invariants.md` | Two contributors: batch-to-edge / bat-count invariants + multimodal verification |
| HERMES-0003 | Core doc patch | `references/ml-plugin-patterns.md` + `ml-plugin-patterns-thor-base-image.md` | Internal contradiction vs SKILL.md/docker-build-deploy; student skills used 25.08 |
| HERMES-0004 | Hold | (eval only) | Graphify-first already in AGENTS.md |

**Held / not shipped:** `agent-bus-onboarding` (project pack), BioCLIP/BISONN project skill as-is, SageAir training skill, bat-counting plugin as-is, personal MEMORY/USER, raw Graphify graphs.

Evals: `skills/sage-waggle/evals/evals.json`. Fixture A/B: `2026-summer-camp-sage-agent-logs/hermes/evals/ab_results.json`.

After `hermes profile update sage`, refresh Graphify on the **installed** profile:

```text
/graphify ~/.hermes/profiles/sage --update
```

Packaged `graphify-baseline.tar.gz` is unchanged until an instructor NIM extract (`scripts/update_hermes_profile_graphify.sh --pack-baseline`).
