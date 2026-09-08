# Foundry — scrape brains, improve Wisp

Instructor loop for turning participant Hermes profiles from Sage events into better shared `sage`
docs. **Not shipped to agents:** `foundry/` is omitted from
`distribution.yaml` `distribution_owned`, so `hermes profile install` / `update`
do not copy it. Graphify ignore files list `foundry/` so clone-side extracts
do not ingest the corpus.

```text
foundry/
  tools/                 reusable miners + harvest scripts
  harvest/1_4_0/         frozen 2026 → profile 1.4.0 campaign
  .work/                 gitignored extracts + intermediate corpus
```

## The loop

1. **Harvest / clean** brains into `foundry/harvest/<id>/brains/` using node ids
   only (`node-H01D/node-H01D_public_sage.tar.gz`). Shared blades get a suffix
   (`node-H037a`, `node-H037b`). Scripts: `tools/clean_public_archive.sh`,
   `tools/redact_secrets.py`.
2. **Unpack** to `foundry/.work/brains/<node>/sage/` (gitignored).
3. **Mine** with `foundry/tools/` (`build_corpus.py`, `make_digests.py`,
   `baseline_index.py --profile .`, `corroborate.py`, …). Control and treatment
   trees are **this repo root** (the live profile).
4. **Grade** with `retrieval_eval.py`. Promote accepted pages into
   `skills/sage-waggle/references/` (and re-run the Graphify baseline scripts
   under `scripts/` if the shipped graph should change).

Tool usage: [`tools/SKILL.md`](tools/SKILL.md). Next-pass backlog: [`NEXT.md`](NEXT.md).

## Unpack the 1.4.0 brains

```bash
# From the Wisp repo root
mkdir -p foundry/.work/brains
for d in foundry/harvest/1_4_0/brains/node-*/; do
  n=$(basename "$d")
  mkdir -p "foundry/.work/brains/$n"
  tar -xzf "$d/${n}_public_sage.tar.gz" -C "foundry/.work/brains/$n"
done
```

## 1.4.0 campaign

The pages this pass proposed are already in profile **1.4.0**. Evidence, paper,
evals, and frozen merge maps: [`harvest/1_4_0/`](harvest/1_4_0/README.md).
Do not merge those candidates again.

A later scrape should be a new directory `foundry/harvest/<id>/` using the same
tools, not an edit of `1_4_0`.
