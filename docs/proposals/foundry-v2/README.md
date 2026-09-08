# Foundry v2 — RELEASED in profile 1.3.0

The ten reference pages proposed by the second mining pass (Hermes Learning Foundry
v2) are **merged into `skills/sage-waggle/references/` on this branch** and indexed in
`SKILL.md`. `distribution.yaml` is bumped to **1.3.0**.

This file remains as a pointer; the pages themselves now live in the profile.

## Release composition

**1.3.0 = 1.2.0 + these ten.** This branch is cut from
`hermes-profile-1.2.0-foundry-uptake`, **not** from `main`.

That matters. v1's release was never merged to `main`, so `main`'s profile is still
1.1.0 (109 `sage-waggle` files). Building 1.3.0 on `main` would have shipped v2's ten
pages while silently dropping v1's three (`thor-host-cpu-dev-first.md`,
`plugin-verification-invariants.md`, `ml-plugin-patterns-thor-base-image.md`), its
`evals.json`, and its `ml-plugin-patterns.md` edits — and it would have broken
`thor-host-torch-hang.md`, which explicitly supersedes `thor-host-cpu-dev-first.md`
and links to it.

**`main` is still 1.1.0.** Merging v1's release to `main` is a separate, still-open
decision.

## The ten pages

| Page | What it fixes |
| --- | --- |
| `agent-shell-environment.md` | agent `HOME` is rewritten into the profile dir; `~` paths resolve nowhere |
| `sudo-allowlist-and-image-import.md` | `sudo k3s ctr images import` cannot run; `k3s` is off the allowlist and there is no TTY |
| `pluginctl-gpu-runtimeclass.md` | pluginctl emits no `runtimeClassName`, so its pods get no GPU |
| `podman-cdi-gpu-passthrough.md` | CDI works; `--runtime=nvidia` errors; `--gpus all` exits 0 injecting nothing |
| `thor-host-torch-hang.md` | `import torch` D-states at module level; SIGKILL will not clear it |
| `thor-conda-forge-no-sm110.md` | conda-forge/pixi torch has no sm_110 kernels |
| `pywaggle-snapshot-channel-order.md` | `snapshot.data` is RGB, not BGR — silent colour swap |
| `pywaggle-camera-offline-dev.md` | misleading zero-arg `Camera()` TypeError; no camera attached |
| `pywaggle-offnode-local-testing.md` | off-node `Plugin()` fails from a background thread |
| `node-registry-x509-trust.md` | registry x509 trust as an ImagePullBackOff cause |

Nine of the ten **correct** shipped guidance rather than adding to it. One
(`thor-host-torch-hang.md`) corrects a page v1 itself shipped.

## Verification of the released tree

Re-run after merge, against the **actual released tree** rather than the staged copy
(so the `SKILL.md` index edit is included):

| k | IMPROVED | REGRESSION | guards hold |
| ---: | ---: | ---: | ---: |
| 1 | 10 | 0 | 5/5 |
| 2 | 10 | 0 | 5/5 |
| 3 | 10 | 0 | 5/5 |
| 5 | 10 | 0 | 5/5 |

Control = 1.2.0, 112 files, fingerprint `971479c99bb63355`. Treatment = 122 files.
Raw: `evals/ab_released_130.json`, `evals/sensitivity_k_released_130.json` in the logs
repo. All cross-references in the merged pages resolve.

## Known issues carried into 1.3.0

- **`SKILL.md` is 117,644 chars against a 100,000-char limit** (17.6% over). It was
  already 14.4% over at 1.1.0, v1 grew it by 631 chars, and indexing these ten added
  2,572 more. The limit is `MAX_SKILL_CONTENT_CHARS`, documented in
  `skills/software-development/hermes-agent-skill-authoring/SKILL.md`; it is a
  **character** cap, not bytes. The in-place `skill_manage action=patch` path aborts
  with a size error, so this file must be split. Tracked as theme T11, deliberately
  not fixed in this release because splitting it needs its own A/B.
- **Six of ten pages are hardware-verified**; four rest on transcript evidence alone.
  The canary corrected one of the six it tested, so treat the four as less certain.
  See `notes/03-canary.md` in the logs repo.

Method, evidence and full results: `2026-summer-camp-sage-agent-logs`, branch
`hermes-foundry-v2-transcript-mining`, under `hermes/foundry-v2/` — start with
`reports/paper.md`.
