import asyncio
import io
from pathlib import PurePosixPath
from typing import IO

import telethon as tg

from .. import command, module, util
from pyrobud.util.bluscream import get_entity, UserStr

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from pyrobud.core.bot import Bot
    from pyrobud import core


class PruneModule(module.Module):
    name = "Prune"
    disabled = False
    bot: "Bot"
    db: util.db.AsyncDB

    async def get_delay(self):
        return await self.db.get("delay") or 2

    async def on_load(self) -> None:
        self.db = self.bot.get_db("prune")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        # chat = await event.message.get_chat()
        user = event.message.sender_id
        dbstr = f'autoprune_{event.message.chat_id}'
        current_users = await self.db.get(dbstr) or []
        if user and user > 0 and user in current_users:
            await asyncio.sleep(await self.get_delay())
            await event.message.delete()

    @command.desc("Sets delay to use between prune operations")
    @command.usage("[seconds]", optional=False)
    async def cmd_prunedelay(self, ctx: command.Context) -> str:
        old_delay = await self.get_delay()
        new_delay = float(ctx.input)
        await self.db.put("delay", new_delay)
        return f"Changed prune delay from {old_delay}s to {new_delay}s"

    @command.desc("Toggles auto pruning of messages of a specified user in the current chat")
    @command.usage("[user name, id or reply]", optional=True, reply=True)
    @command.alias("aprune")
    async def cmd_autoprune(self, ctx: command.Context) -> str:
        ret = ""
        user = await self.bot.client.get_me()
        if ctx.input:
            user = await get_entity(self.bot, ctx)
            if isinstance(user, str): return user

        user = user.id
        
        dbstr = f'autoprune_{ctx.msg.chat_id}'
        print(dbstr)
        current_users = await self.db.get(dbstr) or []
        print(current_users)

        if not user:
            return f"Failed to find user {user}"

        if user in current_users:
            current_users.remove(user)
            ret = f"Removed User {user} from autoprune list for this channel\n({len(current_users)} remaining)" 
        else: 
            current_users.append(user)
            ret = f"Added User {user} to autoprune list for this channel\n({len(current_users)} remaining)" 
        await self.db.put(dbstr, current_users)
        return ret
    

    @command.desc("Prunes all messages of a specified user in the current chat")
    @command.alias("pruneuser")
    @command.usage("[user name, id or reply]", optional=False, reply=True)
    async def cmd_prune(self, ctx: command.Context) -> str:
        chat = ctx.msg.chat_id
        user = await self.bot.client.get_me()
        if ctx.input:
            user = await get_entity(self.bot, ctx)
            if isinstance(user, str): return user

        counter = 0
        
        
        while True:
            # Get messages from the specified user in batches
            messages = await self.bot.client.get_messages(
                chat,
                from_user=user.id,
                limit=100
            )

            if not messages or len(messages) < 1:
                break

            # Delete messages in this batch
            # for message in messages:
            await self.bot.client.delete_messages(chat, messages)
            counter += len(messages)
            await asyncio.sleep(self.get_delay())  # Avoid flood limits

        return f"Successfully deleted {counter} messages from {UserStr(user)}"