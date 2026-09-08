#!/usr/bin/env bash
# Run `graphify extract` on each public student sage profile (AST + semantic LLM).
#
# Streams graphify's stdout/stderr live (also tees to a per-student log).
# Defaults to a local NVIDIA NIM (OpenAI-compatible) via brev port-forward:
#
#   # NIM on Brev H200, forwarded to localhost:8000
#   brev port-forward nim-llama33 -p 8000:8000
#
#   OPENAI_BASE_URL=http://localhost:8000/v1 \
#   OPENAI_API_KEY=not-needed \
#   OPENAI_MODEL=google/gemma-4-31B-it \
#   .venv/bin/graphify extract …/sage --backend openai
#
# Override for NRP ellm (or any other OpenAI-compatible endpoint):
#   OPENAI_BASE_URL=https://ellm.nrp-nautilus.io/v1 \
#   OPENAI_API_KEY=… \
#   OPENAI_MODEL=minimax-m2 \
#   ./foundry/tools/update_public_graphify.sh --all
#
# Usage (from repo root or anywhere):
#   ./foundry/tools/update_public_graphify.sh --all
#   ./foundry/tools/update_public_graphify.sh node-H01D
#   ./foundry/tools/update_public_graphify.sh --all --dry-run
#   ./foundry/tools/update_public_graphify.sh --all --cluster-only --resolution 1.5
#   ./foundry/tools/update_public_graphify.sh --all --scope curated
#   ./foundry/tools/update_public_graphify.sh --all --scope full
#
# Do not put API keys in this file. Pass them via the environment when needed.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PUBLIC_ARCHIVES="${PUBLIC_ARCHIVES:-$ROOT/foundry/harvest/1_4_0/brains}"
PUBLIC_DIR="${PUBLIC_DIR:-$ROOT/foundry/.work}"
AUDIT_TSV="$PUBLIC_DIR/graphify-update-audit.tsv"
AUDIT_SUMMARY="$PUBLIC_DIR/graphify-update-audit-summary.md"
LOG_DIR="$PUBLIC_DIR/graphify-update-logs"
DEFAULT_GRAPHIFYIGNORE_DIR="$ROOT"
DEFAULT_SCOPE="curated"
DEFAULT_GRAPHIFYIGNORE_SRC="$DEFAULT_GRAPHIFYIGNORE_DIR/.graphifyignore.${DEFAULT_SCOPE}"

# Defaults: local NVIDIA NIM (google/gemma-4-31B-it) on localhost:8000
DEFAULT_OPENAI_BASE_URL="http://localhost:8000/v1"
DEFAULT_MODEL="google/gemma-4-31B-it"
DEFAULT_OPENAI_API_KEY="not-needed"
DEFAULT_BACKEND="openai"
DEFAULT_TOKEN_BUDGET="25000"
# Single H200 NIM: keep concurrency modest to avoid KV-cache pressure
DEFAULT_MAX_CONCURRENCY="2"
DEFAULT_API_TIMEOUT="1800"
DEFAULT_RESOLUTION="1.0"

DRY_RUN=0
REPACK=0
FORCE=0
RUN_ALL=0
SYNC_GRAPHIFYIGNORE=0
UNPACK_IF_MISSING=1
SKIP_HEALTH_CHECK=0
SKIP_CLUSTER=0
CLUSTER_ONLY=0
SCOPE="$DEFAULT_SCOPE"
GRAPHIFYIGNORE_SRC_SET=0
BACKEND="$DEFAULT_BACKEND"
MODEL="${OPENAI_MODEL:-$DEFAULT_MODEL}"
TOKEN_BUDGET="$DEFAULT_TOKEN_BUDGET"
MAX_CONCURRENCY="$DEFAULT_MAX_CONCURRENCY"
API_TIMEOUT="$DEFAULT_API_TIMEOUT"
RESOLUTION="$DEFAULT_RESOLUTION"
GRAPHIFY_BIN="${GRAPHIFY_BIN:-}"
GRAPHIFYIGNORE_SRC="${GRAPHIFYIGNORE_SRC:-}"
# Empty = leave GRAPHIFY_VIZ_NODE_LIMIT unset (graphify default, usually 5000)
VIZ_NODE_LIMIT="${GRAPHIFY_VIZ_NODE_LIMIT:-}"
STUDENTS=()

usage() {
  cat >&2 <<'EOF'
Usage:
  update_public_graphify.sh --all [options]
  update_public_graphify.sh <student_node> [...] [options]

Runs (live, streamed):
  graphify extract <sage> --backend openai …
  graphify cluster-only <sage> --backend openai …   # GRAPH_REPORT.md

Environment (openai-compatible; default = local NIM):
  OPENAI_BASE_URL   default http://localhost:8000/v1
  OPENAI_API_KEY    default not-needed (local NIM ignores auth; set for remote)
  OPENAI_MODEL      default google/gemma-4-31B-it (or pass --model)
  GRAPHIFY_VIZ_NODE_LIMIT  HTML viz node cap (or pass --viz-node-limit)

  Ensure the NIM is reachable first, e.g.:
    brev port-forward nim-llama33 -p 8000:8000
    curl -s http://localhost:8000/v1/models

Options:
  --all                      Every public archive
  --backend NAME             default: openai
  --model NAME               default: $OPENAI_MODEL or google/gemma-4-31B-it
  --token-budget N           default: 25000
  --max-concurrency N        default: 2
  --api-timeout S            default: 1800
  --resolution N             Leiden cluster resolution (default: 1.0)
                             higher = more/smaller communities; lower = fewer/larger
  --viz-node-limit N         Set GRAPHIFY_VIZ_NODE_LIMIT (HTML viz; default unset)
  --graphify PATH            graphify binary (else .venv, conda hermes, PATH)
  --scope curated|full       Camp ignore variant to sync into each sage/
                             curated (default): SKILL.md / skill-cards / camp docs
                             full: whole codebase (scripts, references, code)
                             Implies --sync-graphifyignore unless --graphifyignore-src set
  --curated                  Shortcut for --scope curated
  --full                     Shortcut for --scope full
  --sync-graphifyignore      Copy camp .graphifyignore into each sage/ first
  --graphifyignore-src PATH  Source for --sync-graphifyignore (overrides --scope)
  --repack                   Rewrite *_public_sage.tar.gz after SUCCESS
  --no-unpack                Do not extract tar when sage/ is missing
  --cluster-only             Skip extract; only run cluster-only (needs graph.json)
  --skip-cluster             Skip cluster-only after extract
  --force                    Pass --force to graphify extract
  --dry-run                  Print commands only
  --skip-health-check        Do not probe OPENAI_BASE_URL before extract
  -h, --help                 This help
EOF
  exit 1
}

join_notes() {
  local IFS='; '
  echo "$*"
}

resolve_graphify() {
  local candidate
  if [[ -n "$GRAPHIFY_BIN" ]]; then
    [[ -x "$GRAPHIFY_BIN" ]] || { echo "ERROR: --graphify not executable: $GRAPHIFY_BIN" >&2; exit 1; }
    echo "$GRAPHIFY_BIN"
    return 0
  fi
  for candidate in \
    "$ROOT/.venv/bin/graphify" \
    "$ROOT/venv/bin/graphify" \
    "${VIRTUAL_ENV:-}/bin/graphify" \
    "${CONDA_PREFIX:-}/bin/graphify"
  do
    [[ -n "$candidate" && -x "$candidate" ]] && { echo "$candidate"; return 0; }
  done
  if command -v conda >/dev/null 2>&1; then
    local base
    base="$(conda info --base 2>/dev/null || true)"
    if [[ -n "$base" && -x "$base/envs/hermes/bin/graphify" ]]; then
      echo "$base/envs/hermes/bin/graphify"
      return 0
    fi
  fi
  if command -v graphify >/dev/null 2>&1; then
    command -v graphify
    return 0
  fi
  echo "ERROR: graphify not found. Create .venv and pip install graphifyy, or set --graphify" >&2
  exit 1
}

check_openai_endpoint() {
  local base="${OPENAI_BASE_URL%/}"
  local root="${base%/v1}"
  local health_url="${root}/v1/health/ready"
  local models_url="${root}/v1/models"

  echo "[HEALTH] probing ${OPENAI_BASE_URL}" >&2
  if curl -sf --max-time 5 "$health_url" >/dev/null 2>&1; then
    echo "[HEALTH] ready via /v1/health/ready" >&2
    return 0
  fi
  if curl -sf --max-time 5 "$models_url" >/dev/null 2>&1; then
    echo "[HEALTH] reachable via /v1/models" >&2
    return 0
  fi
  echo "ERROR: OpenAI-compatible endpoint not reachable at ${OPENAI_BASE_URL}" >&2
  echo "  For local NIM: ensure the container is up and port-forwarded, e.g." >&2
  echo "    brev ls" >&2
  echo "    brev port-forward nim-llama33 -p 8000:8000" >&2
  echo "    curl -s http://localhost:8000/v1/models" >&2
  echo "  Or pass --skip-health-check / set OPENAI_BASE_URL to another endpoint." >&2
  return 1
}

list_students() {
  local d name
  shopt -s nullglob
  for d in "$PUBLIC_ARCHIVES"/*/; do
    name="$(basename "$d")"
    [[ "$name" == .* ]] && continue
    if [[ -d "$d/sage" || -f "$d/${name}_public_sage.tar.gz" ]]; then
      echo "$name"
    fi
  done
  shopt -u nullglob
}

ensure_sage_tree() {
  local student="$1"
  local dest="$PUBLIC_ARCHIVES/$student"
  local sage_dir="$dest/sage"
  local public_tar="$dest/${student}_public_sage.tar.gz"

  if [[ -d "$sage_dir" ]]; then
    echo "$sage_dir"
    return 0
  fi

  if [[ "$UNPACK_IF_MISSING" != "1" ]]; then
    echo "ERROR: missing sage/ for $student (--no-unpack)" >&2
    return 1
  fi

  if [[ ! -f "$public_tar" ]]; then
    echo "ERROR: no sage/ and no public tar for $student" >&2
    return 1
  fi

  echo "[EXTRACT] $student from $(basename "$public_tar")" >&2
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "$sage_dir"
    return 0
  fi
  mkdir -p "$dest"
  tar -xzf "$public_tar" -C "$dest"
  [[ -d "$sage_dir" ]] || { echo "ERROR: tar missing top-level sage/" >&2; return 1; }
  echo "$sage_dir"
}

sync_graphifyignore() {
  local sage_dir="$1"
  [[ "$SYNC_GRAPHIFYIGNORE" == "1" ]] || return 0
  if [[ ! -f "$GRAPHIFYIGNORE_SRC" ]]; then
    echo "ERROR: graphifyignore source missing: $GRAPHIFYIGNORE_SRC" >&2
    return 1
  fi
  echo "[IGNORE] cp $GRAPHIFYIGNORE_SRC -> $sage_dir/.graphifyignore" >&2
  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi
  cp "$GRAPHIFYIGNORE_SRC" "$sage_dir/.graphifyignore"
}

repack_public_tar() {
  local student="$1"
  local dest="$PUBLIC_ARCHIVES/$student"
  [[ "$REPACK" == "1" ]] || return 0
  [[ -d "$dest/sage" ]] || return 0
  echo "[REPACK] ${student}_public_sage.tar.gz" >&2
  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi
  tar -czf "$dest/${student}_public_sage.tar.gz" -C "$dest" sage
}

run_extract() {
  local sage_dir="$1"
  local graphify="$2"
  local log_file="$3"
  local -a cmd

  cmd=("$graphify" extract "$sage_dir" --backend "$BACKEND")
  [[ -n "$MODEL" ]] && cmd+=(--model "$MODEL")
  [[ -n "$TOKEN_BUDGET" ]] && cmd+=(--token-budget "$TOKEN_BUDGET")
  [[ -n "$MAX_CONCURRENCY" ]] && cmd+=(--max-concurrency "$MAX_CONCURRENCY")
  [[ -n "$API_TIMEOUT" ]] && cmd+=(--api-timeout "$API_TIMEOUT")
  [[ -n "$RESOLUTION" ]] && cmd+=(--resolution "$RESOLUTION")
  [[ "$FORCE" == "1" ]] && cmd+=(--force)

  echo "[CMD] ${cmd[*]}" >&2
  echo "[ENV] OPENAI_BASE_URL=${OPENAI_BASE_URL:-} OPENAI_MODEL=${OPENAI_MODEL:-$MODEL} backend=$BACKEND" >&2

  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi

  mkdir -p "$(dirname "$log_file")"
  {
    echo "==== $(date -u +%Y-%m-%dT%H:%M:%SZ) ===="
    echo "CMD: ${cmd[*]}"
    echo "OPENAI_BASE_URL=${OPENAI_BASE_URL:-}"
    echo "OPENAI_MODEL=${OPENAI_MODEL:-$MODEL}"
    echo "RESOLUTION=$RESOLUTION"
    echo
  } >"$log_file"

  # Live stream graphify output to the terminal AND append to the log.
  # pipefail so graphify's non-zero exit fails the pipeline (not tee's).
  set +e
  PYTHONUNBUFFERED=1 "${cmd[@]}" 2>&1 | tee -a "$log_file"
  local rc=${PIPESTATUS[0]}
  set -e
  return "$rc"
}

# Recluster + regenerate GRAPH_REPORT.md (extract stops at graph.json).
run_cluster_only() {
  local sage_dir="$1"
  local graphify="$2"
  local log_file="$3"
  local -a cmd

  [[ "$SKIP_CLUSTER" == "1" ]] && return 0

  cmd=("$graphify" cluster-only "$sage_dir")
  [[ -n "$BACKEND" ]] && cmd+=(--backend "$BACKEND")
  [[ -n "$MODEL" ]] && cmd+=(--model "$MODEL")
  [[ -n "$RESOLUTION" ]] && cmd+=(--resolution "$RESOLUTION")

  echo "[CLUSTER] ${cmd[*]}" >&2
  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi

  {
    echo
    echo "==== cluster-only $(date -u +%Y-%m-%dT%H:%M:%SZ) ===="
    echo "CMD: ${cmd[*]}"
    echo
  } >>"$log_file"

  set +e
  PYTHONUNBUFFERED=1 "${cmd[@]}" 2>&1 | tee -a "$log_file"
  local rc=${PIPESTATUS[0]}
  set -e
  if [[ "$rc" -ne 0 ]]; then
    if [[ "$CLUSTER_ONLY" == "1" ]]; then
      echo "[FAIL] cluster-only failed for $(basename "$(dirname "$sage_dir")") (rc=$rc) — see $log_file" >&2
      return "$rc"
    fi
    echo "[WARN] cluster-only failed for $(basename "$(dirname "$sage_dir")") (rc=$rc); graph.json kept — see $log_file" >&2
    return 0
  fi
  return 0
}

process_one() {
  local student="$1"
  local graphify="$2"
  local public_path="public/archives/${student}/sage"
  local notes=()
  local status="SUCCESS"
  local sage_dir log_file

  echo >&2
  echo "================================================================" >&2
  echo "======== $student ========" >&2
  echo "================================================================" >&2

  if ! sage_dir="$(ensure_sage_tree "$student")"; then
    status="FAILED"
    notes+=("missing_sage_tree")
    printf '%s\t%s\t%s\t%s\n' "$student" "$public_path" "$status" "$(join_notes "${notes[@]}")" >>"$AUDIT_TSV"
    return 1
  fi

  if ! sync_graphifyignore "$sage_dir"; then
    status="FAILED"
    notes+=("sync_graphifyignore_failed")
    printf '%s\t%s\t%s\t%s\n' "$student" "$public_path" "$status" "$(join_notes "${notes[@]}")" >>"$AUDIT_TSV"
    return 1
  fi
  [[ "$SYNC_GRAPHIFYIGNORE" == "1" ]] && notes+=("synced_graphifyignore")

  log_file="$LOG_DIR/${student}.log"

  if [[ "$CLUSTER_ONLY" == "1" ]]; then
    if [[ "$DRY_RUN" != "1" && ! -f "$sage_dir/graphify-out/graph.json" ]]; then
      status="FAILED"
      notes+=("graph.json=missing_for_cluster_only")
      echo "[FAIL] $student — --cluster-only needs $sage_dir/graphify-out/graph.json" >&2
      printf '%s\t%s\t%s\t%s\n' "$student" "$public_path" "$status" "$(join_notes "${notes[@]}")" >>"$AUDIT_TSV"
      return 1
    fi
    if [[ "$DRY_RUN" != "1" ]]; then
      mkdir -p "$(dirname "$log_file")"
      {
        echo "==== $(date -u +%Y-%m-%dT%H:%M:%SZ) cluster-only ===="
        echo "SAGE=$sage_dir"
        echo "RESOLUTION=$RESOLUTION"
        echo
      } >"$log_file"
    fi
    notes+=("cluster_only_mode")
    notes+=("log=$log_file")
    if run_cluster_only "$sage_dir" "$graphify" "$log_file"; then
      if [[ "$DRY_RUN" == "1" ]]; then
        status="DRY_RUN"
        notes+=("dry_run")
      else
        notes+=("cluster_only_ok")
        notes+=("graph.json=present")
        [[ -f "$sage_dir/graphify-out/GRAPH_REPORT.md" ]] && notes+=("GRAPH_REPORT.md=present")
      fi
    else
      status="FAILED"
      notes+=("cluster_only_failed")
      echo "[FAIL] $student — see $log_file" >&2
      printf '%s\t%s\t%s\t%s\n' "$student" "$public_path" "$status" "$(join_notes "${notes[@]}")" >>"$AUDIT_TSV"
      return 1
    fi
  elif run_extract "$sage_dir" "$graphify" "$log_file"; then
    if [[ "$DRY_RUN" == "1" ]]; then
      status="DRY_RUN"
      notes+=("dry_run")
      run_cluster_only "$sage_dir" "$graphify" "$log_file"
    else
      notes+=("extract_ok")
      notes+=("log=$log_file")
      if [[ -f "$sage_dir/graphify-out/graph.json" ]]; then
        notes+=("graph.json=present")
        run_cluster_only "$sage_dir" "$graphify" "$log_file"
        [[ "$SKIP_CLUSTER" != "1" ]] && notes+=("cluster_only_ok")
        if [[ -f "$sage_dir/graphify-out/GRAPH_REPORT.md" ]]; then
          notes+=("GRAPH_REPORT.md=present")
        fi
      else
        notes+=("graph.json=missing_after_extract")
        status="FAILED"
      fi
    fi
  else
    status="FAILED"
    notes+=("extract_failed")
    notes+=("log=$log_file")
    echo "[FAIL] $student — see $log_file" >&2
    printf '%s\t%s\t%s\t%s\n' "$student" "$public_path" "$status" "$(join_notes "${notes[@]}")" >>"$AUDIT_TSV"
    return 1
  fi

  if [[ "$status" == "SUCCESS" ]]; then
    repack_public_tar "$student"
    [[ "$REPACK" == "1" ]] && notes+=("repacked")
  fi

  printf '%s\t%s\t%s\t%s\n' "$student" "$public_path" "$status" "$(join_notes "${notes[@]}")" >>"$AUDIT_TSV"
  echo "[DONE] $student ($status)" >&2
  [[ "$status" == "SUCCESS" || "$status" == "DRY_RUN" ]]
}

write_summary() {
  local audit_tsv="$1"
  local date_str ok failed dry
  date_str="$(date +%Y-%m-%d)"
  ok="$(awk -F'\t' 'NR>1 && $3=="SUCCESS" {c++} END{print c+0}' "$audit_tsv")"
  failed="$(awk -F'\t' 'NR>1 && $3=="FAILED" {c++} END{print c+0}' "$audit_tsv")"
  dry="$(awk -F'\t' 'NR>1 && $3=="DRY_RUN" {c++} END{print c+0}' "$audit_tsv")"

  {
    echo "# Hermes Public Graphify Update Audit — ${date_str}"
    echo
    echo "## Outcome"
    echo
    echo "- Updated (SUCCESS): ${ok}"
    echo "- Dry-run: ${dry}"
    echo "- Failed: ${failed}"
    echo
    echo "## Per student"
    echo
    echo "| Student folder | Status | Notes |"
    echo "| --- | --- | --- |"
    awk -F'\t' 'NR>1 { printf "| `%s` | %s | %s |\n", $1, $3, $4 }' "$audit_tsv"
    echo
    echo "## Command shape"
    echo
    echo '```bash'
    echo "OPENAI_BASE_URL=${OPENAI_BASE_URL:-$DEFAULT_OPENAI_BASE_URL} \\"
    echo "OPENAI_API_KEY=\$OPENAI_API_KEY \\"
    echo "OPENAI_MODEL=${MODEL} \\"
    echo "./foundry/tools/update_public_graphify.sh --all --backend ${BACKEND} --model ${MODEL}"
    echo '```'
    echo
    echo "Logs: \`foundry/.work/graphify-update-logs/<node>.log\`"
  } >"$AUDIT_SUMMARY"
}

# --- args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) RUN_ALL=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --repack) REPACK=1; shift ;;
    --force) FORCE=1; shift ;;
    --no-unpack) UNPACK_IF_MISSING=0; shift ;;
    --skip-health-check) SKIP_HEALTH_CHECK=1; shift ;;
    --skip-cluster) SKIP_CLUSTER=1; shift ;;
    --cluster-only) CLUSTER_ONLY=1; shift ;;
    --curated) SCOPE="curated"; SYNC_GRAPHIFYIGNORE=1; shift ;;
    --full) SCOPE="full"; SYNC_GRAPHIFYIGNORE=1; shift ;;
    --scope)
      [[ $# -ge 2 ]] || usage
      SCOPE="$2"; SYNC_GRAPHIFYIGNORE=1; shift 2
      ;;
    --scope=*) SCOPE="${1#--scope=}"; SYNC_GRAPHIFYIGNORE=1; shift ;;
    --sync-graphifyignore) SYNC_GRAPHIFYIGNORE=1; shift ;;
    --backend)
      [[ $# -ge 2 ]] || usage
      BACKEND="$2"; shift 2
      ;;
    --backend=*) BACKEND="${1#--backend=}"; shift ;;
    --model)
      [[ $# -ge 2 ]] || usage
      MODEL="$2"; shift 2
      ;;
    --model=*) MODEL="${1#--model=}"; shift ;;
    --token-budget)
      [[ $# -ge 2 ]] || usage
      TOKEN_BUDGET="$2"; shift 2
      ;;
    --token-budget=*) TOKEN_BUDGET="${1#--token-budget=}"; shift ;;
    --max-concurrency)
      [[ $# -ge 2 ]] || usage
      MAX_CONCURRENCY="$2"; shift 2
      ;;
    --max-concurrency=*) MAX_CONCURRENCY="${1#--max-concurrency=}"; shift ;;
    --api-timeout)
      [[ $# -ge 2 ]] || usage
      API_TIMEOUT="$2"; shift 2
      ;;
    --api-timeout=*) API_TIMEOUT="${1#--api-timeout=}"; shift ;;
    --resolution)
      [[ $# -ge 2 ]] || usage
      RESOLUTION="$2"; shift 2
      ;;
    --resolution=*) RESOLUTION="${1#--resolution=}"; shift ;;
    --viz-node-limit)
      [[ $# -ge 2 ]] || usage
      VIZ_NODE_LIMIT="$2"; shift 2
      ;;
    --viz-node-limit=*) VIZ_NODE_LIMIT="${1#--viz-node-limit=}"; shift ;;
    --graphify)
      [[ $# -ge 2 ]] || usage
      GRAPHIFY_BIN="$2"; shift 2
      ;;
    --graphify=*) GRAPHIFY_BIN="${1#--graphify=}"; shift ;;
    --graphifyignore-src)
      [[ $# -ge 2 ]] || usage
      GRAPHIFYIGNORE_SRC="$2"
      GRAPHIFYIGNORE_SRC_SET=1
      SYNC_GRAPHIFYIGNORE=1
      shift 2
      ;;
    --graphifyignore-src=*)
      GRAPHIFYIGNORE_SRC="${1#--graphifyignore-src=}"
      GRAPHIFYIGNORE_SRC_SET=1
      SYNC_GRAPHIFYIGNORE=1
      shift
      ;;
    -h|--help) usage ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      ;;
    *)
      STUDENTS+=("$1")
      shift
      ;;
  esac
done

if [[ "$RUN_ALL" == "1" ]]; then
  while IFS= read -r s; do
    STUDENTS+=("$s")
  done < <(list_students)
fi

[[ ${#STUDENTS[@]} -gt 0 ]] || usage

if [[ "$CLUSTER_ONLY" == "1" && "$SKIP_CLUSTER" == "1" ]]; then
  echo "ERROR: --cluster-only and --skip-cluster conflict" >&2
  exit 1
fi

case "$SCOPE" in
  curated|full) ;;
  *)
    echo "ERROR: --scope must be curated or full (got: $SCOPE)" >&2
    exit 1
    ;;
esac

if [[ "$GRAPHIFYIGNORE_SRC_SET" != "1" ]]; then
  if [[ -n "${GRAPHIFYIGNORE_SRC:-}" ]]; then
    # Env override without --graphifyignore-src flag
    GRAPHIFYIGNORE_SRC_SET=1
  else
    GRAPHIFYIGNORE_SRC="$DEFAULT_GRAPHIFYIGNORE_DIR/.graphifyignore.${SCOPE}"
  fi
fi

# OpenAI-compatible defaults (local NIM unless overridden)
if [[ "$BACKEND" == "openai" ]]; then
  export OPENAI_BASE_URL="${OPENAI_BASE_URL:-$DEFAULT_OPENAI_BASE_URL}"
  export OPENAI_MODEL="${OPENAI_MODEL:-$MODEL}"
  # Local NIM does not require a real key; remote gateways usually do.
  export OPENAI_API_KEY="${OPENAI_API_KEY:-$DEFAULT_OPENAI_API_KEY}"
  if [[ -z "${OPENAI_API_KEY:-}" && "$DRY_RUN" != "1" ]]; then
    echo "ERROR: OPENAI_API_KEY is not set (required for --backend openai)" >&2
    exit 1
  fi
  if [[ "$DRY_RUN" != "1" && "$SKIP_HEALTH_CHECK" != "1" ]]; then
    check_openai_endpoint || exit 1
  fi
fi
[[ "$FORCE" == "1" ]] && export GRAPHIFY_FORCE=1
if [[ -n "$VIZ_NODE_LIMIT" ]]; then
  export GRAPHIFY_VIZ_NODE_LIMIT="$VIZ_NODE_LIMIT"
fi

GRAPHIFY="$(resolve_graphify)"

echo "Repo:          $ROOT" >&2
echo "graphify:      $GRAPHIFY" >&2
echo "backend:       $BACKEND" >&2
echo "model:         $MODEL" >&2
echo "token-budget:  $TOKEN_BUDGET" >&2
echo "concurrency:   $MAX_CONCURRENCY" >&2
echo "api-timeout:   $API_TIMEOUT" >&2
echo "resolution:    $RESOLUTION" >&2
echo "scope:         $SCOPE" >&2
echo "viz-node-limit:${GRAPHIFY_VIZ_NODE_LIMIT:-unset (graphify default)}" >&2
[[ "$BACKEND" == "openai" ]] && echo "OPENAI_BASE_URL=$OPENAI_BASE_URL" >&2
[[ "$CLUSTER_ONLY" == "1" ]] && echo "cluster-only=1 (skip extract)" >&2
[[ "$SKIP_CLUSTER" == "1" ]] && echo "skip-cluster=1" >&2
[[ "$DRY_RUN" == "1" ]] && echo "DRY RUN — no writes / no extract" >&2
[[ "$SYNC_GRAPHIFYIGNORE" == "1" ]] && echo "Sync ignore from: $GRAPHIFYIGNORE_SRC" >&2

mkdir -p "$PUBLIC_DIR" "$LOG_DIR"

# Header only — each process_one appends its own audit row.
# Keep the student loop unredirected so `graphify extract` streams live via tee.
{
  echo -e "student_node\tpublic_path\tstatus\tnotes"
} >"$AUDIT_TSV"

fail_count=0
for student in "${STUDENTS[@]}"; do
  if ! process_one "$student" "$GRAPHIFY"; then
    fail_count=$((fail_count + 1))
  fi
done

write_summary "$AUDIT_TSV"
echo >&2
echo "Wrote $AUDIT_TSV" >&2
echo "Wrote $AUDIT_SUMMARY" >&2
echo "Per-student logs: $LOG_DIR/" >&2

if [[ "$fail_count" -gt 0 ]]; then
  exit 1
fi
