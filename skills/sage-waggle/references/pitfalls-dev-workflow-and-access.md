# SSH/tmux session handling, MCP setup, and node network reach

Extracted from `sage-waggle/SKILL.md` `## Pitfalls`. Each entry is a field-observed
failure and its fix. Routed from the Pitfalls index in SKILL.md.

- **MCP add is interactive**: `hermes mcp add sage --url <url>` prompts for auth token and tool filtering. Pipe `printf 'n\nY\n'` for no-auth, enable-all-tools. Must start new session after adding.

- **Tmux session transcripts**: Save to the dedicated `~/AI-projects/tmux-logs/` directory (NOT the bare `~/AI-projects/` root, NOT inside a project repo). Filename convention: `hermes-yolo-session-YYYY-MM-DD-partN-ansi.txt` — `hermes-yolo-session-` prefix, ISO date, then `partN` (start a fresh `part1` for each new date; bump the part number for additional captures the same day as the tmux history buffer rolls over). Capture full scrollback WITH ANSI color codes: `cd ~/AI-projects/tmux-logs && tmux capture-pane -t <session>:<win>.<pane> -e -p -S - > hermes-yolo-session-YYYY-MM-DD-partN-ansi.txt`. The `-e` flag preserves ANSI SGR codes (verify with `grep -c $'\033' <file>`); `-S -` grabs the entire history buffer (find the pane via `tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} hist=#{history_size}'`). Caveat: tmux only retains what's within its `history-limit`; anything scrolled off before capture is unrecoverable — that's why old sessions were split into part1–7.

- **Sage containers are network-restricted but host processes may not be**: Containers on edge nodes cannot reach external services (Slack, email APIs, etc.). Host processes via SSH on some nodes (e.g. Thor H00F) CAN reach the internet — verified with `curl https://hooks.slack.com/` returning 302. The recommended pattern is still a cloud-side watcher, not a host-side process. See `references/cloud-trigger-notifications.md`.

- **SSH ControlPersist + ProxyJump + passphrase key = frequent disconnects**: When SSH config uses `ControlPersist 10m` on the jump host (sage-vpn) and a passphrase-protected `IdentityFile`, connections through `ProxyJump` expire after 10 minutes of idle. The next SSH command needs the agent to provide the key again, but the agent may have been restarted or the `SSH_AUTH_SOCK` changed. Symptoms: "Permission denied" errors on SSH commands that worked minutes ago, especially during long background operations (Docker builds, k3s imports). **Root cause**: the `*.sage` host block uses `ProxyJump sage-vpn` but has no `IdentityFile` of its own — it relies entirely on the agent. When the control master expires and must reconnect, both the jump and the target need the key. **Fix**: add `IdentityFile ~/.ssh/sage_key` and `IdentitiesOnly yes` to the `*.sage` block so SSH can find the key without the agent. Keep `User root` as default (override with `beckman@` on command line as needed). Save backup: `cp ~/.ssh/config ~/.ssh/config.old`. For long operations (docker build, k3s import), always use `nohup` on Thor so the work survives SSH disconnections:
    ```bash
    ssh beckman@node-H00F.sage "cd /tmp/sage-bioclip && nohup sudo docker build -t bioclip:0.2.0 . > /tmp/build.log 2>&1 &"
    # Check progress:
    ssh beckman@node-H00F.sage "tail -5 /tmp/build.log"
    ```
    Similarly for k3s import: `nohup bash -c 'sudo docker save IMAGE | sudo k3s ctr images import - > /tmp/import.log 2>&1 && echo DONE >> /tmp/import.log' &`
