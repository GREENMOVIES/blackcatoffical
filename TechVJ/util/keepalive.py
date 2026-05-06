import asyncio
import logging
import aiohttp
import traceback
from info import *


async def ping_server():
    if not URL:
        logging.info("URL not provided, Keep-Alive service not started.")
        return
    
    logging.info(f"Keep-Alive service started. Pinging {URL} every {PING_INTERVAL} seconds.")
    sleep_time = PING_INTERVAL
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(URL) as resp:
                    logging.info("Pinged server with response: {}".format(resp.status))
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()
