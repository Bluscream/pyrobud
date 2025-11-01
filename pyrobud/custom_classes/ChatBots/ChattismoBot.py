from ..ChatBot import *


class Bot(ChatBot):
    name: str = "ChattismoBot"
    id: int = 807551872
    disabled = False
    prefix: str = "/"
    genders: dict[Gender, str] = {
        Gender.Male: '👨'
    }
    commands: dict[Command, str] = {
        Command.NEW_CHAT: "search"
    }
    regexes: dict[Regex, re.Pattern] = {
        Regex.SESSION_SEARCHING: re.compile("🔍 Cercando un partner 🔍"),
        Regex.SESSION_START: re.compile("✅ Partner Trovato!"),
        Regex.MESSAGE_PARTNER: re.compile("^(?:(?P<sex>👨) )?Partner » (?P<msg>.*)$"),
        Regex.SESSION_END: re.compile("💔 Il partner è uscito dalla chat 💔|❌ Devi essere in una chat ❌") # "⏹️ Hai cancellato la ricerca ⏹️"
    }