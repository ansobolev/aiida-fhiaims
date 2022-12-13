"""pytest fixtures for simplified testing."""
from pathlib import Path

import pytest

pytest_plugins = [
    "aiida.manage.tests.pytest_fixtures",
    "aiida_testing.mock_code",
    "aiida_testing.export_cache",
]

OUTPUT_FILES_DIR = Path(__file__).parent.resolve() / "tests" / "output_files"


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
        ignore_files=("_aiidasubmit.sh", "file*"),
    )


@pytest.fixture
def species_path():
    """Get a species_defaults path as string"""
    return (Path(__file__).parent.resolve() / "tests" / "species_defaults").as_posix()
