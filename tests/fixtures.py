"""Pytest fixtures for aiida-fhiaims tests"""

from ase.io import read
import pytest
import yaml

from aiida.orm import StructureData

from aiida_fhiaims.data.parameters import AimsParameters
from aiida_fhiaims.data.species_family import BasisFamily

from . import TEST_DIR


@pytest.fixture
def structure():
    """Structure, takes ASE JSON files as inputs"""

    def _get_structure(file_name):
        file_path = TEST_DIR / "inputs" / "structures" / f"{file_name}.json"
        return StructureData(ase=read(file_path))

    return _get_structure


@pytest.fixture
def parameters():
    """Parameters, takes ASE JSON files as inputs"""

    def _get_parameters(file_name):
        file_path = TEST_DIR / "inputs" / "parameters" / f"{file_name}.yaml"
        with open(file_path) as f:
            return AimsParameters(dict=yaml.safe_load(f))

    return _get_parameters


@pytest.fixture
def species_family():
    """Basis family from species_defaults, stored under label"""

    def _get_species_family(label):
        species_folder = TEST_DIR / "species_defaults" / label
        return BasisFamily.from_folder(species_folder, label=label)

    return _get_species_family
