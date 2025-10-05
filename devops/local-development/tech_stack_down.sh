#!/usr/bin/env bash
set -euo pipefail

STACKS=(postgres redpanda pgadmin minio) # keep in sync with up.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ROOT_DIR}/.env"

compose_down() {
  local stack="$1"
  local dir="${ROOT_DIR}/${stack}"
  [[ -f "${dir}/docker-compose.yml" ]] || { echo "⚠️  Skipping ${stack}, no compose file"; return; }
  echo "⏹️  Stopping ${stack} ..."
  ( cd "$dir" && docker compose ${ENV_FILE:+--env-file "$ENV_FILE"} down -v )
}

main() {
  local selection="${1:-all}"   # default to "all" if not provided

  if [[ "$selection" == "all" ]]; then
    for (( i=${#STACKS[@]}-1; i>=0; i-- )); do compose_down "${STACKS[$i]}"; done
  else
    IFS=',' read -r -a chosen <<< "$selection"
    for s in "${chosen[@]}"; do compose_down "$s"; done
  fi

  echo "Done Shutting Down Local Development Tech Stack Services."
}

main "$@"
