import time
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.types import *


if __name__ == "__main__":

 sc = SparkContext(appName="PythonStreamingQueueStream")
ssc = StreamingContext(sc, 3)


spark = SparkSession.builder \
.appName('SparkCassandraApp') \
.config('spark.cassandra.connection.host', '127.0.0.1') \
.config('spark.cassandra.connection.port', '9042') \
.config('spark.cassandra.output.consistency.level','ONE') \
.master('local[2]') \
.getOrCreate()

rddQueue = []
for i in range(5):
 rddQueue += [ssc.sparkContext.parallelize([j for j in range(1, 1001)], 10)]



#dfValues = []
dfValues = ssc.sparkContext.parallelize([(1, 2, 3, 'a b c'),
                                      (4, 5, 6, 'd e f'),
                                      (7, 8, 9, 'g h i')]).toDF(['col1', 'col2', 'col3', 'col4'])
dfValues.show()

schema = StructType([
    StructField("column1",IntegerType(),True),
    StructField("column2",IntegerType(), True),
    StructField("column3",IntegerType(), True),
    StructField("column4",StringType(),True)
])
empty = spark.createDataFrame(sc.emptyRDD(), schema)

empty = empty.unionAll(ssc.sparkContext.parallelize([(1, 2, 3, 'a b c'),
                                      (4, 5, 6, 'd e f'),
                                      (7, 8, 9, 'g h i')]).toDF(['col1', 'col2', 'col3', 'col4']))

testrdds = dfValues.rdd
tCollect = testrdds.collect()

emptyRdd = []
emptyRdd += tCollect

print(testrdds.collect)

rdd=[]
rdd += [ssc.sparkContext.parallelize([(1,2,3,4,5,6)])]#.toDF(['col1', 'col2', 'col3', 'col4'])
inputStream = ssc.queueStream(emptyRdd)
inputStream.pprint()

ssc.start()
time.sleep(6)
ssc.stop(stopSparkContext=True, stopGraceFully=True)