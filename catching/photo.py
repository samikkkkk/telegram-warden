from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from loguru import logger

from config import Config
from database.requests import GetMessage, SaveMessage, UpdateAction

bot = Config.bot
catch_photo = Router()


@catch_photo.business_message(F.photo)
async def msg(msg: Message, bot: Bot):
    # print(f'{msg}')

    saver = SaveMessage(
        type="photo",
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        date=msg.date,
        username=msg.chat.username,
        file_id=msg.photo[-1].file_id,
        caption=msg.caption,
    )
    await saver.save_photo()


@catch_photo.edited_business_message(F.photo)
async def edit_msg(msg: Message, bot: Bot):
    getter = GetMessage(msg.message_id)
    found, message = await getter.get_photo()

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
            await bot.send_photo(
                chat_id=Config.OWNER_ID,
                photo=message.file_id,
                caption=f"📝<b>Message edited</b>\n\n"
                f"<blockquote><b>Chat information:</b>\n"
                f"<b>ID:</b> {msg.chat.id}\n"
                f'<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name or ""}\n'
                f'<b>Username:</b> @{msg.chat.username or "No"}</blockquote>\n\n'
                f'<b>Original caption:</b>\n<blockquote>{message.caption or "No"}</blockquote>\n'
                f'<b>New caption:</b>\n<blockquote>{msg.caption or "Нет"}</blockquote>\n'
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
        logger.error(f"Message not found/from a bot")
