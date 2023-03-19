import io
import json
import os
import pathlib

from collections.abc import Iterable, Iterator, Callable

from helpers.filters import predicate_filter, entity_filter

from lxml import etree


def xml_extractor(file: str | os.PathLike, xpath_pattern: str):
    """Loads an XML file and runs xpath_pattern against it.
    Matches results get str casted, so theXPath expression should match text nodes.
    """

    parser = etree.HTMLParser()  # other solution with xpath namespaces?
    tree = etree.parse(file, parser)

    matches = map(str, tree.xpath(xpath_pattern))

    return matches


def entity_extractor(file: str | os.PathLike, xpath_pattern: str):
    """Extracts entities according to xpath_pattern and applies entity_filter.
    """

    _entities = xml_extractor(file, xpath_pattern)

    return entity_filter(_entities)


def persons_extractor(file: str | os.PathLike):
    """ Extracts person entities according to //rs[@type='person']/text().
    """

    xpath_pattern = "//rs[@type='person']/text()"

    return entity_extractor(file, xpath_pattern)


def predicates_extractor(file: str | os.PathLike, _switch: dict[str, Callable] = None) -> Iterable[str]:
    """
    """

    with open(file) as f:

        extension = pathlib.Path(file).suffix

        switch = _switch or {
            ".json": lambda f: predicate_filter(json.load(f)["predicates"]),
        }

        get_predicates = switch.get(
            extension,
            lambda f: predicate_filter(f.readlines())
        )

        predicates = get_predicates(f)

    return predicates
