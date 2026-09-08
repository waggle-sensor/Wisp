# Agent shell environment on camp Thor nodes (HOME, `~`, and caches)

**Applicability:** any Hermes agent running on a camp Thor blade whose terminal tool
issues shell commands on the participant's account.

## Claim

The agent's shell runs with **`HOME` rewritten to the profile directory**:

```
HOME=/home/<user>/.hermes/profiles/sage/home     # agent shell
/home/<user>                                      # the account's real home (passwd)
```

Every `~` and `$HOME` in an agent-issued command therefore resolves **inside the
profile**, not in the user's home. Because the profile-scoped path usually does not
exist, the shell returns an ordinary "No such file or directory" — the same error a
typo produces — so the cause is easy to misread.

```
/usr/bin/bash: line 3: cd: /home/<user>/.hermes/profiles/sage/home/AI-Projects/birdnet: No such file or directory
```

The give-away is the **doubled path**: a real home path with
`.hermes/profiles/sage/home/` spliced into the middle. If you see that shape, this
is the cause — the project is there, you are not looking where you think you are.

## Rules

1. **Use absolute real-home paths in every terminal call.** Write
   `/home/<user>/project`, never `~/project` or `$HOME/project`.
2. **Resolve the real home once, explicitly**, if you need it programmatically —
   `getent passwd "$(id -un)" | cut -d: -f6` — and do not trust `$HOME` or `~`.
3. **Ask the user for the path** rather than guessing when a `cd` fails with the
   doubled shape.
4. **Expect a separate, cold cache.** `~/.cache`, `~/.local`, `~/.venvs`,
   `~/.config` and container storage under the agent's HOME are *not* the user's.
   A layer the user already pulled will be missing for you.

## Why it matters beyond a failed `cd`

Observed consequences in the 2026 cohort, all from this single cause:

- A container base image re-pulled in full (~5.5 GB) because the agent's podman
  store was cold while the user's interactive shell had the layer cached.
- An SSH key written where `ssh` does not look for it.
- A large export written to a directory the user never finds.
- Hundreds of MB of output images written where nothing reads them.
- "Model not found" while the weights are present — in the real home.

## Scale (2026 camp)

| Measure | Value |
| --- | ---: |
| Students affected | 9 of 11 with transcripts |
| Episodes containing the rewritten path | 52 |
| Explicit `cd … No such file or directory` failures | 18 |

## Related

- `sudo-allowlist-and-image-import.md` — the other environment surprise on these nodes.
