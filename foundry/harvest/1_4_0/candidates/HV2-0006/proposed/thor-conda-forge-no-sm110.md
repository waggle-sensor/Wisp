# conda-forge / pixi PyTorch on Thor: `no kernel image is available`

**Applicability:** Thor host environments built with **pixi** or conda/mamba from
**conda-forge**. Distinct from the PyPI-wheel hang — see the table at the bottom.

## Symptom

The env installs cleanly. `torch.cuda.is_available()` returns **`True`**. Then the
first real kernel launch dies immediately:

```
RuntimeError: CUDA error: no kernel image is available for execution on the device
```

Fast and loud, unlike the PyPI-wheel hang. `is_available() == True` is what makes it
confusing: the device is visible, the *cubins* for it are missing.

## Cause

conda-forge publishes no `linux-aarch64` PyTorch build containing **sm_110**
(Blackwell) cubins — only `cuda129` builds compiled for older architectures. The
`pytorch` and `nvidia` channels have no aarch64 PyTorch at all.

**There is no `pixi.toml` edit, channel addition, or CLI flag that fixes this.** The
artifact does not exist. Time spent hunting for one is wasted — a bounded-search rule
is worth applying here.

## What to do

Two supported paths, and no third:

1. **GPU work in the NVIDIA container** — `nvcr.io/nvidia/pytorch:25.08-py3` or newer
   (CUDA 13, sm_110), via `pluginctl` or CDI. See
   `pluginctl-gpu-runtimeclass.md` and `podman-cdi-gpu-passthrough.md`.
2. **CPU-only on the host** for iteration — but read `thor-host-torch-hang.md` first:
   with PyPI wheels, `CUDA_VISIBLE_DEVICES=''` is *not* sufficient on its own.

Students frequently arrive with a pixi-based research repo and expect to run it
as-is on the node. Say early that the host env is a CPU-only development surface and
that GPU means a container — it saves a day.

## Quick discrimination

```python
import torch
print(torch.cuda.is_available())              # True here, False/hang elsewhere
print(torch.cuda.get_device_capability())     # want (11, 0)
x = torch.randn(8, 8, device="cuda"); print((x @ x).sum().item())   # dies here
```

| Symptom | Cause | Page |
| --- | --- | --- |
| `is_available()` True, **fails fast** at first kernel | conda-forge/pixi, no sm_110 cubins | this page |
| CUDA call **hangs forever**, unkillable (D-state) | PyPI host wheel | `thor-host-torch-hang.md` |
| `is_available()` False fast + nvmap permission error | `/dev/nvmap` perms | `SKILL.md` nvmap pitfall |
