import asyncio
from random import uniform

import telethon as tg

from pyrobud import module


class TextOnlyModule(module.Module):
    name = "Text only"
    chat_id = -1001258434993

    async def on_message(self, msg: tg.custom.Message):
        if msg.chat_id is None or msg.chat_id != self.chat_id: return
        if msg.photo is None or msg.video is None: await msg.delete()

    async def cmd_purge_non_media(self, _msg: tg.custom.Message):
        found_msg_ids = []
        msg: tg.custom.Message
        async for msg in self.bot.client.iter_messages(_msg.chat_id):
            if msg.photo is None and msg.video is None: found_msg_ids.append(msg.id)
        if len(found_msg_ids) < 1: return "Found no messages without media!"
        await self.bot.client.delete_messages(_msg.chat_id, found_msg_ids, revoke=True)
        return f"Purged **{len(found_msg_ids)}** messages without media!"