import datetime
import decimal
import enum
from uuid import UUID

from bali.db import AwareDateTime, db
from bali.utils import timezone
from loguru import logger
from sqlalchemy import JSON, BigInteger, Column, String
from sqlalchemy.event import listens_for
from sqlalchemy.util.langhelpers import symbol

__all__ = ["FieldTracker"]


class FieldTracker(db.BaseModel):
    is_active = None
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_time = Column(AwareDateTime, default=timezone.now)
    updated_time = Column(AwareDateTime, default=timezone.now, onupdate=timezone.now)

    table = Column(String(64), nullable=False)
    row = Column(BigInteger, nullable=False)
    field = Column(String(64), nullable=False)
    old_value = Column(JSON)
    new_value = Column(JSON)

    @classmethod
    def listen_for(cls, *fields):
        for i in fields:

            @listens_for(i, "set")
            @logger.catch
            def create(target, value, oldvalue, initiator):
                if any(
                    [
                        oldvalue is symbol("NO_VALUE"),
                        value == oldvalue,
                    ]
                ):
                    return value

                db.session.add(
                    cls(
                        table=target.__tablename__,
                        row=target.id,
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
    elif isinstance(value, decimal.Decimal):
        return str(value)
    elif isinstance(value, UUID):
        return value.hex
    else:
        return value
