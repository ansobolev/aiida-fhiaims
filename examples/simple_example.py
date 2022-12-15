#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./simple_example.py
"""
from pathlib import Path

from ase.build import bulk
import click

from aiida import cmdline, engine
from aiida.orm import StructureData
from aiida.plugins import CalculationFactory, DataFactory

from aiida_fhiaims import helpers
from aiida_fhiaims.helpers import get_species_family

INPUT_DIR = Path(__file__).parent.resolve() / "input_files"
SPECIES_DIR = Path(__file__).parent.resolve() / "species_defaults"


def test_run(fhiaims_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not fhiaims_code:
        # get code
        computer = helpers.get_computer()
        fhiaims_code = helpers.get_code(entry_point="fhiaims", computer=computer)
    _ = get_species_family("example_family", species_dir=SPECIES_DIR)

    # Prepare input parameters
    ase_struct = bulk("Cu", "fcc", a=3.6)
    parameters = {
        "xc": "pbe",
        "k_grid": [8, 8, 8],
        "species_defaults": {"family": "example_family", "setting": "light"},
    }

    # set up calculation
    inputs = {
        "code": fhiaims_code,
        "structure": StructureData(ase=ase_struct),
        "parameters": DataFactory("fhiaims.parameters")(dict=parameters),
        "metadata": {
            "description": "Test job submission with the aiida_fhiaims plugin",
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    # from aiida.engine import submit
    # future = submit(CalculationFactory('fhiaims'), **inputs)
    result = engine.run(CalculationFactory("fhiaims"), **inputs)

    computed_diff = result["fhiaims"].get_content()
    print(f"Computed diff between files: \n{computed_diff}")


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_01.py --code diff@localhost

    Alternative (creates diff@localhost-test code): $ ./example_01.py

    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
