from app.database.models import async_session
from app.database.models import Giveaway


async def set_giveaway(title, description, photo,
                       count, tg_id, chat_id, sponsors):
    async with async_session() as session:
        giveaway = Giveaway(
            title=title,
            description=description,
            photo=photo,
            count=count,
            tg_id=tg_id,
            chat_id=chat_id,
            sponsors=sponsors
        )
        session.add(giveaway)
        await session.commit()
