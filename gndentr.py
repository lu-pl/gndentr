import re

from collections.abc import Container, Iterable

import rdflib
import requests

from lxml import etree


class GNDEntityResolver:
    """Resolves named entities (e.g. person names) against the GND API and 
    constructs an rdflib.Graph instance based on the GND result set(s).

    Parameters:

    - predicates
    ~Allows to specify the predicates that should be transferred to the graph.
    ~i.e. predicates of the result are only transferred to the graph if in predicates.

    - limit
    """

    def __init__(self,
                 *entities: str,
                 predicates: Container = None,
                 limit: int = None):

        self._entities = entities
        self._predicates = predicates or list()
        self._limit = limit

        self._graph = rdflib.Graph()

    def _get_gnd_json(self, entity: str, params: dict = None) -> dict:
        """Gets json data for entity from the GND API;
        default params search for 'variantName' and filter by 'type:Person'.
        """

        # print(f"Requesting entity: '{entity}'")

        params = params or {
            "q": f"variantName: {entity}",
            "filter": "type:Person"
        }

        response = requests.get("https://lobid.org/gnd/search", params=params)

        return response.json()

    def _construct_json(self,
                        input_json: dict,
                        predicates: Container = None,
                        limit: int = None) -> dict:
        """Constructs json-ld from a gnd result set (input_json);

        Output json-ld is comprised of:
        - basic metadata about the gnd query
        - json data for every 'member' of the gnd set

        Member data gets filtered according to predicates
        ... []
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

        graph = rdflib.Graph()

        for entity in self._entities:

            # get json data
            json_ld = self._get_gnd_json(entity)

            if self._predicates:
                json_ld = self._construct_json(json_ld)

            graph.parse(data=json_ld, format="json-ld")

        return graph

    def to_graph(self):
        self._graph = self._construct_graph()
        return self._graph

    def serialize(self, *args, **kwargs):
        """Proxy for rdflib.Graph.serialize;
        delegates serialization to the rdflib.Graph instance;
        """

        if not self._graph:
            self.to_graph()

        return self._graph.serialize(*args, **kwargs)


if __name__ == "__main__":

    persons = get_person_names("some_file.xml")

    predicates = [
        "id",
        "gndIdentifier",
        "variantNames",
        "dateOfDeath",
        "placeOfDeath",
        "dateOfBirth",
        "dateOfDeath"
    ]

    graph = GNDEntityResolver(*persons, predicates=predicates).to_graph()
