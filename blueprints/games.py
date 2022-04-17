import asyncio

from vkbottle import VKAPIError
from vkbottle.bot import Message, Blueprint

from config import db, GROUP_ID
from functions import numeric, is_bonus
from settings import phrases
from random import choice, randint
import keyboards
from states import States

bp = Blueprint("games")


@bp.on.private_message(state=States.ROULETTE, payload={"roulette": "games"})
async def games_menu(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                 last_activity=message.state_peer.payload["last_activity"],
                                 recommendation=message.state_peer.payload["recommendation"])
    await message.answer('Сыграем во что-нибудь ещё?', keyboard=choice(keyboards.games_menu))


@bp.on.private_message(state=States.ROULETTE, payload={"roulette": "home"})
async def home_menu(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                 last_activity=message.state_peer.payload["last_activity"],
                                 recommendation=message.state_peer.payload["recommendation"])
    if await is_bonus(message.peer_id):
        await message.answer("Главное меню", keyboard=keyboards.menu_positive)
    else:
        await message.answer("Главное меню", keyboard=keyboards.menu_negative)


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
            await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                         last_activity=message.state_peer.payload["last_activity"],
                                         recommendation=message.state_peer.payload["recommendation"],
                                         location='menu',
                                         roulette_bid=bid)
        await message.answer(f'{choice(phrases.roulette_entrance)}\n'
                             '——————\n'
                             f'Баланс: {numeric(balance)}&#128293;',
                             keyboard=keyboards.generate_roulette_menu(bid),
                             attachment='photo318378590_457301573')


@bp.on.private_message(state=States.ROULETTE, payload={"roulette": "menu"})
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
        await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                     last_activity=message.state_peer.payload["last_activity"],
                                     recommendation=message.state_peer.payload["recommendation"],
                                     location='menu',
                                     roulette_bid=bid)
    await message.answer('На что будем ставить?\n'
                         '——————\n'
                         f'Баланс: {numeric(balance)}&#128293;\n',
                         keyboard=keyboards.generate_roulette_menu(bid),
                         attachment=choice(['photo318378590_457301566', 'photo318378590_457301567']))


@bp.on.private_message(state=States.ROULETTE, payload={"roulette": "rules"})
async def roulette_menu(message: Message):
    await message.answer('&#127744;Правила рулетки просты\n'
                         '1. Делаешь ставку на сердце с одним из трёх цветов.\n'
                         '2. Если на рулетке выпадает твой цвет — '
                         'выигрываешь и забираешь кучу огонёчков.\n\n'
                         'Принимаются ставки на:\n'
                         '&#10084; — Вероятность 47.5% (X2&#128293;)\n'
                         '&#128154; — Вероятность 5% (X20&#128293;)\n'
                         '&#128420; — Вероятность 47.5% (X2&#128293;)',
                         attachment='doc318378590_629591772')


@bp.on.private_message(state=States.ROULETTE, payload={"roulette": "bid"})
async def roulette_bid_menu(message: Message):
    balance = await db.get_fire_balance(message.peer_id)
    if balance < 100:
        await message.answer(f'{choice(phrases.games_kick)}\n'
                             '——————\n'
                             f'Баланс: {balance}/100&#128293;',
                             keyboard=choice(keyboards.games_menu),
                             attachment='photo318378590_457301572')
        await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                     last_activity=message.state_peer.payload["last_activity"],
                                     recommendation=message.state_peer.payload["recommendation"])
        return
    elif balance < 999999:
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
    if message.state_peer.payload.get('roulette_bid'):
        bid = message.state_peer.payload['roulette_bid']
        await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                     last_activity=message.state_peer.payload["last_activity"],
                                     recommendation=message.state_peer.payload["recommendation"],
                                     location='bid_menu',
                                     roulette_bid=bid)
    else:
        bid = bids[0]
    await message.answer('Выбери подходящую ставку либо отправь в чат свою\n'
                         '——————\n'
                         f'Баланс: {numeric(balance)}&#128293;',
                         keyboard=keyboards.generate_roulette_bid_menu(bids, bid))


@bp.on.private_message(state=States.ROULETTE, payload_map={"roulette_red": int})
async def home_menu(message: Message):
    bid = message.get_payload_json()['roulette_red']
    balance = await db.get_fire_balance(message.peer_id)
    if balance >= bid:
        message.state_peer.state = States.SPAM
        message_id = await message.answer('Рулетка крутится...', attachment='doc318378590_629631975')
        await asyncio.sleep(3)
        rand_num = randint(0, 100)
        if rand_num < 60:
            balance += bid
            try:
                await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                           message_id=message_id,
                                           message='Ты выиграл — на рулетке &#10084;\n'
                                                   '——————\n'
                                                   f'Баланс: {numeric(balance)}&#128293; (+{numeric(bid)}&#128293;)',
                                           attachment='photo318378590_457301622')
            except VKAPIError(909):
                await message.answer('Ты выиграл — на рулетке &#10084;\n'
                                     '——————\n'
                                     f'Баланс: {numeric(balance)}&#128293; (+{numeric(bid)}&#128293;)',
                                     attachment='photo318378590_457301622')
            await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                         last_activity=message.state_peer.payload["last_activity"],
                                         recommendation=message.state_peer.payload["recommendation"],
                                         location='menu',
                                         roulette_bid=bid
                                         )
        else:
            balance -= bid
            if balance < 100:
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#128420;" if rand_num < 97 else "&#128154;"}\n'
                                                       '——————\n'
                                                       f'{choice(phrases.games_kick)}\n'
                                                       '——————\n'
                                                       f'Баланс: {balance}&#128293; (-{numeric(bid)}&#128293;)',
                                               keyboard=choice(keyboards.games_menu),
                                               attachment='photo318378590_457301572')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#128420;" if rand_num < 97 else "&#128154;"}\n'
                                         '——————\n'
                                         f'{choice(phrases.games_kick)}\n'
                                         '——————\n'
                                         f'Баланс: {balance}&#128293; (-{numeric(bid)}&#128293;)',
                                         keyboard=choice(keyboards.games_menu),
                                         attachment='photo318378590_457301572')
                await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"])
            elif balance < bid:
                if balance < 999999:
                    bid = int(balance)
                else:
                    if balance > 9999999:
                        bid = 9999999
                    else:
                        bid = 999999
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#128420;" if rand_num < 97 else "&#128154;"}\n'
                                                       '——————\n'
                                                       f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                               keyboard=keyboards.generate_roulette_menu(bid),
                                               attachment='photo318378590_457301621')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#128420;" if rand_num < 97 else "&#128154;"}\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                         keyboard=keyboards.generate_roulette_menu(bid),
                                         attachment='photo318378590_457301621')
                await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"],
                                             location='menu',
                                             roulette_bid=bid
                                             )
            else:
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#128420;" if rand_num < 97 else "&#128154;"}\n'
                                                       '——————\n'
                                                       f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                               attachment='photo318378590_457301621')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#128420;" if rand_num < 97 else "&#128154;"}\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                         attachment='photo318378590_457301621')
                await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"],
                                             location='menu',
                                             roulette_bid=bid
                                             )
        await db.update_user_fire_balance(message.peer_id, new_balance=balance)
    else:
        await message.answer(f'{choice(phrases.roulette_low_balance)}\n'
                             f'——————\n'
                             f'Баланс: {numeric(balance)}&#128293;')


@bp.on.private_message(state=States.ROULETTE, payload_map={"roulette_black": int})
async def home_menu(message: Message):
    bid = message.get_payload_json()['roulette_black']
    balance = await db.get_fire_balance(message.peer_id)
    if balance >= bid:
        message.state_peer.state = States.SPAM
        message_id = await message.answer('Рулетка крутится...', attachment='doc318378590_629631975')
        await asyncio.sleep(3)
        rand_num = randint(0, 100)
        if rand_num < 60:
            balance += bid
            try:
                await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                           message_id=message_id,
                                           message='Ты выиграл — на рулетке &#128420;\n'
                                                   '——————\n'
                                                   f'Баланс: {numeric(balance)}&#128293; (+{numeric(bid)}&#128293;)',
                                           attachment='photo318378590_457301622')
            except VKAPIError(909):
                await message.answer('Ты выиграл — на рулетке &#128420;\n'
                                     '——————\n'
                                     f'Баланс: {numeric(balance)}&#128293; (+{numeric(bid)}&#128293;)',
                                     attachment='photo318378590_457301622')
            await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                         last_activity=message.state_peer.payload["last_activity"],
                                         recommendation=message.state_peer.payload["recommendation"],
                                         location='menu',
                                         roulette_bid=bid
                                         )
        else:
            balance -= bid
            if balance < 100:
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#10084;" if rand_num < 97 else "&#128154;"}\n'
                                                       '——————\n'
                                                       f'{choice(phrases.games_kick)}\n'
                                                       '——————\n'
                                                       f'Баланс: {balance}&#128293; (-{numeric(bid)}&#128293;)',
                                               keyboard=choice(keyboards.games_menu),
                                               attachment='photo318378590_457301572')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#10084;" if rand_num < 97 else "&#128154;"}\n'
                                         '——————\n'
                                         f'{choice(phrases.games_kick)}\n'
                                         '——————\n'
                                         f'Баланс: {balance}&#128293; (-{numeric(bid)}&#128293;)',
                                         keyboard=choice(keyboards.games_menu),
                                         attachment='photo318378590_457301572')
                await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"])
            elif balance < bid:
                if balance < 999999:
                    bid = int(balance)
                else:
                    if balance > 9999999:
                        bid = 9999999
                    else:
                        bid = 999999
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#10084;" if rand_num < 97 else "&#128154;"}\n'
                                                       '——————\n'
                                                       f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                               keyboard=keyboards.generate_roulette_menu(bid),
                                               attachment='photo318378590_457301621')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#10084;" if rand_num < 97 else "&#128154;"}\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                         keyboard=keyboards.generate_roulette_menu(bid),
                                         attachment='photo318378590_457301621')
                await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"],
                                             location='menu',
                                             roulette_bid=bid
                                             )
            else:
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#10084;" if rand_num < 97 else "&#128154;"}\n'
                                                       '——————\n'
                                                       f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                               attachment='photo318378590_457301621')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#10084;" if rand_num < 97 else "&#128154;"}\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                         attachment='photo318378590_457301621')
                await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"],
                                             location='menu',
                                             roulette_bid=bid
                                             )
        await db.update_user_fire_balance(message.peer_id, new_balance=balance)
    else:
        await message.answer(f'{choice(phrases.roulette_low_balance)}\n'
                             f'——————\n'
                             f'Баланс: {numeric(balance)}&#128293;')


@bp.on.private_message(state=States.ROULETTE, payload_map={"roulette_green": int})
async def home_menu(message: Message):
    bid = message.get_payload_json()['roulette_green']
    balance = await db.get_fire_balance(message.peer_id)
    if balance >= bid:
        message.state_peer.state = States.SPAM
        message_id = await message.answer('Рулетка крутится...', attachment='doc318378590_629631975')
        await asyncio.sleep(3)
        rand_num = randint(0, 100)
        if rand_num < 5:
            balance += bid * 20
            try:
                await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                           message_id=message_id,
                                           message='Ты выиграл — на рулетке &#128154;\n'
                                                   '——————\n'
                                                   f'Баланс: {numeric(balance)}&#128293; (+{numeric(bid)}&#128293;)',
                                           attachment='photo318378590_457301622')
            except VKAPIError(909):
                await message.answer('Ты выиграл — на рулетке &#128154;\n'
                                     '——————\n'
                                     f'Баланс: {numeric(balance)}&#128293; (+{numeric(bid)}&#128293;)',
                                     attachment='photo318378590_457301622')
            await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                         last_activity=message.state_peer.payload["last_activity"],
                                         recommendation=message.state_peer.payload["recommendation"],
                                         location='menu',
                                         roulette_bid=bid
                                         )
        else:
            balance -= bid
            if balance < 100:
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#10084;" if rand_num < 51 else "&#128420;"}\n'
                                                       '——————\n'
                                                       f'{choice(phrases.games_kick)}\n'
                                                       '——————\n'
                                                       f'Баланс: {balance}&#128293; (-{numeric(bid)}&#128293;)',
                                               keyboard=choice(keyboards.games_menu),
                                               attachment='photo318378590_457301572')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#10084;" if rand_num < 51 else "&#128420;"}\n'
                                         '——————\n'
                                         f'{choice(phrases.games_kick)}\n'
                                         '——————\n'
                                         f'Баланс: {balance}&#128293; (-{numeric(bid)}&#128293;)',
                                         keyboard=choice(keyboards.games_menu),
                                         attachment='photo318378590_457301572')
                await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"])
            elif balance < bid:
                if balance < 999999:
                    bid = int(balance)
                else:
                    if balance > 9999999:
                        bid = 9999999
                    else:
                        bid = 999999
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#10084;" if rand_num < 51 else "&#128420;"}\n'
                                                       '——————\n'
                                                       f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                               keyboard=keyboards.generate_roulette_menu(bid),
                                               attachment='photo318378590_457301621')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#10084;" if rand_num < 51 else "&#128420;"}\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                         keyboard=keyboards.generate_roulette_menu(bid),
                                         attachment='photo318378590_457301621')
                await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"],
                                             location='menu',
                                             roulette_bid=bid
                                             )
            else:
                try:
                    await bp.api.messages.edit(peer_id=message.peer_id, group_id=GROUP_ID,
                                               message_id=message_id,
                                               message=f'Ты проиграл — на рулетке '
                                                       f'{"&#10084;" if rand_num < 51 else "&#128420;"}\n'
                                                       '——————\n'
                                                       f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                               attachment='photo318378590_457301621')
                except VKAPIError(909):
                    await message.answer(f'Ты проиграл — на рулетке '
                                         f'{"&#10084;" if rand_num < 51 else "&#128420;"}\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293; (-{numeric(bid)}&#128293;)',
                                         attachment='photo318378590_457301621')
                await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                             last_activity=message.state_peer.payload["last_activity"],
                                             recommendation=message.state_peer.payload["recommendation"],
                                             location='menu',
                                             roulette_bid=bid
                                             )
        await db.update_user_fire_balance(message.peer_id, new_balance=balance)
    else:
        await message.answer(f'{choice(phrases.roulette_low_balance)}\n'
                             f'——————\n'
                             f'Баланс: {numeric(balance)}&#128293;')


@bp.on.private_message(state=States.ROULETTE, payload_map={'roulette_bid': int})
async def change_bid(message: Message):
    balance = await db.get_fire_balance(message.peer_id)
    bid = message.get_payload_json()['roulette_bid']
    if balance >= bid:
        if bid < 1500000000:
            await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                         last_activity=message.state_peer.payload["last_activity"],
                                         recommendation=message.state_peer.payload["recommendation"],
                                         location='menu',
                                         roulette_bid=bid)
            await message.answer('Ставка изменена!\n'
                                 '——————\n'
                                 f'Баланс: {numeric(balance)}&#128293;',
                                 keyboard=keyboards.generate_roulette_menu(bid),
                                 attachment=choice(['photo318378590_457301566', 'photo318378590_457301567']))
        else:
            await message.answer(f'{choice(phrases.roulette_big_bid)}\n'
                                 f'Предложите ставку меньше 1.500.000.000&#128293;')
    else:
        await message.answer(f'{choice(phrases.roulette_low_balance)}\n'
                             f'——————\n'
                             f'Баланс: {numeric(balance)}&#128293;')


@bp.on.private_message(state=States.ROULETTE)
async def change_bid(message: Message):
    if message.state_peer.payload.get('location') == 'bid_menu':
        if not message.text.isdigit():
            try:
                bid = int(message.text.replace('🔥', ''))
            except ValueError:
                await message.answer('Пришли мне ставку в виде числа')
                return
        else:
            bid = int(message.text)
        balance = await db.get_fire_balance(message.peer_id)
        if balance >= bid:
            if bid > 0:
                if bid < 1500000000:
                    await bp.state_dispenser.set(message.peer_id, States.ROULETTE,
                                                 last_activity=message.state_peer.payload["last_activity"],
                                                 recommendation=message.state_peer.payload["recommendation"],
                                                 location='menu',
                                                 roulette_bid=bid)
                    await message.answer('Ставка изменена!\n'
                                         '——————\n'
                                         f'Баланс: {numeric(balance)}&#128293;\n',
                                         keyboard=keyboards.generate_roulette_menu(bid),
                                         attachment=choice(['photo318378590_457301566', 'photo318378590_457301567']))
                else:
                    await message.answer(f'{choice(phrases.roulette_big_bid)}\n'
                                         f'Предложите ставку меньше 1.500.000.000&#128293;')
            else:
                await message.answer('Ставка должна быть больше 0&#128293;')
        else:
            await message.answer(f'{choice(phrases.roulette_low_balance)}\n'
                                 f'——————\n'
                                 f'Баланс: {numeric(balance)}&#128293;')


@bp.on.private_message(state=States.ACTIVE, payload={"games": "chat"})
async def chat_game_answer(message: Message):
    # for chat_id in chats:
    #     link = chats[chat_id]
    #     if (await bp.api.messages.get_conversations_by_id(peer_ids=chat_id)).items[0].chat_settings.members_count < 2000:
    #         break
    link = 'https://vk.me/join/AJQ1d_47YATsmipYyTfefbkG'
    await message.answer(choice(phrases.chat_games), keyboard=keyboards.link_to_chat.replace('___', link))
