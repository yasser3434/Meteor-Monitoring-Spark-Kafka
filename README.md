Meteor Watch - Real-Time Meteor Alerts
Meteor Watch is a web application built with Flask and Apache Spark. It provides an interface to monitor and display meteor objects, as well as alert users about potentially dangerous meteors in real-time, using HDFS (Hadoop Distributed File System) and Kafka for streaming meteor data.

This project utilizes Flask for the web application, PySpark for distributed data processing, and Kafka for streaming data.

Features
Display recent meteor objects.

Display potentially dangerous meteor alerts based on size and speed.

Real-time meteor data streaming and processing.

Integration with Apache Kafka and HDFS.

Project Structure
bash
Copy
Edit
/meteor-watch
│
├── app.py              # Flask API to handle routes
├── streaming_app.py    # Spark streaming application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates for rendering views
│   ├── base.html       # Base layout for all pages
│   ├── home.html       # Home page view
│   └── table.html      # Table view for displaying data
├── static/             # Static files like CSS, JavaScript, images
│   └── style.css       # Custom styles for the app
├── Dockerfile          # Dockerfile for building the container image
└── README.md           # Project documentation
Prerequisites
Docker: To build and run the application in containers.

Kafka: For streaming meteor data. Ensure that Kafka is up and running.

HDFS: To store the meteor data in Hadoop Distributed File System.

Spark: To process the meteor data using Spark streaming.

Install Dependencies
To install the required Python dependencies, use the following command:

bash
Copy
Edit
pip install -r requirements.txt
Make sure you have PySpark, Flask, and Kafka Python client libraries installed.

Required Python Packages:
Flask

PySpark

Pandas

PyArrow (for reading parquet files)

Kafka-python

Running the Application
1. Using Docker (Recommended)
To run the application with Docker, use the following commands:

Build the Docker image:

bash
Copy
Edit
docker build -t meteor-watch .
Start the services using docker-compose: Ensure you have a docker-compose.yml file with the necessary services (e.g., Flask API, Spark, Kafka). Run the following command:

bash
Copy
Edit
docker-compose up
This will launch both the Flask API and the Spark Streaming components, along with the necessary dependencies for Kafka and HDFS.

2. Manually (Without Docker)
If you prefer to run the application without Docker:

Start Kafka and HDFS:

Ensure Kafka is running and accessible.

Ensure HDFS is running and the meteor data is stored in the directory specified in HDFS_DATA_PATH.

Run the Flask API:

bash
Copy
Edit
python app.py
Run the Spark Streaming Application:

bash
Copy
Edit
python streaming_app.py
Application Endpoints
1. / (Home)
Displays a welcoming page with links to the recent meteor objects and dangerous meteor alerts.

GET: /

Response: HTML page with links to view meteor objects and alerts.

2. /objects
Displays the most recent meteor objects.

GET: /objects

Response: JSON list of the most recent meteor objects.

3. /alerts
Displays potentially dangerous meteor alerts based on size (taille) and speed (vitesse).

GET: /alerts

Response: JSON list of dangerous meteor alerts.
