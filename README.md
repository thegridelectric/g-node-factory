# G Node Factory

[![PyPI](https://img.shields.io/pypi/v/g-node-factory.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/g-node-factory.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/g-node-factory)][python version]
[![License](https://img.shields.io/pypi/l/g-node-factory)][license]

[![Read the documentation at https://g-node-factory.readthedocs.io/](https://img.shields.io/readthedocs/g-node-factory/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/thegridelectric/g-node-factory/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/thegridelectric/g-node-factory/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/g-node-factory/
[status]: https://pypi.org/project/g-node-factory/
[python version]: https://pypi.org/project/g-node-factory
[read the docs]: https://g-node-factory.readthedocs.io/
[tests]: https://github.com/thegridelectric/g-node-factory/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/thegridelectric/g-node-factory
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

The GNodeFactory is an actor in a larger Transactive Energy Management (TEM) system. Within that system, it has the authority for creating and updating GNodes. Among other things, it has the authority for creating and updating `TerminalAssets`, which represent the devices capable of transacting on electricity markets within the TEM.

This repo has been developed through the generous funding of a grant provided by the [Algorand Foundation](https://www.algorand.foundation/). For more context, please read our Algorand [Milestone 1 writeup](docs/wiki/milestone-1.md). For design specifications for the repo, go [here](docs/wiki/milestone-1-specifications.md). For a very short description of what GNodes are and why we need a factory for them, skip to [Background](#Background) below.

# Local Demo setup

1.  Clone [Algorand Sandbox](https://github.com/algorand/sandbox) and from that directory:

```
./sandbox up
```

2. Follow instructions below to install python and its required libraries

3. From `python_code` (the working directory):

```
cp django_related/dev_settings.py django_related/settings.py
```

4. From the `python_code` directory, with `venv` activated, run
   ```
   ./reset-dev-db.sh
   python demo.py
   ```
   This goes through the process of getting `MollyMetermaid` set up as a recognized Validator. The demo requires that all of the various accounts are free of assets. Therefore, if you have run the test suite or already run the demo, you will also need to run `./sandbox reset` from your Algorand sandbox directory before doing the above.

# Testing

From the top level directory with `venv` activated:

```
export PYTHONPATH=`pwd`/python_code:$PYTHONPATH
pytest -v
```

# Developing

## Python related

### Install Python and its required libraries

- Use python 3.10.4
- At present the code is not packaged and assumes `python_code` as the pythonpath. So from `python_code` subdirectory:
  - `python -m venv venv`
  - `source venv/bin/activate`
  - `pip install -r requirements/dev.txt`

### Message Types, Schema, APIs, ABIs - how does this communicate

Over the last year, we have been developing a new structure of APIs and type schema for the various applications in the GridWorks ecosystem. While there are a lot of useful design in existing schema structures (like cap'n proto) we are looking for something that:
(a) allows for single-type schema evolution (where every message sent has a specific type) instead of evolution of an entire collection of types and
(b) allows for significant semantic checking. We have developed our own native mechanisms for this using code generation tools. At present they are overly complicated and not as functional as we want re schema evolution. However, they allow for off-loading almost all of the syntax and semantics validation to the schema sdk, taking this burden off the application code using them.

The semantic is organized into a set of axioms that must hold true for any instance
of the type. To see this working, looka t and run `schema_demo.py` while also
examining the axioms in `schemata/create_tadeed_algo.py

### Adding libraries

- If you want to add a new library used in all contexts, then add it to requirements/base.in and from the `requirements` subfolder run
  - `pip-compile --output-file=base.txt base.in`
  - `pip-compile --output-file=dev.txt dev.in`

We use pip-tools to organize requirements. The `.in` files clarify the key modules (including which ones are important to pin and which ones can be set to the latest release) and then the corresponding `.txt` files are generated via pip-tools. This means we always run on pinned requirements (from the .txt files) and can typically upgrade to the latest release, except for cases where the code requires a pinned older version.

The pip-tools also allow for building layers of requirements on top of each other. This allows us to have development tools that are not needed in production to show up for the first time in `dev.txt`, for example (like the pip-tool itself).

### Python Configuration and secrets

The python code is meant to run out-of-the box as long as you have done the above step. Configurations
and secrets are passed around in a `settings` object of type `GnfSettings` defined in `python_code/settings.py`.
These come with default values defined in settings.py, which are overwritten with values from the
git ignored top-level `.env` file. All dev examples are intended to run without needing to create
a `.env` file. A template `.env-template` is provided as well.

### Python Code derivation tools

The schemata
The primary derivation tool used for this is [ssot.me](https://explore.ssot.me/app/#!/home), developed by EJ Alexandra of [An Abstract Level LLC](https://effortlessapi.com/pages/effortlessapi/blog).

The `ssotme` cli and its upstream `ssotme` service pull data from our [private airtable](https://airtable.com/appgibWM6WZW20bBx/tblRducbzl15OWmwv/viwIvHvZcrMELIP3x?blocks=hide) down into an odxml file and a json file, and then references local `.xslt` scripts in order to derive code. The `.xslt` allows for two toggles - one where files are always overwritten, and one where the derivation tools will leave files alone once any hand-written code is added. Mostly that toggle is set to `always overwrite` since we are working with immutable schemata. Note that the `ssotme cli` requires an internet connection to work, since it needs to access the upstream `ssotme` service.

If you want to add enums or schema, you will need access to the `ssotme cli` and the airtable. Contact Jessica for this.

# Background

What are GNodes and why do we need a factory for them?

GNodes come in several flavors (see [this enum](python_code/enums/core_g_node_role_map.py)), and the first flavor to understand is a [TerminalAsset](docs/wiki/terminal-asset.md). In fact for now the GNodeFactory is really a `TerminalAsset` factory. A `TerminalAsset` is tuple of three things:

- **An electrical device** connected to the grid that can consume and/or produce electrical power;
- **An electrical meter** that meters exactly the Terminal Asset and has the accuracy characteristics required to meet existing and pending grid balancing challenges (that is, the challenge of keeping electric supply and electric demand in balance on various timescales as wind and solar electricity become more prevalent); and
- **A lat/lon pair** that can be used to capture where the electrical device is connected to the topology

Such a triplet in the real world is called a `TransactiveDevice`. So in shorthand, a `TerminalAsset` is a representation in code of a `TransactiveDevice` in the real world.

The goal of GNode Factory is to support transactive devices, especially transactive loads, in taking on the mantle of balancing the electric grid in a renewable future. In short, we need to [redefine demand response](docs/wiki/redefining-demand-response.md). This requires a solid alignment between the online abstraction of the `TerminalAsset` and the physical reality a transactive device, in particular of the three things listed above. It also requires trust from a variety of players that this alignment is solid - i.e., that a `TerminalAsset` code object claiming a particular grade of metering, a particular kind of device and a particular location on the electric grid does in fact mean that there is a real physical transactive device with these three attributes in the physical world.

The GNodeFactory stands at the boundary between the physical world and the world of code, maintaining a high fidelity connection between Transactive Devices and _digital representations_ of these Transactive Devices as `TerminalAssets.`

## Features

- TODO

## Requirements

- TODO

## Installation

You can install _G Node Factory_ via [pip] from [PyPI]:

```console
$ pip install g-node-factory
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_G Node Factory_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/thegridelectric/g-node-factory/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/thegridelectric/g-node-factory/blob/main/LICENSE
[contributor guide]: https://github.com/thegridelectric/g-node-factory/blob/main/CONTRIBUTING.md
[command-line reference]: https://g-node-factory.readthedocs.io/en/latest/usage.html
