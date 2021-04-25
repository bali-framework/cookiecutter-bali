from services.mq.consumers import BaseConsumer
from loguru import logger

def serve():
    for consumer in BaseConsumer.__subclasses__():
        consumer().start()
        logger.info("Start consume topic {}", consumer.topic)

if __name__ == '__main__':
    serve()
