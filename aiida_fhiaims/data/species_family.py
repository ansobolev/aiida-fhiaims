"""
The class that represents Aims' `species_defaults` file family (light, tight, really_tight...)
"""
from collections import defaultdict
from pathlib import Path
import re

from ase.data import chemical_symbols

from aiida.orm import Group

from . import chemical_symbols
from .species_file import BasisFile

__all__ = ("BasisFamily",)

name_re = re.compile(r"\d{2}_([A-Za-z]*)_default")


def files_from_folder(folder: Path) -> list[BasisFile]:
    """Parses a set of basis files from a `folder` to a collection of `BasisFile` nodes.
    Sets `setting` for the nodes to the folder name (light, tight...)"""
    basis_names = [f.name for f in folder.glob("*_default")]
    if len(basis_names) == 0:
        raise FileNotFoundError(f"Folder {folder.as_posix()} contains no basis files")

    labels = [name_re.match(f_name).groups()[0] for f_name in basis_names]
    assert all(label in chemical_symbols for label in labels)
    bases = [
        BasisFile(folder / f_name, element=label, setting=folder.name)
        for f_name, label in zip(basis_names, labels)
    ]
    return bases


class BasisFamily(Group):
    """The top-level basis family class for FHI-aims"""

    _bases = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def from_folder(cls, folder: Path, label: str = None) -> "BasisFamily":
        """Gets basis file family node from a `folder`, sets its label to `label`"""
        if label is None:
            label = folder.name
        family = cls(label=label, description=f"{label} species_defaults family")
        family.store()
        setting_dirs = [d for d in folder.iterdir() if d.is_dir()]

        for d in setting_dirs:
            setting_folder = folder / d
            basis_files = files_from_folder(setting_folder)
            family.add_nodes([basis_file.store() for basis_file in basis_files])
        return family

    @property
    def basis_files(self):
        """A dictionary mapping elements to the basis files of the family"""
        if self._bases is None:
            self._bases = defaultdict(dict)
            for f in self.nodes:
                self._bases[f.setting].update({f.element: f})
        return self._bases

    def elements(self, setting):
        """A list of elements for which the basis files are present in the family with the given `setting`"""
        return list(self.basis_files[setting].keys())

    def basis_file(self, element, setting):
        """A getter for the basis file from the family"""
        return self.basis_files[setting][element]
