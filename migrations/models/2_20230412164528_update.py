from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "service" ALTER COLUMN "container_id" TYPE VARCHAR(64) USING "container_id"::VARCHAR(64);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "service" ALTER COLUMN "container_id" TYPE VARCHAR(20) USING "container_id"::VARCHAR(20);"""
