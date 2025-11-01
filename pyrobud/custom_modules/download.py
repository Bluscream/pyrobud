"""
A pyrobud module to download a file to the host.
Author : Ojas Sinha<sinhaojas67@gmail.com
"""

from io import BytesIO
import os
from pyrobud import command, module, util

class Download(module.Module):
    name: str="Download"
    disabled: bool= False
    folder: str="/home/blu/Downloads/"

    @command.desc("Downloads the replied file on the host machine.")
    @command.alias("dw", "dl")
    async def cmd_download(self, ctx: command.Context):
        if not ctx.msg.is_reply:
            return "__Reply to a file to upload it.__"

        reply_msg = await ctx.msg.get_reply_message()
        if not reply_msg.file:
            return "__That message doesn't contain a file.__"

        ctx.respond("Starting download")

        data = await util.tg.download_file(ctx, reply_msg)
        buffer = BytesIO(data)
        
        if not reply_msg.file.name:
            if ctx.input:
                buffer.name = ctx.input
            else:
                buffer.name = "Unnamed_download"
        else:
            buffer.name = reply_msg.file.name

        buffer.name = buffer.name.split("/")[-1]
        
        with open(self.folder + buffer.name, mode='wb') as save:
            save.write(buffer.getbuffer())

        await ctx.respond("__Download Complete__")
