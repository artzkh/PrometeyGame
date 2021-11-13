from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import Message, Blueprint

from config import ADMINS, db, GROUP_ID
from states import States

import keyboards

bp = Blueprint("admin_commands")


@bp.on.private_message(state=States.ACTIVE, text="/kill <user_id>")
async def back_to_menu(message: Message, user_id):
    if message.peer_id in ADMINS:
        user_id = await check_id(message, user_id)
        if user_id:
            await db.update_status(peer_id=user_id, status="died")
            await bp.state_dispenser.set(user_id, States.DIED)
            await message.answer(f"&#9989; Игрок {user_id} убит &#9989;")
            await bp.api.messages.send(peer_id=user_id, group_id=GROUP_ID,
                                       keyboard=EMPTY_KEYBOARD,
                                       random_id=0,
                                       attachment="photo318378590_457297958",
                                       message="&#128081; Твой персонаж был убит Администратором &#128081;")


@bp.on.private_message(state=States.ACTIVE, text="/give <user_id> <count>")
async def back_to_menu(message: Message, user_id, count):
    if message.peer_id in ADMINS:
        user_id = await check_id(message, user_id)
        if user_id:
            try:
                count = int(count)
            except ValueError:
                await message.answer("&#10060; Неверное количество огонечков &#10060;")
            if count > 10000000:
                await message.answer("Нельзя передать больше 10.000.000&#128293;")
            else:
                await db.add_fire_balance(peer_id=user_id, count=count)
                await message.answer(f"&#9989; Игроку {user_id} начислены огонёчки&#128293; &#9989;")
                await bp.api.messages.send(peer_id=user_id, group_id=GROUP_ID,
                                           random_id=0,
                                           attachment="photo318378590_457299005",
                                           message=f"&#128081; Администратор выдал тебе {count:,}&#128293; &#128081;")


async def check_id(message, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        await message.answer("&#10060; Неверный ID &#10060;")
        return False
    if await db.check_user_id(peer_id=user_id):
        return await db.get_user_peer_id(user_id)
    elif not (await db.check_user_peer_id(peer_id=user_id)):
        await message.answer("&#10060; Неверный ID &#10060;")
        return False
    else:
        return user_id
