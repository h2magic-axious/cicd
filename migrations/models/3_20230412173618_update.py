from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "containerconfigure" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "configure_type" SMALLINT NOT NULL,
    "value" VARCHAR(255) NOT NULL,
    "service_id" INT NOT NULL REFERENCES "service" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "containerconfigure"."configure_type" IS 'PORT: 1\nENVIRONMENT: 2\nVOLUMNE: 3';
COMMENT ON COLUMN "containerconfigure"."service_id" IS '关联服务';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "containerconfigure";"""
