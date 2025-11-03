import asyncio
import logging
import sys
from pathlib import Path

import aiorun
import tomlkit

from . import DEFAULT_CONFIG_PATH, util
from .core import Bot

log = logging.getLogger("launch")
# Silence aiorun's overly verbose logger
aiorun.logger.disabled = True


def setup_asyncio(config: util.config.Config) -> asyncio.AbstractEventLoop:
    """Returns a new asyncio event loop with settings from the given config."""

    asyncio_config: util.config.AsyncIOConfig = config["asyncio"]

    if sys.platform == "win32":
        # Force ProactorEventLoop on Windows for subprocess support
        policy = asyncio.WindowsProactorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)
    elif not asyncio_config["disable_uvloop"]:
        # Initialize uvloop if available
        try:
            # noinspection PyUnresolvedReferences
            import uvloop

            uvloop.install()
            log.info("Using uvloop event loop")
        except ImportError:
            pass

    loop = asyncio.new_event_loop()

    if asyncio_config["debug"]:
        log.info("Enabling asyncio debug mode")
        loop.set_debug(True)

    return loop


async def _upgrade(config: util.config.Config, config_path: str) -> None:
    try:
        await util.config.upgrade(config, config_path)
    finally:
        # Python 3.14+: get the running loop instead of get_event_loop()
        asyncio.get_running_loop().stop()


def main(*, config_path: str = DEFAULT_CONFIG_PATH) -> None:
    """Main entry point for the default bot launcher."""

    log.info("Loading config")
    log.info(f"Config file path: {config_path}")
    
    config_file = Path(config_path)
    log.info(f"Resolved absolute path: {config_file.absolute()}")
    log.info(f"File exists: {config_file.exists()}")
    
    if not config_file.exists():
        log.error(f"Config file not found: {config_path}")
        log.error(f"Absolute path: {config_file.absolute()}")
        log.error(f"Current working directory: {Path.cwd()}")
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Absolute path: {config_file.absolute()}\n"
            f"Please create a config file or check the CONFIG_FILE environment variable.\n"
            f"See config.example.toml for reference."
        )
    
    log.info(f"Reading config from: {config_file.absolute()}")
    config_data = config_file.read_text()
    config: util.config.Config = tomlkit.loads(config_data)
    log.info(f"Config loaded successfully (version: {config.get('version', 'unknown')})")

    # Initialize Sentry reporting here to exempt config syntax errors and query
    # the user's report_errors value, defaulting to enabled if not specified
    if config["bot"].get("report_errors", True):
        log.info("Initializing Sentry error reporting")
        util.sentry.init()

    # Use preliminary loop for config upgrading
    # Python 3.14+: create new event loop instead of get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    aiorun.run(_upgrade(config, config_path), stop_on_unhandled_errors=True, loop=loop)
    loop.close()

    loop = setup_asyncio(config)

    # Start bot
    log.info("Initializing bot")
    aiorun.run(Bot.create_and_run(config, loop=loop), loop=loop)
