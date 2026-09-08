# NVIDIA Skills (vendored)

Catalog of agent skills copied from [NVIDIA/skills](https://github.com/NVIDIA/skills) into this profile’s `skills/` tree. Attribution + commit pin: `skills/_vendor/nvidia-skills-SOURCE.md` (CC-BY-4.0 AND Apache-2.0). Upstream docs: [docs.nvidia.com/skills](https://docs.nvidia.com/skills).

Invoke with `/skill <name>` or `hermes -s <name>`. Browse/install upstream with `npx skills add nvidia/skills --list`.

## Camp-priority (Thor / Jetson)

| Skill area | Examples | When |
|------------|----------|------|
| **Jetson Device** | `jetson-diagnostic`, `jetson-memory-audit`, `jetson-llm-serve`, `jetson-llm-benchmark`, `jetson-inference-mem-tune`, `jetson-headless-mode`, `jetson-package`, `jetson-speculative-decoding`, `jetson-print-device-info` | Live Thor/Jetson after boot — diagnostics, VRAM, LLM serve |
| **Jetson BSP** | `jetson-quick-start`, `jetson-set-target`, `jetson-flash-image`, `jetson-download-bsp`, `jetson-customize-*`, … | BSP flash/customize (host-side image work) |
| **DeepStream / VSS** | `deepstream-dev`, `deepstream-generate-pipeline`, `vss-*` | Video analytics pipelines |
| **TAO** | `tao-list-capabilities`, `tao-train-*`, `tao-run-on-local-docker` | Vision train/export for edge |
| **cuDF / CUDA-X** | `accelerated-computing-cudf`, `dali-dynamic-mode` | GPU DataFrames / data loading |
| **Nemotron / NeMo** | `nemotron-*`, `nemo-retriever`, `launch-nemo-rl` | NVIDIA model customize / RL / retrieval |
| **RAG Blueprint** | `rag-blueprint`, `rag-eval`, `rag-perf` | RAG deploy/troubleshoot |

Sage/Waggle edge plugins still use **`sage-waggle`**. Discover skills/docs with **required Graphify** (`graphify query` / `AGENTS.md`) before grepping. For Hub models use Hugging Face skills (`hf-cli`, …). Thor docs URL index: `nvidia-jetson-thor-docs-index.md`.

## Product catalog (summary)

Full per-skill list is huge (~230 skills). Groups match upstream README:

| Product | Skill name prefix / examples |
|---------|------------------------------|
| AIQ | `aiq-research`, `aiq-deploy` |
| CUDA-Q | `cudaq-guide` |
| cuDF | `accelerated-computing-cudf` |
| cuFOLIO | `cufolio` |
| cuOpt | `cuopt-*` |
| cuPyNumeric | `cupynumeric-*` |
| DALI | `dali-dynamic-mode` |
| Data Designer | `data-designer` |
| DeepStream | `deepstream-*`, `amc-*` |
| Digital Health | `digital-health-clinical-asr-*` |
| Dynamo | `dynamo-*` |
| Earth2Studio | `earth2studio-*` |
| Holoscan SDK | `holoscan-*` |
| Holoscan Sensor Bridge | `hsb-*` |
| Jetson BSP | `jetson-build-*`, `jetson-customize-*`, `jetson-flash-*`, … |
| Jetson Device | `jetson-diagnostic`, `jetson-llm-*`, `jetson-memory-audit`, … |
| Medical AI / MONAI | `dicom-*`, `nv-segment-*`, `nv-generate-*`, … |
| Megatron-Core | `mcore-*` |
| NeMo AutoModel / MBridge / Platform / Retriever / RL | `nemo-*`, `launch-nemo-rl` |
| NemoClaw | `nemoclaw-user-guide` |
| Nemotron / Speech | `nemotron-*` |
| Physical AI / Omniverse | `omniverse-*`, `physical-ai-*` |
| PhysicsNeMo | `physicsnemo-discover` |
| RAG Blueprint | `rag-*` |
| Skill Card Generator | `skill-card-generator` |
| TAO Toolkit | `tao-*` |
| TileGym | `tilegym-*` |
| Video Search and Summarization | `vss-*` |

List installed NVIDIA skills locally:

```bash
hermes skills list | grep -E 'jetson-|deepstream-|tao-|cuopt-|nemo|dynamo-|vss-'
```

## Re-sync from upstream

See `skills/_vendor/nvidia-skills-SOURCE.md`. After re-copying, bump `distribution.yaml` version and record the new upstream commit.
