    # Credit @LazyDeveloper.
    # Please Don't remove credit.
    # Born to make history @LazyDeveloper !

    # Thank you LazyDeveloper for helping us in this Journey
    # 🥰  Thank you for giving me credit @LazyDeveloperr  🥰

    # for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 

from pyrogram import Client, filters
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import random
import os
from PIL import Image

# the Strings used for this "thing"
from pyrogram import Client
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
from database.lazy_ffmpeg import take_screen_shot
from config import DOWNLOAD_LOCATION
from database.database import set_caption, set_thumbnail, get_caption, get_thumbnail, get_lazy_thumbnail, set_lazy_thumbnail,addthumb
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from database.database import add_user, del_user, full_userbase, present_user

@Client.on_message(filters.private & filters.command(['view_thumb','view_thumbnail','vt']))
async def viewthumb(client, message):
    id = message.from_user.id
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass

    thumb = await get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(
	   chat_id=message.chat.id, 
	   photo=thumb,
       caption=f"Current thumbnail for direct renaming",
       reply_markup=InlineKeyboardMarkup([
           [InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ" , callback_data="deleteThumbnail")]
       ]))
    else:
        await message.reply_text("😔**Sorry ! No thumbnail found...**😔") 

@Client.on_message(filters.private & filters.command(['del_thumb','delete_thumb','dt']))
async def removethumb(client, message):
    id = message.from_user.id
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")
            pass

    await set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Okay sweetie, I deleted your custom thumbnail for direct renaming. Now I will apply default thumbnail. ✅️**✅️")

@Client.on_message(filters.private & filters.command(['set_thumbnail','set_thumb','st']))
async def addthumbs(client, message):
    try:
        replied = message.reply_to_message
        id = message.from_user.id
        if not message.from_user:
            return await message.reply_text("What the hell is this...")
        
        if not await present_user(id):
            try:
                await add_user(id)
            except Exception as e:
                print(f"Error adding user: {e}")
                pass

        LazyDev = await message.reply_text("Please Wait ...")
            # Check if there is a replied message and it is a photo
        if replied and replied.photo:
            # Save the photo file_id as a thumbnail for the user
            await set_thumbnail(message.from_user.id, file_id=replied.photo.file_id)
            await LazyDev.edit("**✅ Custom thumbnail set successfully!**")
        else:
            await LazyDev.edit("**❌ Please reply to a photo to set it as a custom thumbnail.**")
    except Exception as lazyerror :
        print(f'Here comes error : {lazyerror}')

@Client.on_message(filters.private & filters.photo)
async def addthumbnail(client,message):
	file_id = str(message.photo.file_id)
	addthumb(message.chat.id , file_id)
	await message.reply_text("**Custom thumbnail saved successfully** ✅")

async def Gthumb01(bot, update):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await get_lazy_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await get_lazy_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))

    return thumbnail

async def Mdata01(download_directory):
          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
          return width, height, duration

async def Mdata02(download_directory):
          width = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")

          return width, duration

async def Mdata03(download_directory):

          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds

          return duration
