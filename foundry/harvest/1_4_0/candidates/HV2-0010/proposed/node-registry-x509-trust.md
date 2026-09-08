# `pluginctl build` succeeds, `pluginctl run` cannot pull: x509 trust

**Applicability:** Thor blades using the node-local registry (`<node-ip>:5000`).

## Symptom

`pluginctl build` succeeds and hands back a `<node-ip>:5000/local/<name>` reference.
`pluginctl run` on the same node then fails to pull it:

```
Failed to pull image ...: x509: certificate signed by unknown authority
```

Confusingly, `openssl verify` of the same chain returns 0 — the certificate is fine;
**kubelet's containerd** does not trust it.

## The surface form is often unrecognisable

The same underlying failure frequently shows up as a status cycle rather than a clear
pull error:

```
Plugin is in "Pending" state. Waiting...
Plugin is in "" state.
Error: Failed to get plugin status pods "<name>" not found
```

That sequence is **ImagePullBackOff followed by pod GC**, not a pluginctl or
scheduler bug. Do not debug the scheduler on this evidence.

## Diagnose

```bash
sudo kubectl describe pod <name> | tail -30      # kubectl is allowlisted
```

Look at `Events:` for the real reason. `describe` is the fastest way from a confusing
pluginctl message to the actual cause, and it distinguishes this from the other
common pull failures:

| Event text | Cause |
| --- | --- |
| `x509: certificate signed by unknown authority` | registry trust — this page |
| `manifest unknown` / `not found` | wrong tag or never pushed |
| `connection refused` / `no route to host` | registry not reachable |
| `OOMKilled` after starting | memory limits, not a pull problem |

## Work around it

1. **Re-import rather than re-pull.** Get the image into the node's containerd
   directly instead of going through the registry — but note that
   `sudo k3s ctr images import` is **not available** on camp accounts; see
   `sudo-allowlist-and-image-import.md` for the allowlisted routes.
2. **Prefer `sudo pluginctl build`**, which builds and pushes in one allowlisted step
   and avoids a manual registry round-trip.
3. Escalate to the instructor if the node's registry CA is genuinely missing from
   containerd's trust store — that is a node provisioning fix, not a per-student one.

## Related

- `sudo-allowlist-and-image-import.md` — what you are allowed to run.
- `pluginctl-gpu-runtimeclass.md` — the other reason a pod "runs" but is wrong.
