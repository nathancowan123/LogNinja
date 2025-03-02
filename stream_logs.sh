#!/bin/bash

# Check if a container name or ID was provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <container_name_or_id>"
    exit 1
fi

CONTAINER_NAME=$1

# Stream logs from the given container
echo "Streaming logs for container: $CONTAINER_NAME..."
docker logs -f $CONTAINER_NAME
