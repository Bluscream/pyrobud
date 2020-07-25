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

    async def on_load(self) -> None:
        self.db: util.db.AsyncDB = self.bot.get_db("nopm")

    async def on_raw_event(self, event: MessageService):
        if not hasattr(event, "message"): return
        if not hasattr(event.message, "action"): return
        if not isinstance(event.message.action, tg.tl.types.MessageActionPhoneCall): return

    @command.desc("")
    @command.alias("toggledm", "nopm", "nodm")
    async def cmd_togglepm(self, ctx: command.Context, arg: str = ""):
        chats: list = await self.db.get("chats")
        txt = ""
        if arg == "list":
            txt = f"PMs not allowed in:\n"
            for chat in chats:
                try:
                    chat = await self.bot.client.get_entity(int(chat))
                    txt += f"\n{util.bluscream.ChatStr(chat)}"
                except: txt += f"\n`{chat}`"
        elif arg == "clear": await self.db.put("chats", list())
        else:
            if (ctx.msg.chat_id in chats):
                chats.remove(ctx.msg.chat_id)
                txt = f"Private messages are now allowed in {util.bluscream.ChatStr(ctx.msg.chat)}!"
            else:
                chats.append(ctx.msg.chat_id)
                txt = f"Private messages no longer allowed in {util.bluscream.ChatStr(ctx.msg.chat)}!"
            await self.db.put("chats", chats)
        await ctx.respond(txt)