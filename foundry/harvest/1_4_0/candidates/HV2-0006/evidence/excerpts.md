# HV2-0006 — evidence

**conda-forge/pixi torch has no sm_110**  ·  independence: 1 student(s)  ·  3 episode(s)

## T06 — conda-forge/pixi torch dies at first kernel launch

- **Claim:** conda-forge publishes no sm_110 PyTorch for linux-aarch64 (only cuda129 builds; the pytorch and nvidia channels have no aarch64 pytorch at all), so a pixi/conda env on a Thor reports torch.cuda.is_available()=True and then dies at the FIRST kernel launch with 'CUDA error: no kernel image is available for execution on the device' — a GPU-capability mismatch masquerading as a model/ultralytics bug; there is no conda pin that fixes it, the only path is the CUDA-13 container base.
- kind: `failure_class` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C002, C015, C028
- **Baseline conflict:** docker-build-deploy.md covers sm_110 for container tags only, never host-side envs. 'pixi' appears nowhere in the baseline.
- **Notes:** Deliberately NOT merged with T05 despite near-total keyword overlap - opposite symptoms (fast failure vs infinite hang) need opposite diagnostics. Merging would misdiagnose both.

### `node-H035-20260723_142740_b07b9d-04`
friction: retry_depth=6 failures=13 wall=2792.6s resolved=True

> Pixi isn't installed on this machine. The terminal tool is running with `$HOME` expanded under the Hermes profile (`~/.hermes/profiles/sage/home`), which I've already seen in earlier calls — so my `~` lookups go there, not the real `/home/<user>`.

### `node-H035-20260723_142740_b07b9d-04`
friction: retry_depth=6 failures=13 wall=2792.6s resolved=True

> NVIDIA Thor with CUDA capability sm_110 is not compatible with the current PyTorch installation.\nThe current PyTorch install supports CUDA capabilities sm_50 sm_60 ... sm_100 sm_120 ... torch.AcceleratorError: CUDA error: no kernel image is available for execution on the device

### `node-H035-20260723_142740_b07b9d-09`
friction: retry_depth=1 failures=1 wall=13000.7s resolved=True

> That specific PyTorch binary was compiled to support a list of GPUs (sm_50, sm_80, sm_90, etc.), but it was **not** compiled with kernels for **sm_110**. ... Conda-forge does not currently provide an aarch64 build of PyTorch that includes sm_110 kernels.

### `node-H035-20260723_142740_b07b9d-15`
friction: retry_depth=0 failures=0 wall=0.0s resolved=False

> the PyTorch wheel conda-forge shipped for `linux-aarch64 + cuda129` was compiled without `sm_110` kernels (Blackwell), so the first kernel launch on this Thor's GPU fails with `no kernel image is available for execution on the device`
