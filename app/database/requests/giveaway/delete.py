from app.database.models import async_session
from app.database.models import Giveaway
from sqlalchemy import delete


async def delete_giveaway(id):
    async with async_session() as session:
        stmt = delete(Giveaway).where(Giveaway.id == id)
        await session.execute(stmt)
        await session.commit()