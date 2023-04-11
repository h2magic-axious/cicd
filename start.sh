#!/usr/bin/env bash

git config --global credential.helper store
git config --global credential.helper 'store --file /app/credentials'

aerich upgrade

uvicorn main:app --host 0.0.0.0 --port 80