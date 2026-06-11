"""
RDD basics in a script.

Note,

* RDD can be implemented as a per-record store or a key-value store
* When implemented as a key-value store, it is possible for a key
to be repeated
    * As such, this allows you to do things like,
        `rdd.reduceByKey(lambda x, y: x + y)`
    * The preceding operation aggregates values shared
    by the same key
    * Other useful operations,
        `rdd.groupByKey(...)`
        `rdd.sortByKey(...)`
        `rdd.keys(...)`
        `rdd.values(...)`
        `rdd.join(...)`
        `rdd.cogroup(...)`
        `rdd.subtractByKey(...)`
* Note that `mapValues(...)` and `flatMapValues(...)` is more efficient
if your transformation doesn't affect keys - this is because it maintains
the existing partitioning scheme (no re-shuffling required!)
"""
import os

from pyspark import (
    SparkConf,
    SparkContext
)

# ---- 0: Constants ----

SPARK_MASTER: str = os.getenv("SPARK_MASTER_URL", "local")
SPARK_APP_NAME: str = "RDD basics - PySpark"
SPARK_DATA_ROOT: str = "/opt/spark/data"  # NB: bind-mounted to `./spark_data`

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


def parse_record(record):
    fields = record.split(",")
    age = int(fields[2])
    num_friends = int(fields[3])
    return (age, num_friends)


def path_to(filename: str):
    return f"file://{SPARK_DATA_ROOT}/{filename}"


records = sc.textFile(
    path_to("fakefriends.csv")
)

rdd = records.map(parse_record)

# ---- 3: Execution Plan (Lazy Evaluation) ----

plan = (
    rdd
    #   ---- 1: Map values ----
    #      (33 (key), 385 (val)) <-- one record
    #   -> (33      , (385, 1) )
    .mapValues(lambda val: (val, 1))
    #   ---- 2: Reduce by key ----
    #      (33 (key), (385 (x[0]), 1 (x[1]) ) ) <-- first record (x == val1)
    #      (33 (key), (2   (y[0]), 1 (y[1]) ) ) <-- second record (y == val2)
    .reduceByKey(
        lambda val1, val2: (val1[0] + val2[0], val1[1] + val2[1])
    )
    #   ---- 3: Average by age ----
    .mapValues(
        lambda val: val[0] / val[1]
    )
)

# ---- 4: Execution Trigger ----

result = plan.collect()

print(result)
