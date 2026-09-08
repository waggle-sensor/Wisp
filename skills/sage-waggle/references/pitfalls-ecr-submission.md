# ECR build/submit model and version rules

Extracted from `sage-waggle/SKILL.md` `## Pitfalls`. Each entry is a field-observed
failure and its fix. Routed from the Pitfalls index in SKILL.md.

- **Naming rules are strict**: repo names = lowercase alphanumeric + hyphens only (NO underscores); job names = lowercase letters, numbers, hyphens only (no underscores, uppercase, dots); plugin names in sage.yaml can use underscores

- **Version immutability**: cannot resubmit same version to ECR — bump version every time

- **Bulk version bumps in monorepos**: when bumping versions (e.g. `0.1.0` → `0.2.0`) across sage.yaml, job YAMLs, Dockerfiles, and docs, skip generic tutorial/example files that use the old version as a hypothetical placeholder (e.g. `docs/sage-runtime-packaging-tutorial.md` using `my-plugin:0.1.0` as a generic example). Use `replace_all=True` per-file rather than a blind global sed to avoid corrupting unrelated examples.

- **ECR multi-arch arm64 build fails with NVIDIA base images (QEMU)**: ECR Jenkins builds both `linux/amd64` and `linux/arm64` from sage.yaml's `source.architectures`. The arm64 build uses QEMU emulation on an amd64 host, which crashes (`qemu: uncaught target signal 6 (Aborted) - core dumped`) when the NVIDIA PyTorch base image tries to `import torch` during any `RUN` step. This affects ALL plugins using `nvcr.io/nvidia/pytorch:*` as base. The amd64 build succeeds fine. **Confirmed**: sage-bioclip v0.3.0 failed on ECR with this exact error at the pip constraints `RUN` step (first step that imports torch). **Fix options**: (1) Remove `linux/arm64` from sage.yaml architectures — ECR builds amd64 only, build arm64 locally on Thor/DGX Spark; (2) Ask ECR team for native arm64 builder (no QEMU); (3) Use a lighter base image for arm64 that doesn't require GPU at build time. Until fixed upstream, arm64 images must be built locally and transferred via `docker save | k3s ctr images import`.

- **ECR is NOT a Docker registry you push to**: Sage ECR pulls source from your public GitHub repo and builds the image. You do NOT run `docker login`, `docker tag`, or `docker push` against `registry.sagecontinuum.org`. The workflow is: push code to GitHub → register on portal.sagecontinuum.org → ECR builds → get registry tag from "Tags" tab. For pre-ECR testing on Thor nodes, use `docker save | gzip` + `scp` + `sudo k3s ctr images import`. **`sesctl submit` validates the image against the ECR app catalog, but `pluginctl deploy` does NOT** — a pluginctl-runnable image can still fail `sesctl submit` with `400 ... does not exist in ECR` if it was never built in the portal pipeline. See `references/docker-build-deploy.md` and `references/sesctl-ecr-validation.md`.
