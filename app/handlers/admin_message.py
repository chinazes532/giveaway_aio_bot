from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect

from app.database.requests.user.select import get_statistics


admin = Router()


@admin.message(AdminProtect(), Command("admin"))
@admin.message(AdminProtect(), F.text == "Админ-панель")
async def admin_panel(message: Message):
    daily_users, monthly_users, total_users = await get_statistics()

    response = (
        f"<b>Добро пожаловать в админ-панель! 🎉</b>\n\n"
        f"📊 <b>Статистика пользователей:</b>\n"
        f"🌟 <b>За сегодня:</b> {daily_users} пользователей\n"
        f"📅 <b>За месяц:</b> {monthly_users} пользователей\n"
        f"🌍 <b>Всего:</b> {total_users} пользователей\n\n"
        f"✨<i>Спасибо за вашу работу!</i>"
    )

    await message.answer(text=response,
                         reply_markup=ikb.admin_panel)
