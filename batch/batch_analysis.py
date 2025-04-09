from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

def run_batch_analysis():
    spark = SparkSession.builder \
        .appName("MeteorBatchAnalysis") \
        .master("spark://spark-master:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
        .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem") \
        .getOrCreate()
    
    time_24h_ago = int((datetime.now() - timedelta(hours=24)).timestamp())
    
    hdfs_data_path = "hdfs://namenode:9000/user/spark/data/dangerous_meteors"
    df = spark.read.parquet(hdfs_data_path)
    
    recent_df = df.filter(F.col("timestamp") >= time_24h_ago)
    
    # ================================ OBJ COUNT
    type_counts = recent_df.groupBy("type").count()
    
    log.info("=== METEOR Objectd Counts by Type ===")
    type_counts.show()
    
    # ================================ 5 FASTEST OBJ
    windowSpec = Window.partitionBy("type").orderBy(F.desc("vitesse"))
    fastest_per_type = recent_df.withColumn("rank", F.row_number().over(windowSpec)) \
                              .filter(F.col("rank") <= 5) \
                              .drop("rank") \
                              .orderBy(F.desc("vitesse"))
    
    log.info("=== Top 5 Fastest Objects Detected in Last 24 Hours ===")
    fastest_per_type.show(5)
    
    # ================================ 5 AVG SPEED
    avg_speed = recent_df.groupBy("type").agg(
        F.avg("vitesse").alias("avg_speed"),
        F.max("vitesse").alias("max_speed"),
        F.min("vitesse").alias("min_speed")
    ).orderBy(F.desc("avg_speed"))
    
    log.info("=== Average Speed by Object Type ===")
    avg_speed.show()
    
    # spark.stop()

if __name__ == "__main__":
    run_batch_analysis()