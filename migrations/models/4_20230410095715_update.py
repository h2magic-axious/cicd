from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "service" ADD "container_id" VARCHAR(20) UNIQUE;
        CREATE UNIQUE INDEX "uid_service_contain_9420df" ON "service" ("container_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_service_contain_9420df";
        ALTER TABLE "service" DROP COLUMN "container_id";"""
