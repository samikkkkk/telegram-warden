from loguru import logger
from tortoise import models, Tortoise, fields

from config import Config


class BaseMessage(models.Model):
    id = fields.IntField(pk=True)
    message_id = fields.BigIntField()
    date = fields.DatetimeField()
    chat_id = fields.BigIntField()
    username = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TextMessage(BaseMessage):
    text = fields.TextField()


class PhotoMessage(BaseMessage):
    file_id = fields.CharField(max_length=255)
    caption = fields.TextField(null=True)


class DocumentMessage(BaseMessage):
    file_id = fields.CharField(max_length=255)
    file_name = fields.CharField(max_length=255)
    mime_type = fields.CharField(max_length=100)
    caption = fields.CharField(max_length=1024, null=True)


class VoiceMessage(BaseMessage):
    file_id = fields.CharField(max_length=255)
    duration = fields.IntField()
    caption = fields.CharField(max_length=1024, null=True)


class VideoMessage(BaseMessage):
    file_id = fields.CharField(max_length=255)
    duration = fields.IntField()


class Update(models.Model):
    message_id = fields.BigIntField()
    new_text = fields.CharField(max_length=1024)
    date = fields.DatetimeField()


async def init_db():
    await Tortoise.init(
        Config.TORTOISE_CONFIG
    )

    await Tortoise.generate_schemas()

    logger.success("[INIT][DB] Database initialized")


async def close_db():
    try:
        if Tortoise._inited:
            await Tortoise.close_connections()
            logger.success("[DB][CLOSE] Database connection closed")

        else:
            logger.warning("[DB][CLOSE] Database was not initialized, skipping close")
            
    except Exception as e:
        logger.warning(f"[DB][CLOSE] Error closing database connections: {e}")
