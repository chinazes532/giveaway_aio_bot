from aiogram.fsm.state import State, StatesGroup


class AddChat(StatesGroup):
    chat_id = State()


class AddGiveaway(StatesGroup):
    chat_id = State()
    title = State()
    description = State()
    photo = State()
    count = State()
    sponsors = State()
