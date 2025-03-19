from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from app.database.requests.giveaway.select import get_giveaway_by_id


async def check_sponsors_sub(giveaway_id, tg_id, bot: Bot):
    giveaway = await get_giveaway_by_id(giveaway_id)
    sponsors = giveaway.sponsors.split("\n")

    print(sponsors)

    try:
        for sponsor in sponsors:
            chat_member = await bot.get_chat_member(sponsor, tg_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                return False
    except Exception as e:
        print(f"{e}")
        return False

    return True


