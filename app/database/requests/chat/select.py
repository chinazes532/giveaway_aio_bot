from app.database.models import async_session
from app.database.models import Chat
from sqlalchemy import select


async def get_chats_by_tg_id(tg_id):
    async with async_session() as session:
        chats = await session.scalars(select(Chat).where(Chat.tg_id == tg_id))
        return chats


async def get_chat_by_id(id):
    async with async_session() as session:
        chat = await session.scalar(select(Chat).where(Chat.id == id))
        return chat
