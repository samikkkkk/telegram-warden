from aiogram import Bot, Router, F
from aiogram.types import Message

from config import Config
from database.requests import SaveMessage

bot = Config.bot
catch_video = Router()


@catch_video.business_message(F.video_note)
async def msg(msg: Message, bot: Bot):

    saver = SaveMessage(
        type="video",
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        date=msg.date,
        username=msg.chat.username,
        file_id=msg.video_note.file_id,
        duration=msg.video_note.duration,
    )
    await saver.save_video()
