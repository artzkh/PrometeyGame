from vkbottle.bot import Message, Blueprint

from functions import generate_attachment
from functions.cases import is_bonus
from functions.generate_attachment import hall_generator
from json_data import pictures
from states import States

import keyboards

bp = Blueprint("main_menu")


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "cases"})
async def menu_cases(message: Message):
    if await is_bonus(message.peer_id):
        await message.answer("Выбери подходящий кейс!", keyboard=keyboards.cases_positive)
    else:
        await message.answer("Выбери подходящий кейс!", keyboard=keyboards.cases_negative)


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "back"})
async def back_to_menu(message: Message):
    if await is_bonus(message.peer_id):
        await message.answer("Главное меню", keyboard=keyboards.menu_positive)
    else:
        await message.answer("Главное меню", keyboard=keyboards.menu_negative)


@bp.on.private_message(state=States.ACTIVE, payload={"main_menu": "room_hall"})
async def rooms_hall(message: Message):
    attachment, msg, keyboard = await hall_generator(peer_id=message.peer_id,
                                                     rec=message.state_peer.payload["recommendation"])
    await message.answer(message=msg, keyboard=keyboard, attachment=attachment)
