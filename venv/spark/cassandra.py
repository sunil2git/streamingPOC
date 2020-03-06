
# Creating PySpark Context
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.streaming import StreamingContext

from pyspark.sql import Row
from pyspark.sql import functions
#from cassandra.cqlengine import connection

#from cassandra import datastax
import com.datastax.spark.connector.cql


import os

"spark = SparkSession.builder \
.appName('SparkCassandraApp') \
.config('spark.cassandra.connection.host', '127.0.0.1') \
.config('spark.cassandra.connection.port', '9042') \
.config('spark.cassandra.output.consistency.level','ONE') \
.master('local[2]') \
.getOrCreate()"


#conf = SparkConf().setMaster("local[*]").setAppName("streaming-test").set("spark.cassandra.connection.host", "127.0.0.1")

conf = SparkConf()
conf.setMaster("local[*]")
conf.setAppName("Spark Cassandra")
conf.set("spark.cassandra.connection.host","127.0.0.1")

sc = SparkContext(conf=conf)




ssc = StreamingContext(conf, 5)


print(ssc)
#df = spark.read.format("org.apache.spark.sql.cassandra").options(table = "emp", keyspace = "testkeyspace").load()



'''empDF= spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="emp",keyspace="testkeyspace") \
    .load().show()'''

#data= ssc.queueStream(ssc,empDF)


ssc.start()
ssc.awaitTermination()


 #data = empDF.isStreaming()




# 2nd method to load data into dataFrame
'''load_options = { "table": "tempemp", "keyspace": "temp", "spark.cassandra.input.split.size_in_mb": "10"}
spark.read.format("org.apache.spark.sql.cassandra").options(**load_options).load().show()'''

print("data inserting process started")
'''empDF.write\
    .format("org.apache.spark.sql.cassandra") \
    .mode('append') \
    .options(table="tempemp", keyspace="temp")\
    .save()'''

print("data inserted")


