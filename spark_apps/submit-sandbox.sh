#!/bin/bash
set -euo pipefail

spark-sql -i ./sql/sandbox.sql \
    --conf spark.sql.warehouse.dir=/opt/spark/data/dwh \
    --database sandbox
