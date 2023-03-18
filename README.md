# GND EntR

GND Entity Resolver - A small utility for resolving named entities against GND and serializing graph data from the result sets.

It provides the following features:

* [todo]
* [todo]

> This project is in an early stage of development and should be used with caution

## Setup 

```shell
$ git clone https://gitlab.com/lupl/gndentr
$ cd gndentr
$ pip install -r requirements.txt
```
## Basic Usage

### CLI

With argument(s), predicates from JSON:

```shell
$ python gndentr-cli.py "Ludwig Wittgenstein" -p ./tests/test_data/predicates.json
```

With argument(s) + TEI/XML-File, predicates from text file:

```shell
python gndentr-cli.py "Ludwig Wittgenstein" --file ./tests/test_data/minimal_tei.xml -x "//rs[@type='person']/text()" -p ./tests/test_data/predicates
```

### Python

```python
```

## Examples

## Contribution

Please feel free to open issues or pull requests.

