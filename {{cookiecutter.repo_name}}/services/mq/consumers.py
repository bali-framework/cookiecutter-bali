from loguru import logger

from services.mq.base_consumer import BaseConsumer


class Info(BaseConsumer):
    topic = "example"
    group = "example"

    def onmessage(self, msg) -> None:
        logger.info(msg)
