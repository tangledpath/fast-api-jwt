#!/bin/bash
echo "Exporting requirements.txt"
poetry export --without-hashes --format=requirements.txt > requirements.txt
