import asyncio
import logging
import aiohttp
import traceback
from info import *

logger = logging.getLogger(__name__)

async def ping_server():
    if not URL:
        logging.info("URL not provided, Keep-Alive service not started.")
        return
    
    # Ping interval: 60s (1 minute) to ensure Koyeb/Heroku container stays awake
    interval = max(15, min(PING_INTERVAL, 60))

    clean_url = URL.strip().rstrip('/')
    ext_url = clean_url if clean_url.endswith('/ping') else f"{clean_url}/ping"
    logging.info(f"Keep-Alive service started. Pinging every {interval} seconds. External: {ext_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    local_url = f"http://127.0.0.1:{PORT}/ping"

    # Wait for the web server to fully start
    await asyncio.sleep(15)

    while True:
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=15),
                headers=headers
            ) as session:
                # 1. Ping Local Endpoint (verifies local web server health)
                try:
                    async with session.get(local_url) as local_resp:
                        if local_resp.status == 200:
                            logging.info(f"Keep-Alive Local: Successfully pinged {local_url} (Status: 200)")
                        else:
                            logging.warning(f"Keep-Alive Local: Pinged {local_url} got status {local_resp.status}")
                except Exception as le:
                    logging.error(f"Keep-Alive Local Error pinging {local_url}: {le}")

                # 2. Ping External/Public Koyeb URL (verifies external edge routing)
                try:
                    async with session.get(ext_url, allow_redirects=True) as resp:
                        if resp.status == 200:
                            logging.info("Keep-Alive External: Success")
                        else:
                            logging.warning(f"Keep-Alive External: Failed ({resp.status})")
                except Exception as ee:
                    logging.error(f"Keep-Alive External: Failed ({ee})")

        except Exception as e:
            logging.error(f"Keep-Alive Loop Error: {e}\n{traceback.format_exc()}")
        
        await asyncio.sleep(interval)
