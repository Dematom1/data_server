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
docker compose up -d
```

Postgres DB needs to be intialized:

```bash
docker exec -it postgres -U postgres -d postgres -f /docker-entrypoint.initdb.d/init.sql
```

You will now see a users, events, and attributed_sucessful_applications table.

The central point of this setup is to simulate click events and successfully attributing successful job applications to users from these events process in "real-time" through flink.

To run the script:

```bash
docker exec jobmanager ./bin/flink run --python .code/attribute_successful_applications
```

It will generate 500 users, and simulate 2000 click events. 


