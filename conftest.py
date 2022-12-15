"""pytest fixtures for simplified testing."""
import pytest

from tests import TEST_DIR

pytest_plugins = [
    "aiida.manage.tests.pytest_fixtures",
    "tests.fixtures",
]

OUTPUT_FILES_DIR = TEST_DIR / "output_files"


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def fhiaims_code(mock_code_factory):
    """Get a fhiaims code."""
    return mock_code_factory(
        label="fhiaims",
        data_dir_abspath=OUTPUT_FILES_DIR,
        entry_point="fhiaims",
        # files *not* to copy into the data directory
        ignore_files=("_aiidasubmit.sh", "_scheduler*"),
    )


@pytest.fixture
def species_path():
    """Get a species_defaults path as string"""
    return TEST_DIR / "species_defaults"


@pytest.fixture
def inputs_path():
    """Get a species_defaults path as string"""
    return TEST_DIR / "inputs"
