from services.mq.base_consumer import BaseConsumer


class Mop(BaseConsumer):
    topic = "mop-tag-topic"
    group = "GID_MOP_2"

    def onmessage(self, msg) -> None:
        print(msg)
