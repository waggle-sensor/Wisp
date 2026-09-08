# Thor GPU plugins: do not use pytorch:24.06-py3

`24.06-py3` tops out around sm_90 and **silently CPU-falls-back** on Blackwell. Thor needs **sm_110** cubins.

**Recommended:** `nvcr.io/nvidia/pytorch:25.08-py3` (CUDA 13.0, torch 2.8, sm_110 + sm_120/sm_121).  
**Do not use `25.04-py3` on Thor** (no sm_110).  
See `docker-build-deploy.md` and sage-waggle SKILL.md NVIDIA base-image table.

This note supersedes any older camp text that recommended `24.06-py3` as the ML plugin default.
