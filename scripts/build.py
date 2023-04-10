import sys
import os

version = sys.argv[1]

REGISTRY = "192.168.31.144:5000"

tag = f"{REGISTRY}/vitae:{version}"

os.system(f"docker build . -t {tag}")
os.system(f"docker push {tag}")
