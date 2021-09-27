from time import time, gmtime, strftime

from config import db


async def is_bonus(peer_id):
    if time() - await db.get_user_bonus_time(peer_id) > 86400:
        return True
    else:
        return False


async def time_to_bonus(peer_id):
    return f"Приходи за бонусом через " \
           f"{strftime('%H:%M:%S', gmtime((await db.get_user_bonus_time(peer_id) + 86400) - int(time())))} &#9203;"
