# GPU passthrough with Podman/CDI on camp Thor nodes

**Applicability:** running a container directly (not via `pluginctl`) on a camp Thor
blade where `docker` is Podman.

## Claim

On these nodes `docker` is **Podman** (4.9.3 observed), and the only working GPU
passthrough flag is **CDI**:

```bash
docker run --rm --device nvidia.com/gpu=all <image>     # WORKS
```

Both alternatives fail:

| Flag | Result (verified on a camp Thor, 2026-09) |
| --- | --- |
| `--runtime=nvidia` | fails loudly: `default OCI runtime "nvidia" not found: invalid argument` |
| `--gpus all` | **exits 0 and injects nothing** — no `/dev/nvidia*` in the container |
| `--device nvidia.com/gpu=all` | works: 4 `/dev/nvidia*` nodes injected |

**`--gpus all` is the dangerous one.** It does not error. The container starts, your
code runs, CUDA is simply absent, and the job looks healthy while running on CPU.
Verify by counting devices, not by checking the exit status:

```bash
docker run --rm --device nvidia.com/gpu=all <image> ls /dev/ | grep -c nvidia   # want > 0
```

CDI specs are pre-installed at `/etc/cdi/nvidia.yaml` and `/var/run/cdi/nvidia.yaml`;
no admin action is needed.

## Why `--runtime=nvidia` cannot be made to work here

The NVIDIA container runtime binary exists but is **not registered with the container
engine**. Registering it means editing `/etc/docker/daemon.json` as root — camp
accounts have no such sudo (see `sudo-allowlist-and-image-import.md`). So this is not
a "run one setup command" gap; on these accounts it is closed.

## Verify the image actually has sm_110 kernels

`torch.cuda.is_available() == True` does **not** mean usable kernels exist — some
Jetson images detect Thor and then fail on real work. Force an actual kernel launch:

```bash
docker run --rm --device nvidia.com/gpu=all <image> \
  python3 -c "import torch; print(torch.cuda.get_device_capability()); \
  x=torch.randn(1000,1000,device='cuda'); print((x@x).sum().item())"
```

Want `(11, 0)` and a finite number. An `sm_87` warning means the wrong image.

## Baseline conflict — read this before following older pages

`SKILL.md` currently says "**Always** use `--runtime=nvidia` … so commands work on
both DGX Spark and Thor", and `references/docker-build-deploy.md` has a section
titled "Docker Runtime: --runtime=nvidia (Not --gpus all)". That guidance is correct
for a Docker host with the nvidia runtime registered, and **wrong for the
Podman/CDI camp node class**, where it cannot be made to work without root.

Decide by engine, not by habit:

```bash
docker --version        # "podman version ..." => use --device nvidia.com/gpu=all
```

> **Verification status:** corroborated across three participants' notes and used
> successfully in-transcript. Re-confirm on a current node before treating the
> Docker-host guidance as superseded fleet-wide — node provisioning varies.

## Related

- `pluginctl-gpu-runtimeclass.md` — the same GPU problem inside k8s pods.
