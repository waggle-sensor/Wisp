#!/usr/bin/env python3
"""Stage 3b - Semantic consolidation of triage clusters into themes.

The lexical clustering in `corroborate.py` under-merges badly by design: it
produced 51 clusters from 53 hits and found only one corroborated theme, while
splitting the single highest-independence fact (the HOME rewrite) across six
clusters. Lexical overlap cannot see that "HOME is rewritten to <profile>/home"
and "$HOME resolves under the profile dir so ~ paths miss" are one fact.

The merge map below is therefore a *human/analyst* judgement, recorded explicitly
as data rather than hidden in prose, so a reviewer can audit or contest any single
grouping. Two rules governed it:

  merge   iff one profile page would satisfy every claim in the group
  split   whenever symptom or diagnostic differs, even under shared vocabulary

The sharpest application of the split rule: host-torch "hangs forever with no
error" (T05) and conda-forge torch "dies immediately at first kernel launch with
`no kernel image is available`" (T06) share every keyword and are different
failure classes with different diagnostics. Merging them would produce a page that
misdiagnoses both.

Independence is recomputed from episode-id attribution rather than the miners'
`student` fields, several of which were over-redacted into placeholders.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

CORPUS = Path("foundry/.work/corpus")

# theme_id: (title, [cluster ids], kind, placement, promote, baseline_conflict, rationale, notes)
THEMES = [
    ("T01", "Agent HOME is rewritten to the profile dir",
     ["C000", "C010", "C019"], "invariant", "SOUL", True,
     None,  # a gap, not a contradiction: nothing in the baseline states otherwise
     "Highest-independence finding in the corpus: 9/11 students, 52 episodes, 18 explicit "
     "cd failures. Symptom is a generic ENOENT indistinguishable from a typo, so no keyword "
     "list would surface it and no student wrote a skill about it.",
     "Corpus-wide grep supersedes cluster metadata for independence. Affected paths include "
     ".ssh, .cache, .local, .venvs, .config, not just project dirs. One episode shows a cold "
     "podman store under the profile HOME forcing a ~5.5GB base-image re-pull."),

    ("T02", "sudo works only for the NOPASSWD allowlist",
     ["C003", "C042"], "correction", "sage-waggle reference", True,
     "SKILL.md instructs `sudo k3s ctr images import` in six places (655,656,657,677,680,681), "
     "calling it CRITICAL and required for local testing. `k3s` is not on the sudoers allowlist.",
     "The baseline's canonical side-load procedure cannot execute on camp accounts. A "
     "bag-of-words A/B scores this topic as thoroughly covered - the keywords appear six times.",
     "MINER DISAGREEMENT, adjudicated against the corpus: one shard claimed a NOPASSWD "
     "allowlist, another claimed sudo never works. 92 episodes across 8 students contain a "
     "successful sudo call; 9 episodes across 5 students hit the TTY error, and every command "
     "near those failures is a non-allowlisted binary (k3s, apt-get, nvidia-ctk, systemctl, "
     "usermod, cat). The shipped claim is the conjunction. The 'sudo never works' phrasing is "
     "over-general and would teach the next agent to abandon a capability that works 92 times."),

    ("T03", "pluginctl pods get no GPU without runtimeClassName",
     ["C014", "C005", "C021", "C043"], "correction", "sage-waggle reference", True,
     "runtimeClassName appears nowhere in the baseline; runtime-packaging-patterns.md:106 "
     "asserts the opposite - 'GPU available via NVIDIA device plugin'.",
     "Measured cost in-episode: 27ms/frame GPU vs ~1.4s/frame CPU (~50x). Silent failure - the "
     "pod runs, publishes, and succeeds, just 50x slower with no error.",
     "Cross-shard: found independently by 4 miners. Includes the negative result that "
     "`--privileged` is NOT a substitute (a plausible workaround a student disproved live), "
     "and the one-command preflight: the node advertises no nvidia.com/gpu allocatable and "
     "the resource.gpu=true label is not evidence the GPU reaches pods."),

    ("T04", "Podman/CDI is the working GPU passthrough, not --runtime=nvidia",
     ["C009", "C044"], "correction", "sage-waggle reference", True,
     "SKILL.md:660 says 'Always use --runtime=nvidia'; docker-build-deploy.md:73 has a section "
     "titled 'Docker Runtime: --runtime=nvidia (Not --gpus all)'.",
     "Registering the nvidia runtime needs root edits to /etc/docker/daemon.json that camp "
     "accounts cannot make. CDI --device=nvidia.com/gpu=all is what actually works.",
     "Corroborated by three students' MEMORY.md independently of the transcripts. Flagged "
     "verify_on_canary: a miner warned the baseline may be drifting from fleet state and that "
     "a stale correction is worse than none."),

    ("T05", "Host PyPI torch hangs forever in D-state",
     ["C001", "C008"], "correction", "sage-waggle reference", True,
     "Corrects v1's own thor-host-cpu-dev-first.md, shipped in 1.2.0, which prescribes "
     "CUDA_VISIBLE_DEVICES= before importing torch as the fix.",
     "v1's fix is insufficient: `import torch` ITSELF enters uninterruptible D-state even with "
     "CUDA_VISIBLE_DEVICES=''. D-state processes survive SIGKILL. Working fix is a subprocess "
     "probe with timeout plus function-body-local torch imports.",
     "The sharpest argument for transcripts over artifacts: v1 mined a student artifact frozen "
     "2026-07-23; the same student superseded it on 07-24. Mining artifacts froze a claim the "
     "cohort had already outgrown."),

    ("T06", "conda-forge/pixi torch dies at first kernel launch",
     ["C002", "C015", "C028"], "failure_class", "sage-waggle reference", True,
     "docker-build-deploy.md covers sm_110 for container tags only, never host-side envs. "
     "'pixi' appears nowhere in the baseline.",
     "Distinct failure class from T05 with a different diagnostic: reports "
     "cuda.is_available()==True then fails FAST at the first kernel with 'no kernel image is "
     "available', rather than hanging. Students arrive with pixi research repos.",
     "Deliberately NOT merged with T05 despite near-total keyword overlap - opposite symptoms "
     "(fast failure vs infinite hang) need opposite diagnostics. Merging would misdiagnose both."),

    ("T07", "snapshot.data is RGB, not BGR",
     ["C020"], "correction", "sage-waggle reference", True,
     "reolink-http-snapshot.md:54 states 'Returns BGR numpy array, same format as "
     "Camera.snapshot().data'.",
     "Silent failure with no error message at all - the class most likely to reach production. "
     "A plugin following the baseline publishes colour-swapped images.",
     "Student measured it rather than asserting it: snapshot.data channel means "
     "[70.8, 116.5, 43.2] vs raw cv2 BGR [42.9, 115.9, 70.9] - channels 0 and 2 demonstrably "
     "swapped. Strongest evidence quality in the corpus."),

    ("T08", "pywaggle Camera() zero-arg raises a misleading TypeError",
     ["C016"], "failure_class", "sage-waggle reference", True,
     "camera-rtsp-patterns.md documents the device-routing chain but not that the zero-arg "
     "default crashes with a type error rather than a graceful device-open failure.",
     "Most common first-plugin stumble; the symptom points at `re`, not at the camera.",
     "Pairs naturally with T09 and the no-camera-attached invariant on one offline-dev page."),

    ("T09", "Off-node Plugin() raises from a background thread",
     ["C017", "C039"], "failure_class", "sage-waggle reference", True,
     "SKILL.md has a 'Local testing (no node required)' section but does not state that "
     "Plugin() raises from a daemon thread and therefore escapes try/except.",
     "The `try: Plugin() except: local-test mode` idiom is the natural thing to write and it "
     "silently does not work - students shipped it twice. Gate on a WAGGLE_* env var instead.",
     "Two miners found this independently via different symptoms (gaierror vs ImportError guard)."),

    ("T10", "Node-local registry x509 trust failure",
     ["C004", "C048"], "failure_class", "sage-waggle reference", True,
     "Baseline documents reachability and image-name causes for ImagePullBackOff; x509 appears "
     "only in control-plane diagnosis contexts, not the registry pull path.",
     "pluginctl build succeeds and hands back a ref that pluginctl run can never pull. Includes "
     "the confusing surface form: Pending -> '' -> 'pods not found' cycling.",
     None),

    ("T11", "sage-waggle SKILL.md exceeds its size limit",
     ["C023"], "invariant", "do-not-promote", False,
     "SKILL.md is 115,244 B (1.1.0) / 115,885 B (1.2.0) against a stated 100 KB limit.",
     "PARTIALLY VERIFIED. The packaging half is confirmed and v1 made it worse. The miner's "
     "read-path claim (skill_view returns 121.8k truncated) could NOT be reproduced: all 50 "
     "skill_view results in state.db pass an explicit file=, none loads the whole body, no "
     "truncated flag is ever set. Not promoted as a content page - it is a packaging action, "
     "recorded as a release constraint instead.",
     "Episodes are inadmissible evidence for a truncation claim because the corpus builder "
     "itself truncates tool results (1,155 elisions). Release constraint: v2 adds NO prose to "
     "SKILL.md; new material goes to references/ only."),

    ("T12", "Camp blades ship with no camera and are SGT-scoped",
     ["C013", "C026", "C036", "C022"], "invariant", "sage-waggle reference", True,
     "auth-api-manifests-and-nodes.md presents the manifest endpoint as the camp default and "
     "never says it returns empty for SGT-project nodes.",
     "All baseline camera guidance assumes an attached Reolink. Confirmed independently on "
     "three nodes. Includes the curl -L 301-empty-body false negative and project-scoped "
     "portal visibility (a healthy node in another project reads as an outage).",
     None),

    ("T13", "ENTRYPOINT shell form swallows pluginctl args",
     ["C025"], "failure_class", "sage-waggle reference", True,
     None,
     "Plugin keeps argparse defaults although kubectl describe proves the args reached the pod "
     "spec - reads as a pluginctl bug, is a Dockerfile bug. Exec-form ENTRYPOINT is the fix.",
     "Complements v1's HERMES-0002 pixi ENTRYPOINT finding; same root cause family."),

    ("T14", "pluginctl build tag derives from directory name",
     ["C012", "C035"], "failure_class", "sage-waggle reference", True,
     None,
     "An uppercase letter in the repo directory name fails with 'repository name must be "
     "lowercase' naming a tag the user never typed, so it misreads as an auth problem. Also "
     "covers the stale-pod --name collision whose giant pod-spec diff is unreadable.",
     None),

    ("T15", "Off-node upload path needs WAGGLE_PLUGIN_UPLOAD_PATH",
     ["C032"], "procedure", "sage-waggle reference", True,
     None,
     "plugin.upload_file() on a dev host dies with PermissionError on /run/waggle, which is "
     "root-owned and absent off-node. This is exactly where the official tutorial wall is.",
     None),

    ("T16", "vLLM on Thor: unified-memory profiling and TRITON_ATTN hang",
     ["C029", "C045", "C046"], "failure_class", "new skill", True,
     None,
     "Two reproducible vLLM failure classes plus the jetson-ai-lab extra-index-url rule. Whole "
     "cluster comes from an agent-created skill (sage-thor-vlm-serving, 11.5 KB) that v1 never "
     "mined. Came from the LOW-friction batches - would have been lost to a friction gate.",
     "Candidate for a domain pack rather than sage-waggle, per v1's placement ladder."),

    ("T17", "Serial peripherals: no dialout group, ttyUSB enumeration",
     ["C034", "C038"], "invariant", "sage-waggle reference", True,
     None,
     "Accounts are in video/render/develop but NOT dialout, so /dev/ttyUSB0 is unreadable. A "
     "device documented as ttyACM0 can enumerate as ttyUSB0 via ftdi_sio. Blocks GPS/LoRa/"
     "Meshtastic work; serial peripherals are an entirely uncovered category.",
     None),

    ("T18", "@once is not a supported cron pattern",
     ["C007"], "failure_class", "sage-waggle reference", True,
     None,
     "SES reports Running forever while the on-node scheduler rejects the rule every ~10s and "
     "never creates a pod. A third 'Running but silent' bucket beyond the two the baseline has. "
     "Ground-truth-confirmed from scheduler logs.",
     None),

    ("T19", "ECR: sage.yaml source fields and S3 quota",
     ["C033", "C041", "C049"], "failure_class", "sage-waggle reference", True,
     None,
     "Two ECR failures the baseline's otherwise thorough catalogue misses: Create-App rejects a "
     "repo whose sage.yaml lacks source.url/source.branch (homepage is display-only), and "
     "publish can fail with a registry-side S3 QuotaExceeded that is not a build or auth error.",
     "Medium confidence: the source.url causal link was inferred from the catalog, not "
     "confirmed by a successful re-registration."),

    ("T20", "Deploy verification: trust the pod image, not the claim",
     ["C040"], "procedure", "sage-waggle reference", True,
     None,
     "Check the SES pod's actual image: and independently GET the ECR catalog entry. Caught a "
     "pod quietly running :0.1.0 while the user believed :0.1.2 - and :0.1.2 404s in ECR.",
     None),

    # ---- not promoted ----
    ("T21", "Fleet-wide web tool outage",
     ["C011", "C024"], "procedure", "do-not-promote", False,
     "Contradicts 'fetch the live URL' guidance in three baseline index files.",
     "Transient provisioning state, not platform knowledge. Shaped 26 of 331 episodes and one "
     "blocked agent filled ECR metadata with unrelated stock photos rather than reporting the "
     "tool as unavailable - a real agent-integrity failure mode worth reporting in the paper. "
     "But a profile page describing a missing pip package is stale the moment the fleet is "
     "reprovisioned.",
     "Kept as a cohort/operational finding for the write-up, excluded from uptake."),

    ("T22", "NVIDIA-hosted provider aborts on vision tool results",
     ["C050"], "failure_class", "do-not-promote", False,
     None,
     "Agent provider-layer bug, outside the Sage domain and outside what a profile page can "
     "fix. Worth an upstream report, not a skill.",
     "Invisible to keyword mining - notable as a category the method reached."),

    ("T23", "Camera audio capability must be probed",
     ["C027", "C031"], "procedure", "sage-waggle reference", False,
     None,
     "Real and useful, but the camp camera set is site-specific hardware that will differ next "
     "year. Hold for instructor review rather than shipping fleet-wide guidance.",
     "Includes the rtsp://10.107.0.1 redirector finding, which is camp-network-specific."),

    ("T24", "birdnet 0.2.16 array API",
     ["C018"], "correction", "archive", False,
     None,
     "Library-version-specific API detail verified by reading installed source. Will be wrong "
     "at the next birdnet release; belongs in a project pack, not the shared baseline.",
     None),

    ("T25", "git-lfs absent on camp nodes",
     ["C030"], "invariant", "sage-waggle reference", False,
     None,
     "True and occasionally costly (LFS files bake into images as 130-byte pointers), but "
     "single-episode evidence and arguably general Git knowledge. Hold.",
     None),

    ("T26", "25.08-py3 ships no cv2 (dead Dockerfile line)",
     ["C037"], "correction", "sage-waggle reference", False,
     None,
     "Plausible and cheap to fix, but rests on one student's observation of a widely-copied "
     "Dockerfile purge line. Needs a container check before shipping a correction.",
     "Exactly the 'stale correction is worse than none' risk a miner warned about."),

    ("T27", "No node-to-node primitive in Sage",
     ["C047"], "invariant", "sage-waggle reference", False,
     None,
     "Architecturally important capability boundary, but stated as a negative that is hard to "
     "verify from one episode. Flag for instructor confirmation.",
     None),

    ("T28", "TFLite/YAMNet-on-Thor toolchain",
     ["C006"], "procedure", "sage-waggle reference", False,
     None,
     "Four verified gates (dead tfhub, kagglehub slug, TF 2.21 dropping tensorflow.lite, fixed "
     "input shape). Genuinely novel - baseline audio coverage is BirdNET-only. Held only "
     "because it is a long procedure needing its own page and a live re-run to confirm.",
     "Strongest not-promoted candidate; recommend for the next pass."),
]


def main() -> None:
    clusters = {c["id"]: c for c in json.loads((CORPUS / "clusters_for_review.json").read_text())}
    seen: set[str] = set()
    themes, not_promoted = [], []

    for tid, title, cids, kind, placement, promote, conflict, rationale, notes in THEMES:
        missing = [c for c in cids if c not in clusters]
        if missing:
            raise SystemExit(f"{tid}: unknown clusters {missing}")
        seen.update(cids)
        group = [clusters[c] for c in cids]
        students = sorted({s for g in group for s in g.get("real_students", [])})
        shards = sorted({s for g in group for s in g["shards"]})
        episodes = sorted({e for g in group for e in g["episodes"]})
        conf = ("high" if any(g["conf"] == "high" for g in group)
                else "medium" if any(g["conf"] == "medium" for g in group) else "low")

        t = {
            "theme_id": tid,
            "title": title,
            "merged_from": cids,
            "canonical_claim": group[0]["claim"],
            "alt_phrasings": [g["claim"] for g in group[1:]],
            "kind": kind,
            "students": students,
            "independence": len(students),
            "shards": shards,
            "cross_shard": len(shards) > 1,
            "episodes": episodes,
            "confidence": conf,
            "generality": group[0]["gen"],
            "is_correction_of_baseline": conflict is not None,
            "baseline_conflict": conflict,
            "suggested_placement": placement,
            "promote": promote,
            "promote_rationale": rationale,
            "notes": notes,
        }
        # T01's independence is corpus-wide (grep), not cluster-derived
        if tid == "T01":
            t["independence"] = 9
            t["independence_source"] = "corpus-wide grep: 9/11 students, 52 episodes"
        themes.append(t)
        if not promote:
            not_promoted.append({"theme_id": tid, "title": title, "reason": rationale})

    unassigned = sorted(set(clusters) - seen)
    out = {
        "themes": themes,
        "not_promoted": not_promoted,
        "unassigned_clusters": unassigned,
        "stats": {
            "clusters_in": len(clusters),
            "themes_out": len(themes),
            "promoted": sum(1 for t in themes if t["promote"]),
            "corrections": sum(1 for t in themes if t["is_correction_of_baseline"]),
            "cross_shard": sum(1 for t in themes if t["cross_shard"]),
        },
    }
    (CORPUS / "consolidated.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    s = out["stats"]
    print(f"clusters {s['clusters_in']} -> themes {s['themes_out']}  "
          f"promoted {s['promoted']}  corrections {s['corrections']}  cross-shard {s['cross_shard']}")
    if unassigned:
        print(f"UNASSIGNED (not in any theme): {unassigned}")
    for t in sorted(themes, key=lambda t: -t["independence"]):
        if t["promote"]:
            flag = "!" if t["is_correction_of_baseline"] else " "
            print(f" {flag} {t['theme_id']} n={t['independence']} "
                  f"{'x-shard' if t['cross_shard'] else '       '} {t['title']}")


if __name__ == "__main__":
    main()
