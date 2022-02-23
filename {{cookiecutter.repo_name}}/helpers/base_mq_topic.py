import logging
from typing import Dict, Union

from loguru import logger
from mq_http_sdk.mq_client import MQClient
from mq_http_sdk.mq_producer import MQProducer, MQTransProducer, TopicMessage
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, stop_after_delay

from conf import settings

__all__ = ["Topic", "TransactionTopic"]


class BaseTopic:
    topic: str
    fail_silently: bool

    class Schema(BaseModel):
        pass

    def __init__(self):
        self.client: MQClient = MQClient(
            settings.MQ_HOST,
            settings.FIN_MQ_ACCESS_ID,
            settings.FIN_MQ_ACCESS_KEY,
            logger=logger,
        )
        self.producer = self.get_producer()

    def get_producer(self) -> Union[MQProducer, MQTransProducer]:
        raise NotImplementedError()

    @retry(reraise=True, stop=(stop_after_delay(5) | stop_after_attempt(3)))
    def _publish(self, message: TopicMessage) -> TopicMessage:
        return self.producer.publish_message(message)

    def make_message(self, body: Dict) -> TopicMessage:
        schema = self.Schema.parse_obj(body)
        return TopicMessage(schema.json())

    def publish(self, body: Dict, *, tag: str = None) -> TopicMessage:
        try:
            message = self.make_message(body)
            if tag is not None:
                tag = tag.lower()
                message.set_message_tag(tag)

            return self._publish(message)
        except Exception as e:
            if not self.fail_silently:
                raise

            logger.error(
                "PublishMessageFailed\ntopic: {}\nmsg: {}\ntag: {}\nerror: {}",
                self.topic,
                body,
                tag,
                repr(e),
            )


class Topic(BaseTopic):
    fail_silently: bool = True

    def get_producer(self) -> MQProducer:
        return self.client.get_producer(settings.MQ_INSTANCE, self.topic)


WARNING = logging.getLevelName(logging.WARNING)


class TransactionTopic(BaseTopic):
    group: str
    tag: str
    fail_silently: bool = False

    def __init__(self, **body):
        super().__init__()
        self.body = body

    def get_producer(self) -> MQTransProducer:
        return self.client.get_trans_producer(
            settings.MQ_INSTANCE, self.topic, self.group
        )

    def make_message(self, body: Dict) -> TopicMessage:
        message = super().make_message(body)
        message.set_trans_check_immunity_time(10)
        return message

    def __enter__(self):
        self.prepare_message = self.publish(self.body, tag=self.tag)
        return self

    @logger.catch(level=WARNING)
    def commit(self):
        self.producer.commit(self.prepare_message.receipt_handle)

    @logger.catch(level=WARNING)
    def rollback(self):
        self.producer.rollback(self.prepare_message.receipt_handle)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
