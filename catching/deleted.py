from aiogram import Router
from aiogram.types.business_messages_deleted import BusinessMessagesDeleted
from aiogram.exceptions import TelegramForbiddenError

from loguru import logger

from config import Config
from database.requests import GetMessage

bot = Config.bot
catch_deleted = Router()


@catch_deleted.deleted_business_messages()
async def handle_deleted_messages(msg: BusinessMessagesDeleted):
    me = await bot.get_me()

    for message_id in msg.message_ids:
        getter = GetMessage(message_id)
        
        for method_name in [
            "get_text",
            "get_photo",
            "get_doc",
            "get_voice",
            "get_video",
        ]:
            method = getattr(getter, method_name)
            found, message = await method()

            if found:
                msg_type = method_name.replace("get_", "")

                if msg_type == "text":
                    try:
                        await bot.send_message(
                            Config.OWNER_ID,
                            f"🚫 <b>Text message deleted</b>\n\n"
                            f"<b>Chat information:</b>\n"
                            f"<b>ID:</b> {msg.chat.id}\n"
                            f"<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name}\n"
                            f"<b>Username:</b> @{msg.chat.username}\n\n"
                            f"<b>Text:</b>\n<blockquote>{message.text}</blockquote>",
                            parse_mode="HTML",
                        )
                    except TelegramForbiddenError as e:
                        logger.error(
                            f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
                        )

                elif msg_type == "photo":
                    try:
                        await bot.send_photo(
                            chat_id=Config.OWNER_ID,
                            photo=message.file_id,
                            caption=f"🚫 <b>Photo message deleted</b>\n\n"
                            f"<b>Chat information:</b>\n"
                            f"<b>ID:</b> {msg.chat.id}\n"
                            f"<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name}\n"
                            f"<b>Username:</b> @{msg.chat.username}\n\n"
                            f"<b>Caption:</b>\n<blockquote>{message.caption or "No"}</blockquote>\n\n"
                            f"<tg-spoiler>Photo attached above.</tg-spoiler>",
                            parse_mode="HTML",
                        )
                    except TelegramForbiddenError as e:
                        logger.error(
                            f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
                        )

                elif msg_type == "doc":
                    try:
                        await bot.send_document(
                            chat_id=Config.OWNER_ID,
                            document=message.file_id,
                            caption=f"🚫 <b>File message deleted</b>\n\n"
                            f"<b>Chat information:</b>\n"
                            f"<b>ID:</b> {msg.chat.id}\n"
                            f"<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name}\n"
                            f"<b>Username:</b> @{msg.chat.username}\n\n"
                            f"<b>Caption:</b>\n<blockquote>{message.caption or "No"}</blockquote>\n\n"
                            f"<tg-spoiler>Document attached above.</tg-spoiler>",
                            parse_mode="HTML",
                        )
                    except TelegramForbiddenError as e:
                        logger.error(
                            f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
                        )

                elif msg_type == "voice":
                    try:
                        await bot.send_voice(
                            chat_id=Config.OWNER_ID,
                            voice=message.file_id,
                            caption=f"🚫 <b>Voice message deleted</b>\n\n"
                            f"<b>Chat information:</b>\n"
                            f"<b>ID:</b> {msg.chat.id}\n"
                            f"<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name}\n"
                            f"<b>Username:</b> @{msg.chat.username}\n\n"
                            f"<b>Duration:</b> <blockquote>{message.duration}</blockquote>\n"
                            f'<b>Caption:</b>\n<blockquote>{message.caption or "No"}</blockquote>\n\n'
                            f"<tg-spoiler>Voice attached above.</tg-spoiler>",
                            parse_mode="HTML",
                        )
                    except TelegramForbiddenError as e:
                        logger.error(
                            f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
                        )

                elif msg_type == "video":
                    try:
                        """
                        Video_note does not support message captions.
                        We send the log in two messages
                        """
                        await bot.send_video_note(
                            chat_id=Config.OWNER_ID, video_note=message.file_id
                        )
                        await bot.send_message(
                            chat_id=Config.OWNER_ID,
                            text=f"🚫 <b>Video-note deleted</b>\n\n"
                            f"<b>Chat information:</b>\n"
                            f"<b>ID:</b> {msg.chat.id}\n"
                            f"<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name}\n"
                            f"<b>Username:</b> @{msg.chat.username}\n\n"
                            f"<b>Duration:</b> {message.duration} second(s)\n"
                            f"<tg-spoiler>Video-note attached above.</tg-spoiler>",
                            parse_mode="HTML",
                        )
                    except TelegramForbiddenError as e:
                        logger.error(
                            f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
                        )

                await message.delete()
                break
