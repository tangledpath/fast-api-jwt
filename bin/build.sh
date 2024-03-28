#!/bin/bash
echo "Cleaning docker images"
docker image rm -f fast-api-jwt-lambda_handler
docker image rm -f fast-api-jwt-fast_api_service

echo "Exporting requirements.txt"
poetry export --without-hashes --format=requirements.txt > requirements.txt
docker compose build