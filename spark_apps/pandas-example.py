"""
This script describes how you can use Pandas-style workflows on top of Apache Spark.

Note: I do not necessarily recommend you reach for this style of writing code with Spark because...
well, I do *not* like pandas syntax! ;)

Some notable ideas,

* `spark.createDataFrame()` -> creates a pyspark DataFrame for downstream manipulation i.e. when you
call this constructor, you now have to use pyspark syntax to process the DataFrame.
* `ps.DataFrame()` -> creates a pyspark DataFrame, under the hood; *but* this time you can use pandas
syntax to process this data; operations will be distributed within the cluster.
"""
import pyspark
import pandas as pd
import pyspark.pandas as ps
import os

from pyspark.sql import SparkSession
from config import path_to


# ---- 1: Configuration ----


os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"


spark = (
    SparkSession.builder
    .appName("Pandas with Spark")
    .config("spark.sql.ansi.enabled", "false")
    .config("spark.executorEnv.PYARROW_IGNORE_TIMEZONE", "1")
    .getOrCreate()
)


# ---- 2: Pandas to Spark ----

# NB: here we are leaving the Pandas world when we execute `spark.createDataFrame()`

pd_df: pd.DataFrame = pd.DataFrame({
    "id": [1, 2, 3, 4, 5],
    "name": ["alice", "bob", "charlie", "david", "emma"],
    "age": [25, 30, 35, 40, 45]
})

spark_df: pyspark.sql.DataFrame = spark.createDataFrame(pd_df)
spark_df.show()

spark_filtered_df = spark_df.filter(spark_df.age > 30)
spark_filtered_df.show()


# ---- 3: Pandas *on* Spark ----

# NB: here we are staying in the Pandas world (from an API perspective) when we execute `ps.DataFrame()`

ps_df: pd.DataFrame = ps.DataFrame(pd_df)

ps_df["age"] = ps_df["age"] + 1
print(ps_df)

spark.stop()