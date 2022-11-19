from config import db


async def get_passport_info(peer_id):
    username, fire_balance, chung_balance, bonus_day, room_lvl, work_experience = await db.get_user_passport(peer_id)
    return f'&#9989; Паспорт игрока: [id{peer_id}|{username}]' \
           f'\n&#128081; Prometey Pass: нет' \
           '\n---------------------------------------------------' \
           f'\n&#126980; Чжун: {chung_balance}' \
           f'\n&#128293; Огонёчков: {fire_balance}' \
           f'\n&#10024; Опыт: {work_experience}' \
           f'\n&#127873; Бонус: {bonus_day} день' \
           f'\n&#127968; Уровень квартиры: {room_lvl}'
