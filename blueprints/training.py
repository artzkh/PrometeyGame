from time import time

from vkbottle.bot import Message, Blueprint

from config import db
from states import States

import keyboards

bp = Blueprint("training")


@bp.on.private_message(state=States.TRAINING)
async def training(message: Message):
    await message.answer("Привет, скоро здесь будет доступно обучение!",
                         attachment="photo318378590_457297324",
                         keyboard=keyboards.menu_positive)
    await bp.state_dispenser.set(message.peer_id, States.ACTIVE, last_activity=time(), recommendation={})
    await db.update_status(peer_id=message.peer_id, status="active")

