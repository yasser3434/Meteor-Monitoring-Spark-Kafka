FROM bitnami/spark:latest

WORKDIR /app
COPY . .
CMD ["sh", "-c", "sleep 5 && /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /app/streaming_app.py"]