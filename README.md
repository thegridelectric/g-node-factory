# G Node Factory

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

The GNodeFactory is an actor in a larger Transactive Energy Management (TEM) system. Within that system, it has the authority for creating and updating GNodes. Among other things, it has the authority for creating and updating `TerminalAssets`, which represent the devices capable of transacting on electricity markets within the TEM.

This repo has been developed through the generous funding of a grant provided by the [Algorand Foundation](https://www.algorand.foundation/). For more context, please read our Algorand [Milestone 1 writeup](docs/wiki/milestone-1.md) and Milestone 2 deck. For design specifications for the repo, go [here](docs/wiki/design-specifications.md). For a very short description of what GNodes are and why we need a factory for them, skip to [Background](#Background) below.

## Local Demo setup

1. Set up python environment

   ```
   poetry install

   poetry shell
   ```

2. Install [docker](https://docs.docker.com/get-docker/)

3. Start docker containers

- **X86 CPU**:

  ```
  docker compose -f docker-demo-x86.yml up -d
  ```

- **arm CPU**:

  ```
  docker compose -f docker-demo-arm.yml up -d
  ```

4. Clone [Algorand Sandbox](https://github.com/algorand/sandbox) and from that directory

   ```
   ./sandbox up dev
   ```

   This starts up a local blockchain on your computer. It can take a couple of minutes for the
   initial setup.

   **note** running the sandbox in dev mode means the chain instantly creates a block as soon as you send a transaction, instead of once every 4 seconds. This means demos and development go much faster.

5. Run before each demo:

- From this repo, **flush database**:
  ```
  ./reset-dev-db.sh
  ```
- From sandbox repo, **flush blockchin**:
  ```
  ./sandbox reset
  ```

6. Start the PythonTaDaemon FastAPI:

   ```
   uvicorn gnf.rest_api:app --reload
   ```

   (go to http://127.0.0.1:8000/docs# for inspecting the api)

7. Run the milestone 1 demo from this repo:

   ```
   python demo.py
   ```

## Explaining what the demo does

1.  **Loads in preliminary GNodes** One axiom for adding a GNode is that its parent must already exist, unless it is the root. Since this demo involves adding `TerminalAssets`, we need to add the root world GNode (`d1`), the root of the electric grid (`d1.isone`), and then a few ConductorTopologyNodes that
    are stepping down in voltage (`d1.isone.ver`, `d1.isone.ver.keene`).
2.  **Creates a new TerminalAsset** Creates a TerminalAsset `d1.isone.ver.keene.holly.ta` for Holly's heating system. This includes first setting up MollyMetermaid as a validator, and then having MollyMetermaid validate Holly's heating system. This process results in a TaValidator certificate (an NFT) for MollyMetermaid and a TaDeed (also an NFT) for HollyHomeowner.
3.  **Adding a new ConductorTopologyNode** Creates a ConductorTopologyNode `d1.isone.ver.keene.pwrs`, which triggers a cascade of updating the aliases for all of its descendants, including HollyHomeowner's `TerminalAsset`.

## Testing

pytest -v

## Configuration and secrets

For non-dev lifecycle,
look at `src/gnf/config`. This has the default values, which are overwritten with values from a
git ignored top-level `.env` file. All dev examples are intended to run without needing to create
a `.env` file. A template `.env-template` is provided.

## Code derivation tools

The primary derivation tool used for this is [ssot.me](https://explore.ssot.me/app/#!/home), developed by EJ Alexandra of [An Abstract Level LLC](https://effortlessapi.com/pages/effortlessapi/blog). All of the xslt code in `CodeGeneration` uses this tool.

The `ssotme` cli and its upstream `ssotme` service pull data from our [private airtable](https://airtable.com/appgibWM6WZW20bBx/tblRducbzl15OWmwv/viwIvHvZcrMELIP3x?blocks=hide) down into an odxml file and a json file, and then references local `.xslt` scripts in order to derive code. The `.xslt` allows for two toggles - one where files are always overwritten, and one where the derivation tools will leave files alone once any hand-written code is added. Mostly that toggle is set to `always overwrite` since we are working with immutable schemata. Note that the `ssotme cli` requires an internet connection to work, since it needs to access the upstream `ssotme` service.

If you want to add enums or schema, you will need access to the `ssotme cli` and the airtable. Contact Jessica for this.

## Background

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
