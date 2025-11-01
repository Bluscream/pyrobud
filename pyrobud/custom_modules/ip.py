"""
Pyrobud module to get details of a given IP address.
Author : Ojas Sinha<sinhaojas67@gmail.com>
"""

import asyncio
import json
import re

from pyrobud import command, module

class Ip(module.Module):
    name: str="IP"
    disabled: bool= False

    @command.desc("Get details of an IP address")
    @command.alias("if")
    @command.usage("[ip]", True)
    async def cmd_ip(self, ctx: command.Context):
        await ctx.respond("Processing...")
        ip_addr: str = ctx.input
        reply: str = f"**{ip_addr}**\n" 
        async with self.bot.http.get(f"http://ip-api.com/json/{ip_addr}") as resp:
            data: dict = json.loads(await resp.text())
            response: str = f'({data["status"]})'

            if response == "(success)":
                reply += f'**IP : ** `{data["query"]}`\n' \
                    f'**Country : ** `{data["country"]}`\n' \
                    f'**Region : ** `{data["regionName"]}`\n' \
                    f'**City : **`{data["city"]}`\n' \
                    f'**ZIP Code : **`{data["zip"]}`\n' \
                    f'**Latitude : **`{data["lat"]}`\n' \
                    f'**Longitude : **`{data["lon"]}`\n' \
                    f'**Timezone : **`{data["timezone"]}`\n' \
                    f'**ISP : **`{data["isp"]}`\n' \
                    f'**Organisation : **`{data["org"]}`\n' \
                    f'**AS : **`{data["as"]}`\n'
            else:
                reply += "Invalid"
            return re.sub("[()]", "", reply)
