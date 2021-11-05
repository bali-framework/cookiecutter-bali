from typing import Any

from loguru import logger
from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import TopicMessage
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, stop_after_delay

from conf import settings

__all__ = ["BaseTopic"]


class BaseTopic:
    topic: str

    class Schema(BaseModel):
        pass

    def __init__(self):
        client = MQClient(
            settings.MQ_HOST, settings.MQ_ACCESS_ID, settings.MQ_ACCESS_KEY
        )
        self.producer = client.get_producer(settings.MQ_INSTANCE, self.topic)

    @retry(stop=(stop_after_delay(5) | stop_after_attempt(3)))
    def _publish(self, topic_message):
        self.producer.publish_message(topic_message)

    def publish(
        self, msg: Any, *, tag: str = None, fail_silently: bool = False
    ) -> None:
        data = self.Schema.parse_obj(msg)
        try:
            topic_message = TopicMessage(data.json(), (tag or "").lower())
            self._publish(topic_message)
        except Exception as e:
            if not fail_silently:
                raise

            logger.warning("Publish msg to {} failed: {}", self.topic, repr(e))
        else:
            logger.info("Publish msg to {} success", self.topic)
