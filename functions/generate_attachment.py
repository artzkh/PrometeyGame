from time import time

import config
import keyboards
from config import db
from math import ceil
from json_data import pictures
from settings.cannot_change import max_room_update, needs_button, rec_limit


async def room_caller(peer_id, rec, button, index, new_index):
    if button == 'ration':
        if await kitchen_change(peer_id, button, index, new_index):
            rec.remove("satiety")
        attachment, message, keyboard = await kitchen_generator(peer_id, rec)
    elif button in ['draw', 'read']:
        if await hall_change(peer_id, button, index, new_index):
            rec.remove("happiness")
        attachment, message, keyboard = await hall_generator(peer_id, rec)
    elif button in ['shower', 'toilet']:
        if await bathroom_change(peer_id, button, index, new_index):
            rec.remove("hygiene")
        attachment, message, keyboard = await bathroom_generator(peer_id, rec)
    else:
        if await bedroom_change(peer_id, button, index, new_index):
            rec.remove("energy")
        attachment, message, keyboard = await bedroom_generator(peer_id, rec)
    return attachment, message, keyboard, rec


async def hall_generator(peer_id, rec):
    body, dirt, face_num, clothes, room_lvl, room_furniture, happiness, max_happiness, \
          time_draw, time_read, health, max_health = await db.get_user_hall(peer_id)
    attachment = f"{body}_{dirt}_{face_num}_{clothes}_{room_lvl}_1_{room_furniture}"
    message = f"Гостинная [{room_furniture}/{max_room_update[room_lvl][1]}]" \
              f"\n\nСчастье: {ceil(happiness)}/{max_happiness} &#127881;"
    if health < max_health:
        message += f"\nЗдоровье: {ceil(health)}/{max_health} &#129505;"

    if time() >= (time_draw + needs_button['draw']['time']):
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


async def hall_change(peer_id, button, old_happiness, happiness):
    energy = await config.db.get_user_energy(peer_id)
    old_happiness, happiness = ceil(old_happiness), ceil(happiness)

    if energy < 30:
        if (old_happiness < rec_limit['happiness']) and (happiness >= rec_limit['happiness']):
            await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 3)
            return True
        else:
            await config.db.update_user_time_button(peer_id, button, happiness)
    elif energy < 80:
        if (old_happiness < rec_limit['happiness']) and (happiness >= rec_limit['happiness']):
            if happiness >= 60:
                await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 2)
            else:
                await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 3)
            return True
        elif (old_happiness < 60) and (happiness >= 60):
            await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 2)
        else:
            await config.db.update_user_time_button(peer_id, button, happiness)
    else:
        if (old_happiness < rec_limit['happiness']) and (happiness >= rec_limit['happiness']):
            if happiness >= 100:
                await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 1)
            elif happiness >= 60:
                await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 2)
            else:
                await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 3)
            return True
        elif (old_happiness < 100) and (happiness >= 100):
            await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 1)
        elif (old_happiness < 60) and (happiness >= 60):
            await config.db.update_user_time_button_with_attachment(peer_id, button, happiness, 'face', 2)
        else:
            await config.db.update_user_time_button(peer_id, button, happiness)
    return False


async def kitchen_generator(peer_id, rec):
    body, dirt, face_num, clothes, room_lvl, room_furniture, \
          satiety, max_satiety, reserve, ration = await db.get_user_kitchen(peer_id)
    attachment = f"{body}_{dirt}_{face_num}_{clothes}_{room_lvl}_2_{room_furniture}"
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


async def kitchen_change(peer_id, button, old_satiety, satiety):
    old_satiety, satiety = ceil(old_satiety), ceil(satiety)

    if (old_satiety < rec_limit['satiety']) and (satiety >= rec_limit['satiety']):
        if satiety < 70:
            await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 2)
        elif satiety >= 70:
            await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 3)
        elif satiety >= 120:
            await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 4)
        elif satiety >= 200:
            await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 5)
        return True
    elif (old_satiety < 70) and (satiety >= 70):
        await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 3)
    elif (old_satiety < 120) and (satiety >= 120):
        await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 4)
    elif (old_satiety < 200) and (satiety >= 200):
        await config.db.update_user_time_button_with_attachment(peer_id, button, satiety, 'body', 5)
    else:
        await config.db.update_user_time_button(peer_id, button, satiety)
    return False


async def buy_satiety(peer_id, old_satiety, satiety, reserve):

    if satiety >= 200:
        body = 5
    elif satiety >= 120:
        body = 4
    elif satiety >= 70:
        body = 3
    else:
        body = 2

    if (old_satiety < rec_limit['satiety']) and (satiety >= rec_limit['satiety']):
        await config.db.buy_satiety_with_attachment(peer_id, satiety, reserve, body)
        return True
    elif (old_satiety < 70) and (satiety >= 70):
        await config.db.buy_satiety_with_attachment(peer_id, satiety, reserve, body)
    elif (old_satiety < 120) and (satiety >= 120):
        await config.db.buy_satiety_with_attachment(peer_id, satiety, reserve, body)
    elif (old_satiety < 200) and (satiety >= 200):
        await config.db.buy_satiety_with_attachment(peer_id, satiety, reserve, body)
    else:
        await config.db.buy_satiety(peer_id, satiety, reserve)


async def kitchen_buy_satiety(peer_id, rec, old_satiety, satiety, reserve):
    if await buy_satiety(peer_id, ceil(old_satiety), ceil(satiety), reserve):
        rec.remove('satiety')
    attachment, message, keyboard = await kitchen_generator(peer_id, rec)
    return attachment, message, keyboard, rec


async def bedroom_generator(peer_id, rec):
    body, dirt, face_num, clothes, room_lvl, room_furniture, energy, max_energy, \
          time_sleep, time_rest, health, max_health = await db.get_user_bedroom(peer_id)
    attachment = f"{body}_{dirt}_{face_num}_{clothes}_{room_lvl}_3_{room_furniture}"
    message = f"Спальня [{room_furniture}/{max_room_update[room_lvl][3]}]" \
              f"\n\nЭнергия: {ceil(energy)}/{max_energy} &#9889;"
    if health < max_health:
        message += f"\nЗдоровье: {ceil(health)}/{max_health} &#129505;"

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


async def bedroom_change(peer_id, button, old_energy, energy):
    happiness = await config.db.get_user_happiness(peer_id)
    old_energy, energy = ceil(old_energy), ceil(energy)

    if happiness >= 100:
        if (old_energy < 80) and (energy >= 80):
            await config.db.update_user_time_button_with_attachment(peer_id, button, energy, 'face', 1)
        elif (old_energy < 30) and (energy >= 30):
            await config.db.update_user_time_button_with_attachment(peer_id, button, energy, 'face', 2)
        else:
            await config.db.update_user_time_button(peer_id, button, energy)
    elif happiness >= 60:
        if (old_energy < 30) and (energy >= 30):
            await config.db.update_user_time_button_with_attachment(peer_id, button, energy, 'face', 2)
        else:
            await config.db.update_user_time_button(peer_id, button, energy)
    else:
        await config.db.update_user_time_button(peer_id, button, energy)

    if (old_energy < rec_limit['happiness']) and (energy >= rec_limit['happiness']):
        return True


async def bathroom_generator(peer_id, rec):
    body, dirt, face_num, clothes, room_lvl, room_furniture, hygiene, max_hygiene, \
          time_shower, time_toilet, health, max_health = await db.get_user_bathroom(peer_id)
    attachment = f"{body}_{dirt}_{face_num}_{clothes}_{room_lvl}_4_{room_furniture}"
    message = f"Ванная [{room_furniture}/{max_room_update[room_lvl][4]}]" \
              f"\n\nГигиена: {ceil(hygiene)}/{max_hygiene} &#129531;"
    if health < max_health:
        message += f"\nЗдоровье: {ceil(health)}/{max_health} &#129505;"

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


async def bathroom_change(peer_id, button, old_hygiene, hygiene):
    old_hygiene, hygiene = ceil(old_hygiene), ceil(hygiene)

    if (old_hygiene < rec_limit['satiety']) and (hygiene >= rec_limit['satiety']):
        await config.db.update_user_time_button_with_attachment(peer_id, button, hygiene, 'dirt', 1)
        return True
    else:
        await config.db.update_user_time_button(peer_id, button, hygiene)
        return False


def rec_msg(rec):
    rec_message = ""
    for i in rec:
        if i == "health":
            # rec_message = f"Проверить здоровье &#129505;\n" + rec_message
            rec_message = "&#129505;" + rec_message
        elif i == "satiety":
            # rec_message += f"Перекусить &#127831;\n"
            rec_message += "&#127831;"
        elif i == "hygiene":
            # rec_message += f"Сходить в душ &#129532;\n"
            rec_message += "&#129531;"
        elif i == "happiness":
            # rec_message += f"Развлечься &#127881;\n"
            rec_message += "&#127881;"
        elif i == "energy":
            # rec_message += f"Восстановить энергию &#9889;\n"
            rec_message += "&#9889;"
    return "Рекомендации:\n" + rec_message
