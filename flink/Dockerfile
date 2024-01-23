FROM flink:latest

RUN set -ex; \
  apt-get update; \
  apt-get -y install python3; \
  apt-get -y install python3-pip; \
  apt-get -y install python3-dev; \
  ln -s /usr/bin/python3 /usr/bin/python; \
  ln -s /usr/bin/pip3 /usr/bin/pip


RUN set -ex; \
  apt-get update; \
  python -m pip install --upgrade pip; \
  pip install apache-flink

RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_2.11/1.12.0/flink-sql-connector-kafka_2.11-1.12.0.jar
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc_2.11/1.12.0/flink-connector-jdbc_2.11-1.12.0.jar
RUN wget -P /opt/flink/lib/ https://jdbc.postgresql.org/download/postgresql-42.2.19.jar

COPY requirements.txt /opt/flink/

RUN pip intsall --no-cache-dir -r /opt/flink/requirements.txt