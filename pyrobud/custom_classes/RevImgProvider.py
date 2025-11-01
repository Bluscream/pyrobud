import asyncio
from dataclasses import dataclass
from enum import Enum
from random import choice, randint, randrange
from urllib import parse
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List, ClassVar, Any
from enum import auto
import telethon as tg
import json, re
from aiohttp import ClientSession, FormData, ClientResponse
from pathlib import Path
from os import path as ospath

# from pyrobud.util.bluscream import get_id

if TYPE_CHECKING:
    from pyrobud.module import Module
    from pyrobud.core.bot import Bot
    from pyrobud import util

# region enums
# endregion enums

class ReverseImageSearchProvider(object):
    module: "Module"
    name: str
    base_url: str
    settings: dict[str,Any] = {
        "enabled": True
    }

    session: ClientSession

    def __init__(self) -> None:
        print(f"Initializing Image Reverse Search provider {self.name}")

    def start(self) -> None:
        self.session = ClientSession()

    async def temp_upload(self, file_path:Path, file_data:bytes) -> ClientResponse | str:
        # headers = {
        #     "Accept": "application/json",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Accept-Encoding": "gzip, deflate, br, zstd",
        #     "Origin": "https://imgdrop.io",
        #     "DNT": "1",
        #     "Sec-GPC": "1",
        #     "Referer": "https://imgdrop.io/json",
        #     "Sec-Fetch-Dest": "empty",
        #     "Sec-Fetch-Mode": "cors",
        #     "Sec-Fetch-Site": "same-origin",
        #     "Sec-CH-Prefers-Color-Scheme": "dark",
        #     "Priority": "u=0",
        #     "Pragma": "no-cache",
        #     "Cache-Control": "no-cache",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        #     "Cookie": "PHPSESSID=eihhpueol002ts4is4ibsl37d4"
        # }
        resp = await self.upload_file("https://catbox.moe/user/api.php", file_path, file_data, headers=None, field_name="fileToUpload")
        if not isinstance(resp, ClientResponse): raise Exception(f"Unable to upload temp file: {resp}")
        url = await resp.text('utf-8')
        print(f"Uploaded file temporarily to {url}")
        return url


    # url variables: {path}/{name}/{extension}
    async def upload_file(self, url:str, file_path:Path, file_data:bytes = None, headers:dict[str,str] = None, field_name="file") -> ClientResponse | str:
        ret: list[str] = [f"Uploading {file_path} to {self.name}"]
        session = self.session
        # async with self.session as session:
        # Create a form data object
        data = FormData()

        # Get the filename and extension of the file
        filename = ospath.basename(file_path)
        extension = ospath.splitext(file_path)[1]
        # Get the content type based on the extension
        if extension == ".jpg" or extension == ".jpeg":
            content_type = "image/jpeg"
        elif extension == ".png":
            content_type = "image/png"
        else:
            content_type = "application/octet-stream"

        # Add the file to the form data
        data.add_field(
            name = field_name,
            value = file_data or open(file_path, "rb"),
            filename=filename,
            content_type=content_type,
        )
        data.add_field(
            name = "reqtype",
            value = "fileupload"
        )
        data.add_field(
            name = "userhash",
            value = ""
        )

        # Send a POST request to the server URL with the form data
        async with session.post(
            url.format(path=file_path,name=filename,extension=extension),
            data=data,
            headers=headers, # {"Authorization": "Bearer 123456"},  # Specify headers if necessary
            ssl=True,
        ) as response:
            # Get the status code, headers, and body of the response
            status = response.status
            body = await response.text('utf-8')
            # Print the response information
            ret.append(f"Status: {status}")
            ret.append(f"Body: {body}")

            # Handle errors or exceptions if any
            if status != 200 and status != 201: ret.append(f"Error: {response.reason}")
            if status >= 200 and status < 300: return response
        ret = '\n'.join(ret)
        print(ret)
        return ret
    
    async def search_file(self, path: Path, data: bytes) -> str:
        return await self.upload_file(self.base_url, path, data)
    async def search_url(self, url:str) -> str: pass

    def stop(self) -> None:
        if self.session:
            self.session.close()
            self.session = None
        print(f"Stopped Image Reverse Search provider {self.name}")