from config import db
from settings import rooms_name


async def generate_attachment(peer_id, room):
    attachment, clothes, room_lvl, room_furniture = await db.get_user_attachment(peer_id, rooms_name.get(room))
    return f"{attachment}_{clothes}_{room_lvl}_{room}_{room_furniture}"
