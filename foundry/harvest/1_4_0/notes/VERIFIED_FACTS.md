# Pre-verified facts (checked by the orchestrator against primary sources)

Do NOT re-verify these; treat as settled. They are given so you can spend your
effort on merging rather than re-grepping.

## Baseline conflicts CONFIRMED (grep against ../summer-camp-2026/hermes-profile/)

1. `runtimeClassName` appears NOWHERE in the baseline sage-waggle tree.
   Worse, `references/runtime-packaging-patterns.md:106` asserts the opposite:
   "GPU available via NVIDIA device plugin". So the baseline steers away from the
   correct diagnosis.

2. `SKILL.md:660` says: "Always use `--runtime=nvidia` in documentation and scripts
   so commands work on both DGX Spark and Thor". `references/docker-build-deploy.md:73`
   has a section titled "Docker Runtime: --runtime=nvidia (Not --gpus all)".
   Both are wrong for the Podman/CDI camp node class.
   `nvidia.com/gpu` / CDI appears only in 2 unrelated files.

3. `sudo k3s ctr images import` is instructed in SIX places in SKILL.md
   (lines 655, 656, 657, 677, 680, 681), called "CRITICAL" and "required for local
   testing". The camp sudoers NOPASSWD allowlist (printed by `sudo -l` in-transcript)
   is: kubectl, docker, docker-compose, runplugin, pluginctl. `k3s` is NOT on it.

4. `references/reolink-http-snapshot.md:54` says: "Returns BGR numpy array, same
   format as Camera.snapshot().data" — contradicted by a student's empirical
   channel-mean measurement showing snapshot.data is RGB.

5. NOT in the baseline at all (confirmed absent): `YOLO_CONFIG_DIR`, `NOPASSWD`,
   git-lfs, `runtimeClassName`, pixi. x509 appears only re: control-plane
   diagnosis, not the node-local registry pull path.

## Sudo adjudication — SETTLED, use this exact framing

Two shards disagreed. Corpus resolution (counted by the orchestrator):
- 92 episodes across 8 students contain a SUCCESSFUL auto-approved sudo call.
- 9 episodes across 5 students contain `sudo: a terminal is required to read the password`.
- Every command near the TTY failures is a NON-allowlisted binary: k3s, apt-get,
  nvidia-ctk, systemctl, usermod, cat.

Correct merged claim (the conjunction): sudo works from the Hermes terminal ONLY for
the NOPASSWD-allowlisted binaries; any other binary needs a password, and with no TTY
and no askpass helper it fails with "a terminal is required" instead of prompting.
The agent should read that error as "this binary is not on the allowlist", NOT as
"sudo is unavailable", and switch to an allowlisted path (`sudo pluginctl build`,
`sudo kubectl apply`) or hand the command to the student.
The shard claiming "cannot run sudo at all" is OVER-GENERAL — do not promote as stated.

## skill_view truncation — DO NOT PROMOTE the truncation half

Shard 06_07 claimed `skill_view("sage-waggle")` returns ~121.8k chars truncated.
Checked against raw state.db (NOT episodes — my own corpus builder truncates tool
results, 1,155 elisions, so episodes cannot evidence a truncation claim):
- 50 skill_view results name sage-waggle; ALL 50 pass an explicit `file=`.
- ZERO request the whole skill body. No `truncated` flag is ever set.
- Payload sizes: min 1,061 / mean 12,152 / max 48,193 chars.
=> The truncation event is NOT observable in this corpus. Drop that half.

The PACKAGING half IS verified and should be promoted:
- The SKILL.md cap is 100,000 CHARACTERS (MAX_SKILL_CONTENT_CHARS), per
  skills/software-development/hermes-agent-skill-authoring/SKILL.md, which is
  byte-identical across all 13 brains carrying it and cites
  tools/skill_manager_tool.py::_validate_frontmatter. That page is NOT in the sage
  baseline (it ships with Hermes), and skill_manager_tool.py has not been read
  directly — strong secondary evidence, not verified in code.
- sage-waggle/SKILL.md is 114,441 chars in 1.1.0 and 115,072 chars in 1.2.0 (v1 GREW
  it by 631), i.e. +14.4% and +15.1% over the limit. Measure CHARS, not bytes: the
  file has multi-byte characters and byte counts (115,244 / 115,885 B) overstate the
  overage.
- A student MEMORY.md corroborates from the write side: "sage-waggle SKILL.md body
  is 114KB (limit 100KB) — can't be patched in place via skill_manage action=patch
  ... the in-place patch path aborts with a size error."
Release consequence: v2 must add NO new prose to SKILL.md; new material goes to
references/ only.

## HOME rewrite — independence measured corpus-wide

grep for the doubled path `profiles/sage/home` across all episodes:
- 9 of 11 students with transcripts
- 52 episodes
- 18 explicit `cd ... No such file or directory` failures
- affected paths include .ssh, .cache, .local, .venvs, .config, and project dirs
This is the highest-independence theme in the corpus. Lexical clustering wrongly
split it across C000, C032, C010, C033, C041, C019 — merge them.

## Corpus totals (for independence sanity checks)

14 brains, 11 with transcripts, 140 sessions, 9,077 messages, 4,424 tool calls,
13.5M chars, 237.8 logged agent-hours, 331 episodes, 19 agent-created skills (0 evals).
