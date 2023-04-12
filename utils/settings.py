from pathlib import Path

from utils.environments import Env

BASE_DIR = Path(__file__).parent.parent.absolute()

CORS_ALLOW_ORIGINS = [
    "*"
]

DB_CONF = {
    "host": Env.DB_HOST,
    "port": Env.DB_PORT,
    "user": "postgres",
    "password": "postgres",
    "database": "cicd",
}

DATABASE = {"default": {"engine": "tortoise.backends.asyncpg", "credentials": DB_CONF}}

DATABASE_MODELS = [
    "service.models"
]

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{DB_CONF['user']}:"
                   f"{DB_CONF['password']}@{DB_CONF['host']}:"
                   f"{DB_CONF['port']}/{DB_CONF['database']}"
    },
    "apps": {
        "models": {
            "models": ["aerich.models"] + DATABASE_MODELS,
            "default_connection": "default",
        }
    },
}
