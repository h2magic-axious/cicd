from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "containerconfigure" ADD "active" BOOL NOT NULL  DEFAULT True;
        ALTER TABLE "containerconfigure" ALTER COLUMN "configure_type" TYPE SMALLINT USING "configure_type"::SMALLINT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "containerconfigure" DROP COLUMN "active";
        ALTER TABLE "containerconfigure" ALTER COLUMN "configure_type" TYPE SMALLINT USING "configure_type"::SMALLINT;"""
