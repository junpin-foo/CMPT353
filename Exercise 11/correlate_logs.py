import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
import math

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        hostname = m.group(1) 
        bytesTrans = m.group(2)
        return Row(hostname=str(hostname), bytesTransfered=float(bytesTrans))

        # TODO
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    row = log_lines.map(line_to_row)
    cleaned = row.filter(not_none)

    return cleaned
    # TODO: return an RDD of Row() objects


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    logs = logs.groupby("hostname").agg(functions.count("hostname"),functions.sum("bytesTransfered"))

    data = logs.agg(
        (functions.count("hostname")).alias("n"),
        (functions.sum("count(hostname)")).alias("x"),
        (functions.sum("sum(bytesTransfered)")).alias("y"),
        (functions.sum(logs["count(hostname)"]**2)).alias("x2"),
        (functions.sum(logs["sum(bytesTransfered)"]**2)).alias("y2"),
        (functions.sum(logs["count(hostname)"] * logs["sum(bytesTransfered)"])).alias("xy")
    )

    data = data.first()

    r = (data["n"] * data["xy"] - data["x"] * data["y"]) / (math.sqrt(data["n"] * data["x2"] - data["x"]**2) * math.sqrt(data["n"] * data["y2"] - data["y"]**2 ))


    print("r = %g\nr^2 = %g" % (r, r**2))

if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
