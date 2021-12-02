from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import Message, Blueprint

from config import ADMINS, db, GROUP_ID
from functions import is_bonus
from states import States

import keyboards

bp = Blueprint("commands")


@bp.on.private_message(state=States.ACTIVE, text="/home")
async def back_to_menu(message: Message):
    if await is_bonus(message.peer_id):
        await message.answer("Главное меню", keyboard=keyboards.menu_positive)
    else:
        await message.answer("Главное меню", keyboard=keyboards.menu_negative)


@bp.on.private_message(state=States.ACTIVE, text="/balance")
async def balance_info(message: Message):
    fire, chung = await db.get_user_full_balance(peer_id=message.peer_id)
    await message.answer(f"Твой баланс: {fire}&#128293;{chung}&#126980;")
