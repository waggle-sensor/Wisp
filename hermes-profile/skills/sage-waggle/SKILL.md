---
name: sage-waggle
description: "Sage Continuum & Waggle: edge computing platform — plugin dev, ECR submission, data APIs, job scheduling, node management, testing."
tags: [edge-computing, iot, sage, waggle, scientific-compute]
triggers:
  - User mentions Sage, Waggle, sagecontinuum, waggle-sensor, Beehive, Beekeeper, WES
  - Tasks involving edge computing plugins that publish sensor data
  - Querying environmental/scientific sensor data from distributed nodes
  - Scheduling jobs on edge nodes (sesctl, pluginctl)
  - Working with sage-data-client or pywaggle
  - Developing Docker-based edge plugins
  - Using the Sage MCP server
globs: ["*sage*", "*waggle*", "*plugin*sage*", "*beehive*"]
---

# Sage Continuum & Waggle Platform

## Architecture Overview

1. **Edge Nodes** — ARM64/x86; WES/k3s. Prefer honesty: real VSNs/names only (`references/data-query-first-report-and-history.md`, `references/data-viz-and-honesty.md`). Key refs: `references/stack-architecture-map.md`, `references/pywaggle2-producer-consumer-architecture.md`, `references/frame-anchored-batch-consumers-and-watchers.md`, `references/frame-anchored-vs-window-pollers.md`, `references/node-ssh-access-and-gpsd-probe.md`, `references/node-identity-and-upload-contract.md`, `references/pywaggle2-nodeinfo-gps-design.md`, `references/wes-pod-config-and-manifest-exposure.md`, `references/pluginctl-sideload-and-node-build.md`, `references/node-sideload-test-and-restore.md`, `references/audio-plugin-multinode-testing.md`, `references/storage-upload-health-verification.md`, `references/ci-handoff-doc-discipline.md`, `references/thor-arm64-deploy-pipeline.md`, `references/scheduling-continuous-vs-oneshot-and-gpu-contention.md`, `references/producer-consumer-gpu-and-shared-mounts.md`.
2. **Beehive (Cloud)** — Receives data uploads, stores in time-series DB + object store. Runs RabbitMQ message bus.
3. **Beekeeper** — Node identity, registration, provisioning, reverse SSH tunnels for management.

## Key APIs

| API | Endpoint | Auth | Notes |
|-----|----------|------|-------|
| Data query (timeseries) | `POST https://data.sagecontinuum.org/api/v1/query` | None (public) | Beehive timeseries from `plugin.publish()`. NDJSON. Filters: `plugin`, `name`, `vsn`, `sensor`. See `references/timeseries-data-query-api.md` |
| Manifests (rich) | `GET https://auth.sagecontinuum.org/manifests/` · `.../manifests/<vsn>` | None | Full node hardware + sensor **URI**s. Collection needs trailing `/`; single VSN slash optional. Prefer per-VSN (full list ≈2MB+). `?project=` |
| Nodes (beta) | `GET https://auth.sagecontinuum.org/api/v-beta/nodes/` · `.../nodes/<vsn>` | None | Flatter node card (type, site, partner, focus, modem). Filters: `?phase=`, `?project__name=` (comma=OR) |
| Edge Scheduler | `https://es.sagecontinuum.org` | Bearer token | Job submission/management |
| MCP Server (Sage) | `https://mcp.sagecontinuum.org/mcp` | None (read-only); Bearer for jobs | 29 Sage tools — `references/mcp-tools.md` |
| MCP Server (GitHub) | `https://api.githubcopilot.com/mcp/` | Bearer GitHub PAT | Repos/issues/PRs/Actions — [registry](https://github.com/mcp/github/github-mcp-server) · `references/github-mcp-server.md` |
| MCP Server (Hugging Face) | `https://huggingface.co/mcp` | Bearer HF token | Models/datasets/Spaces/papers/docs/Jobs — [docs](https://huggingface.co/docs/hub/en/agents-mcp) · `references/huggingface-mcp-server.md` |
| MCP Server (Milvus SDK helper) | `https://sdk.milvus.io/mcp/` | None (`Accept: text/event-stream`) | Prefer **Milvus Lite** + `MilvusClient` — [MCP docs](https://milvus.io/docs/milvus-sdk-helper-mcp.md) · [Lite](https://milvus.io/docs/milvus_lite.md) · `references/milvus-sdk-helper-mcp.md` |
| Portal | `https://portal.sagecontinuum.org` | Browser login | Node management, token generation |
| ECR (Edge Code Repo) | Portal: `https://portal.sagecontinuum.org/apps` · API: `GET https://ecr.sagecontinuum.org/api/apps?public=true` | List public: none | Public plugins/apps available to schedule. Per-app: `/api/apps/<ns>/<name>` · `/api/apps/<ns>/<name>/<ver>`. See `references/ecr-public-apps-api.md` |

Auth / manifest details + related routes (`/computes/`, `/sensors/`, …): **`references/auth-api-manifests-and-nodes.md`**. App source: [waggle-auth-app](https://github.com/waggle-sensor/waggle-auth-app).

Auth tokens: get from `portal.sagecontinuum.org/account/access`. Format: `Authorization: Bearer {token}`.

## Plugin Development

> **Camp default (Thor):** prefer `sudo pluginctl build .` → `sudo pluginctl run` for on-node development. Start with `references/pluginctl-camp-guide.md`. Use raw `podman build` only for ECR-bypass side-load workflows (see `references/pluginctl-sideload-and-node-build.md`).

**Official docs (prefer these URLs when citing Sage):**
- **Full docs catalog (summary + URL for every page):** `references/sage-docs-index.md` — pick a URL, then fetch the live page for full content
- **Public code catalog (`waggle-sensor` org):** `references/waggle-sensor-repos-index.md` — summary + URL per public repo (private skipped)
- **Public code catalog (`sagecontinuum` org):** `references/sagecontinuum-repos-index.md` — summary + URL per public repo (private skipped)
- **NVIDIA Jetson Thor / JetPack docs catalog:** `references/nvidia-jetson-thor-docs-index.md` — product + JetPack + Jetson Linux r39.2 Developer Guide (summary + URL; prefer Thor pages)
- **NVIDIA agent skills (vendored):** `references/nvidia-skills-index.md` — [NVIDIA/skills](https://github.com/NVIDIA/skills) (`jetson-*`, DeepStream, TAO, …)
- **DuckDB docs catalog:** `references/duckdb-docs-index.md` — [duckdb.org/docs](https://duckdb.org/docs/current/) summary + URL (Python/CLI, SQL, CSV/Parquet, guides)
- **Getting started:** <https://sagecontinuum.org/docs/getting-started>
- **Edge apps tutorial:** <https://sagecontinuum.org/docs/category/edge-apps>
- **pluginctl reference:** <https://sagecontinuum.org/docs/reference-guides/pluginctl> · tutorials: <https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/pluginctl>
- **sesctl reference:** <https://sagecontinuum.org/docs/reference-guides/sesctl> · tutorials: <https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/sesctl>

Plugins are Docker containers using **[pywaggle](https://github.com/waggle-sensor/pywaggle)** — the official Python SDK for Waggle plugins (`waggle.plugin`, cameras, microphones, uploads). Prefer that GitHub repo as the source of truth for API, docs, and source layout (`src/waggle/…`).

**Install:**
```bash
pip install -U 'pywaggle[all]'          # core + audio + vision
# or subsets: pywaggle | pywaggle[audio] | pywaggle[vision]
```

**Docs / source:**
- Repo: <https://github.com/waggle-sensor/pywaggle>
- Writing a plugin: <https://github.com/waggle-sensor/pywaggle/blob/main/docs/writing-a-plugin.md>
- Plugin source: <https://github.com/waggle-sensor/pywaggle/tree/main/src/waggle>
- Latest release (PyPI via GitHub releases): check repo Releases (e.g. 0.56.x)

Minimal pattern:

```python
from waggle.plugin import Plugin
import time

with Plugin() as plugin:
    while True:
        value = read_sensor()
        plugin.publish("env.measurement", value, meta={"units": "C"})
        time.sleep(30)
```

### Plugin file structure
- `app.py` — main application
- `Dockerfile` — based on `waggle/plugin-base:1.1.1-base` (ARM64) or `-ml` variant for GPU
- `.dockerignore` — excludes tests/, ecr-meta/, jobs/, __pycache__/, *.pyc, *.md, .git/ from Docker build context
- `sage.yaml` — metadata (name, description, version, authors, resources)
- `ecr-meta/` — ECR submission metadata
- `overview.md` — pedantic/instructive documentation (mini tutorial style)
- `jobs/` — per-plugin job YAMLs for edge scheduler deployment (self-contained)
- `tests/` — self-contained test suite (local test with real GPU inference, test images, harness copy, run script). See `references/testing-patterns.md`

### Camera & Microphone (pywaggle abstractions)
```python
from waggle.data.vision import Camera
cam = Camera("bottom_camera")     # Named (resolved via node data config — only on real Sage nodes)
cam = Camera("rtsp://admin:pass@192.168.1.100:554/h264Preview_01_main")  # RTSP IP camera
cam = Camera("/path/image.jpg")   # Static image — bare path, works on host only (NOT in Docker — see pitfall below)
cam = Camera("file:///path/image.jpg")  # Static image in Docker (bare paths trigger WES config lookup → FileNotFoundError)
sample = cam.snapshot()            # ImageSample: .data (numpy HWC RGB), .timestamp (ns), .save()

from waggle.data.audio import Microphone
mic = Microphone("my_microphone")
sample = mic.record(duration=5)    # AudioSample: .data (numpy), .timestamp, .save()
```

### Audio Plugin Development

For audio-based plugins (bird classification, sound event detection),
the pattern differs from vision plugins:

**Audio input modes:**
1. **pywaggle Microphone** — `Microphone("mic_name").record(duration=3)` for named node microphones
2. **Direct ALSA/PulseAudio** — `sounddevice` or `pyaudio` for direct recording on host
3. **File-based** — `--audio-dir` flag for batch testing against WAV/MP3 files
4. **Network camera audio via `--camera URL`** — extract audio from IP camera via ffmpeg. The `--camera` CLI flag accepts any ffmpeg-compatible audio source URL. The plugin auto-detects the stream type and adds appropriate ffmpeg flags. See `references/camera-audio-capabilities.md` for the full camera comparison. Supported patterns:
   ```bash
   # Mobotix MxPEG (auto-detected by "faststream" + "MxPEG" in URL, adds -f mxg)
   --camera "http://user:pass@IP/control/faststream.jpg?stream=MxPEG&needlength"

   # RTSP (auto-detected by rtsp:// scheme, adds -rtsp_transport tcp)
   --camera "rtsp://user:pass@IP/profile1/media.smp"

   # Any HTTP audio stream
   --camera "http://IP/audio.cgi"
   ```
   **IMPORTANT**: Mobotix M16 cameras may refuse RTSP (port 554 closed) but serve audio fine via MxPEG HTTP. Always try the MxPEG URL first. Tested: M16 delivers pcm_alaw at 8 KHz (4 KHz Nyquist) — marginal for BirdNET, which needs frequencies up to 8-15 KHz. A USB mic at 48 KHz is significantly better. pywaggle's `Microphone` class does NOT support network cameras — the plugin uses subprocess ffmpeg for camera audio.

**Key differences from vision plugins:**
- Audio chunks are typically 3 seconds (vs single-frame snapshots for vision)
- Sample rate matters: BirdNET requires 48 kHz, resampling if needed
- Model formats: TFLite (CPU, ARM64) vs PyTorch (GPU); GPU inference on ARM64
  is not always available (see BirdNET ARM64 limitation)
- Audio files can be large — consider recording to tmpfs and cleaning up
- Noise rejection: most audio classifiers have "non-event" classes for
  filtering environmental noise, human speech, etc.

**BirdNET V2.4 integration pattern (`pip install birdnet`):**
```python
import birdnet

# Load models (auto-download ~77MB acoustic + ~46MB geo on first use)
model = birdnet.load("acoustic", "2.4", "tf")
geo = birdnet.load("geo", "2.4", "tf")

# Species filtering by location + week
species = geo.predict(lat, lon, week=22, min_confidence=0.03)
species_set = species.to_set()  # NOT to_list()

# File-based prediction
predictions = model.predict(
    "recording.wav",
    top_k=5,
    default_confidence_threshold=0.25,  # NOT min_confidence
    sigmoid_sensitivity=1.0,
    custom_species_list=species_set,
    overlap_duration_s=0.0,
    bandpass_fmin=0,        # low-freq cutoff Hz (e.g. 150 to cut wind)
    bandpass_fmax=15000,    # high-freq cutoff Hz (e.g. 4000 for 8kHz camera mic)
    batch_size=1,           # increase for parallel processing of long recordings
)
df = predictions.to_dataframe()
# Columns: input, start_time, end_time, species_name, confidence
# species_name format: "Scientific name_Common name"
```

**API pitfalls discovered:**
- `model.predict()` uses `default_confidence_threshold`, NOT `min_confidence`
- `geo.predict()` returns `GeoPredictionResult` — use `.to_set()` (not `.to_list()`)
- Model auto-downloads on first use to `~/.local/share/birdnet/`
- No `__version__` attribute on the birdnet module
- `birdnet.load("acoustic", "2.4", "tf")` — the `"tf"` backend uses TFLite on ARM64 (CPU only, no GPU)
- Audio plugin Dockerfile should use `python:3.12-slim` (not NVIDIA base) since BirdNET is CPU-only on ARM64

**Audio plugin app.py pattern (proven in birdnet repo):**
- Wrap the model in a classifier class (e.g. `BirdNETClassifier`)
- Three audio source modes via CLI flags (in priority order):
  1. `--input <file>` — read from a local audio file (testing)
  2. `--camera <url>` — capture from network camera via ffmpeg subprocess
  3. (default) — record from USB microphone via pywaggle `Microphone`
- The `--camera` flag accepts any ffmpeg-compatible URL; auto-detects Mobotix MxPEG
  (adds `-f mxg`) and RTSP (adds `-rtsp_transport tcp`). Credentials in URL are
  masked in log output (splits on `@`, shows only the host portion).
- `record_from_camera()` function: spawns ffmpeg, converts to 48 KHz mono WAV in tmpdir,
  raises RuntimeError on ffmpeg failure or empty output. Cleanup via shutil.rmtree in finally block.
- Support `--dry-run` for testing without pywaggle (import Plugin only when needed)
- Support `--interval` for gap between cycles + `--num-recordings` for bounded runs
- `--num-recordings N` (default 1) = run exactly N cycles then exit; `--num-recordings 0` = loop forever (requires `--interval > 0`)
- This matches the old plugin's `--num_rec` + `--silence_int` semantics:
  old: `analyze.py --num_rec 6 --sound_int 5 --silence_int 1`
  new: `app.py --num-recordings 6 --duration 5 --interval 1`
- Publish per-species detections + JSON summary per cycle
- Topic format: `env.detection.audio.<scientific_name>` (lowercase, underscored)
- eBird geo-filtering is fully automatic for live deployments: `--lat`/`--lon` default to -1 which triggers auto-detection from the node manifest (`/etc/waggle/node-manifest-v2.json`). `--week` defaults to `auto` (calculate BirdNET week from current date: `(month-1)*4 + min(4, ceil(day/7.5))`, range 1–48). Resolve both at startup before constructing the classifier, so each scheduler invocation gets the correct location and week. Use explicit values to override for testing (`--lat 41.72 --lon -87.98 --week 25`). Use `--week -1` for year-round (no seasonal filter). The `--week` argparse type should be `str` (not `int`) to accept both `auto` and numeric values.
- Use `argparse.ArgumentDefaultsHelpFormatter` + grouped args (audio, model, location, runtime)
- Clean up temp recording files in `finally` blocks (record to tmpdir, shutil.rmtree after)
- Main loop refactored into `run_cycle(plugin=None)` + `run_loop(plugin=None)` —
  eliminates the old duplicate run_once/run_with_plugin code paths

**Audio plugin Dockerfile differs from vision plugins:**
- Base image: `python:3.12-slim` (not NVIDIA — BirdNET is CPU-only on ARM64)
- System deps: `ffmpeg libsndfile1 libasound2-dev`
- Pre-download models at build time: `RUN python3 -c "import birdnet; birdnet.load(...)"`
- Image size: ~2.9 GB (TensorFlow) vs ~10+ GB for vision plugins on NVIDIA base
- No GPU, no CUDA, no pip constraints file needed

See `references/audio-classification-models.md` for the full model survey.

**Camera device resolution** (`resolve_device()` chain):
1. Named stream (no `://`) → WES data config lookup (`/run/waggle/data-config.json`, Sage nodes only)
2. URL with scheme (`rtsp://`, `http://`) → passed directly to `cv2.VideoCapture()`
3. `file://path` → local file
4. Path object → local file

Named cameras (`bottom_camera`, `top_camera`) are aliases defined in the node's `/run/waggle/data-config.json` — a JSON array where each entry has `match.id` (the name) and `handler.args.url` (the actual RTSP/HTTP URL). This config is managed by WES and only exists on real Sage nodes.

For IP cameras not registered in WES (e.g. a Reolink on the same network), pass the RTSP URL directly to `--stream`. See `references/camera-rtsp-patterns.md` for vendor-specific URL formats, data-config.json format, Docker-on-Thor QA testing workflow, and troubleshooting.

### Plugin CLI input modes
Plugins support four input modes via argparse:
1. **`--stream <camera|rtsp|image>`** — live camera, RTSP URL, or single test image (default: `bottom_camera`)
2. **`--image-dir <path>`** — batch-process all images in a directory (overrides `--stream`)
3. **`--snapshot-url <http-url>`** — fetch a JPEG snapshot from an HTTP URL each cycle (overrides `--stream`). Works with Reolink CGI API, generic IP camera snapshot endpoints, or any URL returning a JPEG. Credentials go in the query string. See `references/reolink-http-snapshot.md`.
4. **`--continuous Y|N`** — loop (camera/snapshot-url) or single-shot. **WARNING**: the main loop's `if continuous != "Y": break` must be guarded with `and not using_image_dir` — otherwise `--image-dir` mode only processes the first image. See Pitfalls.

**Note**: Not all plugins implement `--image-dir`. YOLO and BioCLIP have it; vLLM only has `--stream` (accepts a camera name, RTSP URL, or single image path). For batch testing a plugin without `--image-dir`, loop in shell: `for img in tests/test-images/*.jpg; do python3 app.py --stream "$img" --continuous N; done` — but note each invocation may restart expensive resources (e.g. vLLM server subprocess).

### Exposing third-party library parameters
When a plugin wraps a third-party ML library (Ultralytics YOLO, vLLM, etc.), expose the library's key tuning parameters as CLI flags rather than hardcoding them. Pattern:
1. Add argparse flags with descriptive help text including the default value and a URL to the upstream docs
2. Pass the flag values through to the library's API call (e.g. `model(frame, imgsz=args.imgsz, half=args.half, ...)`)
3. Document all flags in overview.md's Configuration Reference table with consistent `Flag | Type | Default | Description` columns
4. Add a callout linking to the upstream docs page (e.g. `https://docs.ultralytics.com/modes/predict/#inference-arguments`)
5. Add corresponding entries to sage.yaml's `inputs:` section

Example YOLO flags exposed from Ultralytics: `--imgsz` (input resolution), `--half` (FP16), `--max-det` (max detections), `--augment` (TTA), `--agnostic-nms` (class-agnostic NMS). Each help string includes a link to Ultralytics docs so students can read the full parameter reference.

Use `iter_image_dir()` helper to yield `(path, frame, timestamp)` tuples from a directory, matching the Camera snapshot interface. Always filter by `IMAGE_EXTENSIONS` set. See `templates/ml-plugin-app.py` for the full pattern.

### Plugin publish patterns
```python
with Plugin() as plugin:
    plugin.publish("env.temperature", 23.5)
    plugin.publish("env.count.car", 12, timestamp=ts, meta={"camera": "bottom", "model": "yolov7"})
    plugin.upload_file("annotated.jpg")  # Upload large files (images, video)
```

**Meta value rule**: all values in `meta={}` must be `str`. pywaggle's `valid_meta()` raises ValueError on int/float/bool. Always `str()` wrap numeric meta.

### Self-describing publish records
When publishing aggregate records (e.g. `env.count.total`), include the full class breakdown in meta so each record is self-describing without cross-referencing per-class records:
```python
classes_summary = ",".join(f"{c}:{n}" for c, n in sorted(counts.items()))
plugin.publish("env.count.total", total, timestamp=ts,
               meta={"camera": source_name, "model": args.model,
                      "classes": classes_summary if classes_summary else "none",
                      "num_classes": str(len(counts))})
```
Result: `{"name":"env.count.total","value":3,"meta":{"classes":"bottle:1,person:2","num_classes":"2",...}}`

### Local testing (no node required)
```bash
export PYWAGGLE_LOG_DIR=./test-run
python3 app.py --stream test-image.jpg --continuous N
cat test-run/data.ndjson    # Published measurements captured here (NDJSON: one JSON object per line)
ls test-run/uploads/        # Uploaded files captured here as {timestamp}-{original_name}
```

`PYWAGGLE_LOG_DIR` is a built-in pywaggle feature (not custom code). When set, pywaggle redirects all `plugin.publish()` to `data.ndjson` and all `plugin.upload_file()` to `uploads/` inside that directory instead of sending to Beehive. **Without it, pywaggle tries to write to `/run/waggle/uploads/` which only exists on real nodes** — on dev machines you get `PermissionError: [Errno 13] Permission denied: '/run/waggle'`. The local test runners set it automatically; when running `app.py` directly, always `export PYWAGGLE_LOG_DIR=./output/<name>` first.

**Important**: all meta dict values MUST be strings. `plugin.publish("topic", 42, meta={"count": str(n)})` — not `{"count": n}`.

For testing ML plugins, see `references/testing-patterns.md`. All tests require GPU and run real model inference — no mocked unit tests. Each plugin has a self-contained `tests/` directory with its own test file, test images, harness copy, and `run-tests.sh`. A top-level `tests/run-all-tests.sh` auto-discovers and runs all plugin tests (GPU required). Test images live in `plugins/<name>/tests/test-images/` (flat directory, committed to git). All plugins share the same set of real test images — no synthetic generation step needed.

### pluginctl deploy vs docker run: where data goes

- **`docker run` with `-e PYWAGGLE_LOG_DIR=/output`**: data stays local. `plugin.publish()` writes to `data.ndjson`, `plugin.upload_file()` writes to `uploads/` inside the mounted volume. Nothing reaches Beehive.
- **`pluginctl deploy` (no PYWAGGLE_LOG_DIR)**: data goes to the real Sage pipeline. `plugin.publish()` sends measurements via RabbitMQ → Beehive → time-series DB (queryable at `data.sagecontinuum.org`). `plugin.upload_file()` sends files to the object store (Open Storage Network, S3-compatible). This is production data flow.

Use `docker run` + `PYWAGGLE_LOG_DIR` for testing/debugging. Use `pluginctl deploy` for real deployments.

### Plugin CLI tools (on-node via SSH)
```bash
ssh waggle-dev-node-V032           # Dev nodes use V0xx format
sudo pluginctl build .             # Build Docker image from current dir
sudo pluginctl deploy -n my-counter 10.31.81.1:5000/local/my-plugin  # Deploy (use descriptive names — visible across Sage)
sudo pluginctl ps                  # List running plugins
sudo pluginctl logs <plugin-id>    # View logs (sudo required on Thor)
sudo pluginctl rm <plugin-id>      # Remove plugin
```
Note: ALL pluginctl commands require sudo on Thor (k3s kubeconfig is root-only).

### Docker base images (waggle/plugin-base on Docker Hub)
| Image tag | Use case | Size (approx) | Arch |
|-----------|----------|---------------|------|
| `1.1.1-base` | Minimal Python, no ML | ~280MB | multi-arch |
| `1.1.1-ml` | ML with CUDA | ~1.6GB arm64 / ~3.5GB amd64 | multi-arch |
| `1.1.1-ml-torch1.9.0` | PyTorch 1.9 | ~2.6GB arm64 / ~5.3GB amd64 | multi-arch |
| `1.1.1-ml-tensorflow2.3-arm64` | TensorFlow 2.3 | ~1.2GB | arm64 only |
| `1.1.1-ml-tensorflow2.3-amd64` | TensorFlow 2.3 | ~2.6GB | amd64 only |
| `1.1.1-ml-dev` | Dev/debug ML | ~1.6GB | arm64 |
| `1.1.1-ros2-foxy` | ROS2 robotics | varies | varies |

### NVIDIA base images (GPU ML plugins)

For modern ML models (YOLO 8+, BioCLIP, vLLM, transformers), use NVIDIA PyTorch images instead of waggle/plugin-base:

| Image | PyTorch | CUDA | GPU Support | Notes |
|-------|---------|------|-------------|-------|
| `nvcr.io/nvidia/pytorch:25.08-py3` | 2.8 | 13.0 | **Blackwell native: sm_110 (Thor) + sm_120/sm_121 (DGX Spark)** | **Recommended — covers both Thor and DGX Spark** |
| `nvcr.io/nvidia/pytorch:25.04-py3` | 2.7 | 12.9 | sm_120/sm_121 only — **NO sm_110** | ⚠️ Fails on Thor ("sm_110 is not compatible") |
| `nvcr.io/nvidia/pytorch:25.03-py3` | 2.7 | 12.8.1 | Blackwell sm_120 only | No Thor support |
| `nvcr.io/nvidia/pytorch:25.01-py3` | 2.6 | 12.8 | Blackwell sm_120 (first) | Minor caveats (cuSPARSELt), no Thor |
| `nvcr.io/nvidia/pytorch:24.06-py3` | 2.4 | 12.4 | **Hopper max (sm_90)** | ⚠️ **WRONG for Blackwell** — silently falls back to CPU |
| `nvcr.io/nvidia/l4t-pytorch:*` | varies | varies | Jetson-specific | ARM64 only |

**CRITICAL**: On Blackwell GPUs, using `24.06-py3` causes PyTorch to silently fall back to CPU — inference appears to hang (extremely slow). On Thor nodes specifically, `25.04-py3` also fails (no sm_110 cubins). Always use `25.08-py3` or newer for any deployment targeting both DGX Spark and Thor. The 25.08 image requires driver R575+ (DGX Spark: 580.159, Thor: 580.00 — both compatible).

All NGC PyTorch containers are multi-arch (AMD64 + ARM64 SBSA) via manifests — `docker pull` auto-selects the right architecture. The `pytorch/pytorch:*` Docker Hub images are AMD64-only (no ARM64).

Pre-download model weights at build time to **explicit paths** (edge nodes may lack internet). Use `curl -L -o /app/models/<name>.pt <url>` for YOLO, `huggingface-cli download` for HF models. Do NOT rely on ultralytics auto-download (caches to `~/.config/Ultralytics/` — path changes between versions). Set `TRANSFORMERS_OFFLINE=1` and `HF_DATASETS_OFFLINE=1` in Dockerfile. See `references/ml-plugin-patterns.md` for baking patterns and the yolov7-fire ECR reference.

### "Further Reading" appendix pattern
Each plugin's overview.md should end with a "Further Reading" appendix that helps students go beyond the plugin's scope. Topics to cover:
1. **Custom-trained models** — how to fine-tune on domain-specific data and deploy with `--model custom.pt`
2. **Temporal analysis** — the plugin's limitations (single-frame, no tracking) and how the library supports tracking/temporal features
3. **Other tasks** — table of the library's task modes (detect, segment, pose, classify) with use cases, even though the plugin only uses one
4. **Relevant blog posts / papers** — links to upstream vendor articles showing real-world applications in the plugin's domain

This is especially important for student-facing docs. The plugin demonstrates one use case; the appendix shows the frontier.

### Design principle: self-contained teaching units
Each plugin should be independently explorable by a student. A student can copy any single plugin directory out of the monorepo and have everything needed to understand, test, and deploy it: app code, Dockerfile, metadata, documentation, job specs, and tests. Shared infrastructure (venv, top-level test runner) is the exception, not the rule. When in doubt about where a file belongs, put it inside the plugin directory.

### Design principle: no cross-plugin dependencies for ECR
Each plugin is submitted to ECR as an independent entry. Verify before submission: (1) app.py imports only stdlib + pip packages, no sibling plugin imports, (2) Dockerfile COPYs only requirements.txt and app.py from its own directory, (3) no relative paths reaching into other plugin dirs, (4) test_harness.py is copied (not symlinked) into each plugin's tests/ dir. Run `grep -rn 'other-plugin-name' plugins/this-plugin/` to verify.

### Build pipeline (Makefile)
Each standalone plugin repo should have a Makefile with at minimum:
```makefile
IMAGE   := plugin-name
VERSION := 0.1.0
TAG     := $(IMAGE):$(VERSION)

build:    docker build -t $(TAG) .
test:     build test-docker      # default target: build + validate
test-docker:  bash tests/run-tests.sh --docker
test-native:  bash tests/run-tests.sh
clean:    docker rmi $(TAG) 2>/dev/null || true
```
`make test` is the single command for build + validate. `make help` with self-documenting `## comment` targets. Exit code 0/1 for CI integration. NOTE: no `audio:` or `download:` targets — all test assets (images AND audio) must be committed to git. No runtime downloads.

### Standalone repo structure (proven pattern for ECR)
Each plugin repo should match this layout:
```
sage-<plugin>/
├── app.py                 — main application
├── Dockerfile             — NVIDIA base, pip constraints, model bake, patch scripts
├── DOCKER-BUILD.md        — build, test, deploy, ECR submission guide
├── DEPLOY-AND-RUN.md      — pluginctl one-shot test + sesctl scheduled deployment guide
├── THOR-TESTING.md        — quick start for Thor node testing
├── requirements.txt       — pip dependencies
├── sage.yaml              — ECR metadata, inputs, version
├── overview.md            — pedantic tutorial-style documentation
├── .gitignore             — tests/output/, output/, *.pt, __pycache__, ._*, .DS_Store
├── .dockerignore          — tests/, ecr-meta/, jobs/, *.md, .git/
├── patch_pybioclip.py     — (BioCLIP only) pybioclip monkey-patch
├── ecr-meta/              — ECR submission materials (6 files)
├── jobs/                  — per-plugin job YAMLs
└── tests/
    ├── run-tests.sh       — standalone test runner (no monorepo deps)
    ├── test_<name>_local.py — real GPU inference test
    ├── test_harness.py    — test utilities (copied, not shared)
    ├── test-images/       — committed test images
    └── output/            — gitignored test output
```
`run-tests.sh` must work standalone — no references to monorepo venv paths or parent directories. The test script should use the system Python or a local venv, not assume `../../tests/.venv` exists.

### Template repos
- `waggle-sensor/edge-app-template`
- `waggle-sensor/cookiecutter-sage-app`

## Container Runtime & Scheduling Model

Sage plugins follow a **one-shot execution model**: the scheduler fires a container, it processes, publishes, and exits. Pods are ephemeral — no persistent filesystem between runs. One-shot cron is standard; continuous pods are the exception (see `references/job-scheduling-and-liveness.md`). Publish a heartbeat every cycle or quiet jobs look dead. arm64/Thor: portal build crashes (QEMU), push denied — build local+sideload, see `references/ecr-arm64-thor-deployment.md`. Three scheduling modes:

| Mode | YAML | Use case |
|------|------|----------|
| Cronjob | `schedule: "*/10 * * * *"` | Most common — periodic sampling |
<!-- Scheduling debug + Reolink/sesctl gotchas: references/job-scheduling-and-debugging.md -->

| Lambda | `when: {name: ..., cond: ...}` | Data-driven triggers |
| Always | `schedule: "always"` | Continuous (rare, discouraged for GPU) |

k3s + containerd cache Docker image layers locally after first pull. Two plugins sharing the same base image (e.g. both on `nvcr.io/nvidia/pytorch:24.06-py3`) only download unique layers for the second one. **Always use explicit version tags**, never `:latest` — with `:latest`, every cron tick triggers a registry check.

**Dockerfile layer ordering matters**: place rarely-changing layers (base, requirements, model weights) BEFORE frequently-changing layers (app.py). Changing a layer invalidates everything below it. Put `COPY app.py /app/` as the LAST layer so code changes don't trigger model re-downloads.

See `references/runtime-packaging-patterns.md` for full details: pod lifecycle timeline, containerd caching mechanics, imagePullPolicy defaults, cold-start optimization checklist, and analysis of 4 production reference plugins.

## Job Scheduling (sesctl)

**Official docs:**
- Sage reference: <https://sagecontinuum.org/docs/reference-guides/sesctl>
- edge-scheduler tutorials: <https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/sesctl>
- Camp notes (CLI flag reality + ECR catalog gate): `references/sesctl-ecr-validation.md`

### Science rule syntax
Format: `action : condition`

**Actions:**
1. `schedule(image)` — run a plugin container
2. `publish(topic, value)` — publish a message
3. `set(variable, value=X)` — set a variable

**Condition functions:**
1. `v(measurement, sensor=, since="-1h")` — get measurement value
2. `time(unit)` — current time ("hour", "minute", etc.)
3. `cronjob(name, crontab)` — cron schedule (name must be unique per job)
4. `after(name, since="-1d")` — true after a named event
5. `rate(measurement, since, window, unit)` — rate of change

Example rules:
```
schedule(object-counter): cronjob('run-counter', '*/5 * * * *')
schedule(object-counter): v('env.temperature') > 30.0
```

### Job YAML (see templates/job.yaml for full example)

### sesctl CLI
```bash
export SES_HOST=https://es.sagecontinuum.org
export SES_USER_TOKEN=<token-from-portal>
sesctl create -f job.yaml      # flag is -f/--file-path, NOT --from-file; returns numeric job ID
sesctl stat                    # list jobs; sesctl stat -j <id> for one
sesctl submit -j <job-id>      # submit/activate by numeric ID, NOT by name
sesctl rm -j <job-id>          # remove by ID
```
**See `references/job-scheduling-and-liveness.md`** for: ECR app metadata vs Docker image (both must exist for SES — two distinct failure modes), one-shot cron vs continuous pods, pod namespace meaning (default=pluginctl, ses=scheduler), heartbeat/observability pattern, sesctl flag corrections, sage.yaml float type reality, avian-diversity-monitoring baseline schedules, and BioCLIP cold-start considerations.

`create` returns a numeric ID; capture it. Always run `sesctl <subcmd> --help` — this CLI's surface drifts from the published web docs.

> **Deployment model, namespace diagnostics, ECR gate, reading job schedules:**
> see `references/deployment-and-diagnostics.md`. Quick diagnostics:
> pods in the `ses` namespace = scheduler-launched (official); `default`
> namespace = hand-deployed via pluginctl (a `default` pod with multi-day uptime
> is a continuous test pod, NOT a scheduled job). `sesctl submit` requires the
> app to be registered in the ECR **catalog** (portal build) even though
> `pluginctl`/docker pull succeed without it — hence `400 ... does not exist in
> ECR` on submit. Most Sage jobs are cron one-shot, not long-running; weigh
> cold-start vs warm-pod before choosing `--continuous Y`.
> **Reolink audio auth** (BirdNET etc.): FLV/BCS needs creds as query params
cron-job liveness checks — see `references/job-scheduling-and-liveness.md`.**

## Data Access (timeseries)

Scalar / event data from Sage plugins lands in Beehive and is queried at:

**`POST https://data.sagecontinuum.org/api/v1/query`** (public, no auth) → **NDJSON**.

Full patterns: **`references/timeseries-data-query-api.md`**. Tutorial: [Access and use data](https://sagecontinuum.org/docs/tutorials/accessing-data).

### Example — recent samples from `plugin-iio`

```bash
curl https://data.sagecontinuum.org/api/v1/query \
  -d '{"start":"-30m","filter":{"plugin":".*plugin-iio.*"}}'
```

```python
import sage_data_client

df = sage_data_client.query(
    start="-30m",
    filter={
        "plugin": ".*plugin-iio.*",
    },
)
```

### By node / measurement

```python
import sage_data_client

df = sage_data_client.query(
    start="-1h",
    filter={"name": "env.temperature", "vsn": "W030"}
)
# Returns pandas DataFrame with: timestamp, name, value, meta (sensor, vsn, node, plugin)
```

```bash
curl -s -X POST https://data.sagecontinuum.org/api/v1/query -d '
{
  "start": "-1h",
  "filter": {
    "vsn": "H00F",
    "name": "env.count.*"
  }
}'
```

Filters: `name` (measurement), `sensor` (hardware), `vsn` (node ID), `plugin` (source plugin). Supports wildcards / regex (e.g. `".*plugin-iio.*"`).

Large files (images, audio): stored on Open Storage Network (S3-compatible object store), not in the timeseries DB.

## Triggers

- **Cloud-to-edge**: data arrival in Beehive triggers edge job (Lambda Triggers)
- **Edge-to-cloud**: edge data triggers HPC/cloud compute via sage-data-client polling
- **External notifications (Slack, email, etc.)**: run a watcher script externally that polls the data API and reacts. Containers on Sage nodes are network-restricted and cannot reach external services. Host processes on some nodes (e.g. Thor via SSH) CAN reach external URLs — but the recommended pattern is a cloud-side watcher, not a host-side process. See `references/cloud-trigger-notifications.md` for the full pattern, Slack webhook + image upload examples, secret management, and reference implementations (hummingbird-watcher, wildfire-trigger, severe-weather-trigger).
- **Shareable web viz of fleet data** (public API + CORS proxy, themes, WebGL fallback): `references/sage-data-web-viz.md` · 3D globe: `references/sage-data-3d-globe-viz.md` · template: `templates/sage-cors-proxy-server.py`
- **Share a Sage knowledge bundle** (skills tap, secret scrubbing, starter README): `references/sharing-a-sage-knowledge-bundle.md`

## GitHub Organizations

- `sagecontinuum` — public repo catalog: `references/sagecontinuum-repos-index.md` (sage-data-client, sage-gui, sage-storage-*, sage-object-store, …; private skipped)
- `waggle-sensor` — public repo catalog: `references/waggle-sensor-repos-index.md`; **pywaggle SDK:** <https://github.com/waggle-sensor/pywaggle> (also waggle-edge-stack, edge-scheduler / pluginctl+sesctl, plugin-base, virtual-waggle, sage-mcp)

## Hermes Native MCP Integration

### Sage MCP (pre-wired)

Wire up the Sage MCP server as a native Hermes tool so all 29 tools are callable directly (no curl/JSON-RPC):

```bash
# Non-interactive (no auth, enable all tools):
printf 'n\nY\n' | hermes mcp add sage --url "https://mcp.sagecontinuum.org/mcp"

# Verify:
hermes mcp list
```

After adding, start a new session. Tools appear as `mcp_sage_*` (e.g. `mcp_sage_list_available_nodes`, `mcp_sage_find_plugins_for_task`). No auth needed for read-only operations (data queries, node listing, plugin search, docs). Job submission tools (`submit_sage_job`, `submit_plugin_job`) require a Bearer token configured via portal.

### GitHub MCP (optional — enable when needed)

Official server: [MCP Registry — GitHub](https://github.com/mcp/github/github-mcp-server) · remote endpoint `https://api.githubcopilot.com/mcp/`.

Shipped in profile `mcp.json` as **`github` with `enabled: false`** until you add a PAT. Setup: **`references/github-mcp-server.md`**.

```bash
hermes mcp add github --url "https://api.githubcopilot.com/mcp/"
# When prompted, use Authorization Bearer <GITHUB_PAT>
hermes mcp list
```

Use for live GitHub repos/issues/PRs (e.g. `waggle-sensor/pywaggle`). Prefer `/mcp/readonly` or a read-only PAT when you only need browse access.

### Hugging Face MCP (optional — enable when needed)

Official server: [Hugging Face MCP docs](https://huggingface.co/docs/hub/en/agents-mcp) · remote endpoint `https://huggingface.co/mcp`.

Shipped in profile `mcp.json` as **`huggingface` with `enabled: false`** until you add an HF token. Toggle tools/Spaces at [settings/mcp](https://huggingface.co/settings/mcp). Setup: **`references/huggingface-mcp-server.md`**.

```bash
hermes mcp add huggingface --url "https://huggingface.co/mcp"
# When prompted, use Authorization Bearer <HF_TOKEN>
hermes mcp list
```

Use for Hub models/datasets/Spaces/papers, HF documentation search, and Hub Jobs. Prefer Sage MCP for nodes/data; GitHub MCP for repos/PRs.

### Milvus SDK Code Helper (pre-wired)

Official helper: [milvus.io docs](https://milvus.io/docs/milvus-sdk-helper-mcp.md) · endpoint `https://sdk.milvus.io/mcp/` (header `Accept: text/event-stream`). Shipped **enabled** in `mcp.json` as `sdk-code-helper`. Setup notes: **`references/milvus-sdk-helper-mcp.md`**.

```bash
hermes mcp add sdk-code-helper --url "https://sdk.milvus.io/mcp/"
hermes mcp list
```

Use when generating vector-search code: prefer **Milvus Lite** (`pip install -U "pymilvus[milvus-lite]"`, `MilvusClient("./demo.db")`) and current `MilvusClient` APIs — not full Milvus Standalone/Docker unless the user asks.

## Working with This Project

- Project notes live at `~/AI-projects/Sage-agents/sage-agents.md` (15K+ bytes of detailed research)
- Pete Beckman leads the Sage project (Northwestern University, pete.beckman@northwestern.edu — no longer at ANL). He has deep domain expertise and works on ML plugins for Thor nodes (128GB unified memory, aarch64, GB10 Blackwell). Use his Northwestern email in all sage.yaml `authors` fields and ecr-meta credits.
- DGX Spark and Thor nodes share the same 128GB unified memory architecture — model sizing for one applies to the other
- When developing plugins, test with `virtual-waggle` (simulated node environment)
- Data API is public and unauthenticated — good for quick verification
- Node IDs look like W030, W09E, W0A0 (hex-style short codes called VSN)

## Pitfalls

Field-observed failures, grouped. Each line is the symptom plus its key command; the
full cause, fix and evidence are on the linked page — **open the page before acting**,
the one-liners are for routing only.


### Pywaggle publish/upload contracts and node location

→ `references/pitfalls-pywaggle-publishing.md`

- **pywaggle meta values MUST be strings** — `plugin.publish()` calls `valid_meta()` which enforces `isinstance(v, str)` for every meta dict value. Passing int/float meta values (e.g. → `meta={"confidence": str(score), "count": str(n)}`
- **pywaggle topic names MUST be `[a-z0-9_]` joined by dots** — YOLO COCO classes include multi-word names with spaces (`dining table`, `traffic light`, `potted plant`, `hot dog`, `fire hydrant`, `stop sign` → `safe_name = cls_name.replace(" ", "_").replace("-", "_")`
- **Bare file paths fail in Docker with Camera()** — `Camera("/images/test.jpg")` inside a Docker container triggers pywaggle's named-stream lookup (no `://` scheme) → → `. On the host (not in Docker), bare paths work because `
- **pywaggle upload_file may move (not copy) the temp file** — After `plugin.upload_file(tmp_path, ...)`, the file at `tmp_path` may no longer exist — pywaggle moves it to the upload directory. → `if os.path.exists(tmp_path): os.unlink(tmp_path)`
- **Meaningful upload filenames** — Use `os.path.splitext(source_name)[0]` + a suffix (`-annotated.jpg`, `-classified.jpg`, `-described.jpg`) instead of → `tempfile.NamedTemporaryFile(suffix=".jpg")`
- **Auto-detect node location from manifest** — Plugins should read `/etc/waggle/node-manifest-v2.json` for GPS coordinates when `--lat`/`--lon` are not specified.
- **Auto-detect node location for portable job configs** — When `--lat` and `--lon` are left at defaults (-1), the plugin reads `gps_lat`/`gps_lon` from `/etc/waggle/node-manifest-v2.json`.

### Pluginctl, k3s image import, sudo, and Thor GPU access

→ `references/pitfalls-pluginctl-k3s-thor.md`

- Dockerfile MUST have proper ENTRYPOINT or pluginctl will fail
- **NVIDIA Thor nodes: torch CUDA availability** — On Sage Thor nodes (NVIDIA Thor GPU, driver 580.00, CUDA 13.0), `torch.cuda.is_available()` returns False even though `torch.version.cuda` reports → `RuntimeError: No CUDA GPUs are available`
- **pluginctl requires sudo (ALL commands including logs)** — k3s kubeconfig at `/etc/rancher/k3s/k3s.yaml` is root-only. ALL pluginctl commands require sudo on Thor: `sudo pluginctl build .`, …
- **pluginctl deploy "Forbidden: pod updates may not change fields other than image"** — When a plugin pod with the same `-n <name>` already exists, `pluginctl deploy` tries to *patch* the running pod in place. → `sudo kubectl delete pod <name> --grace-period=0 --force`
- **pluginctl deploy requires --resource for GPU plugins** — The default k3s memory limits are too low for YOLO11x and similar large models. → `sudo kubectl get pod <name> -o jsonpath='{.status.containerStatuses[0].state}'`
- **pluginctl deploy with local Docker images on Thor** — After `sudo docker build -t name:tag .`, import into k3s with `sudo docker save name:tag | sudo k3s ctr images import -`, then deploy with → `sudo pluginctl deploy -n job-name docker.io/library/name:tag -- --args`
- **k3s image import required for local testing** — Docker images built on-node are NOT automatically visible to k3s/pluginctl. → `sudo docker save IMAGE:TAG | sudo k3s ctr images import -`
- **k3s image update requires reimport** — After `docker build`, the k3s containerd cache still has the OLD image. → `sudo docker save IMAGE:TAG | sudo k3s ctr images import -`

### ECR build/submit model and version rules

→ `references/pitfalls-ecr-submission.md`

- **Naming rules are strict** — repo names = lowercase alphanumeric + hyphens only (NO underscores); job names = lowercase letters, numbers, hyphens only (no underscores, uppercase …
- **Version immutability** — cannot resubmit same version to ECR — bump version every time
- **Bulk version bumps in monorepos** — when bumping versions (e.g. `0.1.0` → `0.2.0`) across sage.yaml, job YAMLs, Dockerfiles, and docs, skip generic tutorial/example files that use the → `docs/sage-runtime-packaging-tutorial.md`
- **ECR multi-arch arm64 build fails with NVIDIA base images (QEMU)** — ECR Jenkins builds both `linux/amd64` and `linux/arm64` from sage.yaml's `source.architectures`. → ` step (first step that imports torch). **Fix options**: (1) Remove `
- **ECR is NOT a Docker registry you push to** — Sage ECR pulls source from your public GitHub repo and builds the image. → `references/sesctl-ecr-validation.md`

### Sage data/manifest APIs, portal auth, NRP storage and the upload agent

→ `references/pitfalls-data-and-storage.md`

- Manifests collection needs trailing slash (`/manifests/`); single node is `/manifests/<vsn>` (slash optional). → `references/auth-api-manifests-and-nodes.md`
- Data API uses NDJSON (newline-delimited JSON), not standard JSON array
- Portal can be slow/timeout — prefer API endpoints for programmatic access.
- sage-data-client returns pandas DataFrames — ensure pandas is installed
- **Protected data access requires `-L` (follow redirects)** — `curl -L -u <username>:<portal-access-token> -o output.jpg <url>` — token from portal account page. → `, curl gets an empty 302 response and writes a 0-byte file. Always use `
- **Sage portal username for storage auth** — Use the portal username (e.g. "beckman"), not GitHub username. Token from `portal.sagecontinuum.org/account/access`. → `curl -u <portal-username>:<access-token>`
- **Upload agent clears files almost instantly** — The `wes-upload-agent` pod scans `/media/plugin-data/uploads/<job>/<plugin>/<version>/` on the host, rsyncs to `beehive-uploads.sagecontinuum.org` …
- **NRP storage (nrdstor.nationalresearchplatform.org) can lag or break globally** — Beehive receives uploads fine but the Beehive-to-NRP sync can fail globally. → `dig nrdstor.nationalresearchplatform.org`
- **NRP storage has propagation delays or outages** — Files uploaded from edge nodes may 404 on NRP storage even though the Sage data API shows the upload record. → `hostPath: /media/plugin-data/uploads/<job>/<plugin>/<version>/`

### Docker/NVIDIA base images, runtimes, and pinning

→ `references/pitfalls-docker-nvidia-images.md`

- Plugin base images are multi-arch but verify ARM64 vs x86 for target node
- **Never commit `.pt` / `.safetensors` model weights to git** — Model weight files (e.g. `yolo11x.pt`, 110MB) get auto-downloaded by libraries like ultralytics into the working directory. → `*.pt *.pth *.bin *.safetensors`
- **Patching pip-installed packages in Dockerfile** — When monkey-patching a pip-installed library (e.g. pybioclip), the source files are NOT where you'd expect from an editable install. → `/usr/local/lib/python3.12/dist-packages/bioclip/predict.py`
- **Multi-line Python in Dockerfile RUN breaks the parser** — `RUN python3 -c "import foo\\nbar()"` with actual newlines causes `unknown instruction: IMPORT` errors — Docker interprets each line as a Dockerfile …
- **Docker test output lands in project root `output/`** — When running `docker run` with `-e PYWAGGLE_LOG_DIR=/output -v $(pwd)/output/yolo-docker-test:/output`, output goes to `<repo>/output/` not …
- **Thor/Sage nodes have no outbound internet from containers** — Most Sage edge nodes are firewalled — `docker build` with `pip install` fails with DNS resolution errors. → `curl -s https://pypi.org > /dev/null`
- **NVIDIA Container Toolkit: installed ≠ configured** — On dev machines (DGX Spark, personal workstations), the `nvidia-container-toolkit` package may be installed but Docker doesn't know about the → `. Thor nodes have this pre-configured by Sage. See `
- **`--runtime=nvidia` not `--gpus all` for portable Docker commands** — Thor nodes use an older NVIDIA Container Runtime Hook that does NOT support `--gpus all` — it errors with → `. DGX Spark supports both flags. Always use `
- **OpenCV/numpy conflict in NVIDIA base images** — The NVIDIA base image ships its own opencv compiled against a specific numpy. → `ImportError: numpy.core.multiarray failed to import`
- **pip install overwrites NVIDIA base image packages (CRITICAL)** — When `requirements.txt` lists `torch>=2.0.0`, `numpy>=1.24.0`, or `ultralytics` (which depends on all of them), pip replaces the base image's → `RuntimeError: GET was unable to find an engine to execute this computation`
- **NVIDIA base image sm_xx / Blackwell compatibility** — DGX Spark (GB10) is sm_121 (CC 12.1). Thor (NVIDIA Thor / Jetson Thor) is sm_110 (CC 11.0). → `sm_80 sm_86 sm_90 sm_100 sm_120`
- **Ultralytics auto-downloads model weights when run outside Docker** — When running `python3 app.py` directly on a node (not in the Docker container), Ultralytics will download model weights (e.g.

### BioCLIP/YOLO/vLLM model behavior, thresholds and memory

→ `references/pitfalls-ml-models-inference.md`

- **BioCLIP classifies every frame — always produces a prediction** — Unlike YOLO (which only reports when it detects something), BioCLIP's `TreeOfLifeClassifier.predict()` always returns ranked predictions with scores …
- **Low-confidence images: upload only in test mode** — For classification plugins (BioCLIP), only upload annotated images when confidence exceeds threshold in production (camera/snapshot-url mode). → `scale = max(0.5, min(w, h) / 1000.0)`
- **Prefer pybioclip over raw open_clip for BioCLIP plugins** — `pybioclip>=2.1.5` provides `TreeOfLifeClassifier` that handles model loading, taxonomy, and text embeddings automatically. → `hf-hub:imageomics/bioclip-2.5-vith14`
- **Production vs test image upload behavior** — Classification plugins (BioCLIP) should only upload annotated images when confidence exceeds `--min-confidence` threshold in production mode → `if using_image_dir:`
- **BioCLIP model upgrade path (2 → 2.5 → future)** — Upgrading BioCLIP versions requires: (1) change `--model` default in app.py, (2) update the `TreeOfLifeClassifier(model_str=...)` line in → `docker run --entrypoint python3 <image> -c "import bioclip._constants; ..."`
- **vLLM model download can be huge** — Qwen3-VL-32B-Instruct is ~67GB. Budget 10-15 min for first download. Use `--trust-remote-code` for Qwen models. Use non-default port (e.g.
- **vLLM 0.23.0 CLI breaking change** — `--disable-log-requests` was removed; use `--no-enable-log-requests`. → `). When upgrading vLLM, run `
- **Redirect vLLM server output to a log file** — When launching vLLM as a subprocess, send stdout/stderr to DEVNULL (or a log file) instead of `subprocess.PIPE`.
- **Unified memory GPU fraction ≠ discrete GPU** — On 128GB unified memory nodes (DGX Spark, Thor, Grace Hopper), vLLM reports ~121 GiB total but the OS shares the pool. → `--gpu-memory-utilization 0.58`
- **`--enforce-eager` required for large models on unified memory** — CUDA graph capture consumes ~5GB extra memory. For 32B+ models on 128GB unified memory, this causes OOM even at conservative GPU fractions. → `--enforce-eager`

### Reolink/M16 capture, BirdNET behavior and audio test data

→ `references/pitfalls-cameras-and-audio.md`

- **Reolink HTTP snapshot: always request low-res for inference** — The Reolink CGI API returns full 4K (3840x2160, ~445KB) by default. → `&width=640&height=360`
- **Reolink FLV/BCS auth: query params, NOT basic auth (ffmpeg exit 187)** — The Reolink BCS/FLV endpoint (`/flv?port=1935&app=bcs&stream=...`) does NOT accept HTTP basic auth in the URL (`http://user:pass@ip/...`). → ` triggers bash history expansion under double quotes (and `
- **BirdNET does NOT normalize input amplitude — faint audio scores low** — Verified from BirdNET-Analyzer `audio.py` source: BirdNET preserves whatever amplitude is in the file (librosa loads to [-1,1] but does not → `references/reolink-audio-capture.md`
- **Expose ALL model parameters for audio plugins too** — The BirdNET V2.4 `model.predict()` API has parameters beyond the obvious (`top_k`, `min_confidence`): `bandpass_fmin` / `bandpass_fmax` (frequency → `inspect.signature(model.predict)`
- **Recommended M16 deployment command** — (30s audio every 10 min, 0.60 threshold, auto geo-filtering): → `references/node-gps-location-resolution.md`
- **Xavier NX (W nodes) compatibility** — BirdNET V2.4 plugin runs on Xavier NX (Wild Sage W-series nodes). → `python3 app.py --duration 30 --min-confidence 0.50`
- **0.60 confidence threshold for camera audio** — The M16's pcm_alaw 8 KHz (4 KHz Nyquist) produces a noise floor around 0.39 with false positives for geographically impossible species (Sunda …
- **Audio plugin tests must validate species + confidence, not just "runs"** — Pete requires tests that check (1) the top-1 species matches expected, and (2) confidence is within ±5% of reference values. → `write_header = not os.path.exists(output_path)`
- **Xeno-Canto API v3 requires an API key** — The v2 API (`/api/2/recordings`) is gone — returns 404 with "Xeno-canto API v2 is no longer available." The v3 API (`/api/3/recordings`) requires a → `. For test audio without an API key, use BirdNET's official test data repo (`
- **WAV→MP3 conversion can change top-1 species** — When converting test audio from WAV to MP3 (to reduce repo size), MP3 compression artifacts can shift confidence scores enough to flip which species → `generate_manifest.py`
- **Test audio must match deployment geography** — If the model covers North American species, test with North American bird recordings only.

### Pytest layout, CLI mode coverage, and local/dev-machine traps

→ `references/pitfalls-testing-and-local-dev.md`

- **`test_harness.py` is a library, not a test** — When writing test discovery scripts (like `run-all-tests.sh`), exclude `test_harness.py` from the glob `test_*.py`. → `find . -name "test_*_unit.py"`
- **pytest namespace collision across plugins** — Multiple plugins each have `tests/test_harness.py`. pytest's default import mode (`prepend`) treats them as the same module — the second import → `[tool.pytest.ini_options] import_mode = "importlib"`
- **Don't import plugin app.py in unit tests if it has torch/CUDA deps** — mocking `torch` via `sys.modules` poisons `numpy` (reimport fails with "cannot load module more than once"). → `references/testing-patterns.md`
- **`--continuous N` breaks `--image-dir` batch mode** — The common main-loop pattern `if args.continuous != "Y": break` fires after the FIRST image even in `--image-dir` mode, so only one file gets → `if args.continuous != "Y" and not using_image_dir: break`
- **Always test `--image-dir` and `--stream` modes separately** — Plugin app.py files typically have multiple input modes (single image, directory glob, camera stream). → ` without importing it if the initial development only tested `
- **opencv-python-headless for edge plugins** — Always use `opencv-python-headless` in requirements.txt for edge plugins (no GUI on nodes).
- **macOS `._` resource fork files break cv2.imread** — When test images are copied via macOS Finder or Samba, `._*` resource fork files appear alongside each image. These have valid image extensions (e.g. → ` to prevent committing them. The files keep coming back via Samba — add `
- **Samba over Tailscale for remote file browsing** — To mount a node's filesystem on a Mac (Finder Cmd+K), install Samba on the node. → `hosts allow = 100.64.0.0/10 127.0.0.1`
- **`clean.sh` for pre-transfer cleanup** — The repo includes a `clean.sh` script that removes test outputs, downloaded model weights (.pt/.pth/.bin/.safetensors), `__pycache__`, macOS junk → `./clean.sh --force`
- **Unit tests vs real inference tests** — Mocked unit tests (fake detections, no GPU) provide limited value for GPU-dependent edge plugins — they only test pywaggle publish logic (topic → `--image-dir`

### Documentation surfaces that must stay in sync with code

→ `references/pitfalls-doc-surfaces.md`

- **Long tutorial/doc files can stall write_file** — When writing documentation files >~500 lines (like the runtime packaging tutorial), the tool stream can time out.
- **"Multi-stage build" terminology trap in docs** — Dockerfiles with one `FROM` are single-stage builds, even if they have multiple `RUN` steps (download model, warmup, install deps).
- **ALL documentation surfaces must be updated with every code change** — When changing CLI args, audio sources, model features, Waggle topics, or behavior, update ALL four documentation files in the same commit: (1) → `ecr-meta/ecr-science-description.md`
- **overview.md drifts from code quickly** — Line counts, argument counts, meta field lists, Dockerfile snippet ordering, and flag names in overview.md go stale as app.py evolves. → `testing.command`
- **Documentation consistency across plugins** — All plugin config tables should use the same format: `Flag | Type | Default | Description`. Test runner CLI options also get their own table.

### SSH/tmux session handling, MCP setup, and node network reach

→ `references/pitfalls-dev-workflow-and-access.md`

- **MCP add is interactive** — `hermes mcp add sage --url <url>` prompts for auth token and tool filtering. Pipe `printf 'n\nY\n'` for no-auth, enable-all-tools.
- **Tmux session transcripts** — Save to the dedicated `~/AI-projects/tmux-logs/` directory (NOT the bare `~/AI-projects/` root, NOT inside a project repo). → `). Caveat: tmux only retains what's within its `
- **Sage containers are network-restricted but host processes may not be** — Containers on edge nodes cannot reach external services (Slack, email APIs, etc.). Host processes via SSH on some nodes (e.g. → `references/cloud-trigger-notifications.md`
- **SSH ControlPersist + ProxyJump + passphrase key = frequent disconnects** — When SSH config uses `ControlPersist 10m` on the jump host (sage-vpn) and a passphrase-protected `IdentityFile`, connections through `ProxyJump` → `cp ~/.ssh/config ~/.ssh/config.old`

### Credential hygiene, cron safety, and Slack notification delivery

→ `references/pitfalls-secrets-and-notifications.md`

- **Email cron job must NEVER auto-reply** — The email checking cron job must be read-only — list inbox, read unread messages, mark as seen, summarize. → `himalaya flag add -a sage <ID> seen`
- **Slack incoming webhooks cannot upload files** — Webhooks accept JSON text/blocks only. To post images to Slack, use a Slack Bot Token with `slack_sdk` (`pip install slack_sdk`) and → `references/cloud-trigger-notifications.md`
- **Credential hygiene in job YAMLs** — Never commit camera passwords or credentials to git. Use placeholders like `CAMERA_URL_HERE` in committed job YAMLs and pass actual credentials at → `git filter-repo --replace-text replacements.txt --force`

## ECR Readiness Checklist

Before submitting a plugin, verify each item:

1. **Code**: `app.py --help` shows all flags with defaults and descriptions. Third-party library params exposed (not hardcoded). Class names sanitized for pywaggle topics.
2. **Dockerfile**: Base image supports target GPU architecture (25.08-py3 for both DGX Spark sm_121 + Thor sm_110, see NVIDIA base images table). Pip constraints file freezes torch+torchvision+numpy. Model weights baked in (no runtime download). Layer ordering correct (deps → opencv fix → model → app.py). Proper ENTRYPOINT (`python3` not `python` for 3.12+ images). OpenCV headless fix present (uninstall + rm + reinstall). Use `--no-cache` on first build to avoid stale layers.
3. **sage.yaml**: `source.url` and `homepage` point to the ACTUAL repo (not a placeholder like `waggle-sensor/plugin-<name>`). `inputs:` lists every argparse flag. `inputs` types are only `string` or `int` (no `bool` — use `string` for store_true flags). `testing.command` points to the current test file. Fields (`authors`, `collaborators`, `funding`, `license`, `keywords`) match `ecr-meta/` files.
4. **ecr-meta/**: All 6 files present — `ecr-icon.jpg` (512×512), `ecr-science-image.jpg` (1920×1080+), `ecr-science-description.md`, `ecr-credits-license.txt`, `ecr-project-keywords.txt`, `ecr-project-url.txt`.
5. **Tests**: Real GPU inference test passes. Test images committed (not gitignored).
6. **overview.md**: Config table matches argparse exactly. No stale test file references. File tree matches actual directory layout (no duplicates).
7. **Job YAML**: Model name matches Dockerfile baked model (or has a comment explaining the difference).

**Common ECR submission trap**: sage.yaml `source.url` and `homepage` often contain placeholder URLs from initial scaffolding (e.g. `github.com/waggle-sensor/plugin-<name>`) that point to repos that don't exist. `ecr-project-url.txt` sometimes points to `sagecontinuum.org` instead of the actual GitHub repo. Always verify these resolve and point to the real repo.

- **ECR requires one repo per plugin**: ECR pulls from a GitHub repo and expects `sage.yaml` + `Dockerfile` at the repo root. A monorepo with multiple plugins under `plugins/<name>/` does NOT work — ECR cannot target a subdirectory. Each plugin must be a separate public GitHub repo. When splitting: copy the plugin directory contents to the repo root (not into a subdirectory), add a `.gitignore` (test output, model weights, __pycache__, macOS junk), and update `source.url` in sage.yaml to point to the new repo.
- **Per-plugin repo structure must be consistent**: Every standalone plugin repo (sage-yolo, sage-bioclip, sage-vllm) should have the same structure: `app.py`, `Dockerfile`, `.dockerignore`, `.gitignore`, `requirements.txt`, `sage.yaml`, `overview.md`, `DOCKER-BUILD.md`, `THOR-TESTING.md`, `patch_pybioclip.py` (BioCLIP only), `ecr-meta/` (6 files), `jobs/` (job YAML), `tests/` (run-tests.sh, test script, test_harness.py, test-images/). Test output goes ONLY in `tests/output/` (gitignored). Ad-hoc Docker test runs should NOT create a top-level `output/` directory — use `tests/output/` or a temp directory outside the repo. The `tests/run-tests.sh` must work standalone (no monorepo venv path dependency). Tag releases before major upgrades (`git tag v<version>`).

**sage.yaml `inputs` types: only `string` and `int`**: The ECR spec does not support `type: "bool"` or `type: "float"`. Official Sage plugins (e.g. image-sampler) only use `string` and `int`. For argparse `store_true` flags (like `--half`, `--augment`, `--agnostic-nms`), use `type: "string"` and note in the description that it's a presence-only flag: `"Flag (no value needed). Include '--half' in args to enable."` For float parameters (like `--min-confidence 0.1`), use `type: "string"` and document the expected format in the description. In job YAML `args:`, these are just bare strings with no value: `- "--half"`.

**sage.yaml must stay consistent with ecr-meta files**: The `authors`, `collaborators`, `funding`, and `license` fields in sage.yaml should match `ecr-meta/ecr-credits-license.txt`. The `keywords` should match `ecr-meta/ecr-project-keywords.txt` (one keyword per line in the file, comma-separated in sage.yaml). The `homepage` should match `ecr-meta/ecr-project-url.txt`. When updating ecr-meta files, always update sage.yaml to match and vice versa.

## ECR Submission Structure (Proven)

Each plugin needs these files in `ecr-meta/` for ECR portal submission:

| File | Required | Content |
|------|----------|---------|
| `ecr-science-description.md` | Yes | Markdown narrative: what it does, why it matters, methodology |
| `ecr-credits-license.txt` | Yes | Authors, funding acknowledgment (NSF 1935984), license (BSD-3) |
| `ecr-project-keywords.txt` | Yes | One keyword per line, ontology-aligned where possible |
| `ecr-project-url.txt` | Yes | Single line: GitHub repo URL |
| `ecr-icon.jpg` | Yes | 512x512 plugin icon (see `references/ecr-image-generation.md`) |
| `ecr-science-image.jpg` | Yes | 1920x1080+ representative science image (see `references/ecr-image-generation.md`) |
| `README` | Helpful | Submission instructions for the developer |

sage.yaml enhanced format (proven working): add `description` field to each input, `resources` section (GPU, memory, architecture), `testing` section (local testing commands), `collaborators` list, `funding` acknowledgment.

Docker image naming: `registry.sagecontinuum.org/<user>/<plugin-name>:<version>`

**IMPORTANT**: You do NOT `docker push` to `registry.sagecontinuum.org`. ECR is a CI/CD system that pulls from your public GitHub repo and builds for you. Register at portal.sagecontinuum.org → My Apps → Create App → enter repo URL. See `references/docker-build-deploy.md` for the full workflow. **ECR BUILDER BROKEN (2026-07):** every `RUN` step fails at runc init (`can't mask dir /proc/acpi`, from the CVE-2025-31133 runc upgrade) — base-swap does NOT fix it, it's builder infra. Check `~/AI-projects/Infra-problems-to-fix.md` FIRST before diagnosing any Sage build/deploy failure. Workaround: podman on-node + `pluginctl` side-load. Full detail: `references/ecr-builder-proc-acpi-runc-bug.md`.

## See Also

- **`references/duckdb-docs-index.md`** — catalog of [DuckDB docs (current)](https://duckdb.org/docs/current/): title, summary, URL (fetch live for SQL/examples; high-signal Python/CLI/CSV/Parquet list at top)
- **`references/milvus-sdk-helper-mcp.md`** — Milvus SDK helper MCP; camp default **Milvus Lite** (`MilvusClient("./….db")`) not full Milvus — [MCP](https://milvus.io/docs/milvus-sdk-helper-mcp.md) · [Lite](https://milvus.io/docs/milvus_lite.md)
- **`references/huggingface-mcp-server.md`** — Hugging Face MCP remote endpoint `https://huggingface.co/mcp` ([docs](https://huggingface.co/docs/hub/en/agents-mcp)); Hermes add + HF token; tools at [settings/mcp](https://huggingface.co/settings/mcp)
- **`references/huggingface-skills-index.md`** — vendored [huggingface/skills](https://github.com/huggingface/skills) catalog (`hf-cli`, Gradio, Spaces, training, …); pin in `skills/_vendor/`
- **`references/nvidia-skills-index.md`** — vendored [NVIDIA/skills](https://github.com/NVIDIA/skills) catalog (~230 skills; camp priority `jetson-*`); pin in `skills/_vendor/` · [docs.nvidia.com/skills](https://docs.nvidia.com/skills)
- **`references/graphify-guide.md`** — **required** [Graphify](https://github.com/Graphify-Labs/graphify): query `graphify-out/` before grepping; use **`/graphify <path-to-profile>`** (+ `--update`) with **`.venv-graphify`**; unpack `graphify-baseline.tar.gz` when present
- **`references/github-mcp-server.md`** — GitHub MCP remote endpoint `https://api.githubcopilot.com/mcp/` ([registry](https://github.com/mcp/github/github-mcp-server)); Hermes add + PAT auth
- **`references/ecr-public-apps-api.md`** — `GET https://ecr.sagecontinuum.org/api/apps?public=true` to list scheduleable public ECR plugins (fields, related `/apps/<ns>/<name>` URLs)
- **`references/timeseries-data-query-api.md`** — `POST https://data.sagecontinuum.org/api/v1/query` for plugin/node timeseries (curl + `sage_data_client`; e.g. `plugin: ".*plugin-iio.*"`)
- **`references/nvidia-jetson-thor-docs-index.md`** — catalog of [Jetson Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/), [JetPack](https://developer.nvidia.com/embedded/jetpack), and [Jetson Linux Developer Guide r39.2](https://docs.nvidia.com/jetson/archives/r39.2/DeveloperGuide/): title, summary, URL (fetch live for full content; Thor-focused quick list at top)
- **`references/auth-api-manifests-and-nodes.md`** — `auth.sagecontinuum.org` manifests + `api/v-beta/nodes` (+ `/computes/`, `/sensors/`): URL, auth, field-level descriptions; source [waggle-auth-app](https://github.com/waggle-sensor/waggle-auth-app)
- **`references/sage-docs-index.md`** — catalog of every page under [sagecontinuum.org/docs](https://sagecontinuum.org/docs/getting-started): title, summary, URL (fetch live for full content)
- **`references/waggle-sensor-repos-index.md`** — catalog of **public** repos under [github.com/orgs/waggle-sensor](https://github.com/orgs/waggle-sensor/repositories): summary + URL (clone/browse for source; private repos omitted)
- **`references/sagecontinuum-repos-index.md`** — catalog of **public** repos under [github.com/orgs/sagecontinuum](https://github.com/orgs/sagecontinuum/repositories): summary + URL (private repos omitted; many edge-stack tools live under `waggle-sensor` instead)
- **`references/stack-architecture-map.md`** — end-to-end Sage/Waggle stack map (edge ↔ Beehive ↔ portal)
- **`references/pywaggle2-producer-consumer-architecture.md`** — producer/consumer plugin architecture (pywaggle2)
- **`references/frame-anchored-batch-consumers-and-watchers.md`** / **`references/frame-anchored-vs-window-pollers.md`** — frame-anchored batch consumers vs window pollers
- **`references/crop-producer-detect-classify-cascade.md`** / **`references/detect-then-crop-then-classify-cascade.md`** — detect → crop → classify cascades
- **`references/node-sideload-test-and-restore.md`** — on-node sideload test + restore workflow
- **`references/audio-plugin-multinode-testing.md`** — multi-node audio plugin testing
- **`references/wes-pod-config-and-manifest-exposure.md`** — WES pod config + manifest exposure
- **`references/git-bundle-transfer-to-node.md`** — git bundle transfer onto a node
- **`references/ecr-build-to-ses-cutover.md`** — ECR build → SES cutover
- **`references/jobspec-verification-discipline.md`** / **`references/node-access-and-job-ownership.md`** — jobspec verification + node access/ownership
- **`references/ci-handoff-doc-discipline.md`** — CI handoff / doc discipline
- **`references/external-project-edge-porting-review.md`** — reviewing external projects for edge porting
- **`references/data-query-first-report-and-history.md`** / **`references/data-viz-and-honesty.md`** — query-first reporting + viz honesty (no fabricated VSNs/data)
- **`references/sage-data-web-viz.md`** / **`references/sage-data-3d-globe-viz.md`** — shareable Sage data web / 3D globe viz
- **`references/sharing-a-sage-knowledge-bundle.md`** — packaging/sharing a Sage Hermes knowledge bundle
- **`scripts/sample_wind_history.py`** / **`scripts/sigpipe-pipefail-regression.sh`** — sample wind history helper + SIGPIPE/`pipefail` regression check
- **`templates/sage-cors-proxy-server.py`** — CORS proxy template for browser viz against the public data API
- **Edge apps (tutorial series):** <https://sagecontinuum.org/docs/category/edge-apps>
- **pluginctl:** <https://sagecontinuum.org/docs/reference-guides/pluginctl> · <https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/pluginctl>
- **sesctl:** <https://sagecontinuum.org/docs/reference-guides/sesctl> · <https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/sesctl>
- **pywaggle (plugin SDK):** <https://github.com/waggle-sensor/pywaggle> — install, Writing a plugin guide, `src/waggle` source. Skill notes on uploads/timestamps assume this package.
- Monorepo archive: https://github.com/flint-pete/sage-edge-plugins
- Per-plugin repos (required for ECR submission; each has DOCKER-BUILD.md + THOR-TESTING.md): https://github.com/flint-pete/sage-yolo, sage-bioclip (v0.3.0 = BioCLIP 2.5 Huge, v0.2.1 = BioCLIP 2), sage-vllm, birdnet, image-sampler2. birdnet = BirdNET V2.4 audio classifier (`pip install birdnet`, TFLite CPU ARM64); sources `--input`/`--camera` URL/USB mic; Reolink FLV audio uses QUERY-PARAM auth not basic; auto-detects node location+week. Detail: references/audio-plugin-debugging-birdnet.md, references/birdnet-audio-debugging-and-geofilter.md, references/reolink-audio-capture.md.
- `references/architecture-detail.md` — full architecture notes
- `references/mcp-tools.md` — Sage MCP server tools catalog
- `references/rtsp-metadata-preservation.md` — WHY the RTSP H.264/H.265 stream carries NO per-frame JPEG metadata; metadata-rich path is a SEPARATE HTTP snapshot endpoint (Reolink Snap / Hanwha SUNAPI / Mobotix still); best->floor acquisition ladder; WSN Hanwha facts. Read before "preserving metadata over RTSP."
- `references/ecr-build-proc-acpi-failure.md` — fleet-wide ECR build regression: EVERY RUN dies at runc init (`can't mask /proc/acpi`, CVE-2025-31133). Base-image-INDEPENDENT (proven) — do NOT chase a base-image fix. Workaround = podman build + pluginctl side-load.
- `references/upload-naming-metadata-and-provenance.md` — pywaggle upload naming/metadata, timestamps, JPG/EXIF provenance, event-log linking, ns-uniqueness pitfall
- `templates/plugin-app.py` — minimal sensor plugin template
- `templates/ml-plugin-app.py` — ML vision plugin template (YOLO11-style with Camera, argparse, --image-dir, --snapshot-url with fetch_snapshot(), iter_image_dir, self-describing env.count.total with classes meta, topic name sanitization, RawDescriptionHelpFormatter epilog)
- `templates/ml-plugin-Dockerfile` — Dockerfile for ML plugins (nvcr.io/nvidia/pytorch base, model baking patterns)
- `templates/sage.yaml` — complete sage.yaml with inputs section
- `templates/job.yaml` — job YAML with science rules and success criteria reference
- `scripts/query-data.py` — standalone data query script (no sage-data-client needed)
- `references/ml-plugin-patterns.md` — production ML plugin patterns: base image selection, model baking, sidecar architecture, BioCLIP/vLLM specifics, measurement topics
- `references/runtime-packaging-patterns.md` — container runtime patterns: one-shot execution model, k3s/containerd caching, imagePullPolicy, Dockerfile layer ordering, cold-start optimization, reference plugin analysis
- `references/ecr-plugin-examples.md` — real ECR plugin examples (yolov7-fire): Dockerfile patterns, model hosting options, ECR API for inspecting existing plugins
- `references/ecr-image-generation.md` — programmatic ECR icon (512×512) and science image (1920×1080) generation with Pillow: design principles, color palettes, pipeline visualization, quality checklist
- `references/testing-patterns.md` — GPU-based testing: real model inference, pywaggle local output format, test harness utilities, `--image-dir` batch mode pitfalls, meaningful upload filenames, COCO topic name sanitization, `--add-no-detect-text` feature, integration test elimination rationale
- `references/pluginctl-camp-guide.md` — camp onboarding for pluginctl on Thor: build/run/logs workflow, sudo requirement, Dockerfile rules, vs podman/sesctl
- `references/thor-host-cpu-dev-first.md` — host PyPI torch CUDA **hang** vs `/dev/nvmap` False; CPU-dev-first; GPU only in 25.08-py3 via pluginctl
- `references/plugin-verification-invariants.md` — three-way CLI/sage.yaml/docs, COPY/ENTRYPOINT, silent-zero detections, outcome≠SES, class differentiation
- `references/ml-plugin-patterns-thor-base-image.md` — Thor/Spark NVIDIA tag table (25.08-py3; not 24.06/25.04 on Thor)
- `references/agent-shell-environment.md` — the agent shell's `HOME` is rewritten into the profile dir; `~`/`$HOME` paths resolve to a non-existent tree. Use absolute paths or the student's real home; also explains cold container stores and surprise base-image re-pulls
- `references/sudo-allowlist-and-image-import.md` — camp sudo is NOPASSWD for an allowlist only (`kubectl, docker, docker-compose, runplugin, pluginctl`); `k3s` is **not** on it and the agent terminal has no TTY, so `sudo k3s ctr images import` cannot run. Working paths: `sudo pluginctl build`, or a privileged import pod via `sudo kubectl`
- `references/pluginctl-gpu-runtimeclass.md` — pluginctl never emits `runtimeClassName`, so its pods get **no GPU** even on a node labelled `resource.gpu=true`; `--privileged`/`--selector` are not substitutes. Preflight `nvidia.com/gpu` allocatable; verified by controlled A/B (CUDA False/0 devices vs True/5)
- `references/podman-cdi-gpu-passthrough.md` — `docker` is Podman on camp Thors: `--device nvidia.com/gpu=all` (CDI) works, `--runtime=nvidia` errors, and **`--gpus all` exits 0 while injecting zero devices**. Verify by counting `/dev/nvidia*`, never by exit status
- `references/thor-host-torch-hang.md` — host PyPI torch: `import torch` itself hangs in uninterruptible **D-state** on CUDA init even with `CUDA_VISIBLE_DEVICES=''`; SIGKILL will not clear it. Never import torch at **module level** — gate it inside function bodies, probe in a subprocess with a timeout
- `references/thor-conda-forge-no-sm110.md` — conda-forge/pixi torch builds carry no sm_110 kernels and die at first kernel launch on Thor; use the NVIDIA container instead
- `references/pywaggle-snapshot-channel-order.md` — `snapshot.data` is **RGB, not BGR**: `ImageSample.__init__` applies `cv2.cvtColor(..., COLOR_BGR2RGB)` on construction, so channel 0 is red. Silently colour-swaps published images if treated as raw cv2 output
- `references/pywaggle-camera-offline-dev.md` — zero-arg `Camera()` raises a misleading `TypeError: expected string or bytes-like object, got 'int'`; camp blades ship with **no camera attached** (`/dev/video*` absent). Offline development patterns
- `references/pywaggle-offnode-local-testing.md` — off-node `Plugin()` fails from a **background thread** after the constructor returns, so `try/except` around it does not catch the `socket.gaierror`. Correct local-testing pattern
- `references/node-registry-x509-trust.md` — node-local registry x509 trust failures as an ImagePullBackOff cause, and how to distinguish them from the usual suspects
- `references/pluginctl-sideload-and-node-build.md` — side-load vs SES, registry workarounds, podman import on node
- `references/direct-node-testing.md` — testing plugins directly on Thor/DGX nodes without Docker: rsync, shared venv, per-plugin run commands, unified memory pitfalls, Samba over Tailscale for Mac Finder access, clean.sh for pre-transfer cleanup
- `references/docker-build-deploy.md` — building Docker images for Blackwell nodes: base image selection (25.08-py3 for both DGX Spark sm_121 + Thor sm_110), pip constraints file (freeze torch+torchvision+numpy), OpenCV fix, --runtime=nvidia (not --gpus all), NVIDIA Container Toolkit setup, local testing, ECR portal submission, docker-save transfer, pluginctl deploy workflow (including --resource memory for OOMKilled prevention, k3s ctr images import)
- `references/camera-rtsp-patterns.md` — pywaggle Camera device resolution chain, RTSP URL formats by vendor (Reolink, Axis, Hikvision, Hanwha/Wisenet, ONVIF), HTTP snapshot API (Reolink CGI with low-res params), --snapshot-url flag for HTTP-only cameras, using RTSP with Sage plugins, troubleshooting
- `references/rtsp-vs-still-metadata-acquisition.md` — WHY RTSP H.264/H.265 has NO per-frame JPEG metadata; the metadata-preserving path is the vendor HTTP still (Reolink cmd=Snap / Hanwha SUNAPI stw-cgi / Mobotix current.jpg), NOT RTSP video. 3-case acquisition table + Hanwha XNV-8081Z/XNF-8010RV WSN camera notes + verify-before-build open items
- `references/hanwha-xnp6400rw-audio.md` — XNP-6400RW audio capture: no built-in mic, SPM-4210 I/O Box required, RTSP audio extraction with ffmpeg, alternative audio input paths for BirdNET
- `references/reolink-http-snapshot.md` — Reolink HTTP snapshot CGI API: URL format, low-res parameters (&width=640&height=360 for 38x bandwidth savings on LTE), --snapshot-url plugin flag, bandwidth estimation table
- `references/reolink-focus-control.md` — Reolink focus/zoom control via HTTP API: GetZoomFocus, StartZoomFocus (FocusPos/ZoomPos), SetAutoFocus (disable/enable), lock-focus workflow, curl examples
- `references/cloud-trigger-notifications.md` — Cloud trigger / external notification pattern: polling data API, Sage storage image download (curl -L, NRP propagation delay/outages, diagnostic steps), Slack text webhooks + image uploads (bot token + slack_sdk files_upload_v2), secret management, YOLO COCO class reference, multi-measurement watcher (bird+person+fork), BioCLIP species enrichment (query env.species.species when YOLO triggers, include species name in Slack alert), reference implementations (hummingbird-watcher, wildfire, weather)
- `references/audio-classification-models.md` — Wildlife audio classification models for edge: BirdNET V2.4 (primary), Google Perch 2.0 (alternative), BatDetect2, BattyBirdNET, AnuraSet, YAMNet, NatureLM-audio. Edge deployment matrix, ARM64 notes, plugin development guidance, test audio sources (Xeno-Canto v3 API key required, Wikimedia rate limits, geographic matching rule).
- **Never commit credentials to git**: Camera URLs with inline credentials (e.g. `http://user:pass@IP/...`) must NEVER appear in committed files — GitHub secret scanning flags them. Use placeholders (`CAMERA_URL_HERE`) in job YAMLs and docs. If credentials are accidentally committed, scrub all history with `pip install git-filter-repo && git filter-repo --replace-text replacements.txt --force && git push --force origin main`. Format: `old_string==>new_string` one per line. The `filter-repo` command removes the `origin` remote — re-add with `git remote add origin URL` then `git push --set-upstream origin main`.
- **Reolink FLV audio: always use sub-stream**: When pulling audio from a Reolink camera via HTTP FLV, use `channel0_sub.bcs` not `channel0_main.bcs`. ffmpeg receives the full FLV (video + audio) over the network before discarding video locally. Sub-stream is 640x360 H.264 (~500 kbps) vs main stream 3840x2160 H.265 (~8-15 Mbps) — 30-50x less bandwidth for identical audio. Native audio is AAC 16 kHz (8 kHz Nyquist); ffmpeg upsamples if `-ar 48000` is requested but no real information above 8 kHz. Set `--bandpass-fmax 8000`. See `references/reolink-audio-capture.md`.
- **Reolink silent audio gotcha**: The FLV stream contains an audio track header even when the camera mic is disabled in settings. ffmpeg completes without error, produces a valid WAV file — but it's pure silence (no background noise). BirdNET reports 0 detections, which looks like "no birds" but actually means "mic is off." Always listen to the raw capture first. Enable mic via API: `curl -s "http://IP:PORT/api.cgi?cmd=SetEnc&user=U&password=P" -d '[{"cmd":"SetEnc","action":0,"param":{"Enc":{"channel":0,"audio":1}}}]'`. See `references/reolink-audio-capture.md`.
- **Reolink API may require token auth (not just URL credentials)**: Short-session auth (`user=X&password=Y` in URL) works for some Reolink commands but some models/endpoints return `rspCode: -6` ("please login first"). Fall back to token auth: POST Login command, get token name, pass as `&token=TOKEN` on subsequent calls. Token expires after leaseTime (typically 3600s). See `references/reolink-focus-control.md`.
- **Preserve old CLI arg semantics when rewriting plugins**: When rewriting a plugin from scratch, compare old vs new CLI args explicitly. If the old code supported bounded recording cycles (`--num_rec 6 --silence_int 1`), the new code must too (`--num-recordings 6 --interval 1`). Dropping a capability (e.g. replacing finite `--num_rec` with infinite `--interval`) is a regression even if the new design seems cleaner. The user WILL notice.
- **Make job YAMLs portable — auto-detect node-specific values at runtime**: Plugins should auto-detect values that vary per node (lat/lon, camera IPs, sensor names) rather than hard-coding them in job YAMLs. Pattern: read from `/etc/waggle/node-manifest-v2.json` (mounted in k3s pods at `/etc/waggle/`). Available fields: `gps_lat`, `gps_lon`, `vsn`, `name`, `address`, `sensors` (array with `uri`, `hardware.hw_model`). Fall back gracefully when manifest is missing (local testing). This allows the same job YAML to deploy across multiple nodes without modification. Similarly, compute time-dependent values (week of year, season) at runtime rather than baking them into config.
- **Test audio committed to git (no runtime downloads)**: Audio test files MUST be committed to the repo (like vision plugin test images). No download-at-runtime scripts. Convert WAV→MP3 to keep size manageable (~16 MB for 9 files vs 54 MB WAV). MP3 compression may shift confidences slightly — always baseline from the committed MP3, never from originals. Use `generate_manifest.py` to rebuild `manifest.json` after conversion, then update test expectations in `run-tests.sh`. Check each file individually — some will be stable (e.g. single-species recordings at 99%+), others with close top-2 scores may flip. **CRITICAL**: when converting, verify top-1 species didn't change before deleting the WAV — if it did, either keep that file as WAV or update the test baseline to the new MP3 top-1.
- `references/camera-audio-capabilities.md` — Camera audio comparison for BirdNET: Mobotix M16 (built-in mic, best option), XNV-8081Z (audio input on body), AXIS Q6055-E (multicable), XNP-6400RW (no audio without I/O box). RTSP URLs per vendor, audio quality impact on BirdNET (16 KHz = 8 KHz Nyquist covers most passerines), test capture script, troubleshooting.
- `references/reolink-audio-capture.md` — Reolink audio for BirdNET: FLV stream over HTTP when RTSP port is unmapped (`/flv?port=1935&app=bcs&stream=channel0_sub.bcs`), use sub-stream to minimize bandwidth (640x360 vs 4K), native audio is AAC 16 kHz (8 kHz Nyquist), focus control API (StartZoomFocus with token auth), audio quality comparison table (USB > Reolink > M16).
- Sage infra issues report: `~/AI-projects/sage-infra-issues-2026-06-18.md` — 5 issues: NRP storage sync broken globally, ECR multi-arch QEMU failure, pybioclip 2.5 support missing, BioCLIP 2.5 OOM at 8Gi/16Gi, SSH agent key loss
- `references/bioclip-25-upgrade.md` — BioCLIP 2 → 2.5 Huge upgrade: model comparison table, text embeddings location, pybioclip patch procedure (string matching pitfalls), Dockerfile pattern, test results, upgrade checklist
