from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import TopicMessage

from conf import settings

__all__ = ["BaseProducer"]


class BaseProducer:
    instance: str
    topic: str

    def __init__(self):
        client = MQClient(
            settings.MQ_HOST, settings.MQ_ACCESS_ID, settings.MQ_ACCESS_KEY
        )
        self.producer = client.get_producer(self.instance, self.topic)

    def publish(self, msg: str, tag: str = None) -> None:
        msg_ = TopicMessage(msg, tag or "")
        self.producer.publish_message(msg_)
