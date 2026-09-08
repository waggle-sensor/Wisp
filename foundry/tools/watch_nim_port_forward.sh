#!/usr/bin/env bash
# Watch a Brev NIM port-forward and restart it whenever localhost stops responding.
#
# Loops forever until you stop it (Ctrl+C).
#
# Usage:
#   ./foundry/tools/watch_nim_port_forward.sh
#   ./foundry/tools/watch_nim_port_forward.sh --instance nim-h200 --port 8000
#   INTERVAL=15 ./foundry/tools/watch_nim_port_forward.sh
#
# Env overrides:
#   BREV_INSTANCE   default: nim-h200
#   LOCAL_PORT      default: 8000
#   REMOTE_PORT     default: 8000
#   INTERVAL        seconds between checks (default: 10)
#   CURL_TIMEOUT    curl max-time seconds (default: 5)
set -euo pipefail

INSTANCE="${BREV_INSTANCE:-nim-h200}"
LOCAL_PORT="${LOCAL_PORT:-8000}"
REMOTE_PORT="${REMOTE_PORT:-8000}"
INTERVAL="${INTERVAL:-10}"
CURL_TIMEOUT="${CURL_TIMEOUT:-5}"

usage() {
  cat >&2 <<'EOF'
Usage:
  watch_nim_port_forward.sh [options]

Options:
  --instance NAME     Brev instance (default: nim-h200)
  --port N            Local and remote port (default: 8000)
  --local-port N      Local listen port (default: 8000)
  --remote-port N     Remote NIM port (default: 8000)
  --interval S        Seconds between health checks (default: 10)
  -h, --help          This help

Stop with Ctrl+C.
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
    --port)
      [[ $# -ge 2 ]] || usage
      LOCAL_PORT="$2"; REMOTE_PORT="$2"; shift 2
      ;;
    --port=*) LOCAL_PORT="${1#--port=}"; REMOTE_PORT="$LOCAL_PORT"; shift ;;
    --local-port)
      [[ $# -ge 2 ]] || usage
      LOCAL_PORT="$2"; shift 2
      ;;
    --local-port=*) LOCAL_PORT="${1#--local-port=}"; shift ;;
    --remote-port)
      [[ $# -ge 2 ]] || usage
      REMOTE_PORT="$2"; shift 2
      ;;
    --remote-port=*) REMOTE_PORT="${1#--remote-port=}"; shift ;;
    --interval)
      [[ $# -ge 2 ]] || usage
      INTERVAL="$2"; shift 2
      ;;
    --interval=*) INTERVAL="${1#--interval=}"; shift ;;
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

HEALTH_URL="http://127.0.0.1:${LOCAL_PORT}/v1/health/ready"
MODELS_URL="http://127.0.0.1:${LOCAL_PORT}/v1/models"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

endpoint_up() {
  curl -sf --max-time "$CURL_TIMEOUT" "$HEALTH_URL" >/dev/null 2>&1 \
    || curl -sf --max-time "$CURL_TIMEOUT" "$MODELS_URL" >/dev/null 2>&1
}

kill_stale_listeners() {
  local pids
  pids="$(lsof -tiTCP:"$LOCAL_PORT" -sTCP:LISTEN 2>/dev/null || true)"
  if [[ -n "$pids" ]]; then
    log "Killing stale listener(s) on :${LOCAL_PORT}: $pids"
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true
    sleep 1
  fi
}

bring_up_forward() {
  log "Starting: brev port-forward ${INSTANCE} -p ${LOCAL_PORT}:${REMOTE_PORT}"
  kill_stale_listeners
  # brev port-forward typically exits after SSH LocalForward is established;
  # the ssh child keeps listening on LOCAL_PORT.
  if ! brev port-forward "$INSTANCE" -p "${LOCAL_PORT}:${REMOTE_PORT}"; then
    log "ERROR: brev port-forward failed"
    return 1
  fi
  sleep 1
  if endpoint_up; then
    log "Port-forward healthy (localhost:${LOCAL_PORT} -> ${INSTANCE}:${REMOTE_PORT})"
    return 0
  fi
  log "ERROR: port-forward ran but endpoint still unreachable"
  return 1
}

cleanup() {
  log "Stopped watching (signal)."
  exit 0
}
trap cleanup INT TERM

if ! command -v brev >/dev/null 2>&1; then
  echo "ERROR: brev not found in PATH" >&2
  exit 1
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "ERROR: curl not found in PATH" >&2
  exit 1
fi

log "Watching NIM port-forward forever"
log "  instance=${INSTANCE}  map=localhost:${LOCAL_PORT}->:${REMOTE_PORT}  interval=${INTERVAL}s"
log "  Stop with Ctrl+C"

# Immediate bring-up if already down
if endpoint_up; then
  log "Already up"
else
  log "Down at start — bringing up"
  bring_up_forward || true
fi

while true; do
  sleep "$INTERVAL"
  if endpoint_up; then
    # Quiet when healthy; uncomment for verbose heartbeat:
    # log "ok"
    continue
  fi
  log "DOWN — restarting port-forward"
  bring_up_forward || true
done
