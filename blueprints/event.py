from asyncio import sleep
from time import time
import json
from random import choice

from vkbottle import VKAPIError, EMPTY_KEYBOARD
from vkbottle.bot import Blueprint
from vkbottle_types import GroupTypes
from vkbottle_types.events import GroupEventType

from config import GROUP_ID, db
from json_data import pictures
from functions import generate_attachment, room_upgrade_message, buy_room_upgrade
from settings import event_block_time
from states import States

import errors
import keyboards

bp = Blueprint("event")


@bp.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent, rec: dict = None):
    peer_state = await bp.state_dispenser.get(event.object.peer_id)
    payload = event.object.payload
    state = peer_state.state
    try:
        if rec:
            rec_message = ""
            sorted_keys = sorted(rec, key=rec.get)
            for i in sorted_keys:
                if i == "health":
                    rec_message = f"Здоровье: {rec[i]} &#129505;\n" + rec_message
                elif i == "satiety":
                    rec_message += f"Сытость: {rec[i]} &#127831;\n"
                elif i == "hygiene":
                    rec_message += f"Гигиена: {rec[i]} &#129532;\n"
                elif i == "happiness":
                    rec_message += f"Счастье: {rec[i]} &#127881;\n"
                elif i == "energy":
                    rec_message += f"Энергия: {rec[i]} &#9889;\n"
            await bp.api.messages.send(peer_id=event.object.peer_id,
                                       group_id=GROUP_ID,
                                       random_id=0,
                                       message="Рекомендации: \n" + rec_message)
        if state == States.ACTIVE:
            if payload.get("room_menu"):
                if payload["room_menu"] == "hall":
                    await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                               keyboard=keyboards.room_hall,
                                               conversation_message_id=event.object.conversation_message_id,
                                               message="//Тестовое сообщение",
                                               attachment=pictures[
                                                    await generate_attachment(peer_id=event.object.peer_id, room=1)])
                elif payload["room_menu"] == "kitchen":
                    await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                               keyboard=choice([keyboards.room_kitchen_1, keyboards.room_kitchen_2]),
                                               conversation_message_id=event.object.conversation_message_id,
                                               message="100 &#128293;",
                                               attachment=pictures[
                                                   await generate_attachment(peer_id=event.object.peer_id, room=2)])
                elif payload["room_menu"] == "bedroom":
                    await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID, keyboard=keyboards.room_bedroom,
                                               conversation_message_id=event.object.conversation_message_id,
                                               message="100 &#128293;",
                                               attachment=pictures[
                                                   await generate_attachment(peer_id=event.object.peer_id, room=3)])
                elif payload["room_menu"] == "bathroom":
                    await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID, keyboard=keyboards.room_bathroom,
                                               conversation_message_id=event.object.conversation_message_id,
                                               message="100 &#128293;",
                                               attachment=pictures[
                                                   await generate_attachment(peer_id=event.object.peer_id, room=4)])
            elif payload.get("room_upgrade"):
                if payload["room_upgrade"] == "hall":
                    message = await room_upgrade_message(event.object.peer_id, 1)
                    if message:
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.upgrade_hall,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message)
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Продавцу больше нечего "
                                                                                    "предложить для Гостинной. "
                                                                                    "Заходи за апгрейдами к "
                                                                                    "другим комнатам &#128717;"}))
                elif payload["room_upgrade"] == "kitchen":
                    message = await room_upgrade_message(event.object.peer_id, 2)
                    if message:
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.upgrade_kitchen,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message)
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Продавцу больше нечего "
                                                                                    "предложить для Кухни. "
                                                                                    "Заходи за апгрейдами к "
                                                                                    "другим комнатам &#128717;"}))
                elif payload["room_upgrade"] == "bedroom":
                    message = await room_upgrade_message(event.object.peer_id, 3)
                    if message:
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.upgrade_bedroom,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message)
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Продавцу больше нечего "
                                                                                    "предложить для Спальни. "
                                                                                    "Заходи за апгрейдами к "
                                                                                    "другим комнатам &#128717;"}))
                elif payload["room_upgrade"] == "bathroom":
                    message = await room_upgrade_message(event.object.peer_id, 4)
                    if message:
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.upgrade_bathroom,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message)
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Продавцу больше нечего "
                                                                                    "предложить для Ванной. "
                                                                                    "Заходи за апгрейдами к "
                                                                                    "другим комнатам &#128717;"}))
            elif payload.get("buy_upgrade"):
                if payload["buy_upgrade"] == "hall":
                    message = await buy_room_upgrade(event.object.peer_id, 1)
                    if message:
                        if isinstance(message, str):
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_hall_true,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=message)
                        else:
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_hall_false,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=f"Эй, обмануть меня решил? "
                                                               f"Тут не хватает {message} &#128293;")
                    else:
                        await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID, user_id=event.object.user_id,
                                                     conversation_message_ids=[event.object.conversation_message_id],
                                                     delete_for_all=True)

                elif payload["buy_upgrade"] == "kitchen":
                    message = await buy_room_upgrade(event.object.peer_id, 2)
                    if message:
                        if isinstance(message, str):
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_kitchen_true,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=message)
                        else:
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_kitchen_false,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=f"Эй, обмануть меня решил? "
                                                               f"Тут не хватает {message} &#128293;")
                    else:
                        await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID, user_id=event.object.user_id,
                                                     conversation_message_ids=[event.object.conversation_message_id],
                                                     delete_for_all=True)
                elif payload["buy_upgrade"] == "bedroom":
                    message = await buy_room_upgrade(event.object.peer_id, 3)
                    if message:
                        if isinstance(message, str):
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_bedroom_true,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=message)
                        else:
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_bedroom_false,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=f"Эй, обмануть меня решил? "
                                                               f"Тут не хватает {message} &#128293;")
                    else:
                        await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID, user_id=event.object.user_id,
                                                     conversation_message_ids=[event.object.conversation_message_id],
                                                     delete_for_all=True)
                elif payload["buy_upgrade"] == "bathroom":
                    message = await buy_room_upgrade(event.object.peer_id, 4)
                    if message:
                        if isinstance(message, str):
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_bathroom_true,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=message)
                        else:
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboards.buy_upgrade_bathroom_false,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=f"Эй, обмануть меня решил? "
                                                               f"Тут не хватает {message} &#128293;")
                    else:
                        await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID, user_id=event.object.user_id,
                                                     conversation_message_ids=[event.object.conversation_message_id],
                                                     delete_for_all=True)
        elif state == States.DIED:
            if payload.get("died") == "start_over":
                await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                           keyboard=keyboards.start_over,
                                           conversation_message_id=event.object.conversation_message_id,
                                           message="Ты потеряешь всё, что у тебя было. "
                                                   "Уверен, что хочешь начать сначала?")
            elif payload.get("died") == "start_over_no":
                await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                           keyboard=keyboards.died,
                                           conversation_message_id=event.object.conversation_message_id,
                                           attachment="photo318378590_457297958")
            elif payload.get("died") == "start_over_yes":
                await db.start_over(event.object.peer_id)
                await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                           keyboard=keyboards.menu_positive,
                                           conversation_message_id=event.object.conversation_message_id,
                                           message="Не подведи меня в этот раз!"
                                                   "\n"
                                                   "\nПомощь от государства: 1000 &#128293;")
                await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE, last_activity=time())
            else:
                await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                           keyboard=keyboards.died,
                                           conversation_message_id=event.object.conversation_message_id,
                                           attachment="photo318378590_457297958",
                                           message="Здоровье твоего персонажа достигло 0")

    except VKAPIError(9):
        await bp.state_dispenser.set(event.object.peer_id, States.SPAM)
        await bp.api.messages.send(peer_id=event.object.peer_id,
                                   group_id=GROUP_ID,
                                   random_id=0,
                                   keyboard=EMPTY_KEYBOARD,
                                   message=choice(errors.spam_errors))
        await sleep(event_block_time)

        if peer_state == States.ACTIVE:
            await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE, last_activity=peer_state.payload["last_activity"])
            await bp.api.messages.send(peer_id=event.object.peer_id,
                                       group_id=GROUP_ID,
                                       random_id=0,
                                       keyboard=keyboards.menu_positive,
                                       message="Персонаж разблокирован!")  # позитив негатив
        elif peer_state == States.TRAINING:
            await bp.state_dispenser.set(event.object.peer_id, States.TRAINING,
                                         time=time(),
                                         messages=0,
                                         position=peer_state.payload["position"])
            await bp.api.messages.send(peer_id=event.object.peer_id,
                                       group_id=GROUP_ID,
                                       random_id=0,
                                       keyboard=keyboards.menu_positive,
                                       message="Персонаж разблокирован!")  # позитив негатив
