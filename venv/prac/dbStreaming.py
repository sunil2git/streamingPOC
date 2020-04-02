
# Creating PySpark Context
from pyspark import SparkContext, SparkConf
import time
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.types import *
from pyspark.sql import SQLContext, SparkSession
from pyspark.streaming import StreamingContext

from pyspark.sql import Row
from pyspark.sql import functions
#from cassandra.cqlengine import connection

#from cassandra import datastax
import com.datastax.spark.connector.cql


import os

sc = SparkContext(appName="PythonStreamingQueueStream")
ssc = StreamingContext(sc, 3)

spark = SparkSession.builder \
.appName('SparkCassandraApp') \
.config('spark.cassandra.connection.host', '127.0.0.1') \
.config('spark.cassandra.connection.port', '9042') \
.config('spark.cassandra.output.consistency.level','ONE') \
.master('local[2]') \
.getOrCreate()

# To test the database value using RDD
# we get the RDD by converting the DF of table data
# Issue :  Ones data load in the DF then it only stream data not the new arrival data
empDF=spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="emp",keyspace="testkeyspace") \
    .load()

collectRdd= empDF.rdd.collect()
print(empDF.rdd.collect())

emptyRdd = []
emptyRdd += collectRdd


print("data inserting process started")
# empDF.write\
#     .format("org.apache.spark.sql.cassandra") \
#     .mode('append') \
#     .options(table="tempemp", keyspace="temp")\
#     .save()



print("data inserted")

inputStream = ssc.queueStream(emptyRdd)
inputStream.pprint()

ssc.start()
time.sleep(6)
ssc.awaitTermination()
# ssc.stop(stopSparkContext=True, stopGraceFully=True)


