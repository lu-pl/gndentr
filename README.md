# GND EntR

GND Entity Resolver - A small utility for resolving named entities against GND and serializing graph data from the result sets.

It provides the following features:

* gndentr.GNDEntityresolver: ...
* gndentr-cli: A CLI ...

See examples below.

> This project is in an early stage of development and should be used with caution

## Requirements

* python >= 3.10

## Setup 

Activate a virtual environment and run the following shell commands:

```shell
git clone https://gitlab.com/lupl/gndentr
cd gndentr
pip install -r requirements.txt
```
## Basic Usage

### CLI

Run `python gndentr-cli.py --help` to see CLI options.

#### Examples

With argument(s), predicates from JSON:

```shell
python gndentr-cli.py "Ludwig Wittgenstein" -p ./tests/test_data/predicates.json
```

With argument(s) + TEI/XML-File, predicates from text file:

```shell
python gndentr-cli.py "Ludwig Wittgenstein" --file ./tests/test_data/minimal_tei.xml -x "//rs[@type='person']/text()" -p ./tests/test_data/predicates
```

### Python

#### Examples

```python
```


## Contribution

Please feel free to open issues or pull requests.

