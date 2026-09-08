#!/usr/bin/env bash
# Bring up a NIM (OpenAI-compatible) endpoint on a Brev GPU instance and leave it
# serving on the instance's :8000. Pair with watch_nim_port_forward.sh locally.
#
# This is the step the notebook never recorded: it documented the port-forward but
# not how the NIM behind it got there, which made the environment unreproducible.
#
# Usage:
#   ./foundry/tools/start_nim_on_brev.sh --key-file ~/.ngc/apikey
#   NGC_API_KEY=<your-ngc-key> ./foundry/tools/start_nim_on_brev.sh --instance nim-h200
#
# Never pass the key as an argument (it lands in shell history and `ps`); use
# --key-file or the NGC_API_KEY environment variable.
#
# Env:
#   NGC_API_KEY     NGC key (or use --key-file)
#   BREV_INSTANCE   default: nim-h200
#   NIM_IMAGE       default: nvcr.io/nim/google/gemma-4-31b-it:1.7.1-variant
#   NIM_PORT        default: 8000
set -euo pipefail

INSTANCE="${BREV_INSTANCE:-nim-h200}"
IMAGE="${NIM_IMAGE:-nvcr.io/nim/google/gemma-4-31b-it:1.7.1-variant}"
PORT="${NIM_PORT:-8000}"
KEY_FILE=""

usage() {
  cat >&2 <<'EOF'
Usage:
  start_nim_on_brev.sh [options]

Options:
  --instance NAME     Brev instance (default: nim-h200)
  --image REF         NIM container image (default: gemma-4-31b-it:1.7.1-variant)
  --port N            Port NIM serves on, instance-side (default: 8000)
  --key-file PATH     File containing the NGC API key (mode 600)
  -h, --help          This help

The NGC key may also be supplied via the NGC_API_KEY environment variable.
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --instance) [[ $# -ge 2 ]] || usage; INSTANCE="$2"; shift 2 ;;
    --instance=*) INSTANCE="${1#--instance=}"; shift ;;
    --image) [[ $# -ge 2 ]] || usage; IMAGE="$2"; shift 2 ;;
    --image=*) IMAGE="${1#--image=}"; shift ;;
    --port) [[ $# -ge 2 ]] || usage; PORT="$2"; shift 2 ;;
    --port=*) PORT="${1#--port=}"; shift ;;
    --key-file) [[ $# -ge 2 ]] || usage; KEY_FILE="$2"; shift 2 ;;
    --key-file=*) KEY_FILE="${1#--key-file=}"; shift ;;
    -h|--help) usage ;;
    *) echo "Unexpected argument: $1" >&2; usage ;;
  esac
done

command -v brev >/dev/null 2>&1 || { echo "ERROR: brev not found in PATH" >&2; exit 1; }

if [[ -n "$KEY_FILE" ]]; then
  [[ -r "$KEY_FILE" ]] || { echo "ERROR: cannot read --key-file $KEY_FILE" >&2; exit 1; }
  NGC_API_KEY="$(tr -d '\r\n' < "$KEY_FILE")"
fi
: "${NGC_API_KEY:?NGC_API_KEY must be set (or pass --key-file)}"

echo "[NIM] instance=$INSTANCE image=$IMAGE port=$PORT"

# The key is written to a 600 file on the instance and read from there, so it
# never appears in an argument list.
brev exec "$INSTANCE" "umask 077 && cat > ~/.ngckey" <<< "$NGC_API_KEY"

brev exec "$INSTANCE" "
set -euo pipefail
NGC_API_KEY=\$(cat ~/.ngckey)
IMAGE='$IMAGE'
PORT='$PORT'
CACHE=\"\$HOME/.cache/nim\"
mkdir -p \"\$CACHE\"

echo \"\$NGC_API_KEY\" | docker login nvcr.io --username '\\\$oauthtoken' --password-stdin
docker rm -f nim >/dev/null 2>&1 || true
docker pull \"\$IMAGE\"
docker run -d --name nim --gpus all --shm-size=16g -e NGC_API_KEY \
  -v \"\$CACHE:/opt/nim/.cache\" -u \"\$(id -u)\" -p \"\${PORT}:8000\" \"\$IMAGE\"
echo 'container started; weights download + load takes ~10-15 min on a cold cache'
"

echo "[NIM] waiting for /v1/health/ready on ${INSTANCE}:${PORT} (up to 30 min)"
for i in $(seq 1 180); do
  code="$(brev exec "$INSTANCE" \
    "curl -s -o /dev/null -w '%{http_code}' http://localhost:${PORT}/v1/health/ready" \
    2>/dev/null | tr -dc '0-9' | tail -c 3 || true)"
  if [[ "$code" == "200" ]]; then
    echo "[NIM] READY"
    brev exec "$INSTANCE" "curl -s http://localhost:${PORT}/v1/models" 2>/dev/null | tail -3
    echo
    echo "Next, locally:"
    echo "  ./foundry/tools/watch_nim_port_forward.sh --instance ${INSTANCE} --port ${PORT}"
    echo "  export OPENAI_BASE_URL=http://localhost:${PORT}/v1"
    exit 0
  fi
  alive="$(brev exec "$INSTANCE" "docker ps -q -f name=nim | wc -l" 2>/dev/null | tr -dc '0-9' | head -c 1 || true)"
  if [[ "$alive" == "0" ]]; then
    echo "[NIM] ERROR: container exited" >&2
    brev exec "$INSTANCE" "docker logs --tail 30 nim" >&2 2>/dev/null || true
    exit 1
  fi
  sleep 10
done

echo "[NIM] TIMEOUT waiting for health" >&2
brev exec "$INSTANCE" "docker logs --tail 40 nim" >&2 2>/dev/null || true
exit 1
