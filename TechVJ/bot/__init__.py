# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

from pyrogram import Client, types
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from aiohttp import web


class TechVJXBot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=150,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def set_self(self):
        temp.BOT = self
    
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while current <= limit:
            new_diff = min(200, (limit - current) + 1)
            if new_diff <= 0:
                return
            batch_ids = list(range(current, current + new_diff))
            try:
                messages = await self.get_messages(chat_id, batch_ids)
                for message in messages:
                    if message:
                        yield message
            except Exception as e:
                logger.error(f"Error fetching messages for chat {chat_id} batch {current}-{current+new_diff}: {e}")
            current += new_diff
      
TechVJBot = TechVJXBot()

multi_clients = {}
work_loads = {}
