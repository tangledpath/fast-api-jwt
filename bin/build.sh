#!/bin/bash
echo "Cleaning docker images"
docker compose down
docker image rm -f terracoil.fast_api_service
docker image rm -f terracoil.lambda_handler

echo "Exporting requirements.txt"
poetry export --without-hashes --format=requirements.txt > requirements.txt
docker compose build