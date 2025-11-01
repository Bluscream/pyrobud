import asyncio
import io
from pathlib import PurePosixPath, Path
from typing import IO

import telethon as tg
from .. import command, module, util
from aiohttp import ClientSession
from ..custom_classes.RevImgProviders import iqdb, tineye
from ..custom_classes.RevImgProvider import ReverseImageSearchProvider

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from pyrobud.core.bot import Bot
    from pyrobud import core
    # from pyrobud.custom_modules.ChatIncognitoBotClasses import *


class ReverseImageSearch(module.Module):
    name = "Reverse Image search"
    disabled = False

    bot: "Bot"
    # client: tg.TelegramClient
    db: util.db.AsyncDB

    providers: list[ReverseImageSearchProvider] = [
        iqdb.Provider(),
        # dans.Provider(),
        # sauce.Provider(),
        # tineye.Provider()x
    ]

    async def on_load(self) -> None:
        self.db = self.bot.get_db("reverse_image_search")
        for provider in self.providers:
            provider.start()

    # async def on_message(self, event: tg.events.NewMessage.Event) -> None:
    #     self.log.info(f"Received message: {event.message}")
    #     await self.db.inc("messages_received")

    @command.desc("Reverse search a image or a profile picture")
    @command.alias("rev")
    # @command.usage("[text to echo?, or reply]", optional=True, reply=True)
    async def cmd_reverse(self, ctx: command.Context) -> str:
        await ctx.respond("Processing...")

        photos: dict[str,bytes] = {}

        if ctx.msg.is_reply:
            replied_msg: tg.types.Message = await ctx.msg.get_reply_message()
            if replied_msg.media.photo:
                replied_photo_filename = f"{replied_msg.media.photo.id}{replied_msg.file.ext}"
                photos[replied_photo_filename] = await replied_msg.download_media(bytes)

            profile_picture_file_name = f"{replied_msg.from_id.user_id}.png"
            photos[profile_picture_file_name] = await self.bot.client.download_profile_photo(replied_msg.from_id.user_id, bytes)


        if len(photos) < 1: return "No photos found anywhere."

        res: list[str] = []

        tres = ""

        for provider in self.providers:
            print(f"Searching with {provider.name}")
            res.append(f"# Similar Images on [{provider.name}]({provider.base_url}):\n")
            for path, data in photos.items():
                tres += f"Searching with {provider.name} for {path}...\n"
                await ctx.respond(tres)
                print(f"Searching for photo: {path}")
                resp = await provider.search_file(path, data)
                res.append(resp)


        return '\n'.join(res)

    async def get_image(self, url: str) -> IO[bytes]:
        # Get the link to a random cat picture
        async with self.bot.http.get(url) as resp:
            # Read and parse the response as JSON
            data = await resp.read()
        # Construct a byte stream from the data.
        # This is necessary because the bytes object is immutable, but we need to add a "name" attribute to set the
        # filename. This facilitates the setting of said attribute without altering behavior.
        
        # Set the name of the cat picture before sending.
        # This is necessary for Telethon to detect the file type and send it as a photo/GIF rather than just a plain
        # unnamed file that doesn't render as media in clients.
        # We abuse pathlib to extract the filename section here for convenience, since URLs are *mostly* POSIX paths
        # with the exception of the protocol part, which we don't care about here.
        data.name = PurePosixPath(data).name
        return data
