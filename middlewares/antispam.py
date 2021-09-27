from time import time

from vkbottle import BaseMiddleware, MiddlewareResponse
from vkbottle.bot import Message
from vkbottle_types import GroupTypes

from config import ADMINS, db
from functions import calculate_indicators
from states import state_dispenser, States


class MessageSpamMiddleware(BaseMiddleware):
    async def pre(self, message: Message):
        if message.state_peer is None:
            user_status = await db.get_user_status(peer_id=message.peer_id)
            if user_status == "active":
                await state_dispenser.set(message.peer_id, States.ACTIVE,
                                          last_activity=await db.get_user_last_activity(message.peer_id))
                message.state_peer = await state_dispenser.get(message.peer_id)
            elif user_status == "training":
                await state_dispenser.set(message.peer_id, States.TRAINING, position=0)
                message.state_peer = await state_dispenser.get(message.peer_id)
                return True
            elif user_status == "died":
                await state_dispenser.set(message.peer_id, States.DIED)
                message.state_peer = await state_dispenser.get(message.peer_id)
                return True
            elif user_status is None:
                await db.add_user(
                    peer_id=message.peer_id,
                    username=(await message.get_user(user_id=message.peer_id)).first_name
                )
                await state_dispenser.set(message.peer_id, States.TRAINING, position=0)
                message.state_peer = await state_dispenser.get(message.peer_id)
                return True
            else:
                return MiddlewareResponse(False)
        elif message.state_peer.state == States.TRAINING or message.state_peer.state == States.DIED:
            return True
        if (time() - message.state_peer.payload["last_activity"]) // 60 > 5:
            rec = await calculate_indicators(message.peer_id, message.state_peer.payload["last_activity"])
            if rec == {}:
                await message.answer(str(await db.get_user_indicators(message.peer_id)) + "\nРекомендаций нет")
                await state_dispenser.set(message.peer_id, States.ACTIVE, last_activity=time())
            elif rec:
                await message.answer(str(await db.get_user_indicators(message.peer_id)) + "\nРекомендации:\n" + str(rec))
                await state_dispenser.set(message.peer_id, States.ACTIVE, last_activity=time())
            else:
                await state_dispenser.set(message.peer_id, States.DIED)
                message.state_peer = await state_dispenser.get(message.peer_id)
                await db.update_status(message.peer_id, "died")
                return True
            message.state_peer = await state_dispenser.get(message.peer_id)


class EventSpamMiddleware(BaseMiddleware):
    async def pre(self, event: GroupTypes.MessageEvent):
        state_peer = await state_dispenser.get(event.object.peer_id)
        if state_peer is None:
            user_status = await db.get_user_status(peer_id=event.object.peer_id)
            if user_status == "active":
                await state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                          last_activity=await db.get_user_last_activity(event.object.peer_id))
                state_peer = await state_dispenser.get(event.object.peer_id)
            elif user_status == "training":
                await state_dispenser.set(event.object.peer_id, States.TRAINING, position=0)
                return
            elif user_status == "died":
                await state_dispenser.set(event.object.peer_id, States.DIED)
                return True
            elif user_status is None:
                await db.add_user(
                    peer_id=event.object.peer_id,
                    username="Прометей"
                )
                await state_dispenser.set(event.object.peer_id, States.TRAINING, position=0)
                return True
            else:
                return MiddlewareResponse(False)
        elif state_peer.state == States.TRAINING or state_peer.state == States.DIED:
            return True
        if (time() - state_peer.payload["last_activity"]) // 60 > 5:
            rec = await calculate_indicators(event.object.peer_id, state_peer.payload["last_activity"])
            if rec == {}:
                await state_dispenser.set(event.object.peer_id, States.ACTIVE, last_activity=time())
                return True
            elif rec:
                await state_dispenser.set(event.object.peer_id, States.ACTIVE, last_activity=time())
                return {'rec': rec}
            else:
                await state_dispenser.set(event.object.peer_id, States.DIED)
                await db.update_status(event.object.peer_id, "died")
                return True
