import telethon as tg
import asyncio
from telethon.tl.types import PeerUser
from datetime import timedelta, datetime
from .. import module, util
from random import shuffle, choice


class SuperEval(module.Module):
    name = "SuperEval"
    enabled_for = [PeerUser(user_id=689222097)]
    blocked_for = []
    command = "seval"
    min_chars = 15
    max_chars = 1500
    max_chars_scramble_case = 50
    last_used = datetime.min
    min_time = timedelta(minutes=10)
    template = """**Command:**
```{command}```

**Result:**
```{result}```

Time: `{time}`
"""

    def __init__(self, bot):
        super().__init__(bot)

    def scrambleText(self, text):
        lst = list(text); shuffle(lst)
        return ''.join(lst)

    def scrambleCase(self, text):
        chars = list(text)
        for idx, ch in enumerate(chars):
            if choice((True, False)): ch = ch.upper()
            chars[idx] = ch
        return "".join(chars)

    async def on_message(self, msg: tg.custom.Message):
        if msg.to_id is None or msg.to_id not in self.enabled_for: return
        if not msg.raw_text.startswith(self.bot.prefix): return
        if msg.from_id in self.blocked_for: return
        text = util.tg.filter_code_block(msg.raw_text)
        txt = text.lower().replace(self.bot.prefix, "", 1)
        if not txt.startswith(self.command): return
        now = datetime.now()
        since_last = now - self.last_used
        if since_last < self.min_time:
            msg = await msg.reply(f"You'll have to wait {self.min_time - since_last} to use this command again")
            await asyncio.sleep(5)
            await msg.delete()
            return
        # txt = txt.replace(command, "", 0)
        text = text[len(self.bot.prefix + self.command):].replace("`", "").strip()
        if len(text) < self.min_chars: await msg.reply(f"Statement has to be at least {self.min_chars} chars long!"); return
        if len(text) > self.max_chars: await msg.reply(f"Statement can't be longer than {self.max_chars}!"); return
        self.last_used = now
        if len(text) < self.max_chars_scramble_case: text = self.scrambleCase(text)
        text = self.scrambleText(text)

        def _eval():
            nonlocal msg, self

            # pylint: disable=unused-variable
            def send(text):
                return self.bot.loop.create_task(msg.respond(text))

            return eval(text)

        before = util.time.usec()
        try:  result = await util.run_sync(_eval)
        except Exception as err: result = str(err)
        after = util.time.usec()

        el_us = after - before
        el_str = util.time.format_duration_us(el_us)

        await msg.reply(self.template.format(command=str(text).replace("`", ""), result=str(result).replace("`", ""), time=el_str))

    async def cmd_supereval(self, msg: tg.custom.Message, args: str):
        if args:
            args = args.lower().split()
            if args[0] == "time":
                if len(args) > 1 and args[1].isdigit():
                    self.min_time = timedelta(seconds=int(args[1]))
                return f"Min time between uses is now {self.min_time}!"
            elif args[0] == "reset":
                self.last_used = datetime.min
                return f"Supereval has been reset and can be used now!"
            elif args[0] == "block":
                repl: tg.custom.Message = await msg.get_reply_message()
                if repl.from_id in self.blocked_for: self.blocked_for.remove(repl.from_id)
                else: self.blocked_for.append(repl.from_id)
                state = "blocked" if repl.from_id in self.blocked_for else "unblocked"
                return f"`{repl.from_id}` has been {state} from using supereval"
        else:
            if msg.to_id in self.enabled_for:
                self.enabled_for.remove(msg.to_id)
            else:
                self.enabled_for.append(msg.to_id)
            state = "enabled" if msg.to_id in self.enabled_for else "disabled"
            return f"Supereval has been {state} in this chat!" # ({', '.join(str(a) for a in self.enabled_for)})"
