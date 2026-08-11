# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

import logging, asyncio, traceback
from pyrogram import Client, filters, enums
from pyrogram.errors import RPCError, FloodWait
from info import CHANNELS, API_ID, API_HASH, SESSION_STRING, USER_SESSION_STRING
from database.ia_filterdb import (
    save_file, 
    clean_file_name, 
    unpack_new_file_id, 
    is_file_already_saved, 
    get_last_indexed_msg_id, 
    update_last_indexed_msg_id,
    retry_mongo_op
)
from utils import temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUPPORTED_MEDIA = [
    enums.MessageMediaType.DOCUMENT,
    enums.MessageMediaType.VIDEO,
    enums.MessageMediaType.AUDIO,
    enums.MessageMediaType.ANIMATION,
    enums.MessageMediaType.VOICE,
    enums.MessageMediaType.VIDEO_NOTE,
    enums.MessageMediaType.PHOTO
]

media_filter = (
    filters.document | filters.video | filters.audio | 
    filters.animation | filters.voice | filters.video_note | filters.photo
)

# User Session Client Initialization if SESSION_STRING is configured
UserClient = None
sess_str = SESSION_STRING or USER_SESSION_STRING
if sess_str and API_ID and API_HASH:
    try:
        UserClient = Client(
            name="user_session_indexer",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=sess_str
        )
        logger.info("User session client created.")
    except Exception as e:
        logger.error(f"Telegram error creating user session client: {e}\n{traceback.format_exc()}")


async def process_channel_message(client, message):
    """Extract metadata, check duplicates, save file, and update resume pointer."""
    try:
        if not message or message.empty:
            return

        media_type_enum = message.media
        if not media_type_enum or media_type_enum not in SUPPORTED_MEDIA:
            return

        media_type = media_type_enum.value
        logger.info(f"Processing message: {message.id} | Detected media type: '{media_type}' in channel_id: {message.chat.id}")

        media = getattr(message, media_type, None)
        if not media:
            return

        # Photo in Pyrogram can be a list or Photo object
        if media_type == "photo" and isinstance(media, list):
            media = media[-1]

        file_id = getattr(media, 'file_id', None)
        file_unique_id = getattr(media, 'file_unique_id', None)
        if not file_id:
            return

        file_size = getattr(media, 'file_size', 0)
        mime_type = getattr(media, 'mime_type', 'unknown')
        caption = message.caption or ""
        media.caption = caption

        raw_file_name = (
            getattr(media, 'file_name', None) or 
            getattr(media, 'title', None) or 
            (caption.split('\n')[0] if caption else None) or 
            f"{media_type}_{message.id}"
        )
        file_name = clean_file_name(raw_file_name)
        if not getattr(media, 'file_name', None) and not getattr(media, 'title', None):
            setattr(media, 'file_name', raw_file_name)

        logger.info(
            f"Extracted metadata: file_name='{file_name}', file_id='{file_id[:15]}...', "
            f"file_unique_id='{file_unique_id}', size={file_size}, mime='{mime_type}', "
            f"date='{message.date}', media_type='{media_type}'"
        )

        unpacked_file_id = unpack_new_file_id(file_id)
        logger.info(f"Checking duplicate for file_id: {unpacked_file_id}, file_unique_id: {file_unique_id}")

        # Duplicate Check
        try:
            is_duplicate = await retry_mongo_op(lambda: is_file_already_saved(unpacked_file_id, file_name))
        except Exception as e:
            logger.error(f"MongoDB error checking duplicate: {e}\n{traceback.format_exc()}")
            is_duplicate = False

        if is_duplicate:
            logger.info(f"Duplicate skipped: {file_name} (file_id: {unpacked_file_id})")
            await update_last_indexed_msg_id(message.chat.id, message.id)
            logger.info(f"Resume updated to message_id: {message.id} for channel {message.chat.id}")
            return

        # Save File
        logger.info(f"save_file() called for '{file_name}'")
        try:
            saved, code = await retry_mongo_op(lambda: save_file(media))
        except Exception as e:
            logger.error(f"MongoDB error saving file '{file_name}': {e}\n{traceback.format_exc()}")
            saved, code = False, 2

        if saved:
            logger.info(f"File indexed: '{file_name}' (message_id: {message.id})")
        elif code == 0:
            logger.info(f"Duplicate skipped: '{file_name}'")
        else:
            logger.error(f"MongoDB error saving '{file_name}' (code {code})")

        # Update resume pointer persistently
        await update_last_indexed_msg_id(message.chat.id, message.id)
        logger.info(f"Resume updated to message_id: {message.id} for channel {message.chat.id}")

    except Exception as e:
        logger.error(f"Indexing failed for message {getattr(message, 'id', 'unknown')}: {e}\n{traceback.format_exc()}")


async def catchup_channel_indexing(client):
    """Historical bulk catch-up scanner for channels."""
    for chat_id in CHANNELS:
        try:
            last_indexed = await get_last_indexed_msg_id(chat_id)
            logger.info(f"Resuming from message {last_indexed + 1} for channel {chat_id}")

            highest_id = 0
            async for m in client.get_chat_history(chat_id, limit=1):
                highest_id = m.id

            if highest_id > last_indexed:
                logger.info(f"Bulk indexing started for channel {chat_id} from {last_indexed + 1} to {highest_id}")
                if hasattr(client, 'iter_messages'):
                    async for message in client.iter_messages(chat_id, highest_id, last_indexed):
                        if not message or message.empty:
                            continue
                        if message.media not in SUPPORTED_MEDIA:
                            await update_last_indexed_msg_id(chat_id, message.id)
                            continue
                        await process_channel_message(client, message)
                logger.info(f"Bulk indexing completed for channel {chat_id}")
        except RPCError as e:
            logger.error(f"Telegram error in bulk indexing for channel {chat_id}: {e}\n{traceback.format_exc()}")
        except Exception as e:
            logger.error(f"Indexing failed in bulk indexing for channel {chat_id}: {e}\n{traceback.format_exc()}")


async def init_user_session():
    """Start User Session client, verify session/channel access, catch up history, and enable live indexing."""
    if not UserClient:
        return
    try:
        # Guard: only call start() when not already connected
        if not getattr(UserClient, 'is_connected', False):
            logger.info("Starting User Session client...")
            await UserClient.start()
        else:
            logger.info("User Session client already connected — skipping start().")
        user_me = await UserClient.get_me()
        logger.info(f"User session started successfully as @{user_me.username or user_me.id}")

        for chat_id in CHANNELS:
            try:
                chat = await UserClient.get_chat(chat_id)
                logger.info(f"Connected to channel: {chat.title} ({chat_id})")
            except Exception as e:
                logger.error(f"Telegram error verifying channel access for {chat_id}: {e}\n{traceback.format_exc()}")

        # Register live event handler on UserClient
        @UserClient.on_message(filters.chat(CHANNELS) & media_filter)
        async def user_live_handler(client, message):
            logger.info(f"Received channel post: {message.id} via User Session in channel_id: {message.chat.id}")
            await process_channel_message(client, message)

        logger.info("Live indexing enabled for User Session client.")

        # Run historical bulk catch-up
        await catchup_channel_indexing(UserClient)

    except Exception as e:
        logger.error(f"Telegram error in User Session initialization: {e}\n{traceback.format_exc()}")


# Bot Client Live Event Handlers
@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Triggered on new channel posts or chat updates in CHANNELS."""
    logger.info(f"Received channel post: {message.id} in channel_id: {message.chat.id}")
    
    # Auto-trigger user session / catchup scan once per session
    if not getattr(temp, 'CATCHUP_STARTED', False):
        temp.CATCHUP_STARTED = True
        if UserClient:
            asyncio.create_task(init_user_session())
        else:
            asyncio.create_task(catchup_channel_indexing(bot))

    await process_channel_message(bot, message)
