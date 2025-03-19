from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import CHANNEL_LINK

user_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои чаты/каналы", callback_data="my_chats")],
        [InlineKeyboardButton(text="Мои розыгрыши", callback_data="my_giveaways")]
    ]
)

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="user_back")]
    ]
)

user_skip_photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пропустить", callback_data="skip")],
        [InlineKeyboardButton(text="Отмена", callback_data="user_back")]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Текст 1", callback_data="text_1")],
    ]
)

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]
    ]
)

