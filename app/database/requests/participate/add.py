from app.database.models import async_session
from app.database.models import Participate


async def set_participate(tg_id,  giveaway_id):
    async with async_session() as session:
        participate = Participate(tg_id=tg_id,
                                  giveaway_id=giveaway_id)
        session.add(participate)
        await session.commit()