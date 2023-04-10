from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "configure" DROP COLUMN "data_type";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "configure" ADD "data_type" VARCHAR(6) NOT NULL;"""
