"""
The class that represents Aims' `species_defaults` file family (light, tight, really_tight...)
"""
from pathlib import Path
import re

from ase.data import chemical_symbols

from aiida.orm import Group

from aiida_fhiaims.data.species_file import BasisFile


class BasisFamily(Group):
    """The top-level basis family class for FHI-aims"""

    _bases = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self._bases is None:
            self._bases = {}

    @classmethod
    def from_folder(cls, folder: Path, label: str) -> "BasisFamily":
        """Gets basis file family node from a `folder`, sets its label to `label`"""
        family = cls(label=label, description=f"{label} species_defaults family")
        basis_files = cls.files_from_folder(folder)
        family.store()
        family.add_nodes([basis_file.store() for basis_file in basis_files])
        return family

    @classmethod
    def files_from_folder(cls, folder: Path) -> list[BasisFile]:
        """Parses a set of basis files from a `folder` to a collection of `BasisFile` nodes"""
        basis_names = [f.name for f in folder.glob("*_default")]
        if len(basis_names) == 0:
            raise FileNotFoundError(
                f"Folder {folder.as_posix()} contains no basis files"
            )
        name_re = re.compile(r"(\d{2})_([A-Za-z]*)_default")
        labels = [name_re.match(f_name).groups() for f_name in basis_names]
        symbols = [
            "Emptium",
        ] + chemical_symbols
        assert all(label[1] in symbols for label in labels)
        bases = [
            BasisFile(folder / f_name, label=label[1])
            for f_name, label in zip(basis_names, labels)
        ]
        return bases

    @property
    def basis_files(self):
        """A dictionary mapping elements to the basis files of the family"""
        if not self._bases:
            self._bases = {f.label: f for f in self.nodes}
        return self._bases

    @property
    def elements(self):
        """A list of elements for which the basis files are present in the family"""
        return list(self.basis_files.keys())

    def basis_file(self, element):
        """A getter for the basis file from the family"""
        return self.basis_files[element]
