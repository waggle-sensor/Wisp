# sudo on camp Thor accounts: NOPASSWD allowlist, and how to import an image

**Applicability:** camp Thor blades, participant accounts, commands issued from the
Hermes terminal tool (no TTY).

## Claim

Camp accounts have **passwordless sudo for an explicit binary allowlist only**:

```
(ALL) NOPASSWD: /usr/local/bin/kubectl, /usr/bin/docker, /usr/local/bin/docker,
                /usr/bin/docker-compose, /usr/local/bin/docker-compose,
                /usr/bin/runplugin, /usr/bin/pluginctl
```

Anything else needs a password. The Hermes terminal has **no TTY and no askpass
helper**, so instead of prompting it fails:

```
sudo: a terminal is required to read the password; either use the -S option to read
from standard input or configure an askpass helper
```

**Read that error as "this binary is not on the allowlist" — not as "sudo is
unavailable."** `sudo kubectl`, `sudo docker` and `sudo pluginctl` work fine and are
used constantly. Notably absent: **`k3s`**, `ctr`, `crictl`, `apt-get`, `systemctl`,
`nvpmodel`, `nvidia-ctk`, `usermod`, and `cat`.

## Consequence: `sudo k3s ctr images import` cannot be used

The widely-copied side-load step

```bash
sudo docker save IMAGE:TAG | sudo k3s ctr images import -    # DOES NOT WORK HERE
```

fails on the `k3s` half. Use one of these instead.

### Preferred — let pluginctl do the build and the push

```bash
sudo pluginctl build .        # builds AND pushes to the node-local registry
sudo pluginctl run <ref> -- <args>
```

`pluginctl` is allowlisted, so this is the shortest working path. (If the run then
fails to pull with an x509 error, see `node-registry-x509-trust.md` — a different
problem.)

### Fallback — a privileged import pod via `sudo kubectl`

`kubectl` is allowlisted, so a short-lived privileged pod can reach the node's
containerd socket and perform the import that `sudo k3s ctr` would have done.
Use when you must import a tarball rather than build in place.

## For the agent

- Do **not** retry a password-failing command. Nothing about the second attempt is
  different, and repeated `sudo` failures clear the credential cache.
- Either switch to an allowlisted path, or hand the exact command to the student to
  run in their own shell (they have a TTY).
- `sudo -l` prints the current allowlist; it is cheap and settles the question.

## Related

- `agent-shell-environment.md` — the other environment surprise on these nodes.
- `node-registry-x509-trust.md` — a pull failure that looks like an import failure.
