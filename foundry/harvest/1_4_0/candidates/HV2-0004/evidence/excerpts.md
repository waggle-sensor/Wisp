# HV2-0004 — evidence

**Podman/CDI GPU passthrough**  ·  independence: 2 student(s)  ·  2 episode(s)

## T04 — Podman/CDI is the working GPU passthrough, not --runtime=nvidia

- **Claim:** On camp Thor blades the working docker/podman GPU flag is CDI `--device=nvidia.com/gpu=all`, not `--gpus all` and not `--runtime=nvidia` — `--runtime=nvidia` needs nvidia-container-runtime registered in /etc/docker/daemon.json (root-only, which camp accounts lack), so the baseline's `--runtime=nvidia (Not --gpus all)` guidance is stale for these nodes.
- kind: `correction` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C009, C044
- **Baseline conflict:** SKILL.md:660 says 'Always use --runtime=nvidia'; docker-build-deploy.md:73 has a section titled 'Docker Runtime: --runtime=nvidia (Not --gpus all)'.
- **Notes:** Corroborated by three students' MEMORY.md independently of the transcripts. Flagged verify_on_canary: a miner warned the baseline may be drifting from fleet state and that a stale correction is worse than none.

### `node-H035-20260724_011258_f7a2ab-04`
friction: retry_depth=1 failures=2 wall=219.0s resolved=False

> This replaces the old docker flags
> # do not use this!
> --gpus all
> 
> # use this instead
> --device=nvidia.com/gpu=all

### `node-H021-20260723_004314_437672-04`
friction: retry_depth=0 failures=0 wall=35.1s resolved=False

> The container can't access the GPU. `--gpus all` gives a "NVIDIA Driver was not detected" warning and `cuda False`. `--runtime=nvidia` fails with "default OCI runtime nvidia not found."
