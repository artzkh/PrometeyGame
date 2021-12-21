from vkbottle import Bot

from blueprints import bps

from middlewares import EventSpamMiddleware, MessageSpamMiddleware
from states import state_dispenser
from config import api, db


def setup_blueprints(bot_: Bot):
    for bp in bps:
        bp.load(bot_)


def setup_middlewares(bot_: Bot):
    bot_.labeler.raw_event_view.register_middleware(EventSpamMiddleware())
    bot_.labeler.message_view.register_middleware(MessageSpamMiddleware())


def init_bot():
    bot_ = Bot(api=api)
    bot_.state_dispenser = state_dispenser
    setup_middlewares(bot_)
    setup_blueprints(bot_)
    return bot_


async def init_db():
    await db.create()
    await db.create_table_users()


bot = init_bot()
bot.loop_wrapper.on_startup.append(init_db())
