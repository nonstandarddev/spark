"""
Demonstrates how to 'broadcast' an object in memory across an entire cluster.

In this example, we are broadcasting a relatively small lookup.

Note that this action should be reserved for relatively
small 'reference' tables.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, LongType
from config import path_to


# ---- 0: Config ----


def load_movie_reference():
    """
    Source: https://files.grouplens.org/datasets/movielens/ml-100k/
    """
    movies = {}
    with open(
        "/opt/spark/data/ml-100k/u.item",
        "r",
        encoding='ISO-8859-1',
        errors='ignore'
    ) as f:
        for line in f:
            fields = line.split('|')
            movies[int(fields[0])] = fields[1]
    return movies


spark = (
    SparkSession.builder
    .appName("Spark - Broadcasting Example")
    .getOrCreate()
)


movie_reference = (
    spark
    .sparkContext
    .broadcast(
        load_movie_reference()
    )
)


def lookup_movie(id: int):
    return movie_reference.value[id]


lookup_movie_udf = func.udf(lookup_movie)


schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("movie_id", IntegerType(), True),
    StructField("rating", IntegerType(), True),
    StructField("timestamp", LongType(), True)
])


# ---- 1: Runtime ----


movies_df = (
    spark
    .read
    .option("sep", "\t")
    .schema(schema)
    .csv(path_to("ml-100k/u.data"))
)

top_10 = (
    movies_df
    .groupBy("movie_id")
    .count()
    .withColumn("movie_title", lookup_movie_udf(func.col("movie_id")))
    .orderBy(func.desc("count"))
    .show(10, False)
)


spark.stop()
