import os

import dotenv

print("加载环境变量...")
dotenv.load_dotenv()


class Env:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", 5432)

    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASS = os.getenv("ADMIN_PASS", "admin")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

    DOCKER_SOCK = os.getenv("DOCKER_SOCK", None)
    REGISTRY = os.getenv("REGISTRY", None)
    NETWORK = os.getenv("NETWORK")

    GIT_USER = os.getenv("GIT_USERNAME")
    GIT_PASS = os.getenv("GIT_PASSWORD")
