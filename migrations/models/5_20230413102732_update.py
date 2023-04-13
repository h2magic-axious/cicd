from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "containerconfigure" ADD "c_name" VARCHAR(64);
        ALTER TABLE "containerconfigure" RENAME COLUMN "value" TO "c_value";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "containerconfigure" RENAME COLUMN "c_value" TO "value";
        ALTER TABLE "containerconfigure" DROP COLUMN "c_name";"""
