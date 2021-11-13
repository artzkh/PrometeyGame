from asyncio import sleep
from time import time, strftime, gmtime
import json
from random import choice

from vkbottle import VKAPIError, EMPTY_KEYBOARD
from vkbottle.bot import Blueprint
from vkbottle_types import GroupTypes
from vkbottle_types.events import GroupEventType

import config
from config import GROUP_ID, db
from functions import room_upgrade_message, buy_room_upgrade, kitchen_generator, \
    bedroom_generator, bathroom_generator, hall_generator, room_caller, kitchen_buy_satiety
from settings import event_block_time
from settings.cannot_change import products, needs_button
from states import States

import errors
import keyboards

bp = Blueprint("event")


@bp.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent):
    peer_state = await bp.state_dispenser.get(event.object.peer_id)
    payload = event.object.payload
    state = peer_state.state
    try:
        if state == States.ACTIVE:
            rec = peer_state.payload["recommendation"]
            try:
                if payload.get("room_menu"):
                    if payload["room_menu"] == "hall":
                        attachment, message, keyboard = await hall_generator(peer_id=event.object.peer_id, rec=rec)
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message,
                                                   attachment=attachment)
                    elif payload["room_menu"] == "kitchen":
                        attachment, message, keyboard = await kitchen_generator(peer_id=event.object.peer_id, rec=rec)
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message,
                                                   attachment=attachment)
                    elif payload["room_menu"] == "bedroom":
                        attachment, message, keyboard = await bedroom_generator(peer_id=event.object.peer_id, rec=rec)
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message,
                                                   attachment=attachment)
                    elif payload["room_menu"] == "bathroom":
                        attachment, message, keyboard = await bathroom_generator(peer_id=event.object.peer_id, rec=rec)
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message,
                                                   attachment=attachment)
                elif payload.get('products'):
                    balance, reserve = await config.db.get_balance_and_reserve(event.object.peer_id)
                    if balance < products[payload['products']]['fire']:
                        await bp.api.messages.send_message_event_answer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar",
                                                   "text": f"Для покупки {products[payload['products']]['emoji']} "
                                                           f"не хватает "
                                                           f"{products[payload['products']]['fire'] - balance}"
                                                           "&#128293;"}))
                    else:
                        balance -= products[payload['products']]['fire']
                        await config.db.buy_product(event.object.peer_id, balance,
                                                    products[payload['products']]['reserve'])
                        await bp.api.messages.send_message_event_answer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar",
                                                   "text": f"+{products[payload['products']]['reserve']}&#129377; "
                                                           f"к запасу еды. Баланс: {balance}&#128293;"
                                                           f"{reserve+products[payload['products']]['reserve']}&#129377;"}))
                elif payload.get('shop_house'):
                    if payload["shop_house"] == "products":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.products_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Продуктовая лавка',
                                                   attachment='photo318378590_457298973')
                    elif payload["shop_house"] == "coffee":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.coffee_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Кофейня',
                                                   attachment='photo318378590_457298978')
                    elif payload["shop_house"] == "sauna":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.sauna_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Сауна',
                                                   attachment='photo318378590_457298980')
                    elif payload["shop_house"] == "game":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.game_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Геймерская',
                                                   attachment='photo318378590_457298981')
                    elif payload["shop_house"] == "hookah":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.hookah_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Кальянная',
                                                   attachment='photo318378590_457298982')
                elif payload.get('reserve'):
                    reserve, ind, max_ind, ration = await config.db.get_user_reserve_satiety(event.object.peer_id)
                    if ind > max_ind - 1:
                        await bp.api.messages.send_message_event_answer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar",
                                                   "text": f"У тебя полные показатели сытости &#127831;"}))
                    elif reserve < 1:
                        await bp.api.messages.send_message_event_answer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar",
                                                   "text": "Пополни запасы в городской лавке"})
                        )
                    else:
                        if (ind > max_ind - 10) or (reserve < 10):
                            new_ind, reserve = ind+1, reserve-1
                        else:
                            new_ind, reserve = ind + 10, reserve - 10
                        attachment, message, keyboard, new_rec = await kitchen_buy_satiety(event.object.peer_id, rec,
                                                                                           ind, new_ind, reserve)
                        if rec != new_rec:
                            await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                         last_activity=peer_state.payload["last_activity"],
                                                         recommendation=new_rec)
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message,
                                                   attachment=attachment)

                elif payload.get('need_button'):
                    time_ind, ind, max_ind = await db.get_user_time_button(event.object.peer_id,
                                                                           payload.get('need_button'))
                    if ind > max_ind - 1:
                        await bp.api.messages.send_message_event_answer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar",
                                                   "text": needs_button[payload.get('need_button')]['full_snackbar']}))
                    elif time() >= (time_ind + needs_button[payload.get('need_button')]['time']):
                        recovery = needs_button[payload.get('need_button')]['recovery']
                        if (ind + recovery) >= max_ind:
                            new_ind = max_ind
                        else:
                            new_ind = ind + recovery
                        attachment, message, keyboard, new_rec = await room_caller(event.object.peer_id, rec,
                                                                                      payload.get('need_button'),
                                                                                      ind, new_ind)
                        if rec != new_rec:
                            await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                         last_activity=peer_state.payload["last_activity"],
                                                         recommendation=new_rec)
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message,
                                                   attachment=attachment)
                    else:
                        text = needs_button[payload.get('need_button')]['time_snackbar']
                        button_time = needs_button[payload.get('need_button')]['time']
                        if (time_ind + button_time) - time() >= 3600:
                            text += f"{strftime('%H:%M:%S', gmtime((time_ind + button_time) - int(time())))} &#9203;"
                        else:
                            text += f"{strftime('%M:%S', gmtime((time_ind + button_time) - int(time())))} &#9203;"
                        await bp.api.messages.send_message_event_answer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps({"type": "show_snackbar",
                                                   "text": text}))
                elif payload.get("room_upgrade"):
                    if payload["room_upgrade"] == "kitchen":
                        room = 2
                        keyboard = keyboards.upgrade_kitchen
                    elif payload["room_upgrade"] == "bedroom":
                        room = 3
                        keyboard = keyboards.upgrade_bedroom
                    elif payload["room_upgrade"] == "bathroom":
                        room = 4
                        keyboard = keyboards.upgrade_bathroom
                    else:
                        room = 1
                        keyboard = keyboards.upgrade_hall

                    message = await room_upgrade_message(event.object.peer_id, room)
                    if message:
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message=message)
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Заходи за апгрейдами к "
                                                                                    "другим комнатам &#128717;"}))
                elif payload.get("buy_upgrade"):
                    if payload["buy_upgrade"] == "kitchen":
                        room = 2
                        keyboard = [keyboards.buy_upgrade_kitchen_false,
                                    keyboards.buy_upgrade_kitchen_true]
                    elif payload["buy_upgrade"] == "bedroom":
                        room = 3
                        keyboard = [keyboards.buy_upgrade_bedroom_false,
                                    keyboards.buy_upgrade_bedroom_true]
                    elif payload["buy_upgrade"] == "bathroom":
                        room = 4
                        keyboard = [keyboards.buy_upgrade_bathroom_false,
                                    keyboards.buy_upgrade_bathroom_true]
                    else:
                        room = 1
                        keyboard = [keyboards.buy_upgrade_hall_false,
                                    keyboards.buy_upgrade_hall_true]

                    message = await buy_room_upgrade(event.object.peer_id, room)
                    if message:
                        if isinstance(message, str):
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboard[1],
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=message)
                        else:
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboard[0],
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=f"Эй, обмануть меня решил? "
                                                               f"Тут не хватает {message} &#128293;")
                    else:
                        await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                     user_id=event.object.user_id, delete_for_all=True,
                                                     conversation_message_ids=[event.object.conversation_message_id])
                elif payload.get("died"):
                    await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                 user_id=event.object.user_id,
                                                 conversation_message_ids=[event.object.conversation_message_id],
                                                 delete_for_all=True)
            except VKAPIError(909):
                attachment, message, keyboard = await hall_generator(peer_id=event.object.peer_id, rec=rec)
                await bp.api.messages.send(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                           keyboard=keyboard,
                                           random_id=0,
                                           message=message,
                                           attachment=attachment)
        elif state == States.DIED:
            try:
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
                                               message="Игра началась заново, "
                                                       "ты снова можешь нажимать на кнопки в нижнем меню. "
                                                       "На этот раз будь осторожнее!"
                                                       "\n"
                                                       "\nПомощь от государства: 1000 &#128293;")
                    await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE, last_activity=time(),
                                                 recommendation=[])
                else:
                    await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                               keyboard=keyboards.died,
                                               conversation_message_id=event.object.conversation_message_id,
                                               attachment="photo318378590_457297958",
                                               message="Здоровье твоего персонажа достигло 0")
            except VKAPIError(909):
                await bp.api.messages.send(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                           keyboard=keyboards.died,
                                           random_id=0,
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
        if state == States.ACTIVE:
            await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                         last_activity=peer_state.payload["last_activity"],
                                         recommendation=peer_state.payload["recommendation"])
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
