from audioop import avg
import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('wikipedia most').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wiki_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('view', types.LongType()),
    types.StructField('memory', types.LongType()),
])

def pathConverter(pathname):
    match = re.search(r'\d\d\d\d\d\d\d\d+-+\d\d', pathname)

    if(match):
        return match.group()
    else:
        return None





def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, schema=wiki_schema, sep=' ').withColumn('filename', functions.input_file_name())

    filter_en = data.filter(data['language'] == 'en')
    filter_main = filter_en.filter(filter_en['title'] != 'Main_Page')
    filtered = filter_main.filter(filter_main['title'] != 'Special:')

    path_to_hour = functions.udf(lambda z: pathConverter(z), returnType=types.StringType())
    filtered = filtered.withColumn('filename', path_to_hour('filename')).cache()

    group = filtered.groupBy('filename')
    result = group.agg(functions.max(filtered['view']))

    filtered2 = filtered.join(result, on = 'filename').filter(filtered['view'] == result['max(view)'])
    filtered2 = filtered2.orderBy(['filename'])
    filtered2 = filtered2.drop('language', 'memory', 'max(view)')

    filtered2.show()

    filtered2.write.csv(out_directory, mode='overwrite')
    

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)