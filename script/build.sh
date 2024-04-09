#!/bin/bash

#poetry run pdoc fast_api_jwt --logo https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/fast_api_jwt.png --favicon https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/fast_api_jwt_sm.png
poetry run pdoc fast_api_jwt -o ./docs --logo https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/fast_api_jwt.png --favicon https://raw.githubusercontent.com/tangledpath/fast-api-jwt/master/fast_api_jwt_sm.png

# TODO: For when we have docker integration
#echo "Cleaning docker images"
#docker image rm -f terracoil.fast_api_service
#docker image rm -f terracoil.lambda_handler
#
echo "Exporting requirements.txt"
poetry export --without-hashes --format=requirements.txt > requirements.txt