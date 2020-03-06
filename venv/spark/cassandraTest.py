from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark import SparkContext


conf = SparkConf() \
	.setAppName("PySpark Cassandra Test") \
	.setMaster("spark://192.192.141.21:7077") \
	.set("spark.cassandra.connection.host", "192.192.141.26:9042")

sc = SparkContext("local", "Filter app")

sc = CassandraSparkContext(conf=conf)
# sc = SparkContext(conf=conf)
# sqlContext = SQLContext(sc)
#sc = SQLContext(conf=conf)
dd = sc.cassandraTable("emp", "testkeyspace")\
	.collect()

print(dd)
