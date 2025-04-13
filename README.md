# jsonid

<!-- markdownlint-disable -->
<img
    src="https://github.com/ffdev-info/jsonid/blob/main/static/images/JSON_logo-crockford.png?raw=true"
    alt="JSON ID logo based on JSON Logo by Douglas Crockford"
    width="200px" />
<!-- markdownlint-enable -->

[JSON][JSON-1]-Identification ruleset and tool.

[JSON-1]: https://www.json.org/json-en.html

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
    "key 1": "value
}
```

PRONOM signatures are not expressive enough for complicated JSON objects.

If I want PRONOM to find `key 1` I have to use a wildcard, so something like:

```text
BOF: "7B*226B6579203122"
EOF: "7D"
```

But if I then want to match on `key 2` as well as `key 1` things start getting
complicated as they aren't guaranteed by the JSON spec to be in the same order.
They're not even guaranteed to be in the same positions (from a visual
perspective) when other keys are also used in the object.

`jsonid` tries to compensate for this by using JSON's own strengths to use its
keys and values as "markers" that can help to identify what we're looking
at.

## Ruleset

`jsonid` currently defines a small set of rules that help us to identify JSON
documents.

The rules are each their own data-structures. The structures are processed
sequentially in order to determine what kind of JSON document we might be
looking at. jsonid is currently designed to identify the existence of
information but you can also add some negation, e.g. to remove false-positives.
Do this carefully!

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

> NB.: `jsonid` is an
early-days tool so there is a lot of opportunity to add/remove to these
if it proves its worth

## Registry

A "registry" module is used to store JSON markers for identifying documents
and objects. The registry is a work in progress and will be exported and
rewritten if `jsonid` can prove useful to its communities.

The registry can be read in the source code here:

* [Registry](src/jsonid/registry_data.py).

## PRONOM

Ideally we will add PRONOM identifiers `jsonid`'s formats. The tool can be
used to generate evidence enough to be able to add tthis data to PRONOM
in future.

## Output format

A very basic `yaml` output is used to output data about identified files.
This will need to be reformatted and reshaped as the concept is proved.

## What does `jsonid` get you?

At the very least, `jsonid` should identify json files on your system as json.
That's already a pretty good position to be in.

The ruleset should then allow you to identify a decent number of json objects,
especially those that have a well-defined structure. Examples we have in the
registry data include things like ActivityPub streams, RO-CRATE metadata,
IIIF API data and so on.

If the ruleset works for JSON we might be able to apply it to other formats
such as YAML in future.

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
make package-source
### build process here ###
Successfully built python_repo_jsonid-1.0.0rc1.tar.gz and python_repo_jsonid-1.0.0rc1-py3-none-any.whl
```

### Local packaging

To create a python wheel for testing locally, or distributing to colleagues
run:

* `make package-source`

A `tar` and `whl` file will be stored in a `dist/` directory. The `whl` file
can be installed as follows:

* `pip install <your-package>.whl`

### Publishing

Publishing for public use can be achieved with:

* `make package-upload-test` or `make package-upload`

`make-package-upload-test` will upload the package to [test.pypi.org][pypi-1]
which provides a way to look at package metadata and documentation and ensure
that it is correct before uploading to the official [pypi.org][pypi-2]
repository using `make package-upload`.

[pypi-1]: https://test.pypi.org
[pypi-2]: https://pypi.org
