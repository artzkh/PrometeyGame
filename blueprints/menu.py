from vkbottle.bot import Message, Blueprint

from config import db
from functions import generate_attachment, get_passport_info
from functions.cases import is_bonus
from functions.generate_attachment import hall_generator
from json_data import pictures
from states import States

import keyboards

bp = Blueprint("main_menu")


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
    passport_info, attachment = await get_passport_info(message.peer_id)
    await message.answer(message=passport_info, attachment=attachment)


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "room_hall"})
async def rooms_hall(message: Message):
    attachment, msg, keyboard = await hall_generator(peer_id=message.peer_id,
                                                     rec=message.state_peer.payload["recommendation"])
    await message.answer(message=msg, keyboard=keyboard, attachment=attachment)
