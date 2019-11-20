    @command.desc("Ban users from all chats where you have permissions to do so")
    @command.alias("gban")
    async def cmd_globalban(self, msg: tg.events.newmessage, *users: tuple):
        users = list(map(int, users))
        if msg.is_reply:
            replied_msg = await msg.get_reply_message()
            users.append(replied_msg.from_id)
        users = list(set(users))
        chatcount = 0;
        users_to_ban = []
        for userid in users:
            user = await self.bot.client.get_entity(userid)
            users_to_ban.append(user)
        async for dialog in self.bot.client.iter_dialogs():
            if not dialog.is_group or not dialog.is_channel: continue
            chat = await self.bot.client.get_entity(dialog.id)
            async for user in self.bot.client.iter_participants(chat, filter=tg.tl.types.ChannelParticipantsAdmins):
                if user.id == self.bot.uid:
                    await self.banUsers(users_to_ban, chat)
                    chatcount += 1
                    break
        return f"{len(users_to_ban)} users have been banned from {chatcount} chats!"