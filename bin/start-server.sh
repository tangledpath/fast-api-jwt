#!/bin/bash
uvicorn fast_api_jwt.service.main:app --port 9000 --reload