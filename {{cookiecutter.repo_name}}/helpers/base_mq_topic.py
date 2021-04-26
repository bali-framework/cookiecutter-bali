from loguru import logger
from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import TopicMessage

from conf import settings

__all__ = ["BaseTopic"]


class BaseTopic:
    topic: str

    def __init__(self):
        client = MQClient(
            settings.MQ_HOST, settings.MQ_ACCESS_ID, settings.MQ_ACCESS_KEY
        )
        self.producer = client.get_producer(settings.MQ_INSTANCE, self.topic)

    def publish(self, msg: str, *, tag: str = None, fail_silently: bool = False) -> None:
        try:
            msg_ = TopicMessage(msg, tag or "")
            self.producer.publish_message(msg_)
        except Exception as e:
            if not fail_silently:
                raise

            logger.warning("Publish msg to {} failed: {}", self.topic, repr(e))
