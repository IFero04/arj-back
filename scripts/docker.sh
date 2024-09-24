#!/bin/bash
if [[ $2 == "down" ]]; then
    echo "Running docker-compose down"
    docker-compose down
elif [[ $2 == "up" ]] && [[ $1 == "prod" || $1 == "sit" || $1 == "dev" ]]; then
    fileEnv="./docker/compose/docker-compose.${1}.yaml"
    echo "Running docker-compose -f docker-compose.yaml -f $fileEnv up -d --build"
    docker-compose -f docker-compose.yaml -f $fileEnv up -d --build
else
    echo "Need to follow format ./docker.sh prod|dev down|up"
fi