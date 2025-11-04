"""
Example module demonstrating pyrobud module features.

This comprehensive example module demonstrates:
- Commands with aliases, usage info, and error handling
- Database operations (get, set, increment, delete)
- Event listeners (messages, edits, start/stop)
- HTTP requests and JSON parsing
- File handling and uploads
- Async operations and proper error handling
- Dependency management (see ExampleWithDeps class below)

See full documentation at: https://bluscream.github.io/pyrobud/
"""

import asyncio
import io
from pathlib import PurePosixPath
from typing import IO, ClassVar

import telethon as tg

from .. import command, module, util


class ExampleModule(module.Module):
    """Comprehensive example showing all major pyrobud features."""

    name: ClassVar[str] = "Example"
    disabled: ClassVar[bool] = True  # Set to False to enable

    # Instance variables with type hints
    db: util.db.AsyncDB
    message_count: int

    async def on_load(self) -> None:
        """Called when the module is loaded - initialize resources here."""
        self.db = self.bot.get_db("example")
        self.message_count = 0

        # You can load saved state from database
        self.message_count = await self.db.get("message_count", 0)

        self.log.info(f"Example module loaded (message count: {self.message_count})")

    async def on_start(self, time_us: int) -> None:
        """Called when the bot starts (after on_load, after user info loaded)."""
        self.log.info("Bot started! Ready to process messages.")

    async def on_stop(self) -> None:
        """Called when the bot is stopping - cleanup resources here."""
        # Save state before shutdown
        await self.db.put("message_count", self.message_count)
        self.log.info("Example module shutting down, state saved")

    async def on_message(self, event: tg.events.NewMessage.Event) -> None:
        """
        Event listener: Called for every new message (sent or received).

        This demonstrates event listening. You can add conditions to only
        process certain messages.
        """
        self.message_count += 1

        # Example: Only log messages from specific chats
        # if event.chat_id in [123456789, 987654321]:
        #     self.log.info(f"Message in monitored chat: {event.message.text}")

        # Update stats in database
        await self.db.inc("messages_received")

    async def on_message_edit(self, event: tg.events.MessageEdited.Event) -> None:
        """Event listener: Called when a message is edited."""
        # You can track edits if needed
        await self.db.inc("messages_edited")

    @command.desc("Simple echo/test command")
    @command.alias("echotest", "test2")
    @command.usage("[text to echo?, or reply]", optional=True, reply=True)
    async def cmd_test(self, ctx: command.Context) -> str:
        """
        Basic command example with optional input.

        This shows:
        - Command with multiple aliases
        - Optional parameter (can work without input)
        - Responding to user before completion
        - Returning a string that becomes the final message
        """
        # Send a temporary message while processing
        await ctx.respond("Processing...")

        # Simulate some work
        await asyncio.sleep(1)

        # If user provided input, echo it back
        if ctx.input:
            return ctx.input

        # Otherwise return default message
        return "✅ It works!"

    @command.desc("Show database statistics")
    @command.alias("dbstats")
    async def cmd_stats(self, ctx: command.Context) -> str:
        """
        Demonstrates database operations.

        Shows how to:
        - Read values from database
        - Format output nicely
        - Handle missing values with defaults
        """
        messages_received = await self.db.get("messages_received", 0)
        messages_edited = await self.db.get("messages_edited", 0)
        message_count = await self.db.get("message_count", 0)

        return f"""**Example Module Stats:**

📨 Messages received: {messages_received}
✏️ Messages edited: {messages_edited}
🔢 Session message count: {message_count}

💾 Database: {self.db._prefix}"""

    @command.desc("Reset all statistics")
    async def cmd_resetstats(self, ctx: command.Context) -> str:
        """Demonstrates database deletion operations."""
        # Clear all stats
        await self.db.delete("messages_received")
        await self.db.delete("messages_edited")
        await self.db.put("message_count", 0)
        self.message_count = 0

        return "✅ All statistics have been reset"

    async def get_cat(self) -> IO[bytes]:
        """
        Helper method to fetch a random cat picture.

        Demonstrates:
        - HTTP requests with aiohttp
        - JSON parsing
        - Binary data handling
        - File stream creation for Telegram uploads
        - Error handling for network operations
        """
        try:
            # Get the link to a random cat picture
            async with self.bot.http.get("https://aws.random.cat/meow") as resp:
                if resp.status != 200:
                    raise Exception(f"API returned status {resp.status}")

                # Read and parse the response as JSON
                json = await resp.json()
                # Get the "file" field from the parsed JSON object
                cat_url = json["file"]

            # Get the actual cat picture
            async with self.bot.http.get(cat_url) as resp:
                if resp.status != 200:
                    raise Exception(f"Image fetch returned status {resp.status}")

                # Get the data as a byte array (bytes object)
                cat_data = await resp.read()

            # Construct a byte stream from the data.
            # This is necessary because the bytes object is immutable, but we need to add a "name" attribute to set the
            # filename. This facilitates the setting of said attribute without altering behavior.
            cat_stream = io.BytesIO(cat_data)

            # Set the name of the cat picture before sending.
            # This is necessary for Telethon to detect the file type and send it as a photo/GIF rather than just a plain
            # unnamed file that doesn't render as media in clients.
            # We abuse pathlib to extract the filename section here for convenience, since URLs are *mostly* POSIX paths
            # with the exception of the protocol part, which we don't care about here.
            cat_stream.name = PurePosixPath(cat_url).name

            return cat_stream

        except Exception as e:
            self.log.error(f"Failed to fetch cat picture: {e}")
            raise

    @command.desc("Get a random cat picture")
    async def cmd_cat(self, ctx: command.Context) -> str:
        """
        Demonstrates file uploads and error handling.

        Shows:
        - Async file operations
        - Upload files to Telegram
        - Proper error handling and user feedback
        """
        await ctx.respond("🐱 Fetching cat...")

        try:
            cat_stream = await self.get_cat()

            # Upload and send the cat picture
            # mode="repost" replaces the "Fetching cat..." message
            await ctx.respond(file=cat_stream, mode="repost")

        except Exception as e:
            return f"⚠️ Failed to fetch cat picture: {str(e)}"


# ============================================================================
# DEPENDENCY MANAGEMENT EXAMPLE
# ============================================================================
# The following class demonstrates the powerful dependency management system.
# Uncomment the decorator below to test automatic dependency installation.
# ============================================================================

# @util.dependencies.requires('beautifulsoup4>=4.9.0', 'requests>=2.28.0')
class ExampleWithDeps(module.Module):
    """
    Advanced example showing the dependency management system.

    This demonstrates:
    - Automatic dependency installation via @requires decorator
    - Using external packages (beautifulsoup4, requests)
    - Graceful handling of missing dependencies
    - Best practices for module dependencies

    To enable and test:
    1. Uncomment the @util.dependencies.requires decorator above (line 147)
    2. Set disabled = False below
    3. Restart the bot
    4. Dependencies will auto-install on first load!
    5. Use .fetch <url> to test

    See full documentation at: docs/dependencies.md
    """

    name: ClassVar[str] = "Example Deps"
    disabled: ClassVar[bool] = True  # Set to False to enable

    db: util.db.AsyncDB

    async def on_load(self) -> None:
        """Initialize the module - dependencies are already installed by decorator."""
        # If you uncommented the decorator, these imports will work:
        # from bs4 import BeautifulSoup
        # import requests

        self.db = self.bot.get_db("example_deps")
        self.log.info("Example dependency module loaded")
        self.log.info("Try .fetch <url> to test web scraping")
    
    @command.desc("Fetch and parse a web page title")
    @command.usage("[URL]")
    async def cmd_fetch(self, ctx: command.Context) -> str:
        """
        Demonstrates dependency usage after auto-installation.

        This command:
        - Uses beautifulsoup4 and requests (auto-installed by decorator)
        - Fetches a URL and parses HTML
        - Extracts structured data from web pages
        - Shows proper error handling for network operations
        """
        # Import dependencies when needed (they're guaranteed to be installed by @requires)
        try:
            from bs4 import BeautifulSoup
            import requests
        except ImportError:
            return """⚠️ **Dependencies not installed**

To enable this command:
1. Uncomment line 147: `# @util.dependencies.requires(...)`
2. Restart the bot
3. Dependencies will auto-install!

See docs/dependencies.md for more info."""

        if not ctx.input:
            return "⚠️ Please provide a URL\n\n**Usage:** `.fetch https://example.com`"

        url = ctx.input.strip()

        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        await ctx.respond(f"🌐 Fetching {url}...")

        try:
            # Fetch the page
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title = soup.find('title')
            title_text = title.string.strip() if title else "No title found"

            # Extract meta description
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag.get('content', 'No description') if description_tag else 'No description'

            return f"""**📄 Page Info:**

**Title:** {title_text}

**Description:** {description[:200]}{'...' if len(description) > 200 else ''}

**URL:** {url}
**Status:** {response.status_code}"""

        except requests.RequestException as e:
            return f"⚠️ **Network Error:**\n{str(e)}"
        except Exception as e:
            return f"⚠️ **Parsing Error:**\n{str(e)}"
    
    @command.desc("Test dependency installation")
    async def cmd_deptest(self, ctx: command.Context) -> str:
        """Test that dependencies are properly installed."""
        results = []
        
        # Test beautifulsoup4
        try:
            from bs4 import BeautifulSoup
            results.append("✅ beautifulsoup4 (bs4) - installed")
        except ImportError:
            results.append("❌ beautifulsoup4 (bs4) - not installed")
        
        # Test requests
        try:
            import requests
            results.append(f"✅ requests - installed (version {requests.__version__})")
        except ImportError:
            results.append("❌ requests - not installed")
        
        return "\n".join(results)
