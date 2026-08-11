# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, glob, importlib, logging, logging.config, pytz, asyncio, signal, traceback
from pyrogram.errors import (NetworkMigrate, PhoneMigrate, FloodWait,
    ServiceUnavailable, BadRequest, Unauthorized, ConnectionError as PyroConnectionError)
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

logger = logging.getLogger("recovery")
logger.setLevel(logging.INFO)

from pyrogram import Client, idle
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server
from plugins.clone import restart_bots

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)

RUNNING_TASKS = {}
IS_SHUTTING_DOWN = False


async def verify_mongodb_connection(max_retries=5):
    """Verify and reconnect to MongoDB with exponential backoff retries."""
    delays = [2, 5, 10, 15, 30]
    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to MongoDB (attempt {attempt + 1}/{max_retries})...")
            await db.db.command("ping")
            logger.info("Reconnection: MongoDB connected successfully.")
            return True
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}. Retrying in {delays[min(attempt, len(delays)-1)]}s...")
            if attempt == max_retries - 1:
                logger.critical("MongoDB error: Unable to connect after max retries.")
                raise e
            await asyncio.sleep(delays[min(attempt, len(delays)-1)])


# Errors that indicate a transient / recoverable connection problem
_RETRIABLE_ERRORS = (
    PyroConnectionError,
    NetworkMigrate,
    PhoneMigrate,
    FloodWait,
    ServiceUnavailable,
    TimeoutError,
    ConnectionError,
    OSError,
)

# Errors that are programming bugs — never retry, fail immediately
_FATAL_ERRORS = (
    AttributeError,
    ImportError,
    TypeError,
    SyntaxError,
    NameError,
)


async def start_bot_with_retry(client, max_retries=5):
    """Start Pyrogram client with retry only for transient connection failures.

    Guards against calling start() on an already-connected client.
    Fails immediately for programming errors (AttributeError, ImportError, etc.).
    """
    delays = [2, 5, 10, 15, 30]

    # Guard: never call start() if the client is already connected.
    if getattr(client, 'is_connected', False):
        logger.info("Telegram Client is already connected — skipping start().")
        return True

    for attempt in range(max_retries):
        try:
            logger.info(f"Starting Telegram Client (attempt {attempt + 1}/{max_retries})...")
            await client.start()
            logger.info("Telegram Client started successfully.")
            return True
        except _FATAL_ERRORS as e:
            # Programming errors — do not retry, propagate immediately
            logger.critical(
                f"Fatal programming error starting Telegram Client: {e}\n{traceback.format_exc()}"
            )
            raise
        except _RETRIABLE_ERRORS as e:
            wait = delays[min(attempt, len(delays) - 1)]
            logger.error(
                f"Transient connection error (attempt {attempt + 1}/{max_retries}): {e}. "
                f"Retrying in {wait}s..."
            )
            if attempt == max_retries - 1:
                logger.critical("Fatal: Failed to connect to Telegram API after max retries.")
                raise
            await asyncio.sleep(wait)
        except Exception as e:
            # Unknown exception — log and do not retry
            logger.critical(
                f"Unexpected error starting Telegram Client: {e}\n{traceback.format_exc()}"
            )
            raise


async def watchdog_monitor():
    """Watchdog monitor that periodically checks background tasks and restarts failed ones."""
    logger.info("Watchdog monitoring started.")
    while not IS_SHUTTING_DOWN:
        try:
            for task_name, task in list(RUNNING_TASKS.items()):
                if task.done():
                    exc = task.exception()
                    if exc:
                        logger.error(f"Watchdog detected failed task '{task_name}': {exc}\n{traceback.format_exc()}")
                        # Automatic Task Recovery
                        if task_name == "ping_server" and ON_HEROKU:
                            logger.info("Task restart: Resuming ping_server...")
                            RUNNING_TASKS["ping_server"] = asyncio.create_task(ping_server())
                        elif task_name == "catchup_indexing":
                            logger.info("Task restart: Resuming catchup_indexing...")
                            try:
                                from plugins.channel import catchup_channel_indexing
                                RUNNING_TASKS["catchup_indexing"] = asyncio.create_task(catchup_channel_indexing(TechVJBot))
                            except Exception as er:
                                logger.error(f"Failed to restart catchup_indexing: {er}")
                    else:
                        logger.info(f"Task '{task_name}' finished cleanly.")
        except Exception as e:
            logger.error(f"Watchdog error: {e}")
        await asyncio.sleep(15)


async def shutdown_bot():
    """Gracefully shutdown the bot, saving runtime state and stopping tasks."""
    global IS_SHUTTING_DOWN
    if IS_SHUTTING_DOWN:
        return
    IS_SHUTTING_DOWN = True
    logger.info("Shutdown: Initiating graceful shutdown...")
    logger.info("Saving runtime state before exit...")
    try:
        for name, task in list(RUNNING_TASKS.items()):
            if not task.done():
                logger.info(f"Stopping background task '{name}'...")
                task.cancel()
        logger.info("Stopping Telegram client...")
        await TechVJBot.stop()
        logger.info("Shutdown: Clean shutdown completed successfully.")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    finally:
        sys.exit(0)


def setup_signal_handlers():
    """Register SIGTERM and SIGINT signal handlers for graceful shutdown."""
    def _on_signal(sig, frame=None):
        signame = signal.Signals(sig).name
        logger.info(f"Received signal {signame}. Triggering graceful shutdown.")
        asyncio.create_task(shutdown_bot())

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            asyncio.get_event_loop().add_signal_handler(sig, lambda s=sig: _on_signal(s))
        except (NotImplementedError, AttributeError):
            signal.signal(sig, _on_signal)


async def start():
    logger.info("Startup: Initializing bot recovery system...")
    print('\nInitalizing Your Bot')

    # Step 1: Reconnect & Verify MongoDB Connection
    await verify_mongodb_connection()

    # Step 2: Start Telegram Client with Retries
    await start_bot_with_retry(TechVJBot)
    bot_info = await TechVJBot.get_me()
    await initialize_clients()

    # Step 3: Reload Plugins
    # Any plugin load failure stops the client cleanly and exits.
    try:
        for name in files:
            if name.endswith("__init__.py"):
                continue
            with open(name) as a:
                patt = Path(a.name)
                plugin_name = patt.stem.replace(".py", "")
                plugins_dir = Path(f"plugins/{plugin_name}.py")
                import_path = "plugins.{}".format(plugin_name)
                spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
                if spec and spec.loader:
                    load = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(load)
                    sys.modules["plugins." + plugin_name] = load
                    print("Tech VJ Imported => " + plugin_name)
    except Exception as e:
        logger.critical(
            f"Plugin loading failed for '{plugin_name}': {e}\n{traceback.format_exc()}"
        )
        # Stop client cleanly before exiting so the connection is released
        try:
            await TechVJBot.stop()
        except Exception:
            pass
        sys.exit(1)

    logger.info("Recovery: Plugins reloaded successfully.")

    # Step 4: Setup Background Tasks & Watchdog
    if ON_HEROKU:
        RUNNING_TASKS["ping_server"] = asyncio.create_task(ping_server())

    RUNNING_TASKS["watchdog"] = asyncio.create_task(watchdog_monitor())

    # Step 5: Restore State & Resume Indexing
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    logger.info("Resume indexing: Triggering channel indexing catch-up...")
    try:
        from plugins.channel import catchup_channel_indexing
        RUNNING_TASKS["catchup_indexing"] = asyncio.create_task(catchup_channel_indexing(TechVJBot))
    except Exception as e:
        logger.error(f"Failed to start catchup indexing task: {e}")

    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time_str = now.strftime("%H:%M:%S %p")
    try:
        await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time_str))
    except:
        print("Make Your Bot Admin In Log Channel With Full Rights")
    for ch in CHANNELS:
        try:
            k = await TechVJBot.send_message(chat_id=ch, text="**Bot Restarted**")
            await k.delete()
        except:
            print("Make Your Bot Admin In File Channels With Full Rights")
    try:
        k = await TechVJBot.send_message(chat_id=AUTH_CHANNEL, text="**Bot Restarted**")
        await k.delete()
    except:
        print("Make Your Bot Admin In Force Subscribe Channel With Full Rights")

    if CLONE_MODE == True:
        print("Restarting All Clone Bots.......")
        await restart_bots()
        print("Restarted All Clone Bots.")

    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, int(PORT)).start()

    setup_signal_handlers()
    logger.info("Startup complete. Bot is fully active and monitoring.")
    await idle()
    await shutdown_bot()


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
    except Exception as fatal_err:
        logging.critical(f"Fatal crash: {fatal_err}\n{traceback.format_exc()}")
        sys.exit(1)
