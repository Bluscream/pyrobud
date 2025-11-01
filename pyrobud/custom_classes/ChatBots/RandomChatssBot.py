from ..ChatBot import *


class Bot(ChatBot):
    name: str = "RandomChatssBot"
    id: int = 1390401778
    disabled = False
    prefix: str = "/"
    genders: dict[Gender, str] = {
        Gender.Male: '🧔',
        Gender.Unspecified: '👤'
    }
    commands: dict[Command, str] = {
        Command.NEW_CHAT: "start"
    }
    regexes: dict[Regex, re.Pattern] = {
        Regex.SESSION_END: re.compile("\*\*Chat beendet\*\*"),
        Regex.SESSION_START: re.compile("\n🗣\w+ (?P<sex>👤|🧔) \w+\n")
    }