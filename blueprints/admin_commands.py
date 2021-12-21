from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import Message, Blueprint

from config import ADMINS, db, GROUP_ID
from functions import is_bonus
from states import States

import keyboards

bp = Blueprint("admin_commands")


@bp.on.private_message(state=States.ACTIVE, text="/kill <user_id>")
async def command_kill(message: Message, user_id):
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
                                       message="&#128081; Небесная кара &#128081;")


@bp.on.private_message(state=States.ACTIVE, text="/give <user_id> <count>")
async def command_give(message: Message, user_id, count):
    if message.peer_id in ADMINS:
        user_id = await check_id(message, user_id)
        if user_id:
            try:
                count = int(count)
            except ValueError:
                await message.answer("&#10060; Неверное количество &#10060;")
            if count > 10000000:
                await message.answer("&#10060; >10.000.000&#128293; &#10060;")
            else:
                await db.add_fire_balance(peer_id=user_id, count=count)
                await message.answer(f"&#9989; Игроку {user_id} начислены огонёчки&#128293; &#9989;")
                await bp.api.messages.send(peer_id=user_id, group_id=GROUP_ID,
                                           random_id=0,
                                           attachment="photo318378590_457299005",
                                           message=f"&#128081; Тебе начислено {count:,}&#128293; &#128081;")


@bp.on.private_message(state=States.ACTIVE, text="/ban <user_id>")
async def command_ban(message: Message, user_id):
    if message.peer_id in ADMINS:
        user_id = await check_id(message, user_id)
        if user_id:
            if user_id in ADMINS:
                await message.answer("&#10060; Нельзя заблокировать Администратора &#10060;")
            else:
                await db.update_status(peer_id=user_id, status="ban")
                await bp.state_dispenser.set(user_id, States.SPAM)
                await message.answer(f"&#9989; Игрок {user_id} забанен &#9989;")
                await bp.api.messages.send(peer_id=user_id, group_id=GROUP_ID,
                                           keyboard=EMPTY_KEYBOARD,
                                           random_id=0,
                                           attachment="photo318378590_457297958",
                                           message="&#128081; Ты был забанен &#128081;")


@bp.on.private_message(state=States.ACTIVE, text="/unban <user_id>")
async def command_unban(message: Message, user_id):
    if message.peer_id in ADMINS:
        user_id = await check_id(message, user_id)
        if user_id:
            await db.update_status(peer_id=user_id, status="active")
            await bp.state_dispenser.set(user_id, States.ACTIVE, last_activity=0, rec=[])
            await message.answer(f"&#9989; Игрок {user_id} Разблокирован &#9989;")
            if await is_bonus(message.peer_id):
                await bp.api.messages.send(peer_id=user_id, group_id=GROUP_ID,
                                           keyboard=keyboards.menu_positive,
                                           random_id=0,
                                           message="&#128081; Ты был разбанен &#128081;")
            else:
                await bp.api.messages.send(peer_id=user_id, group_id=GROUP_ID,
                                           keyboard=keyboards.menu_negative,
                                           random_id=0,
                                           message="&#128081; Ты был разбанен &#128081;")


async def check_id(message, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        await message.answer("&#10060; Неверный ID &#10060;")
        return False
    if not (await db.check_user_peer_id(peer_id=user_id)):
        await message.answer("&#10060; Неверный ID &#10060;")
        return False
    else:
        return user_id
