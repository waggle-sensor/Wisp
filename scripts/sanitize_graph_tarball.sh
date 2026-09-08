#!/usr/bin/env bash
# Strip build-machine absolute paths out of a graphify baseline tarball.
# Repacked artifacts must not carry the packager's home directory.
#
# .graphify_root is DELETED, and the installer must rewrite it with a real
# absolute path (see README / hermes-agent.md).
#
# Why not just rewrite it here: graphify reads the marker with Path(text) and
# does no shell expansion, so a literal "$HOME/..." resolves to a bogus nested
# path that fails exists(). A build-machine absolute path is equally wrong on
# the student's host. There is no portable string we can bake into the tarball,
# so the marker is omitted and written at install time instead.
#
# Deleting it is NOT sufficient on its own. `graphify update` resolves the
# marker relative to the CWD (GRAPHIFY_OUT defaults to the relative name
# "graphify-out"), so with no marker it falls back to Path(".") and scans
# whatever directory the user happens to be in — from $HOME that means the
# entire home tree. Verified on a Thor node 2026-09-03: 8,746 files scanned and
# a stray ~/graphify-out created. With a correct absolute marker and CWD at the
# profile it scans the right 244 files.
set -euo pipefail
TARBALL="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
INSTALL_ROOT="${2:-\$HOME/.hermes/profiles/sage}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

tar -xzf "$TARBALL" -C "$WORK"
DIR="$WORK/graphify-out"
[[ -d "$DIR" ]] || { echo "no graphify-out/ in $TARBALL" >&2; exit 1; }

# .graphify_root: remove it; no portable value exists (see header). The install
# step writes the real absolute path.
rm -f "$DIR/.graphify_root"

# Everything else (GRAPH_REPORT.md, graph.html <title>, dated backups): these
# are display strings only, so a literal $HOME placeholder is fine here.
while IFS= read -r f; do
  INSTALL_ROOT="$INSTALL_ROOT" perl -pi -e 's{(?:/Users|/home)/[^/\s"]+/[^\s"]*?hermes-profile}{$ENV{INSTALL_ROOT}}g' "$f"
done < <(grep -rlE '(/Users|/home)/[^/[:space:]"]+/' "$DIR" 2>/dev/null || true)

remaining="$( { grep -rlE '(/Users|/home)/[^/[:space:]"]+/' "$DIR" 2>/dev/null || true; } | wc -l | tr -d ' ')"
if [[ "$remaining" != "0" ]]; then
  echo "WARNING: $remaining file(s) still contain absolute home paths:" >&2
  grep -rlE '(/Users|/home)/[^/[:space:]"]+/' "$DIR" >&2
fi

( cd "$WORK" && tar -czf "$TARBALL" graphify-out )
echo "sanitized: $TARBALL"
