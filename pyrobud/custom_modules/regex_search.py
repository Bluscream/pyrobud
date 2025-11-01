import re
from pyrobud import command, module, util
from pyrobud.module import Module
import re
from telethon.events import register
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
from datetime import datetime

class ChatSearch(module.Module):
    name: str="Chat Search"
    description: str=""
    disabled: bool= False

    @command.desc("Search chat history using regex patterns")
    async def cmd_search(self, ctx: command.Context):
        msg = ctx.msg
        
        args = ctx.input.split()[1:]
        
        if not args:
            await msg.reply("Usage: !search <pattern> [max_messages]")
            return
            
        pattern:str = args[0]
        max_messages = int(args[1]) if len(args) > 1 else 100
        
        chat_id = ctx.event.chat_id
        
        try:
            # Try to compile the regex pattern
            re.compile(pattern)
        except re.error as e:
            await ctx.event.edit(f"Invalid regex pattern: {str(e)}")
            return
            
        # Initialize search parameters
        limit = 100  # Number of messages to fetch per request
        offset_id = 0
        results = []
        
        await ctx.event.edit("Searching messages...")
        
        while True:
            # Create search request
            search_request = SearchRequest(
                peer=ctx.event.chat,
                q="",  # Empty query to get all messages
                filter=InputMessagesFilterEmpty(),
                min_date=None,
                max_date=datetime.now(),
                offset_id=offset_id,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0,
                add_offset=0  # Required parameter
            )
            
            # Execute search
            response = await ctx.event.client(search_request)
            
            # Process messages
            for msg in response.messages:
                if re.search(pattern, msg.message):
                    results.append(msg)
                    
            # Check if we've reached the end
            if len(response.messages) < limit:
                break
                
            offset_id = response.messages[-1].id
            
            # Prevent rate limiting
            await ctx.event.client.disconnected
            
        # Format and send results
        if not results:
            await ctx.event.edit("No matches found")
            return
            
        result_text = f"Found {len(results)} matches:\n\n"
        for i, msg in enumerate(results, 1):
            link = f"https://t.me/c/{msg.chat.id}/{msg.id}"
            result_text += f"{i}. [{msg.sender.username}]({link})\n"
            result_text += f"   {msg.message[:50]}...\n\n"
            
        await ctx.event.edit(result_text)