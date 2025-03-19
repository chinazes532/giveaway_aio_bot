from aiogram import Bot

from app.database.requests.giveaway.select import get_giveaways_by_full_params

import app.keyboards.builder as bkb


async def send_giveaway(title, description, photo, count, tg_id, chat_id, sponsors, bot: Bot):
    giveaway = await get_giveaways_by_full_params(title, description, photo,
                                                  count, tg_id, chat_id, sponsors)

    if giveaway:
        if giveaway.photo:
            try:
                await bot.send_photo(chat_id=giveaway.chat_id,
                                     photo=giveaway.photo,
                                     caption=f"{title}\n\n{description}",
                                     reply_markup=await bkb.participate(giveaway.id))
            except Exception as e:
                if str(e) in "Telegram server says - Bad Request: need administrator rights in the channel chat":
                    await bot.send_message(chat_id=tg_id,
                                           text="<b>Бот не смог разослать розыгрыш в канал, так как у него нет прав Администратора!")
                else:
                    print(e)
        else:
            try:
                await bot.send_message(chat_id=giveaway.chat_id,
                                       text=f"{title}\n\n{description}",
                                       reply_markup=await bkb.participate(giveaway.id),
                                       disable_web_page_preview=True)
            except Exception as e:
                if str(e) in "Telegram server says - Bad Request: need administrator rights in the channel chat":
                    await bot.send_message(chat_id=tg_id,
                                           text="<b>Бот не смог разослать розыгрыш в канал, так как у него нет прав Администратора!")
                else:
                    print(e)

    else:
        await bot.send_message(chat_id=tg_id,
                               text="<b>Конкурс не найден!</b>")