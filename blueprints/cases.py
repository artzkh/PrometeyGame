from vkbottle.bot import Message, Blueprint

from functions import is_bonus, time_to_bonus
from states import States

bp = Blueprint("cases")


@bp.on.private_message(state=States.ACTIVE, payload={"case": "bonus"})
async def bonus_case(message: Message):
    if await is_bonus(message.peer_id):
        pass
    else:
        await message.answer(await time_to_bonus(message.peer_id))

