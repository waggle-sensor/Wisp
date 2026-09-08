# Host PyPI torch on Thor: an unkillable hang, not a fallback

**Applicability:** Jetson AGX Thor host Python (venv or system), stock **PyPI**
`torch` wheels. **Supersedes the guidance in `thor-host-cpu-dev-first.md`** — see
"Correction" below.

> **Scope:** this page covers only the case where a CUDA call never returns. A fast
> failure with a device-permission message is a different problem — see
> `references/direct-node-testing.md`.

## Symptom

`import torch` succeeds. Then any CUDA entry point — `torch.cuda.is_available()`,
`.cuda()`, the first tensor op, even `nvidia-smi` on the host in some cases — **hangs
forever**: no traceback, no timeout, no CPU fallback.

The process enters uninterruptible **D-state** and **cannot be killed with
SIGKILL**. Observed in-transcript:

```
kylelim+ 1734938 ... Dl 17:27 ... python scripts/train_and_evaluate.py
```

> "They're in D state (uninterruptible), can't be killed even with SIGKILL."

Practical effect: the tool call times out, retries pile up, and the node accumulates
unkillable processes until reboot. It reads as a slow download, not a hang.

## Cause

PyPI aarch64 wheels (e.g. `torch 2.13.0+cu130`) carry no working Blackwell **sm_110**
kernels, and the CUDA runtime initialisation path blocks in the driver rather than
failing.

## Correction — `CUDA_VISIBLE_DEVICES=` alone is NOT enough

Earlier camp guidance (profile 1.2.0, `thor-host-cpu-dev-first.md`) prescribed:

> export `CUDA_VISIBLE_DEVICES=` … at the top of host scripts, before importing torch

**This is insufficient.** `import torch` *itself* triggers CUDA runtime init and
D-states even with `CUDA_VISIBLE_DEVICES=''`. Setting the variable does not help if
the import happens at module level.

## Working pattern

**1. Never import torch at module level** in a script whose main path does not need
it. sklearn/numpy paths must be reachable without touching torch:

```python
# NOTE: torch is NOT imported at module level — the CUDA init hangs in D-state on
# Blackwell even with CUDA_VISIBLE_DEVICES=''. Import lazily, inside the function
# that actually needs it, behind an explicit opt-in.
import numpy as np
from sklearn.svm import SVC

def run_mlp(...):
    if not _torch_cpu_probe():
        print("SKIPPED — torch CPU probe failed/timed out")
        return None
    import torch                      # only here
    import torch.nn as nn
```

**2. Probe torch in a subprocess with a timeout**, never in-process — an in-process
`signal.alarm` cannot interrupt a D-state:

```python
def _torch_cpu_probe(timeout=10):
    """True if torch can do a CPU matmul without hanging.

    Runs in a subprocess because torch may enter an uninterruptible D-state during
    Blackwell CUDA init; SIGALRM cannot interrupt that, a process boundary can.
    """
    import subprocess, sys
    code = ("import os; os.environ['CUDA_VISIBLE_DEVICES']=''; "
            "import torch; t=torch.randn(4,64); _=t@t.T; print('OK')")
    try:
        r = subprocess.run([sys.executable, "-c", code],
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0 and "OK" in r.stdout
    except Exception:
        return False
```

**3. Do GPU work in a container**, via `pluginctl` or CDI — see
`pluginctl-gpu-runtimeclass.md` and `podman-cdi-gpu-passthrough.md`.

## Distinguish from two neighbours

| Symptom | Cause | Page |
| --- | --- | --- |
| CUDA call **hangs forever**, process unkillable | PyPI host wheel, no sm_110, D-state | this page |
| `is_available()` **True**, then `no kernel image is available` at first kernel | conda-forge/pixi host env | `thor-conda-forge-no-sm110.md` |
| `is_available()` **False fast**, device-permission error | host device permissions | `direct-node-testing.md` |

Three different failures, three different fixes. The hang is the one that costs a
reboot.
