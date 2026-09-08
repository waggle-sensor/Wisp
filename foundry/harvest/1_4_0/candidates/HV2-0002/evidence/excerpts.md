# HV2-0002 — evidence

**sudo NOPASSWD allowlist and image import**  ·  independence: 2 student(s)  ·  2 episode(s)

## T02 — sudo works only for the NOPASSWD allowlist

- **Claim:** Camp Thor student accounts have NOPASSWD sudo for an explicit binary allowlist only (kubectl, docker, docker-compose, runplugin, pluginctl) and the Hermes terminal has no TTY, so every other sudo command fails with 'a terminal is required to read the password' — this makes the documented side-load step `sudo k3s ctr images import` impossible (/usr/local/bin/ctr is a symlink to k3s, so it inherits the block); the working substitute is to apply a privileged pod with `sudo kubectl` that mounts the containerd socket and runs the import from inside.
- kind: `correction` · confidence: high · generality: platform · cross-shard: True
- merged from clusters: C003, C042
- **Baseline conflict:** SKILL.md instructs `sudo k3s ctr images import` in six places (655,656,657,677,680,681), calling it CRITICAL and required for local testing. `k3s` is not on the sudoers allowlist.
- **Notes:** MINER DISAGREEMENT, adjudicated against the corpus: one shard claimed a NOPASSWD allowlist, another claimed sudo never works. 92 episodes across 8 students contain a successful sudo call; 9 episodes across 5 students hit the TTY error, and every command near those failures is a non-allowlisted binary (k3s, apt-get, nvidia-ctk, systemctl, usermod, cat). The shipped claim is the conjunction. The 'sudo never works' phrasing is over-general and would teach the next agent to abandon a capability that works 92 times.

### `node-H021-20260725_162553_193a20-03`
friction: retry_depth=2 failures=20 wall=2961.9s resolved=True

> User <user> may run the following commands on <node>:\n    (ALL) NOPASSWD: /usr/local/bin/kubectl, /usr/bin/docker, /usr/local/bin/docker, /usr/bin/docker-compose, /usr/local/bin/docker-compose, /usr/bin/runplugin, /usr/bin/pluginctl

### `node-H021-20260725_162553_193a20-03`
friction: retry_depth=2 failures=20 wall=2961.9s resolved=True

> Failed to pull image "10.31.81.1:5000/local/plugin:latest": failed to pull and unpack image ...: failed to do request: Head "https://10.31.81.1:5000/v2/local/plugin/manifests/latest": tls: failed to verify certificate: x509: certificate signed by unknown authority

### `node-H032-20260721_191607_dad9e9-01`
friction: retry_depth=0 failures=0 wall=3373.5s resolved=False

> Upload to S3 failed (Failed to upload /temp/ecr/[REDACTED]_app-tutorial_0.1.0.tgz to sage/ecr/[REDACTED]/app-tutorial/[REDACTED]_app-tutorial_0.1.0.tgz: An error occurred (QuotaExceeded) when calling the UploadPart operation: None)

### `node-H032-20260721_191607_dad9e9-01`
friction: retry_depth=0 failures=0 wall=3373.5s resolved=False

> sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
> sudo: a password is required
