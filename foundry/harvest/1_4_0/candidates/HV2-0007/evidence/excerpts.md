# HV2-0007 — evidence

**snapshot.data is RGB not BGR**  ·  independence: 1 student(s)  ·  1 episode(s)

## T07 — snapshot.data is RGB, not BGR

- **Claim:** pywaggle's `Camera` defaults to `format=RGB` and `ImageSample.__init__` applies `cv2.cvtColor(data, COLOR_BGR2RGB)` on construction, so `snapshot.data[...,0]` is RED — a plugin that reasons about `snapshot.data` as if it were raw cv2 BGR publishes silently swapped R/B channels.
- kind: `correction` · confidence: high · generality: toolchain · cross-shard: False
- merged from clusters: C020
- **Baseline conflict:** reolink-http-snapshot.md:54 states 'Returns BGR numpy array, same format as Camera.snapshot().data'.
- **Notes:** Student measured it rather than asserting it: snapshot.data channel means [70.8, 116.5, 43.2] vs raw cv2 BGR [42.9, 115.9, 70.9] - channels 0 and 2 demonstrably swapped. Strongest evidence quality in the corpus.

### `node-H035-20260721_202140_e3f58b-00`
friction: retry_depth=1 failures=1 wall=241.6s resolved=True

> snapshot.data mean per channel: [ 70.83785067 116.5195262   43.16166252]
> raw cv2 BGR mean per channel:   [ 42.92750985 115.93265991  70.93280802]
> 
> If snapshot.data mean[0] > raw BGR mean[0], then channel 0 is now RED (RGB order).
