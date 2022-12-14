[![Build Status][ci-badge]][ci-link]
[![Coverage Status][cov-badge]][cov-link]
[![Docs status][docs-badge]][docs-link]
[![PyPI version][pypi-badge]][pypi-link]

# aiida-fhiaims

An AiiDA plugin for FHI-aims code

This plugin is the default output of the
[AiiDA plugin cutter](https://github.com/aiidateam/aiida-plugin-cutter),
intended to help developers get started with their AiiDA plugins.

## Repository contents

* [`.github/`](.github/): [Github Actions](https://github.com/features/actions) configuration
  * [`ci.yml`](.github/workflows/ci.yml): runs tests, checks test coverage and builds documentation at every new commit
  * [`publish-on-pypi.yml`](.github/workflows/publish-on-pypi.yml): automatically deploy git tags to PyPI - just generate a [PyPI API token](https://pypi.org/help/#apitoken) for your PyPI account and add it to the `pypi_token` secret of your github repository
* [`aiida_fhiaims/`](aiida_fhiaims/): The main source code of the plugin package
  * [`data/`](aiida_fhiaims/data/): A new `DiffParameters` data class, used as input to the `DiffCalculation` `CalcJob` class
  * [`calculations.py`](aiida_fhiaims/calculations.py): A new `DiffCalculation` `CalcJob` class
  * [`cli/`](aiida_fhiaims/cli/): Extensions of the `verdi data` command line interface for the `Aims` `species_default` class
  * [`parsers/`](aiida_fhiaims/parsers/): A set of parsers for FHI-aims output files
* [`docs/`](docs/): A documentation template ready for publication on [Read the Docs](http://aiida-fhiaims.readthedocs.io/en/latest/)
* [`examples/`](examples/): An example of how to submit a calculation using this plugin
* [`tests/`](tests/): Basic regression tests using the [pytest](https://docs.pytest.org/en/latest/) framework (submitting a calculation, ...). Install `pip install -e .[testing]` and run `pytest`.
* [`.gitignore`](.gitignore): Telling git which files to ignore
* [`.pre-commit-config.yaml`](.pre-commit-config.yaml): Configuration of [pre-commit hooks](https://pre-commit.com/) that sanitize coding style and check for syntax errors. Enable via `pip install -e .[pre-commit] && pre-commit install`
* [`.readthedocs.yml`](.readthedocs.yml): Configuration of documentation build for [Read the Docs](https://readthedocs.org/)
* [`LICENSE`](LICENSE): License for your plugin
* [`README.md`](README.md): This file
* [`conftest.py`](conftest.py): Configuration of fixtures for [pytest](https://docs.pytest.org/en/latest/)
* [`pyproject.toml`](setup.json): Python package metadata for registration on [PyPI](https://pypi.org/) and the [AiiDA plugin registry](https://aiidateam.github.io/aiida-registry/) (including entry points)


For more information, see the [developer guide](https://aiida-fhiaims.readthedocs.io/en/latest/developer_guide).


## Features

 * Add input files using `SinglefileData`:
   ```python
   SinglefileData = DataFactory('singlefile')
   inputs['file1'] = SinglefileData(file='/path/to/file1')
   inputs['file2'] = SinglefileData(file='/path/to/file2')
   ```

 * Specify command line options via a python dictionary and `DiffParameters`:
   ```python
   d = { 'ignore-case': True }
   DiffParameters = DataFactory('fhiaims')
   inputs['parameters'] = DiffParameters(dict=d)
   ```

 * `DiffParameters` dictionaries are validated using [voluptuous](https://github.com/alecthomas/voluptuous).
   Find out about supported options:
   ```python
   DiffParameters = DataFactory('fhiaims')
   print(DiffParameters.schema.schema)
   ```

## Installation

```shell
pip install aiida-fhiaims
verdi quicksetup  # better to set up a new profile
verdi plugin list aiida.calculations  # should now show your calclulation plugins
```


## Usage

Here goes a complete example of how to submit a test calculation using this plugin.

A quick demo of how to submit a calculation:
```shell
verdi daemon start     # make sure the daemon is running
cd examples
./example_01.py        # run test calculation
verdi process list -a  # check record of calculation
```

The plugin also includes verdi commands to inspect its data types:
```shell
verdi data fhiaims list
verdi data fhiaims export <PK>
```

## Development

```shell
git clone https://github.com/ansobolev/aiida-fhiaims .
cd aiida-fhiaims
pip install --upgrade pip
pip install -e .[pre-commit,testing]  # install extra dependencies
pre-commit install  # install pre-commit hooks
pytest -v  # discover and run all tests
```

See the [developer guide](http://aiida-fhiaims.readthedocs.io/en/latest/developer_guide/index.html) for more information.

## License

MIT
## Contact

sobolev@fhi.mpg.de


[ci-badge]: https://github.com/ansobolev/aiida-fhiaims/workflows/ci/badge.svg?branch=master
[ci-link]: https://github.com/ansobolev/aiida-fhiaims/actions
[cov-badge]: https://coveralls.io/repos/github/ansobolev/aiida-fhiaims/badge.svg?branch=master
[cov-link]: https://coveralls.io/github/ansobolev/aiida-fhiaims?branch=master
[docs-badge]: https://readthedocs.org/projects/aiida-fhiaims/badge
[docs-link]: http://aiida-fhiaims.readthedocs.io/
[pypi-badge]: https://badge.fury.io/py/aiida-fhiaims.svg
[pypi-link]: https://badge.fury.io/py/aiida-fhiaims
