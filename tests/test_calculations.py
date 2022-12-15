""" Tests for calculations."""
from aiida.engine import run_get_node
from aiida.plugins import CalculationFactory


def test_process(fhiaims_code, species_family, structure, parameters):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    # Prepare input parameters
    ga_as_structure = structure("GaAs")
    parameters = parameters("simple")
    assert species_family(label=parameters["species_defaults"]["family"])

    # set up calculation
    inputs = {
        "code": fhiaims_code,
        "structure": ga_as_structure,
        "parameters": parameters,
    }

    _, node = run_get_node(CalculationFactory("fhiaims"), **inputs)
    assert node.is_finished_ok
