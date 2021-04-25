from loguru import logger
from mq_http_sdk.mq_consumer import Message

from services.mq.base_consumer import BaseConsumer


class Info(BaseConsumer):
    topic = "example"
    group = "example"

    def onmessage(self, msg: Message) -> None:
        logger.info(msg)
