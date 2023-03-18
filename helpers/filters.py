import re

from collections.abc import Iterable, Iterator, Callable
from typing import Union

import toolz


StringFilterType = Iterable[Callable[[Iterable], Iterable[str]]]


@toolz.curry
def filter_chain(iterable: Iterable[str], *,
                 filters: StringFilterType) -> Iterable[str]:

    composite = toolz.compose(*filters)

    return composite(iterable)


def filter_regex(regex):

    def _wrapper(iterator):

        for i in iterator:
            yield re.sub(regex, "", i)

    return _wrapper


def filter_string_strip(iterator):

    for i in iterator:
        yield " ".join(i.split())


def filter_empty_string(iterator):
    for i in iterator:
        if i:
            yield i


regex = re.compile(
    r"([Ss]ein\w*).*|([Ii]hr\w*)|(Herrn?\s)|(Frau)|(Sig\.\s)|(Signor\w*\s)|(['’]s)")

entity_str_filters = (
    set,
    filter_empty_string,
    filter_regex(regex),
    filter_string_strip,
)

predicate_str_filters = (
    set,
    filter_empty_string,
    filter_string_strip,
)

entity_filter = filter_chain(filters=entity_str_filters)
predicate_filter = filter_chain(filters=predicate_str_filters)
