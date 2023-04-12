#!/usr/bin/env bash

cd `pwd`

source venv/bin/activate

aerich upgrade

kill -9 `lsof -i:65530 -t`

uvicorn main:app --host 0.0.0.0 --port 65530 --reload

