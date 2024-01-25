FROM flink:1.18.1
ARG FLINK_VERSION=1.18.1

# From apache flink docs for custom build with pyflink

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    python -m pip install --upgrade pip; \
    pip install apache-flink==${FLINK_VERSION}; \
    pip install kafka-python;


RUN   wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector/${FLINK_VERSION}/flink-connector-${FLINK_VERSION}.jar && \
      wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/${FLINK_VERSION}/flink-sql-connector-kafka-${FLINK_VERSION}.jar; \
      wget -P /opt/flink/lib/ https://jdbc.postgresql.org/download/postgresql-42.2.19.jar


COPY requirements.txt /opt/flink/
RUN pip install --no-cache-dir -r /opt/flink/requirements.txt
