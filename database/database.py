import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def get_thumbnail(id):
    try:
        thumbnail = await user_data.find_one({'id': int(id)})
        if thumbnail:
            return thumbnail.get('file_id')
        else:
            return None
    except Exception as e:
        print(e)

async def set_thumbnail(id, file_id):
    await user_data.update_one({'id': int(id)}, {'$set': {'file_id': file_id}})


async def get_thumbnail(id):
    try:
        thumbnail = await user_data.find_one({'id': int(id)})
        if thumbnail:
            return thumbnail.get('file_id')
        else:
            return None
    except Exception as e:
        print(e)
# Born to make history @LazyDeveloper ! => Remember this name forever <=

async def set_caption(id, caption):
    await user_data.update_one({'id': int(id)}, {'$set': {'caption': caption}})

async def get_caption(id):
    user = await user_data.find_one({'id': int(id)})
    return user.get('caption', None)

async def get_lazy_thumbnail(id):
    user = await user_data.find_one({'id': int(id)})
    return user.get('thumbnail', None)

async def get_lazy_caption(id):
    user = await user_data.find_one({'id': int(id)})
    return user.get('lazy_caption', None)

async def set_lazy_thumbnail(id, thumbnail):
    await user_data.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})

# Born to make history @LazyDeveloper ! => Remember this name forever <=
