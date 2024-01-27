#!/bin/bash
set -e
echo "Deploying application...."

git pull 
docker-compose down 
echo "docker down"
docker-compose build --no-cache
docker-compose up -d
echo "docker up"

echo "🚀 Deployment Successful"
