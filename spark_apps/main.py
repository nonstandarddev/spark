from pyspark import (
    SparkConf,
    SparkContext
)

conf = (
    SparkConf()
    .setAppName("Sample Script - PySpark")
)
sc = SparkContext(conf=conf)

rdd = sc.parallelize(range(100))

plan = (
    rdd
    .map(lambda x: x * x)
    .filter(lambda x: x % 2 == 0)
)

result = plan.collect()

print(result)
