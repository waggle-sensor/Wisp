# Plugin verification invariants (edge ML / Sage)

Reusable checks distilled from camp plugin work. Use after code changes and **before claiming success**. These are procedures, not project defaults.

## 1. Three-way config consistency

The same default must appear in **all three** (they drift independently):

1. CLI / argparse defaults in `app.py` (what `pluginctl run` executes)
2. `sage.yaml` inputs (what SES/ECR scheduling injects)
3. README / overview tables (what humans copy)

After changing a default: grep the old value across all three. Run `python3 app.py --help` and diff against `sage.yaml` and docs.

## 2. Dockerfile COPY matches imports

A image that only `COPY app.py` but not sibling modules (`thermal.py`, `audio.py`, `__init__.py`, vendored trackers) **builds** and then **crashes on first import**. Verify every `import` has a COPY (or is a pip dep). Prefer `python3 -c "import app"` inside the image.

Pixi-based images: `ENTRYPOINT` must use the **pixi env interpreter**, not distro `python`. Distro python cannot see pixi packages → exit in ~1s (`startedAt` ≈ `finishedAt`) before your logs. Forms that work:

```dockerfile
ENTRYPOINT ["/root/.pixi/envs/default/bin/python", "plugin/app.py"]
# or
ENTRYPOINT ["bash", "-lc", "exec pixi run python plugin/app.py"]
```

## 3. Escalation threshold ≠ reporting threshold

If fusion/alert logic **filters detections by the publish/report confidence first**, sub-threshold signals never reach escalation (e.g. weak smoke + thermal → fire). Keep a **lower** escalation candidate list independent of the report gate.

Do not encode fragile `and`/`or` chains with `None`; compute explicit booleans.

Clamp unbounded modality scores (e.g. crest-factor ratios) to `[0, 1]` before `max()` into a published score.

## 4. Preprocess / weight match (“silent zero detections”)

Plugin **runs**, pod **Succeeded**, publishes — but **0 boxes / 0 events on every frame**.

Before blaming CUDA or pluginctl:

1. Confirm baked weights are the intended checkpoint (`md5` vs source; Dockerfile `COPY` comments).
2. Confirm **runtime preprocessing matches training** (background subtraction on/off, amplification, class-id filter, ROI normalized vs pixels). A model trained on debackgrounded frames will look “dead” on raw frames.
3. Sweep candidate weights on a **fixture frame** at low conf, **with and without** the plugin preprocess. Wrong weights: max conf stays tiny on both. Preprocess mismatch: dead on raw, alive after preprocess.

Do not declare “weights are wrong” from a raw-frame-only sweep.

Bake weights at an explicit path; do not rely on runtime ultralytics/HF download on firewalled nodes (`ml-plugin-patterns.md`).

## 5. Outcome state, not a plausible log

**Fail** if you only have: SES `Running`, a tidy stdout line, or `pluginctl` “started”.

**Require at least one** of:

- `kubectl get pods` (or `pluginctl ps`) shows the expected container **Running or Completed**, not CrashLoop / empty namespace
- A published measurement / file / expected event count on a **known fixture**
- Import/compile of the container entrypoint succeeded **and** a bounded smoke run processed N frames

SES “Running” means the **job spec was accepted**, not that WES created a live pod (`job-scheduling-and-liveness.md`, `scheduling-continuous-vs-oneshot-and-gpu-contention.md`).

## 6. Class differentiation (X vs confusable Y)

Do not answer “can it tell wildfire from campfire?” from a single confidence. Run the **project model** on real positives, confusable negatives, and true negatives; route through the project’s own verdict function. If both classes alarm at similar confidence, say **no** and show the table. Fusion that only **escalates** cannot invent a missing class.

## Checklist (copy into a PR)

- [ ] argparse / sage.yaml / docs defaults match (`--help` diff)
- [ ] Dockerfile COPY + ENTRYPOINT cover imports (pixi python if pixi)
- [ ] Escalation uses unfiltered candidates; scores clamped
- [ ] Weights provenance + preprocess match; fixture not all-zeros for the right checkpoint
- [ ] Outcome verified (pod/events/fixture), not SES-only
- [ ] If asked “X vs Y”, category table exists
