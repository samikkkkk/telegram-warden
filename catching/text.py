from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from loguru import logger

from config import Config
from database.requests import GetMessage, SaveMessage, UpdateAction

bot = Config.bot
catch_text = Router()


@catch_text.business_message(F.text)
async def msg(msg: Message):
    # print(f'{msg}')

    saver = SaveMessage(
        type="text",
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        date=msg.date,
        username=msg.chat.username,
        text=msg.text,
    )
    await saver.save_text()


@catch_text.edited_business_message(F.text)
async def edit_msg(msg: Message):
    getter = GetMessage(msg.message_id)
    found, message = await getter.get_text()

    await UpdateAction(
        message_id=msg.message_id, date=msg.edit_date, text=msg.text
    ).save_message_update()

    updates_found, updates = await UpdateAction(
        message_id=msg.message_id, date=msg.edit_date, text=msg.text
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
            await bot.send_message(
                Config.OWNER_ID,
                f"📝<b>Message edited</b>\n\n"
                f"<blockquote><b>Chat information:</b>\n"
                f"<b>ID:</b> {msg.chat.id}\n"
                f'<b>Nickname:</b> {msg.chat.first_name} {msg.chat.last_name or ""}\n'
                f'<b>Username:</b> @{msg.chat.username or "No"}</blockquote>\n'
                # f'<b>Дата/время изменения:</b> {new_time.strftime("%Y-%m-%d %H:%M:%S")}</blockquote>\n\n'
                f"<b>Original text:</b>\n<blockquote>{message.text}</blockquote>\n"
                f"<b>New text:</b>\n<blockquote>{msg.text}</blockquote>\n"
                f"<b>Change history:</b>\n<blockquote>{updates_text}</blockquote>\n\n"
                f"<a href='https://github.com/samikkkkk/telegram-warden'><b>GITHUB</b></a>",
                disable_web_page_preview=True,
                parse_mode="HTML",
            )

            message.text = msg.text
            await message.save()

        except TelegramForbiddenError as e:
            me = await bot.get_me()
            logger.error(
                f"[CATCH][SEND-LOG] The message change log was not sent to the private message. Start a conversation with the bot - @{me.username}"
            )
    else:
        logger.error("Message not found or message from bot")
