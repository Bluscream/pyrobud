import re

import telethon as tg

from .. import module

class RexyModule(module.Module):
    name = "Rexy"
    disabled = False

    search = r'(\W|^)mau+(\W|$)'
    replace = r'\1rawr\2'
    id = 6464525758

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:

        if event.chat_id != self.id: return

        if event.message.sender_id == self.id: return
        

        text = event.message.text        
        if not text or not re.search(self.search, text, flags = re.IGNORECASE | re.MULTILINE): return

        new_text = re.sub(self.search, self.replace, text, flags=re.IGNORECASE | re.MULTILINE)

        await event.message.edit(text=new_text)