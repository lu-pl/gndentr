import io
import json
import os
import pathlib

from collections.abc import Iterable, Iterator, Callable

from helpers.filters import predicate_filter, entity_filter

from lxml import etree


def xml_extractor(file: str | os.PathLike, xpath_pattern: str) -> map[str]:
    """Loads an XML file and runs xpath_pattern against it.
    Matches results get str casted, so theXPath expression should match text nodes.
    """

    parser = etree.HTMLParser()  # other solution with xpath namespaces?
    tree = etree.parse(file, parser)

    matches = map(str, tree.xpath(xpath_pattern))

    return matches


def entity_extractor(file: str | os.PathLike, xpath_pattern: str):

    _entities = xml_extractor(file, xpath_pattern)

    return entity_filter(_entities)


def persons_extractor(file: str | os.PathLike):

    xpath_pattern = "//rs[@type='person']/text()"

    return entity_extractor(file, xpath_pattern)


def predicates_extractor(file: str | os.PathLike, _switch: dict[str, Callable] = None) -> Iterable[str]:

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


##################################################
# [passes] test predicates-extractor
# print(predicates_extractor("../tests/test_data/predicates"))
# print()
# print(predicates_extractor("../tests/test_data/predicates.json"))

# [passes] test persons_extractor
# print(persons_extractor("../tests/test_data/corpus_full_dedup.xml"))

# [passes] test xml_extractor
# print(xml_extractor("../tests/test_data/corpus_full_dedup.xml", "//rs[@type='person']"))

# print(persons_extractor("../tests/test_data/corpus_full_dedup.xml"))
