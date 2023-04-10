from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "service" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "alias" VARCHAR(30) NOT NULL,
    "description" TEXT,
    "repository" VARCHAR(255) NOT NULL,
    "container_id" VARCHAR(20)  UNIQUE
);
COMMENT ON COLUMN "service"."name" IS '服务名';
COMMENT ON COLUMN "service"."alias" IS '别名';
COMMENT ON COLUMN "service"."description" IS '描述';
COMMENT ON COLUMN "service"."repository" IS '代码仓库';
COMMENT ON COLUMN "service"."container_id" IS '运行中的容器ID';
CREATE TABLE IF NOT EXISTS "history" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "version" VARCHAR(20) NOT NULL,
    "image_id" VARCHAR(64),
    "running" BOOL NOT NULL  DEFAULT False,
    "service_id" INT NOT NULL REFERENCES "service" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "history"."version" IS '版本号';
COMMENT ON COLUMN "history"."running" IS '运行?';
COMMENT ON COLUMN "history"."service_id" IS '关联服务';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
