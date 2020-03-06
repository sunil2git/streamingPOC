
# Creating PySpark Context
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.streaming import StreamingContext

from pyspark.sql import Row
from pyspark.sql import functions
#from cassandra.cqlengine import connection

import com.datastax.spark.connector
import com.datastax.spark.connector.cql


import os

spark = SparkSession.builder \
.appName('SparkCassandraApp') \
.config('spark.cassandra.connection.host', '127.0.0.1') \
.config('spark.cassandra.connection.port', '9042') \
.config('spark.cassandra.output.consistency.level','ONE') \
.master('local[2]') \
.getOrCreate()



#df = spark.read.format("org.apache.spark.sql.cassandra").options(table = "emp", keyspace = "testkeyspace").load()
load_options = { "table": "emp", "keyspace": "testkeyspace", "spark.cassandra.input.split.size_in_mb": "10"}

empdf= spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="emp",keyspace="testkeyspace") \
    .load()


empdf.write\
.format("org.apache.spark.sql.cassandra")\
.mode('append')\
.options(table="tempemp", keyspace="temp")\
.save()

print("Data Inserted")
