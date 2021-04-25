from services.mq.base_consumer import BaseConsumer


class Print(BaseConsumer):
    topic = "example"
    group = "example"

    def onmessage(self, msg) -> None:
        print(msg)
