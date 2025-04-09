FROM bitnami/spark:latest

WORKDIR /app
COPY batch_analysis.py .

CMD ["sh", "-c", "sleep 30 && /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 /app/batch_analysis.py"]