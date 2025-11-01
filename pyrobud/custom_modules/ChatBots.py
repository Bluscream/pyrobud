import asyncio
from random import choice, randrange
from pyrobud import command, module, util
from re import match, compile
from urllib.parse import urlparse

from pyrobud.util.bluscream import has_affecting_media, get_id

from ..custom_classes.ChatBot import *
from ..custom_classes.ChatBots import ChatIncognitoBot, BetaIncognitoBot, ChattismoBot, RandomChatssBot, AnonimeChatBot

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from pyrobud.core.bot import Bot
    from pyrobud import core
    # from pyrobud.custom_modules.ChatIncognitoBotClasses import *
# else:


class ChatBots(module.Module):
    bot: "Bot"
    db: util.db.AsyncDB
    
    disabled = False
    name = "ChatBots"
    bots: list[ChatBot] = list()

    async def on_load(self) -> None:
        self.db = self.bot.get_db(self.name)
        self.bots.append(ChatIncognitoBot.Bot(self))
        self.bots.append(BetaIncognitoBot.Bot(self))
        self.bots.append(ChattismoBot.Bot(self))
        self.bots.append(RandomChatssBot.Bot(self))
        self.bots.append(AnonimeChatBot.Bot(self))
        print(f"Loaded {len(self.bots)} chatbots ({','.join([b.name for b in self.bots])})")
        for bot in self.bots:
            print(bot)

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        if self.disabled: return
        chat_id = get_id(event.message.peer_id)
        # from_id = get_id(event.message.from_id) or event.message.sender_id
        to_id = get_id(event.message.to_id)
        # print("New message in", chat_id, "from", from_id, "to", to_id,":",event.message.text)
        for bot in self.bots:
            # print(f"bot: {bot.id} chat: {chat_id} from: {from_id} to: {to_id}")
            if chat_id != bot.id: continue
            if to_id == bot.id: await bot.on_message_to_bot(event.message)
            else: await bot.on_message_from_bot(event.message)

    async def on_message_edit(self, event: tg.events.MessageEdited.Event):
        if self.disabled: return
        chat_id = get_id(event.message.peer_id)
        from_id = get_id(event.message.from_id) or event.message.sender_id
        for bot in self.bots:
            if chat_id == bot.id:
                if from_id == self.bot.uid: await bot.on_self_message_edited(event.message)
                else: await bot.on_message_edited(event.message)

    @command.desc("List all sessions")
    @command.alias("chatbotsessions", "csessions")
    async def cmd_cs(self, ctx: command.Context) -> str:
        txt = "Sessions:"
        cnt = 0
        for bot in self.bots:
            txt += f"\n#{bot.name}"
            for session in bot.sessions:
                cnt+=1
                txt += f"\n``` {session} ```\n"
        return f"{cnt} {txt}"

        # elif chat_id in UIDS.keys():
        #     from_id = get_id(event.message.from_id) or chat_id
        #     bot = UIDS[chat_id]
        #     await self.logSessions()
        #     if from_id == self.bot.uid: # self -> bot
        #         sd
        #     elif from_id in UIDS.keys(): # bot -> self
        #         await self.printLog(f"=== NEW MESSAGE from {bot} ===")
        #         await self.printLog(f"```\n{event}\n```")
        #         # await self.log("check_for_media:", self.check_for_media, "has_affecting_media:", has_affecting_media(msg), "startswith(Emojis.Other.AuthorMessage):", event.message.text.startswith(Emojis.Other.AuthorMessage))
        #         if self.check_for_media and has_affecting_media(event.message) and not event.message.text.startswith(Emojis.Other.AuthorMessage): # Media
        #             _now = datetime.now()
        #             if self.last_deleted_media < _now - timedelta(minutes=10):
        #                 await event.message.reply("`Media deleted. Please don't send media directly here.`")
        #                 self.last_deleted_media = _now
        #             await event.message.delete()
        #         # await self.log("partnermsg_pattern", self.partnermsg_pattern)
        #         r_match = self.partnermsg_pattern.match(event.message.text)
        #         await self.printLog("r_match", r_match)
        #         if r_match: # Partner Message
        #             await self.printLog("got partner message (session active:", self.sessionActive, ")") # , ", greeted:", self.activeSession.greeted)
        #             if not self.sessionActive: await self.newSession()
        #             if not self.activeSession.greeted: await self.greet(event.message, self.activeSession)
        #             # self.activeSession.state = SessionState.Active
        #             self.session_state = SessionState.Active
        #             self.activeSession.setGender(r_match.group(1))
        #             self.activeSession.messages.append(event.message.id)
        #         else: # Bot Message
        #             await self.printLog("got bot message", Emojis.Session.start, Emojis.Session.end, Emojis.Session.searching)
        #             if Emojis.Session.end in event.message.text:
        #                 await self.printLog("Emojis.Session.end in event.message.text")
        #                 if self.sessionActive:
        #                     for entity in event.message.entities:
        #                         if hasattr(entity, "url"): self.activeSession.reopen_url = urlparse(entity.url)
        #                     self.activeSession.close()
        #                     await self.bot.client.send_message(self.log_channel, self.sessions[-1].print())
        #                 self.session_state = SessionState.Ended # Todo: Set searching if used next!
        #                 #  await self.replyAndDelete(msg, Commands.new_chat, delete_after_s=10)
        #                 if Emojis.Session.searching not in event.message.text: await event.message.reply(Commands.new_chat)
        #                 await self.printLog("session stopped!")
        #             """
        #             for char in list(event.message.text): # todo: remove debug shit
        #                 await self.log(char, "==", Emojis.Session.start, ":", char == Emojis.Session.start, char.encode('ascii', 'backslashreplace'))
        #             """
        #             await self.printLog(event.message.text)
        #             await self.printLog("Emojis.Session.start in event.message.text ==", Emojis.Session.start in event.message.text)

        #             if Emojis.Session.start in event.message.text:
        #                 await self.printLog("Emojis.Session.start in event.message.text")
        #                 await self.newSession(event.message)
        #                 if not self.activeSession.greeted and choice(True, False): await self.greet(event.message, self.activeSession)
        #                 await self.printLog("new session!")
        #             if Emojis.Session.searching in event.message.text:
        #                 await self.printLog("Emojis.Session.searching in event.message.text")
        #                 if self.sessionActive: self.activeSession.close()
        #                 self.session_state = SessionState.Searching
        #                 await self.printLog("searching!")