# GPU in pluginctl pods requires `runtimeClassName: nvidia`

**Applicability:** Thor blades where `pluginctl run` starts a pod that needs CUDA.

## Symptom

The pod builds, starts, publishes, and **succeeds** — but:

- `torch.cuda.is_available()` is `False` inside the pod
- there is no `/dev/nvidia*` in the container
- inference is ~50x slower than expected, with **no error and no OOMKill**

Measured on a camp node: **27 ms/frame with GPU vs ~1.4 s/frame on CPU.**

## Cause

Two independent conditions, both of which must be checked:

1. **`pluginctl run` never sets `runtimeClassName`.** Without it the pod gets the
   default runtime and no GPU devices are injected.
2. **Some camp nodes run no nvidia-device-plugin DaemonSet**, so the cluster
   advertises no `nvidia.com/gpu` allocatable resource at all.

## Preflight — one command, before you debug anything else

```bash
sudo kubectl describe node <node> | grep -A5 Allocatable
```

If `nvidia.com/gpu` is **absent**, no amount of pod-spec tuning will get a GPU
through the scheduler on this node.

> **The `resource.gpu=true` node label is not evidence the GPU reaches pods.** It is
> present on nodes that cannot serve GPU to a pod. Do not treat it as a check.

## What does NOT fix it

- **`--privileged` is not a substitute for `runtimeClassName`.** Verified live: with
  `--privileged --selector resource.gpu=true` the pod still reports
  `torch.cuda.is_available() == False` and `/dev/nvidia*` is still absent. This is a
  plausible workaround that a student disproved — do not spend time on it.
- Adding the user to `video`. That is the *host* `/dev/nvmap` issue, a different
  failure with a fast, loud error (see the nvmap material in `SKILL.md`).
- Swapping the base image. sm_110 tags matter, but only once devices are injected.

## Fix

Bypass pluginctl's generated spec and apply a manifest that names the runtime class:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <plugin>
spec:
  runtimeClassName: nvidia
  nodeSelector:
    resource.gpu: "true"
  containers:
    - name: <plugin>
      image: <ref>
```

```bash
sudo kubectl apply -f pod.yaml      # kubectl is on the sudo allowlist
```

Useful while iterating: `pluginctl deploy --dry-run` prints the generated pod spec
with no RBAC needed, so you can see exactly what is missing.

## Note on baseline drift

`references/runtime-packaging-patterns.md` states "GPU available via NVIDIA device
plugin". That holds on nodes that run the device plugin and **not** on the camp
blades observed here. Confirm per node with the preflight above rather than assuming
either way.

## Related

- `podman-cdi-gpu-passthrough.md` — GPU outside k8s, on the same nodes.
- `thor-host-torch-hang.md` — CUDA problems that are not about pods at all.
