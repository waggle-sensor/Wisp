#!/usr/bin/env python3
"""Stage 4 - Retrieval A/B: does the profile surface the right page for a real question?

v1's A/B graded by bag-of-words: it asked whether required keyword tokens appeared
*anywhere* in the control corpus. Its own limitations section flags the consequence -
"over-credits control when keywords already exist" - which is exactly what happened on
HERMES-0002 (1/7 targeted improvements, six of them lost to token overlap).

The failure is that a keyword can be present in a corpus and still be unfindable and
unactionable. An agent does not grep the whole tree; it retrieves a page and follows it.
So this harness grades the two things that actually matter, per task:

  1. RETRIEVAL  - rank the corpus files against the task query with BM25 and ask
                  whether the file that answers the question lands in the top-k.
                  Control and treatment are ranked over their own corpora, so
                  adding a file can *demote* an answer - regressions are visible.
  2. ACTIONABILITY - within the top-k retrieved text only (not the whole tree),
                  does the required symptom / cause / fix triad appear?

A task improves only if the answer becomes retrievable AND actionable. A keyword
scattered across three unrelated pages no longer counts as a pass.

BM25 is a deliberate choice: deterministic, dependency-free, no LLM, no GPU, and
re-runnable by a reviewer on a laptop with no network - the same reproducibility
constraint v1 set for itself.

Usage:
  python3 retrieval_eval.py --control <sage-waggle dir> --treatment <dir> \
      --tasks tasks.json --out results.json [--k 3]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

TOKEN = re.compile(r"[a-z0-9_.\-/]+")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


class BM25:
    """Standard Okapi BM25 over a set of documents."""

    def __init__(self, docs: dict[str, str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.names = list(docs)
        self.tf = [Counter(tokenize(docs[n])) for n in self.names]
        self.len = [sum(c.values()) for c in self.tf]
        self.avg = sum(self.len) / len(self.len) if self.len else 0.0
        df = Counter()
        for c in self.tf:
            df.update(c.keys())
        self.idf = {
            t: math.log(1 + (len(self.tf) - n + 0.5) / (n + 0.5)) for t, n in df.items()
        }

    def rank(self, query: str) -> list[tuple[str, float]]:
        q = tokenize(query)
        scores = []
        for i, name in enumerate(self.names):
            tf, dl = self.tf[i], self.len[i]
            s = 0.0
            for t in q:
                f = tf.get(t)
                if not f:
                    continue
                denom = f + self.k1 * (1 - self.b + self.b * dl / (self.avg or 1))
                s += self.idf.get(t, 0.0) * f * (self.k1 + 1) / denom
            scores.append((name, s))
        scores.sort(key=lambda x: -x[1])
        return scores


def load_corpus(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): p.read_text(encoding="utf-8", errors="replace")
        for p in sorted(root.rglob("*.md"))
    }


def phrase_present(text: str, phrase: str) -> bool:
    """Whitespace-normalised, case-insensitive substring match."""
    norm = lambda s: re.sub(r"\s+", " ", s.lower())
    return norm(phrase) in norm(text)


def grade(corpus: dict[str, str], task: dict, k: int) -> dict:
    ranked = BM25(corpus).rank(task["query"])
    topk = [n for n, s in ranked[:k] if s > 0]
    retrieved_text = "\n\n".join(corpus[n] for n in topk)

    # Retrieval: did any file we consider a valid answer make the cut?
    want = task.get("answer_files", [])
    retrieval_hit = bool(want) and any(
        any(w in n for n in topk) for w in want
    )

    # Actionability: graded ONLY over what was retrieved, not the whole tree.
    triad = task.get("must_contain_all", [])
    anyof = task.get("must_contain_any", [])
    have_all = [p for p in triad if phrase_present(retrieved_text, p)]
    have_any = [p for p in anyof if phrase_present(retrieved_text, p)]
    actionable = len(have_all) == len(triad) and (not anyof or bool(have_any))

    return {
        "top_k": topk,
        "top_scores": [round(s, 2) for _, s in ranked[:k]],
        "retrieval_hit": retrieval_hit,
        "actionable": actionable,
        "pass": bool(retrieval_hit and actionable),
        "missing_required": [p for p in triad if p not in have_all],
        "missing_any_of": anyof if (anyof and not have_any) else [],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", required=True)
    ap.add_argument("--treatment", required=True)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()

    control = load_corpus(Path(args.control))
    # Baseline provenance: grading against the wrong control silently inflates the
    # result, and nothing downstream can detect it. Record a fingerprint of the
    # control corpus in the output so a reviewer can confirm which baseline was used.
    control_fp = hashlib.sha256(
        "".join(f"{n}:{len(t)}" for n, t in sorted(control.items())).encode()
    ).hexdigest()[:16]
    treatment = load_corpus(Path(args.treatment))
    tasks = json.loads(Path(args.tasks).read_text())

    rows, summary = [], Counter()
    for t in tasks:
        c = grade(control, t, args.k)
        x = grade(treatment, t, args.k)
        if c["pass"] and not x["pass"]:
            verdict = "REGRESSION"
        elif x["pass"] and not c["pass"]:
            verdict = "IMPROVED"
        elif x["pass"]:
            verdict = "both_pass"
        else:
            verdict = "both_fail"
        summary[verdict] += 1
        rows.append({
            "id": t["id"], "candidate": t.get("candidate"), "split": t.get("split"),
            "query": t["query"], "verdict": verdict, "control": c, "treatment": x,
        })

    out = {
        "k": args.k,
        "control_fingerprint": control_fp,
        "control_root": str(Path(args.control)),
        "control_files": len(control),
        "treatment_files": len(treatment),
        "summary": dict(summary),
        "tasks": rows,
    }
    Path(args.out).write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"control={len(control)} files [fp {control_fp}]  "
          f"treatment={len(treatment)} files  k={args.k}")
    for v in ("IMPROVED", "REGRESSION", "both_pass", "both_fail"):
        print(f"  {v:11s} {summary[v]}")
    for r in rows:
        flag = {"IMPROVED": "+", "REGRESSION": "!", "both_pass": "=", "both_fail": "-"}[r["verdict"]]
        print(f"  [{flag}] {r['id']:38s} ctrl(ret={int(r['control']['retrieval_hit'])},"
              f"act={int(r['control']['actionable'])}) -> "
              f"treat(ret={int(r['treatment']['retrieval_hit'])},"
              f"act={int(r['treatment']['actionable'])})")


if __name__ == "__main__":
    main()
