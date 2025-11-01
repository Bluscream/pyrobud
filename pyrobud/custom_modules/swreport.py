"""
Pyrobud module to report a message to spamwat.ch
Author : Ojas Sinha<sinhaojas67@gmail.com>
"""

import asyncio

from pyrobud import command, module, util
from telethon import functions, types
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import telethon as tg

class SpamWatchReport(module.Module):
    name: str = "spamwat.ch reporter"
    disabled: bool = False

    async def append(self, ctx, lines, txt):
        lines += txt
        await ctx.respond('\n'.join(lines))

    @command.desc("Reports replied message to https://t.me/SpamWatchSupport")
    @command.alias("sw","spam")
    @command.usage("[reply to a spam message]", reply=True)
    async def cmd_spamr(self, ctx: command.Context):
        group: str = "-1001275988180" # "t.me/SpamWatchSupport"
        if (not ctx.msg.is_reply and not ctx.msg.file):
            return "__Reply to a message to report!__"

        spam = ctx.msg if ctx.msg.file else await ctx.msg.get_reply_message()
        client: tg.TelegramClient = self.bot.client
        lines = []
        sender = await spam.forward.get_sender() or await spam.get_sender()

        await self.append(ctx, lines, "__Reporting message to Telegram for spam__")

        try:
            result = client(functions.messages.ReportRequest(
                peer=sender.username,
                id=[spam.id],
                option=b'Spam',
                message=spam.text
            ))
            if not result: raise Exception("ReportRequest returned False")
            await self.append(ctx, lines, result.stringify())
        except Exception as ex:
            await self.append(ctx, lines, f"Failed to report to Telegram: {ex.Message}")

        await self.append(ctx, lines, "__Reporting message to SpamWatch__")

        if sender: lines.append(f"Message author ID: `{sender.id}`")

        if spam.forward and spam.forward.from_id: lines.append(f"Forwarded message author ID: `{spam.forward.from_id}`")

        msg_data = "\n".join(lines)
        
        await self.bot.client.forward_messages(entity=group, messages=spam, silent=True)
        await self.bot.client.send_message(group, msg_data)

        await self.append(ctx, lines, "__Reported to SpamWatch__")
