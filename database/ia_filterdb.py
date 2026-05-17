# Don't Remove Credit #blackcatoffical
# Subscribe YouTube Channel For Amazing Bot #blackcatoffical
# Ask Doubt on telegram edison

import re, base64, json, asyncio
from struct import pack
from pyrogram.file_id import FileId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import motor.motor_asyncio
from info import FILE_DB_URI, SEC_FILE_DB_URI, DATABASE_NAME, COLLECTION_NAME, MULTIPLE_DATABASE, USE_CAPTION_FILTER, MAX_B_TN

# First Database For File Saving 
client = motor.motor_asyncio.AsyncIOMotorClient(FILE_DB_URI)
db = client[DATABASE_NAME]
col = db[COLLECTION_NAME]

# Second Database For File Saving
sec_client = motor.motor_asyncio.AsyncIOMotorClient(SEC_FILE_DB_URI)
sec_db = sec_client[DATABASE_NAME]
sec_col = sec_db[COLLECTION_NAME]


async def save_file(media):
    """Save file in the database."""
    
    file_id = unpack_new_file_id(media.file_id)
    file_name = clean_file_name(media.file_name)
    
    file = {
        'file_id': file_id,
        'file_name': file_name,
        'file_size': media.file_size,
        'caption': media.caption.html if media.caption else None
    }

    if await is_file_already_saved(file_id, file_name):
        return False, 0

    try:
        await col.insert_one(file)
        print(f"{file_name} is successfully saved.")
        return True, 1
    except DuplicateKeyError:
        print(f"{file_name} is already saved.")
        return False, 0
    except:
        if MULTIPLE_DATABASE:
            try:
                await sec_col.insert_one(file)
                print(f"{file_name} is successfully saved.")
                return True, 1
            except DuplicateKeyError:
                print(f"{file_name} is already saved.")
                return False, 0
        else:
            print("Your Current File Database Is Full, Turn On Multiple Database Feature And Add Second File Mongodb To Save File.")

def clean_file_name(file_name):
    """Clean and format the file name."""
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(file_name)) 
    unwanted_chars = ['[', ']', '(', ')', '{', '}']
    
    for char in unwanted_chars:
        file_name = file_name.replace(char, ' ')
        
    cleaned_name = ' '.join(filter(lambda x: not x.startswith('@') and not x.startswith('http') and not x.startswith('www.') and not x.startswith('t.me'), file_name.split()))
    return cleaned_name if cleaned_name else str(file_name)

async def is_file_already_saved(file_id, file_name):
    """Check if the file is already saved in either collection."""
    found = {'file_id': file_id}

    for collection in [col, sec_col]:
        if await collection.find_one(found):
            return True
            
    return False

async def get_search_results(chat_id, query, file_type=None, max_results=10, offset=0, filter=False):
    """For given query return (results, next_offset)"""
    
    query = query.strip()
    if not query:
        raw_pattern = '.'
    else:
        words = query.split()
        raw_pattern = r'^' + r''.join(f'(?=.*\\b{re.escape(word)}\\b)' for word in words)
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        regex = query
    filter_criteria = {'file_name': regex}
    files = []
    
    if MULTIPLE_DATABASE:
        # Run both queries in parallel for speed
        results = await asyncio.gather(
            col.find(filter_criteria).sort('$natural', -1).skip(offset).limit(max_results).to_list(length=max_results),
            sec_col.find(filter_criteria).sort('$natural', -1).skip(offset).limit(max_results).to_list(length=max_results)
        )
        for cursor in results:
            for file in cursor:
                files.append(file)
        
        # Count in parallel too
        counts = await asyncio.gather(
            col.count_documents(filter_criteria),
            sec_col.count_documents(filter_criteria)
        )
        total_results = sum(counts)
    else:
        files = await col.find(filter_criteria).sort('$natural', -1).skip(offset).limit(max_results).to_list(length=max_results)
        total_results = await col.count_documents(filter_criteria)

    next_offset = "" if (offset + max_results) >= total_results else (offset + max_results)
    return files, next_offset, total_results

async def get_bad_files(query, file_type=None, use_filter=False):
    """For given query return (results, next_offset)"""
    query = query.strip()
    
    if not query:
        raw_pattern = '.'
    else:
        words = query.split()
        raw_pattern = r'^' + r''.join(f'(?=.*\\b{re.escape(word)}\\b)' for word in words)
    
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except re.error:
        return [], 0

    filter_criteria = {'file_name': regex}
    if USE_CAPTION_FILTER:
        filter_criteria = {'$or': [filter_criteria, {'caption': regex}]}

    async def count_docs(collection):
        return await collection.count_documents(filter_criteria)

    if MULTIPLE_DATABASE:
        total_results = await count_docs(col) + await count_docs(sec_col)
    else:
        total_results = await count_docs(col)

    async def find_docs(collection):
        return await collection.find(filter_criteria).to_list(length=None)

    if MULTIPLE_DATABASE:
        files = await find_docs(col) + await find_docs(sec_col)
    else:
        files = await find_docs(col)

    return files, total_results

async def get_file_details(query):
    return await col.find_one({'file_id': query}) or await sec_col.find_one({'file_id': query})

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0
    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0
            r += bytes([i])
    return base64.urlsafe_b64encode(r).decode().rstrip("=")
    
def unpack_new_file_id(new_file_id):
    """Return file_id"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    return file_id
    
