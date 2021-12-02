from time import time

from vkbottle import BaseMiddleware, MiddlewareResponse
from vkbottle.bot import Message
from vkbottle_types import GroupTypes

from config import db
from functions import calculate_indicators, rec_msg
from states import state_dispenser, States


class MessageSpamMiddleware(BaseMiddleware):
    async def pre(self, message: Message):
        if message.state_peer is None:
            user_status = await db.get_user_status(peer_id=message.peer_id)
            if user_status == "active":
                await state_dispenser.set(message.peer_id, States.ACTIVE,
                                          last_activity=await db.get_user_last_activity(message.peer_id),
                                          recommendation=[])
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
            elif user_status == "ban":
                await state_dispenser.set(message.peer_id, States.SPAM)
                return MiddlewareResponse(False)
            else:
                return MiddlewareResponse(False)
        elif message.state_peer.state == States.SPAM:
            return False
        elif message.state_peer.state == States.TRAINING or message.state_peer.state == States.DIED:
            return True
        if (time() - message.state_peer.payload["last_activity"]) // 60 > 5:
            rec = await calculate_indicators(message.peer_id, message.state_peer.payload["last_activity"])
            if rec is False:
                await state_dispenser.set(message.peer_id, States.DIED)
                message.state_peer = await state_dispenser.get(message.peer_id)
                await db.update_status(message.peer_id, "died")
                return True
            else:
                await state_dispenser.set(message.peer_id, States.ACTIVE,
                                          last_activity=time(), recommendation=rec)
            message.state_peer = await state_dispenser.get(message.peer_id)


class EventSpamMiddleware(BaseMiddleware):
    async def pre(self, event: GroupTypes.MessageEvent):
        state_peer = await state_dispenser.get(event.object.peer_id)
        if state_peer is None:
            user_status = await db.get_user_status(peer_id=event.object.peer_id)
            if user_status == "active":
                await state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                          last_activity=await db.get_user_last_activity(event.object.peer_id),
                                          recommendation=[])
                state_peer = await state_dispenser.get(event.object.peer_id)
            elif user_status == "training":
                await state_dispenser.set(event.object.peer_id, States.TRAINING, position=0)
                return
            elif user_status == "died":
                await state_dispenser.set(event.object.peer_id, States.DIED)
                return
            elif user_status is None:
                await db.add_user(
                    peer_id=event.object.peer_id,
                    username="Прометей"
                )
                await state_dispenser.set(event.object.peer_id, States.TRAINING, position=0)
                return
            elif user_status == "ban":
                await state_dispenser.set(event.object.peer_id, States.SPAM)
                return MiddlewareResponse(False)
            else:
                return MiddlewareResponse(False)
        elif state_peer.state == States.SPAM:
            return False
        elif state_peer.state == States.TRAINING or state_peer.state == States.DIED:
            return True
        if state_peer.state == States.ACTIVE:
            if (time() - state_peer.payload["last_activity"]) // 60 > 5:
                rec = await calculate_indicators(event.object.peer_id, state_peer.payload["last_activity"])
                if rec is False:
                    await state_dispenser.set(event.object.peer_id, States.DIED)
                    await db.update_status(event.object.peer_id, "died")
                else:
                    await state_dispenser.set(event.object.peer_id, States.ACTIVE,
                                              last_activity=time(), recommendation=rec)
