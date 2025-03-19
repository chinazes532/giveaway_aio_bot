from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.chat.select import get_chats_by_tg_id
from app.database.requests.giveaway.select import get_giveaways_by_tg_id
from app.database.requests.participate.select import get_participates_by_giveaway_id, count_participates_by_giveaway_id


async def user_chats(tg_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Добавить чат/канал", callback_data="add_chat"))

    chats = await get_chats_by_tg_id(tg_id)

    for chat in chats:
        kb.row(InlineKeyboardButton(text=f"{chat.chat_id}", callback_data=f"chat_{chat.id}"))

    kb.row(InlineKeyboardButton(text="Назад", callback_data="user_back"))

    return kb.as_markup()


async def chat_panel(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Удалить", callback_data=f"deletechat_{id}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="my_chats"))

    return kb.as_markup()


async def user_giveaways(tg_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Добавить розыгрыш", callback_data="add_giveaway"))

    giveaways = await get_giveaways_by_tg_id(tg_id)

    for giveaway in giveaways:
        kb.row(InlineKeyboardButton(text=f"{giveaway.title}", callback_data=f"giveaway_{giveaway.id}"))

    kb.row(InlineKeyboardButton(text="Назад", callback_data="user_back"))

    return kb.as_markup()


async def user_chats_for_giveaway(tg_id):
    kb = InlineKeyboardBuilder()

    chats = await get_chats_by_tg_id(tg_id)

    for chat in chats:
        kb.row(InlineKeyboardButton(text=f"{chat.chat_id}", callback_data=f"userchat_{chat.id}"))

    kb.row(InlineKeyboardButton(text="Назад", callback_data="user_back"))

    return kb.as_markup()


async def participate(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text=f"Принять участие", callback_data=f"participate_{id}"))

    return kb.as_markup()


async def giveaway_panel(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Подвести итоги", callback_data=f"over_{id}"))
    kb.row(InlineKeyboardButton(text="Удалить", callback_data=f"deletegiveaway_{id}"))
    kb.row(InlineKeyboardButton(text="Назад", callback_data="my_giveaways"))

    return kb.as_markup()