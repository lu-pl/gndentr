from collections.abc import Iterable, Callable

from gndentr.helpers import filters


def all_of_type_p(iterable: Iterable, type: type):

    return all(
        True if isinstance(i, type) else False
        for i in iterable
    )


##################################################
# actual tests


def test_filter_chain():

    chain_comp = filters.filter_chain

    chain_iter = chain_comp(
        ["test 1", "test 2", "test 1"],
    )

    chain = chain_iter(
        filters=[
            set,
            lambda iterable: map(lambda str: str.upper(), iterable)
        ]
    )

    # chain types:
    assert isinstance(chain_comp, Callable)
    assert isinstance(chain_iter, Callable)
    assert isinstance(chain, Iterable)

    # chain elements:
    # set?
    assert len(chain) == 2
    # all strings?
    assert all_of_type_p(chain, str)


def test_string_filters():

    filter1 = filters.entity_str_filters
    filter2 = filters.predicate_str_filters

    # all callable?
    assert(all_of_type_p(filter1, Callable))
    assert(all_of_type_p(filter2, Callable))

    # all filters take iterables of strings?
    for filter in [*filter1, *filter2]:
        try:
            filter(["some string", "another string"])
        except Exception:
            raise AssertionError
