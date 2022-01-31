from asyncio import sleep
from math import ceil
from time import time, strftime, gmtime
import json
from random import choice, randint

from vkbottle import VKAPIError, EMPTY_KEYBOARD
from vkbottle.bot import Blueprint
from vkbottle_types import GroupTypes
from vkbottle_types.events import GroupEventType

import config
from config import GROUP_ID, db
from functions import room_upgrade_message, buy_room_upgrade, kitchen_generator, \
    bedroom_generator, bathroom_generator, hall_generator, room_caller, kitchen_buy_satiety
from settings import event_block_time, rooms_update
from settings.cannot_change import products, needs_button, customers, coffee
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
                elif payload.get('shop_house'):
                    if payload["shop_house"] == "products":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.products_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Продуктовая лавка',
                                                   attachment='photo318378590_457300110')
                    elif payload["shop_house"] == "coffee":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.coffee_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Кофейня',
                                                   attachment='photo318378590_457300108')
                    elif payload["shop_house"] == "sauna":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.sauna_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Сауна',
                                                   attachment='photo318378590_457300111')
                    elif payload["shop_house"] == "game":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.game_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Игровой клуб',
                                                   attachment='photo318378590_457300109')
                    elif payload["shop_house"] == "hookah":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.hookah_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='VIP-комната',
                                                   attachment='photo318378590_457300112')
                    elif payload["shop_house"] == "pharmacy":
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboards.pharmacy_house,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   message='Аптека',
                                                   attachment='photo318378590_457300107')
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
                    elif payload["room_upgrade"] == "hall":
                        room = 1
                        keyboard = keyboards.upgrade_hall
                    else:
                        price = int(payload["room_upgrade"])
                        room_lvl, balance, hall, kitchen, bedroom, bathroom = \
                            await db.get_user_room_lvl_balance_rooms(peer_id=event.object.peer_id)
                        rooms = [hall, kitchen, bedroom, bathroom]
                        for room in range(4):
                            if rooms[room] != len(rooms_update[room_lvl][room + 1]):
                                await bp.api.messages.delete(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                             user_id=event.object.user_id,
                                                             conversation_message_ids=[
                                                                 event.object.conversation_message_id],
                                                             delete_for_all=True)
                                return
                        if room_lvl < len(rooms_update):
                            if balance >= price > 0:
                                new_balance = balance - price
                                await db.update_user_room_lvl(room_lvl + 1, new_balance,
                                                              event.object.peer_id)
                                attachment, _, keyboard = await hall_generator(peer_id=event.object.peer_id, rec=rec)
                                if room_lvl == 1:
                                    message = "Ура-ура, наконец-то мы выбрались из этой хрущевки!\n" \
                                             f"Покупка квартиры: -{price}&#128293;\n" \
                                             f"Баланс: {new_balance}&#128293;"
                                else:
                                    message = "Обожаю новоселья! &#127881;\n" \
                                              f"Покупка квартиры: -{price:,}&#128293;\n" \
                                              f"Баланс: {new_balance:,}&#128293;"
                                await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                           keyboard=keyboard,
                                                           conversation_message_id=event.object.conversation_message_id,
                                                           attachment=attachment,
                                                           message=message)
                                await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                             last_activity=peer_state.payload["last_activity"],
                                                             recommendation=peer_state.payload["recommendation"])
                            else:
                                await bp.api.messages.send_message_event_answer \
                                    (event_id=event.object.event_id,
                                     user_id=event.object.user_id,
                                     peer_id=event.object.peer_id,
                                     event_data=json.dumps({"type": "show_snackbar",
                                                            "text": f"Не хватает "
                                                                    f"{price - balance:,}"
                                                                    f"&#128293;"}))
                        else:
                            await bp.api.messages.send_message_event_answer \
                                (event_id=event.object.event_id,
                                 user_id=event.object.user_id,
                                 peer_id=event.object.peer_id,
                                 event_data=json.dumps({"type": "show_snackbar",
                                                        "text": f"Ты достиг фэншуя! &#9775;"}))
                        return

                    message, attachment = await room_upgrade_message(event.object.peer_id, room)
                    if message:
                        await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                   keyboard=keyboard,
                                                   conversation_message_id=event.object.conversation_message_id,
                                                   attachment=attachment,
                                                   message=message)
                    elif message is None:
                        if peer_state.payload.get("num_offer"):
                            if peer_state.payload["num_offer"] > 2:
                                await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                                user_id=event.object.user_id,
                                                                                peer_id=event.object.peer_id,
                                                                                event_data=json.dumps({
                                                                                    "type": "show_snackbar",
                                                                                    "text": "Предложения скоро появятся &#128172;"}))
                                return
                            else:
                                await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                             last_activity=peer_state.payload["last_activity"],
                                                             recommendation=peer_state.payload["recommendation"],
                                                             num_offer=peer_state.payload["num_offer"]+1)
                        else:
                            await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                         last_activity=peer_state.payload["last_activity"],
                                                         recommendation=peer_state.payload["recommendation"],
                                                         num_offer=1)
                        if room == 2:
                            keyboard = keyboards.upgrade_room_lvl_kitchen
                        elif room == 3:
                            keyboard = keyboards.upgrade_room_lvl_bedroom
                        elif room == 4:
                            keyboard = keyboards.upgrade_room_lvl_bathroom
                        else:
                            keyboard = keyboards.upgrade_room_lvl_hall
                        balance = await db.get_user_fire_balance(peer_id=event.object.peer_id)
                        price = randint(1, 10)
                        if price == 2:
                            price = choice([8499, 7700, 7499, 7000, 6999])
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       keyboard=keyboard.replace('lvl', str(price)),
                                                       message=f"&#128081; Предложение от админов &#128081;\n"
                                                               f"[id318378590|Артём] и [id214904186|Артем] предложили "
                                                               f"купить квартиру"
                                                               f"\n\nЦена: {price}&#128293;"
                                                               f"\nБаланс: {balance}&#128293;")
                        else:
                            price = choice([9499, 9999, 10000, 12499, 11990, 13500, 15000, 19900, 22000])
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       keyboard=keyboard.replace('lvl', str(price)),
                                                       message=f"{choice(customers)} "
                                                               f"купить новую квартиру"
                                                               f"\n\nЦена: {price}&#128293;"
                                                               f"\nБаланс: {balance}&#128293;")
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Заходи за мебелью к "
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

                    message, attachment = await buy_room_upgrade(event.object.peer_id, room)
                    if message:
                        if isinstance(message, str):
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboard[1],
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       attachment=attachment,
                                                       message=message)
                        else:
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       keyboard=keyboard[0],
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       message=f"Эй, обмануть меня решил?"
                                                               f"\nТут не хватает {message}&#128293;")
                    elif message is None:
                        if peer_state.payload.get("num_offer"):
                            if peer_state.payload["num_offer"] > 2:
                                await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                                user_id=event.object.user_id,
                                                                                peer_id=event.object.peer_id,
                                                                                event_data=json.dumps({
                                                                                    "type": "show_snackbar",
                                                                                    "text": "Предложения скоро появятся &#128172;"}))
                                return
                            else:
                                await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                             last_activity=peer_state.payload["last_activity"],
                                                             recommendation=peer_state.payload["recommendation"],
                                                             num_offer=peer_state.payload["num_offer"]+1)
                        else:
                            await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                         last_activity=peer_state.payload["last_activity"],
                                                         recommendation=peer_state.payload["recommendation"],
                                                         num_offer=1)
                        if room == 2:
                            keyboard = keyboards.upgrade_room_lvl_kitchen
                        elif room == 3:
                            keyboard = keyboards.upgrade_room_lvl_bedroom
                        elif room == 4:
                            keyboard = keyboards.upgrade_room_lvl_bathroom
                        else:
                            keyboard = keyboards.upgrade_room_lvl_hall
                        balance = await db.get_user_fire_balance(peer_id=event.object.peer_id)
                        price = randint(1, 10)
                        if price == 2:
                            price = choice([8499, 7700, 7499, 7000, 6999])
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       keyboard=keyboard.replace('lvl', str(price)),
                                                       message=f"&#128081; Предложение от админов &#128081;\n"
                                                               f"[id318378590|Артём] и [id214904186|Артем] предложили "
                                                               f"купить квартиру"
                                                               f"\n\nЦена: {price}&#128293;"
                                                               f"\nБаланс: {balance}&#128293;")
                        else:
                            price = choice([9499, 9999, 10000, 12499, 11990, 13500, 15000, 19900, 22000])
                            await bp.api.messages.edit(peer_id=event.object.peer_id, group_id=GROUP_ID,
                                                       conversation_message_id=event.object.conversation_message_id,
                                                       keyboard=keyboard.replace('lvl', str(price)),
                                                       message=f"{choice(customers)} "
                                                               f"купить новую квартиру"
                                                               f"\n\nЦена: {price}&#128293;"
                                                               f"\nБаланс: {balance}&#128293;")
                        await bp.state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                                     last_activity=peer_state.payload["last_activity"],
                                                     recommendation=peer_state.payload["recommendation"],
                                                     price=price)
                    else:
                        await bp.api.messages.send_message_event_answer(event_id=event.object.event_id,
                                                                        user_id=event.object.user_id,
                                                                        peer_id=event.object.peer_id,
                                                                        event_data=json.dumps({
                                                                            "type": "show_snackbar",
                                                                            "text": "Заходи за мебелью к "
                                                                                    "другим комнатам &#128717;"}))
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
