#!/usr/bin/env bash
# collect_tegrastats.sh
# Usage: ./collect_tegrastats.sh [output_file] [interval_ms]
# Example: sudo ./collect_tegrastats.sh tegrastats_raw.txt 1000
# Notes:
#   - Requires NVIDIA tegrastats to be available on the Jetson device.
#   - We prepend an ISO-8601 timestamp to each tegrastats line for easy merging.
set -euo pipefail
OUT=${1:-tegrastats_raw.txt}
INTERVAL_MS=${2:-1000}

if ! command -v tegrastats >/dev/null 2>&1; then
  echo "ERROR: tegrastats not found. Install NVIDIA Jetson tools or update your PATH." >&2
  exit 1
fi

stdbuf -oL tegrastats --interval ${INTERVAL_MS} | awk '{ cmd="date +%Y-%m-%dT%H:%M:%S%z"; cmd | getline ts; close(cmd); print ts, $0; fflush(); }' > "$OUT"
