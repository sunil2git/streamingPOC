

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, current_timestamp
from pyspark.sql.functions import split
from pyspark.sql.functions import window
from pyspark.sql.types import StructType, TimestampType
from pyspark.streaming import StreamingContext


staging_dir = 'monitoring_data'

spark = SparkSession.builder \
.appName('SparkCassandraApp') \
.config('spark.cassandra.connection.host', '127.0.0.1') \
.config('spark.cassandra.connection.port', '9042') \
.config('spark.cassandra.output.consistency.level','ONE') \
.master('local[2]') \
.getOrCreate()

userSchema = StructType()\
              .add("id", "integer")\
              .add("name", "string")
              # .add("dept", "integer")
#spark.read.format("csv").option("header", "false").load("/Users/acs/Documents/sparkData/op/matches.csv").show()


activity = spark.readStream \
.option("sep", ",")\
.schema(userSchema)\
.csv("/Users/acs/Documents/sparkData/op/")

#
# .schema(userSchema)\
#print(activity)

Employee = spark.createDataFrame([
                        ('1', 'Joe',   '70000', '1'),
                        ('2', 'Henry', '80000', '2'),
                        ('3', 'Sam',   '60000', '2'),
                        ('4', 'Max',   '90000', '1')],
                        ['Id', 'name', 'salary','dept']
)


'''query = activity \
    .writeStream.trigger(processingTime='10 seconds') \
    .format("parquet") \
    .option("checkpointLocation", "applicationHistory") \
    .option("path", staging_dir + "/out") \
    .start()'''


# query = activity \
#     .writeStream.trigger(processingTime='2 seconds') \
#     .format("parquet") \
#     .option("checkpointLocation", "applicationHistory") \
#     .option("/Users/acs/Documents/sparkData/empDfSave/") \
#     .start()

# activity.write\
#     .format("org.apache.spark.sql.cassandra") \
#     .mode('append') \
#     .options(table="stream", keyspace="temp")\
#     .save()


query2 = activity \
    .writeStream \
    .trigger(processingTime='2 seconds') \
    .format("console") \
    .start()

query2.awaitTermination()