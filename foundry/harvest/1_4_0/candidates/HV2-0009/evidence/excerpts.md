# HV2-0009 — evidence

**Off-node Plugin() thread failure**  ·  independence: 1 student(s)  ·  2 episode(s)

## T09 — Off-node Plugin() raises from a background thread

- **Claim:** Wrapping `Plugin()` construction in try/except does NOT make a plugin safe to run off-node: pywaggle's RabbitMQ publisher runs on a background thread, so the `socket.gaierror: [Errno -2] Name or service not known` surfaces as an unhandled traceback from `rabbitmq.py` after the constructor already returned — gate plugin init on a Sage env var (e.g. WAGGLE_PLUGIN_NAME / WAGGLE_NODE_ID) instead of on exception handling.
- kind: `failure_class` · confidence: high · generality: toolchain · cross-shard: True
- merged from clusters: C017, C039
- **Baseline conflict:** SKILL.md has a 'Local testing (no node required)' section but does not state that Plugin() raises from a daemon thread and therefore escapes try/except.
- **Notes:** Two miners found this independently via different symptoms (gaierror vs ImportError guard).

### `node-H035-20260727_024905_596214-05`
friction: retry_depth=0 failures=0 wall=321.4s resolved=False

> File "/usr/local/lib/python3.12/dist-packages/waggle/plugin/rabbitmq.py", line 47, in __connect_and_flush_messages\n    with pika.BlockingConnection(self.params) as conn, conn.channel() as ch:

### `node-H035-20260727_024905_596214-13`
friction: retry_depth=1 failures=1 wall=383.1s resolved=True

> The issue is that `waggle.plugin.Plugin()` starts a **background thread** that immediately tries to connect to RabbitMQ. The DNS resolution fails in that thread, and the exception happens there — not in our try/except block which only wraps the main-thread constructor call.
