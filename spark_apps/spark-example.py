"""
Outlines the __general__ approach to building Apache Spark applications.

* Cluster configuration details (via `SparkConf` & `SparkContext`)
* Data ingestion
* Execution plan
* Execution trigger (i.e. the trigger for Apache Spark to process)
"""
import os

from pyspark import (
    SparkConf,
    SparkContext
)

# ---- 0: Constants ----

SPARK_MASTER: str = os.getenv("SPARK_MASTER_URL", "local")
SPARK_APP_NAME: str = "Sample Script - PySpark"

# ---- 1: Configuration ----

conf = (
    SparkConf()
    .setMaster(
        SPARK_MASTER
    )
    .setAppName(
        SPARK_APP_NAME
    )
)
sc = SparkContext(conf=conf)

# ---- 2: Data Assembly ----

rdd = sc.parallelize(range(100))

# ---- 3: Execution Plan (Lazy Evaluation) ----

plan = (
    rdd
    .map(lambda x: x * x)
    .filter(lambda x: x % 2 == 0)
)

# ---- 4: Execution Trigger ----

result = plan.collect()

print(result)
