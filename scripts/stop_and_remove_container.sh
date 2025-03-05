#!/bin/bash

# Define the container name
CONTAINER_NAME="log_ninja_core"

# Stop the container if it's running
echo "Stopping container $CONTAINER_NAME..."
docker stop $CONTAINER_NAME

# Remove the container
echo "Removing container $CONTAINER_NAME..."
docker rm $CONTAINER_NAME

# Verify the container is removed
echo "Checking if the container is removed..."
docker ps -a | grep $CONTAINER_NAME

if [ $? -eq 0 ]; then
    echo "Failed to remove the container $CONTAINER_NAME."
else
    echo "Container $CONTAINER_NAME removed successfully."
fi
