from typing import Annotated

from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=False)

async_session = async_sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    date: Mapped[str]


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[intpk]
    chat_id: Mapped[str] = mapped_column(BigInteger)
    tg_id: Mapped[str] = mapped_column(BigInteger)


class Giveaway(Base):
    __tablename__ = "giveaways"

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str]
    photo: Mapped[str] = mapped_column(nullable=True)
    count: Mapped[int]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    sponsors: Mapped[str] = mapped_column(nullable=True)


class Participate(Base):
    __tablename__ = "participates"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    giveaway_id: Mapped[int]


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
