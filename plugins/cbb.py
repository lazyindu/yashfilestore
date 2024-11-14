
from pyrogram import __version__, filters
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply
from config import *
import asyncio
from lazydeveloperr.handlers import save_batch_media_in_channel
LazyList = {}
from lazydeveloperr.renameutils import progress_for_pyrogram
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os 
import humanize
from PIL import Image
from database.database import get_thumbnail, set_caption, get_caption
import logging
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

@Bot.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	user_id = update.message.chat.id
	date = update.message.date
	await update.message.delete()
	await update.message.reply_text("»»——— 𝙋𝙡𝙚𝙖𝙨𝙚 𝙚𝙣𝙩𝙚𝙧 𝙣𝙚𝙬 𝙛𝙞𝙡𝙚 𝙣𝙖𝙢𝙚...",	
	reply_to_message_id=update.message.reply_to_message.id,  
	reply_markup=ForceReply(True))  
    
# Born to make history @LazyDeveloper !
@Bot.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    try:
        type = update.data.split("_")[1]
        new_name = update.message.text
        new_filename = new_name.split(":-")[1]
        file = update.message.reply_to_message
        file_path = f"downloads/{new_filename}"
        ms = await update.message.edit("\n༻☬ད 𝘽𝙪𝙞𝙡𝙙𝙞𝙣𝙜 𝙇𝙖𝙯𝙮 𝙈𝙚𝙩𝙖𝘿𝙖𝙩𝙖...")
        c_time = time.time()
        try:
            path = await bot.download_media(
                    message=file,
                    progress=progress_for_pyrogram,
                    progress_args=("**\n  ღ♡ ꜰɪʟᴇ ᴜɴᴅᴇʀ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ... ♡♪**", ms, c_time))
        except Exception as e:
            await ms.edit(e)
            return
        splitpath = path.split("/downloads/")
        dow_file_name = splitpath[1]
        old_file_name =f"downloads/{dow_file_name}"
        os.rename(old_file_name, file_path)
        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
               duration = metadata.get('duration').seconds
        except:
            pass
        user_id = int(update.message.chat.id) 
        ph_path = None 
        media = getattr(file, file.media.value)
        filesize = humanize.naturalsize(media.file_size) 
        c_caption = await get_caption(update.message.chat.id)
        c_thumb = await get_thumbnail(update.message.chat.id)
        if c_caption:
             try:
                 caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size), duration=convert(duration))
             except Exception as e:
                 await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
                 return 
        else:
            caption = f"**{new_filename}** \n\n⚡️Data costs: `{filesize}`"
        if (media.thumbs or c_thumb):
            if c_thumb:
               ph_path = await bot.download_media(c_thumb) 
            else:
               ph_path = await bot.download_media(media.thumbs[0].file_id)
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")
        await ms.edit("三 𝘗𝘳𝘦𝘱𝘢𝘳𝘪𝘯𝘨 𝘵𝘰 𝘳𝘦𝘤𝘦𝘪𝘷𝘦 𝘓𝘢𝘻𝘺 𝘧𝘪𝘭𝘦...︻デ═一")
        c_time = time.time() 
        try:
           if type == "document":
              await bot.send_document(
	            update.message.chat.id,
                       document=file_path,
                       thumb=ph_path, 
                       caption=caption, 
                       progress=progress_for_pyrogram,
                       progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time))
           
           elif type == "video": 
               await bot.send_video(
	            update.message.chat.id,
	            video=file_path,
	            caption=caption,
	            thumb=ph_path,
	            duration=duration,
	            progress=progress_for_pyrogram,
	            progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time))
           elif type == "audio": 
               await bot.send_audio(
	            update.message.chat.id,
	            audio=file_path,
	            caption=caption,
	            thumb=ph_path,
	            duration=duration,
	            progress=progress_for_pyrogram,
	            progress_args=( "**⎝⎝✧ ʀᴇᴄɪᴇᴠɪɴɢ ꜰɪʟᴇ ꜰʀᴏᴍ ʟᴀᴢʏ ꜱᴇʀᴠᴇʀ ✧⎠⎠**",  ms, c_time   )) 
        except Exception as e: 
            await ms.edit(f" Erro {e}") 
            os.remove(file_path)
            if ph_path:
              os.remove(ph_path)
            return 
        await ms.delete() 
        os.remove(file_path) 
        if ph_path:
           os.remove(ph_path) 
    except Exception as e:
        logger.error(f"error 2 : {e}")


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"○ Owner : <a href='https://t.me/Simplifytuber'>❤ Simplifytuber ❤</a>\n○  Updates Channel: <a href='https://t.me/simplifytuberyt'> simplifytuberyt </a> </b>\n\n○ Dev : <a href='https://t.me/LazyDeveloperr'>❤LazyDeveloperr❤</a>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton("⚡️ ᴄʟᴏsᴇ", callback_data = "close"),
                    InlineKeyboardButton('🍁 ᴘʀᴇᴍɪᴜᴍ', url='https://t.me/Simplifytuber')
                    ]
                ]
            )
        )
    
    elif "addToLazyBatch" in data:
            if LazyList.get(f"{str(query.from_user.id)}", None) is None:
                LazyList[f"{str(query.from_user.id)}"] = []
            file_id = query.message.reply_to_message.id
            LazyList[f"{str(query.from_user.id)}"].append(file_id)
            await query.message.edit("This file is added to Batch List!\n\n"
                                "Press below button to get batch link or just send another file and click on Add to Batch list.",
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("⚡️ ɢᴇᴛ ʙᴀᴛᴄʜ ꜰɪʟᴇꜱ ⚡️", callback_data="getBatchLink")],
                                    [InlineKeyboardButton("Close Message", callback_data="close")]
                                ]))
    
    elif "getBatchLink" in data:
            message_ids = LazyList.get(f"{str(query.from_user.id)}", None)
            if message_ids is None:
                await query.answer("ʙᴀᴛᴄʜ ʟɪꜱᴛ ᴇᴍᴘᴛʏ!", show_alert=True)
                return
            await query.message.edit("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ, ɢᴇɴᴇʀᴀᴛɪɴɢ ʙᴀᴛᴄʜ ʟɪɴᴋ...")
            await save_batch_media_in_channel(bot=client, editable=query.message, message_ids=message_ids)
            LazyList[f"{str(query.from_user.id)}"] = []

    elif data.startswith("ban_user_"):
        user_id = data.split("_", 2)[-1]
        if FORCE_SUB_CHANNEL and FORCE_SUB_CHANNEL2 and FORCE_SUB_CHANNEL3 is None:
            await query.answer("ꜱᴏʀʀʏ ꜱɪʀ, ʏᴏᴜ ᴅɪᴅɴ'ᴛ ꜱᴇᴛ ᴀɴʏ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ!", show_alert=True)
            return
        if not int(query.from_user.id) == OWNER_ID:
            await query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True)
            return
        try:
            await client.kick_chat_member(chat_id=int(FORCE_SUB_CHANNEL), user_id=int(user_id))
            asyncio.sleep(1)
            await client.kick_chat_member(chat_id=int(FORCE_SUB_CHANNEL2), user_id=int(user_id))
            asyncio.sleep(1)
            await client.kick_chat_member(chat_id=int(FORCE_SUB_CHANNEL3), user_id=int(user_id))
            await query.answer("USEƦ BANNED FƦOM ALL UPDATES CHANNEL!", show_alert=True)
        except Exception as e:
            await query.answer(f"ᴄᴀɴ'ᴛ ʙᴀɴ ʜɪᴍ!\n\nError: {e}", show_alert=True)

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
