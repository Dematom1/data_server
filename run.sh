docker compose down
docker compose up --build -d
docker exec jobmanager ./bin/flink run --python code/attribute_successful_applications.py
