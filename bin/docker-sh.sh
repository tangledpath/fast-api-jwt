#!/bin/bash
docker run --add-host=host.docker.internal:host-gateway --platform linux/amd64 -it --entrypoint sh terracoil.fast_api_service

