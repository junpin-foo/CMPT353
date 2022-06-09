import sys
from pyspark.sql import SparkSession, functions, types

data = spark.read.text(sys.argv[1])
