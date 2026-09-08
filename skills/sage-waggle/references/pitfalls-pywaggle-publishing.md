# Pywaggle publish/upload contracts and node location

Extracted from `sage-waggle/SKILL.md` `## Pitfalls`. Each entry is a field-observed
failure and its fix. Routed from the Pitfalls index in SKILL.md.

- **pywaggle meta values MUST be strings**: `plugin.publish()` calls `valid_meta()` which enforces `isinstance(v, str)` for every meta dict value. Passing int/float meta values (e.g. `{"confidence": 0.95}`) silently raises ValueError. Always wrap: `meta={"confidence": str(score), "count": str(n)}`

- **pywaggle topic names MUST be `[a-z0-9_]` joined by dots**: YOLO COCO classes include multi-word names with spaces (`dining table`, `traffic light`, `potted plant`, `hot dog`, `fire hydrant`, `stop sign`, `tennis racket`, `cell phone`, `teddy bear`, etc.). Using these directly in `plugin.publish(f"env.count.{cls_name}", ...)` raises `ValueError: publish name invalid`. Sanitize before publishing: `safe_name = cls_name.replace(" ", "_").replace("-", "_")`. This bug is insidious — the per-class publish calls before the offending class succeed, but `env.count.total` and `upload_file()` never run for that image, making it appear to have zero detections.

- **Bare file paths fail in Docker with Camera()**: `Camera("/images/test.jpg")` inside a Docker container triggers pywaggle's named-stream lookup (no `://` scheme) → `FileNotFoundError: /run/waggle/data-config.json`. Fix: use `file://` prefix: `Camera("file:///images/test.jpg")`. On the host (not in Docker), bare paths work because `resolve_device_from_data_config` falls through to `resolve_device_from_path`. This only bites you in Docker where `/run/waggle/data-config.json` doesn't exist.

- **pywaggle upload_file may move (not copy) the temp file**: After `plugin.upload_file(tmp_path, ...)`, the file at `tmp_path` may no longer exist — pywaggle moves it to the upload directory. Guard any cleanup: `if os.path.exists(tmp_path): os.unlink(tmp_path)`.

- **Meaningful upload filenames**: Use `os.path.splitext(source_name)[0]` + a suffix (`-annotated.jpg`, `-classified.jpg`, `-described.jpg`) instead of `tempfile.NamedTemporaryFile(suffix=".jpg")`. pywaggle prepends a timestamp to the filename passed to `upload_file()`, so the final name becomes `{timestamp}-{stem}-annotated.jpg` — human-readable instead of `{timestamp}-tmpjoktpbnb.jpg`.

- **Auto-detect node location from manifest**: Plugins should read `/etc/waggle/node-manifest-v2.json` for GPS coordinates when `--lat`/`--lon` are not specified. The manifest has `gps_lat` and `gps_lon` fields. Pattern: default `--lat`/`--lon` to -1, then in `main()` call `read_node_location()` which reads the manifest and returns `(lat, lon)` or `None`. This makes job YAMLs portable across nodes — no hard-coded coordinates. Combine with `--week auto` for fully automatic geo-filtering. Fail gracefully (log "No node manifest found — geo-filtering disabled") when the manifest is absent (dev machines, `--dry-run` testing). The manifest is at `/etc/waggle/node-manifest-v2.json` on both W nodes (Xavier NX) and Thor nodes.

- **Auto-detect node location for portable job configs**: When `--lat` and `--lon` are left at defaults (-1), the plugin reads `gps_lat`/`gps_lon` from `/etc/waggle/node-manifest-v2.json`. Combined with `--week auto`, this means the same job YAML deploys to any node without hard-coding location or season. Pattern: `read_node_location()` function with try/except around manifest read, returns `None` if no manifest (graceful fallback for testing on dev machines).
