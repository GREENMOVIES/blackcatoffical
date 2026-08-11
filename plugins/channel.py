# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

import logging, asyncio
from pyrogram import Client, filters, enums
from info import CHANNELS
from database.ia_filterdb import (
    save_file, 
    clean_file_name, 
    unpack_new_file_id, 
    is_file_already_saved, 
    get_last_indexed_msg_id, 
    update_last_indexed_msg_id
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

async def process_channel_message(bot, message):
    """Extract metadata, check duplicates, save file, and update resume pointer."""
    try:
        if not message or message.empty:
            return

        media_type_enum = message.media
        if not media_type_enum or media_type_enum not in SUPPORTED_MEDIA:
            return

        media_type = media_type_enum.value
        logger.info(f"Detected media type: '{media_type}' for message_id: {message.id} in channel_id: {message.chat.id}")

        media = getattr(message, media_type, None)
        if not media:
            return

        # Photo in Pyrogram can be a list or Photo object
        if media_type == "photo" and isinstance(media, list):
            media = media[-1]

        # Extract metadata
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
            f"Extracted filename: '{file_name}' | file_id: {file_id[:15]}... | "
            f"file_unique_id: {file_unique_id} | size: {file_size} | mime: {mime_type} | "
            f"date: {message.date}"
        )

        unpacked_file_id = unpack_new_file_id(file_id)
        logger.info(f"Checking duplicate for file_id: {unpacked_file_id}, file_unique_id: {file_unique_id}")

        # Duplicate Check
        if await is_file_already_saved(unpacked_file_id, file_name):
            logger.info(f"Duplicate skipped: '{file_name}' (file_id: {unpacked_file_id})")
            await update_last_indexed_msg_id(message.chat.id, message.id)
            logger.info(f"Updated last indexed message to {message.id} for channel {message.chat.id}")
            return

        # Save File
        logger.info(f"Calling save_file() for '{file_name}'")
        saved, code = await save_file(media)

        if saved:
            logger.info(f"File indexed successfully: '{file_name}' (message_id: {message.id})")
        elif code == 0:
            logger.info(f"Duplicate skipped: '{file_name}'")
        else:
            logger.error(f"MongoDB error while saving '{file_name}' (code {code})")

        # Update resume pointer persistently
        await update_last_indexed_msg_id(message.chat.id, message.id)
        logger.info(f"Updated last indexed message to {message.id} for channel {message.chat.id}")

    except Exception as e:
        logger.exception(f"Indexing failed for message {getattr(message, 'id', 'unknown')}: {e}")


async def catchup_channel_indexing(bot):
    """Background catch-up scan for historical channel messages on startup."""
    for chat_id in CHANNELS:
        try:
            last_indexed = await get_last_indexed_msg_id(chat_id)
            logger.info(f"Resuming from message {last_indexed + 1} for channel {chat_id}")

            highest_id = 0
            async for m in bot.get_chat_history(chat_id, limit=1):
                highest_id = m.id

            if highest_id > last_indexed:
                logger.info(f"Bulk indexing started for channel {chat_id} from {last_indexed + 1} to {highest_id}")
                if hasattr(bot, 'iter_messages'):
                    async for message in bot.iter_messages(chat_id, highest_id, last_indexed):
                        if not message or message.empty:
                            continue
                        if message.media not in SUPPORTED_MEDIA:
                            await update_last_indexed_msg_id(chat_id, message.id)
                            continue
                        await process_channel_message(bot, message)
                logger.info(f"Bulk indexing completed for channel {chat_id}")
        except Exception as e:
            logger.exception(f"Bulk indexing failed for channel {chat_id}: {e}")


@Client.on_message(filters.chat(CHANNELS) & media_filter)
@Client.on_channel_post(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Triggered on new channel posts or chat updates in CHANNELS."""
    logger.info(f"Received channel post: {message.id} in channel_id: {message.chat.id}")
    
    # Auto-trigger catchup scan once per session
    if not getattr(temp, 'CATCHUP_STARTED', False):
        temp.CATCHUP_STARTED = True
        asyncio.create_task(catchup_channel_indexing(bot))

    await process_channel_message(bot, message)
