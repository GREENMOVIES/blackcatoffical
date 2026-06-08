import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS
from database.users_chats_db import db
from utils import broadcast_messages

SPB_STATE = {}
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@Client.on_message(filters.command("spb") & filters.private & filters.incoming)
async def spb_command(client, message):
    user_id = message.from_user.id
    logger.info(f"SPB command received | User ID: {user_id}")
    
    is_admin = user_id in ADMINS
    logger.info(f"SPB admin check | User ID: {user_id} | Result: {'PASSED' if is_admin else 'FAILED'}")
    
    if not is_admin:
        return await message.reply_text("❌ You are not authorized to use this command.")
    
    SPB_STATE[user_id] = {
        'state': 'WAITING_FOR_TITLE',
        'title': '',
        'details': '',
        'buttons_count': 0,
        'buttons': [],
        'current_button': 1
    }
    logger.info(f"SPB session started | User ID: {user_id}")
    await message.reply_text("📌 Send the movie title.")

async def check_spb_state(_, __, message):
    return message.from_user and message.from_user.id in SPB_STATE

spb_state_filter = filters.create(check_spb_state)

@Client.on_message(filters.private & filters.user(ADMINS) & filters.text & filters.incoming & ~filters.regex(r"^/") & spb_state_filter, group=-1)
async def spb_text_handler(client, message):
    user_id = message.from_user.id
    logger.info(f"SPB state handler triggered | User ID: {user_id}")
    # Stop propagation so pm_filter.py does not also handle this message
    message.stop_propagation()

    state_info = SPB_STATE[user_id]
    state = state_info['state']
    
    if state == 'WAITING_FOR_TITLE':
        state_info['title'] = message.text
        state_info['state'] = 'WAITING_FOR_DETAILS'
        await message.reply_text("Send the movie details/description.")
        
    elif state == 'WAITING_FOR_DETAILS':
        state_info['details'] = message.text
        state_info['state'] = 'WAITING_FOR_BUTTON_COUNT'
        await message.reply_text("How many buttons do you want to add?")
        
    elif state == 'WAITING_FOR_BUTTON_COUNT':
        try:
            count = int(message.text)
            if count < 1 or count > 10:
                await message.reply_text("Please send a valid number between 1 and 10.")
                return
        except ValueError:
            await message.reply_text("Please send a valid number between 1 and 10.")
            return
            
        state_info['buttons_count'] = count
        state_info['state'] = 'WAITING_FOR_BUTTON_NAME'
        await message.reply_text("Send name for Button 1")
        
    elif state == 'WAITING_FOR_BUTTON_NAME':
        state_info['current_button_name'] = message.text
        state_info['state'] = 'WAITING_FOR_BUTTON_URL'
        await message.reply_text(f"Send URL for Button {state_info['current_button']}")
        
    elif state == 'WAITING_FOR_BUTTON_URL':
        url = message.text
        if not url.startswith(("http://", "https://", "t.me/")):
            await message.reply_text("Please send a valid URL starting with http://, https://, or t.me/")
            return
            
        state_info['buttons'].append({
            'name': state_info['current_button_name'],
            'url': url
        })
        
        if state_info['current_button'] < state_info['buttons_count']:
            state_info['current_button'] += 1
            state_info['state'] = 'WAITING_FOR_BUTTON_NAME'
            await message.reply_text(f"Send name for Button {state_info['current_button']}")
        else:
            state_info['state'] = 'PREVIEW'
            await send_spb_preview(client, message.chat.id, user_id)

async def send_spb_preview(client, chat_id, user_id):
    state_info = SPB_STATE[user_id]
    
    text = f"🎬 NEW MOVIE ADDED\n\n📌 Title: {state_info['title']}\n\n📝 Details:\n{state_info['details']}"
    
    buttons = []
    for btn in state_info['buttons']:
        buttons.append([InlineKeyboardButton(text=btn['name'], url=btn['url'])])
        
    buttons.append([
        InlineKeyboardButton("✅ Send Broadcast", callback_data="spb_send"),
        InlineKeyboardButton("❌ Cancel", callback_data="spb_cancel")
    ])
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(chat_id, text, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex(r"^spb_(send|cancel)$") & filters.user(ADMINS))
async def spb_callback(client, query):
    user_id = query.from_user.id
    if user_id not in SPB_STATE:
        await query.answer("No active broadcast session found.", show_alert=True)
        return
        
    action = query.matches[0].group(1)
    
    if action == "cancel":
        del SPB_STATE[user_id]
        await query.message.edit_text("Broadcast cancelled.")
        return
        
    if action == "send":
        state_info = SPB_STATE[user_id]
        
        text = f"🎬 NEW MOVIE ADDED\n\n📌 Title: {state_info['title']}\n\n📝 Details:\n{state_info['details']}"
        buttons = []
        for btn in state_info['buttons']:
            buttons.append([InlineKeyboardButton(text=btn['name'], url=btn['url'])])
            
        reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
        
        del SPB_STATE[user_id]
        
        await query.message.edit_text("Broadcast started! You will receive a report once it's done.")
        
        # The broadcast message to be sent to users
        b_msg = await client.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=reply_markup
        )
        
        users = await db.get_all_users()
        
        success = 0
        failed = 0
        total = 0
        
        async def perform_broadcast():
            nonlocal success, failed, total
            async for user in users:
                total += 1
                pti, sh = await broadcast_messages(int(user['id']), b_msg)
                if pti:
                    success += 1
                elif sh == "Blocked":
                    failed += 1
                elif sh == "Deleted":
                    failed += 1
                elif sh == "Error":
                    failed += 1
                await asyncio.sleep(0.1) # small delay to prevent flood waits
            
            report = f"📢 Broadcast Completed\n\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total: {total}"
            await client.send_message(chat_id=user_id, text=report)
            
        asyncio.create_task(perform_broadcast())
