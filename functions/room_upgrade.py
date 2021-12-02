from random import choice

from config import db
from settings import rooms_update, rooms_name


async def room_upgrade_message(peer_id, room):

    room_lvl, furniture, balance = await db.get_user_room_lvl_furniture(peer_id, rooms_name[room])

    if furniture == len(rooms_update[room_lvl][room]):
        rooms = await db.get_user_rooms(peer_id)
        for room in range(4):
            if rooms[room] != len(rooms_update[room_lvl][room+1]):
                return False, None
        return None, None
    else:
        return f"{choice(rooms_update[room_lvl][room][furniture]['before'])}\n\n" \
               f"Цена: {rooms_update[room_lvl][room][furniture]['cost']}&#128293;" \
               f"\nБаланс: {balance}&#128293;",\
               rooms_update[room_lvl][room][furniture]['before_attachment']


async def buy_room_upgrade(peer_id, room):
    room_lvl, furniture, balance = await db.get_user_room_lvl_furniture_balance(peer_id, rooms_name[room])
    if furniture == len(rooms_update[room_lvl][room]):
        rooms = await db.get_user_rooms(peer_id)
        for room in range(4):
            if rooms[room] != len(rooms_update[room_lvl][room+1]):
                return False, None
        return None, None
    else:
        cost = rooms_update[room_lvl][room][furniture]['cost']
        if balance >= cost:
            await db.update_balance_furniture(peer_id, balance-cost, rooms_name[room], furniture + 1)
            return rooms_update[room_lvl][room][furniture]['after'],\
                rooms_update[room_lvl][room][furniture]['after_attachment']
        else:
            return rooms_update[room_lvl][room][furniture]['cost'] - balance, None
