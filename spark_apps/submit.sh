#!/bin/bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <script.py> [script args...]"
    exit 1
fi

script="$1"
shift

spark-submit \
    --master spark://spark-master:7077 \
    --deploy-mode client \
    "/opt/spark/apps/$script" \
    "$@"