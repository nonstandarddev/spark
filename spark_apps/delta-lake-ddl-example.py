"""
Processing Delta Lake I/O (DDL) via `pyspark`.
"""
import config
from pyspark.sql import SparkSession

# ---- 1: Configuration ----

spark = (
    SparkSession.builder
    .appName("SQL with Spark")
    .config("spark.sql.warehouse.dir", f"{config.SPARK_DATA_ROOT}/dwh")
    .config("spark.sql.ansi.enabled", "false")
    .getOrCreate()
)

# ---- 2: Spark SQL (DDL) ----

spark.sql(
    """
    -- SQL
    CREATE TABLE IF NOT EXISTS foo (
        bar LONG,
        baz STRING,
        bam STRING
    ) USING DELTA;
    """
)

spark.stop()
