# Credential hygiene, cron safety, and Slack notification delivery

Extracted from `sage-waggle/SKILL.md` `## Pitfalls`. Each entry is a field-observed
failure and its fix. Routed from the Pitfalls index in SKILL.md.

- **Email cron job must NEVER auto-reply**: The email checking cron job must be read-only — list inbox, read unread messages, mark as seen, summarize. NEVER compose or send replies from a cron job. Each cron run is a fresh session with no memory of previous runs, so it cannot track "I already replied to this." Without state tracking, auto-reply + failed mark-as-read = spam loop (28 duplicate emails sent in one incident). Replies should only happen when explicitly requested in a live chat session. The correct himalaya flag syntax is `himalaya flag add -a sage <ID> seen` (positional arg, NOT `--flag seen`).

- **Slack incoming webhooks cannot upload files**: Webhooks accept JSON text/blocks only. To post images to Slack, use a Slack Bot Token with `slack_sdk` (`pip install slack_sdk`) and `files_upload_v2()` — this is the current API (old `files.upload` retired March 2025). Requires creating a Slack app with `files:write` + `chat:write` scopes, installing it, and inviting the bot to the channel. Store the bot token and channel ID in `secrets/bot-secrets` (shell export format, gitignored, `chmod 600`). See `references/cloud-trigger-notifications.md` for the full setup and working code.

- **Credential hygiene in job YAMLs**: Never commit camera passwords or credentials to git. Use placeholders like `CAMERA_URL_HERE` in committed job YAMLs and pass actual credentials at deploy time via `pluginctl deploy -- --camera "http://user:pass@..."`. GitHub secret scanning will flag Basic Auth strings in URLs. If credentials are accidentally committed, use `git filter-repo --replace-text replacements.txt --force` to scrub all history, then `git push --force`. Install with `pip install git-filter-repo`.
