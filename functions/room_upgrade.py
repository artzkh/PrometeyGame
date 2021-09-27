from random import choice

from config import db
from settings import rooms_update, rooms_name


async def room_upgrade_message(peer_id, room):

    room_lvl, furniture = await db.get_user_room_lvl_furniture(peer_id, rooms_name[room])

    if furniture == len(rooms_update[room_lvl][room]):
        return False
    else:
        return f"{choice(rooms_update[room_lvl][room][furniture]['before'])}\n\n" \
               f"Цена: {rooms_update[room_lvl][room][furniture]['cost']} &#128293;"


async def buy_room_upgrade(peer_id, room):

    room_lvl, furniture, balance = await db.get_user_room_lvl_furniture_balance(peer_id, rooms_name[room])

    if furniture == len(rooms_update[room_lvl][room]):
        return False
    else:
        cost = rooms_update[room_lvl][room][furniture]['cost']
        if balance >= cost:
            await db.update_balance_furniture(peer_id, balance-cost, rooms_name[room], furniture + 1)
            return rooms_update[room_lvl][room][furniture]['after']
        else:
            return rooms_update[room_lvl][room][furniture]['cost'] - balance
