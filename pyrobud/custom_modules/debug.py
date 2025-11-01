from re import MULTILINE, finditer

import telethon as tg

from pyrobud.util.bluscream import UserStr, telegram_uid_regex, linkify_fullname
from .. import command, module

from typing import TYPE_CHECKING
if TYPE_CHECKING: from ..custom_classes.DataCenter import DataCenter


class DebugModuleAddon(module.Module):
    name = "Debug Extensions"
    disabled = False

    @command.desc("Prints info about a certain user")
    @command.alias("uinfo")
    async def cmd_userinfo(self, ctx: command.Context) -> str:
        text = ctx.input
        user: tg.types.User = None
        if text: user = await self.bot.client.get_entity(int(text)) 
        elif ctx.msg.is_reply: user = (await ctx.msg.get_reply_message()).get_sender()
        if not user: return "Could not find user anywhere!"
        dc: DataCenter = self.bot.dc.dcs[user.photo.dc_id]
        reply = f'**Display Name: ** `{user.first_name} {user.last_name}`\n' \
            f'**Username:** `@{user.username}`\n' \
            f'**User ID:** `{user.id}`\n' \
            f'**Status:** `{user.status.stringify()}`\n' \
            f'**Datacenter:** `{dc.geo.city}, {dc.geo.country} ({dc.id})`\n' \
            f'**Region:** `{dc.geo.continent}`\n'
        return reply

    @command.desc("Prints info about data centers")
    @command.alias("dcs")
    async def cmd_datacenters(self, ctx: command.Context) -> str:
        reply = ["**Telegram Data Centers:**"]
        dc: DataCenter
        for dc in self.bot.dc.dcs.values():
            reply.append(f'DC{dc.id} {dc.geo.continent if dc.geo else ""}: {dc.ping or -1}ms')
        return '\n'.join(reply)

    @command.desc("Dump all the data of a message to your cloud")
    @command.alias("mdp")
    async def cmd_mdumpprivate(self, ctx: command.Context) -> str:
        if not ctx.msg.is_reply: return
        reply_msg = await ctx.msg.get_reply_message()
        await ctx.msg.delete()
        data = f"```{reply_msg.stringify()}```"
        await self.bot.client.send_message("me", data)

    @command.desc("Convert all tg uids to profile links")
    @command.alias("idlink", "linkids", "linkid")
    async def cmd_idlinks(self, ctx: command.Context) -> str:
        text = ctx.input
        if not text and ctx.msg.is_reply: text = (await ctx.msg.get_reply_message()).text
        matches = finditer(telegram_uid_regex, text, MULTILINE)
        uids = set()
        for _, match in enumerate(matches, start=1):
            uids.add(match.group())

        if len(uids) < 1: return "No UIDs found in the given message."
        ret = f"Found **{len(uids)}** UIDs:\n"
        for uid in uids:
            try:
                user = await self.bot.client.get_entity(int(uid))
                ret += f"\n - {UserStr(user, True)}"
            except: ret += f"\n - [{uid}](tg://user?id={uid})"
        return ret

    @command.desc("Returns the profile link for a user id")
    async def cmd_link(self, ctx: command.Context) -> str:
        uid = ctx.input
        # try:
        user = await self.bot.client.get_entity(int(uid))
        fullname = ""
        if user.first_name: fullname += user.first_name
        if user.last_name: fullname += f" {user.last_name}"
        
        self.bot.client.send_message(ctx.msg.chat_id, message=f"[{fullname if fullname else user.id}](tg://user?id={user.id})") # , parse_mode=tg.client.messageparse.MessageParseMethods.parse_mode)
        # except: return f"[{uid}](tg://user?id={uid})"