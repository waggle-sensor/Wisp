# Thor host: CPU-dev-first for PyPI torch (distinct from container GPU)

**Applicability:** Jetson AGX Thor / JetPack R38-class aarch64 **host venv** using **PyPI** `torch` wheels. Not a substitute for the existing `/dev/nvmap` + `video` group pitfall (that path returns `torch.cuda.is_available() == False` with a permission error). This page is the **hang** failure class.

## Claim

On Thor host Python, stock PyPI torch often **imports cleanly** then **hangs indefinitely** on `torch.cuda.is_available()`, `.cuda()`, or first CUDA op: no traceback, no timeout. Root cause class: host wheels lack working Blackwell **sm_110** kernels. This is **not** fixed by adding the user to `video`.

**Do development CPU-only on the host. Defer GPU to `pluginctl` / NVIDIA container images (`nvcr.io/nvidia/pytorch:25.08-py3` or newer with sm_110).**

## Preflight (before `import torch` in a host venv)

```bash
# 1) Do not probe CUDA from a PyPI host venv if a previous probe hung.
# 2) Force CPU for all host scripts:
export CUDA_VISIBLE_DEVICES=
```

At the **top** of host scripts, before importing torch:

```python
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
```

Then install/run as usual (`pip install torch torchvision …` in the project venv).

## What NOT to do

- Do not wait on `torch.cuda.is_available()` from the host venv — it may never return.
- Do not assume `docker run --gpus all` / `--runtime=nvidia` without daemon config is the camp path. Camp default is `sudo pluginctl build` → `sudo pluginctl run --selector resource.gpu=true` (see `pluginctl-camp-guide.md`).
- Do not pass `--device /dev/nvidia0` and expect host-style CUDA libs to appear.

## Contrast: `/dev/nvmap` permission (already in sage-waggle)

If `torch.cuda.is_available()` returns **False quickly** with `NvRmMemInitNvmap Permission denied`, that is the **video group / `/dev/nvmap`** issue documented in `SKILL.md` (host `python3 app.py` vs pluginctl GPU injection). Different symptom, different fix.

| Symptom | Typical cause | Fix |
| --- | --- | --- |
| CUDA call **hangs forever** on host PyPI torch | Missing/invalid sm_110 kernels in the wheel | `CUDA_VISIBLE_DEVICES=` on host; GPU only in 25.08+ NVIDIA container via pluginctl |
| CUDA **False** + nvmap permission error | `/dev/nvmap` not accessible to the user | pluginctl GPU pod, or `video` group if you must run on host |

## GPU packaging (after CPU PoC)

- Base image: `nvcr.io/nvidia/pytorch:25.08-py3` (CUDA 13, sm_110). See `docker-build-deploy.md`. Do not use `25.04-py3` or `24.06-py3` on Thor.
- Deploy: `pluginctl` with GPU selector / resources. Freeze torch/torchvision/numpy with a pip constraints file so `pip install` does not replace NVIDIA wheels.

## Related

- `docker-build-deploy.md`, `ml-plugin-patterns.md`, `pluginctl-camp-guide.md`, `thor-arm64-deploy-pipeline.md`
