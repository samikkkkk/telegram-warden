import os
from datetime import timedelta

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.exceptions import TelegramForbiddenError

from loguru import logger

from config import Config
from utils.get_file import get_file

catch_destructing = Router()

"""
The saving/capturing of self-destructing messages is implemented differently than other types of catching 
because aiogram cannot catch messages of this type (SelfDestructingPhoto, SelfDestructingVoice, SelfDestructingVideoNote, etc.), 
and it is also not possible to send such files via file_id. 

We obtain the message object by responding to the message with self-destructing content. 
After catching the response, we get the ID of the photo/voice/video note and temporarily download it to the device(via utils/get_file), 
and then we send its log locally from the device before deleting it.
"""
@catch_destructing.business_message(
    F.reply_to_message.has_protected_content == True, F.reply_to_message.photo
)
async def photo(msg: Message, bot: Bot):

    if msg.reply_to_message.photo:
        path = await get_file(msg.reply_to_message.photo[-1].file_id, bot)
        new_time = msg.reply_to_message.date + timedelta(hours=3)

        try:
            await bot.send_photo(
                chat_id=Config,
                photo=FSInputFile(path=path),
                caption=f"✅ Photo catched!\n\n"
                f"<b>Chat information:</b>\n"
                f"<blockquote><b>ID:</b> {msg.reply_to_message.chat.id}\n"
                f"<b>Nickname:</b> {msg.reply_to_message.chat.first_name} {msg.reply_to_message.chat.last_name}\n"
                f"<b>Username:</b> @{msg.reply_to_message.chat.username}\n"
                f'<b>Date/time of sending:</b> {new_time.strftime("%Y-%m-%d %H:%M:%S")}</blockquote>\n\n',
                parse_mode="HTML",
            )
            os.remove(path=path)

        except TelegramForbiddenError:
            me = await bot.get_me()
            logger.error(
                f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
            )


@catch_destructing.business_message(
    F.reply_to_message.has_protected_content == True, F.reply_to_message.video_note
)
async def video_note(msg: Message, bot: Bot):
    if msg.reply_to_message.video_note:
        path = await get_file(msg.reply_to_message.video_note.file_id, bot)
        new_time = msg.reply_to_message.date + timedelta(hours=3)

        try:
            await bot.send_video_note(chat_id=Config.OWNER_ID, video_note=path)

            await bot.send_message(
                chat_id=Config.OWNER_ID,
                text=f"✅ Video-note catched!\n\n"
                f"<b>Chat information:</b>\n"
                f"<blockquote><b>ID:</b> {msg.reply_to_message.chat.id}\n"
                f"<b>Nickname:</b> {msg.reply_to_message.chat.first_name} {msg.reply_to_message.chat.last_name}\n"
                f"<b>Username:</b> @{msg.reply_to_message.chat.username}\n"
                f'<b>Date/time of sending:</b> {new_time.strftime("%Y-%m-%d %H:%M:%S")}</blockquote>\n\n',
                parse_mode="HTML",
            )
            os.remove(path=path)

        except TelegramForbiddenError:
            me = await bot.get_me()
            logger.error(
                f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
            )


@catch_destructing.business_message(
    F.reply_to_message.has_protected_content == True, F.reply_to_message.voice
)
async def voice(msg: Message, bot: Bot):
    if msg.reply_to_message.voice:
        path = await get_file(msg.reply_to_message.voice.file_id, bot)
        new_time = msg.reply_to_message.date + timedelta(hours=3)

        try:
            await bot.send_voice(
                chat_id=Config.OWNER_ID,
                voice=FSInputFile(path=path),
                caption=f"✅ Voice catched!\n\n"
                f"<b>Chat information:</b>\n"
                f"<blockquote><b>ID:</b> {msg.reply_to_message.chat.id}\n"
                f"<b>Nickname:</b> {msg.reply_to_message.chat.first_name} {msg.reply_to_message.chat.last_name}\n"
                f"<b>Username:</b> @{msg.reply_to_message.chat.username}\n"
                f'<b>Date/time of sending:</b> {new_time.strftime("%Y-%m-%d %H:%M:%S")}</blockquote>\n\n',
                parse_mode="HTML",
            )
            os.remove(path=path)

        except TelegramForbiddenError:
            me = await bot.get_me()
            logger.error(
                f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
            )


@catch_destructing.business_message(
    F.reply_to_message.has_protected_content == True, F.reply_to_message.video
)
async def video(msg: Message, bot: Bot):
    if msg.reply_to_message.video:
        path = await get_file(msg.reply_to_message.video.file_id, bot)
        new_time = msg.reply_to_message.date + timedelta(hours=3)

        try:
            await bot.send_video(
                chat_id=Config.OWNER_ID,
                video=FSInputFile(path=path),
                caption=f"✅ Video catched!\n\n"
                f"<b>Chat information:</b>\n"
                f"<blockquote><b>ID:</b> {msg.reply_to_message.chat.id}\n"
                f"<b>Nickname:</b> {msg.reply_to_message.chat.first_name} {msg.reply_to_message.chat.last_name}\n"
                f"<b>Username:</b> @{msg.reply_to_message.chat.username}\n"
                f'<b>Date/time of sending:</b> {new_time.strftime("%Y-%m-%d %H:%M:%S")}</blockquote>\n\n',
                parse_mode="HTML",
            )
            os.remove(path=path)

        except TelegramForbiddenError:
            me = await bot.get_me()
            logger.error(
                f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
            )
