from loguru import logger

from database.structure import (
    TextMessage,
    PhotoMessage,
    DocumentMessage,
    VideoMessage,
    VoiceMessage,
    Update,
)


class GetMessage:
    def __init__(self, message_id):
        self.message_id = message_id

    async def get_text(self):
        msg = await TextMessage.filter(message_id=self.message_id).first()

        if msg:
            logger.debug(
                "[DATABASE][REQUESTS][GET-MESSAGE] Text message successfully found"
            )
            return True, msg
        
        else:
            logger.warning("[DATABASE][REQUESTS][GET-MESSAGE] Text message not found")
            return False, msg

    async def get_photo(self):
        msg = await PhotoMessage.filter(message_id=self.message_id).first()

        if msg:
            logger.debug(
                "[DATABASE][REQUESTS][GET-MESSAGE] Photo message successfully found"
            )
            return True, msg
        
        else:
            logger.warning("[DATABASE][REQUESTS][GET-MESSAGE] Photo message not found")
            return False, msg

    async def get_doc(self):
        msg = await DocumentMessage.filter(message_id=self.message_id).first()

        if msg:
            logger.debug(
                "[DATABASE][REQUESTS][GET-MESSAGE] Doc message successfully found"
            )
            return True, msg
        
        else:
            logger.warning("[DATABASE][REQUESTS][GET-MESSAGE] Doc message not found")
            return False, msg

    async def get_voice(self):
        msg = await VoiceMessage.filter(message_id=self.message_id).first()

        if msg:
            logger.debug(
                "[DATABASE][REQUESTS][GET-MESSAGE] Voice message successfully found"
            )
            return True, msg
        
        else:
            logger.warning("[DATABASE][REQUESTS][GET-MESSAGE] Voice message not found")
            return False, msg

    async def get_video(self):
        msg = await VideoMessage.filter(message_id=self.message_id).first()

        if msg:
            logger.debug(
                "[DATABASE][REQUESTS][GET-MESSAGE] Video message successfully found"
            )
            return True, msg
        
        else:
            logger.warning("[DATABASE][REQUESTS][GET-MESSAGE] Video message not found")
            return False, msg


class SaveMessage:
    def __init__(self, type, message_id, chat_id, date, username, **kwargs):
        self.message_id = message_id
        self.type = type
        self.chat_id = chat_id
        self.date = date
        self.username = username
        self.text = kwargs.get("text", "Нет")
        self.file_id = kwargs.get(
            "file_id",
            "https://upload.wikimedia.org/wikipedia/commons/3/3d/%D0%9D%D0%B5%D1%82_%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F.jpg",
        )
        self.caption = kwargs.get("caption", "No")
        self.file_name = kwargs.get("file_name", "No")
        self.mime_type = kwargs.get("mime_type", "No")
        self.duration = kwargs.get("duration", "No")

    async def save_text(self):
        try:
            msg = await TextMessage.create(
                message_id=self.message_id,
                date=self.date,
                chat_id=self.chat_id,
                username=self.username,
                text=self.text,
            )
            logger.success(
                "[DATABASE][REQUESTS][SAVE-MESSAGE] Text message successfully saved"
            )
            return True, msg
        
        except Exception as e:
            logger.error(
                f"[DATABASE][REQUESTS][SAVE-MESSAGE] Text message not saved with error: {e}"
            )
            return False, e

    async def save_photo(self):
        try:
            msg = await PhotoMessage.create(
                message_id=self.message_id,
                date=self.date,
                chat_id=self.chat_id,
                username=self.username,
                file_id=self.file_id,
                caption=self.caption,
            )
            logger.success(
                "[DATABASE][REQUESTS][SAVE-MESSAGE] Photo message successfully saved"
            )
            return True, msg
        
        except Exception as e:
            logger.error(
                f"[DATABASE][REQUESTS][SAVE-MESSAGE] Photo message not saved with error: {e}"
            )
            return False, e

    async def save_doc(self):
        try:
            msg = await DocumentMessage.create(
                message_id=self.message_id,
                date=self.date,
                chat_id=self.chat_id,
                username=self.username,
                file_id=self.file_id,
                file_name=self.file_name,
                mime_type=self.mime_type,
                caption=self.caption,
            )
            logger.success(
                "[DATABASE][REQUESTS][SAVE-MESSAGE] Doc message successfully saved"
            )
            return True, msg
        
        except Exception as e:
            logger.error(
                f"[DATABASE][REQUESTS][SAVE-MESSAGE] Doc message not saved with error: {e}"
            )
            return False, e

    async def save_voice(self):
        try:
            msg = await VoiceMessage.create(
                message_id=self.message_id,
                date=self.date,
                chat_id=self.chat_id,
                username=self.username,
                file_id=self.file_id,
                duration=self.duration,
            )
            logger.success(
                "[DATABASE][REQUESTS][SAVE-MESSAGE] Voice message successfully saved"
            )
            return True, msg
        
        except Exception as e:
            logger.error(
                f"[DATABASE][REQUESTS][SAVE-MESSAGE] Voice message not saved with error: {e}"
            )
            return False, e

    async def save_video(self):
        try:
            msg = await VideoMessage.create(
                message_id=self.message_id,
                date=self.date,
                chat_id=self.chat_id,
                username=self.username,
                file_id=self.file_id,
                duration=self.duration,
            )
            logger.success(
                "[DATABASE][REQUESTS][SAVE-MESSAGE] Video message successfully saved"
            )
            return True, msg
        
        except Exception as e:
            logger.error(
                f"[DATABASE][REQUESTS][SAVE-MESSAGE] Video message not saved with error: {e}"
            )
            return False, e


class UpdateAction:
    def __init__(self, message_id, date, text):
        self.message_id = message_id
        self.date = date
        self.text = text

    async def save_message_update(self):
        try:
            update = await Update.create(
                message_id=self.message_id, new_text=self.text, date=self.date
            )
            logger.success(
                "[DATABASE][REQUESTS][SAVE-UPDATE] Update successfully saved"
            )
            return True, update
        
        except Exception as e:
            logger.error(
                f"[DATABASE][REQUESTS][SAVE-UPDATE] Update not saved with error: {e}"
            )
            return False, e

    async def get_message_updates(self):
        try:
            updates = await Update.filter(message_id=self.message_id).all()
            logger.success(
                "[DATABASE][REQUESTS][GET-UPDATES] Updates received successfully"
            )
            return True, updates
        
        except Exception as e:
            logger.success(
                f"[DATABASE][REQUESTS][GET-UPDATES] Updates not found/with error: {e}"
            )
            return False, e
