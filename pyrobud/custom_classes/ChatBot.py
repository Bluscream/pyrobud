import asyncio
from dataclasses import dataclass
from enum import Enum
from random import choice, randint, randrange
from urllib import parse
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List, ClassVar, Any
from enum import auto
import telethon as tg
import json, re

# from pyrobud.util.bluscream import get_id

if TYPE_CHECKING:
    from pyrobud.module import Module
    from pyrobud.core.bot import Bot
    from pyrobud import util
    

# region enums
class Command(Enum):
    NEXT_CHAT = auto()
    LEAVE_CHAT = auto() 
    NEW_CHAT = auto()
    REVOKE_MESSAGE = auto()
    STOP_SEARCHING = auto()
    SETTINGS = auto()
    LANGUAGE = auto()
    HELP = auto()
class Regex(Enum):
    SESSION_SEARCHING = auto()
    SESSION_START = auto()
    SESSION_END = auto()
    SESSION_URL = auto()
    PARTNER_AGE = auto()
    PARTNER_DISTANCE = auto()
    PARTNER_GENDER = auto()
    MESSAGE_PARTNER = auto()
    MESSAGE_AUTHOR = auto()
    MESSAGE_GENDER = auto()
class Gender(Enum):
    Unknown = auto()
    Unspecified = auto()
    Male = auto()
    Female = auto()
    Nonbinary = auto()
class SessionState(Enum):
    Unknown = auto()
    Searching = auto()
    Active = auto()
    Ended = auto()
class SessionCloser(Enum):
    You = auto()
    Partner = auto()
# endregion enums

# region subclasses
class Partner(object):
    gender: Gender = None
    age: int = None
    location: tg.tl.custom.inlineresult.InlineResult.LOCATION = None
    vip: bool = None
    @property
    def distance_km(self) -> int:
        return -1 # Todo: Implement
    
    def __str__(self) -> str:
        parts = []
        if self.gender is not None:
            parts.append(f"Gender: {self.gender.name}")
        if self.age is not None:
            parts.append(f"Age: {self.age}")
        if self.distance_km is not None:
            parts.append(f"Distance: {self.distance_km}km")
        if self.vip is not None:
            parts.append(f"VIP: {self.vip}")
        return "\n".join(parts) if parts else "Unknown Partner"

    # def setGender(self, gender: str):
    #     if not self.partner: self.partner = Partner()
    #     if self.partner.gender: return
    #     if gender == Emojis.Gender.Unknown:
    #         self.partner_gender = Gender.Unspecified
    #     elif gender == Emojis.Gender.Female:
    #         self.partner_gender = Gender.Female
    #     elif gender == Emojis.Gender.Male:
    #         self.partner_gender = Gender.Male
    #     # else: self.partner_gender = Gender.Unknown

class Session(object):
    bot: "ChatBot"
    state: SessionState = SessionState.Unknown
    partner: Partner = None
    starttime: datetime = None
    endtime: datetime = None
    reopen_url: parse.ParseResult = None
    messages: List[int] = list()
    closer: SessionCloser = None
    greeted: str = ""

    @property
    def duration(self) -> timedelta:
        return self.endtime - self.starttime

    def __str__(self) -> str:
        pp = "State: " + str(self.state)
        if self.partner is not None: pp += "\nPartner: " + str(self.partner)
        if self.starttime is not None: pp += "\nStarttime: " + str(self.starttime)
        if self.endtime is not None: pp += "\nEndtime: " + str(self.endtime)
        if self.reopen_url is not None: pp += "\nURL: " + str(self.reopen_url)
        pp += "\n" + str(len(self.messages)) + " Messages: " + str(self.messages)
        if self.closer is not None: pp += "\nCloser: " + str(self.closer)
        if self.greeted is not None: pp += "\nGreeted with: " + str(self.greeted)
        return pp

    @classmethod
    def close(self):
        self.endtime = datetime.now()
        self.state = SessionState.Ended

    # @classmethod
    # def stop(self, module):  # : ChatIncognitoBot.ChatIncognitoBot):
    #     module.sendAndDelete(self.comm)
    #     self.close()

    def __init__(self, chatbot: "ChatBot"):  #  = SessionState.Searching
        self.bot = chatbot
        self.starttime = datetime.now()
        if not self.partner: self.partner = Partner()
        # self.state = state


class Settings(object):
    language: str
    use_keyboards: bool
    own_gender: Gender
    partner_gender: Gender
    location: tg.tl.custom.inlineresult.InlineResult.LOCATION
    birthdate: datetime
    partner_age_min: int
    partner_age_max: int
    reopen_requests_enabled: bool
# endregion subclasses

class ChatBot(object):
    module: "Module"
    name: str
    id: int
    prefix: str = "/"
    commands: dict[Command, str] = dict()
    regexes: dict[Regex, re.Pattern] = dict()
    genders: dict[Gender, str] = dict()
    sessions: list[Session] = list()
    log_channels: dict[int, str] = { -1001344802682: "ChatIncognitoBotLog" }
    settings: dict[str,Any] = {
        "enabled": True,
        "greet": True,
        "greeting": "{r;Hallo|Hi|Hey|Was geht|Yo|Jo} {r;;:3|:D|<3|♥|👌|✌|c:|?}" # \n\nIm felix (m, 20) from germany\nwho are you and where are you from?
    }

# region methods
    def __init__(self, mod: "Module"):
        self.module = mod

    def __str__(self):
        return f"`{self.name}` (`{self.id}`)\nPrefix: `{self.prefix}`\nCommands: `{len(self.commands)}`\nPatterns: `{len(self.regexes)}`\nSessions: `{len(self.sessions)}`" # Greeting Combinations: `{len(self.greeting_prefixes)*len(self.greeting_suffixes)}
    
    def print(self, *args, **kwargs):
        print(f"[{self.name}]", *args, **kwargs)

    def getCurrentSession(self) -> Session:
        if len(self.sessions) < 1: self.sessions.append(Session(self))
        return self.sessions[-1]

    def updateCurrentSession(self,
                      state: SessionState = None, closer: SessionCloser = None, 
                      gender: Gender = None, age: int = None, distance_km: int = None, vip: bool = None, greeted: str = None
        ):
        session = self.getCurrentSession()
        if state is not None:
            session.state = state
            match state:
                case SessionState.Active:
                    session.starttime = datetime.now()
                case SessionState.Ended:
                    session.endtime = datetime.now()
        if closer is not None: session.closer = closer
        if greeted is not None: session.greeted = greeted
        if not session.partner: session.partner = Partner()
        if gender is not None: session.partner.gender = gender
        if age is not None: session.partner.age = age
        if distance_km is not None: session.partner.distance_km = distance_km
        if vip is not None: session.partner.vip = vip
        self.print(f"Updated Session: {session}")

    async def greet(self):
        return
        session = self.getCurrentSession()
        if session.greeted or session.state is not SessionState.Active or not self.id: return
        await asyncio.sleep(randrange(1, 3)) # Todo: Sometimes wait for them to write first
        prefix: str = choice(self.greeting_prefixes)
        if choice((True, False)): prefix = prefix.lower()
        greeting = f"{prefix} {choice(self.greeting_suffixes)}"
        if self.add_info: greeting += ""
        await self.send_text(greeting)
        session.greeted = greeting

    def get_gender(self, txt: str):
        for gender, gender_txt in self.genders.items():
            if gender_txt == txt:
                return gender
        return Gender.Unknown
    
    def get_match_group(self, match: re.Match, name: str, _as: type = None):
        if not name in match.groupdict(): return None
        ret = match.group(name)
        if ret is None: return None
        match _as:
            case type(bool): return bool(ret)
            case type(float): return float(ret)
            case type(int): return int(ret)
        return ret

    async def send_text(self, text: str, delete_after_s=None):
        self.print(f"send_text(\"{text}\",delete_after_s={delete_after_s})")
        msg = await self.module.bot.client.send_message(self.id, text)
        self.print(msg)
        if delete_after_s != None:
            await asyncio.sleep(delete_after_s)
            # await msg.delete()

    async def send_command(self, command: Command, delete_after_s=5):
        cmd = self.prefix + self.commands[command]
        self.print(f"send_command(\"{cmd}\",delete_after_s={delete_after_s})")
        await self.send_text(cmd, delete_after_s)

    def match(self, pattern: Regex, text: str) -> re.Match | None:
        # self.print("pattern",pattern, "text", text)
        if not pattern in self.regexes: return None
        # patt = self.regexes[pattern]
        # self.print("patt",patt)
        # ret = patt.match(text, re.MULTILINE | re.UNICODE | re.DOTALL)
        # self.print("ret",ret)
        ret = self.regexes[pattern].match(text, re.MULTILINE | re.UNICODE | re.DOTALL)
        if ret: return ret
        ret = self.regexes[pattern].match(text, re.MULTILINE | re.UNICODE)
        if ret: return ret
        ret = self.regexes[pattern].match(text, re.MULTILINE)
        if ret: return ret
        ret = self.regexes[pattern].match(text)
        return ret
# endregion methods

# region events
    async def on_message_from_bot(self, message: tg.tl.custom.message.Message) -> None:
        partner_match = self.match(Regex.MESSAGE_PARTNER, message.text)
        session_start_match = self.match(Regex.SESSION_START, message.text)
        session_end_match = self.match(Regex.SESSION_END, message.text)
        session_search_match = self.match(Regex.SESSION_SEARCHING, message.text)
        self.print(f"on_message_from_bot (partner: {partner_match}, started={session_start_match}, ended={session_end_match}, searching={session_search_match})\n\"{message.text}\"")
        if partner_match:
            gender = self.get_match_group(partner_match, 'sex')
            msg = self.get_match_group(partner_match, 'msg')
            self.print(f"Got message from {gender} partner: {msg}")
            self.updateCurrentSession(SessionState.Active, None, gender)
            return
        if session_end_match:
            self.updateCurrentSession(SessionState.Ended)
            await asyncio.sleep(randint(1,10))
            self.sessions.remove(self.getCurrentSession())
            await self.send_command(Command.NEW_CHAT)
            await self.module.db.inc("sessions_ended")
        if session_start_match:
            self.updateCurrentSession(
                SessionState.Active, None,
                self.get_gender(self.get_match_group(session_start_match, '')),
                self.get_match_group(session_start_match, 'age', type(int)),
                self.get_match_group(session_start_match, 'distance', type(int)),
                self.get_match_group(session_start_match, 'vip', type(bool)),
                greeted=None
            )
            await self.greet()
            await self.module.db.inc("sessions_started")
        elif session_search_match:
            self.updateCurrentSession(SessionState.Searching)
        elif self.match(Regex.MESSAGE_AUTHOR, message.text):
            self.print("Got author message, deleting: \"{message.text}\"")
            try:
                if message.is_reply: await self.module.bot.client.delete_messages(message.chat_id, message.reply_to_msg_id)
            except Exception as ex: self.print(ex)
            await message.delete()

    async def on_message_to_bot(self, message: tg.tl.custom.message.Message) -> None:
        self.print(f"on_message_to_bot: \"{message.text}\"")
        lower_txt = message.text.lower()
        if lower_txt == "/session":
            lines = list()
            # lines.append(f"Media blacklisted: `{self.check_for_media}`")
            # lines.append(f"Last deleted media at: `{self.last_deleted_media}`")
            lines.append(f"Sessions: `{len(self.sessions)}`")
            if self.sessions: lines.append(f"Last Session: `{self.getCurrentSession()}`")
            if len(lines) > 0: await message.edit("\n".join(lines))
        elif lower_txt == "/media":
            self.check_for_media = not self.check_for_media
            await self.replyAndDelete(message, text=f"You are {'no longer allowed to send media ❌' if self.check_for_media else 'allowed to send media now ✔'}", delete_after_s=15, delete_original=True)
        elif lower_txt.startswith("/setting "):
            args = lower_txt.replace("/setting ", "").split(" ")
            self.settings[args[0]] = not self.settings[args[0]]
            distr = "Enabled" if self.settings["enabled"] else "Disabled"
            await message.edit(f"{distr} `{self.name}` (`{self.id}`)")
        elif lower_txt == "/toggleinfo":
            self.add_info = not self.add_info
            distr = "Enabled" if self.add_info else "Disabled"
            await message.edit(f"{distr} info for `{self.name}` (`{self.id}`)")
        elif lower_txt == "/stats":
            sessions_started = await self.module.db.get("sessions_started", -1)
            sessions_ended = await self.module.db.get("sessions_ended", -1)
            await message.edit(f"`{self.name}` (`{self.id}`):\n\nSessions started: {sessions_started}\nSessions ended: {sessions_ended}")

    async def on_message_edited(self, message: tg.tl.custom.message.Message):
        pass # self.print(f"on_message_edited")

    async def on_self_message_edited(self, message: tg.tl.custom.message.Message):
        self.print(f"on_self_message_edited")
        if Command.REVOKE_MESSAGE in self.commands and not message.text.startswith("/") and not message.text.startswith("."):
            await self.send_command(Command.REVOKE_MESSAGE, delete_after_s=5)
            await self.send_text(message.text)
            await message.delete()
# endregion events
