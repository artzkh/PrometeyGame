from vkbottle.bot import Message, Blueprint

from states import States

bp = Blueprint("nepon")


@bp.on.private_message()
async def nepon(message: Message):
    pass

