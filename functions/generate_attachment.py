from config import db
from math import ceil
from json_data import pictures
from settings.cannot_change import max_room_update


async def hall_generator(peer_id, rec):
    attachment, clothes, room_lvl, room_furniture, happiness, max_happiness, reserve = await db.get_user_hall(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_1_{room_furniture}"
    message = f"Гостинная [{room_furniture}/{max_room_update[room_lvl][1]}]" \
              f"\n\nСчастье: {ceil(happiness)}/{max_happiness} &#127881;" \
              f"\nВ запасе: {reserve} &#11088;"
    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message


async def kitchen_generator(peer_id, rec):
    attachment, clothes, room_lvl, room_furniture, satiety, max_satiety, reserve = await db.get_user_kitchen(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_2_{room_furniture}"
    message = f"Кухня [{room_furniture}/{max_room_update[room_lvl][2]}]" \
              f"\n\nСытость: {ceil(satiety)}/{max_satiety} &#127831;" \
              f"\nВ запасе: {reserve} &#11088;"
    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message


async def bedroom_generator(peer_id, rec):
    attachment, clothes, room_lvl, room_furniture, energy, max_energy, reserve = await db.get_user_bedroom(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_3_{room_furniture}"
    message = f"Спальня [{room_furniture}/{max_room_update[room_lvl][3]}]" \
              f"\n\nЭнергия: {ceil(energy)}/{max_energy} &#9889;" \
              f"\nВ запасе: {reserve} &#11088;"
    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message


async def bathroom_generator(peer_id, rec):
    attachment, clothes, room_lvl, room_furniture, hygiene, max_hygiene, reserve = await db.get_user_bathroom(peer_id)
    attachment = f"{attachment}_{clothes}_{room_lvl}_4_{room_furniture}"
    message = f"Ванная [{room_furniture}/{max_room_update[room_lvl][4]}]" \
              f"\n\nГигиена: {ceil(hygiene)}/{max_hygiene} &#129532;" \
              f"\nВ запасе: {reserve} &#11088;"
    if rec:
        message += f"\n\n{rec_msg(rec)}"

    return pictures[attachment], message


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
