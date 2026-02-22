from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from loguru import logger

from config import Config
from database.requests import GetMessage, SaveMessage, UpdateAction

bot = Config.bot
catch_doc = Router()


@catch_doc.business_message(F.document)
async def msg(msg: Message, bot: Bot):

    saver = SaveMessage(
        type="doc",
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        date=msg.date,
        username=msg.chat.username,
        file_id=msg.document.file_id,
        file_name=msg.document.file_name,
        mime_type=msg.document.mime_type,
        caption=msg.caption,
    )
    await saver.save_doc()


@catch_doc.edited_business_message(F.document)
async def edit_msg(msg: Message, bot: Bot):
    getter = GetMessage(msg.message_id)
    found, message = await getter.get_doc()

    await UpdateAction(
        message_id=msg.message_id, date=msg.edit_date, text=msg.caption or "No caption"
    ).save_message_update()

    updates_found, updates = await UpdateAction(
        message_id=msg.message_id, date=msg.edit_date, text=msg.caption
    ).get_message_updates()

    updates_text = ""
    if updates_found and updates:
        updates_text = "\n".join(
            [
                f"{update.date.strftime('%Y-%m-%d %H:%M:%S')}\n ┗{update.new_text}\n"
                for update in updates
            ]
        )
        
    else:
        updates_text = "No change history"

    if not msg.from_user.is_bot and found:
        try:
            await bot.send_document(
                chat_id=Config.OWNER_ID,
                document=message.file_id,
                caption=f"📝<b>Message edited</b>\n\n"
                f"<blockquote><b>Chat information:</b>\n"
                f"<b>ID:</b> {msg.chat.id}\n"
                f'<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name or ""}\n'
                f'<b>Username:</b> @{msg.chat.username or "No"}</blockquote>\n\n'
                f"<b>📁File information</b>\n"
                f"<blockquote><b>File name:</b> {msg.document.file_name}\n"
                f"<b>File weight:</b> {round(msg.document.file_size/1024, 2)} КБ\n"
                f"<b>File type:</b> {msg.document.mime_type}</blockquote>\n\n"
                f'<b>Original description:</b>\n<blockquote>{message.caption or "No"}</blockquote>\n'
                f'<b>New description:</b>\n<blockquote>{msg.caption or "No"}</blockquote>\n'
                f"<b>Change history:</b>\n<blockquote>{updates_text}</blockquote>\n\n"
                f"<a href='https://github.com/samikkkkk/telegram-warden'><b>GITHUB</b></a>",
                disable_web_page_preview=True,
                parse_mode="HTML",
            )
            message.caption = msg.caption
            await message.save()
        except TelegramForbiddenError:
            me = await bot.get_me()
            logger.error(
                f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
            )

    else:
        logger.error("Message not found/from bot")
