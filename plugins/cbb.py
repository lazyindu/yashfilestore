
from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
import asyncio
from lazydeveloperr.handlers import save_batch_media_in_channel
LazyList = {}

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
