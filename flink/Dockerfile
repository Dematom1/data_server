FROM flink:1.18.1
ARG FLINK_VERSION=1.18.1

# From apache flink docs for custom build with pyflink

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    apt-get install -y default-jdk && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    python -m pip install --upgrade pip && \
    pip install apache-flink==${FLINK_VERSION}



RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector/${FLINK_VERSION}/flink-connector-${FLINK_VERSION}.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${FLINK_VERSION}/flink-sql-connector-kafka-${FLINK_VERSION}.jar && \
    wget -P /opt/flink/lib/ https://jdbc.postgresql.org/download/postgresql-42.2.19.jar

COPY requirements.txt /opt/flink/
RUN pip install --no-cache-dir -r /opt/flink/requirements.txt


# # Start from the OpenJDK image
# FROM openjdk:17.0.1
# ARG FLINK_VERSION=1.18.0

# # Install Python and other necessary components
# RUN apt-get update && \
#     apt-get install -y wget software-properties-common python3 python3-pip python3-dev && \
#     ln -s /usr/bin/python3 /usr/bin/python && \
#     python -m pip install --upgrade pip && \
#     pip install apache-flink==${FLINK_VERSION}

# # Download Flink connectors and JDBC driver
# RUN mkdir -p /opt/flink/lib && \
#     wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka_${FLINK_VERSION}/flink-connector-kafka_${FLINK_VERSION}-${FLINK_VERSION}.jar && \
#     wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_${FLINK_VERSION}/flink-sql-connector-kafka_${FLINK_VERSION}-${FLINK_VERSION}.jar && \
#     wget -P /opt/flink/lib/ https://jdbc.postgresql.org/download/postgresql-42.2.19.jar

# # Copy your application files
# COPY requirements.txt /opt/flink/
# RUN pip install --no-cache-dir -r /opt/flink/requirements.txt


# FROM python:3.8-slim

# # Install OpenJDK
# RUN apt-get update && \
#     apt-get install -y openjdk-17-jdk && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Set environment variable for Java
# ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
# ENV PATH $JAVA_HOME/bin:$PATH

# # Install Apache Flink
# ARG FLINK_VERSION=1.18.0
# RUN pip install --upgrade pip && \
#     pip install apache-flink==${FLINK_VERSION}

# # Install Flink connectors and JDBC driver
# RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector/${FLINK_VERSION}/flink-connector-${FLINK_VERSION}.jar && \
#     wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${FLINK_VERSION}/flink-sql-connector-kafka-${FLINK_VERSION}.jar && \
#     wget -P /opt/flink/lib/ https://jdbc.postgresql.org/download/postgresql-42.2.19.jar

# # Copy requirements and install additional Python dependencies
# COPY requirements.txt /opt/flink/
# RUN pip install --no-cache-dir -r /opt/flink/requirements.txt
