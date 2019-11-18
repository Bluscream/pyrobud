from enum import Enum
from urllib import parse
from datetime import datetime, timedelta
from typing import List, ClassVar
import telethon as tg

from typing import TYPE_CHECKING
if TYPE_CHECKING: from pyrobud.custom_modules.ChatIncognitoBot import ChatIncognitoBot

prefix = "/"

class Commands(object):
    next_chat = prefix+"nextchat"
    leave_chat = prefix+"leavechat"
    new_chat = prefix+"newchat"
    revoke_message = prefix+"revoke"
    stop_searching = prefix+"stopsearching"
    settings = prefix+"settings"
    language = prefix+"language"
    help = prefix+"help"

class Emojis(object):
    class Session(object):
        searching = "🔍"
        start = "⬇️️️"
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
    state: SessionState
    partner_gender: Gender
    partner_age: int
    partner_distance_km: int
    starttime: datetime
    endtime: datetime
    reopen_url: parse.ParseResult
    messages: List[int]
    closer: SessionCloser
    greeted: bool = False

    @property
    def duration(self) -> timedelta:
        return self.endtime - self.starttime

    @classmethod
    def close(self):
        self.endtime = datetime.now()
        self.state = SessionState.Ended

    @classmethod
    def stop(self, module: ChatIncognitoBot):
        module.sendAndDelete(Commands.leave_chat)
        self.close()

    @classmethod
    def setGender(self, gender: str):
        if self.partner_gender: return
        if gender == Emojis.Gender.Unknown: self.partner_gender = Gender.Unspecified
        elif gender == Emojis.Gender.Female: self.partner_gender = Gender.Female
        elif gender == Emojis.Gender.Male: self.partner_gender = Gender.Male
        # else: self.partner_gender = Gender.Unknown

    def __init__(self, age=None, distance_km=None): # , state: SessionState = SessionState.Searching
        self.starttime = datetime.now()
        self.age = age
        self.distance_km = distance_km
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