""" Tests for command line interface of ."""
from click.testing import CliRunner

from aiida_fhiaims.cli.species_defaults import install, list_
from aiida_fhiaims.data.species_family import BasisFamily


# pylint: disable=attribute-defined-outside-init
class TestDataCli:
    """Test verdi data cli plugin."""

    def setup_method(self):
        """Prepare nodes for cli tests."""
        self.runner = CliRunner()

    def test_install(self, species_path):
        """Test 'verdi data species-default install <path>'

        Tests that it can be reached and that it installs the test basis family
        """
        # noinspection PyTypeChecker
        result = self.runner.invoke(
            install, species_path.as_posix(), catch_exceptions=False
        )
        assert "OK" in result.output
        family = BasisFamily.collection.get(label="good")
        assert len(family.basis_files) == 2
        assert "As" in family.elements("light")
        assert "As" in family.elements("tight")

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

    def test_list(self, species_family):
        """A test of `list` command line option"""
        _ = species_family(label="good")
        # noinspection PyTypeChecker
        result = self.runner.invoke(list_, catch_exceptions=False)
        assert "good" in result.output
