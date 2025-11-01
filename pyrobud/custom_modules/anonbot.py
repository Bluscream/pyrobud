import asyncio
import io
from pathlib import PurePosixPath
from typing import IO

import telethon as tg

from .. import command, module, util


class ExampleModule(module.Module):
    name = "Anonymous Bot Automation"
    disabled = True
    bot_ids = [
        6007681571, # betaincognitobot
        339959826   # ChatIncognitoBot
    ]

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        self.db = self.bot.get_db("anonbot")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if hasattr(event, "chat") and event.chat_id not in self.bot_ids: return

        self.log.info(f"{event.chat.username}: {event.message}")