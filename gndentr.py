import re

from collections.abc import Container, Iterable

import rdflib
import requests

from lxml import etree


class GNDEntityResolver:
    """Resolves named entities (e.g. person names) against the GND API and 
    constructs an rdflib.Graph instance based on the GND result sets.

    For basic usage and parameters see https://gitlab.com/lupl/gndentr/-/tree/main/#usage.
    """

    def __init__(self,
                 *entities: str,
                 predicates: Container = None,
                 limit: int = None):

        self._entities = entities
        self._predicates = predicates or list()
        self._limit = limit

        self._graph = rdflib.Graph()

    def _get_gnd_json(self, entity: str, params: dict = None) -> dict:  # remove?
        """Gets JSON data for entity from the GND API;
        default params search for 'variantName'.
        """

        # print(f"Requesting entity: '{entity}'")

        params = params or {
            "q": f"variantName: {entity}",
            # "filter": "type:Person"
        }

        response = requests.get("https://lobid.org/gnd/search", params=params)

        return response.json()

    def _construct_json(self,
                        input_json: dict,
                        predicates: Container = None,
                        limit: int = None) -> dict:
        """Constructs JSON-LD from a GND result set (input_json).

        Output JSON-LD is comprised of:

        - basic metadata about the gnd query
        - json data for every 'member' of the gnd set

        For predicates and limit parameters see class documenation.

        """

        predicates = predicates or self._predicates
        limit = limit or self._limit

        output_json = {
            "@context": "https://lobid.org/gnd/context.jsonld",
            "id": f"{input_json['id']}",
            "totalItems": input_json['totalItems'],
            "member": []
        }

        members = input_json["member"][:limit] if limit else input_json["member"]

        # for member in input_json["member"]:
        for member in members:

            member_dict = {}

            for p, o in member.items():
                if p in self._predicates:
                    member_dict.update({p: o})

            output_json["member"].append(member_dict)

        return output_json

    def _construct_graph(self) -> rdflib.Graph:
        """Fetches JSON data from the API,
        applies predicates contraint if applicable,
        and parses JSON-LD data into an rdflib.Graph instance.
        """

        graph = rdflib.Graph()

        for entity in self._entities:

            # get json data
            json_ld = self._get_gnd_json(entity)

            # apply predicates constraints
            if self._predicates:
                json_ld = self._construct_json(json_ld)

            # merge graph
            graph.parse(data=json_ld, format="json-ld")

        return graph

    def to_graph(self):
        """
        Getter for graph representation.
        """

        self._graph = self._construct_graph()
        return self._graph

    # could this imply that GNDEntityResolver /is/ an rdflib.Graph?
    def serialize(self, *args, **kwargs):
        """Proxy for rdflib.Graph.serialize;
        delegates serialization to the rdflib.Graph instance;
        """

        if not self._graph:
            self.to_graph()

        return self._graph.serialize(*args, **kwargs)


class GNDPersonResolver(GNDEntityResolver):

    def _get_gnd_json(self, entity: str, params: dict = None) -> dict:

        person_params = {
            "q": f"variantName: {entity}",
            "filter": "type:Person"
        }

        return super()._get_gnd_json(entity, person_params)
