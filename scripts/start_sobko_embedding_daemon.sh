#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p .omx/logs .omx/state

if curl -sf http://127.0.0.1:8769/health >/dev/null 2>&1; then
  echo "Sobko embedding daemon already running:"
  curl -s http://127.0.0.1:8769/health
  echo
  exit 0
fi

setsid python scripts/run_embedding_daemon.py > .omx/logs/sobko-embedding-daemon.log 2>&1 < /dev/null &
echo $! > .omx/state/sobko-embedding-daemon.pid
sleep 3

echo "Sobko embedding daemon started. PID=$(cat .omx/state/sobko-embedding-daemon.pid)"
curl -s http://127.0.0.1:8769/health
echo
