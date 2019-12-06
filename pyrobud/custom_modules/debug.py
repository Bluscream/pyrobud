import telethon as tg
from .. import command, module, util

class DebugModuleAddon(module.Module):
    name = "Debug Extensions"

    @command.desc("Dump all the data of a message to your cloud")
    @command.alias("mdp")
    async def cmd_mdumpprivate(self, msg: tg.custom.Message):
        if not msg.is_reply: pass
        reply_msg = await msg.get_reply_message()
        await msg.delete()
        data = f"```{reply_msg.stringify()}```"
        await self.bot.client.send_message("me", data)