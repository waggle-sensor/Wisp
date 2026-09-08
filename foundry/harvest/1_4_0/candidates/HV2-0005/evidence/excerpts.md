# HV2-0005 — evidence

**Host PyPI torch D-state hang**  ·  independence: 1 student(s)  ·  2 episode(s)

## T05 — Host PyPI torch hangs forever in D-state

- **Claim:** On a camp Thor (JetPack R38.2.1 / L4T 38.2.1), a generic PyPI aarch64 torch wheel (torch 2.13.0+cu130) imports fine but every CUDA entry point — torch.cuda.is_available(), .cuda(), even nvidia-smi on the host — HANGS FOREVER rather than returning False or raising; the misleading symptom is a series of tool timeouts that look like 'slow first import', and the fix is to stop probing on the host and do all GPU work inside nvcr.io/nvidia/pytorch:25.08-py3.
- kind: `correction` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C001, C008
- **Baseline conflict:** Corrects v1's own thor-host-cpu-dev-first.md, shipped in 1.2.0, which prescribes CUDA_VISIBLE_DEVICES= before importing torch as the fix.
- **Notes:** The sharpest argument for transcripts over artifacts: v1 mined a student artifact frozen 2026-07-23; the same student superseded it on 07-24. Mining artifacts froze a claim the cohort had already outgrown.

### `node-H021-20260723_004314_437672-02`
friction: retry_depth=3 failures=11 wall=861.7s resolved=True

> torch ok: 2.13.0+cu130\nchecking cuda...\n\n[Command timed out after 40s]

### `node-H021-20260723_004314_437672-07`
friction: retry_depth=1 failures=2 wall=374.1s resolved=True

> PyPI torch (2.13.0+cu130) in a host venv imports fine but HANGS INDEFINITELY on any CUDA call (no error, no timeout) — lacks Blackwell sm_110 kernels. Use `nvcr.io/nvidia/pytorch:25.08-py3` (torch 2.8, CUDA 13.0, sm_110/sm_121) for GPU work.
