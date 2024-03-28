#!/bin/bash
docker run --add-host=host.docker.internal:host-gateway --platform linux/amd64 -it --entrypoint sh fast-api-jwt-fast_api_service
# docker run --platform linux/arm64 -it  earbug:artist_harvester sh
