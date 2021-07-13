# Cookiecutter for bali style service

### QuickStart
```shell
pip3 install cookiecutter
cookiecutter https://github.com/Ed-XCF/cookiecutter-bali.git
cd your_project
git init
make env
```

### Testing
```shell
tox
```

### Service include
* FastAPI
* RocketMQ
* gRPC

### Hooks in pre commit
* pre-commit-hooks
* black
* isort
* flake8

### MQ consumer example
```python
from loguru import logger
from mq_http_sdk.mq_consumer import Message

from services.mq.base_consumer import BaseConsumer


class Example(BaseConsumer):
    topic = "example"
    group = "example"

    def onmessage(self, msg: Message) -> None:
        logger.info("Hello {}", msg)
```

### MQ producer example
```python
from pydantic import BaseModel

from helpers.base_mq_topic import BaseTopic


class Example(BaseTopic):
    topic = "example"

    class Schema(BaseModel):
        uuid: str
        user_uuid: str
```

### SQLAlchemy field tracking
```python
from bali.db import AwareDateTime, db
from sqlalchemy import BigInteger, Column

from models.field_tracker import FieldTracker


class Example(db.BaseModel):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    example_time_1 = Column(AwareDateTime)
    example_time_2 = Column(AwareDateTime)


FieldTracker.listen_for(
    Example.example_time_1,
    Example.example_time_2,
)
```
