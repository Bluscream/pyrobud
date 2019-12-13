import asyncio
from random import choice, randrange
from pyrobud import module
from re import match, compile
from urllib.parse import urlparse
from pyrobud.util.bluscream import has_affecting_media

from ..custom_classes.ChatIncognitoBot import *

# from typing import TYPE_CHECKING
# if TYPE_CHECKING: from pyrobud.custom_modules.ChatIncognitoBotClasses import *
# else:


class ChatIncognitoBot(module.Module):
    name = "ChatIncognitoBot"
    # funcs = [str.lower, str.upper]
    prefixes = ["Hallo", "Hi", "Hey", "Was geht", "Yo", "Jo"]
    suffixes = ["", ":3", ":D", "<3", "♥", "👌", "✌", "c:", "?"]
    last_deleted_media = datetime.min
    partnermsg_pattern = compile("([👦🗣👧])\*\*Partner\*\*: (.*)")
    bot_uid = 339959826
    log_channel = "ChatIncognitoBotLog"

    check_for_media = True
    session_state: SessionState = SessionState.Unknown
    sessions: List[Session] = []

    def printSessions(self):
        print(len(self.sessions), "sessions:", self.sessions)
        # for session in self.sessions: session.print()

    @property
    def sessionActive(self) -> bool:
        if len(self.sessions) > 0: return self.sessions[-1].endtime is None
        return False

    @property
    def activeSession(self) -> Session:
        if self.sessionActive: return self.sessions[-1]
        else:
            session = Session()
            self.sessions.append(session)
            self.session_state = SessionState.Unknown
            return session

    async def replyAndDelete(self, original_msg: tg.custom.Message, text: str, delete_after_s=5, respond_only=False, delete_original=False):
        msg = await original_msg.respond(text) if respond_only else await original_msg.reply(text) # self.bot.client.send_message()(
        await asyncio.sleep(delete_after_s)
        await msg.delete()
        if delete_original: await original_msg.delete()

    async def sendAndDelete(self, text: str, delete_after_s=5):
        msg = await self.bot.client.send_message(self.bot_uid, text)
        await asyncio.sleep(delete_after_s)
        await msg.delete()

    def newSession(self, msg: tg.custom.Message = None) -> Session:
        if self.sessionActive: self.activeSession.close()
        session = self.activeSession
        session.state = SessionState.Active
        if msg:
            # line: str
            for line in msg.text.splitlines():
                print("first line char:", line[:1])
                if line.startswith(Emojis.Partner.age):
                    session.partner_age = int(line.split(": ")[1])
                elif line.startswith(Emojis.Partner.distance):
                    session.partner_distance_km = int(line.split(" ")[2])
        return session

    async def greet(self, msg: tg.custom.Message, session: Session):
        if session.greeted: return
        await asyncio.sleep(randrange(1, 3)) # Todo: Sometimes wait for them to write first
        prefix: str = choice(self.prefixes)
        if choice((True, False)): prefix = prefix.lower()
        if session.state is not SessionState.Active: return
        await msg.respond(prefix + " " + choice(self.suffixes))
        session.greeted = True

    async def on_message(self, msg: tg.custom.Message):
        if msg.chat_id != self.bot_uid: return
        print("=== NEW MESSAGE ===")
        self.printSessions()
        if msg.from_id == self.bot.uid: # self -> bot
            lower_txt = msg.text.lower()
            if lower_txt == "/session":
                lines = list()
                lines.append(f"Session State: `{self.session_state}`")
                lines.append(f"Media blacklisted: `{self.check_for_media}`")
                lines.append(f"Last deleted media at: `{self.last_deleted_media}`")
                lines.append(f"Sessions: `{len(self.sessions)}`")
                if self.sessions: lines.append(f"Last Session: `{self.sessions[-1].print()}`")
                if len(lines) > 0: await msg.edit("\n".join(lines))
            elif lower_txt == "/media":
                self.check_for_media = not self.check_for_media
                await self.replyAndDelete(msg, text=f"You are {'no longer allowed to send media ❌' if self.check_for_media else 'allowed to send media now ✔'}", delete_after_s=15, delete_original=True)
        elif msg.from_id == self.bot_uid:
            # print("check_for_media:", self.check_for_media, "has_affecting_media:", has_affecting_media(msg), "startswith(Emojis.Other.AuthorMessage):", msg.text.startswith(Emojis.Other.AuthorMessage))
            if self.check_for_media and has_affecting_media(msg) and not msg.text.startswith(Emojis.Other.AuthorMessage): # Media
                _now = datetime.now()
                if self.last_deleted_media < _now - timedelta(minutes=10):
                    await msg.reply("`Media deleted. Please don't send media directly here.`")
                    self.last_deleted_media = _now
                await msg.delete()
            # print("partnermsg_pattern", self.partnermsg_pattern)
            r_match = self.partnermsg_pattern.match(msg.text)
            print("r_match", r_match)
            if r_match: # Partner Message
                print("got partner message (session active:", self.sessionActive, ")") # , ", greeted:", self.activeSession.greeted)
                if not self.sessionActive: self.newSession()
                if not self.activeSession.greeted: await self.greet(msg, self.activeSession)
                # self.activeSession.state = SessionState.Active
                self.session_state = SessionState.Active
                self.activeSession.setGender(r_match.group(1))
                self.activeSession.messages.append(msg.id)
            else: # Bot Message
                print("got bot message", Emojis.Session.start, Emojis.Session.end, Emojis.Session.searching)
                if Emojis.Session.end in msg.text:
                    print("Emojis.Session.end in msg.text")
                    if self.sessionActive:
                        for entity in msg.entities:
                            if hasattr(entity, "url"): self.activeSession.reopen_url = urlparse(entity.url)
                        self.activeSession.close()
                        await self.bot.client.send_message(self.log_channel, self.sessions[-1].print())
                    self.session_state = SessionState.Ended # Todo: Set searching if used next!
                    #  await self.replyAndDelete(msg, Commands.new_chat, delete_after_s=10)
                    if Emojis.Session.searching not in msg.text: await msg.reply(Commands.new_chat)
                    print("session stopped!")
                """
                for char in list(msg.text): # todo: remove debug shit
                    print(char, "==", Emojis.Session.start, ":", char == Emojis.Session.start, char.encode('ascii', 'backslashreplace'))
                """
                print(msg.text)
                print("Emojis.Session.start in msg.text ==", Emojis.Session.start in msg.text)

                if Emojis.Session.start in msg.text:
                    print("Emojis.Session.start in msg.text")
                    self.newSession(msg)
                    if not self.activeSession.greeted and choice(True, False): await self.greet(msg, self.activeSession)
                    print("new session!")
                if Emojis.Session.searching in msg.text:
                    print("Emojis.Session.searching in msg.text")
                    if self.sessionActive: self.activeSession.close()
                    self.session_state = SessionState.Searching
                    print("searching!")


    async def on_message_edit(self, event: tg.events.MessageEdited.Event):
        if event.chat_id == 339959826 and event.message.from_id is not None and event.message.from_id == self.bot.uid and not event.message.text.startswith("/"):
            await event.message.reply("/revoke")
            await event.message.respond(event.message.text)