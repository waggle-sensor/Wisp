# HV2-0001 — evidence

**Agent HOME rewrite on camp Thor nodes**  ·  independence: 9 student(s)  ·  3 episode(s)

## T01 — Agent HOME is rewritten to the profile dir

- **Claim:** In the camp Hermes terminal tool, $HOME is rewritten to <profile>/home, so any command using ~ or $HOME silently resolves under /home/<user>/.hermes/profiles/sage/home/ instead of the real /home/<user>/ — producing bogus 'No such file or directory' for files that plainly exist and making installed tools look missing (which pixi -> not found while /home/<user>/.pixi/bin/pixi exists); fix: always use absolute /home/<user>/... paths in terminal commands and never rely on ~ or a login-shell PATH.
- kind: `invariant` · confidence: high · generality: toolchain · cross-shard: True
- merged from clusters: C000, C010, C019
- **Notes:** Corpus-wide grep supersedes cluster metadata for independence. Affected paths include .ssh, .cache, .local, .venvs, .config, not just project dirs. One episode shows a cold podman store under the profile HOME forcing a ~5.5GB base-image re-pull.

### `node-H01D-20260724_140109_2d7d81-00`
friction: retry_depth=1 failures=1 wall=78.5s resolved=True

> /usr/bin/bash: line 3: cd: /home/<user>/.hermes/profiles/sage/home/AI-Projects/birdnet: No such file or directory

### `node-H01D-20260725_173920_3bddee-00`
friction: retry_depth=1 failures=2 wall=172.8s resolved=True

> HOME=/home/<user>/.hermes/profiles/sage/home
> PWD=/home/<user>
> no ~/.ssh
> ---
> /home/<user>/.hermes/profiles/sage/home/.ssh
> ---
> /home/<user>/.hermes/profiles/sage/home/.ssh

### `node-H035-20260723_142740_b07b9d-04`
friction: retry_depth=6 failures=13 wall=2792.6s resolved=True

> Pixi isn't installed on this machine. The terminal tool is running with `$HOME` expanded under the Hermes profile (`~/.hermes/profiles/sage/home`), which I've already seen in earlier calls — so my `~` lookups go there, not the real `/home/<user>`.

### `node-H035-20260723_142740_b07b9d-04`
friction: retry_depth=6 failures=13 wall=2792.6s resolved=True

> NVIDIA Thor with CUDA capability sm_110 is not compatible with the current PyTorch installation.\nThe current PyTorch install supports CUDA capabilities sm_50 sm_60 ... sm_100 sm_120 ... torch.AcceleratorError: CUDA error: no kernel image is available for execution on the device
