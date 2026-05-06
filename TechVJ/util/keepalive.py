import asyncio
import logging
import aiohttp
import traceback
from info import *


async def ping_server():
    if not URL:
        logging.info("URL not provided, Keep-Alive service not started.")
        return
    
    # Wait for the web server to fully start
    await asyncio.sleep(30)
    
    logging.info(f"Keep-Alive service started. Pinging {URL} every {PING_INTERVAL} seconds.")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    while True:
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10),
                headers=headers
            ) as session:
                async with session.get(URL) as resp:
                    if resp.status == 200:
                        logging.info(f"Keep-Alive: Successfully pinged {URL} (Status: {resp.status})")
                    else:
                        logging.warning(f"Keep-Alive: Pinged {URL} but got status {resp.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Keep-Alive: Connection error while pinging {URL}: {e}")
        except Exception:
            logging.error(f"Keep-Alive: Unexpected error:\n{traceback.format_exc()}")
        
        await asyncio.sleep(PING_INTERVAL)
