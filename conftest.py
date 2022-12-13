"""pytest fixtures for simplified testing."""
from pathlib import Path

import pytest

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def fhiaims_code(aiida_local_code_factory):
    """Get a fhiaims code."""
    return aiida_local_code_factory(executable="aims.x", entry_point="fhiaims")


@pytest.fixture
def species_path():
    """Get a species_defaults path as string"""
    return (Path(__file__).parent.resolve() / "tests" / "species_defaults").as_posix()
