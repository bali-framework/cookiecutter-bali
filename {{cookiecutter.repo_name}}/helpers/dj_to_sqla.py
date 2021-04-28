from typing import Tuple

from sqlalchemy import desc, asc
from sqlalchemy.sql import operators
from sqlalchemy.sql.expression import extract

OPERATORS = {
    'isnull': lambda c, v: (c == None) if v else (c != None),  # noqa
    'exact': operators.eq,
    'ne': operators.ne,  # not equal or is not (for None)
    'gt': operators.gt,
    'gte': operators.ge,
    'lt': operators.lt,
    'lte': operators.le,
    'in': operators.in_op,
    'notin': operators.notin_op,
    'between': lambda c, v: c.between(v[0], v[1]),
    'like': operators.like_op,
    'ilike': operators.ilike_op,
    'startswith': operators.startswith_op,
    'istartswith': lambda c, v: c.ilike(v + '%'),
    'endswith': operators.endswith_op,
    'iendswith': lambda c, v: c.ilike('%' + v),
    'contains': lambda c, v: c.ilike('%{v}%'.format(v=v)),
    'year': lambda c, v: extract('year', c) == v,
    'year_ne': lambda c, v: extract('year', c) != v,
    'year_gt': lambda c, v: extract('year', c) > v,
    'year_ge': lambda c, v: extract('year', c) >= v,
    'year_lt': lambda c, v: extract('year', c) < v,
    'year_le': lambda c, v: extract('year', c) <= v,
    'month': lambda c, v: extract('month', c) == v,
    'month_ne': lambda c, v: extract('month', c) != v,
    'month_gt': lambda c, v: extract('month', c) > v,
    'month_ge': lambda c, v: extract('month', c) >= v,
    'month_lt': lambda c, v: extract('month', c) < v,
    'month_le': lambda c, v: extract('month', c) <= v,
    'day': lambda c, v: extract('day', c) == v,
    'day_ne': lambda c, v: extract('day', c) != v,
    'day_gt': lambda c, v: extract('day', c) > v,
    'day_ge': lambda c, v: extract('day', c) >= v,
    'day_lt': lambda c, v: extract('day', c) < v,
    'day_le': lambda c, v: extract('day', c) <= v,
}


def dj_lookup_to_sqla(expression: str) -> Tuple:
    splitter = "__"
    col_name, op_name = expression, "exact"
    if splitter in col_name:
        col_name, op_name = col_name.rsplit(splitter, 1)
    return OPERATORS[op_name], col_name


def dj_ordering_to_sqla(expression: str):
    reverse = "-"
    wrapper = desc if expression.startswith(reverse) else asc
    return wrapper(expression.lstrip(reverse))
