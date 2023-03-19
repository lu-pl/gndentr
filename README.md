# GND EntR

GND Entity Resolver - Basic functionality for resolving named entities against the [GND API](https://lobid.org/gnd/api) and serializing graph data from the result sets.

> This project is in an early stage of development and should be used with caution

## Requirements

* python >= 3.10

## Setup 

Activate a virtual environment (python >= 3.10) and run the following shell commands:

```shell
git clone https://gitlab.com/lupl/gndentr
cd gndentr
pip install -r requirements.txt
```
## Usage

GND EntR provides a general `GNDEntityResolver` class and also a small Command Line Interface.

> For a quick overview checkout the CLI Examples below.

### GNDEntityResolver 

`GNDEntityResolver` resolves named entities (e.g. person names) against the GND API and constructs an [rdflib.Graph](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph) instance based on the GND result sets fetched from the API.

Parameters:

* **entities**: For each element in `entities` a request is sent to the GND API matching against 'variantName' (for control over this behavior see the `GNDPersonResolver` example below).
* **predicates**: Predicates of the GND result sets are only transferred to the graph if present in the `predicates` argument.
* **limit**: Allows to control the maximum number of query result set members *per result set* that get transferred to the graph.

```python
from gndentr import GNDEntityResolver

entities = ["Ludwig Wittgenstein", "Rudolf Carnap"]

predicates = [
    "id",
    "gndIdentifier",
    "variantNames",
    "dateOfDeath",
    "placeOfDeath",
    "dateOfBirth",
    "dateOfDeath"
]

graph = GNDEntityResolver(*entities, predicates=predicates)

print(graph.serialize(format="ttl"))
```

As mentioned, requests are sent to the GND API matching against 'variantName' by default.
This behavior is easily customizable, since API query strings can be controlled by overriding `GNDEntityResolver._get_gnd_json` and providing an appropriate `params` parameter.

E.g. `GNDPersonResolver` is implemented like so:

```python
class GNDPersonResolver(GNDEntityResolver):

    def _get_gnd_json(self, entity: str, params: dict = None) -> dict:

        person_params = {
            "q": f"variantName: {entity}",
            "filter": "type:Person"
        }

        return super()._get_gnd_json(entity, person_params)
```


### CLI

A small CLI that utilizes `GNDEntityResolver`.

Also allows to read entities from an XML file according to some XPath pattern.

`GNDEntityResolver`'s mandatory `predicate` parameter is read from a file (JSON, text, possibly other formats (see the `_switch` parameter of `predicates_extractor` in `gndentr.helpers.extractors`)).

> Run `python gndentr-cli.py --help` to see available CLI options.

#### CLI Examples

With single argument, predicates from JSON:

```shell
python gndentr-cli.py "Ludwig Wittgenstein" -p ./tests/test_data/predicates.json
```

With multiple arguments, predicates from JSON:

```shell
python gndentr-cli.py "Ludwig Wittgenstein" "Rudolf Carnap" -p ./tests/test_data/predicates.json
```

With entity extraction from a TEI/XML-File using xpath pattern; predicates from text file:

```shell
python gndentr-cli.py --file ./tests/test_data/minimal_tei.xml -x "//rs[@type='person']/text()" -p ./tests/test_data/predicates
```

With argument + TEI/XML-File; entities from arguments and TEI/XML-File are merged ; predicates from text file:

```shell
python gndentr-cli.py "Ludwig Wittgenstein" --file ./tests/test_data/minimal_tei.xml -x "//rs[@type='person']/text()" -p ./tests/test_data/predicates
```

## Contribution

Please feel free to open issues or pull requests.

