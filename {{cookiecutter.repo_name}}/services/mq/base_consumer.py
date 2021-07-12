import threading
import time
from typing import List, Union

from bali.db import db
from loguru import logger
from mq_http_sdk.mq_client import MQClient, MQExceptionBase
from mq_http_sdk.mq_consumer import Message

from conf import settings

__all__ = ["BaseConsumer"]


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

    def __init__(self):
        super().__init__()
        client = MQClient(
            settings.MQ_HOST, settings.MQ_ACCESS_ID, settings.MQ_ACCESS_KEY
        )
        self.consumer = client.get_consumer(
            settings.MQ_INSTANCE, self.topic, self.group, self.message_tag
        )

    def run(self) -> None:
        while True:
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
                    logger.debug("Received msg: {}", vars(i))
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

    def onmessage(self, msg: Message) -> None:
        raise NotImplementedError()
