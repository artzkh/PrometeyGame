import random
from random import choice

from vkbottle.bot import Message, Blueprint
from vkbottle.modules import json

from config import GROUP_ID
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
                                 '\n➕ Огонёчки: 1-5🔥'
                                 '\n➕ Опыт: 1✨'
                                 '\n➖ Энергия: 5-10⚡', keyboard=keyboards.cleaner_menu)
        elif payload == 'cleaner:start':
            await message.answer('Принимайся за работу!'
                                 '\n-----------------------------------------'
                                 '\nПодметай в нужных местах, '
                                 'нажимая на зелёные кнопки.',
                                 keyboard=choice(keyboards.cleaner_work),
                                 attachment='photo318378590_457302748')
        elif payload == 'cleaner:true':
            text = ''
            fire = 0
            for i in range(10):
                trash = random.choice(cleaner_trash)
                text += trash['emoji']
                fire += trash['fire']
            await message.answer('🧹 Продолжай в том же духе!'
                                 '\n---------------------------------------------------'
                                 f'\n{text}'
                                 '\n---------------------------------------------------'
                                 f'\n➕ Огонёчков: {fire}🔥'
                                 f'\n➕ Опыт: 1✨'
                                 f'\n➖ Энергия: ..⚡', keyboard=choice(keyboards.cleaner_work))
        elif payload == 'cleaner:false':
            await message.answer('🧹 Ты че, воздух подметаешь?'
                                 '\n---------------------------------------------------'
                                 f'\n💨💨💨💨💨💨💨💨💨💨'
                                 '\n---------------------------------------------------'
                                 f'\n➕ Огонёчков: 0🔥'
                                 f'\n➕ Опыт: ...✨'
                                 f'\n➖ Энергия: ...⚡', keyboard=choice(keyboards.cleaner_work))
