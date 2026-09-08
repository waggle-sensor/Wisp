# Sage data/manifest APIs, portal auth, NRP storage and the upload agent

Extracted from `sage-waggle/SKILL.md` `## Pitfalls`. Each entry is a field-observed
failure and its fix. Routed from the Pitfalls index in SKILL.md.

- Manifests collection needs trailing slash (`/manifests/`); single node is `/manifests/<vsn>` (slash optional). Prefer per-VSN; also use `/api/v-beta/nodes/<vsn>` for flatter site/type metadata — see `references/auth-api-manifests-and-nodes.md`

- Data API uses NDJSON (newline-delimited JSON), not standard JSON array

- Portal can be slow/timeout — prefer API endpoints for programmatic access. Portal rebuilds DB on Sundays.

- sage-data-client returns pandas DataFrames — ensure pandas is installed

- **Protected data access requires `-L` (follow redirects)**: `curl -L -u <username>:<portal-access-token> -o output.jpg <url>` — token from portal account page. The Sage storage API at `storage.sagecontinuum.org` returns a **302 redirect** to the actual backend (`nrdstor.nationalresearchplatform.org`) with a signed JWT in the query string. Without `-L`, curl gets an empty 302 response and writes a 0-byte file. Always use `-L` when downloading from Sage storage. In Python, use `subprocess.run(["curl", "-s", "-f", "-L", "-u", ...])` rather than urllib — the NRP backend may do a double redirect that urllib can't follow.

- **Sage portal username for storage auth**: Use the portal username (e.g. "beckman"), not GitHub username. Token from `portal.sagecontinuum.org/account/access`. Format: `curl -u <portal-username>:<access-token>`.

- **Upload agent clears files almost instantly**: The `wes-upload-agent` pod scans `/media/plugin-data/uploads/<job>/<plugin>/<version>/` on the host, rsyncs to `beehive-uploads.sagecontinuum.org`, and deletes immediately. There is no practical window to intercept files on-node before they're cleaned up. Don't try to race it; use the Sage data API to find upload URLs instead.

- **NRP storage (nrdstor.nationalresearchplatform.org) can lag or break globally**: Beehive receives uploads fine but the Beehive-to-NRP sync can fail globally. Symptoms: data API shows upload records with valid URLs, but `curl -L -u user:token <url>` returns 404 ("Unable to open ... no such file or directory") from the NRP backend. Old files may still work while new ones 404. Debug: (1) check `wes-upload-agent` logs on node — if it shows "uploaded all files found" with no errors, the node side is fine; (2) try downloading from a different node's recent uploads — if those also 404, it's a global NRP issue; (3) `dig nrdstor.nationalresearchplatform.org` to see which replica you're hitting. This is a Sage infrastructure issue — escalate to the cyberinfrastructure team.

- **NRP storage has propagation delays or outages**: Files uploaded from edge nodes may 404 on NRP storage even though the Sage data API shows the upload record. This can be propagation delay (minutes) or a Beehive-to-NRP sync outage (hours+, affects all nodes globally). To diagnose: (1) check if old uploads still work (propagation vs outage), (2) try uploads from other nodes (node-specific vs global), (3) check the upload agent on the node: `sudo kubectl logs wes-upload-agent-<id> --tail=30` — if it shows "uploading/cleaning/done" cycles with no errors, the node side is fine and the problem is downstream. The upload agent uses rsync to `beehive-uploads.sagecontinuum.org`. Upload files live briefly at `hostPath: /media/plugin-data/uploads/<job>/<plugin>/<version>/` before being rsynced and deleted — the window is too short to intercept. Alternative for image delivery when NRP is down: SSH to the node and grab a fresh camera snapshot directly (`curl` the Reolink HTTP snapshot URL from the host).
