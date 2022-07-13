import threading
import time
from typing import List, Union

from bali.db import db
from loguru import logger
from mq_http_sdk.mq_client import MQClient, MQExceptionBase
from mq_http_sdk.mq_consumer import Message

from conf import settings

__all__ = ["BaseConsumer", "BaseHalfMessageConsumer"]


class BaseConsumer(threading.Thread):
    topic: str
    group: str
    message_tag: str = ""
    batch_size: int = 16
    wait_seconds: int = 30
    need_ack: bool = True
    consume_interval: Union[int, float] = 0.001

    def __init_subclass__(cls, **kwargs):
        assert cls.batch_size <= 16, "max batch size is 16"
        assert cls.wait_seconds <= 30, "max wait seconds is 30"

    def __init__(self, stop_event: threading.Event):
        super().__init__()
        self.stop_event = stop_event
        self.client = MQClient(
            settings.MQ_HOST,
            settings.MQ_ACCESS_ID,
            settings.MQ_ACCESS_KEY,
            logger=logger,
        )
        self.consumer = self.client.get_consumer(
            settings.MQ_INSTANCE, self.topic, self.group, self.message_tag
        )
        logger.info("Start consume topic {}", self.topic)

    def run(self) -> None:
        while not self.stop_event.is_set():
            try:
                received: List[Message] = self.consumer.consume_message(
                    self.batch_size, self.wait_seconds
                )
            except MQExceptionBase as e:
                if e.type != "MessageNotExist":
                    logger.exception("Consume msg failed: {}", repr(e))
            else:
                receipt_handle_list = []
                for i in received:
                    logger.info("Received msg: {}", vars(i))
                    try:
                        self.onmessage(i)
                    except Exception as e:
                        logger.exception(
                            "Exception raised when handle msg: {}", repr(e)
                        )
                    else:
                        if self.need_ack:
                            receipt_handle_list.append(i.receipt_handle)
                    finally:
                        db.session.remove()

                try:
                    self.consumer.ack_message(receipt_handle_list)
                except MQExceptionBase as e:
                    logger.exception("Ack Failed: {}", repr(e))

            finally:
                time.sleep(self.consume_interval)

        logger.info("Stop consume topic {}", self.topic)

    def onmessage(self, msg: Message) -> None:
        raise NotImplementedError()


class BaseHalfMessageConsumer(threading.Thread):
    topic: str
    group: str
    batch_size: int = 16
    wait_seconds: int = 30
    consume_interval: Union[int, float] = 1

    def __init_subclass__(cls, **kwargs):
        assert cls.batch_size <= 16, "max batch size is 16"
        assert cls.wait_seconds <= 30, "max wait seconds is 30"

    def __init__(self, stop_event: threading.Event):
        super().__init__()
        self.stop_event = stop_event
        self.client = MQClient(
            settings.MQ_HOST,
            settings.MQ_ACCESS_ID,
            settings.MQ_ACCESS_KEY,
            logger=logger,
        )
        self._trans_producer = self.client.get_trans_producer(
            settings.MQ_INSTANCE, self.topic, self.group
        )
        logger.info("Start consume half message topic {}", self.topic)

    def onmessage(self, msg: Message):
        raise NotImplementedError()

    def commit(self, msg: Message):
        return self._trans_producer.commit(msg.receipt_handle)

    def rollback(self, msg: Message):
        return self._trans_producer.rollback(msg.receipt_handle)

    def run(self) -> None:
        while not self.stop_event.is_set():
            try:
                received: List[Message] = self._trans_producer.consume_half_message(
                    self.batch_size, self.wait_seconds
                )
            except MQExceptionBase as e:
                if e.type != "MessageNotExist":
                    logger.exception("Consume half msg failed: {}", repr(e))
            else:
                for i in received:
                    logger.info("Received half msg: {}", vars(i))
                    try:
                        self.onmessage(i)
                    except Exception as e:
                        logger.exception(
                            "Exception raised when handle half msg: {}", repr(e)
                        )
                    finally:
                        db.session.remove()
