from app.database.models import async_session
from app.database.models import Giveaway
from sqlalchemy import select


async def get_giveaways_by_tg_id(tg_id):
    async with async_session() as session:
        giveaways = await session.scalars(select(Giveaway).where(Giveaway.tg_id == tg_id))
        return giveaways


async def get_giveaways_by_full_params(title, description, photo, count,
                                       tg_id, chat_id, sponsors):
    async with async_session() as session:
        giveaway = await session.scalar(select(Giveaway).where(Giveaway.title == title).where(Giveaway.description == description)
                                  .where(Giveaway.photo == photo).where(Giveaway.count == count).where(Giveaway.tg_id == tg_id)
                                  .where(Giveaway.chat_id == chat_id).where(Giveaway.sponsors == sponsors))
        return giveaway


async def get_giveaway_by_id(id):
    async with async_session() as session:
        giveaway = await session.scalar(select(Giveaway).where(Giveaway.id == id))
        return giveaway


