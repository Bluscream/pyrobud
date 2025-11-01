import asyncio
import io
from pathlib import PurePosixPath
from typing import IO

import telethon as tg

from .. import command, module, util
from pyrobud.util.bluscream import has_affecting_media, get_id


class CalModule(module.Module):
    name = "Callxifer"
    disabled = False
    lastmsg = ""

    id_user_cal = 7727407006 # 689222097
    id_group_rce = -1001257455615

    # db: util.db.AsyncDB

    async def on_load(self) -> None: pass
        # self.db = self.bot.get_db("cal")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if self.disabled or not hasattr(self.bot, "uid") or self.bot.uid != 5527614231: return
        chat_id = event.chat_id
        from_id = get_id(event.message.from_id) or event.message.sender_id
        to_id = get_id(event.message.to_id)

        if from_id != self.id_user_cal: return

        text = event.message.text

        if self.lastmsg != event.message.text:

            cmd = text.split(" ")

            match(chat_id):
                case self.id_group_rce:
                    match(text):
                        case "/rankings@ChatFightBot":
                            await event.message.reply("/rankings@ChatFightBot")
                        case "/groupstats@ChatFightBot":
                            await event.message.reply("/groupstats@ChatFightBot")
                    return
        self.lastmsg = text