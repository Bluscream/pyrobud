import asyncio
import re
from datetime import timedelta, datetime, timezone
from telethon.tl.types import PeerUser, PeerChannel
from .. import command, module, util
import telethon as tg
from telethon.tl.patched import MessageService

class CallUtilsModule(module.Module):
    name = "CallUtils"
    disabled = True

    async def on_ready(self):
        pass

    async def on_raw_event(self, event: MessageService):
        if not hasattr(event, "message"): return
        if not hasattr(event.message, "action"): return
        if not isinstance(event.message.action, tg.tl.types.MessageActionPhoneCall): return
        await self.bot.client.send_message(event.message.to_id, await self.get_total_duration(event.message.to_id))

    @command.alias("lcd")
    async def cmd_last_call_duration(self, msg: tg.custom.Message):
        calls = await self.get_calls_for(msg.to_id)
        if len(calls) < 1: return "No calls yet"
        call = next( (x for x in calls if hasattr(x.action, "duration") and x.action.duration is not None), None)
        return f"Last call was `{timedelta(seconds=call.action.duration)}` long."

    @command.alias("tcd")
    async def cmd_total_call_duration(self, msg: tg.custom.Message):
        return await self.get_total_duration(msg.to_id)

    @command.alias("tvd")
    async def cmd_total_voice_duration(self, _msg: tg.custom.Message):
        msg: tg.custom.Message
        count = 0
        duration = 0
        async for msg in self.bot.client.iter_messages(await _msg.get_input_chat(), filter=tg.types.InputMessagesFilterVoice):
            if msg.voice:
                count += 1
                duration += msg.media.document.attributes[0].duration
        duration = timedelta(seconds=duration)
        return f"`{count}` voice messages with a total duration of `{duration}`"

    async def get_calls_for(self, target_id = "0"):
        calls = []
        msg: tg.custom.Message
        async for msg in self.bot.client.iter_messages(tg.types.InputPeerEmpty(), filter=tg.types.InputMessagesFilterPhoneCalls):
            if msg.from_id == target_id or msg.to_id == target_id: calls.append(msg)
        return calls

    async def get_total_duration(self, target_id):
        msg: tg.custom.Message
        count = 0
        duration = 0
        calls = await self.get_calls_for(target_id)
        for msg in calls:
        # async for msg in self.bot.client.iter_messages(tg.types.InputPeerEmpty(), filter=tg.types.InputMessagesFilterPhoneCalls):
            # if msg.from_id == target_id or msg.to_id == target_id:
                # action: tg.tl.types.MessageActionPhoneCall = msg.action
                if msg.action.duration is not None: duration += msg.action.duration
                count += 1
        duration = timedelta(seconds=duration)
        return f"`{count}` calls with a total duration of `{duration}`"