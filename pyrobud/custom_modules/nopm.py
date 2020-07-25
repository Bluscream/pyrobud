import asyncio
import re
from datetime import timedelta, datetime, timezone
from telethon.tl.types import PeerUser, PeerChannel
from .. import command, module, util
import telethon as tg
from telethon.tl.patched import MessageService
from typing import ClassVar, Optional

class NoPMModule(module.Module):
    name: ClassVar[str] = "No PM"
    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db("nopm")

    async def on_raw_event(self, event: MessageService):
        if not hasattr(event, "message"): return
        if not hasattr(event.message, "action"): return
        if not isinstance(event.message.action, tg.tl.types.MessageActionPhoneCall): return
        await self.bot.client.send_message(event.message.to_id, await self.get_total_duration(event.message.to_id))

    @command.desc("")
    @command.alias("toggledm", "nopm", "nodm")
    async def cmd_togglepm(self, ctx: command.Context):
        calls = await self.get_calls_for(ctx.msg.to_id)
        if len(calls) < 1: return "No calls yet"
        call = next( (x for x in calls if hasattr(x.action, "duration") and x.action.duration is not None), None)
        return f"Last call was `{timedelta(seconds=call.action.duration)}` long."