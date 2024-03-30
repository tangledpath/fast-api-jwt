#!/script/bash
docker run --add-host=host.docker.internal:host-gateway --platform linux/amd64 -it --entrypoint sh terracoil.lambda_handler

