import random
import math
from random import choice

from vkbottle.bot import Message, Blueprint
from vkbottle.modules import json

from config import GROUP_ID, db
from functions import work_update_cleaner
from settings.cannot_change import cleaner_trash
from states import States

import keyboards

bp = Blueprint("works")


@bp.on.private_message(state=States.ACTIVE, payload_map={"work": str})
async def work(message: Message):
    payload = json.loads(message.payload)['work']
    if 'cleaner' in payload:
        if payload == 'cleaner':
            await message.answer('🧹 Работа дворником'
                                 '\n-----------------------------------------'
                                 '\n➕ Огонёчки: 1-15🔥'
                                 '\n➕ Опыт: 1✨'
                                 '\n➖ Энергия: 5-10⚡', keyboard=keyboards.cleaner_menu)
        elif payload == 'cleaner:start':
            energy = await db.get_user_energy(message.peer_id)
            if energy <= 9:
                await message.answer('🚫 Тебе не хватает энергии!'
                                     '\n-----------------------------------------'
                                     f'\nУ тебя: {math.ceil(energy)}⚡'
                                     '\nНеобходимо: 10⚡')
            else:
                await message.answer('🧹 Принимайся за работу!'
                                     '\n---------------------------------------------------'
                                     '\nПодметай в нужных местах, '
                                     'нажимая на зелёные кнопки.',
                                     keyboard=choice(keyboards.cleaner_work),
                                     attachment='photo318378590_457302748')
        elif payload == 'cleaner:true':
            fire_balance, work_experience, energy, happiness = await db.get_fire_work_energy_happiness(message.peer_id)
            if energy <= 9:
                await message.answer('🚫 Тебе не хватает энергии!'
                                     '\n-----------------------------------------'
                                     f'\nУ тебя: {math.ceil(energy)}⚡'
                                     '\nНеобходимо: 10⚡')
            else:
                text = ''
                new_fire_balance = fire_balance
                for i in range(10):
                    trash = random.choice(cleaner_trash)
                    text += trash['emoji']
                    new_fire_balance += trash['fire']
                new_energy = energy - random.randint(5, 10)
                new_work_experience = work_experience + 1
                if await work_update_cleaner(message.peer_id, energy, new_energy, happiness,
                                             new_fire_balance, new_work_experience):
                    try:
                        await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                                     last_activity=message.state_peer.payload["last_activity"],
                                                     recommendation=
                                                     (message.state_peer.payload["recommendation"]).remove('energy'))
                    except Exception:
                        pass
                await message.answer('🧹 Продолжай в том же духе!'
                                     '\n---------------------------------------------------'
                                     f'\n{text}'
                                     '\n---------------------------------------------------'
                                     f'\n➕ Огонёчков: {new_fire_balance}🔥'
                                     f'\n➕ Опыт: {new_work_experience}✨'
                                     f'\n➖ Энергия: {math.ceil(new_energy)}⚡', keyboard=choice(keyboards.cleaner_work))
        elif payload == 'cleaner:false':
            fire_balance, work_experience, energy, happiness = await db.get_fire_work_energy_happiness(message.peer_id)
            if energy <= 9:
                await message.answer('🚫 Тебе не хватает энергии!'
                                     '\n-----------------------------------------'
                                     f'\nУ тебя: {math.ceil(energy)}⚡'
                                     '\nНеобходимо: 10⚡')
            else:
                new_energy = energy - random.randint(5, 10)
                new_work_experience = work_experience + 1
                if await work_update_cleaner(message.peer_id, energy, new_energy, happiness,
                                             fire_balance, new_work_experience):
                    try:
                        await bp.state_dispenser.set(message.peer_id, States.ACTIVE,
                                                     last_activity=message.state_peer.payload["last_activity"],
                                                     recommendation=
                                                     (message.state_peer.payload["recommendation"]).remove('energy'))
                    except Exception:
                        pass
                await message.answer('🧹 Ты че, воздух подметаешь?'
                                     '\n---------------------------------------------------'
                                     f'\n💨💨💨💨💨💨💨💨💨💨'
                                     '\n---------------------------------------------------'
                                     f'\n➕ Огонёчков: {fire_balance}🔥'
                                     f'\n➕ Опыт: {new_work_experience}✨'
                                     f'\n➖ Энергия: {math.ceil(new_energy)}⚡', keyboard=choice(keyboards.cleaner_work))
                await db.update_fire_work_energy(message.peer_id, fire_balance, new_work_experience, new_energy)
