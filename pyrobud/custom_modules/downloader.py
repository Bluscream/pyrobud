from pyrobud import command, module, util
import os
from pathlib import Path
from typing import Optional, Any
import telethon as tg
from pyrobud.util.bluscream import get_entity, UserStr
from time import time

class MediaDownloader(module.Module):
    """Module to download all media from a chat."""

    name = "Media Downloader"
    help = "Downloads all media from a specified chat"
    disabled = False
    commands = {}
    
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log

    @command.desc("Downloads all media in the given chat.")
    @command.alias("dlall")
    async def cmd_downloadall(self, ctx: command.Context):
        """
        Download all media from a specified chat.
        
        Usage: .download_media [chat_username]
        """
        
        chat_username = ctx.input
        
        # Create downloads directory if it doesn't exist
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)
        
        # Get the chat entity
        try:
            # chat_entity = await get_entity(self.bot, ctx)
            chat_entity = await self.bot.client.get_entity(ctx.input)
            # chat_entity = await ctx.event.client.get_input_entity(chat_username)
        except ValueError:
            await ctx.respond(f"Could not find chat {chat_username}")
            return
            
        # Create chat-specific directory
        chat_path = downloads_dir / str(chat_entity.id)
        chat_path.mkdir(exist_ok=True)
        
        # Get all messages with media
        #  iter_messages(entity: hints.EntityLike, limit: float = None, *, offset_date: hints.DateLike = None, offset_id: int = 0, max_id: int = 0, min_id: int = 0, add_offset: int = 0, search: str = None, filter: Union[types.TypeMessagesFilter, Type[types.TypeMessagesFilter]] = None, from_user: hints.EntityLike = None, wait_time: float = None, ids: Union[int, Sequence[int]] = None, reverse: bool = False, reply_to: int = None, scheduled: bool = False) → Union[_MessagesIter, _IDsIter]

        # all_photos = ctx.event.client.iter_messages(
        #     chat_entity, filter=tg.types.InputMessagesFilterPhotos
        # )
        # for photo in all_photos:
        #     ctx.event.client.download_media(photo)
        # all_photos = ctx.event.client.iter_messages(
        #     chat_entity, filter=tg.types.InputMessagesFilterVideo
        # )
        # for photo in all_photos:
        #     ctx.event.client.download_media(photo)

        total_messages = await ctx.event.client.get_messages(
            chat_entity,
            limit=None,
            filter=tg.types.InputMessagesFilterPhotoVideo
        )
        
        if not total_messages:
            await ctx.respond("No media found in this chat.")
            return
            
        # Download each media file
        downloaded_count = 0
        for msg in total_messages:
            if msg.media:
                try:
                    file_path = await msg.download_media(chat_path)
                    print(file_path)
                    try: os.utime(file_path, (msg.date.timestamp(), time.time()))
                    except Exception as e: print(f"Error setting file timestamp: {str(e)}")
                    downloaded_count += 1
                    # await event.client.send_message(
                    #     event.chat_id,
                    #     f"Downloaded {downloaded_count}/{len(total_messages)} files"
                    # )
                except Exception as e:
                    await ctx.respond(f"Error downloading media: {str(e)}")
                    continue
        
        await ctx.respond(
            f"Finished downloading {downloaded_count} files from {chat_username}"
        )