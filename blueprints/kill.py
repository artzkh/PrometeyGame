from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import Message, Blueprint

from config import ADMINS
from states import States

import keyboards

bp = Blueprint("kill")


@bp.on.private_message(state=States.ACTIVE, text="/kill")
async def back_to_menu(message: Message):
    if message.peer_id in ADMINS:
        await message.answer("Здоровье твоего персонажа достигло 0",
                             keyboard=EMPTY_KEYBOARD)
        await message.answer(attachment="photo318378590_457297958",
                             keyboard=keyboards.died)
        await bp.state_dispenser.set(message.peer_id, States.DIED)
