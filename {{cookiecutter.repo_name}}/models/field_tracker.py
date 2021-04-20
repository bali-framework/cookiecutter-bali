import datetime
import decimal
import enum
import uuid

from bali.db import db
from loguru import logger
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.event import listens_for
from sqlalchemy.util.langhelpers import symbol

__all__ = ["FieldTracker"]


class FieldTracker(db.BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    table = Column(String(64), nullable=False)
    uuid = Column(String(32))
    field = Column(String(64), nullable=False)
    old_value = Column(JSON)
    new_value = Column(JSON)

    @classmethod
    def listen_for(cls, *fields):
        for i in fields:

            @listens_for(i, "set")
            @logger.catch
            def create(target, value, oldvalue, initiator):
                if oldvalue is symbol("NO_VALUE"):
                    return value

                db.session.add(
                    cls(
                        table=target.__tablename__,
                        uuid=target.uuid,
                        field=initiator.key,
                        old_value=_convert(oldvalue),
                        new_value=_convert(value),
                    )
                )
                return value


def _convert(value):
    if isinstance(value, datetime.datetime):
        r = value.isoformat()
        if value.microsecond:
            r = r[:23] + r[26:]
        return r
    elif isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, datetime.time):
        assert value.utcoffset() is None, "aware time not allowed"
        r = value.isoformat()
        if value.microsecond:
            r = r[:12]
        return r
    elif isinstance(value, enum.Enum):
        return value.name
    elif isinstance(value, (decimal.Decimal, uuid.UUID)):
        return str(value)
    else:
        return value
