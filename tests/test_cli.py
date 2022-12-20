""" Tests for command line interface of ."""
from click.testing import CliRunner
import pytest

from aiida.common.exceptions import NotExistent

from aiida_fhiaims.cli.species_defaults import install, list_
from aiida_fhiaims.data.species_family import BasisFamily


# pylint: disable=attribute-defined-outside-init
class TestDataCli:
    """Test verdi data cli plugin."""

    def setup_method(self):
        """Prepare nodes for cli tests."""
        self.runner = CliRunner()

    def test_install_one(self, species_path):
        """Tests 'verdi data species-defaults install <path to one family>'"""
        test_path = species_path / "default"
        # noinspection PyTypeChecker
        result = self.runner.invoke(
            install, test_path.as_posix(), catch_exceptions=False
        )
        assert "OK" in result.output
        family = BasisFamily.collection.get(label="default")
        assert len(family.basis_files["light"]) == 2
        assert "As" in family.elements("really_tight")
        with pytest.raises(NotExistent):
            BasisFamily.collection.get(label="NAO-J")

    def test_install_several(self, species_path):
        """Test 'verdi data species-default install <path>'

        Tests that it can be reached and that it installs the test basis family
        """
        # noinspection PyTypeChecker
        result = self.runner.invoke(
            install, species_path.as_posix(), catch_exceptions=False
        )
        assert "OK" in result.output
        family = BasisFamily.collection.get(label="default")
        assert len(family.basis_files) == 3
        assert len(family.basis_files["light"]) == 2
        assert len(family.basis_files["really_tight"]) == 2
        assert "As" in family.elements("really_tight")
        assert "No" in family.elements("tight")
        family = BasisFamily.collection.get(label="NAO-J")
        assert "NAO-J-2" in family.basis_files
        assert "C" in family.elements("NAO-J-2")
        assert "N" in family.elements("NAO-J-3")

    def test_install_from_env_var(self, species_path):
        """A test to check if the basis family can be installed using `AIMS_SPECIES_DIR` environmental variable"""
        env = {"AIMS_SPECIES_DIR": "some_dir"}
        # noinspection PyTypeChecker
        result = self.runner.invoke(install, catch_exceptions=False, env=env)
        assert "Invalid value for 'PATH'" in result.output
        env = {"AIMS_SPECIES_DIR": species_path.as_posix()}
        # noinspection PyTypeChecker
        result = self.runner.invoke(install, catch_exceptions=False, env=env)
        assert "OK" in result.output

    def test_install_fail(self, inputs_path):
        """Test failing installation due to providing the wrong path to the species_defaults family"""
        # noinspection PyTypeChecker
        result = self.runner.invoke(
            install, inputs_path.as_posix(), catch_exceptions=False
        )
        assert "FAILED" in result.output

    def test_list(self, species_path):
        """A test of `list` command line option"""
        # noinspection PyTypeChecker
        self.runner.invoke(install, species_path.as_posix(), catch_exceptions=False)
        # noinspection PyTypeChecker
        result = self.runner.invoke(list_, catch_exceptions=False)
        assert "default" in result.output
