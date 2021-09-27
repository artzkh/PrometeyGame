from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import Message, Blueprint

from states import States

import keyboards

bp = Blueprint("died")


@bp.on.private_message(state=States.DIED)
async def died(message: Message):
    await message.answer("Здоровье твоего персонажа достигло 0",
                         keyboard=EMPTY_KEYBOARD)
    await message.answer(attachment="photo318378590_457297958",
                         keyboard=keyboards.died)
    await bp.state_dispenser.set(message.peer_id, States.DIED)

