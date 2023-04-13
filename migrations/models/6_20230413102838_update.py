from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "containerconfigure" RENAME COLUMN "c_name" TO "c_left";
        ALTER TABLE "containerconfigure" RENAME COLUMN "c_value" TO "c_right";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "containerconfigure" RENAME COLUMN "c_right" TO "c_value";
        ALTER TABLE "containerconfigure" RENAME COLUMN "c_left" TO "c_name";"""
