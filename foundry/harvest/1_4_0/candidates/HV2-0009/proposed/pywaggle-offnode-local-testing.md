# `try/except` around `Plugin()` does not make a plugin off-node safe

**Applicability:** running a Waggle plugin outside a WES pod — a dev host, a laptop,
or a plain container.

## The idiom that does not work

```python
try:
    from waggle.plugin import Plugin
    plugin = Plugin()
except ImportError:
    plugin = None          # "local test mode"
```

Both halves fail for the same reason: **the error does not arrive where you are
catching it.**

- The import usually succeeds — pywaggle is installed — so `ImportError` never fires.
- `Plugin()` returns, and the failure surfaces **later, from a background thread**:

```
socket.gaierror: [Errno -2] Name or service not known
  File ".../waggle/plugin/rabbitmq.py", line 36, in __main
```

pywaggle's RabbitMQ publisher runs on its own daemon thread and resolves the broker
hostname there. Off-node that name does not resolve. A `try/except` around the
constructor cannot catch a raise on another thread — the traceback prints, the thread
dies, and the main program keeps running in a half-initialised state.

Two participants shipped this guard believing it worked.

## Working pattern — gate on the environment, not on exceptions

WES injects `WAGGLE_*` variables into every plugin pod. Their **absence** is a
reliable, synchronous signal that you are off-node:

```python
import os

ON_NODE = bool(os.environ.get("WAGGLE_PLUGIN_NAME") or os.environ.get("WAGGLE_NODE_ID"))

if ON_NODE:
    from waggle.plugin import Plugin
    plugin = Plugin()
else:
    plugin = None      # or a no-op recorder that logs what would be published
```

A small no-op shim beats `None` — it keeps call sites free of `if plugin:` and lets
you assert on what *would* have been published:

```python
class LocalPlugin:
    def publish(self, name, value, **kw):   print(f"[local] publish {name}={value} {kw}")
    def upload_file(self, path, **kw):      print(f"[local] upload {path} {kw}")
    def __enter__(self):  return self
    def __exit__(self, *a): return False
```

## Rule

Decide on-node vs off-node from **environment**, synchronously, at startup. Never
infer it from an exception — pywaggle's failures are asynchronous and will not
arrive in your handler.

## Related

- `pywaggle-camera-offline-dev.md` — the camera half of off-node development.
