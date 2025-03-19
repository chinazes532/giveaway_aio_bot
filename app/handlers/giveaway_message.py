from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.inline as ikb
import app.keyboards.builder as bkb
from app.database.requests.participate.select import count_participates_by_giveaway_id, get_winners_by_giveaway_id

from app.filters.send_giveaway import send_giveaway

from app.states import AddGiveaway

from app.database.requests.chat.select import get_chat_by_id
from app.database.requests.giveaway.add import set_giveaway
from app.database.requests.giveaway.select import get_giveaway_by_id
from app.database.requests.giveaway.delete import delete_giveaway


giveaway = Router()


@giveaway.callback_query(F.data == "my_giveaways")
async def my_giveaways(callback: CallbackQuery):
    tg_id = callback.from_user.id

    try:
        await callback.message.edit_text("<b>Все Ваши розыгрыши:</b>",
                                         reply_markup=await bkb.user_giveaways(tg_id))
    except Exception:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer("<b>Все Ваши розыгрыши:</b>",
                                         reply_markup=await bkb.user_giveaways(tg_id))


@giveaway.callback_query(F.data == "add_giveaway")
async def add_giveaway(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id

    await callback.message.edit_text("<b>Выберите чат/канал, для которого хотите сделать розыгрыш:</b>",
                                     reply_markup=await bkb.user_chats_for_giveaway(tg_id))

    await state.set_state(AddGiveaway.chat_id)


@giveaway.callback_query(AddGiveaway.chat_id, F.data.startswith("userchat_"))
async def user_select_chat(callback: CallbackQuery, state: FSMContext):
    chat_id = int(callback.data.split("_")[1])
    chat = await get_chat_by_id(chat_id)

    await state.update_data(chat_id=chat.chat_id)

    await callback.message.edit_text("<b>Введите заголовок для розыгрыша:</b>",
                                     reply_markup=ikb.user_cancel)

    await state.set_state(AddGiveaway.title)


@giveaway.message(AddGiveaway.title)
async def giveaway_title(message: Message, state: FSMContext):
    if message.text and len(message.text) < 128:
        await state.update_data(title=message.html_text)

        await message.answer("<b>Введите описание для розыгрыша:</b>",
                             reply_markup=ikb.user_cancel)

        await state.set_state(AddGiveaway.description)

    else:
        await message.answer("<b>Заголовок не должен превышать 128 символов!</b>",
                             reply_markup=ikb.user_cancel)


@giveaway.message(AddGiveaway.description)
async def giveaway_description(message: Message, state: FSMContext):
    if message.text and len(message.text) < 1500:
        await state.update_data(description=message.html_text)

        await message.answer("<b>Пришлите фотографию для розыгрыша, если ее нет, то нажмите на кнопку"
                             "\"Пропустить\"</b>",
                             reply_markup=ikb.user_skip_photo)

        await state.set_state(AddGiveaway.photo)

    else:
        await message.answer("<b>Описание не должно превышать 1500 символов!</b>",
                             reply_markup=ikb.user_cancel)


@giveaway.callback_query(AddGiveaway.photo, F.data == "skip")
async def skip_photo(callback: CallbackQuery, state: FSMContext):
    await state.update_data(photo=None)

    await callback.message.edit_text("<b>Введите максимальное количество победителей:</b>",
                                     reply_markup=ikb.user_cancel)

    await state.set_state(AddGiveaway.count)


@giveaway.message(AddGiveaway.photo)
async def giveaway_photo(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)

        await message.answer("<b>Введите максимальное количество победителей:</b>",
                                         reply_markup=ikb.user_cancel)

        await state.set_state(AddGiveaway.count)

    else:
        await message.answer("<b>Пришлите изображение или пропустите этот пункт!</b>",
                             reply_markup=ikb.user_skip_photo)


@giveaway.message(AddGiveaway.count)
async def giveaway_count(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) > 0:
        await state.update_data(count=int(message.text))

        await message.answer("<b>Введите юзернейм спонсоров (чаты/каналы для обязательной подписки):\n"
                             "Пример:\n"
                             "@channel1\n"
                             "@channel2\n\n"
                             "Если спонсоров нет, то пропустите этот пункт</b>",
                             reply_markup=ikb.user_skip_photo)

        await state.set_state(AddGiveaway.sponsors)

    else:
        await message.answer("<b>Минимальное число победителей не должно быть меньше 1!</b>",
                             reply_markup=ikb.user_cancel)


@giveaway.callback_query(AddGiveaway.sponsors, F.data == "skip")
async def skip_sponsors(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(sponsors=None)

    data = await state.get_data()

    tg_id = callback.from_user.id
    chat_id = data.get("chat_id")
    title = data.get("title")
    description = data.get("description")
    photo = data.get("photo")
    count = data.get("count")
    sponsors = data.get("sponsors")

    await set_giveaway(title, description, photo, count, tg_id, chat_id, sponsors)

    await send_giveaway(title, description, photo, count, tg_id, chat_id, sponsors, bot)

    await callback.message.edit_text("<b>Розыгрыш был успешно создан!</b>",
                                     reply_markup=await bkb.user_giveaways(tg_id))

    await state.clear()


@giveaway.message(AddGiveaway.sponsors)
async def giveaway_sponsors(message: Message, state: FSMContext, bot: Bot):
    if message.text:
        result = []
        sponsors = message.text.split("\n")
        for sponsor in sponsors:
            try:
                chat_member = await bot.get_chat_member(sponsor, bot.id)
                if chat_member.status in ['administrator', 'creator']:
                    await state.update_data(sponsors=sponsors)
                    result.append(sponsor)
            except Exception as e:
                print(e)

        if result != sponsors:
            await message.answer("<b>Не все спонсоры являются администраторами в чате/канале!</b>",
                                 reply_markup=ikb.user_skip_photo)
        else:
            tg_id = message.from_user.id

            data = await state.get_data()

            chat_id = data.get("chat_id")
            title = data.get("title")
            description = data.get("description")
            photo = data.get("photo")
            count = data.get("count")
            sponsors = data.get("sponsors")
            result = '\n'.join(sponsors)

            await set_giveaway(title, description, photo, count, tg_id, chat_id, result)

            await send_giveaway(title, description, photo, count, tg_id, chat_id, result, bot)

            await message.answer("<b>Розыгрыш был успешно создан!</b>",
                                     reply_markup=await bkb.user_giveaways(tg_id))

    else:
        await message.answer("Введите юзернеймы спонсоров",
                             reply_markup=ikb.user_cancel)


@giveaway.callback_query(F.data.startswith("giveaway_"))
async def giveaway_info(callback: CallbackQuery):
    giveaway_id = int(callback.data.split("_")[1])
    giveaway = await get_giveaway_by_id(giveaway_id)
    count = await count_participates_by_giveaway_id(giveaway_id)

    if giveaway.photo:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer_photo(photo=giveaway.photo,
                                            caption=f"<b>Панель управления розыгрышем №{giveaway.id}</b>\n\n"
                                                    f"<b>Заголовок:</b> {giveaway.title}\n"
                                                    f"<b>Описание:</b> {giveaway.description}\n"
                                                    f"<b>Число победителей:</b> {giveaway.count}\n"
                                                    f"<b>Число участников:</b> {count}\n"
                                                    f"<b>Спонсоры:</b> {giveaway.sponsors if giveaway.sponsors else 'Нет'}",
                                            reply_markup=await bkb.giveaway_panel(giveaway.id))
    else:
        await callback.message.edit_text(f"<b>Панель управления розыгрышем №{giveaway.id}</b>\n\n"
                                                    f"<b>Заголовок:</b> {giveaway.title}\n"
                                                    f"<b>Описание:</b> {giveaway.description}\n"
                                                    f"<b>Число победителей:</b> {giveaway.count}\n"
                                                    f"<b>Число участников:</b> {count}\n"
                                                    f"<b>Спонсоры:</b> {giveaway.sponsors if giveaway.sponsors else 'Нет'}",
                                         reply_markup=await bkb.giveaway_panel(giveaway.id))


@giveaway.callback_query(F.data.startswith("deletegiveaway_"))
async def delete_giveaway_cb(callback: CallbackQuery):
    giveaway_id = int(callback.data.split("_")[1])

    await delete_giveaway(giveaway_id)

    tg_id = callback.from_user.id

    try:
        await callback.message.edit_text("<b>Розыгрыш был успешно удален!</b>",
                                         reply_markup=await bkb.user_giveaways(tg_id))
    except Exception:
        await callback.answer()
        await callback.message.delete()

        await callback.message.answer("<b>Розыгрыш был успешно удален!</b>",
                                      reply_markup=await bkb.user_giveaways(tg_id))


@giveaway.callback_query(F.data.startswith("over_"))
async def over_giveaway(callback: CallbackQuery, bot: Bot):
    giveaway_id = int(callback.data.split("_")[1])
    giveaway = await get_giveaway_by_id(giveaway_id)
    winners = await get_winners_by_giveaway_id(giveaway_id, giveaway.count)

    result = []

    for winner in winners:
        result.append(str(winner.tg_id))

    res = '\n'.join(result)

    await callback.message.edit_text(f"<b>Победители:</b>\n\n"
                                     f"{res}",
                                     reply_markup=ikb.user_cancel)

    try:
        await bot.send_message(chat_id=giveaway.chat_id,
                               text=f"<b>Победители:</b>\n\n"
                                    f"{res}")
    except Exception:
        await callback.message.answer("<b>Не удалось отправить результаты в сообщество :(",
                                      reply_markup=ikb.user_cancel)





