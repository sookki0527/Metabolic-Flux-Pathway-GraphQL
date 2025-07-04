from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy import delete, text, Float, select

load_dotenv()  
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with async_session() as session:
        await session.execute(text("DROP TABLE IF EXISTS metabolite_reaction CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS pathway_reaction CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS flux_reaction CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS pathways CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS reactions CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS metabolites CASCADE"))
        await session.execute(text("DROP TABLE IF EXISTS flux CASCADE"))
        await session.commit()


# Dependency
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db