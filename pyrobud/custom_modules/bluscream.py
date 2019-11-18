import asyncio
from datetime import datetime, timedelta
from random import choice

import telethon as tg

from pyrobud import module


class Bluscream(module.Module):
    name = "Bluscream"

    async def on_message(self, msg: tg.custom.Message):
        if msg.chat_id is not None and msg.chat_id == self.bot.uid:
            await msg.forward_to(-280032537)

    async def on_message_edit(self, event: tg.events.MessageEdited.Event):
        pass

    async def cmd_bluscream(self, msg):
        return "lol"
