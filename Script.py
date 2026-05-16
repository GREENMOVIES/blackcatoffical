class script(object):
    START_TXT = """<b><blockquote>ʜᴇʟʟᴏ {} 👋,</blockquote>
    🐈‍⬛ Welcome to BLACK CAT 🖤

✨ The Ultimate Advanced Auto Filter Bot ✨

⚡ Fast • Smart • Powerful • Reliable

🔎 Instantly find files in your group
🎬 Movies, Series, Anime & More
🚀 Lightning-fast auto filtering
🛡 Smooth and stable performance
💬 Easy to use for everyone

📌 Add BLACK CAT to your group and enjoy a smarter searching experience.

🖤 BLACK CAT — Silent, Fast & Deadly Accurate.
<blockquote>⍟───[  @greenmoviebot]───⍟</blockquote></b>"""

    CLONE_START_TXT = """<b><blockquote>ʜᴇʟʟᴏ {}, ᴍʏ ɴᴀᴍᴇ <a href=https://t.me/{}>{}</a></blockquote>
    
ɪ ᴀᴍ ᴀᴅᴠᴀɴᴄᴇ ᴀɴᴅ ᴘᴏᴡᴇʀғᴜʟʟ ᴀᴜᴛᴏғɪʟᴛᴇʀ ʙᴏᴛ ᴡɪᴛʜ ᴀᴍᴀᴢɪɴɢ ғᴇᴀᴛᴜʀᴇs ᴊᴜsᴛ ᴛʏᴘᴇ ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜᴇɴ sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ 💘
⚡ Fast • Smart • Powerful • Reliable

🔎 Instantly find files in your group
🎬 Movies, Series, Anime & More
🚀 Lightning-fast auto filtering
🛡 Smooth and stable performance
💬 Easy to use for everyone</b>"""
    
    HELP_TXT = """<b>ʜᴇʟʟᴏ {}
ʜᴇʀᴇ ɪs ᴀʟʟ ᴍʏ ᴜsᴇғᴜʟʟ ғᴇᴀᴛᴜʀᴇs.</b>"""

    ABOUT_TXT = """<b><blockquote>⍟───[ ᴍʏ ᴅᴇᴛᴀɪʟꜱ ]───⍟</blockquote>
    
‣ ᴍʏ ɴᴀᴍᴇ : <a href=https://t.me/{}>{}</a>
‣ ᴍʏ ʙᴇsᴛ ғʀɪᴇɴᴅ : <a href='tg://settings'>ᴛʜɪs ᴘᴇʀsᴏɴ</a> 
‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/edisonwriter'>ᴇᴅɪsᴏɴ</a> 
‣ ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ</a> 
‣ ʟᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/download/releases/3.0/'>ᴘʏᴛʜᴏɴ 3</a> 
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a> 
‣ ʙᴏᴛ sᴇʀᴠᴇʀ : <a href='https://heroku.com'>ʜᴇʀᴏᴋᴜ</a> 
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ2.7.1 [sᴛᴀʙʟᴇ]></b>"""

    CLONE_ABOUT_TXT = """<b><blockquote>⍟───[ ᴍʏ ᴀʙᴏᴜᴛ ]───⍟</blockquote>
    
‣ ᴍʏ ɴᴀᴍᴇ : {}
‣ ᴍʏ ʙᴇsᴛ ғʀɪᴇɴᴅ : <a href='tg://settings'>ᴛʜɪs ᴘᴇʀsᴏɴ</a> 
‣ ᴄʟᴏɴᴇᴅ ғʀᴏᴍ : <a href=https://t.me/{}>{}</a>
‣ ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ</a> 
‣ ʟᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/download/releases/3.0/'>ᴘʏᴛʜᴏɴ 3</a> 
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a> 
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ2.7.1 [sᴛᴀʙʟᴇ]></b>"""

    CLONE_TXT = """<b>🌟 <u>CLONE MODE</u>

- Yᴏᴜ Cʀᴇᴀᴛᴇ Yᴏᴜʀ Oᴡɴ Cʟᴏɴᴇ Bᴏᴛ Bʏ /clone Cᴏᴍᴍᴀɴᴅ 
- Yᴏᴜ Cᴀɴ Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Yᴏᴜʀ Cʟᴏɴᴇ Bᴏᴛs
- Aɴᴅ Mɪʟʟɪᴏɴ Oғ Fɪʟᴇs Iɴᴅᴇx Aʟʀᴇᴀᴅʏ Nᴏ Nᴇᴇᴅ Tᴏ Aᴅᴅ Aɴʏ Fɪʟᴇ

👨‍💻 Cᴏᴍᴍᴀɴᴅ : /clone</b>"""

    SUBSCRIPTION_TXT = """
<b>ʀᴇғᴇʀʀᴇ ʏᴏᴜʀ ʟɪɴᴋ ᴛᴏ ʏᴏᴜʀ ғʀɪᴇɴᴅs, ғᴀᴍɪʟʏ, ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ɢʀᴏᴜᴘ ᴛᴏ ɢᴇᴛ ғʀᴇᴇ ᴘʀᴇᴍɪᴜᴍ ғᴏʀ {}

ʀᴇғᴇʀᴀʟ ʟɪɴᴋ - https://telegram.me/{}?start=VJ-{}

ɪғ {} ᴜɴɪǫᴜᴇ ᴜsᴇʀ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜ ʏᴏᴜʀ ʀᴇғᴇʀᴀʟ ʟɪɴᴋ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴅᴅᴇᴅ ɪɴ ᴘʀᴇᴍɪᴜᴍ ʟɪsᴛ.

ʙᴜʏ ᴘᴀɪᴅ ᴘʟᴀɴ ʙʏ - /plan</b>"""

    MANUELFILTER_TXT = """ʜᴇʟᴘ: <b>ꜰɪʟᴛᴇʀꜱ</b>
- ꜰɪʟᴛᴇʀ ɪꜱ ᴀ ꜰᴇᴀᴛᴜʀᴇ ᴡᴇʀᴇ ᴜꜱᴇʀꜱ ᴄᴀɴ ꜱᴇᴛ ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ʀᴇᴘʟɪᴇꜱ ꜰᴏʀ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴋᴇʏᴡᴏʀᴅ ᴀɴᴅ ɪ ᴡɪʟʟ ʀᴇꜱᴘᴏɴᴅ ᴡʜᴇɴᴇᴠᴇʀ ᴀ ᴋᴇʏᴡᴏʀᴅ ɪꜱ ꜰᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ
<b>ɴᴏᴛᴇ:</b>
1. ᴛʜɪꜱ ʙᴏᴛ ꜱʜᴏᴜʟᴅ ʜᴀᴠᴇ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇ.
2. ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴀᴅᴅ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴀ ᴄʜᴀᴛ.
3. ᴀʟᴇʀᴛ ʙᴜᴛᴛᴏɴꜱ ʜᴀᴠᴇ ᴀ ʟɪᴍɪᴛ ᴏꜰ 64 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ.
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /filter - <code>ᴀᴅᴅ ᴀ ꜰɪʟᴛᴇʀ ɪɴ ᴀ ᴄʜᴀᴛ</code>
• /filters - <code>ʟɪꜱᴛ ᴀʟʟ ᴛʜᴇ ꜰɪʟᴛᴇʀꜱ ᴏꜰ ᴀ ᴄʜᴀᴛ</code>
• /del - <code>ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴛᴇʀ ɪɴ ᴀ ᴄʜᴀᴛ</code>
• /delall - <code>ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ᴡʜᴏʟᴇ ꜰɪʟᴛᴇʀꜱ ɪɴ ᴀ ᴄʜᴀᴛ (ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)</code>"""

    # Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

    BUTTON_TXT = """ʜᴇʟᴘ: <b>ʙᴜᴛᴛᴏɴꜱ</b>
- ᴛʜɪꜱ ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛꜱ ʙᴏᴛʜ ᴜʀʟ ᴀɴᴅ ᴀʟᴇʀᴛ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴꜱ.
<b>ɴᴏᴛᴇ:</b>
1. ᴛᴇʟᴇɢʀᴀᴍ ᴡɪʟʟ ɴᴏᴛ ᴀʟʟᴏᴡꜱ ʏᴏᴜ ᴛᴏ ꜱᴇɴᴅ ʙᴜᴛᴛᴏɴꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴄᴏɴᴛᴇɴᴛ, ꜱᴏ ᴄᴏɴᴛᴇɴᴛ ɪꜱ ᴍᴀɴᴅᴀᴛᴏʀʏ.
2. ᴛʜɪꜱ ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛꜱ ʙᴜᴛᴛᴏɴꜱ ᴡɪᴛʜ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴛʏᴘᴇ.
3. ʙᴜᴛᴛᴏɴꜱ ꜱʜᴏᴜʟᴅ ʙᴇ ᴘʀᴏᴘᴇʀʟʏ ᴘᴀʀꜱᴇᴅ ᴀꜱ ᴍᴀʀᴋᴅᴏᴡɴ ꜰᴏʀᴍᴀᴛ
<b>ᴜʀʟ ʙᴜᴛᴛᴏɴꜱ:</b>
<code>[Button Text](buttonurl:https://t.me/vj_bots/3)</code>
<b>ᴀʟᴇʀᴛ ʙᴜᴛᴛᴏɴꜱ:</b>
<code>[Button Text](buttonalert:ᴛʜɪꜱ ɪꜱ ᴀɴ ᴀʟᴇʀᴛ ᴍᴇꜱꜱᴀɢᴇ)</code>"""

    AUTOFILTER_TXT = """ʜᴇʟᴘ: <b>ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ</b>
<b>ɴᴏᴛᴇ: Fɪʟᴇ Iɴᴅᴇx</b>
1. ᴍᴀᴋᴇ ᴍᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏꜰ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ɪꜰ ɪᴛ'ꜱ ᴘʀɪᴠᴀᴛᴇ.
2. ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴅᴏᴇꜱ ɴᴏᴛ ᴄᴏɴᴛᴀɪɴꜱ ᴄᴀᴍʀɪᴘꜱ, ᴘᴏʀɴ ᴀɴᴅ ꜰᴀᴋᴇ ꜰɪʟᴇꜱ.
3. ꜰᴏʀᴡᴀʀᴅ ᴛʜᴇ ʟᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴇ ᴡɪᴛʜ Qᴜᴏᴛᴇꜱ. ɪ'ʟʟ ᴀᴅᴅ ᴀʟʟ ᴛʜᴇ ꜰɪʟᴇꜱ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴍʏ ᴅʙ.

<b>Nᴏᴛᴇ: AᴜᴛᴏFɪʟᴛᴇʀ</b>
1. Aᴅᴅ ᴛʜᴇ ʙᴏᴛ ᴀs ᴀᴅᴍɪɴ ᴏɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
2. Usᴇ /connect ᴀɴᴅ ᴄᴏɴɴᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ ᴛʜᴇ ʙᴏᴛ.
3. Usᴇ /settings ᴏɴ ʙᴏᴛ's PM ᴀɴᴅ ᴛᴜʀɴ ᴏɴ AᴜᴛᴏFɪʟᴛᴇʀ ᴏɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ."""

    CONNECTION_TXT = """ʜᴇʟᴘ: <b>ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ</b>
- ᴜꜱᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ʙᴏᴛ ᴛᴏ ᴘᴍ ꜰᴏʀ ᴍᴀɴᴀɢɪɴɢ ꜰɪʟᴛᴇʀꜱ 
- ɪᴛ ʜᴇʟᴘꜱ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴘᴀᴍᴍɪɴɢ ɪɴ ɢʀᴏᴜᴘꜱ.
<b>ɴᴏᴛᴇ:</b>
1. ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴀᴅᴅ ᴀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.
2. ꜱᴇɴᴅ <code>/ᴄᴏɴɴᴇᴄᴛ</code> ꜰᴏʀ ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴘᴍ
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /connect  - <code>ᴄᴏɴɴᴇᴄᴛ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴄʜᴀᴛ ᴛᴏ ʏᴏᴜʀ ᴘᴍ</code>
• /disconnect  - <code>ᴅɪꜱᴄᴏɴɴᴇᴄᴛ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ</code>
• /connections - <code>ʟɪꜱᴛ ᴀʟʟ ʏᴏᴜʀ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ</code>"""

    # Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

    EXTRAMOD_TXT = """ʜᴇʟᴘ: Exᴛʀᴀ Mᴏᴅᴜʟᴇs
<b>ɴᴏᴛᴇ:</b>
 <b>✯ Maintained by : <a href={}>ᴇᴅɪsᴏɴ</a></b>
  
 <b>✯ Join here : <a href={}>Update Channel</a></b> 
  
 ./id - <code>ɢᴇᴛ ɪᴅ ᴏꜰ ᴀ ꜱᴘᴇᴄɪꜰɪᴇᴅ ᴜꜱᴇʀ.</ 
 code> 
  
 ./info  - <code>ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜꜱᴇʀ.</code> 
  
 ./song - Download any song [<code>example /song vaa vaathi song</code>] 
  
 ./telegraph - <code>Telegraph generator sen under 5MB video or photo I give telegraph link</code> 
  
 ./tts - <code>This command usage text to voice converter</code> 
  
 ./video - This command usage any YouTube video download hd [<code>example /video https://youtu.be/example...</code>]

./font - This command usage stylish and cool font generator [<code>example /font hi</code>]"""


    ADMIN_TXT = """ʜᴇʟᴘ: Aᴅᴍɪɴ Mᴏᴅs
<b>ɴᴏᴛᴇ:</b>
Tʜɪs Mᴏᴅᴜʟᴇ Oɴʟʏ Wᴏʀᴋs Fᴏʀ Mʏ Aᴅᴍɪɴs
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /logs - <code>ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʀᴇᴄᴇɴᴛ ᴇʀʀᴏʀꜱ</code>
• /stats - <code>ᴛᴏ ɢᴇᴛ ꜱᴛᴀᴛᴜꜱ ᴏꜰ ꜰɪʟᴇꜱ ɪɴ ᴅʙ. [Tʜɪs Cᴏᴍᴍᴀɴᴅ Cᴀɴ Bᴇ Usᴇᴅ Bʏ Aɴʏᴏɴᴇ]</code>
• /delete - <code>ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.</code>
• /leave  - <code>ᴛᴏ ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ᴀ ᴄʜᴀᴛ.</code>
• /disable  -  <code>ᴛᴏ ᴅɪꜱᴀʙʟᴇ ᴀ ᴄʜᴀᴛ.</code>
• /ban  - <code>ᴛᴏ ʙᴀɴ ᴀ ᴜꜱᴇʀ.</code>
• /unban  - <code>ᴛᴏ ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ.</code>
• /channel - <code>ᴛᴏ ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴛᴏᴛᴀʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀɴɴᴇʟꜱ</code>
• /broadcast - <code>ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ</code>
• /grp_broadcast - <code>Tᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs.</code>
• /gfilter - <code>ᴛᴏ ᴀᴅᴅ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀs</code>
• /gfilters - <code>ᴛᴏ ᴠɪᴇᴡ ʟɪsᴛ ᴏғ ᴀʟʟ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀs</code>
• /delg - <code>ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ sᴘᴇᴄɪғɪᴄ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀ</code>
• /request - <code>Tᴏ sᴇɴᴅ ᴀ Mᴏᴠɪᴇ/Sᴇʀɪᴇs ʀᴇᴏ̨ᴜᴇsᴛ ᴛᴏ ʙᴏᴛ ᴀᴅᴍɪɴs. Oɴʟʏ ᴡᴏʀᴋs ᴏɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ. [Tʜɪs Cᴏᴍᴍᴀɴᴅ Cᴀɴ Bᴇ Usᴇᴅ Bʏ Aɴʏᴏɴᴇ]</code>
• /delallg - <code>Tᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ Gғɪʟᴛᴇʀs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ.</code>
• /deletefiles - <code>Tᴏ ᴅᴇʟᴇᴛᴇ CᴀᴍRɪᴘ ᴀɴᴅ PʀᴇDVD Fɪʟᴇs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ.</code>"""

    SEC_STATUS_TXT = """<b>★ Tᴏᴛᴀʟ Usᴇʀs: unavailabe
★ Tᴏᴛᴀʟ Cʜᴀᴛs: unavailabe
★ Tᴏᴛᴀʟ Fɪʟᴇs: <code>{}</code>
★ Usᴇᴅ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code>
★ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code></b>"""

    STATUS_TXT = """<b>Total Files From All DBs: <code>{}</code>



FILE FIRST DB :-
★ Tᴏᴛᴀʟ Fɪʟᴇs: <code>{}</code>
★ Usᴇᴅ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code>
★ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code>

FILE SECOND DB :-
★ Tᴏᴛᴀʟ Fɪʟᴇs: <code>{}</code>
★ Usᴇᴅ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code>
★ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code>

OTHER DB :-
★ Usᴇᴅ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code>
★ Fʀᴇᴇ Sᴛᴏʀᴀɢᴇ: <code>{} MB</code></b>"""

    LOG_TEXT_G = """#NewGroup
Gʀᴏᴜᴘ = {}(<code>{}</code>)
Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs = <code>{}</code>
Aᴅᴅᴇᴅ Bʏ - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Nᴀᴍᴇ - {}"""

    ALRT_TXT = """ʜᴇʟʟᴏ {},
ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ʏᴏᴜʀ ᴍᴏᴠɪᴇ ʀᴇQᴜᴇꜱᴛ,
ʀᴇQᴜᴇꜱᴛ ʏᴏᴜʀ'ꜱ..."""

    OLD_ALRT_TXT = """ʜᴇʏ {},
ʏᴏᴜ ᴀʀᴇ ᴜꜱɪɴɢ ᴏɴᴇ ᴏꜰ ᴍʏ ᴏʟᴅ ᴍᴇꜱꜱᴀɢᴇꜱ, 
ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ʀᴇQᴜᴇꜱᴛ ᴀɢᴀɪɴ."""

    CUDNT_FND = """ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏᴛʜɪɴɢ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ {}
ᴅɪᴅ ʏᴏᴜ ᴍᴇᴀɴ ᴀɴʏ ᴏɴᴇ ᴏꜰ ᴛʜᴇꜱᴇ?"""

    I_CUDNT = """<b>sᴏʀʀʏ ɴᴏ ꜰɪʟᴇs ᴡᴇʀᴇ ꜰᴏᴜɴᴅ ꜰᴏʀ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ {} 😕

ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ɪɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ 😃

ᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ 👇

ᴇxᴀᴍᴘʟᴇ : Uncharted or Uncharted 2022 or Uncharted En

ꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ 👇

ᴇxᴀᴍᴘʟᴇ : Loki S01 or Loki S01E04 or Lucifer S03E24

🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)</b>"""

    I_CUD_NT = """ɪ ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴀɴʏ ᴍᴏᴠɪᴇ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ {}.
ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ꜱᴘᴇʟʟɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ ᴏʀ ɪᴍᴅʙ..."""

    MVE_NT_FND = """ᴍᴏᴠɪᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ..."""

    TOP_ALRT_MSG = """Cʜᴇᴄᴋɪɴɢ Fᴏʀ Mᴏᴠɪᴇ Iɴ Dᴀᴛᴀʙᴀsᴇ..."""

    MELCOW_ENG = """<b>Hᴇʟʟᴏ {} 😍, Aɴᴅ Wᴇʟᴄᴏᴍᴇ Tᴏ {} Gʀᴏᴜᴘ ❤️</b>"""

    SHORTLINK_INFO = """

🫵 Select Your Language And Earn Money 💰"""

    REQINFO = """
⚠ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ⚠

ᴀꜰᴛᴇʀ 5 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ

ɪꜰ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ꜱᴇᴇ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴍᴏᴠɪᴇ / sᴇʀɪᴇs ꜰɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ɴᴇxᴛ ᴘᴀɢᴇ"""

    SELECT = """sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘʀᴇғᴇʀʀᴇᴅ ʟᴀɴɢᴜᴀɢᴇ, ǫᴜᴀʟɪᴛʏ, sᴇᴀsᴏɴ ᴀɴᴅ ᴇᴘɪsᴏᴅᴇ"""

    SINFO = """
🫣 For Movie Join First Then Click On Try Again Button 😅"""

    NORSLTS = """ 
★ #𝗡𝗼𝗥𝗲𝘀𝘂𝗹𝘁𝘀 ★

𝗜𝗗 <b>: {}</b>

𝗡𝗮𝗺𝗲 <b>: {}</b>

𝗠𝗲𝘀𝘀𝗮𝗴𝗲 <b>: {}</b>"""

    CAPTION = """<b>📂 ғɪʟᴇɴᴀᴍᴇ : {file_name}
    
<b>⚙️ sɪᴢᴇ : {file_size}</b>
<b>🎬 ǫᴜᴀʟɪᴛʏ : {quality}</b>
<b>🎞 sᴇᴀsᴏɴ : {season}</b>
<b>📺 ᴇᴘɪsᴏᴅᴇ : {episode}</b>
<b>🌐 ʟᴀɴɢᴜᴀɢᴇ : {language}</b>
<b>📅 ʏᴇᴀʀ : {year}</b>
<b>📀 ғᴏʀᴍᴀᴛ : {format}</b>

BY YOUR @GREENMOVIEBOT""" 

    IMDB_TEMPLATE_TXT = """
<b>Query: {qurey}

IMDb Data:

<b>🏷 Title</b>: <a href={url}>{title}</a>
🎭 Genres: {genres}
📆 Year: <a href={url}/releaseinfo>{year}</a>
🌟 Rating: <a href={url}/ratings>{rating}</a> / 10 (based on {votes} user ratings.)
☀️ Languages : <code>{languages}</code>
📀 RunTime: {runtime} Minutes
📆 Release Info : {release_date}
🎛 Countries : <code>{countries}</code>


⏰Result Shown in: {remaining_seconds} <i>seconds</i> 🔥

Requested by : {user_mention}</b>"""

    ALL_FILTERS = """
<b>Hᴇʏ {}, Tʜᴇsᴇ ᴀʀᴇ ᴍʏ ᴛʜʀᴇᴇ ᴛʏᴘᴇs ᴏғ ғɪʟᴛᴇʀs.</b>"""

    GFILTER_TXT = """
<b>Wᴇʟᴄᴏᴍᴇ ᴛᴏ Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs. Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs ᴀʀᴇ ᴛʜᴇ ғɪʟᴛᴇʀs sᴇᴛ ʙʏ ʙᴏᴛ ᴀᴅᴍɪɴs ᴡʜɪᴄʜ ᴡɪʟʟ ᴡᴏʀᴋ ᴏɴ ᴀʟʟ ɢʀᴏᴜᴘs.</b>
    
Aᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:
• /gfilter - <code>Tᴏ ᴄʀᴇᴀᴛᴇ ᴀ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀ.</code>
• /gfilters - <code>Tᴏ ᴠɪᴇᴡ ᴀʟʟ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀs.</code>
• /delg - <code>Tᴏ ᴅᴇʟᴇᴛᴇ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ɢʟᴏʙᴀʟ ғɪʟᴛᴇʀ.</code>
• /delallg - <code>ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ɢʟᴏʙᴀʟ ꜰɪʟᴛᴇʀꜱ.</code>"""

    FILE_STORE_TXT = """
<b>Fɪʟᴇ sᴛᴏʀᴇ ɪs ᴛʜᴇ ғᴇᴀᴛᴜʀᴇ ᴡʜɪᴄʜ ᴡɪʟʟ ᴄʀᴇᴀᴛᴇ ᴀ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ ᴏғ ᴀ sɪɴɢʟᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ғɪʟᴇs.</b>

Aᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:
• /batch - <code>Tᴏ ᴄʀᴇᴀᴛᴇ ᴀ ʙᴀᴛᴄʜ ʟɪɴᴋ ᴏғ ᴍᴜʟᴛɪᴘʟᴇ ғɪʟᴇs.</code>
• /link - <code>Tᴏ ᴄʀᴇᴀᴛᴇ ᴀ sɪɴɢʟᴇ ғɪʟᴇ sᴛᴏʀᴇ ʟɪɴᴋ.</code>
• /pbatch - <code>Jᴜsᴛ ʟɪᴋᴇ /batch, ʙᴜᴛ ᴛʜᴇ ғɪʟᴇs ᴡɪʟʟ ʙᴇ sᴇɴᴅ ᴡɪᴛʜ ғᴏʀᴡᴀʀᴅ ʀᴇsᴛʀɪᴄᴛɪᴏɴs.</code>
• /plink - <code>Jᴜsᴛ ʟɪᴋᴇ /link, ʙᴜᴛ ᴛʜᴇ ғɪʟᴇ ᴡɪʟʟ ʙᴇ sᴇɴᴅ ᴡɪᴛʜ ғᴏʀᴡᴀʀᴅ ʀᴇsᴛʀɪᴄᴛɪᴏɴ.</code>"""

    SONG_TXT = """<b>ꜱᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴏᴅᴜʟᴇ</b> 
      
 <b>ꜱᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴏᴅᴜʟᴇ, ꜰᴏʀ ᴛʜᴏꜱᴇ ᴡʜᴏ ʟᴏᴠᴇ ᴍᴜꜱɪᴄ. yᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜᴇ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴy ꜱᴏɴɢ ᴡɪᴛʜ ꜱᴜᴩᴇʀ ꜰᴀꜱᴛ ꜱᴩᴇᴇᴅ. ᴡᴏʀᴋꜱ ʙᴏᴛ ᴀɴᴅ ɢʀᴏᴜᴩꜱ ᴏɴʟy...</b> 
  
 <b>ᴄᴏᴍᴍᴀɴᴅꜱ</b> :<b> 𝄟⃝.  /song ꜱᴏɴɢ ɴᴀᴍᴇ</b></b>""" 

    YTDL_TXT = """<b>ʜᴇʟᴩ yᴏᴜ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ꜰʀᴏᴍ yᴏᴜᴛᴜʙᴇ. 
  
 ᴜꜱᴀɢᴇ : yᴏᴜ ᴄᴀɴ ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴy ᴠɪᴅᴇᴏ ꜰʀᴏᴍ yᴏᴜᴛᴜʙᴇ 
  
 ʜᴏᴡ ᴛᴏ ᴜꜱᴇ : ᴛyᴩᴇ - /video ᴏʀ /mp4 
  
 ᴇxᴀᴍᴩʟᴇ :<code>/mp4 https://youtu.be/example...</code></b>""" 

    TTS_TXT = """<b>ᴛᴛꜱ 🎤 ᴍᴏᴅᴜʟᴇ : ᴛʀᴀɴꜱʟᴀᴛᴇ ᴛᴇxᴛ ᴛᴏ ꜱᴩᴇᴇᴄʜ 
  
 ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴜꜱᴀɢᴇ : /tts</b>""" 

    GTRANS_TXT = """<b>ʜᴇʟᴩ:ɢᴏᴏɢʟᴇ ᴛʀᴀɴꜱʟᴀᴛᴇʀ 
  
 ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʜᴇʟᴩꜱ yᴏᴜ ᴛᴏ ᴛʀᴀɴꜱʟᴀᴛᴇ ᴀ ᴛᴇxᴛ ᴛᴏ ᴀɴy ʟᴀɴɢᴜᴀɢᴇꜱ yᴏᴜ ᴡᴀɴᴛ. ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋꜱ ᴏɴ ʙᴏᴛʜ ᴩᴍ ᴀɴᴅ ɢʀᴏᴜᴏ  
  
 ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴜꜱᴀɢᴇ : /tr - ᴛᴏ ᴛʀᴀɴꜱʟᴀᴛᴇʀ ᴛᴇxᴛꜱ ᴛᴏ ᴀ ꜱᴩᴇᴄɪꜰᴄ ʟᴀɴɢᴜᴀɢᴇ 
  
 ɴᴏᴛᴇ: ᴡʜɪʟᴇ ᴜꜱɪɴɢ /tr yᴏᴜ ꜱʜᴏᴜʟᴅ ꜱᴩᴇᴄɪꜰy ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ 
  
 ᴇxᴀᴍᴩʟᴇ: /𝗍𝗋 ᴍʟ 
 • ᴇɴ = ᴇɴɢʟɪꜱʜ 
 • ᴍʟ = ᴍᴀʟᴀyᴀʟᴀᴍ 
 • ʜɪ = ʜɪɴᴅɪ</b>""" 

    TELE_TXT = """<b>ʜᴇʟᴘ: ᴛᴇʟᴇɢʀᴀᴘʜ ᴅᴏ ᴀꜱ ʏᴏᴜ ᴡɪꜱʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀ.ᴘʜ ᴍᴏᴅᴜʟᴇ! 
  
 ᴜꜱᴀɢᴇ: /telegraph - ꜱᴇɴᴅ ᴍᴇ ᴘɪᴄᴛᴜʀᴇ ᴏʀ ᴠɪᴅᴇ ᴜɴᴅᴇʀ (5ᴍʙ) 
  
 ɴᴏᴛᴇ: 
 ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ɢᴏᴜᴘꜱ ᴀɴᴅ ᴘᴍꜱ 
 ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ʙʏ ᴇᴠᴇʀʏᴏɴᴇ</b>""" 

    CORONA_TXT = """<b>ʜᴇʟᴩ: ᴄᴏᴠɪᴅ 
  
 ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʜᴇʟᴩꜱ yᴏᴜ ᴛᴏ ᴋɴᴏᴡ ᴅᴀɪʟy ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴄᴏᴠɪᴅ 
  
 ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴜꜱᴀɢᴇ: 
  
 /covid - ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜ yᴏᴜʀ ᴄᴏᴜɴᴛʀy ɴᴀᴍᴇ ᴛᴏ ɢᴇᴛ ᴄᴏᴠɪᴅᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ 
 ᴇxᴀᴍᴩʟᴇ:<code>/covid 𝖨𝗇𝖽𝗂𝖺</code> 
  
 ⚠️ ᴛʜɪꜱ ꜱᴇʀᴠɪᴄᴇ ʜᴀꜱ ʙᴇᴇɴ ꜱᴛᴏᴩᴩᴇᴅ 
  
 </b>""" 

    PROGRESS_BAR = """\n
╭━━━━❰ File Is Renaming... ❱━➣
┣⪼ 🗂️ : {1} | {2}
┣⪼ ⏳️ : {0}%
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━➣ """

    ABOOK_TXT = """<b>ʜᴇʟᴩ : ᴀᴜᴅɪᴏʙᴏᴏᴋ 
  
 yᴏᴜ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴀ ᴩᴅꜰ ꜰɪʟᴇ ᴛᴏ ᴀ ᴀᴜᴅɪᴏ ꜰɪʟᴇ ᴡɪᴛʜ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ✯ 
  
 ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴜꜱᴀɢᴇ: 
 /audiobook: ʀᴇᴩʟy ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴀɴy ᴩᴅꜰ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴛʜᴇ ᴀᴜᴅɪᴏ 
</b>""" 


    PINGS_TXT = """<b>ᴘɪɴɢ ᴛᴇꜱᴛɪɴɢ:ʜᴇʟᴘꜱ ʏᴏᴜ ᴛᴏ ᴋɴᴏᴡ ʏᴏᴜʀ ᴘɪɴɢ🪄 
  
 ᴄᴏᴍᴍᴀɴᴅꜱ: 
 • /alive - ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜ ᴀʀᴇ ᴀʟɪᴠᴇ. 
 • /help - To get help. 
 • /ping - <b>ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴘɪɴɢ. 
  
 ᴜꜱᴀɢᴇ : 
 • ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘᴍ ᴀɴᴅ ɢʀᴏᴜᴘꜱ 
 • ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ʙᴜʏ ᴇᴠᴇʀʏᴏɴᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ʙᴏᴛꜱ ᴘᴍ 
 • ꜱʜᴀʀᴇ ᴜꜱ ꜰᴏʀ ᴍᴏʀᴇ ꜰᴇᴀᴛᴜʀᴇꜱ 
  </b>""" 

    STICKER_TXT = """<b>yᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴍᴏᴅᴜʟᴇ ᴛᴏ ꜰɪɴᴅᴀɴy  ꜱᴛɪᴄᴋᴇʀꜱ ɪᴅ. 
 • ᴜꜱᴀɢᴇ :ᴛᴏ ɢᴇᴛ ꜱᴛɪᴄᴋᴇʀ 
   
 ⭕ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ 
 /stickerid
 </b>""" 

    FONT_TXT= """<b>ᴜꜱᴀɢᴇ 
  
 yᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴄʜᴀɴɢᴇ ꜰᴏɴᴛ ꜱᴛyʟᴇ   
  
 ᴄᴏᴍᴍᴀɴᴅ : /font yᴏᴜʀ ᴛᴇxᴛ (ᴏᴩᴛɪᴏɴᴀʟ) 
 ᴇɢ:- /font ʜᴇʟʟᴏ 
  
 </b>""" 

    PURGE_TXT = """<b>ᴘᴜʀɢᴇ 
      
 ᴅᴇʟᴇᴛᴇ ᴀ ʟᴏᴛ ᴏꜰ ᴍᴇssᴀɢᴇs ꜰʀᴏᴍ ɢʀᴏᴜᴘs!  
      
  ᴀᴅᴍɪɴ  
  
 ◉ /purge :- ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs ꜰʀᴏᴍ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴍᴇssᴀɢᴇ, ᴛᴏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴍᴇssᴀɢᴇ</b>""" 

    WHOIS_TXT = """<b>ᴡʜᴏɪꜱ ᴍᴏᴅᴜʟᴇ 
  
 ɴᴏᴛᴇ:- ɢɪᴠᴇ ᴀ ᴜꜱᴇʀ ᴅᴇᴛᴀɪʟꜱ 
 /whois :- ɢɪᴠᴇ ᴀ ᴜꜱᴇʀ ꜰᴜʟʟ ᴅᴇᴛᴀɪʟꜱ 📑 
 </b>""" 

    JSON_TXT = """<b> 
 ᴊsᴏɴ:  
 ʙᴏᴛ ʀᴇᴛᴜʀɴs ᴊsᴏɴ ꜰᴏʀ ᴀʟʟ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇs ᴡɪᴛʜ /json 
  
 ꜰᴇᴀᴛᴜʀᴇs: 
  
 ᴍᴇssᴀɢᴇ ᴇᴅɪᴛᴛɪɴɢ ᴊsᴏɴ 
 ᴘᴍ sᴜᴘᴘᴏʀᴛ 
 ɢʀᴏᴜᴘ sᴜᴘᴘᴏʀᴛ 
  
 ɴᴏᴛᴇ: 
  
 ᴇᴠᴇʀʏᴏɴᴇ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ , ɪꜰ sᴘᴀᴍɪɴɢ ʜᴀᴘᴘᴇɴs ʙᴏᴛ ᴡɪʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʙᴀɴ ʏᴏᴜ ꜰʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.</b>""" 

    URLSHORT_TXT = """<b>ʜᴇʟᴩ: ᴜʀʟ ꜱʜᴏʀᴛɴᴇʀ 
  
 <i><b>𝚃𝚑𝚒𝚜ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʜᴇʟᴩꜱ yᴏᴜ ᴛᴏ ꜱʜᴏʀᴛ ᴛᴏ ᴜʀʟ </i></b> 
  
 ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴜꜱᴀɢᴇ: 
  
 /short: <b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡɪᴛʜ yᴏᴜʀ ʟɪɴᴋ ᴛᴏ ɢᴇᴛ ꜱʜᴏʀᴛ ʟɪɴᴋꜱ</b> 
 ᴇxᴀᴍᴩʟᴇ:<code>/short https://youtu.be/example...</code> 
</b>""" 

    CARB_TXT = """<b>ʜᴇʟᴩ ꜰᴏʀ ᴄᴀʀʙᴏɴ 
  
 ᴄᴀʀʙᴏɴ ɪꜱ ᴀ ꜰᴇᴜᴛᴜʀᴇ ᴛᴏ ᴍᴀᴋᴇ ᴛʜᴇ ɪᴍᴀɢᴇ ᴀꜱ ꜱʜᴏᴡɴ ɪɴ ᴛʜᴇ ᴛᴏᴩ ᴡɪᴛʜ ʏᴏᴜʀ ᴛᴇxᴛꜱ. 
 ꜰᴏʀ ᴜꜱɪɴɢ ᴛʜᴇ ᴍᴏᴅᴜʟᴇ ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴛʜᴇ ᴛᴇxᴛ ᴀɴᴅ ᴏᴇᴩʟᴀʏ ᴛɪ ɪᴛ ᴡɪᴛʜ  /carbon ᴄᴏᴍᴍᴀɴᴅ ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ᴩᴇᴩᴀʏ ᴡɪᴛʜ ᴛʜᴇ ᴄᴀʀʙᴏɴ ɪᴍᴀɢᴇ 
</b>""" 
    GEN_PASS = """<b>Hᴇʟᴘ: Pᴀꜱꜱᴡᴏʀᴅ Gᴇɴᴇʀᴀᴛᴏʀ 
  
 Tʜᴇʀᴇ Iꜱ Nᴏᴛʜɪɴɢ Tᴏ Kɴᴏᴡ Mᴏʀᴇ. Sᴇɴᴅ Mᴇ Tʜᴇ Lɪᴍɪᴛ Oғ Yᴏᴜʀ Pᴀꜱꜱᴡᴏʀᴅ. 
 - I Wɪʟʟ Gɪᴠᴇ Tʜᴇ Pᴀꜱꜱᴡᴏʀᴅ Oғ Tʜᴀᴛ Lɪᴍɪᴛ. 
  
 Cᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ Uꜱᴀɢᴇ: 
 • /genpassword ᴏʀ /genpw 𝟸𝟶 
  
 NOTE: 
 • Oɴʟʏ Dɪɢɪᴛꜱ Aʀᴇ Aʟʟᴏᴡᴇᴅ 
 • Mᴀxɪᴍᴜᴍ Aʟʟᴏᴡᴇᴅ Dɪɢɪᴛꜱ Tɪʟʟ 𝟾𝟺  
 (I Cᴀɴ'ᴛ Gᴇɴᴇʀᴀᴛᴇ Pᴀꜱꜱᴡᴏʀᴅꜱ Aʙᴏᴠᴇ Tʜᴇ Lᴇɴɢᴛʜ 𝟾𝟺) 
 • IMDʙ ꜱʜᴏᴜʟᴅ ʜᴀᴠᴇ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟʟᴀɢᴇ. 
 • Tʜᴇꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴡᴏʀᴋꜱ ᴏɴ ʙᴏᴛʜ ᴘᴍ ᴀɴᴅ ɢʀᴏᴜᴘ. 
 • Tʜᴇꜱᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ᴜꜱᴇᴅ ʙʏ ᴀɴʏ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀ.</b>""" 

    SHARE_TXT = """<b>Get your text share url. 
  
 - ᴇx :- /share
  
 </b>""" 

    PIN_TXT = """<b>ᴩɪɴ ᴍᴏᴅᴜʟᴇ 
 ᴩɪɴ ᴀ ᴍᴇꜱꜱᴀɢᴇ... 
  
 ᴀʟʟ ᴛʜᴇ ᴩɪɴ ʀᴇᴩʟᴀᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅꜱ ᴄᴀɴ ʙᴇ ꜰᴏᴜɴᴅ ʜᴇʀᴇ: 
  
 📌ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴜꜱᴀɢᴇ📌 
  
 /pin :- ᴛᴏ ᴩɪɴ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴏɴ ʏᴏᴜʀ ᴄʜᴀᴛꜱ 
 /unpin :- ᴛᴏ ᴜɴᴩɪɴ ᴛʜᴇ ᴄᴜʀʀᴇᴇɴᴛ ᴩɪɴɴᴇᴅ ᴍᴇꜱꜱᴀɢᴇ</b>"""


    RESTART_TXT = """
<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !

📅 Dᴀᴛᴇ : <code>{}</code>
⏰ Tɪᴍᴇ : <code>{}</code>
🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code>
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: <code>v2.7.1 [ Sᴛᴀʙʟᴇ ]</code></b>"""

    LOGO = """
             ██████████   ████████████
             ███    ███   ███      ████
             ███    ███   ███       ███
             ██████████   ███ █████████
             ██████████   ███ ███████
             ███    ███   ███ █████
             ███    ███   ███  ██████
             ███    ███   ███    ██████
             ███    ███   ███      ████"""


    RENAME_TXT = """
🌌 <b><u>HOW TO SET THUMBNAIL</u></b>
  
•> /set_thumb - send any picture to automatically set thumbnail.
•> /del_thumb use this command and delete your old thumbnail.
•> /view_thumb use this command view your current thumbnail.

📑 <b><u>HOW TO SET CUSTOM CAPTION</u></b>

•> /set_caption - set a custom caption
•> /see_caption - see your custom caption
•> /del_caption - delete custom caption

Example:- /set_caption 📕 File Name: {filename}
💾 Size: {filesize}
⏰ Duration: {duration}

✏️ <b><u>HOW TO RENAME A FILE</u></b>

•> /rename - send any file and click rename option and type new file name and \nthen select [ document, video, audio ]👈 choice this.
"""

    STREAM_TXT = """<b><u>HOW TO GET STREAM AND DOWNLOAD LINK :</u>

/stream - ɢᴇᴛ sᴛʀᴇᴀᴍᴀʙʟᴇ ᴀɴᴅ ᴅᴏᴡɴʟᴏᴀᴅᴀʙʟᴇ ʟɪɴᴋ ᴏғ ᴀɴʏ ғɪʟᴇ</b>"""
