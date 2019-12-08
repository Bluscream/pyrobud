from re import compile, MULTILINE

import telethon as tg

from pyrobud.util.bluscream import UserStr
from .. import command, module


class DebugModuleAddon(module.Module):
    name = "Debug Extensions"

    uid_regex = compile(r"(?<!\d)\d{9}(?!\d)")

    @command.desc("Dump all the data of a message to your cloud")
    @command.alias("mdp")
    async def cmd_mdumpprivate(self, msg: tg.custom.Message):
        if not msg.is_reply: return
        reply_msg = await msg.get_reply_message()
        await msg.delete()
        data = f"```{reply_msg.stringify()}```"
        await self.bot.client.send_message("me", data)

    @command.desc("Convert all tg uids to profile links")
    @command.alias("idlink", "linkids", "linkid")
    async def cmd_idlinks(self, msg: tg.custom.Message):
        if not msg.is_reply: return
        reply_msg = await msg.get_reply_message()
        matches = self.uid_regex.finditer(reply_msg.text, MULTILINE)
        uids = list()
        for matchNum, match in enumerate(matches, start=1):
            if not match.group() in uids:
                uids.append(match.group())
        if len(uids) < 1: return "No UIDs found in the given message."
        ret = f"Found **{len(uids)}** UIDs:\n"
        for uid in uids:
            try:
                user = await self.bot.client.get_entity(int(uid))
                ret += f"\n - {UserStr(user, True)}"
            except: ret += f"\n - [{uid}](tg://user?id={uid})"""
        return ret