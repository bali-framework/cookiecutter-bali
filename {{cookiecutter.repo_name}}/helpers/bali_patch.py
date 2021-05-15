from datetime import date, datetime
from decimal import Decimal
from enum import Enum

import pytz
from bali.utils import timezone
from google.protobuf import json_format
from sqlalchemy import DateTime, TypeDecorator


class AwareDateTime(TypeDecorator):
    impl = DateTime

    @property
    def python_type(self):
        return datetime

    def process_result_value(self, value, dialect):
        if value is not None:
            value = timezone.make_aware(value, timezone=pytz.utc)

        return value

    def process_bind_param(self, value, dialect):
        if value is not None and timezone.is_aware(value):
            value = timezone.make_naive(value, timezone=pytz.utc)

        return value


class ProtobufParser(json_format._Parser):  # noqa
    def _ConvertValueMessage(self, value, message):
        """Convert a JSON representation into Value message."""
        if isinstance(value, dict):
            self._ConvertStructMessage(value, message.struct_value)
        elif isinstance(value, list):
            self._ConvertListValueMessage(value, message.list_value)
        elif value is None:
            message.null_value = 0
        elif isinstance(value, bool):
            message.bool_value = value
        elif isinstance(value, json_format.six.string_types):
            message.string_value = value
        elif isinstance(value, json_format._INT_OR_FLOAT):  # noqa
            message.number_value = value
        elif isinstance(value, (datetime, date)):
            message.string_value = value.isoformat()
        elif isinstance(value, Enum):
            message.string_value = value.name
        elif isinstance(value, Decimal):
            message.string_value = str(value)
        else:
            raise json_format.ParseError(
                "Value {0} has unexpected type {1}.".format(value, type(value))
            )


def ParseDict(  # noqa
    js_dict,
    message,
    ignore_unknown_fields=False,
    descriptor_pool=None,
):
    parser = ProtobufParser(ignore_unknown_fields, descriptor_pool)
    parser.ConvertMessage(js_dict, message)
    return message
