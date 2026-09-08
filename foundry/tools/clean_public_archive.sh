#!/usr/bin/env bash
# Extract a private Hermes brain tarball into foundry/harvest/<id>/brains/<node>/sage/,
# keeping only brain-contribution content and scrubbing secrets.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRIVATE_ARCHIVES="${PRIVATE_ARCHIVES:-$ROOT/foundry/.work/private/archives}"
PUBLIC_ARCHIVES="${PUBLIC_ARCHIVES:-$ROOT/foundry/harvest/1_4_0/brains}"
PUBLIC_DIR="${PUBLIC_DIR:-$ROOT/foundry/.work}"
REDACT_PY="$SCRIPT_DIR/redact_secrets.py"

SKIP_STUDENTS=("nseveryns_node-H042")

DROP_DIRS=(
  home bin lsp .venv-graphify
  cache audio_cache image_cache images
  sandboxes pairing plans skins workspace hooks
)

DROP_FILES=(
  auth.json auth.lock .env
  models_dev_cache.json provider_models_cache.json ollama_cloud_models_cache.json
  context_length_cache.yaml
  interrupt_debug.log processes.json .update_check .DS_Store
)

TAR_EXCLUDES=(
  --exclude='sage/home'
  --exclude='sage/home/*'
  --exclude='*/home'
  --exclude='*/home/*'
  --exclude='sage/bin'
  --exclude='sage/bin/*'
  --exclude='*/bin'
  --exclude='*/bin/*'
  --exclude='sage/lsp'
  --exclude='sage/lsp/*'
  --exclude='*/lsp'
  --exclude='*/lsp/*'
  --exclude='sage/.venv-graphify'
  --exclude='sage/.venv-graphify/*'
  --exclude='*/.venv-graphify'
  --exclude='*/.venv-graphify/*'
  --exclude='sage/cache'
  --exclude='sage/cache/*'
  --exclude='sage/audio_cache'
  --exclude='sage/audio_cache/*'
  --exclude='sage/image_cache'
  --exclude='sage/image_cache/*'
  --exclude='sage/images'
  --exclude='sage/images/*'
  --exclude='sage/sandboxes'
  --exclude='sage/sandboxes/*'
  --exclude='sage/pairing'
  --exclude='sage/pairing/*'
  --exclude='sage/plans'
  --exclude='sage/plans/*'
  --exclude='sage/skins'
  --exclude='sage/skins/*'
  --exclude='sage/workspace'
  --exclude='sage/workspace/*'
  --exclude='sage/hooks'
  --exclude='sage/hooks/*'
)

usage() {
  echo "Usage: $0 <private-tar.gz> | --all" >&2
  exit 1
}

is_skipped() {
  local student="$1"
  local s
  for s in "${SKIP_STUDENTS[@]}"; do
    [[ "$student" == "$s" ]] && return 0
  done
  return 1
}

join_notes() {
  local IFS='; '
  echo "$*"
}

bytes_of() {
  if [[ -f "$1" ]]; then
    stat -f%z "$1" 2>/dev/null || stat -c%s "$1"
  elif [[ -d "$1" ]]; then
    du -sk "$1" | awk '{print $1 * 1024}'
  else
    echo 0
  fi
}

human_size() {
  local b="$1"
  awk -v b="$b" 'BEGIN {
    split("B KB MB GB TB", u, " ");
    s=b+0;
    i=1;
    while (s >= 1024 && i < 5) { s/=1024; i++ }
    printf (i==1 ? "%d%s" : "%.1f%s"), s, u[i]
  }'
}

drop_runtime() {
  local sage_dir="$1"
  local name
  [[ -d "$sage_dir" ]] || return 0
  chmod -R u+rwX "$sage_dir" 2>/dev/null || true
  for name in "${DROP_DIRS[@]}"; do
    if [[ -e "$sage_dir/$name" ]]; then
      find "$sage_dir/$name" -type d -exec chmod u+rwx {} + 2>/dev/null || true
      find "$sage_dir/$name" -type f -exec chmod u+rw {} + 2>/dev/null || true
      rm -rf "$sage_dir/$name"
    fi
  done
  for name in "${DROP_FILES[@]}"; do
    rm -f "$sage_dir/$name" 2>/dev/null || true
  done
  find "$sage_dir" -name '.DS_Store' -delete 2>/dev/null || true
}

redact_secrets() {
  local sage_dir="$1"
  python3 "$REDACT_PY" "$sage_dir"
}

normalize_to_sage() {
  local dest_student="$1"
  local sage_dir="$dest_student/sage"

  if [[ -d "$sage_dir" ]]; then
    echo "$sage_dir"
    return 0
  fi

  if [[ -d "$dest_student/default" ]]; then
    mv "$dest_student/default" "$sage_dir"
    echo "$sage_dir"
    return 0
  fi

  # Flat root (veday): skills/, memories/, docs/ etc. at student dir
  if [[ -d "$dest_student/skills" || -d "$dest_student/memories" || -f "$dest_student/AGENTS.md" ]]; then
    mkdir -p "$sage_dir"
    local item base
    shopt -s dotglob nullglob
    for item in "$dest_student"/*; do
      base="$(basename "$item")"
      [[ "$base" == "sage" ]] && continue
      mv "$item" "$sage_dir/"
    done
    shopt -u dotglob nullglob
    echo "$sage_dir"
    return 0
  fi

  echo "ERROR: could not find sage/ (or normalizable root) under $dest_student" >&2
  return 1
}

process_one_tsv() {
  local tar_path="$1"
  local scrub_only="${2:-0}"

  [[ -f "$tar_path" ]] || { echo "Missing tar: $tar_path" >&2; return 1; }

  local student
  student="$(basename "$(dirname "$tar_path")")"
  local size_before
  size_before="$(bytes_of "$tar_path")"
  local rel_private="private/archives/${student}/$(basename "$tar_path")"
  local public_path="public/archives/${student}/sage"
  local dest_student="$PUBLIC_ARCHIVES/$student"
  local notes=()
  local row_status

  if is_skipped "$student"; then
    row_status="SKIPPED"
    notes+=("wrong profile root (default/); not a correct sage profile; not extracted to public")
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$student" "$rel_private" "" "$row_status" "$size_before" "0" "$(join_notes "${notes[@]}")"
    echo "[SKIP] $student" >&2
    return 0
  fi

  mkdir -p "$dest_student"

  if [[ "$scrub_only" == "1" ]]; then
    row_status="SCRUB_ONLY"
    notes+=("already extracted; scrub + drop-list only")
    echo "[SCRUB] $student" >&2
  else
    row_status="SUCCESS"
    rm -rf "$dest_student"
    mkdir -p "$dest_student"
    echo "[EXTRACT] $student from $(basename "$tar_path")" >&2
    tar -xzf "$tar_path" -C "$dest_student" "${TAR_EXCLUDES[@]}"
    notes+=("selective extract with bulk excludes")
  fi

  local sage_dir
  if ! sage_dir="$(normalize_to_sage "$dest_student")"; then
    row_status="FAILED"
    notes+=("normalize_to_sage failed")
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$student" "$rel_private" "" "$row_status" "$size_before" "0" "$(join_notes "${notes[@]}")"
    return 1
  fi

  if [[ "$student" == "node-H03A" ]]; then
    notes+=("nonstandard tar root; wrapped into sage/")
  fi

  drop_runtime "$sage_dir"
  notes+=("removed runtime/bulk/credential paths")

  local redacted
  redacted="$(redact_secrets "$sage_dir" || echo 0)"
  notes+=("redacted_files=${redacted}")

  local size_after
  size_after="$(bytes_of "$dest_student")"

  # Pack cleaned sage/ into a tarball alongside the tree (same folder layout as private).
  local public_tar="$dest_student/${student}_public_sage.tar.gz"
  tar -czf "$public_tar" -C "$dest_student" sage
  notes+=("wrote $(basename "$public_tar")")
  size_after="$(bytes_of "$dest_student")"

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$student" "$rel_private" "$public_path" "$row_status" "$size_before" "$size_after" "$(join_notes "${notes[@]}")"

  echo "[DONE] $student $(human_size "$size_before") -> $(human_size "$size_after") ($row_status); tar=$(basename "$public_tar")" >&2
}

write_audit_summary() {
  local audit_tsv="$1"
  local summary="$PUBLIC_DIR/audit-summary.md"
  local date_str
  date_str="$(date +%Y-%m-%d)"

  local success scrubbed skipped failed
  success="$(awk -F'\t' 'NR>1 && $4=="SUCCESS" {c++} END{print c+0}' "$audit_tsv")"
  scrubbed="$(awk -F'\t' 'NR>1 && $4=="SCRUB_ONLY" {c++} END{print c+0}' "$audit_tsv")"
  skipped="$(awk -F'\t' 'NR>1 && $4=="SKIPPED" {c++} END{print c+0}' "$audit_tsv")"
  failed="$(awk -F'\t' 'NR>1 && $4=="FAILED" {c++} END{print c+0}' "$audit_tsv")"
  local total=$((success + scrubbed + skipped + failed))
  local published=$((success + scrubbed))

  {
    echo "# Hermes Public Brain Cleanup Audit — ${date_str}"
    echo
    echo "## Outcome"
    echo
    echo "- Private archives considered: ${total}"
    echo "- Published to \`public/archives/\` (cleaned): ${published}"
    echo "  - Fresh extract + clean: ${success}"
    echo "  - Already present; scrub-only: ${scrubbed}"
    echo "- Skipped (not a correct sage profile): ${skipped}"
    if [[ "$failed" -gt 0 ]]; then
      echo "- Failed: ${failed}"
    fi
    echo "- Private originals left untouched under \`private/archives/\`"
    echo
    echo "## Successful public brains"
    echo
    echo "| Student folder | Status | Public path | Private tar (bytes) | Public tree (bytes) |"
    echo "| --- | --- | --- | --- | --- |"
    awk -F'\t' 'NR>1 && ($4=="SUCCESS" || $4=="SCRUB_ONLY") {
      printf "| `%s` | %s | `%s` | %s | %s |\n", $1, $4, $3, $5, $6
    }' "$audit_tsv"
    echo
    echo "## Skipped"
    echo
    local skip_lines
    skip_lines="$(awk -F'\t' 'NR>1 && $4=="SKIPPED" {
      printf "- `%s` — %s\n", $1, $7
    }' "$audit_tsv")"
    if [[ -n "$skip_lines" ]]; then
      echo "$skip_lines"
    else
      echo "- (none)"
    fi
    echo
    echo "## Processing rules applied"
    echo
    echo "Keep (brain contribution): \`memories/\`, \`skills/\`, \`sessions/\`, \`state.db*\`, profile docs (\`SOUL.md\`, \`AGENTS.md\`, \`config.yaml\`, …), Graphify artifacts, \`pastes/\`, \`scripts/\`, logs/history templates."
    echo
    echo "Delete: \`home/\`, \`bin/\`, \`lsp/\`, \`.venv-graphify/\`, runtime caches, empty runtime dirs, \`auth.json\`, \`.env\`, model catalog caches, debug noise."
    echo
    echo "Secrets: credential files removed; common API key/token patterns in kept text files replaced with \`[REDACTED]\`."
    echo
    echo "Folder layout: \`public/archives/<student_node>/sage/\` plus \`<student_node>_public_sage.tar.gz\` (same student folder names as private; tarball contains top-level \`sage/\`)."
    echo
    echo "See \`audit.tsv\` for per-archive source path, sizes, status, and notes."
  } >"$summary"
}

run_all_clean() {
  local audit_tsv="$PUBLIC_DIR/audit.tsv"
  mkdir -p "$PUBLIC_ARCHIVES" "$PUBLIC_DIR"
  {
    echo -e "student_node\tsource_private_archive\tpublic_path\tstatus\tsize_bytes_before\tsize_bytes_after\tnotes"
    local tar_path student scrub
    for tar_path in "$PRIVATE_ARCHIVES"/*/*.tar.gz; do
      student="$(basename "$(dirname "$tar_path")")"
      scrub=0
      # Prefer scrub-only when a cleaned sage tree already exists (no home/ bulk).
      if [[ -d "$PUBLIC_ARCHIVES/$student/sage" && ! -d "$PUBLIC_ARCHIVES/$student/sage/home" ]]; then
        scrub=1
      fi
      process_one_tsv "$tar_path" "$scrub"
    done
  } >"$audit_tsv"

  write_audit_summary "$audit_tsv"
  echo "Wrote $audit_tsv and $PUBLIC_DIR/audit-summary.md" >&2
}

main() {
  if [[ "${1:-}" == "--all" ]]; then
    run_all_clean
  elif [[ -n "${1:-}" ]]; then
    process_one_tsv "$1" 0
  else
    usage
  fi
}

main "$@"
