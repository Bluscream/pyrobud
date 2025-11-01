# from datetime import datetime, timezone
from .. import command, module, util
from ..util.bluscream import *
# import re, json, http.client
import telethon as tg

class UserHistory(module.Module):
    name = "User History"
    disabled = False
    db: util.db.AsyncDB
    bot_id: int = 300860929
    bot_msg_prefix: str = '👤 **History for'
    group_id: int = 2411900682
    last_saved : str = ""

    async def on_load(self) -> None:
        self.db = self.bot.get_db("userhistory")

    async def on_message(self, msg: tg.custom.Message):
        user = await msg.get_sender()
        if user is None: return
        if user.id == self.bot_id and msg.text.startswith(self.bot_msg_prefix):
            if self.last_saved == msg.text: return
            self.last_saved = msg.text or ""
            try: await msg.forward_to(self.group_id)
            except tg.errors.rpcerrorlist.ChatForwardsRestrictedError:
                await self.bot.client.send_message(self.group_id, message=msg.text)
            

    @command.desc("Looks up a user's history via @SongMata")
    @command.alias("h")
    @command.usage("[user or reply]", optional=True, reply=True)
    async def cmd_history(self, ctx: command.Context) -> str:
        args = split_args(ctx.input)
        user = None
        if ctx.msg.is_reply:
            msg: tg.types.Message = await ctx.msg.get_reply_message()
            user = await msg.get_sender()
        elif len(args) == 1:
            user = await self.bot.client.get_entity(args[1])

        await ctx.msg.delete()

        await self.bot.client.send_message(self.bot_id, message=f"{user.id}")