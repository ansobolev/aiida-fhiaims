"""Tests for aiida-fhiaims BasisFamily class"""
import pytest

from aiida.orm import SinglefileData

from aiida_fhiaims.data.species_family import BasisFamily


def test_basis_family_install(species_path):
    """A test of installing a species_defaults family"""
    species_dir = species_path / "default"
    family = BasisFamily.from_folder(species_dir)
    assert family.label == "default"
    assert "Ga" in family.elements("light")
    assert "As" in family.elements("tight")
    species_dir = species_path / ".." / "inputs"
    with pytest.raises(FileNotFoundError):
        BasisFamily.from_folder(species_dir)


def test_basis_family(default_species_family, structure):
    """Test working with the BasisFamily entity"""
    assert "Ga" in default_species_family.elements("light")
    with pytest.raises(ValueError):
        default_species_family.basis_file("H", setting="light")
    with pytest.raises(ValueError):
        default_species_family.get_species_defaults(
            setting="light", elements=["Ga", "As"], structure=structure
        )
    with pytest.raises(ValueError):
        default_species_family.get_species_defaults(setting="light")
    with pytest.raises(ValueError):
        default_species_family.get_species_defaults(setting="light", elements="Ga")
    with pytest.raises(ValueError):
        default_species_family.get_species_defaults(setting="light", structure="Ga")
    species_defaults = default_species_family.get_species_defaults(
        setting="light", elements=["Ga", "As"]
    )
    assert "Ga" in species_defaults
    assert isinstance(species_defaults["Ga"], SinglefileData)
