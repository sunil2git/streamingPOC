from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext,dstream



sc = SparkContext("local[2]", "NetworkWordCount")

# Single sparkContext
spark = SparkSession.builder \
.appName('SparkCassandraApp') \
.config('spark.cassandra.connection.host', '127.0.0.1') \
.config('spark.cassandra.connection.port', '9042') \
.config('spark.cassandra.output.consistency.level','ONE') \
.master('local[2]') \
.getOrCreate()

#sc = spark.SparkContext

ssc = StreamingContext(sc, 5)
conf = SparkConf().setAppName("PySpark Cassandra Test")


stream_data = ssc.textFileStream('/Users/acs/PycharmProjects/POC/venv/spark/demo')\
    .map(lambda x: x.split(","))


empdf= spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="emp",keyspace="testkeyspace") \
    .load()
empdf.show()

stream_data.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
