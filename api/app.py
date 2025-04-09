from flask import Flask, render_template, jsonify
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pandas as pd
import pyarrow.parquet as pq

app = Flask(__name__)

spark = SparkSession.builder \
    .appName("HDFS API Example") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem") \
    .getOrCreate()
    
HDFS_DATA_PATH = "hdfs://namenode:9000/user/spark/data/dangerous_meteors"


def load_parquet_data():
    df = spark.read.parquet(HDFS_DATA_PATH)
    return df


@app.route("/")
def home():
    # return jsonify({
    #     "message": "Welcome to Meteor Alerts API",
    #     "endpoints": {
    #         "objects": "/objects - Get recent meteor objects",
    #         "alerts": "/alerts - Get dangerous meteor alerts"
    #     }
    # })
    return render_template("home.html")


@app.route("/objects", methods=["GET"])
def get_objects():
    # df = load_parquet_data()
    # last_20_rows = df.tail(20)  
    # data = [row.asDict() for row in last_20_rows]
    # return jsonify(data)

    df = load_parquet_data()
    last_20_rows = df.orderBy(F.desc("timestamp")).limit(20).toPandas()
    return render_template(
        "table.html",
        title="Recent Meteor Objects",
        data=last_20_rows.to_dict('records')
    )


@app.route("/alerts", methods=["GET"])
def get_alerts():
    # df = load_parquet_data()
    # filtered_df = df.filter((F.col("vitesse") > 25) & (F.col("taille") > 10))
    # last_20_rows = filtered_df.tail(20) 
    # dangerous = [{"id": row["id"], "vitesse": row["vitesse"], "taille": row["taille"], "type": row["type"]} for row in last_20_rows]

    # return jsonify(dangerous)

    df = load_parquet_data()
    dangerous_df = df.filter(
        (F.col("vitesse") > 25) & (F.col("taille") > 10)
    ).orderBy(F.desc("timestamp")).limit(20).toPandas()

    return render_template(
        "table.html",
        title="Dangerous Meteor Alerts",
        data=dangerous_df.to_dict('records')
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
