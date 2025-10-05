#!/usr/bin/env bash
# -e (errexit)
# Exit immediately if any command returns a non-zero (error) status.

# -u (nounset)
# Treat unset variables as an error and exit immediately.
# Catches typos and missing env vars early.

# -o pipefail
# Makes a pipeline (cmd1 | cmd2 | cmd3) fail if any command in the pipeline fails.
# Without this, only the exit status of the last command is checked.

set -euo pipefail

# List of sub-stacks (folders with docker-compose.yml)
STACKS=(postgres redpanda pgadmin minio) # add spark trino if needed

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

compose_up() {
  local stack="$1"
  local dir="${ROOT_DIR}/${stack}"
  [[ -f "${dir}/docker-compose.yml" ]] || { echo "⚠️  Skipping ${stack}, no compose file"; return; }
  echo "▶️  Bringing up ${stack} ..."
  ( cd "$dir" && docker compose ${ENV_FILE:+--env-file "$ENV_FILE"} up -d )
}

main() {
  local selection="${1:-all}"   # default to "all" if not provided

  if [[ "$selection" == "all" ]]; then
    for s in "${STACKS[@]}"; do compose_up "$s"; done
  else
    IFS=',' read -r -a chosen <<< "$selection"
    for s in "${chosen[@]}"; do compose_up "$s"; done
  fi

  echo "Done. Running Local Development Tech Stack services:"
  for s in "${STACKS[@]}"; do
    if [[ -d "${ROOT_DIR}/${s}" ]]; then
      ( cd "${ROOT_DIR}/${s}" && docker compose ${ENV_FILE:+--env-file "$ENV_FILE"} ps ) || true
    fi
  done
}

main "$@"
