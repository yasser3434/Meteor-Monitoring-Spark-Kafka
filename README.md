# Meteor Watch - Real-Time Meteor Alerts

Meteor Watch is a web application built with Flask and Apache Spark. It provides an interface to monitor and display meteor objects, as well as alert users about potentially dangerous meteors in real-time, using HDFS (Hadoop Distributed File System) and Kafka for streaming meteor data.

## Prerequisites

- **Docker**: To build and run the application in containers.
- **Kafka**: For streaming meteor data. Ensure that Kafka is up and running.
- **HDFS**: To store the meteor data in Hadoop Distributed File System.
- **Spark**: To process the meteor data using Spark streaming.

## Install Dependencies

To install the required Python dependencies

## HDFS
Create the directory and change the permissions
hdfs dfs -chmod 777 /user/spark/data

## RUN
``` docker compose un --build ```
Re run the producer is you're getting error
``` docker compose up --build producer ```
