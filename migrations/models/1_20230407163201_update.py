from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "configure" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "data_type" VARCHAR(6) NOT NULL,
    "value" TEXT NOT NULL,
    "active" BOOL NOT NULL  DEFAULT True
);
COMMENT ON COLUMN "configure"."name" IS '配置名';
COMMENT ON COLUMN "configure"."data_type" IS '数据类型';
COMMENT ON COLUMN "configure"."active" IS '启用?';;
        CREATE TABLE IF NOT EXISTS "history" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "version" VARCHAR(20) NOT NULL,
    "published" BOOL NOT NULL  DEFAULT False,
    "service_id" INT NOT NULL REFERENCES "service" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "history"."version" IS '版本号';
COMMENT ON COLUMN "history"."published" IS '发布?';
COMMENT ON COLUMN "history"."service_id" IS '关联服务';;
        CREATE TABLE IF NOT EXISTS "service" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "alias" VARCHAR(30) NOT NULL,
    "description" TEXT NOT NULL,
    "repository" VARCHAR(255) NOT NULL,
    "container_name" VARCHAR(20) NOT NULL UNIQUE
);
COMMENT ON COLUMN "service"."name" IS '服务名';
COMMENT ON COLUMN "service"."alias" IS '别名';
COMMENT ON COLUMN "service"."description" IS '描述';
COMMENT ON COLUMN "service"."repository" IS '代码仓库';
COMMENT ON COLUMN "service"."container_name" IS '容器名';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "configure";
        DROP TABLE IF EXISTS "history";
        DROP TABLE IF EXISTS "service";"""
