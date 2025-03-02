#!/bin/bash

# Stop and remove running containers
echo "Stopping and removing existing containers..."
docker-compose down

# Optional: Remove volumes if you want to start with clean data
# Uncomment the following line if you want to remove volumes as well
# docker-compose down -v

# Rebuild and restart the containers
echo "Rebuilding and restarting containers..."
docker-compose up --build -d

# View the status of the containers after rebuilding
docker ps
