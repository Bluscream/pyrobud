from datetime import timedelta, datetime
import telethon as tg
from telethon.tl.types import ChannelParticipantsAdmins
from .. import command, module, util

class LoggerModule(module.Module):
    name = "Logger"
    enabled = True

    async def on_load(self):
        pass

    def is_enabled(self, event):
        return True

    async def on_chat_action(self, action: tg.events.chataction.ChatAction.Event):
        if not self.enabled: return
        txt = f"```\n{action.stringify().strip()}\n```"
        await self.bot.client.send_message("RawLog", txt)
        if hasattr(action, "user_id") and action.user_id is not None and action.user_id != self.bot.uid: return
        notify = True
        if action.user_joined or action.user_left:
            _action = "⤵ Joined" if action.user_joined else "🔙 Left"
            date = action.action_message.date if (hasattr(action, "action_message") and action.action_message is not None) else datetime.now()
            txt = f"{date}\n{_action} {util.bluscream.ChatStr(action.chat)}"
            if action.is_group and action.user_joined:
                admins = await self.bot.client.get_participants(action.chat, filter=ChannelParticipantsAdmins)
                _admins = len(admins)
                if _admins > 0:
                    txt += f"\n\n**Admins ({_admins}):**"
                    for admin in admins: txt += f"\n{util.bluscream.UserStr(admin, True)}"
                notify = False
        await self.bot.client.send_message("JoinLog", txt.strip(),
                                           schedule=timedelta(seconds=10) if notify else None)

    @command.desc("Toggle selflog")
    async def cmd_selflog(self, msg):
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        return f"Selflog is now **{status}**."
