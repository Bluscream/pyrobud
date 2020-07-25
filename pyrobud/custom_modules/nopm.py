from .. import command, module, util
import telethon as tg
from typing import ClassVar, Optional, List, Set
from telethon.tl.functions import *
from telethon.tl.types import *
from asyncio import sleep

class NoPMModule(module.Module):
    name: ClassVar[str] = "No PM"
    db: util.db.AsyncDB

    async def updateWhitelist(self):
        if hasattr(self, "whitelist"): return
        await sleep(2)
        dl: List[int] = list()
        async for d in self.bot.client.iter_dialogs():
            if d.id != 0: dl.append(d.id)
        self.whitelist = dl
        print(f"Updated whitelist ({len(self.whitelist)})")

    async def on_load(self) -> None:
        print("on_load")
        self.db: util.db.AsyncDB = self.bot.get_db("nopm")

    async def on_start(self) -> None:
        print("on_start")
        await self.updateWhitelist()

    async def on_raw_event(self, event: MessageService):
        if not hasattr(event, "message"): return
        if not hasattr(event.message, "action"): return
        if not isinstance(event.message.action, MessageActionPhoneCall): return

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        await self.updateWhitelist()
        if not hasattr(self, "whitelist"): return
        event.message: tg.custom.Message
        if not event.is_private: return
        if event.chat_id in self.whitelist:
            print(f"{str(event.chat_id)} in {str(self.whitelist)}")
        who = await event.get_input_chat()
        print(str(who))
        response: messages.Chats = await self.bot.client(tg.functions.messages.GetCommonChatsRequest(who, 0, 100))
        # print(response.stringify())
        _chats: list = await self.db.get("chats")
        chats = list()
        for chat in response.chats:
            if chat.id in _chats: chats.append(chat)
        if len(chats) < 1: return
        msg = "Forbidden chats:\n"
        for chat in chats:
            msg += "\n" + util.bluscream.ChatStr(chat)
        await event.message.reply(msg)
        return
        await self.bot.client(messages.ReportSpamRequest(who))
        await self.bot.client(contacts.BlockRequest(who))
        await self.bot.client(messages.DeleteHistoryRequest(who, 0))


    @command.desc("")
    @command.alias("toggledm", "nopm", "nodm")
    async def cmd_togglepm(self, ctx: command.Context):
        chats: list = await self.db.get("chats")
        txt = ""
        if ctx.input == "list":
            txt = f"PMs not allowed in:\n"
            for chat in chats:
                try:
                    chat = await self.bot.client.get_entity(int(chat))
                    txt += f"\n{util.bluscream.ChatStr(chat)}"
                except: txt += f"\n`{chat}`"
        elif ctx.input == "clear":
            await self.db.put("chats", list())
            txt = "Cleared NoPM list!"
        else:
            if (ctx.msg.chat_id in chats):
                chats.remove(ctx.msg.chat_id)
                txt = f"Private messages are now allowed in {util.bluscream.ChatStr(ctx.msg.chat)}!"
            else:
                chats.append(ctx.msg.chat_id)
                txt = f"Private messages no longer allowed in {util.bluscream.ChatStr(ctx.msg.chat)}!"
            await self.db.put("chats", chats)
        await ctx.respond(txt)


"""

whitelist = {d.id for d in client.get_dialogs() if d.id > 0}

@client.on(events.NewMessage)
async def handler(event):
    if not event.is_private or event.chat_id in whitelist:
      return
    who = await event.get_input_chat()
    await client(f.messages.ReportSpamRequest(who))
    await client(f.contacts.BlockRequest(who))
    await client(f.messages.DeleteHistoryRequest(who, 0))
#block #PM #report

"""