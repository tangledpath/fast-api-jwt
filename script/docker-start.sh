#!/script/bash
clear
echo "Starting docker image..."
docker --log-level debug run --add-host=host.docker.internal:host-gateway --platform linux/arm64 --env-file .env.docker -p 9000:8080 earbug:artist_harvester

# Usage:
# clear && curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"artist_name":"Sonata Arctica"}'
