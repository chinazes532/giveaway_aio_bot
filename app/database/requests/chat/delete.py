from app.database.models import async_session
from app.database.models import Chat
from sqlalchemy import delete


async def delete_chat(id):
    async with async_session() as session:
        stmt = delete(Chat).where(Chat.id == id)
        await session.execute(stmt)
        await session.commit()
