# HV2-0004 — A/B results

Retrieval@k (BM25) + actionability within retrieved text. Control = profile 1.2.0 sage-waggle (112 md). Treatment = control + proposed (122 md).

| task | control ret/act | treatment ret/act | verdict |
| --- | --- | --- | --- |
| `V2-T04-cdi-gpu-flag` | 0/0 | 1/1 | **IMPROVED** |

Stable across k in {1,2,3,5}: 10/10 targeted improved, 0 regressions (see `../../evals/sensitivity_k.json`).

**Not validated here:** live on-node behaviour. These graders measure retrievability and actionability of text, not hardware outcomes. Instructor canary required before fleet-wide trust — see REVIEW.md.