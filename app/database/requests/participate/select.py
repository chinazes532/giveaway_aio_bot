import random

from app.database.models import async_session
from app.database.models import Participate
from sqlalchemy import select, func


async def get_participates_by_giveaway_id(giveaway_id):
    async with async_session() as session:
        participates = await session.scalars(select(Participate).where(Participate.giveaway_id == giveaway_id))
        return participates


async def count_participates_by_giveaway_id(giveaway_id):
    async with async_session() as session:
        count_query = select(func.count()).select_from(Participate).where(Participate.giveaway_id == giveaway_id)
        count = await session.scalar(count_query)
        return count


async def get_participate_by_tg_id_and_giveaway_id(tg_id, giveaway_id):
    async with async_session() as session:
        participate = await session.scalar(
            select(Participate).where(Participate.tg_id == tg_id)
            .where(Participate.giveaway_id == giveaway_id)
        )

        return participate


async def get_winners_by_giveaway_id(giveaway_id, count):
    async with async_session() as session:
        statement = (
            select(Participate)
            .filter(Participate.giveaway_id == giveaway_id)
            .order_by(func.random())
            .limit(count)
        )

        result = await session.execute(statement)
        winners = result.scalars().all()

        return winners

