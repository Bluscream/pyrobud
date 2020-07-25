from datetime import timedelta
from telethon.tl.types import PeerUser
from .. import command, module
import telethon as tg
from telethon.tl.patched import MessageService

class CallUtilsModule(module.Module):
    name = "CallUtils"

    async def on_ready(self):
        pass

    async def on_raw_event(self, event: MessageService):
        if not hasattr(event, "message"): return
        if not hasattr(event.message, "action"): return
        if not isinstance(event.message.action, tg.tl.types.MessageActionPhoneCall): return
        await self.bot.client.send_message(event.message.to_id, await self.get_total_duration(event.message.to_id))

    @command.alias("lcd")
    async def cmd_last_call_duration(self, ctx: command.Context):
        calls = await self.get_calls_for(ctx.msg.to_id)
        if len(calls) < 1: return "No calls yet"
        call = next( (x for x in calls if hasattr(x.action, "duration") and x.action.duration is not None), None)
        return f"Last call was `{timedelta(seconds=call.action.duration)}` long."

    @command.alias("tcd")
    async def cmd_total_call_duration(self, ctx: command.Context):
        return await self.get_total_duration(ctx.msg.to_id)

    @command.alias("tvd")
    async def cmd_total_voice_duration(self, _ctx: command.Context):
        ctx: command.Context
        count = 0
        duration = 0
        async for msg in self.bot.client.iter_messages(await _ctx.msg.get_input_chat(), filter=tg.types.InputMessagesFilterVoice):
            if ctx.msg.voice:
                count += 1
                duration += ctx.msg.media.document.attributes[0].duration
        duration = timedelta(seconds=duration)
        return f"`{count}` voice messages with a total duration of `{duration}`"

    async def get_calls_for(self, target_id = "0"):
        calls = []
        ctx: command.Context
        async for msg in self.bot.client.iter_messages(tg.types.InputPeerEmpty(), filter=tg.types.InputMessagesFilterPhoneCalls):
            if ctx.msg.from_id == target_id or ctx.msg.to_id == target_id: calls.append(msg)
        return calls

    async def get_total_duration(self, target_id):
        ctx: command.Context
        count = 0
        duration = 0
        calls = await self.get_calls_for(target_id)
        for msg in calls:
        # async for msg in self.bot.client.iter_messages(tg.types.InputPeerEmpty(), filter=tg.types.InputMessagesFilterPhoneCalls):
            # if ctx.msg.from_id == target_id or ctx.msg.to_id == target_id:
                # action: tg.tl.types.MessageActionPhoneCall = ctx.msg.action
                if ctx.msg.action.duration is not None: duration += ctx.msg.action.duration
                count += 1
        duration = timedelta(seconds=duration)
        return f"`{count}` calls with a total duration of `{duration}`"