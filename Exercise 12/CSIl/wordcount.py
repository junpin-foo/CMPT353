import sys
from pyspark.sql import SparkSession, functions, types
import string, re

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

def main(in_directory,out_directory):

    data = spark.read.text(in_directory)

    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
    data = data.select(functions.split(data.value, wordbreak).alias('str'))
    data = data.select(functions.explode(data.str))
    data = data.select((functions.lower(data.col)).alias('word'))
    dataGrp = data.groupBy('word').agg((functions.count('word')).alias('count'))
    dataGrp = dataGrp.orderBy(functions.desc('count'), "word").filter(dataGrp['word'] != "")

    dataGrp.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory,out_directory)