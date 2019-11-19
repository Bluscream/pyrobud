from enum import Enum
from urllib import parse
from datetime import datetime, timedelta
from typing import List, ClassVar
import telethon as tg

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
# from ..custom_modules.ChatIncognitoBot import ChatIncognitoBot

prefix = "/"


class Commands(object):
    next_chat = prefix + "nextchat"
    leave_chat = prefix + "leavechat"
    new_chat = prefix + "newchat"
    revoke_message = prefix + "revoke"
    stop_searching = prefix + "stopsearching"
    settings = prefix + "settings"
    language = prefix + "language"
    help = prefix + "help"


class Emojis(object):
    class Session(object):
        searching = "🔍" # b'\\U0001f50d'
        start = "⬇️️️️" # u\2B07
        end = "⬆️"
        # url = "🔓🔑"

    class Partner(object):
        age = "📆"
        distance = "📍"

    class Gender(object):
        Unknown = "🗣"
        Female = "👧"
        Male = "👦"


class Gender(Enum):
    # Unknown = 1
    Unspecified = 1
    Male = 2
    Female = 3


class SessionState(Enum):
    Unknown = 1
    Searching = 2
    Active = 3
    Ended = 4


class SessionCloser(Enum):
    You = 1
    Partner = 2


class Session(object):
    state: SessionState = None
    partner_gender: Gender = None
    partner_age: int = None
    partner_distance_km: int = None
    starttime: datetime = None
    endtime: datetime = None
    reopen_url: parse.ParseResult = None
    messages: List[int] = list()
    closer: SessionCloser = None
    greeted: bool = False

    @property
    def duration(self) -> timedelta:
        return self.endtime - self.starttime

    @classmethod
    def print(self, doPrint = False) -> str:
        pp = "State: " + str(self.state)
        if self.partner_gender is not None: pp += "\nGender: " + str(self.partner_gender)
        if self.partner_age is not None: pp += "\nAge: " + str(self.partner_age)
        if self.partner_distance_km is not None: pp += "\nDistance: " + str(self.partner_distance_km) + "KM"
        if self.starttime is not None: pp += "\nStarttime: " + str(self.starttime)
        if self.endtime is not None: pp += "\nEndtime: " + str(self.endtime)
        if self.reopen_url is not None: pp += "\nURL: " + str(self.reopen_url)
        pp += "\n" + str(len(self.messages)) + " Messages: " + str(self.messages)
        if self.closer is not None: pp += "\nCloser: " + str(self.closer)
        if self.greeted is not None: pp += "\nGreeted: " + str(self.greeted)
        if doPrint: print(pp)
        return pp

    @classmethod
    def close(self):
        self.endtime = datetime.now()
        self.state = SessionState.Ended

    @classmethod
    def stop(self, module):  # : ChatIncognitoBot.ChatIncognitoBot):
        module.sendAndDelete(Commands.leave_chat)
        self.close()

    @classmethod
    def setGender(self, gender: str):
        if self.partner_gender: return
        if gender == Emojis.Gender.Unknown:
            self.partner_gender = Gender.Unspecified
        elif gender == Emojis.Gender.Female:
            self.partner_gender = Gender.Female
        elif gender == Emojis.Gender.Male:
            self.partner_gender = Gender.Male
        # else: self.partner_gender = Gender.Unknown

    def __init__(self, age=None, distance=None):  # , state: SessionState = SessionState.Searching
        self.starttime = datetime.now()
        self.partner_age = age
        self.partner_distance_km = distance
        # self.state = state


class Settings(object):
    language: str
    use_keyboards: bool
    own_gender: Gender
    partner_gender: Gender
    location: tg.custom.inlineresult.InlineResult.LOCATION
    birthdate: datetime
    partner_age_min: int
    partner_age_max: int
    reopen_requests_enabled: bool
