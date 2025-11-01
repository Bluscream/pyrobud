from typing import Union, List

import telethon as tg
from .. import command, module, util
from re import compile, MULTILINE, IGNORECASE
from json import dumps
from telethon.tl.functions.messages import GetCommonChatsRequest

try:
    from BeautifulSoup import BeautifulSoup, element
except ImportError:
    from bs4 import BeautifulSoup, element

class TopListModule(module.Module):
    name = "Top Lists"
    disabled = True
    # no_mention_pattern = compile(r'<template type="([\w_]+)" value_type="([\w_]+)">([\w\s_]+)</template>')
    # user_pattern = compile(r'<user id="(\d+)" first_name="\w+" last_name="\w+" user_name="\w+"/>')
    last_edited = 0

    async def parse_message(self, msg: tg.custom.Message):
        txt = msg.raw_text
        html = BeautifulSoup(txt, features="html.parser")
        user: element.Tag
        changes = 0
        for user in html.find_all("user"):
            changes += 1
            user.replace_with(util.bluscream.ParseUserStr(
                id=int(user.attrs["id"]) if user.has_attr("id") else None,
                first_name=user.attrs["first_name"] if user.has_attr("first_name") else None,
                last_name=user.attrs["last_name"] if user.has_attr("last_name") else None,
                user_name=user.attrs["user_name"] if user.has_attr("user_name") else None))
        if changes > 0 and self.last_edited != msg.id:
            self.last_edited = msg.id
            await msg.edit(html.text)
        """
        matches = self.no_mention_pattern.finditer(msg.text, MULTILINE | IGNORECASE)
        new_txt: str = msg.text
        for match in matches:
            repl = ""
            if match.group(1) == "no_mention":
                if match.group(2) == "userid":
                    repl = match.group(3)
            new_txt = new_txt.replace(match.group(0))
        """

    async def on_message(self, msg: tg.custom.Message):
        if msg.from_id != self.bot.uid: return
        print("on_msg")
        await self.parse_message(msg)

    async def on_message_edit(self, event: tg.events.MessageEdited.Event):
        if event.message.from_id != self.bot.uid: return
        print("on_msg_edit")
        await self.parse_message(event.message)

    @command.alias("top")
    async def cmd_toplist(self, msg: tg.custom.Message, count: int = 5):
        count = int(count) if count else 5
        chat: Union[tg.types.Chat, tg.types.Channel] = await msg.get_chat()
        members: List[tg.types.User] = list()
        member: tg.types.User
        async for member in  self.bot.client.iter_participants(chat):
            if member.is_self: continue
            chats = await self.bot.client(GetCommonChatsRequest(member, 0, 100))
            member.common_chats = len(chats.chats)
            if member.common_chats < 1: continue
            members.append(member)
        members.sort(key=lambda member: member.common_chats, reverse=True)
        if len(members) > count: members = members[:count]
        txt = f"**Top {len(members)} of {chat.title}:**\n"
        for member in members:
            txt += f"\n - `{member.common_chats}`: {util.bluscream.UserStr(member)}" + u'\u202C'
        return txt # "\n- ".join([f"`{member.common_chats}`: {util.bluscream.UserStr(member)}" for member in members])
        await msg.delete()
        await msg.respond(txt)