from time import time

import keyboards
from config import db
from math import ceil
from json_data import pictures
from settings.cannot_change import max_room_update, needs_button


async def room_caller(peer_id, rec, button):
    if button == 'ration':
        return await kitchen_generator(peer_id, rec)
    elif button in ['draw', 'read']:
        return await hall_generator(peer_id, rec)
    elif button in ['shower', 'toilet']:
        return await bathroom_generator(peer_id, rec)
    else:
        return await bedroom_generator(peer_id, rec)


async def hall_generator(peer_id, rec, changes=False):
    attachment, clothes, room_lvl, room_furniture, happiness, max_happiness, time_draw, time_read = \
        await db.get_user_hall(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_1_{room_furniture}"
    message = f"Гостинная [{room_furniture}/{max_room_update[room_lvl][1]}]" \
              f"\n\nСчастье: {ceil(happiness)}/{max_happiness} &#127881;"

    if time() >= (time_read + needs_button['draw']['time']):
        if time() >= (time_read + needs_button['read']['time']):
            keyboard = keyboards.room_hall_true_true
        else:
            keyboard = keyboards.room_hall_true_false
    else:
        if time() >= (time_read + needs_button['read']['time']):
            keyboard = keyboards.room_hall_false_true
        else:
            keyboard = keyboards.room_hall

    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message, keyboard


async def kitchen_generator(peer_id, rec, changes=False):
    attachment, clothes, room_lvl, room_furniture, satiety, max_satiety, reserve, ration = \
        await db.get_user_kitchen(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_2_{room_furniture}"
    message = f"Кухня [{room_furniture}/{max_room_update[room_lvl][2]}]" \
              f"\n\nСытость: {ceil(satiety)}/{max_satiety} &#127831;" \
              f"\nВ запасе: {reserve} &#129377;"

    if (satiety > max_satiety - 10) or (reserve < 10):
        if time() >= (ration + needs_button['ration']['time']):
            keyboard = keyboards.room_kitchen_snack_true
        else:
            keyboard = keyboards.room_kitchen_snack
    else:
        if time() >= (ration + needs_button['ration']['time']):
            keyboard = keyboards.room_kitchen_eat_true
        else:
            keyboard = keyboards.room_kitchen_eat

    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message, keyboard


async def bedroom_generator(peer_id, rec, changes=False):
    attachment, clothes, room_lvl, room_furniture, energy, max_energy, time_sleep, time_rest = \
        await db.get_user_bedroom(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_3_{room_furniture}"
    message = f"Спальня [{room_furniture}/{max_room_update[room_lvl][3]}]" \
              f"\n\nЭнергия: {ceil(energy)}/{max_energy} &#9889;"

    if time() >= (time_sleep + needs_button['sleep']['time']):
        if time() >= (time_rest + needs_button['rest']['time']):
            keyboard = keyboards.room_bedroom_true_true
        else:
            keyboard = keyboards.room_bedroom_true_false
    else:
        if time() >= (time_rest + needs_button['rest']['time']):
            keyboard = keyboards.room_bedroom_false_true
        else:
            keyboard = keyboards.room_bedroom

    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message, keyboard


async def bathroom_generator(peer_id, rec, changes=False):
    attachment, clothes, room_lvl, room_furniture, hygiene, max_hygiene, time_shower, time_toilet = \
        await db.get_user_bathroom(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_4_{room_furniture}"
    message = f"Ванная [{room_furniture}/{max_room_update[room_lvl][4]}]" \
              f"\n\nГигиена: {ceil(hygiene)}/{max_hygiene} &#129532;"

    if time() >= (time_shower + needs_button['shower']['time']):
        if time() >= (time_toilet + needs_button['toilet']['time']):
            keyboard = keyboards.room_bathroom_true_true
        else:
            keyboard = keyboards.room_bathroom_true_false
    else:
        if time() >= (time_toilet + needs_button['toilet']['time']):
            keyboard = keyboards.room_bathroom_false_true
        else:
            keyboard = keyboards.room_bathroom

    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message, keyboard


def rec_msg(rec):
    rec_message = ""
    for i in rec:
        if i == "health":
            rec_message = f"Проверить здоровье &#129505;\n" + rec_message
        elif i == "satiety":
            rec_message += f"Перекусить &#127831;\n"
        elif i == "hygiene":
            rec_message += f"Сходить в душ &#129532;\n"
        elif i == "happiness":
            rec_message += f"Развлечься &#127881;\n"
        elif i == "energy":
            rec_message += f"Восстановить энергию &#9889;\n"
    return "Рекомендации:\n" + rec_message
