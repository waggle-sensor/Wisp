#!/usr/bin/env bash
# Wait until update_public_graphify.sh exits, then tear down the NIM session:
#   1) stop watch_nim_port_forward.sh (if running)
#   2) drop localhost:8000 listeners
#   3) brev stop <instance>   (optional: --delete)
#
# Typical usage (in a third terminal, while the other two are already running):
#   ./foundry/tools/update_public_graphify.sh --all
#   ./foundry/tools/watch_nim_port_forward.sh
#   ./foundry/tools/stop_nim_after_graphify.sh
#
# Env:
#   BREV_INSTANCE   default: nim-h200
#   INTERVAL        poll seconds (default: 15)
#   LOCAL_PORT      default: 8000
set -euo pipefail

INSTANCE="${BREV_INSTANCE:-nim-h200}"
INTERVAL="${INTERVAL:-15}"
LOCAL_PORT="${LOCAL_PORT:-8000}"
DELETE=0
FORCE_IF_NOT_RUNNING=0
WAIT_FOR_START=0
DRY_RUN=0

usage() {
  cat >&2 <<'EOF'
Usage:
  stop_nim_after_graphify.sh [options]

Waits until update_public_graphify.sh is no longer running, then stops the
Brev NIM instance (and the port-forward watchdog).

Options:
  --instance NAME     Brev instance (default: nim-h200)
  --interval S        Poll interval seconds (default: 15)
  --wait-for-start    If graphify is not running yet, wait until it appears
  --force             If graphify is not running, stop the instance immediately
  --delete            brev delete instead of brev stop
  --dry-run           Print actions only
  -h, --help          This help
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --instance)
      [[ $# -ge 2 ]] || usage
      INSTANCE="$2"; shift 2
      ;;
    --instance=*) INSTANCE="${1#--instance=}"; shift ;;
    --interval)
      [[ $# -ge 2 ]] || usage
      INTERVAL="$2"; shift 2
      ;;
    --interval=*) INTERVAL="${1#--interval=}"; shift ;;
    --wait-for-start) WAIT_FOR_START=1; shift ;;
    --force) FORCE_IF_NOT_RUNNING=1; shift ;;
    --delete) DELETE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      ;;
    *)
      echo "Unexpected argument: $1" >&2
      usage
      ;;
  esac
done

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

# Match the graphify driver script only (not this waiter, not unrelated shells).
# Covers: foundry/tools/update_public_graphify.sh, ./update_public_graphify.sh, etc.
graphify_pids() {
  pgrep -f '(^|/)update_public_graphify\.sh([[:space:]]|$)' 2>/dev/null || true
}

watch_pids() {
  pgrep -f '(^|/)watch_nim_port_forward\.sh([[:space:]]|$)' 2>/dev/null || true
}

graphify_running() {
  [[ -n "$(graphify_pids)" ]]
}

cleanup() {
  log "Interrupted — leaving instance as-is."
  exit 130
}
trap cleanup INT TERM

if ! command -v brev >/dev/null 2>&1; then
  echo "ERROR: brev not found in PATH" >&2
  exit 1
fi

log "Will stop Brev instance '${INSTANCE}' after update_public_graphify.sh exits"
log "  poll=${INTERVAL}s  delete=${DELETE}  dry_run=${DRY_RUN}"

if graphify_running; then
  log "Detected update_public_graphify.sh (pids: $(graphify_pids | tr '\n' ' '))"
elif [[ "$WAIT_FOR_START" == "1" ]]; then
  log "graphify not running yet — waiting for it to start (--wait-for-start)"
  while ! graphify_running; do
    sleep "$INTERVAL"
  done
  log "Detected update_public_graphify.sh (pids: $(graphify_pids | tr '\n' ' '))"
elif [[ "$FORCE_IF_NOT_RUNNING" == "1" ]]; then
  log "graphify not running — --force set, proceeding to stop instance"
else
  echo "ERROR: update_public_graphify.sh is not running." >&2
  echo "  Start it first, or pass --wait-for-start / --force." >&2
  exit 1
fi

# Wait until graphify exits (no-op if --force and already not running).
while graphify_running; do
  log "graphify still running (pids: $(graphify_pids | tr '\n' ' ')) — sleeping ${INTERVAL}s"
  sleep "$INTERVAL"
done

log "update_public_graphify.sh has stopped"

# Stop port-forward watchdog
wpids="$(watch_pids)"
if [[ -n "$wpids" ]]; then
  log "Stopping watch_nim_port_forward.sh (pids: $(echo "$wpids" | tr '\n' ' '))"
  if [[ "$DRY_RUN" != "1" ]]; then
    # shellcheck disable=SC2086
    kill $wpids 2>/dev/null || true
    sleep 1
  fi
else
  log "watch_nim_port_forward.sh not running"
fi

# Drop leftover SSH LocalForward listeners on LOCAL_PORT
stale="$(lsof -tiTCP:"$LOCAL_PORT" -sTCP:LISTEN 2>/dev/null || true)"
if [[ -n "$stale" ]]; then
  log "Killing listeners on :${LOCAL_PORT}: $(echo "$stale" | tr '\n' ' ')"
  if [[ "$DRY_RUN" != "1" ]]; then
    # shellcheck disable=SC2086
    kill $stale 2>/dev/null || true
  fi
fi

if [[ "$DELETE" == "1" ]]; then
  log "brev delete ${INSTANCE}"
  if [[ "$DRY_RUN" != "1" ]]; then
    brev delete "$INSTANCE"
  fi
else
  log "brev stop ${INSTANCE}"
  if [[ "$DRY_RUN" != "1" ]]; then
    if ! brev stop "$INSTANCE"; then
      echo "ERROR: brev stop failed (this machine type may not be stoppable)." >&2
      echo "  To tear it down fully: $0 --force --delete" >&2
      echo "  Or manually: brev delete ${INSTANCE}" >&2
      exit 1
    fi
  fi
fi

log "Done. Current instances:"
brev ls || true
