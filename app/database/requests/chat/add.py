from app.database.models import async_session
from app.database.models import Chat


async def set_chat(chat_id, tg_id):
    async with async_session() as session:
        chat = Chat(chat_id=chat_id,
                    tg_id=tg_id)
        session.add(chat)
        await session.commit()