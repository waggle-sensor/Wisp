# HV2-0003 — evidence

**pluginctl GPU requires runtimeClassName**  ·  independence: 2 student(s)  ·  6 episode(s)

## T03 — pluginctl pods get no GPU without runtimeClassName

- **Claim:** On a Thor node with NO nvidia-device-plugin pod, `pluginctl run` silently produces a CPU-only pod (torch.cuda.is_available()=False) because pluginctl never sets `runtimeClassName` and the node advertises no `nvidia.com/gpu` allocatable resource; the fix is to bypass pluginctl and `kubectl apply` a hand-written pod manifest with `runtimeClassName: nvidia` + `nodeSelector: resource.gpu="true"`, which restores GPU (verified 27ms/frame YOLO vs ~1.4s on CPU).
- kind: `correction` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C014, C005, C021, C043
- **Baseline conflict:** runtimeClassName appears nowhere in the baseline; runtime-packaging-patterns.md:106 asserts the opposite - 'GPU available via NVIDIA device plugin'.
- **Notes:** Cross-shard: found independently by 4 miners. Includes the negative result that `--privileged` is NOT a substitute (a plausible workaround a student disproved live), and the one-command preflight: the node advertises no nvidia.com/gpu allocatable and the resource.gpu=true label is not evidence the GPU reaches pods.

### `node-H035-20260723_142740_b07b9d-06`
friction: retry_depth=1 failures=1 wall=656.3s resolved=True

> The `nvidia` RuntimeClass exists (handler: `nvidia`), but `pluginctl run` doesn't request a RuntimeClass, and there's no nvidia-device-plugin to advertise `nvidia.com/gpu` resources. So `pluginctl run` simply creates a pod with the default runtime (crun or runc), no GPU attached.

### `node-H035-20260723_142740_b07b9d-07`
friction: retry_depth=0 failures=0 wall=8667.8s resolved=False

> `pluginctl run` does NOT set `runtimeClassName` — it creates the pod with the default runtime (crun/runc), which does not wire `/dev/nvidia*` into the container even when the node has `resource.gpu=true` / `resource.cuda110=true` labels.

### `node-H035-20260723_142740_b07b9d-07`
friction: retry_depth=0 failures=0 wall=8667.8s resolved=False

> ===wes-identity contents===
> apiVersion: v1
> data:
>   WAGGLE_NODE_ID: [REDACTED]
>   WAGGLE_NODE_VSN: H035
> ... \"project\": \"SGT\", ... \"sensors\": [], \"resources\": []

### `node-H035-20260723_142740_b07b9d-11`
friction: retry_depth=0 failures=0 wall=0.0s resolved=False

> Definitive: the container has **no GPU access** — `/dev/nvidia*` devices are absent and `runtimeClassName` is empty (no NVIDIA runtime class attached). On a Thor this normally "just works" via the NVIDIA container runtime, but apparently not for `pluginctl run` on this node.

### `node-H035-20260723_142740_b07b9d-12`
friction: retry_depth=1 failures=1 wall=0.0s resolved=True

> there is no `nvidia-device-plugin` pod anywhere (no `kube-system` nvidia-device-plugin, no `gpu-operator`), and the node's `allocatable` resources list NO `nvidia.com/gpu`. On a stock Jetson/Thor with the NVIDIA container runtime correctly configured, you see `nvidia.com/gpu: 1` ... Here it's absent

### `node-H035-20260724_011258_f7a2ab-06`
friction: retry_depth=2 failures=4 wall=774.1s resolved=True

> sudo pluginctl run --privileged --selector resource.gpu=true --resource limit.memory=16Gi,request.memory=4Gi  --name batman-app 10.31.81.1:5000/local/plugin -- --camera-source videos/P1.1.2_grey.mov\n...\n2026-07-24 02:24:49,014 INFO Model loaded. torch.cuda.is_available()=False

### `node-H03F-20260727_003225_269cc7-01`
friction: retry_depth=0 failures=0 wall=3194.1s resolved=False

> The Thor node has working NVIDIA GPU access through Podman (--device=nvidia.com/gpu=0), but Kubernetes does not advertise nvidia.com/gpu capacity. kubectl describe node shows no NVIDIA resources and there is no NVIDIA device plugin pod.
