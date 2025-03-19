from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb


back = Router()


@back.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(f"{callback.from_user.full_name}, добро пожаловать!\n"
                             f"В боте вы сможете создавать розыгрыши для Ваших подписчиков!",
                             reply_markup=ikb.user_panel)
    except Exception:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer(f"{callback.from_user.full_name}, добро пожаловать!\n"
                             f"В боте вы сможете создавать розыгрыши для Ваших подписчиков!",
                             reply_markup=ikb.user_panel)

    await state.clear()
