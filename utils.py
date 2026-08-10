# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

import logging, asyncio, os, re, random, pytz, aiohttp, requests, string, json, http.client, aiofiles
from info import *
from imdb import Cinemagoer 
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import enums
from pyrogram.errors import *
from typing import Union
from Script import script
from datetime import datetime, date
from typing import List
from database.users_chats_db import db
from database.join_reqs import JoinReqs
from bs4 import BeautifulSoup
from shortzy import Shortzy
from urllib.parse import quote_plus


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
join_db = JoinReqs
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\((buttonurl|buttonalert):(?:/{0,2})(.+?)(:same)?\))")

imdb = Cinemagoer('s3', uri='sqlite:///cinemagoer.db') 
TOKENS = {}
VERIFIED = {}
BANNED = {}
SECOND_SHORTENER = {}
SMART_OPEN = '“'
SMART_CLOSE = '”'
START_CHAR = ('\'', '"', SMART_OPEN)

# temp db for banned 
class temp(object):
    BANNED_USERS = []
    BANNED_CHATS = []
    ME = None
    BOT = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None
    GETALL = {}
    SHORT = {}
    SETTINGS = {}
    IMDB_CAP = {}


async def pub_is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(int(id), query.from_user.id)
        except UserNotParticipant:
            btn.append(
                [InlineKeyboardButton(f'Join {chat.title}', url=chat.invite_link)]
            )
        except Exception as e:
            pass
    return btn

async def is_subscribed(bot, query):
    if not AUTH_CHANNEL:
        return True
    if REQUEST_TO_JOIN_MODE == True and join_db().isActive():
        try:
            user = await join_db().get_user(query.from_user.id)
            if user and user["user_id"] == query.from_user.id:
                return True
            else:
                try:
                    user_data = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
                except UserNotParticipant:
                    pass
                except Exception as e:
                    logger.exception(e)
                else:
                    if user_data.status != enums.ChatMemberStatus.BANNED:
                        return True
        except Exception as e:
            logger.exception(e)
            return False
    else:
        try:
            user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
        except UserNotParticipant:
            pass
        except Exception as e:
            logger.exception(e)
        else:
            if user.status != enums.ChatMemberStatus.BANNED:
                return True
        return False

POSTER_CACHE = {}

async def get_tmdb_poster(query, bulk=False, id=False):
    if not bulk and not id and query in POSTER_CACHE:
        return POSTER_CACHE[query]
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            if id:
                # Assuming query is the TMDB ID or IMDb ID
                media_type = "movie" # Default to movie
                tmdb_id = query
                if str(query).startswith('tt'):
                    # Fetch by IMDb ID
                    find_url = f"https://api.themoviedb.org/3/find/{query}?api_key={TMDB_API_KEY}&external_source=imdb_id"
                    async with session.get(find_url) as find_resp:
                        find_res = await find_resp.json()
                        if find_res.get('movie_results'):
                            tmdb_id = find_res['movie_results'][0]['id']
                            media_type = 'movie'
                        elif find_res.get('tv_results'):
                            tmdb_id = find_res['tv_results'][0]['id']
                            media_type = 'tv'
                        else:
                            return None
                else:
                    # Check if it's a TV show or Movie (this is tricky if we only have numeric ID)
                    # We can try movie first, then TV
                    pass # We'll handle this by trying movie details first
                
                detail_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}&append_to_response=credits,release_dates,content_ratings"
                async with session.get(detail_url) as detail_response:
                    if detail_response.status != 200 and media_type == 'movie':
                        # Try TV
                        media_type = 'tv'
                        detail_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}&append_to_response=credits,release_dates,content_ratings"
                        async with session.get(detail_url) as detail_response:
                            if detail_response.status != 200: return None
                            movie = await detail_response.json()
                    else:
                        movie = await detail_response.json()
                return await format_tmdb_detail(movie, media_type)

            url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={quote_plus(query)}"
            async with session.get(url) as response:
                res = await response.json()
                if not res.get('results'):
                    return None
                
                if bulk:
                    results = []
                    for r in res['results']:
                        if r.get('media_type') in ['movie', 'tv']:
                            # Mock Cinemagoer object structure for compatibility
                            class Movie:
                                def __init__(self, data):
                                    self.data = data
                                    self.movieID = data.get('id')
                                    self.title = data.get('title') or data.get('name')
                                    self.year = (data.get('release_date') or data.get('first_air_date') or "0000")[:4]
                                def get(self, key): return getattr(self, key, None)
                            results.append(Movie(r))
                    return results
                
                result = res['results'][0]
                media_type = result.get('media_type')
                if media_type not in ['movie', 'tv']:
                    for r in res['results']:
                        if r.get('media_type') in ['movie', 'tv']:
                            result = r
                            media_type = r.get('media_type')
                            break
                    else:
                        return None
                
                tmdb_id = result.get('id')
                detail_url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}&append_to_response=credits,release_dates,content_ratings"
                async with session.get(detail_url) as detail_response:
                    movie = await detail_response.json()
                    res = await format_tmdb_detail(movie, media_type)
                    if not bulk and not id:
                        POSTER_CACHE[query] = res
                    return res
    except Exception as e:
        logger.error(f"TMDB Error: {e}")
        return None

async def format_tmdb_detail(movie, media_type):
    poster = f"https://image.tmdb.org/t/p/original{movie.get('poster_path')}" if movie.get('poster_path') else None
    credits = movie.get('credits', {})
    cast = [c.get('name') for c in credits.get('cast', [])[:10]]
    crew = credits.get('crew', [])
    director = [c.get('name') for c in crew if c.get('job') == 'Director']
    writer = [c.get('name') for c in crew if c.get('job') in ['Writer', 'Screenplay', 'Author']]
    producer = [c.get('name') for c in crew if c.get('job') == 'Producer']
    genres = [g.get('name') for g in movie.get('genres', [])]
    
    rating = "N/A"
    if media_type == 'movie':
        for r in movie.get('release_dates', {}).get('results', []):
            if r.get('iso_3166_1') == 'IN':
                rating = r.get('release_dates', [{}])[0].get('certification', 'N/A')
                break
    else:
        for r in movie.get('content_ratings', {}).get('results', []):
            if r.get('iso_3166_1') == 'IN':
                rating = r.get('rating', 'N/A')
                break

    return {
        'title': movie.get('title') or movie.get('name'),
        'votes': movie.get('vote_count'),
        "aka": movie.get("original_title") or movie.get("original_name"),
        "seasons": movie.get("number_of_seasons", "N/A"),
        "box_office": movie.get('revenue', 'N/A'),
        'localized_title': movie.get('title') or movie.get('name'),
        'kind': media_type,
        "imdb_id": movie.get('imdb_id'),
        "cast": ", ".join(cast) if cast else "N/A",
        "runtime": f"{movie.get('runtime') or movie.get('episode_run_time', [0])[0]} min",
        "countries": ", ".join([c.get('name') for c in movie.get('production_countries', [])]),
        "certificates": rating,
        "languages": ", ".join([l.get('english_name') for l in movie.get('spoken_languages', [])]),
        "director": ", ".join(director) if director else "N/A",
        "writer": ", ".join(writer) if writer else "N/A",
        "producer": ", ".join(producer) if producer else "N/A",
        "composer": "N/A",
        "cinematographer": "N/A",
        "music_team": "N/A",
        "distributors": "N/A",
        'release_date': movie.get('release_date') or movie.get('first_air_date'),
        'year': (movie.get('release_date') or movie.get('first_air_date') or "0000")[:4],
        'genres': ", ".join(genres) if genres else "N/A",
        'poster': poster,
        'plot': movie.get('overview'),
        'rating': str(movie.get("vote_average")),
        'url': f"https://www.themoviedb.org/{media_type}/{movie.get('id')}"
    }

def clean_query(query):
    query = query.lower()
    # Remove common extra terms with word boundaries
    extra_terms = [
        "malayalam", "tamil", "hindi", "telugu", "kannada", "english", "bengali", "punjabi", "marathi", "gujarati",
        "web-dl", "webrip", "bluray", "brrip", "hdrip", "hdtv", "hevc", "x264", "x265", "1080p", "720p", "480p", "360p",
        "dual", "audio", "org", "original", "hc", "sub", "subs", "esub", "dubbed", "movie", "full", "series"
    ]
    
    # Extract year
    year_match = re.search(r'\b(19|20)\d{2}\b', query)
    year_str = year_match.group(0) if year_match else None
    
    # Remove year from title search if it's there
    title = query
    if year_str:
        title = title.replace(year_str, "")
        
    for term in extra_terms:
        title = re.sub(r'\b' + re.escape(term) + r'\b', '', title)
        
    # Remove non-alphanumeric at ends and multiple spaces
    title = re.sub(r'[^a-zA-Z0-9\s]', ' ', title)
    title = " ".join(title.split())
    
    return title.strip(), year_str

async def get_poster(query, bulk=False, id=False, file=None):
    if not id:
        # Try original first
        tmdb_res = await get_tmdb_poster(query, bulk=bulk, id=id)
        if tmdb_res:
            return tmdb_res
            
        # Try cleaned version
        title, year = clean_query(query)
        if title:
            # Try title + year
            if year:
                tmdb_res = await get_tmdb_poster(f"{title} {year}", bulk=bulk, id=id)
                if tmdb_res: return tmdb_res
            
            # Try title only
            tmdb_res = await get_tmdb_poster(title, bulk=bulk, id=id)
            if tmdb_res: return tmdb_res
            
    # Fallback to old logic or original search
    tmdb_res = await get_tmdb_poster(query, bulk=bulk, id=id)
    if tmdb_res:
        return tmdb_res

    if not id:
        query = (query.strip()).lower()
        title = query
        year = re.findall(r'[1-2]\d{3}$', query, re.IGNORECASE)
        if year:
            year = list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r'[1-2]\d{3}', file, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1]) 
        else:
            year = None
        
        movieid = await asyncio.to_thread(imdb.search_movie, title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = query
    
    movie = await asyncio.to_thread(imdb.get_movie, movieid)
    if not movie:
        return None
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    plot = ""
    if not LONG_IMDB_DESCRIPTION:
        plot = movie.get('plot')
        if plot and len(plot) > 0:
            plot = plot[0]
    else:
        plot = movie.get('plot outline')
    if plot and len(plot) > 800:
        plot = plot[0:800] + "..."

    return {
        'title': movie.get('title'),
        'votes': movie.get('votes'),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get('box office'),
        'localized_title': movie.get('localized title'),
        'kind': movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str(movie.get("runtimes")),
        "countries": list_to_str(movie.get("countries")),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_str(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer":list_to_str(movie.get("writer")),
        "producer":list_to_str(movie.get("producer")),
        "composer":list_to_str(movie.get("composer")) ,
        "cinematographer":list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        'release_date': date,
        'year': movie.get('year'),
        'genres': list_to_str(movie.get("genres")),
        'poster': movie.get('full-size cover url'),
        'plot': plot,
        'rating': str(movie.get("rating")),
        'url':f'https://www.imdb.com/title/tt{movieid}'
    }


async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"

async def broadcast_messages_group(chat_id, message):
    try:
        kd = await message.copy(chat_id=chat_id)
        try:
            await kd.pin()
        except:
            pass
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages_group(chat_id, message)
    except Exception as e:
        return False, "Error"
    
async def search_gagala(text):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/61.0.3163.100 Safari/537.36'
        }
    text = text.replace(" ", '+')
    url = f'https://www.google.com/search?q={text}'
    response = requests.get(url, headers=usr_agent)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all( 'h3' )
    return [title.getText() for title in titles]

async def get_settings(group_id):
    settings = await db.get_settings(group_id)
    return settings
    
async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current.update({key: value})
    await db.update_settings(group_id, current)
    
def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  

def get_file_id(msg: Message):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj

def extract_user(message: Message) -> Union[int, str]:
    user_id = None
    user_first_name = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name

    elif len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == enums.MessageEntityType.TEXT_MENTION
        ):
           
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id
        try:
            user_id = int(user_id)
        except ValueError:
            pass
    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
    return (user_id, user_first_name)

def list_to_str(k):
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    elif MAX_LIST_ELM:
        k = k[:int(MAX_LIST_ELM)]
        return ' '.join(f'{elem}, ' for elem in k)
    else:
        return ' '.join(f'{elem}, ' for elem in k)

def last_online(from_user):
    time = ""
    if from_user.is_bot:
        time += "🤖 Bot :("
    elif from_user.status == enums.UserStatus.RECENTLY:
        time += "Recently"
    elif from_user.status == enums.UserStatus.LAST_WEEK:
        time += "Within the last week"
    elif from_user.status == enums.UserStatus.LAST_MONTH:
        time += "Within the last month"
    elif from_user.status == enums.UserStatus.LONG_AGO:
        time += "A long time ago :("
    elif from_user.status == enums.UserStatus.ONLINE:
        time += "Currently Online"
    elif from_user.status == enums.UserStatus.OFFLINE:
        time += from_user.last_online_date.strftime("%a, %d %b %Y, %H:%M:%S")
    return time

def split_quotes(text: str) -> List:
    if not any(text.startswith(char) for char in START_CHAR):
        return text.split(None, 1)
    counter = 1  # ignore first char -> is some kind of quote
    while counter < len(text):
        if text[counter] == "\\":
            counter += 1
        elif text[counter] == text[0] or (text[0] == SMART_OPEN and text[counter] == SMART_CLOSE):
            break
        counter += 1
    else:
        return text.split(None, 1)

    # 1 to avoid starting quote, and counter is exclusive so avoids ending
    key = remove_escapes(text[1:counter].strip())
    # index will be in range, or `else` would have been executed and returned
    rest = text[counter + 1:].strip()
    if not key:
        key = text[0] + text[0]
    return list(filter(None, [key, rest]))

def gfilterparser(text, keyword):
    if "buttonalert" in text:
        text = (text.replace("\n", "\\n").replace("\t", "\\t"))
    buttons = []
    note_data = ""
    prev = 0
    i = 0
    alerts = []
    for match in BTN_URL_REGEX.finditer(text):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            note_data += text[prev:match.start(1)]
            prev = match.end(1)
            if match.group(3) == "buttonalert":
                # create a thruple with button label, url, and newline status
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"gfilteralert:{i}:{keyword}"
                    ))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"gfilteralert:{i}:{keyword}"
                    )])
                i += 1
                alerts.append(match.group(4))
            elif bool(match.group(5)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(4).replace(" ", "")
                ))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(4).replace(" ", "")
                )])

        else:
            note_data += text[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += text[prev:]

    try:
        return note_data, buttons, alerts
    except:
        return note_data, buttons, None

def parser(text, keyword):
    if "buttonalert" in text:
        text = (text.replace("\n", "\\n").replace("\t", "\\t"))
    buttons = []
    note_data = ""
    prev = 0
    i = 0
    alerts = []
    for match in BTN_URL_REGEX.finditer(text):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            note_data += text[prev:match.start(1)]
            prev = match.end(1)
            if match.group(3) == "buttonalert":
                # create a thruple with button label, url, and newline status
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"alertmessage:{i}:{keyword}"
                    ))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"alertmessage:{i}:{keyword}"
                    )])
                i += 1
                alerts.append(match.group(4))
            elif bool(match.group(5)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(4).replace(" ", "")
                ))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(4).replace(" ", "")
                )])

        else:
            note_data += text[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += text[prev:]

    try:
        return note_data, buttons, alerts
    except:
        return note_data, buttons, None

def remove_escapes(text: str) -> str:
    res = ""
    is_escaped = False
    for counter in range(len(text)):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
    return res

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'



async def get_clone_shortlink(link, url, api):
    shortzy = Shortzy(api_key=api, base_site=url)
    link = await shortzy.convert(link)
    return link
                           
async def get_shortlink(chat_id, link):
    settings = await get_settings(chat_id) #fetching settings for group
    if 'shortlink' in settings.keys():
        URL = settings['shortlink']
        API = settings['shortlink_api']
    else:
        URL = SHORTLINK_URL
        API = SHORTLINK_API
    if URL.startswith("shorturllink") or URL.startswith("terabox.in") or URL.startswith("urlshorten.in"):
        URL = SHORTLINK_URL
        API = SHORTLINK_API
    if URL == "api.shareus.io":
        url = f'https://{URL}/easy_api'
        params = {
            "key": API,
            "link": link,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.text()
                    return data
        except Exception as e:
            logger.error(e)
            return link
    else:
        shortzy = Shortzy(api_key=API, base_site=URL)
        link = await shortzy.convert(link)
        return link
    
async def get_tutorial(chat_id):
    settings = await get_settings(chat_id) #fetching settings for group
    return settings['tutorial']
        
async def get_verify_shorted_link(link, url, api):
    API = api
    URL = url
    if URL == "api.shareus.io":
        url = f'https://{URL}/easy_api'
        params = {
            "key": API,
            "link": link,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.text()
                    return data
        except Exception as e:
            logger.error(e)
            return link
    else:
        shortzy = Shortzy(api_key=API, base_site=URL)
        link = await shortzy.convert(link)
        return link
        
async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    link = f"{link}verify-{user.id}-{token}"
    shortened_verify_url = await get_verify_shorted_link(link, VERIFY_SHORTLINK_URL, VERIFY_SHORTLINK_API)
    if VERIFY_SECOND_SHORTNER == True:
        snd_link = await get_verify_shorted_link(shortened_verify_url, VERIFY_SND_SHORTLINK_URL, VERIFY_SND_SHORTLINK_API)
        return str(snd_link)
    else:
        return str(shortened_verify_url)

async def verify_user(bot, userid, token):
    user = await bot.get_users(userid)
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    VERIFIED[user.id] = str(today)

async def check_verification(bot, userid):
    user = await bot.get_users(userid)
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    if user.id in VERIFIED.keys():
        EXP = VERIFIED[user.id]
        years, month, day = EXP.split('-')
        comp = date(int(years), int(month), int(day))
        if comp<today:
            return False
        else:
            return True
    else:
        return False  
    
async def send_all(bot, userid, files, ident, chat_id, user_name, query):
    settings = await get_settings(chat_id)
    if 'is_shortlink' in settings.keys():
        ENABLE_SHORTLINK = settings['is_shortlink']
    else:
        await save_group_settings(chat_id, 'is_shortlink', False)
        ENABLE_SHORTLINK = False
    try:
        if ENABLE_SHORTLINK:
            for file in files:
                title = file["file_name"]
                size = get_size(file["file_size"])
                if not await db.has_premium_access(userid) and SHORTLINK_MODE == True:
                    await bot.send_message(chat_id=userid, text=f"<b>Hᴇʏ ᴛʜᴇʀᴇ {user_name} 👋🏽 \n\n✅ Sᴇᴄᴜʀᴇ ʟɪɴᴋ ᴛᴏ ʏᴏᴜʀ ғɪʟᴇ ʜᴀs sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴇᴇɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ ᴅᴏᴡɴʟᴏᴀᴅ ʙᴜᴛᴛᴏɴ\n\n🗃️ Fɪʟᴇ Nᴀᴍᴇ : {title}\n🔖 Fɪʟᴇ Sɪᴢᴇ : {size}</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📤 Dᴏᴡɴʟᴏᴀᴅ 📥", url=await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}"))]]))
        else:
            for file in files:
                f_caption = file["caption"]
                title = file["file_name"]
                size = get_size(file["file_size"])
                if CUSTOM_FILE_CAPTION:
                    try:
                        file_info = get_file_info(title)
                        f_caption = CUSTOM_FILE_CAPTION.format(
                            file_name='' if title is None else title,
                            file_size='' if size is None else size,
                            file_caption='' if f_caption is None else f_caption,
                            quality=file_info['quality'],
                            season=file_info['season'],
                            episode=file_info['episode'],
                            language=file_info['language'],
                            year=file_info['year'],
                            format=file_info['format']
                        )
                    except Exception as e:
                        print(e)
                        f_caption = f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                await send_file(
                    bot=bot,
                    chat_id=userid,
                    file_id=file["file_id"],
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                            InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                        ],[
                            InlineKeyboardButton("Bᴏᴛ Oᴡɴᴇʀ", url=OWNER_LNK)
                        ]]
                    )
                )
    except UserIsBlocked:
        await query.answer('Uɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ ᴍᴀʜɴ !', show_alert=True)
    except PeerIdInvalid:
        await query.answer('Hᴇʏ, Sᴛᴀʀᴛ Bᴏᴛ Fɪʀsᴛ Aɴᴅ Cʟɪᴄᴋ Sᴇɴᴅ Aʟʟ', show_alert=True)
    except Exception as e:
        await query.answer('Hᴇʏ, Sᴛᴀʀᴛ Bᴏᴛ Fɪʀsᴛ Aɴᴅ Cʟɪᴄᴋ Sᴇɴᴅ Aʟʟ', show_alert=True)
        
async def get_cap(settings, remaining_seconds, files, query, total_results, search):
    if settings["imdb"]:
        IMDB_CAP = temp.IMDB_CAP.get(query.from_user.id)
        if IMDB_CAP:
            cap = IMDB_CAP
            cap+="<b>\n\n<u>🍿 Your Movie Files 👇</u></b>\n\n"
            for file in files:
                cap += f"<b>📁 <a href='https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}'>[{get_size(file['file_size'])}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file['file_name'].split()))}\n\n</a></b>"
        else:
            imdb = await get_poster(search, file=(files[0])["file_name"]) if settings["imdb"] else None
            if imdb:
                TEMPLATE = script.IMDB_TEMPLATE_TXT
                cap = TEMPLATE.format(
                    qurey=search,
                    title=imdb['title'],
                    votes=imdb['votes'],
                    aka=imdb["aka"],
                    seasons=imdb["seasons"],
                    box_office=imdb['box_office'],
                    localized_title=imdb['localized_title'],
                    kind=imdb['kind'],
                    imdb_id=imdb["imdb_id"],
                    cast=imdb["cast"],
                    runtime=imdb["runtime"],
                    countries=imdb["countries"],
                    certificates=imdb["certificates"],
                    languages=imdb["languages"],
                    director=imdb["director"],
                    writer=imdb["writer"],
                    producer=imdb["producer"],
                    composer=imdb["composer"],
                    cinematographer=imdb["cinematographer"],
                    music_team=imdb["music_team"],
                    distributors=imdb["distributors"],
                    release_date=imdb['release_date'],
                    year=imdb['year'],
                    genres=imdb['genres'],
                    poster=imdb['poster'],
                    plot=imdb['plot'],
                    rating=imdb['rating'],
                    url=imdb['url'],
                    **locals()
                )
                cap+="<b>\n\n<u>🍿 Your Movie Files 👇</u></b>\n\n"
                for file in files:
                    cap += f"<b>📁 <a href='https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}'>[{get_size(file['file_size'])}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file['file_name'].split()))}\n\n</a></b>"
            else:
                cap = f"<b>Tʜᴇ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ☞ {search}\n\nRᴇǫᴜᴇsᴛᴇᴅ Bʏ ☞ {query.from_user.mention}\n\nʀᴇsᴜʟᴛ sʜᴏᴡ ɪɴ ☞ {remaining_seconds} sᴇᴄᴏɴᴅs\n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ ☞ : {query.message.chat.title}\n\n⚠️ ᴀꜰᴛᴇʀ 5 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ 🗑️\n\n</b>"
                cap+="<b><u>🍿 Your Movie Files 👇</u></b>\n\n"
                for file in files:
                    cap += f"<b>📁 <a href='https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}'>[{get_size(file['file_size'])}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file['file_name'].split()))}\n\n</a></b>"
    else:
        cap = f"<b>Tʜᴇ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ☞ {search}\n\nRᴇǫᴜᴇsᴛᴇᴅ Bʏ ☞ {query.from_user.mention}\n\nʀᴇsᴜʟᴛ sʜᴏᴡ ɪɴ ☞ {remaining_seconds} sᴇᴄᴏɴᴅs\n\nᴘᴏᴡᴇʀᴇᴅ ʙʏ ☞ : {query.message.chat.title} \n\n⚠️ ᴀꜰᴛᴇʀ 5 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ 🗑️\n\n</b>"
        cap+="<b><u>🍿 Your Movie Files 👇</u></b>\n\n"
        for file in files:
            cap += f"<b>📁 <a href='https://telegram.me/{temp.U_NAME}?start=files_{file['file_id']}'>[{get_size(file['file_size'])}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file['file_name'].split()))}\n\n</a></b>"
    return cap


async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:]
        if value:
            value = int(value)
        return value, unit
    value, unit = extract_value_and_unit(time_string)
    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0

def get_file_info(file_name):
    file_name = file_name.lower()
    
    # Quality
    quality = "N/A"
    qualities = ["360p", "480p", "720p", "1080p", "1440p", "2160p", "4k", "blu-ray", "web-dl", "hdtv", "hdrip"]
    for q in qualities:
        if q in file_name:
            quality = q.upper()
            break
            
    # Season/Episode
    season = "N/A"
    episode = "N/A"
    s_match = re.search(r's(\d{1,2})', file_name)
    if s_match: season = f"S{s_match.group(1).zfill(2)}"
    e_match = re.search(r'e(\d{1,3})', file_name)
    if e_match: episode = f"E{e_match.group(1).zfill(2)}"
    
    # Language
    language = "N/A"
    languages = ["english", "hindi", "tamil", "telugu", "malayalam", "kannada", "bengali", "punjabi", "marathi", "gujarati", "dual", "multi"]
    found_langs = []
    for l in languages:
        if l in file_name:
            found_langs.append(l.title())
    if found_langs:
        language = ", ".join(found_langs)
        
    # Year
    year = "N/A"
    y_match = re.search(r'(19|20)\d{2}', file_name)
    if y_match: year = y_match.group(0)
    
    # Format
    format = "N/A"
    if "." in file_name:
        format = file_name.split(".")[-1].upper()
        
    return {
        "quality": quality,
        "season": season,
        "episode": episode,
        "language": language,
        "year": year,
        "format": format
    }

async def download_global_thumb():
    if not GLOBAL_THUMB or not GLOBAL_THUMB.startswith(("http://", "https://")):
        return GLOBAL_THUMB
    
    thumb_path = "thumbnails/global_thumb.png"
    if os.path.exists(thumb_path):
        return thumb_path
    
    if not os.path.exists("thumbnails"):
        os.makedirs("thumbnails")
        
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GLOBAL_THUMB) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(thumb_path, mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                    return thumb_path
    except Exception as e:
        logger.error(f"Error downloading global thumb: {e}")
    return None

async def send_file(bot, chat_id, file_id, caption, protect_content=False, reply_markup=None, **kwargs):
    thumb = await download_global_thumb()
    try:
        # Try sending as document with custom thumb
        return await bot.send_document(
            chat_id=chat_id,
            document=file_id,
            thumb=thumb,
            caption=caption,
            protect_content=protect_content,
            reply_markup=reply_markup,
            **kwargs
        )
    except Exception as e:
        logger.error(f"Error sending file with custom thumb: {e}. Falling back to send_cached_media.")
        return await bot.send_cached_media(
            chat_id=chat_id,
            file_id=file_id,
            caption=caption,
            protect_content=protect_content,
            reply_markup=reply_markup,
            **kwargs
        )


async def _correct_spelling_with_gemini(query):
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    prompt = (
        f"The user searched for a movie or TV series with the query: \"{query}\". "
        "Correct any misspellings in the main title. Also, carefully identify and extract any specific filters for year (e.g., 2023), quality (e.g., 1080p, 720p, 480p, 2160p, 4K), language (e.g., Hindi, Tamil, Telugu, Malayalam, English, Kannada, Dual Audio), season (format standardized as S01, S02, etc.), and episode (format standardized as E01, E02, etc.) if present in the user's query.\n"
        "Return ONLY the corrected official title followed by any extracted filters separated by spaces, without colons, symbols, or punctuation. "
        "For example, if query is 'avengrs inifinty war 1080p hndi 2018 s1 ep5', return exactly: 'Avengers Infinity War 2018 1080p Hindi S01 E05'."
    )
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        if parts:
                            corrected = parts[0].get("text", "").strip()
                            return corrected
                else:
                    err_text = await response.text()
                    logger.error(f"Gemini API returned status {response.status}: {err_text}")
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
    return None

async def correct_spelling_with_openai(query):
    if not OPENAI_API_KEY:
        return None
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    prompt = (
        f"The user searched for a movie or TV series with the query: \"{query}\". "
        "Correct any misspellings in the main title. Also, carefully identify and extract any specific filters for year (e.g., 2023), quality (e.g., 1080p, 720p, 480p, 2160p, 4K), language (e.g., Hindi, Tamil, Telugu, Malayalam, English, Kannada, Dual Audio), season (format standardized as S01, S02, etc.), and episode (format standardized as E01, E02, etc.) if present in the user's query.\n"
        "Return ONLY the corrected official title followed by any extracted filters separated by spaces, without colons, symbols, or punctuation. "
        "For example, if query is 'avengrs inifinty war 1080p hndi 2018 s1 ep5', return exactly: 'Avengers Infinity War 2018 1080p Hindi S01 E05'."
    )
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a precise movie search and filter standardization assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    choices = data.get("choices", [])
                    if choices:
                        corrected = choices[0].get("message", {}).get("content", "").strip()
                        return corrected
                else:
                    err_text = await response.text()
                    logger.error(f"OpenAI API returned status {response.status}: {err_text}")
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
    return None

async def correct_spelling_with_aiml(query):
    if not AIML_API_KEY:
        return None
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIML_API_KEY}"
    }
    prompt = (
        f"The user searched for a movie or TV series with the query: \"{query}\". "
        "Correct any misspellings in the main title. Also, carefully identify and extract any specific filters for year (e.g., 2023), quality (e.g., 1080p, 720p, 480p, 2160p, 4K), language (e.g., Hindi, Tamil, Telugu, Malayalam, English, Kannada, Dual Audio), season (format standardized as S01, S02, etc.), and episode (format standardized as E01, E02, etc.) if present in the user's query.\n"
        "Return ONLY the corrected official title followed by any extracted filters separated by spaces, without colons, symbols, or punctuation. "
        "For example, if query is 'avengrs inifinty war 1080p hndi 2018 s1 ep5', return exactly: 'Avengers Infinity War 2018 1080p Hindi S01 E05'."
    )
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "system", "content": "You are a precise movie search and filter standardization assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=10) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    choices = data.get("choices", [])
                    if choices:
                        corrected = choices[0].get("message", {}).get("content", "").strip()
                        return corrected
                else:
                    err_text = await response.text()
                    logger.error(f"AIML API returned status {response.status}: {err_text}")
    except Exception as e:
        logger.error(f"AIML API error: {e}")
    return None

async def correct_spelling_with_gemini(query):
    res = await _correct_spelling_with_gemini(query)
    if res:
        return res
    logger.info("Gemini AI failed or unavailable, falling back to OpenAI (Tier 2)...")
    res2 = await correct_spelling_with_openai(query)
    if res2:
        return res2
    logger.info("OpenAI failed or unavailable, falling back to AIML API (Tier 3)...")
    return await correct_spelling_with_aiml(query)

