# jsonid

<!-- markdownlint-disable -->
<img
    src="https://github.com/ffdev-info/jsonid/blob/main/static/images/JSON_logo-crockford.png?raw=true"
    alt="JSON ID logo based on JSON Logo by Douglas Crockford"
    width="200px" />
<!-- markdownlint-enable -->

[JSON][json-1]IDentification tool, and ruleset. `jsonid` can be downloaded via
PyPi: [here][pypi-download-1].

[json-1]: https://www.json.org/json-en.html
[pypi-download-1]: https://pypi.org/project/jsonid/

## Function

`jsonid` borrows from the Python approach to ask forgiveness rather than
permission (EAFP) to attempt to open every object it scans and see if it
parses as JSON. If it doesn't we move along. If it does, we then have an
opportunity to identify the characteristics of the JSON we have opened.

Python being high-level also provides an easier path to processing files
and parsing JSON quickly with very little other knowledge required
of the underlying data structure.

## Why?

Consider these equivalent forms:

```json
{
    "key 1": "value",
    "key 2": "value"
}
```

```json
{
    "key 2": "value",
    "key 1": "value"
}
```

PRONOM signatures are not expressive enough for complicated JSON objects.

If I want DROID to find `key 1` I have to use a wildcard, so I would write
something like:

```text
BOF: "7B*226B6579203122"
EOF: "7D"
```

But if I then want to match on `key 2` as well as `key 1` things start getting
complicated as they aren't guaranteed by the JSON specification to be in the
same "position' (if we think about order visually). When other keys are used in
the object they aren't necessarily guaranteed to be next to each other.

`jsonid` tries to compensate for this by using the format's own strengths to
parse binary data as JSON and then if successful, use a grammar describing
specific key-valyes as "markers" that can begin to help to identify the
JSON objects that we might be looking at.

## What does `jsonid` get you?

To begin, `jsonid` should identify JSON files on your system as JSON.
That's already a pretty good position to be in.

The ruleset should then allow you to identify a decent number of JSON objects,
especially those that have a well-defined structure. Examples we have in the
registry data include things like ActivityPub streams, RO-CRATE metadata,
IIIF API data and so on.

If the ruleset works for JSON we might be able to apply it to other formats
such as YAML, and TOML in future.

## Ruleset

`jsonid` currently defines a small set of rules that help us to identify JSON
documents.

The rules are described in their own data-structures. The structures are
processed as a list (they need not necessarily be in order) and each must
match for a given set of ruls to determine what kind of JSON document we might
be looking at.

`jsonid` can identify the existence of information but you can also use
wildcards and provide some negation as required, e.g. to remove
false-positives between similar JSON entities.

| rule       | meaning                                               |
|------------|-------------------------------------------------------|
| INDEX      | index (from which to read when structure is an array) |
| GOTO       | goto key (read key at given key)                      |
| KEY        | key to read                                           |
| CONTAINS   | value contains string                                 |
| STARTSWITH | value startswith string                               |
| ENDSWITH   | value endswith string                                 |
| IS         | value matches exactly                                 |
| REGEX      | value matches a regex pattern                         |
| EXISTS     | key exists                                            |
| NOEXIST    | key doesn't exists                                    |
| ISTYPE     | key is a specific type (string, number, dict, array)  |

Stored in a list within a `RegistryEntry` object, they are then processed
in order.

For example:

```json
    [
        { "KEY": "name", "IS": "value" },
        { "KEY": "schema", "CONTAINS": "/schema/version/1.1/" },
        { "KEY": "data", "IS": { "more": "data" } },
    ]
```

All rules need to match for a positive ID.

> **NB.**: `jsonid` is a
work-in-progress and requires community input to help determine the grammar
in its fullness and so there is a lot of opportunity to add/remove to these
methods as its development continues. Additionally, help formalizing the
grammar/ruleset would be greatly appreciated 🙏.

### Backed by testing

The ruleset has been developed using test-driven-development practices (TDD)
and the current set of tests can be reviewed in the repository's
[test folder][testing-1]. More tests should be added, in general, and over
time.

[testing-1]: https://github.com/ffdev-info/jsonid/tree/main/tests

## Registry

A temporary "registry" module is used to store JSON markers.
The registry is a work in progress and must be exported and
rewritten somewhere more centralized (and easier to manage) if `jsonid` can
prove useful to the communities that might use it (*see notes on PRONOM below*).

The registry web-page is here:

* [jsonid registry][registry-htm-1].

[registry-htm-1]: https://ffdev-info.github.io/jsonid/registry/

The registry's source is here:

* [Registry](https://github.com/ffdev-info/jsonid/blob/main/src/jsonid/registry_data.py).

### Registry examples

#### Identifying JSON-LD Generic

```python
    RegistryEntry(
        identifier="id0009",
        name=[{"@en": "JSON-LD (generic)"}],
        markers=[
            {"KEY": "@context", "EXISTS": None},
            {"KEY": "id", "EXISTS": None},
        ],
    ),
```

> **Pseudo code**:
Test for the existence of keys: `@context` and `id` in the primary JSON object.

#### Identifying Tika Recursive Metadata

```python
    RegistryEntry(
        identifier="id0024",
        name=[{"@en": "tika recursive metadata"}],
        markers=[
            {"INDEX": 0, "KEY": "Content-Length", "EXISTS": None},
            {"INDEX": 0, "KEY": "Content-Type", "EXISTS": None},
            {"INDEX": 0, "KEY": "X-TIKA:Parsed-By", "EXISTS": None},
            {"INDEX": 0, "KEY": "X-TIKA:parse_time_millis", "EXISTS": None},
        ],
```

> **Pseudo code**:
Test for the existence of keys: `Content-Length`, `Content-Type`,
`X-TIKA:Parsed-By` and `X-TIKA:parse_time_millis` in the `zeroth` (first)
JSON object where the primary document is a list of JSON objects.

#### Identifying SOPS encrypted secrets file

```python
    RegistryEntry(
        identifier="id0012",
        name=[{"@en": "sops encrypted secrets file"}],
        markers=[
            {"KEY": "sops", "EXISTS": None},
            {"GOTO": "sops", "KEY": "kms", "EXISTS": None},
            {"GOTO": "sops", "KEY": "pgp", "EXISTS": None},
        ],
    ),
```

> **Pseudo code**:
Test for the existence of keys `sops` in the primary JSON object.
>
> Goto the `sops` key and test for the existence of keys: `kms` and `pgp`
within the `sops` object/value.

## PRONOM

Ideally `jsonid` can generate evidence enough to warrant the creration of
PRONOM IDs that can then be referenced in the `jsonid` output.

Evantually, PRONOM or a PRONOM-like tool might host an authoritative version
of the `jsonid` registry.

## Output format

For ease of development, the utility currently outputs `yaml`. The structure
is still very fluid, and will also vary depending on the desired level of
detail in the registry, e.g. there isn't currently a lot of information about
the contents beyond a basic title and identifier.

E.g.:

```yaml
---
jsonid: 0.0.0
scandate: 2025-04-21T18:40:48Z
---
file: integration_files/plain.json
additional:
- '@en': data is dict type
depth: 1
documentation:
- archive_team: http://fileformats.archiveteam.org/wiki/JSON
identifiers:
- rfc: https://datatracker.ietf.org/doc/html/rfc8259
- pronom: http://www.nationalarchives.gov.uk/PRONOM/fmt/817
- loc: https://www.loc.gov/preservation/digital/formats/fdd/fdd000381.shtml
- wikidata: https://www.wikidata.org/entity/Q2063
mime:
- application/json
name:
- '@en': JavaScript Object Notation (JSON)
---
```

The structure should become more concrete as `jsonid` is formalized.

## Utils

### json2json

UTF-16 can be difficult to read as UTF-16 uses two bytes per every one, e.g.
`..{.".a.".:. .".b.".}.` is simply `{"a": "b"}`. The utility `json2json.py`
in the utils folder will output UTF-16 as UTF-8 so that signatures can be
more easily derived. A signature derived for UTF-16 looks exactly the same
as UTF-8.

`json2json` can be called from the command line when installed via pip, or
find it in [src.utils][json2json-1].

[json2json-1]: src/utils/json2json.py

## Docs

Dev docs are [available][dev-docs-1].

[dev-docs-1]: https://ffdev-info.github.io/jsonid/jsonid/

----

## Developer install

### pip

Setup a virtual environment `venv` and install the local development
requirements as follows:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements/local.txt
```

### tox

#### Run tests (all)

```bash
python -m tox
```

#### Run tests-only

```bash
python -m tox -e py3
```

#### Run linting-only

```bash
python -m tox -e linting
```

### pre-commit

Pre-commit can be used to provide more feedback before committing code. This
reduces reduces the number of commits you might want to make when working on
code, it's also an alternative to running tox manually.

To set up pre-commit, providing `pip install` has been run above:

* `pre-commit install`

This repository contains a default number of pre-commit hooks, but there may
be others suited to different projects. A list of other pre-commit hooks can be
found [here][pre-commit-1].

[pre-commit-1]: https://pre-commit.com/hooks.html

## Packaging

The [`justfile`][just-1] contains helper functions for packaging and release.
Run `just help` for more information.

[just-1]: https://github.com/casey/just

### pyproject.toml

Packaging consumes the metadata in `pyproject.toml` which helps to describe
the project on the official [pypi.org][pypi-2] repository. Have a look at the
documentation and comments there to help you create a suitably descriptive
metadata file.

### Versioning

Versioning in Python can be hit and miss. You can label versions for
yourself, but to make it reliaable, as well as meaningful is should be
controlled by your source control system. We assume git, and versions can
be created by tagging your work and pushing the tag to your git repository,
e.g. to create a release candidate for version 1.0.0:

```sh
git tag -a 1.0.0-rc.1 -m "release candidate for 1.0.0"
git push origin 1.0.0-rc.1
```

When you build, a package will be created with the correct version:

```sh
just package-source
### build process here ###
Successfully built python_repo_jsonid-1.0.0rc1.tar.gz and python_repo_jsonid-1.0.0rc1-py3-none-any.whl
```

### Local packaging

To create a python wheel for testing locally, or distributing to colleagues
run:

* `just package-source`

A `tar` and `whl` file will be stored in a `dist/` directory. The `whl` file
can be installed as follows:

* `pip install <your-package>.whl`

### Publishing

Publishing for public use can be achieved with:

* `just package-upload-test` or `just package-upload`

`just-package-upload-test` will upload the package to [test.pypi.org][pypi-1]
which provides a way to look at package metadata and documentation and ensure
that it is correct before uploading to the official [pypi.org][pypi-2]
repository using `just package-upload`.

[pypi-1]: https://test.pypi.org
[pypi-2]: https://pypi.org
