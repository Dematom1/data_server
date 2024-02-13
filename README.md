[![Build](https://github.com/Dematom1/data_server/actions/workflows/build.yaml/badge.svg?branch=Master)](https://github.com/Dematom1/data_server/actions/workflows/build.yaml)
#  Data Pipeline Server

This project is an example of a end to end data pipeline. 

It has the following:
- Pyflink
- Kafka
    - w/ Zookeeper
- Postgres
- Airflow
- DBT
- Metabase

Normally these services would be spread out across a few VM's, but this is just for demonstraction purposes.

## For development
Pull git repo

```bash
docker compose up --build -d
```

Postgres DB will be initialized
You will see a users, events, and attributed_sucessful_applications table.

A seperate process will generate users, click events, and job applicaiton events, the proceed to populate the tables.

It will generate 500 users, and 2000 click events. 

The central point of this setup is to simulate click events and successfully attributing successful job applications to users from these events processed in "real-time" through flink.

Open up the JobManager UI in your browser
localhost:8081

You will need to create the topics:
```bash
docker exec -it kafka /bin/bash

kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 1 --topic clicks

kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 1 --topic applications

exit

```

Run the Job:

```bash
docker exec jobmanager ./bin/flink run --python code/attribute_successful_applications.py
```


Or simply run run.sh
```bash
./run.sh
```


