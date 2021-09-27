from vkbottle.bot import Message, Blueprint

from states import States

bp = Blueprint("nepon")


@bp.on.private_message()
async def nepon(message: Message):
    await message.answer("Не совсем понимаю тебя")

