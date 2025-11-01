from ..ChatBot import *


class Bot(ChatBot):
    name: str = "AnonimeChatBot"
    id: int = 465316912
    disabled = False
    prefix: str = "/"
    genders: dict[Gender, str] = {
        Gender.Male: '👦',
        Gender.Unspecified: '👤'
    }
    commands: dict[Command, str] = {
        Command.NEW_CHAT: "newchat",
        Command.NEXT_CHAT: "nextchat",
        Command.LEAVE_CHAT: "end",
        Command.REVOKE_MESSAGE: "delete"
    }
    regexes: dict[Regex, re.Pattern] = {
        Regex.SESSION_SEARCHING: re.compile("🔍 Searching... Use /stopsearch if you want to stop it"),
        Regex.SESSION_START: re.compile("(?:Gender: (?P<sex>👤|👦)\n\n)?(?:📅 Age: (?P<age>\d+)\n\n)?ID CHAT: (?P<id>.+)"), # (?:Gender:\s+(?P<sex>👤|👦)\s+)?(?:📅\s+Age:\s+(?P<age>\d+))?.*\s+ID\s+CHAT:\s+(?P<id>.+)")
        # Regex.MESSAGE_PARTNER: re.compile(""),
        Regex.SESSION_END: re.compile("👋 Your partner has left the chat"),
    }