# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

import datetime
import time
import asyncio
import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.users_chats_db import db
from info import ADMINS
from utils import broadcast_messages, broadcast_messages_group

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ─────────────────────────────────────────────────────────────────────────────
# SPB (Smart Post Broadcast) — in-memory wizard state per admin
# ─────────────────────────────────────────────────────────────────────────────
SPB_STATE = {}


async def _spb_state_check(_, __, message):
    try:
        return bool(message.from_user and message.from_user.id in SPB_STATE)
    except Exception:
        return False


spb_state_filter = filters.create(_spb_state_check)


# ── /spb command — start wizard ───────────────────────────────────────────────
@Client.on_message(filters.command("spb") & filters.user(ADMINS))
async def spb_start(bot, message):
    user_id = message.from_user.id
    logger.info(f"SPB command received | User ID: {user_id}")

    SPB_STATE.pop(user_id, None)

    await message.reply_text(
        "✅ **SPB wizard started.**\n\n"
        "📌 **Step 1 of 4:** Send the **movie title**."
    )

    SPB_STATE[user_id] = {
        "state": "WAITING_FOR_TITLE",
        "title": "",
        "details": "",
        "buttons_count": 0,
        "buttons": [],
        "current_button": 1,
        "current_button_name": "",
    }
    logger.info(f"SPB session opened | User ID: {user_id}")


# ── Wizard step handler ───────────────────────────────────────────────────────
@Client.on_message(
    filters.user(ADMINS)
    & filters.text
    & filters.private
    & ~filters.regex(r"^/")
    & spb_state_filter
)
async def spb_steps(bot, message):
    user_id = message.from_user.id

    if user_id not in SPB_STATE:
        return

    info = SPB_STATE[user_id]
    state = info["state"]
    logger.info(f"SPB step | User ID: {user_id} | State: {state}")

    if state == "WAITING_FOR_TITLE":
        info["title"] = message.text.strip()
        info["state"] = "WAITING_FOR_DETAILS"
        await message.reply_text(
            "✅ Title saved.\n\n📝 **Step 2 of 4:** Send the **movie details / description**."
        )

    elif state == "WAITING_FOR_DETAILS":
        info["details"] = message.text.strip()
        info["state"] = "WAITING_FOR_BUTTON_COUNT"
        await message.reply_text(
            "✅ Details saved.\n\n🔢 **Step 3 of 4:** How many **buttons** to add? (1–10)"
        )

    elif state == "WAITING_FOR_BUTTON_COUNT":
        try:
            count = int(message.text.strip())
            if not 1 <= count <= 10:
                raise ValueError
        except ValueError:
            return await message.reply_text("⚠️ Send a number between **1** and **10**.")
        info["buttons_count"] = count
        info["current_button"] = 1
        info["state"] = "WAITING_FOR_BUTTON_NAME"
        await message.reply_text("🔘 **Step 4 of 4:** Send the **name** for Button 1.")

    elif state == "WAITING_FOR_BUTTON_NAME":
        info["current_button_name"] = message.text.strip()
        info["state"] = "WAITING_FOR_BUTTON_URL"
        await message.reply_text(
            f"🔗 Send the **URL** for Button {info['current_button']}.\n"
            "_(Must start with http://, https://, or t.me/)_"
        )

    elif state == "WAITING_FOR_BUTTON_URL":
        url = message.text.strip()
        if not url.startswith(("http://", "https://", "t.me/")):
            return await message.reply_text(
                "⚠️ Invalid URL. Must start with `http://`, `https://`, or `t.me/`"
            )
        info["buttons"].append({"name": info["current_button_name"], "url": url})

        if info["current_button"] < info["buttons_count"]:
            info["current_button"] += 1
            info["state"] = "WAITING_FOR_BUTTON_NAME"
            await message.reply_text(
                f"🔘 Send the **name** for Button {info['current_button']}."
            )
        else:
            info["state"] = "PREVIEW"
            await _spb_show_preview(bot, message.chat.id, user_id)


# ── Preview helper ────────────────────────────────────────────────────────────
async def _spb_show_preview(bot, chat_id, user_id):
    info = SPB_STATE.get(user_id)
    if not info:
        return
    text = (
        f"🎬 **NEW MOVIE ADDED**\n\n"
        f"📌 **Title:** {info['title']}\n\n"
        f"📝 **Details:**\n{info['details']}"
    )
    buttons = [[InlineKeyboardButton(b["name"], url=b["url"])] for b in info["buttons"]]
    buttons.append([
        InlineKeyboardButton("✅ Send Broadcast", callback_data="spb_send"),
        InlineKeyboardButton("❌ Cancel",         callback_data="spb_cancel"),
    ])
    await bot.send_message(
        chat_id,
        f"**📋 Preview:**\n\n{text}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ── Callback: confirm send / cancel ──────────────────────────────────────────
@Client.on_callback_query(filters.regex(r"^spb_(send|cancel)$") & filters.user(ADMINS))
async def spb_callback(bot, query):
    user_id = query.from_user.id
    action  = query.matches[0].group(1)

    if user_id not in SPB_STATE:
        return await query.answer("No active session. Use /spb to start.", show_alert=True)

    if action == "cancel":
        SPB_STATE.pop(user_id, None)
        return await query.message.edit_text("🚫 Broadcast **cancelled**.")

    # ── send ──
    info = SPB_STATE.pop(user_id, None)
    if not info:
        return await query.answer("Session expired. Use /spb again.", show_alert=True)

    text = (
        f"🎬 **NEW MOVIE ADDED**\n\n"
        f"📌 **Title:** {info['title']}\n\n"
        f"📝 **Details:**\n{info['details']}"
    )
    buttons = [[InlineKeyboardButton(b["name"], url=b["url"])] for b in info["buttons"]]
    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

    await query.message.edit_text("📢 **Broadcast started!** You'll receive a report when done.")

    b_msg = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)

    users   = await db.get_all_users()
    success = failed = total = 0

    async def _run():
        nonlocal success, failed, total
        async for user in users:
            total += 1
            try:
                pti, sh = await broadcast_messages(int(user["id"]), b_msg)
                if pti:
                    success += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.05)
        report = (
            f"📢 **Broadcast Completed**\n\n"
            f"✅ Success: {success}\n"
            f"❌ Failed: {failed}\n"
            f"👥 Total: {total}"
        )
        try:
            await bot.send_message(chat_id=user_id, text=report)
        except Exception:
            pass

    asyncio.create_task(_run())


# ─────────────────────────────────────────────────────────────────────────────
# Normal user broadcast
# ─────────────────────────────────────────────────────────────────────────────
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def pm_broadcast(bot, message):
    b_msg = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Broadcast Message")
    try:
        users = await db.get_all_users()
        sts = await message.reply_text("Broadcasting your messages...")
        start_time = time.time()
        total_users = await db.total_users_count()
        done = blocked = deleted = failed = success = 0

        async for user in users:
            if "id" in user:
                pti, sh = await broadcast_messages(int(user["id"]), b_msg)
                if pti:
                    success += 1
                elif pti is False:
                    if sh == "Blocked":
                        blocked += 1
                    elif sh == "Deleted":
                        deleted += 1
                    elif sh == "Error":
                        failed += 1
            else:
                failed += 1
            done += 1
            if not done % 20:
                await sts.edit(
                    f"Broadcast in progress:\n\n"
                    f"Total Users {total_users}\n"
                    f"Completed: {done} / {total_users}\n"
                    f"Success: {success}\nBlocked: {blocked}\nDeleted: {deleted}"
                )

        time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
        await sts.edit(
            f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\n"
            f"Total Users: {total_users}\n"
            f"Completed: {done} / {total_users}\n"
            f"Success: {success}\nBlocked: {blocked}\nDeleted: {deleted}"
        )
    except Exception as e:
        print(f"error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Group broadcast
# ─────────────────────────────────────────────────────────────────────────────
@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS))
async def broadcast_group(bot, message):
    b_msg = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Broadcast Message")
    groups = await db.get_all_chats()
    sts = await message.reply_text(text="Broadcasting your messages To Groups...")
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = failed = success = 0

    async for group in groups:
        pti, sh = await broadcast_messages_group(int(group["id"]), b_msg)
        if pti:
            success += 1
        elif sh == "Error":
            failed += 1
        done += 1
        if not done % 20:
            await sts.edit(
                f"Broadcast in progress:\n\n"
                f"Total Groups {total_groups}\n"
                f"Completed: {done} / {total_groups}\n"
                f"Success: {success}"
            )

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(
        f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\n"
        f"Total Groups {total_groups}\n"
        f"Completed: {done} / {total_groups}\n"
        f"Success: {success}"
    )
