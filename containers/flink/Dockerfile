FROM flink:1.17.0

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip default-jdk python3-dev openjdk-11-jdk && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.17.0/flink-sql-connector-kafka-1.17.0.jar && wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.0.0-1.16/flink-connector-jdbc-3.0.0-1.16.jar && wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar


COPY requirements.txt /opt/flink/
RUN pip install --no-cache-dir -r /opt/flink/requirements.txt
