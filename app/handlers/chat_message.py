from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.states import AddChat

from app.database.requests.chat.add import set_chat
from app.database.requests.chat.select import get_chat_by_id
from app.database.requests.chat.delete import delete_chat


chat = Router()


@chat.callback_query(F.data == "my_chats")
async def my_chats(callback: CallbackQuery):
    tg_id = callback.from_user.id
    await callback.message.edit_text("<b>Ваши чаты и каналы:</b>",
                                     reply_markup=await bkb.user_chats(tg_id))


@chat.callback_query(F.data == "add_chat")
async def add_chat(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Для добавления чата или канала, отправьте его юзернейм\n"
                                     "(Пример: @channel):\n"
                                     "Также добавьте бота в чат/канал как администратора!</b>",
                                     reply_markup=ikb.user_cancel)

    await state.set_state(AddChat.chat_id)


@chat.message(AddChat.chat_id)
async def check_chat_id(message: Message, state: FSMContext, bot: Bot):
    if message.text and message.text[0] == '@':
        tg_id = message.from_user.id
        chat_id = message.text
        try:
            chat_member = await bot.get_chat_member(chat_id, bot.id)
            if chat_member.status in ['administrator', 'creator']:
                await state.update_data(chat_id=chat_id)

                await set_chat(message.text, tg_id)

                await message.answer("<b>Чат был успешно добавлен!</b>",
                                     reply_markup=await bkb.user_chats(tg_id))

                await state.clear()
            else:
                await message.answer("<b>Бот должен быть администратором в этом чате!</b>",
                                     reply_markup=ikb.user_cancel)
        except Exception:
            await message.answer("<b>Не удалось получить информацию о чате. Убедитесь, что указанный чат существует и бот добавлен в него.</b>",
                                 reply_markup=ikb.user_cancel)

    else:
        await message.answer("<b>Неверный формат ввода, попробуйте еще раз!</b>",
                             reply_markup=ikb.user_cancel)


@chat.callback_query(F.data.startswith("chat_"))
async def chat_info(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[1])
    chat = await get_chat_by_id(chat_id)

    await callback.message.edit_text(f"<b>Панель управления чатом №{chat.id}</b>\n\n"
                                     f"<b>Юзернейм:</b> {chat.chat_id}\n\n"
                                     f"<b><i>Выберите действие:</i></b>",
                                     reply_markup=await bkb.chat_panel(chat_id),
                                     disable_web_page_preview=True)


@chat.callback_query(F.data.startswith("deletechat_"))
async def delete_chat_cb(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[1])
    tg_id = callback.from_user.id

    await delete_chat(chat_id)

    await callback.message.edit_text("<b>Чат был успешно удален!</b>",
                                     reply_markup=await bkb.user_chats(tg_id))

