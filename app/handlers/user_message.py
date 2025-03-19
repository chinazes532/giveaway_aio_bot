import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.filters.admin_filter import AdminProtect

from app.database.requests.user.add import set_user
from app.database.requests.giveaway.select import get_giveaway_by_id
from app.database.requests.giveaway.add import set_giveaway
from app.database.requests.participate.select import get_participate_by_tg_id_and_giveaway_id
from app.database.requests.participate.add import set_participate
from app.filters.check_giveaway_subs import check_sponsors_sub

user = Router()


@user.message(CommandStart())
async def start_command(message: Message):
    admin = AdminProtect()
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    if not await admin(message):  
        await message.answer(f"{message.from_user.full_name}, добро пожаловать!\n"
                             f"В боте вы сможете создавать розыгрыши для Ваших подписчиков!",
                             reply_markup=ikb.user_panel)
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
    else:
        await message.answer(f"{message.from_user.full_name}, добро пожаловать!\n"
                             f"В боте вы сможете создавать розыгрыши для Ваших подписчиков!",
                             reply_markup=ikb.user_panel)
        await set_user(message.from_user.id, message.from_user.full_name, current_date)
        await message.answer(f"Вы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)



@user.callback_query(F.data.startswith("participate_"))
async def user_participate(callback: CallbackQuery, bot: Bot):
    giveaway_id = int(callback.data.split("_")[1])
    tg_id = callback.from_user.id
    giveaway = await get_giveaway_by_id(giveaway_id)

    if giveaway.sponsors:
        is_subscribed = await check_sponsors_sub(giveaway_id, tg_id, bot)
        if not is_subscribed:
            await callback.answer("Вы должны подписаться на всех спонсоров, чтобы участвовать в розыгрыше!",
                                  show_alert=True)
            return  # Прекращаем выполнение функции, если пользователь не подписан
    else:
        # Если нет спонсоров, можно сразу продолжать
        pass

    participate = await get_participate_by_tg_id_and_giveaway_id(tg_id, giveaway_id)

    if participate is None:
        await set_participate(tg_id, giveaway_id)
        await callback.answer("Вы приняли участие в розыгрыше!",
                              show_alert=True)
    elif participate:
        await callback.answer("Вы уже участвуете!",
                              show_alert=True)
    else:
        await callback.answer("Розыгрыш не найден!",
                              show_alert=True)




