from datetime import datetime, timezone
from .. import command, module, util
from ..util.bluscream import *
import re, json, http.client
# import telethon as tg


class Bluscream(module.Module):
    name = "Bluscream"
    disabled = False

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db("bluscream")

    # async def on_message(self, msg: tg.custom.Message):
    #     if msg.chat_id is not None and msg.chat_id == self.bot.uid:
    #         await msg.forward_to(-280032537)

    @command.desc("Temporarily approve someone in chat")
    @command.alias("tapprove")
    @command.usage("<timespan> [user or reply]", optional=True, reply=True)
    async def cmd_tempapprove(self, ctx: command.Context) -> str:
        args = split_args(ctx.input)
        timespan = parse_timespan(args[0])
        msg = ctx.msg
        user = None

        if msg.is_reply:
            msg: tg.types.Message = await ctx.msg.get_reply_message()
            user = await msg.get_sender()
            await msg.reply("/approve")
        elif len(args) == 2:
            user = await self.bot.client.get_entity(args[1])
            await self.bot.client.send_message(ctx.msg.chat_id, f"/approve {user.id}")

        await ctx.msg.delete()

        await asyncio.sleep(2)
        timespan_fmt = strfdelta(timespan, "{days}d {hours}h {minutes}m {seconds}s")
        await self.bot.client.send_message(ctx.msg.chat_id, message=f"{UserStr(user)}, you have been temporarily approved for {timespan_fmt}. Use your time wisely ;)")

        await asyncio.sleep(timespan.total_seconds())

        await self.bot.client.send_message(ctx.msg.chat_id, f"/unapprove {user.id}")


    @command.desc("Simple say command")
    @command.usage("[text to say?]", optional=False)
    async def cmd_say(self, ctx: command.Context) -> str:
        chat_id = ctx.msg.chat_id
        text = ctx.msg.text.replace('.say ', '')
        await ctx.msg.delete()
        await self.bot.client.send_message(chat_id, text)

    @command.desc("Send local date and time to chat")
    @command.usage("[text to echo?, or reply]", optional=True, reply=True)
    async def cmd_time(self, ctx: command.Context) -> str:
        local_time = datetime.now()
        formatted_time = local_time.strftime("Local Time:\n`%H:%M %p` (`GMT+1`)\n`%d.%m.%Y`") # todo: unhardcode TZ
        return formatted_time