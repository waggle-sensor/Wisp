# `snapshot.data` is RGB, not BGR

**Applicability:** any plugin reading frames through pywaggle's `Camera`.

## Claim

pywaggle's `Camera` defaults to `format=RGB`, and `ImageSample.__init__` applies
`cv2.cvtColor(data, cv2.COLOR_BGR2RGB)` **on construction**. So:

```python
snapshot = camera.snapshot()
snapshot.data[..., 0]   # RED, not blue
```

Code that treats `snapshot.data` as a raw OpenCV BGR array silently swaps red and
blue — in saved images, in uploads, and in any model input built from it.

## Why it is easy to miss

There is **no error**. The pipeline runs, publishes, and looks healthy; only the
colours are wrong, and on many scenes that is not obvious by eye. Detection models
degrade quietly rather than failing.

## Measure it rather than trusting either claim

A participant settled this empirically by comparing channel means on the same frame:

```
snapshot.data mean per channel: [ 70.84  116.52   43.16 ]
raw cv2 BGR   mean per channel: [ 42.93  115.93   70.93 ]
```

Channels 0 and 2 are transposed. Reproduce with:

```python
import cv2, numpy as np
print("snapshot.data:", snapshot.data.reshape(-1, 3).mean(0))
print("raw cv2 BGR  :", cv2.imread(path).reshape(-1, 3).mean(0))
```

## Correct handling

```python
frame_rgb = snapshot.data                       # already RGB
frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

cv2.imwrite("out.jpg", frame_bgr)               # cv2 expects BGR
# PIL / most torch preprocessing expects RGB — pass frame_rgb directly
```

Rule of thumb: **convert at the boundary of the library you are calling**, and label
the variable with its order (`frame_rgb`, `frame_bgr`). Do not let an unlabelled
`frame` cross function boundaries.

## Baseline conflict

`references/reolink-http-snapshot.md` states: "Returns BGR numpy array, same format
as `Camera.snapshot().data`". The first half is right — `cv2.imdecode` of an HTTP
snapshot *is* BGR — but the equivalence to `Camera.snapshot().data` is wrong. The two
paths differ in channel order, which is exactly the trap: mixing an HTTP-snapshot
path and a `Camera` path in one plugin gives inconsistent colour with no error.
