#!/usr/bin/env bash
set -euo pipefail

BLOCK=${1:-}
INPUT=${2:-}

if [[ -z "$BLOCK" || -z "$INPUT" ]]; then
  echo "Usage: run_block.sh <brief|prompt|variation|scene|render|export> <input.json>"
  exit 1
fi

case "$BLOCK" in
  brief|prompt|variation|scene|render|export)
    ;;
  *)
    echo "Unsupported block: $BLOCK"
    exit 2
    ;;
esac

# bkit-lite v1 stub executor: logs and passes through for adapter integration
mkdir -p studio/logs
TS=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$TS] run_block block=$BLOCK input=$INPUT" >> studio/logs/run_block.log

echo "{\"ok\":true,\"block\":\"$BLOCK\",\"input\":\"$INPUT\"}"
