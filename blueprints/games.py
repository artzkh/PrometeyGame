from vkbottle.bot import Message, Blueprint

from config import db
from functions import numeric
from settings import phrases
from random import choice
import keyboards
from states import States

bp = Blueprint("games")


@bp.on.private_message(state=States.ACTIVE, payload={"games": "roulette"})
async def roulette_menu(message: Message):
    balance = await db.get_fire_balance(message.peer_id)
    if balance < 100:
        await message.answer(f'{choice(phrases.low_balance_games)}\n'
                             f'——————\n'
                             f'Баланс: {balance}/100&#128293;',
                             attachment='photo318378590_457301572')
    else:
        if message.state_peer.payload.get('roulette_bid'):
            bid = message.state_peer.payload['roulette_bid']
        else:
            if balance < 999999:
                factor = len(str(balance)) - 3
                bid = int(round(balance / 20, -factor))
            else:
                bid = 90000
            await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                         last_activity=message.state_peer.payload["last_activity"],
                                         recommendation=message.state_peer.payload["recommendation"],
                                         game='roulette_menu',
                                         roulette_bid=bid)
        await message.answer(f'{choice(phrases.roulette_entrance)}\n'
                             '——————\n'
                             f'Баланс: {numeric(balance)}&#128293;',
                             keyboard=keyboards.generate_roulette_menu(bid),
                             attachment='photo318378590_457301573')
#choice(['photo318378590_457301566', 'photo318378590_457301567'])


@bp.on.private_message(state=States.ACTIVE, payload={"roulette": "menu"})
async def roulette_menu(message: Message):
    balance = await db.get_fire_balance(message.peer_id)
    if message.state_peer.payload.get('roulette_bid'):
        bid = message.state_peer.payload['roulette_bid']
    else:
        if balance < 999999:
            factor = len(str(balance)) - 3
            bid = int(round(balance / 20, -factor))
        else:
            bid = 90000
        await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                     last_activity=message.state_peer.payload["last_activity"],
                                     recommendation=message.state_peer.payload["recommendation"],
                                     game='roulette_menu',
                                     roulette_bid=bid)
    await message.answer('На что будем ставить?\n'
                         '——————\n'
                         f'Баланс: {numeric(balance)}&#128293;',
                         keyboard=keyboards.generate_roulette_menu(bid),
                         attachment=choice(['photo318378590_457301566', 'photo318378590_457301567']))


@bp.on.private_message(state=States.ACTIVE, payload={"roulette": "rules"})
async def roulette_menu(message: Message):
    await message.answer('&#127744;Правила рулетки просты\n'
                         '1. Делаешь ставку на сердце с одним из трёх цветов.\n'
                         '2. Если на рулетке выпадает твой цвет — '
                         'выигрываешь и забираешь кучу огонёчков.\n\n'
                         'Принимаются ставки на:\n'
                         '&#10084; — Вероятность 49.5% (X2&#128293;)\n'
                         '&#128154; — Вероятность 1% (X35&#128293;)\n'
                         '&#128420; — Вероятность 49.5% (X2&#128293;)',
                         attachment='doc318378590_629591772')


@bp.on.private_message(state=States.ACTIVE, payload={"roulette": "bid"})
async def roulette_bid_menu(message: Message):
    balance = await db.get_fire_balance(message.peer_id)
    if message.state_peer.payload.get('roulette_bid'):
        await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                     last_activity=message.state_peer.payload["last_activity"],
                                     recommendation=message.state_peer.payload["recommendation"],
                                     game='roulette_menu',
                                     roulette_bid=message.state_peer.payload['roulette_bid'])
    if balance < 999999:
        factor = len(str(balance))-3
        bids = [int(round(balance/20, -factor)),
                int(round(balance/10, -factor)),
                int(round(balance/5, -factor)),
                int(round(balance/2, -factor)),
                int(balance)]
    else:
        bids = [90000, 250000, 500000]
        if balance > 9999999:
            bids.append(9999999)
        else:
            bids.append(999999)
        bids.append(balance)
    await message.answer('Выбери подходящую ставку либо отправь в чат свою\n'
                         '——————\n'
                         f'Баланс: {numeric(balance)}&#128293;',
                         keyboard=keyboards.generate_roulette_bid_menu(bids))


@bp.on.private_message(state=States.ACTIVE, payload={"games": "chat"})
async def chat_game_answer(message: Message):
    # for chat_id in chats:
    #     link = chats[chat_id]
    #     if (await bp.api.messages.get_conversations_by_id(peer_ids=chat_id)).items[0].chat_settings.members_count < 2000:
    #         break
    link = 'https://vk.me/join/AJQ1d_47YATsmipYyTfefbkG'
    await message.answer(choice(phrases.chat_games), keyboard=keyboards.link_to_chat.replace('___', link))
