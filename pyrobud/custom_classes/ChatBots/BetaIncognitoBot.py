from ..ChatBot import *

class Bot(ChatBot):
    disabled = False
    prefix: str = "/"
    name: str = "ChatIncognitoBot"
    id: int = 339959826
    genders: dict[Gender, str] = {
        Gender.Female: '👧',
        Gender.Male: '👦',
        Gender.Unspecified: '🗣'
    }
    commands: dict[Command, str] = {
        Command.HELP: "help",
        Command.LANGUAGE: "language",
        Command.NEW_CHAT: "newchat",
        Command.NEXT_CHAT: "nextchat",
        Command.LEAVE_CHAT: "leavechat",
        Command.STOP_SEARCHING: "stopsearching",
        Command.SETTINGS: "settings",
        Command.REVOKE_MESSAGE: "revoke"

    }
    regexes: dict[Regex, re.Pattern] = {
        Regex.SESSION_SEARCHING: re.compile(".*🔍$"), # b'\\U0001f50d'
        Regex.SESSION_START: re.compile("⬇️️️️.*⬇️️️️"), # u\2B07
        Regex.SESSION_END: re.compile("⬆️.*⬆️"),
        Regex.SESSION_URL: re.compile("🔓🔑"),
        Regex.PARTNER_AGE: re.compile("📆\s+\w+\:\s+(?P<age>\d+)"),
        Regex.PARTNER_DISTANCE: re.compile("\📍\s*[<>]?\s+(?P<distance>\d+)\s+km"),
        Regex.MESSAGE_PARTNER: re.compile(".*(?P<sex>[🗣👧👦])Partner: (?P<msg>.*)"),
        Regex.MESSAGE_AUTHOR: re.compile("^[⚠⚠️]"),
    }