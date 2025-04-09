from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
import time

print('WAITING FOR OTHER SERVICES TO START...')
time.sleep(5)


spark = SparkSession.builder \
    .appName("tp_meteors") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem") \
    .getOrCreate()

schema = T.StructType([
    T.StructField("id", T.StringType()),
    T.StructField("timestamp", T.IntegerType()),
    T.StructField("position", T.MapType(T.StringType(), T.FloatType())),
    T.StructField("vitesse", T.FloatType()),
    T.StructField("taille", T.FloatType()),
    T.StructField("type", T.StringType())
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "space_data") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(F.from_json(F.col("value"), schema).alias("data")) \
    .select("data.*")

checkpoint_location = "hdfs://namenode:9000/checkpoints/meteors"

query = json_df.writeStream \
    .format("parquet") \
    .option("path", "hdfs://namenode:9000/user/spark/data/dangerous_meteors") \
    .option("checkpointLocation", checkpoint_location) \
    .trigger(processingTime="10 seconds") \
    .start()

# Debugging
query2 = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

spark.streams.awaitAnyTermination()

# query.awaitTermination()
