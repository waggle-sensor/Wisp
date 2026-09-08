# HV2-0010 — evidence

**Node-local registry x509 trust**  ·  independence: 1 student(s)  ·  2 episode(s)

## T10 — Node-local registry x509 trust failure

- **Claim:** `pluginctl build` can succeed and hand back a 10.31.81.1:5000/local/... ref that `pluginctl run` can never pull: kubelet rejects the node-local registry with x509 'certificate signed by unknown authority' even though /etc/rancher/k3s/registries.yaml names the CA and `openssl verify` of the serving cert against that CA returns 0 — i.e. containerd has not loaded the registries.yaml, and the diagnosis is that a build-succeeds/run-ImagePullBackOff pair is a registry-trust fault, not a build or image-name fault.
- kind: `failure_class` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C004, C048
- **Baseline conflict:** Baseline documents reachability and image-name causes for ImagePullBackOff; x509 appears only in control-plane diagnosis contexts, not the registry pull path.

### `node-H021-20260725_162553_193a20-03`
friction: retry_depth=2 failures=20 wall=2961.9s resolved=True

> User <user> may run the following commands on <node>:\n    (ALL) NOPASSWD: /usr/local/bin/kubectl, /usr/bin/docker, /usr/local/bin/docker, /usr/bin/docker-compose, /usr/local/bin/docker-compose, /usr/bin/runplugin, /usr/bin/pluginctl

### `node-H021-20260725_162553_193a20-03`
friction: retry_depth=2 failures=20 wall=2961.9s resolved=True

> Failed to pull image "10.31.81.1:5000/local/plugin:latest": failed to pull and unpack image ...: failed to do request: Head "https://10.31.81.1:5000/v2/local/plugin/manifests/latest": tls: failed to verify certificate: x509: certificate signed by unknown authority

### `node-H021-20260725_162553_193a20-04`
friction: retry_depth=0 failures=0 wall=151.3s resolved=False

> That's the first failed `pluginctl run` attempt from earlier — the one that hit the ImagePullBackOff on the k3s registry TLS cert issue. It exited with code 1 because the pod was GC'd after the image pull failure.
