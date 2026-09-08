# Developing a camera plugin with no camera attached

**Applicability:** camp Thor blades (which ship **without** a camera) and any dev box
where `/dev/video*` does not exist.

## The camp blades have no camera

Confirmed independently on three nodes: no `/dev/video*`, empty
`v4l2-ctl --list-devices`, no `/run/waggle/data-config.json`, `"sensors": []` in the
node manifest, and no port-554 host on either node subnet. `Camera("bottom_camera")`
and friends cannot work here. This is a normal state, not a broken node — all
baseline camera guidance assumes an attached Reolink that these blades do not have.

## Failure 1 — zero-arg `Camera()` raises a type error, not a device error

```python
camera = Camera()      # as in the tutorial app
```

```
TypeError: expected string or bytes-like object, got 'int'
```

**Cause:** the default is `device=0`, an **int**, and `Camera.__init__` passes it
straight into `re.match`, which only accepts strings. The traceback points at `re`,
so it reads as a library bug rather than "no camera here". This is the single most
common first-plugin stumble.

**Fix:** always pass a device **string**.

## Failure 2 — a real device string still fails with no camera

```
RuntimeError: unable to open video capture for device 0
```

Expected on a blade with no `/dev/video*`.

## Working offline-dev pattern

```python
camera = Camera("file://example.jpg")
snapshot = camera.snapshot()
```

`file://` loads a still through the **same** `Camera → snapshot → numpy` path the
real plugin uses, and disables the background grabber daemon. That makes it a better
local test than `cv2.imread`, which bypasses the abstraction you are trying to
exercise — and bypasses the RGB conversion (see
`pywaggle-snapshot-channel-order.md`).

Also set the upload path, or `plugin.upload_file()` will fail on the root-owned
`/run/waggle`:

```bash
mkdir -p "$HOME/work/uploads"
export WAGGLE_PLUGIN_UPLOAD_PATH="$HOME/work/uploads"
```

(See `agent-shell-environment.md` — if an agent sets this, `$HOME` is not the user's
home.)

Offline, `publish()` calls succeed silently: there is no Beehive to route to. Files
stage locally and nothing ships. That is correct behaviour, not a failure.

## Related

- `pywaggle-offnode-local-testing.md` — why `try/except` around `Plugin()` does not work.
- `pywaggle-snapshot-channel-order.md` — the channel-order trap on the same object.
