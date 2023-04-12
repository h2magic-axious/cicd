#!/usr/bin/env bash

cd `pwd`

source venv/bin/activate

aerich upgrade

uvicorn main:app --host 0.0.0.0 --port 80