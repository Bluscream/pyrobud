from ..RevImgProvider import *
from pyrobud import command, module, util
from pathlib import Path
from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from os import path as ospath

class Provider(ReverseImageSearchProvider):
    name: str = "IQDB"
    base_url: str = 'https://iqdb.org'

    async def search_file(self, path: Path, data: bytes) -> str:
        resp = await self.upload_file(self.base_url, path, data)
        if isinstance(resp, ClientResponse): return await self.parse_response(resp)
        return resp.text()
    
    async def parse_response(self, resp: ClientResponse):
        soup = BeautifulSoup(await resp.text(), 'html.parser')
        # This is for the no relevant matches case
        pages_div = soup.find(id='pages').find_all('div')[1]
        # stop searching if no relevant match was found
        if str(pages_div.find('th')) == '<th> No relevant matches </th>':
            await self.bot.reply('No relevant Match was found')

        matches = soup.find(id='pages')
        best_match = matches.select('a')[0].attrs['href']
        danbooru_found = False
        for match in matches.select('a'):
            source = match.attrs['href']
            if source.startswith('//danbooru.donmai.us') and not danbooru_found:
                danbooru_found = True
                danbooru = 'http:'+source
                characters, artist, franchise = await self._danbooru_api(danbooru)
                message = ''
                if characters:
                    message += '\n**Characters:** {} \n'.format(characters)
                if artist:
                    message += '**Artist:** {} \n'.format(artist)
                if franchise:
                    message += '**Copyright:** {} \n'.format(franchise)

                message += '**Source:** <{}> \n'.format(danbooru)
                return message
        if not danbooru_found:
            return f"https:{best_match}"