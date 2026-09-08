# Foundry v2 — live canary on a camp Thor

**Node:** `node-H039.sage` (`sgt-thor-1423225065711-H039`), aarch64, JetPack-class.
**Date:** 2026-09-02. **Access:** root over SSH.
**Purpose:** close the largest limitation of this pass — every earlier result was
textual (retrievability/actionability), never hardware truth. Nine of ten candidates
*correct* shipped guidance, and a stale correction is worse than none.

> **Caveat that qualifies every result below.** The canary ran as **root**; the 2026
> students were non-root members of `%develop`. Claims about the *content* of node
> configuration (sudoers, CDI, RuntimeClass, pod specs, library source) transfer
> directly. Claims about what a *student* is permitted to do are read from
> configuration here, not experienced. Where that distinction matters it is flagged.

## Summary

| Candidate | Claim | Verdict |
| --- | --- | --- |
| HV2-0002 | sudo NOPASSWD allowlist excludes `k3s` | **CONFIRMED** (config) |
| HV2-0003 | pluginctl pods get no GPU without `runtimeClassName` | **CONFIRMED** (causal A/B) |
| HV2-0004 | CDI is the working GPU flag, not `--runtime=nvidia` | **CONFIRMED + corrected** |
| HV2-0006 | Thor is sm_110; NVIDIA container works | **CONFIRMED** (partial) |
| HV2-0007 | `snapshot.data` is RGB, not BGR | **CONFIRMED** (source + runtime) |
| HV2-0008 | `Camera()` raises a misleading `TypeError`; no camera attached | **CONFIRMED** |
| HV2-0005 | Host PyPI torch hangs in D-state | **NOT TESTED** — see below |
| HV2-0001, 0009, 0010 | HOME rewrite; off-node thread; registry x509 | **NOT TESTED** — see below |

Six of ten verified on real hardware. One correction to a candidate's text resulted.

## HV2-0002 — sudo allowlist (CONFIRMED from node config)

`/etc/sudoers.d/admin-users`:

```
%admin   ALL=(ALL) NOPASSWD: ALL
%develop ALL=(ALL) NOPASSWD: \
    /usr/local/bin/kubectl, /usr/bin/docker, /usr/local/bin/docker, \
    /usr/bin/docker-compose, /usr/local/bin/docker-compose, \
    /usr/bin/runplugin, /usr/bin/pluginctl
```

Character-for-character the allowlist a student's `sudo -l` printed in July, from an
independent node. **`k3s` is absent** — while `SKILL.md` instructs
`sudo k3s ctr images import` in six places, calling it CRITICAL and required.

This is configuration, not inference. (As root the command itself would succeed here,
which is exactly why the config is the right evidence.)

## HV2-0003 — pluginctl GPU (CONFIRMED by controlled A/B)

**Step 1 — pluginctl never emits the field.** `pluginctl deploy --dry-run` across
three variants; `runtimeClassName` appears in **none**:

| Variant | `runtimeClassName` in generated spec? |
| --- | --- |
| plain | no |
| `--selector resource.gpu=true` | no — sets `nodeSelector` only |
| `--privileged` | no — sets `privileged: true` only |

This independently confirms the miner's negative result that `--privileged` is not a
substitute: it changes a different field entirely.

**Step 2 — the field is what decides GPU.** Two pods, identical but for one line,
same image (`nvcr.io/nvidia/pytorch:25.08-py3`), same `nodeSelector`:

| Pod | `runtimeClassName` | `torch.cuda.is_available()` | `/dev/nvidia*` count |
| --- | --- | --- | ---: |
| `v2-noclass` | *(absent)* | **False** | 0 |
| `v2-withclass` | `nvidia` | **True** | 5 |

Single-variable causal evidence. The `nvidia` RuntimeClass **exists** on the node
(`kubectl get runtimeclass` → `crun`, `lunatic`, `nvidia`, `nvidia-experimental`) and
the node carries `resource.gpu=true`. Both are present; neither is used by pluginctl.

So the node *looks* GPU-ready by every label a student would check, and every
pluginctl-deployed GPU plugin silently runs on CPU. Confirms the ~50x slowdown
mechanism reported in-transcript.

Also confirmed: **no `nvidia.com/gpu` in `kubectl describe node` allocatable** and no
device-plugin pod in any namespace — the preflight the candidate recommends.

## HV2-0004 — GPU flags (CONFIRMED, and the page was corrected)

`docker` is **Podman 4.9.3**; OCI runtime is `crun`; `/etc/docker/daemon.json` does
not exist; `/etc/cdi/nvidia.yaml` is present (152 KB).

| Flag | Result |
| --- | --- |
| `--runtime=nvidia` | `Error: default OCI runtime "nvidia" not found: invalid argument` |
| `--gpus all` | **exit 0, zero `/dev/nvidia*` injected** |
| `--device nvidia.com/gpu=all` | works — 4 `/dev/nvidia*` injected |

**The canary corrected the candidate.** The draft said `--gpus all` is "not
implemented by Podman / driver-hook error", implying a loud failure. It does not
fail: it exits 0 and silently injects nothing, which is strictly more dangerous than
erroring. `HV2-0004` was rewritten with the measured table and a device-count
verification step rather than an exit-status check.

This is the canary doing the job it was added for — and a caution for the write-up:
five of these pages were drafted from transcript evidence alone and one of them was
subtly wrong in a way only hardware could reveal.

## HV2-0006 — sm_110 (CONFIRMED, partial)

In `nvcr.io/nvidia/pytorch:25.08-py3` via CDI:

```
cuda: True
cap: (11, 0)
matmul ok: 5324.998046875
```

Confirms the container path and the sm_110 capability. The conda-forge/pixi *failure*
half was not reproduced — that needs a pixi env built on the host (see untested).

## HV2-0007 / HV2-0008 — pywaggle (CONFIRMED at source and runtime)

```
Camera.__init__ signature: (self, device=0, format=<class '...vision.RGB'>)

ImageSample.__init__:
    self.data = self.format.cv2_to_format(data)

RGB.cv2_to_format:
    return cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
```

Runtime behaviour:

```
Camera() -> TypeError: expected string or bytes-like object, got 'int'
input BGR ch0(blue)=200  ->  sample ch0=0, ch2=200
```

Both exactly as claimed. Channel 0 and 2 are transposed on construction, so
`snapshot.data` is RGB — the baseline's `reolink-http-snapshot.md:54` ("Returns BGR
numpy array, same format as `Camera.snapshot().data`") is wrong about the
equivalence, and wrong silently.

`/dev/video*` does not exist on this node and `/run/waggle` is absent, confirming the
no-camera-attached invariant in HV2-0008.

## Not tested, and why

- **HV2-0005 (host torch D-state hang)** — deliberately not run. Reproducing it means
  `pip install torch` on a shared node and then triggering CUDA init, whose entire
  claim is that the resulting process is **unkillable by SIGKILL** and clears only on
  reboot. Running it would risk leaving exactly that state on a node others use. The
  claim is already supported by transcript evidence (`ps` output showing `Dl` state
  across three episodes) plus a student's own written correction. **Recommend the
  instructor run this on a node they can reboot**, with a scheduled reboot window.
- **HV2-0001 (HOME rewrite)** — a property of the Hermes agent harness, not the node.
  Reproducing it requires running Hermes with the sage profile, not an SSH shell.
  Corpus evidence is the strongest in the pass (9/11 students, 52 episodes).
- **HV2-0009 (off-node `Plugin()` thread)** — needs a WES-less environment plus a
  pywaggle broker resolution failure; partially observable but not attempted here.
- **HV2-0010 (registry x509)** — requires the node-local registry at `:5000` and a
  student-context pull; not reproduced as root.

## What the canary changes about the conclusions

1. **The three provisioning-dependent candidates flagged as "may have drifted since
   July" have not drifted.** HV2-0002, HV2-0003 and HV2-0004 all reproduce on a
   different node six weeks later. The miner's caution was right to raise and is now
   discharged for these three.
2. **One candidate was wrong in a detail** and is fixed. Text-only evidence produced
   a subtly incorrect claim about `--gpus all`; only hardware caught it.
3. **The strongest single result of the pass is now causal, not correlational.** The
   `runtimeClassName` A/B isolates one variable and flips CUDA from False to True.
4. **The remaining untested claims are honestly bounded** — one is a harness property,
   one is unsafe to reproduce on shared hardware, two need a student context.
