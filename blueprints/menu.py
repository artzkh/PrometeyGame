from random import choice

from vkbottle.bot import Message, Blueprint

from config import db
from functions import get_passport_info
from functions.cases import is_bonus
from functions.generate_attachment import hall_generator
from settings.cannot_change import clothes_info
from states import States

import keyboards

bp = Blueprint("main_menu")


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "games"})
async def games_menu(message: Message):
    await message.answer('Выбери игру по душе!', keyboard=choice(keyboards.games_menu))


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "cases"})
async def menu_cases(message: Message):
    fire, chung, bonus_time = await db.get_cases_menu(peer_id=message.peer_id)
    if await is_bonus(message.peer_id, bonus_time):
        await message.answer(f"Баланс: {fire}&#128293;{chung}&#126980;"
                             f"\nСкорее забирай бонус! &#127873;", attachment="photo318378590_457298952",
                             keyboard=keyboards.cases_positive)
    else:
        await message.answer(f"Баланс: {fire}&#128293;{chung}&#126980;"
                             f"\nВыбери подходящий сундук!", attachment="photo318378590_457298952",
                             keyboard=keyboards.cases_negative)


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "back"})
async def back_to_menu(message: Message):
    if await is_bonus(message.peer_id):
        await message.answer("Главное меню", keyboard=keyboards.menu_positive)
    else:
        await message.answer("Главное меню", keyboard=keyboards.menu_negative)


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "passport"})
async def back_to_menu(message: Message):
    await message.answer(message=await get_passport_info(message.peer_id), attachment="photo318378590_457301656")


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "room_hall"})
async def rooms_hall(message: Message):
    attachment, msg, keyboard = await hall_generator(peer_id=message.peer_id,
                                                     rec=message.state_peer.payload["recommendation"])
    await message.answer(message=msg, keyboard=keyboard, attachment=attachment)


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "work"})
async def works_menu(message: Message):
    await message.answer(message='Выбери работу из списка, тебя уже ждут!', keyboard=keyboards.works_list)


@bp.on.private_message(state=States.ACTIVE, payload={"shop": "clothes"})
async def clothes_shop(message: Message):
    num = await db.get_current_clothes(message.peer_id)
    clothes = {}
    for i in clothes_info:
        if clothes_info[i]['id'] == num:
            clothes = clothes_info[i]
            num = i
            break
    await message.answer(f"✅ {clothes['name']} [{num}/7]"
                         f"\n***\n{clothes['description']}", keyboard=keyboards.shop_clothes_back(num), attachment=clothes['picture'])
