import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.filters.check_sub import CheckSubscription, CheckSubscriptionCallback
from config import BOT_TOKEN

from app.handlers.user_message import user
from app.handlers.admin_message import admin
from app.handlers.chat_message import chat
from app.handlers.giveaway_message import giveaway
from app.handlers.back_message import back

from app.database.models import create_db


async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # dp.message.middleware(CheckSubscription())
    # dp.callback_query.middleware(CheckSubscriptionCallback())

    dp.include_router(user)
    dp.include_router(chat)
    dp.include_router(giveaway)
    dp.include_router(back)
    dp.include_router(admin)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
