import json
import pathlib

from dataclasses import dataclass

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


@dataclass
class HelpData:
    """Data container for CLI --help strings.
    """

    file: str
    xpath: str
    format: str
    limit: str
    predicates: str


help_ = HelpData(

    file=(
        "Path to an XML file from which entities are extracted according to some XPath pattern. "
        "Entities extracted from --file are merged with entities passed as arguments. "
        "Note that the --file flag requires the --xpath flag to be present (and vice versa)."
    ),

    xpath=(
        "XPath expression used for extracting entities from an XML file. "
        "XPath should match text nodes. "
        "Note that the --xpath flag requires the --file flag to be present (and vice versa)."
    ),

    format=(
        "Specifies the graph serialization format. "
        "The value of --format gets passed to rdflib.Graph.serialize; "
        "for applicable serialization formats see "
        "https://rdflib.readthedocs.io/en/stable/plugin_serializers.html."

    ),

    limit=(
        "Allows to control the maximum number of query result set members "
        "per result set that get transferred to the graph."
    ),

    predicates=(
        "Specifies the predicates used in graph construction. "
        "Predicates of the GND result set(s) are only transferred to the graph if present in the predicates argument. "
        "--predicates expects a path to a file from which predicates are extracted; "
        "either a JSON file with a single key 'predicates' that holds an array of predicate strings "
        "or a plain text file, in which case each line gets interpreted as a predicate."
        "If --predicates is not supplied all predicates from the GND result set are transferred to the graph."
    )
)


@click.command()
@click.argument("entities",
                type=click.STRING,
                nargs=-1)
@click.option("-f", "--file",
              type=click.Path(),
              cls=RequiredIf,
              required_if="xpath",
              help=help_.file)
@click.option("-x", "--xpath",
              cls=RequiredIf,
              required_if="file",
              help=help_.xpath)
@click.option("--format",
              default="ttl",
              show_default=True,
              help=help_.format)  # click.Options?
@click.option("--limit",
              type=click.INT,
              default=None,
              help=help_.limit)
@click.option("-p", "--predicates",
              type=click.Path(),
              default=None,
              help=help_.predicates)
def gndentr_cli(entities, file, xpath, format, limit, predicates):
    """GND Entity Resolver Command Line Interface\n

    Basic functionality for resolving named entities against the GND API and serializing graph data from the result sets.\n

    ENTITIES: Entity name(s) to be sent to the GND API.
    """

    if file:
        file_entities = entity_extractor(file, xpath)
        # merge entities
        entities = [*entities, *file_entities]

    predicates = predicates_extractor(predicates) if predicates else predicates

    graph = GNDEntityResolver(*entities, predicates=predicates, limit=limit)

    click.echo(graph.serialize(format=format))


if __name__ == "__main__":
    gndentr_cli()
