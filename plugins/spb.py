print("🚀 SPB MODULE LOADED")
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS
from database.users_chats_db import db
from utils import broadcast_messages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# In-memory state store for the SPB wizard
SPB_STATE = {}

# ─── Admin helper ────────────────────────────────────────────────────────────
# ADMINS may contain ints OR strings depending on how id_pattern matched.
# Always compare as int to be safe.
def _is_admin(user_id: int) -> bool:
    try:
        admins_as_int = [int(a) for a in ADMINS]
        return int(user_id) in admins_as_int
    except Exception:
        return False

# ─── State filter ────────────────────────────────────────────────────────────
async def _check_spb_state(_, __, message) -> bool:
    try:
        return bool(message.from_user and message.from_user.id in SPB_STATE)
    except Exception:
        return False

spb_state_filter = filters.create(_check_spb_state)

# ─── /spb command handler ────────────────────────────────────────────────────
@Client.on_message(filters.command("spb") & filters.private & filters.incoming)
async def spb_command(client, message):
    try:
        if not message.from_user:
            logger.warning("SPB command received from anonymous sender — ignoring.")
            return

        user_id = message.from_user.id
        logger.info(f"SPB command received | User ID: {user_id}")

        is_admin = _is_admin(user_id)
        logger.info(
            f"SPB admin check | User ID: {user_id} | ADMINS list: {ADMINS} | Is Admin: {is_admin}"
        )

        if not is_admin:
            logger.info(f"SPB blocked — user {user_id} is not an admin.")
            return await message.reply_text(
                "❌ You are not authorized to use this command.\n\n"
                f"Your ID: <code>{user_id}</code>",
                parse_mode="html"
            )

        # Clear any existing session for this admin
        SPB_STATE.pop(user_id, None)

        # Immediate acknowledgement — always send this first
        await message.reply_text(
            "✅ <b>SPB wizard started.</b>\n\n"
            "📌 <b>Step 1/4:</b> Send the <b>movie title</b>.",
            parse_mode="html"
        )

        # Initialise wizard state after replying
        SPB_STATE[user_id] = {
            "state": "WAITING_FOR_TITLE",
            "title": "",
            "details": "",
            "buttons_count": 0,
            "buttons": [],
            "current_button": 1,
            "current_button_name": "",
        }
        logger.info(f"SPB session initialised | User ID: {user_id}")

    except Exception as exc:
        logger.exception(f"SPB command handler crashed | User ID: {getattr(message.from_user, 'id', '?')} | Error: {exc}")
        try:
            await message.reply_text("⚠️ An internal error occurred. Please try again.")
        except Exception:
            pass


# ─── Step-by-step text handler ───────────────────────────────────────────────
@Client.on_message(
    filters.private
    & filters.text
    & filters.incoming
    & ~filters.regex(r"^[/]")
    & spb_state_filter
)
async def spb_text_handler(client, message):
    try:
        if not message.from_user:
            return

        user_id = message.from_user.id

        # Guard: only process if user is admin AND has an active SPB session
        if not _is_admin(user_id):
            return
        if user_id not in SPB_STATE:
            return

        logger.info(f"SPB text handler triggered | User ID: {user_id}")

        state_info = SPB_STATE[user_id]
        state = state_info["state"]

        if state == "WAITING_FOR_TITLE":
            state_info["title"] = message.text.strip()
            state_info["state"] = "WAITING_FOR_DETAILS"
            await message.reply_text(
                "✅ Title saved.\n\n"
                "📝 <b>Step 2/4:</b> Send the <b>movie details / description</b>.",
                parse_mode="html"
            )

        elif state == "WAITING_FOR_DETAILS":
            state_info["details"] = message.text.strip()
            state_info["state"] = "WAITING_FOR_BUTTON_COUNT"
            await message.reply_text(
                "✅ Details saved.\n\n"
                "🔢 <b>Step 3/4:</b> How many <b>inline buttons</b> do you want to add? (1–10)",
                parse_mode="html"
            )

        elif state == "WAITING_FOR_BUTTON_COUNT":
            try:
                count = int(message.text.strip())
                if not (1 <= count <= 10):
                    raise ValueError
            except ValueError:
                return await message.reply_text("⚠️ Please send a valid number between <b>1</b> and <b>10</b>.", parse_mode="html")

            state_info["buttons_count"] = count
            state_info["state"] = "WAITING_FOR_BUTTON_NAME"
            state_info["current_button"] = 1
            await message.reply_text(
                f"🔘 <b>Step 4/{count + 3}:</b> Send the <b>name</b> for Button 1.",
                parse_mode="html"
            )

        elif state == "WAITING_FOR_BUTTON_NAME":
            state_info["current_button_name"] = message.text.strip()
            state_info["state"] = "WAITING_FOR_BUTTON_URL"
            await message.reply_text(
                f"🔗 Send the <b>URL</b> for Button {state_info['current_button']}.\n"
                "<i>Must start with http://, https://, or t.me/</i>",
                parse_mode="html"
            )

        elif state == "WAITING_FOR_BUTTON_URL":
            url = message.text.strip()
            if not url.startswith(("http://", "https://", "t.me/")):
                return await message.reply_text(
                    "⚠️ Invalid URL. Must start with <code>http://</code>, <code>https://</code>, or <code>t.me/</code>",
                    parse_mode="html"
                )

            state_info["buttons"].append({
                "name": state_info["current_button_name"],
                "url": url
            })

            if state_info["current_button"] < state_info["buttons_count"]:
                state_info["current_button"] += 1
                state_info["state"] = "WAITING_FOR_BUTTON_NAME"
                await message.reply_text(
                    f"🔘 Send the <b>name</b> for Button {state_info['current_button']}.",
                    parse_mode="html"
                )
            else:
                state_info["state"] = "PREVIEW"
                await _send_spb_preview(client, message.chat.id, user_id)

    except Exception as exc:
        logger.exception(f"SPB text handler crashed | User ID: {getattr(message.from_user, 'id', '?')} | Error: {exc}")
        try:
            await message.reply_text("⚠️ An internal error occurred in the wizard. Please restart with /spb.")
        except Exception:
            pass


# ─── Preview builder ──────────────────────────────────────────────────────────
async def _send_spb_preview(client, chat_id: int, user_id: int):
    try:
        state_info = SPB_STATE[user_id]
        text = (
            "🎬 <b>NEW MOVIE ADDED</b>\n\n"
            f"📌 <b>Title:</b> {state_info['title']}\n\n"
            f"📝 <b>Details:</b>\n{state_info['details']}"
        )
        buttons = [
            [InlineKeyboardButton(text=btn["name"], url=btn["url"])]
            for btn in state_info["buttons"]
        ]
        buttons.append([
            InlineKeyboardButton("✅ Send Broadcast", callback_data="spb_send"),
            InlineKeyboardButton("❌ Cancel", callback_data="spb_cancel"),
        ])
        await client.send_message(
            chat_id,
            f"<b>📋 Preview:</b>\n\n{text}",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="html"
        )
    except Exception as exc:
        logger.exception(f"SPB preview builder crashed | User ID: {user_id} | Error: {exc}")
        SPB_STATE.pop(user_id, None)
        try:
            await client.send_message(chat_id, "⚠️ Failed to build preview. Please restart with /spb.")
        except Exception:
            pass


# ─── Callback: Send or Cancel ─────────────────────────────────────────────────
@Client.on_callback_query(filters.regex(r"^spb_(send|cancel)$"))
async def spb_callback(client, query):
    try:
        user_id = query.from_user.id

        if not _is_admin(user_id):
            return await query.answer("❌ Not authorized.", show_alert=True)

        if user_id not in SPB_STATE:
            return await query.answer("⚠️ No active broadcast session found. Please restart with /spb.", show_alert=True)

        action = query.matches[0].group(1)

        if action == "cancel":
            SPB_STATE.pop(user_id, None)
            return await query.message.edit_text("🚫 Broadcast <b>cancelled</b>.", parse_mode="html")

        if action == "send":
            state_info = SPB_STATE.pop(user_id, None)
            if not state_info:
                return await query.answer("Session expired. Please restart with /spb.", show_alert=True)

            text = (
                "🎬 <b>NEW MOVIE ADDED</b>\n\n"
                f"📌 <b>Title:</b> {state_info['title']}\n\n"
                f"📝 <b>Details:</b>\n{state_info['details']}"
            )
            buttons = [
                [InlineKeyboardButton(text=btn["name"], url=btn["url"])]
                for btn in state_info["buttons"]
            ]
            reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

            await query.message.edit_text(
                "📢 <b>Broadcast started!</b>\nYou will receive a report once it's done.",
                parse_mode="html"
            )

            # Send preview copy to admin first
            b_msg = await client.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="html"
            )

            users = await db.get_all_users()
            success = 0
            failed = 0
            total = 0

            async def _perform_broadcast():
                nonlocal success, failed, total
                try:
                    async for user in users:
                        total += 1
                        try:
                            pti, sh = await broadcast_messages(int(user["id"]), b_msg)
                            if pti:
                                success += 1
                            else:
                                failed += 1
                        except Exception as e:
                            logger.warning(f"Broadcast failed for user {user.get('id')}: {e}")
                            failed += 1
                        await asyncio.sleep(0.05)
                except Exception as exc:
                    logger.exception(f"Broadcast loop crashed: {exc}")
                finally:
                    report = (
                        f"📢 <b>Broadcast Completed</b>\n\n"
                        f"✅ Success: <b>{success}</b>\n"
                        f"❌ Failed: <b>{failed}</b>\n"
                        f"👥 Total: <b>{total}</b>"
                    )
                    try:
                        await client.send_message(chat_id=user_id, text=report, parse_mode="html")
                    except Exception:
                        pass

            asyncio.create_task(_perform_broadcast())

    except Exception as exc:
        logger.exception(f"SPB callback crashed | Error: {exc}")
        try:
            await query.answer("⚠️ An error occurred.", show_alert=True)
        except Exception:
            pass
