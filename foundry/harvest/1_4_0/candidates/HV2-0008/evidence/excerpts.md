# HV2-0008 — evidence

**Camera offline development**  ·  independence: 1 student(s)  ·  4 episode(s)

## T08 — pywaggle Camera() zero-arg raises a misleading TypeError

- **Claim:** Calling pywaggle's `Camera()` with no argument raises `TypeError: expected string or bytes-like object, got 'int'` (not a missing-camera error) because the default `device=0` is an int that `Camera.__init__` feeds straight into `re.match`; always pass a device STRING (`"file://example.jpg"`, an RTSP URL, or a data-shim name).
- kind: `failure_class` · confidence: high · generality: toolchain · cross-shard: False
- merged from clusters: C016
- **Baseline conflict:** camera-rtsp-patterns.md documents the device-routing chain but not that the zero-arg default crashes with a type error rather than a graceful device-open failure.
- **Notes:** Pairs naturally with T09 and the no-camera-attached invariant on one offline-dev page.

### `node-H032-20260720_205548_b91283-00`
friction: retry_depth=1 failures=1 wall=98.4s resolved=True

> TypeError: expected string or bytes-like object, got 'int'
>   File ".../waggle/data/vision.py", line 163, in __init__
>     match = re.match(r"([A-Za-z-9]+)://(.*)$", device)

## T12 — Camp blades ship with no camera and are SGT-scoped

- **Claim:** Camp Thor blades ship with NO camera attached — no `/dev/video*`, empty `v4l2-ctl --list-devices`, no `/run/waggle/data-config.json`, an empty `"sensors": []` in the node manifest, and no port-554 host on either node subnet — so `Camera()`, `Camera("bottom_camera")` and any RTSP plugin will fail until hardware is physically added and registered; probe those five things before writing camera code.
- kind: `invariant` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C013, C026, C036, C022
- **Baseline conflict:** auth-api-manifests-and-nodes.md presents the manifest endpoint as the camp default and never says it returns empty for SGT-project nodes.

### `node-H035-20260721_015837_deb440-01`
friction: retry_depth=0 failures=0 wall=126.2s resolved=False

> W072 actually returns HTTP 200 and a full manifest from the auth API — so the node is registered in the Sage fleet. The cloud-side manifest knows about it: it's a DAWN project node at "TBD, Chicago, IL" ... project DAWN, with an active nxcore (Xavier NX), nxagent, rpi, etc.

### `node-H035-20260721_015837_deb440-01`
friction: retry_depth=0 failures=0 wall=126.2s resolved=False

> === W072 manifest (HTTP status) ===\nHTTP 301\n=== W072 nodes API (HTTP status) ===\nHTTP 301\n=== known-good node W088 manifest ===\n\n=== W088 HTTP status ===\nHTTP 301

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

### `node-H035-20260724_011258_f7a2ab-09`
friction: retry_depth=1 failures=2 wall=16143.7s resolved=True

> === V4L2 devices ===
> === check /dev ===
> crw-rw----+ 1 root video 505, 0 Jun  5 15:36 /dev/media0
> crw-rw-rw-  1 root root    1, 3 Jan  1  1970 /dev/v4l2-nvdec
> crw-rw-rw-  1 root root    1, 3 Jan  1  1970 /dev/v4l2-nvenc
