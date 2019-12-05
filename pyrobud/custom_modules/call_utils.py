import asyncio
import re
from datetime import timedelta, datetime, timezone
from telethon.tl.types import PeerUser, PeerChannel
from .. import command, module, util
import telethon as tg
from telethon.tl.patched import MessageService

class CallUtilsModule(module.Module):
    name = "CallUtils"

    async def on_ready(self):
        pass

    async def on_raw_event(self, event: MessageService):
        # print("test 1", event)
        if not hasattr(event, "message"): return
        if not hasattr(event.message, "action"): return
        if not isinstance(event.message.action, tg.tl.types.MessageActionPhoneCall): return
        await self.bot.client.send_message(event.message.to_id, await self.get_total_duration(event.message.to_id))

    async def get_total_duration(self, target_id):
        msg: tg.custom.Message
        count = 0
        duration = 0
        async for msg in self.bot.client.iter_messages(tg.types.InputPeerEmpty(), filter=tg.types.InputMessagesFilterPhoneCalls):
            if msg.from_id == target_id or msg.to_id == target_id:
                # action: tg.tl.types.MessageActionPhoneCall = msg.action
                if msg.action.duration is not None: duration += msg.action.duration
                count += 1
        duration = timedelta(seconds=duration)
        return f"`{count}` calls with a total duration of `{duration}`"


    async def cmd_calls(self, msg: tg.custom.Message, target_id = 0):
        if msg.is_reply and target_id < 1:
            reply_msg = await msg.get_reply_message()
            user = await reply_msg.get_sender()
            target_id = user.id
        calls = []
        msg: tg.custom.Message
        async for msg in self.bot.client.iter_messages(tg.types.InputPeerEmpty(), filter=tg.types.InputMessagesFilterPhoneCalls):
            if target_id < 1 or (msg.from_id == target_id or msg.to_id == target_id):
                calls.append(msg)
        return calls