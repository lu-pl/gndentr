import json
import pathlib

from helpers.extractors import entity_extractor, predicates_extractor

import click
from gndentr import GNDEntityResolver


class RequiredIf(click.Option):

    def __init__(self, *args, required_if: str = None, ** kwargs):

        self._required_if = required_if
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):

        this_option_present = self.name in opts
        required_option_present = self._required_if in opts

        if required_option_present and not this_option_present:
            raise click.UsageError(
                f"Missing required option '--{self.name}'.")

        return super().handle_parse_result(ctx, opts, args)


@click.command()
@click.argument("entities", type=click.STRING, nargs=-1)
@click.option("-f", "--file", cls=RequiredIf, required_if="xpath", type=click.Path())
@click.option("-x", "--xpath", cls=RequiredIf, required_if="file")
@click.option("--format", default="ttl", show_default=True)  # click.Options?
@click.option("--limit", default=None, type=click.INT)
@click.option("-p", "--predicates", type=click.Path(), required=True)
def gndentr_cli(entities, file, xpath, format, limit, predicates):
    """gndentr_cli - GND Entity Resolver Command Line Interface
    ...
    """

    if file:
        file_entities = entity_extractor(file, xpath)
        # merge entities
        entities = [*entities, *file_entities]

    predicates = predicates_extractor(predicates)

    graph = GNDEntityResolver(*entities, predicates=predicates, limit=limit)

    click.echo(graph.serialize(format=format))


if __name__ == "__main__":
    gndentr_cli()
