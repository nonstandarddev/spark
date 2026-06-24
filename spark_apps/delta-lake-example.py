"""
Outlines the __general__ approach to utilising Delta Lake via Apache Spark.

This workload must be administered via `spark-submit`,

`make submit app=delta-lake-example.py`.
"""
from pyspark.sql import (
    SparkSession
)
from config import (
    SPARK_MASTER,
    SPARK_DATA_ROOT
)


# ---- 1: Configuration ----

SPARK_APP_NAME: str = "Delta Lake (via Spark) - Test"

spark = (
  SparkSession.builder
  .master(
    SPARK_MASTER
  )
  .appName(
    SPARK_APP_NAME
  )
  .getOrCreate()
)

# ---- 2: Runtime ----

# Create a Spark DataFrame
data = spark.range(0, 5)

# Write to a Delta Lake table
(
    data
    .write
    .format("delta")
    .mode("overwrite")
    .save(f"{SPARK_DATA_ROOT}/delta-table")
)

# Read from the Delta Lake table
df = (
    spark
    .read
    .format("delta")
    .load(f"{SPARK_DATA_ROOT}/delta-table")
    .orderBy("id")
)

df.show()
