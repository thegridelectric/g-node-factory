# G Node Factory

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

The [GNodeFactory](https://gridworks.readthedocs.io/en/latest/g-node-factory.html) is a foundational actor in GridWorks.
Please go to [Gridworks Docs](https://gridworks.readthedocs.io/en/latest/index.html) to read more, and
go to [The Millinocket Tutorial](https://gridworks.readthedocs.io/en/latest/millinocket-tutorial.html) for a dev use-case of
this repo.

This repo has been developed through the generous funding of a grant provided by the [Algorand Foundation](https://www.algorand.foundation/).

## Testing

pytest -v

## Code derivation tools

The primary derivation tool used for this is [ssot.me](https://explore.ssot.me/app/#!/home), developed by EJ Alexandra of [An Abstract Level LLC](https://effortlessapi.com/pages/effortlessapi/blog). All of the xslt code in `CodeGeneration` uses this tool.

The `ssotme` cli and its upstream `ssotme` service pull data from our [private airtable](https://airtable.com/appgibWM6WZW20bBx/tblRducbzl15OWmwv/viwIvHvZcrMELIP3x?blocks=hide) down into an odxml file and a json file, and then references local `.xslt` scripts in order to derive code. The `.xslt` allows for two toggles - one where files are always overwritten, and one where the derivation tools will leave files alone once any hand-written code is added. Mostly that toggle is set to `always overwrite` since we are working with immutable schemata. Note that the `ssotme cli` requires an internet connection to work, since it needs to access the upstream `ssotme` service.

If you want to add enums or schema, you will need access to the `ssotme cli` and the airtable. Contact Jessica for this.

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
