# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

# Clone Code Credit : YT - #blackcatoffical / TG - #blackcatoffical / GitHub - @VJBots

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

from pyrogram import Client, idle, filters
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

logger = logging.getLogger(__name__)

async def start():
    print('\n')
    print('Initalizing Your Bot')
    
    # START THE BOT CLIENT FIRST
    await TechVJBot.start()
    logging.info("✅ TechVJBot started successfully")
    print("✅ TechVJBot started successfully")
    
    bot_info = await TechVJBot.get_me()
    logging.info(f"✅ Bot logged in as: {bot_info.first_name} (@{bot_info.username})")
    print(f"✅ Bot logged in as: {bot_info.first_name} (@{bot_info.username})")
    
    # VERIFY HANDLERS ARE REGISTERED
    try:
        total_handlers = sum(len(h) for h in TechVJBot.dispatcher.handlers.values())
        logging.info(f"📊 Total handlers registered: {total_handlers}")
        print(f"📊 Total handlers registered: {total_handlers}")
        if total_handlers == 0:
            logging.warning("⚠️ WARNING: No handlers registered! Commands may not work.")
            print("⚠️ WARNING: No handlers registered! Commands may not work.")
    except Exception as e:
        logging.error(f"Error counting handlers: {e}")
    
    # DEBUG: LIST ALL LOADED PLUGINS
    print("\n📦 Loaded Plugins:")
    loaded_plugins = []
    for plugin_module in sys.modules:
        if 'plugins' in plugin_module and not plugin_module.startswith('pyrogram'):
            loaded_plugins.append(plugin_module)
            print(f"  ✓ {plugin_module}")
    
    if not loaded_plugins:
        logging.warning("⚠️ WARNING: No plugins loaded!")
        print("⚠️ WARNING: No plugins loaded!")
    
    print("\n✅ Plugins loaded via Pyrogram's plugins= parameter")
    
    await initialize_clients()
    
    # Get banned users/chats - now uses correct event loop
    try:
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        logging.info(f"✅ Loaded {len(b_users)} banned users and {len(b_chats)} banned chats")
    except Exception as e:
        print(f"⚠️ Failed to load banned users/chats: {e}")
        logging.warning(f"Failed to load banned users/chats: {e}")
        temp.BANNED_USERS = []
        temp.BANNED_CHATS = []
    
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    logging.info(script.LOGO)
    
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    
    try:
        await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
        logging.info("✅ Restart message sent to LOG_CHANNEL")
    except Exception as e:
        print("Make Your Bot Admin In Log Channel With Full Rights")
        logging.warning(f"Failed to send restart message to LOG_CHANNEL: {e}")
    
    for ch in CHANNELS:
        try:
            k = await TechVJBot.send_message(chat_id=ch, text="**Bot Restarted**")
            await k.delete()
        except Exception as e:
            print(f"Make Your Bot Admin In File Channels With Full Rights: {e}")
            logging.debug(f"Failed to send message to channel {ch}: {e}")
    
    try:
        k = await TechVJBot.send_message(chat_id=AUTH_CHANNEL, text="**Bot Restarted**")
        await k.delete()
        logging.info("✅ Restart notification sent to AUTH_CHANNEL")
    except Exception as e:
        print("Make Your Bot Admin In Force Subscribe Channel With Full Rights")
        logging.warning(f"Failed to send restart message to AUTH_CHANNEL: {e}")
    
    if CLONE_MODE == True:
        print("Restarting All Clone Bots.......")
        try:
            await restart_bots()
            print("✅ Restarted All Clone Bots.")
            logging.info("✅ Restarted All Clone Bots")
        except Exception as e:
            print(f"⚠️ Failed to restart clone bots: {e}")
            logging.error(f"Failed to restart clone bots: {e}")
    
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    logging.info(f"✅ Web server started on {bind_address}:{PORT}")
    print(f"✅ Web server started on {bind_address}:{PORT}")
    
    if URL:
        asyncio.create_task(ping_server())
        logging.info(f"✅ Keep-Alive service started for {URL}")
    
    print("\n" + "="*60)
    print("✅ BOT IS RUNNING SUCCESSFULLY!")
    print(f"✅ Bot: @{temp.U_NAME}")
    print(f"✅ Commands Ready: /start, /spb, /testdebug, etc.")
    print("="*60 + "\n")
    logging.info("✅ Bot is running successfully!")
    
    await idle()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
        print('Service Stopped Bye 👋')
