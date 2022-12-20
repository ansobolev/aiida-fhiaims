"""
The class that represents Aims' `species_defaults` file family (light, tight, really_tight...)
"""
from collections import defaultdict
from pathlib import Path
import re
from typing import Dict, List

from ase.data import chemical_symbols

from aiida.orm import Group, StructureData

from . import chemical_symbols
from .species_file import BasisFile

__all__ = ("BasisFamily",)

name_re = re.compile(r"\d{2,3}_([A-Za-z]*)_default")


def files_from_folder(folder: Path) -> List[BasisFile]:
    """Parses a set of basis files from a `folder` to a collection of `BasisFile` nodes.
    Sets `setting` for the nodes to the folder name (light, tight...)"""
    basis_names = [f.name for f in folder.glob("*_default")]
    if len(basis_names) == 0:
        raise FileNotFoundError(f"Folder {folder.as_posix()} contains no basis files")

    labels = [
        name_re.match(f_name).groups()[0]
        for f_name in basis_names
        if name_re.match(f_name) is not None
    ]
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

        # we call the directory `settings dir` if it's inside a folder and there are *_default files inside it
        setting_dirs = [
            d for d in folder.iterdir() if d.is_dir() and list(d.glob("*_default"))
        ]
        if not setting_dirs:
            raise FileNotFoundError(f"No species_defaults files found inside {folder}")

        if label is None:
            label = folder.name
        family = cls(label=label, description=f"{label} species_defaults family")
        family.store()

        for d in setting_dirs:
            setting_folder = folder / d
            basis_files = files_from_folder(setting_folder)
            family.add_nodes([basis_file.store() for basis_file in basis_files])
        return family

    @property
    def basis_files(self) -> Dict[str, Dict[str, BasisFile]]:
        """A dictionary mapping elements to the basis files of the family"""
        if self._bases is None:
            self._bases = defaultdict(dict)
            for f in self.nodes:
                self._bases[f.setting].update({f.element: f})
        return self._bases

    def elements(self, setting: str) -> List[str]:
        """A list of elements for which the basis files are present in the family with the given `setting`"""
        return list(self.basis_files[setting].keys())

    def basis_file(self, element: str, setting: str) -> BasisFile:
        """A getter for the basis file from the family"""
        if setting in self.basis_files:
            if element in self.basis_files[setting]:
                return self.basis_files[setting][element]
        raise ValueError(
            f"Family {self.label} does not contain the basis file for element {element} with {setting} "
            f"setting"
        )

    def get_species_defaults(
        self,
        setting: str,
        elements: List[str] = None,
        structure: StructureData = None,
    ) -> Dict[str, BasisFile]:
        """Returns the dictionary mapping the given `elements` (or elements of a given `structure`)
        to basis files for a given `setting`. Loosely based upon `aiida_pseudo.groups.family.pseudo.get_pseudos`
        """
        if elements is not None and structure is not None:
            raise ValueError(
                "Cannot specify both keyword arguments `elements` and `structure`."
            )

        if elements is None and structure is None:
            raise ValueError(
                "Have to specify one of the keyword arguments `elements` and `structure`."
            )

        if elements is not None and not isinstance(elements, (list, tuple)):
            raise ValueError("elements should be a list or tuple of symbols.")

        if structure is not None and not isinstance(structure, StructureData):
            raise ValueError("structure should be a `StructureData` instance.")

        if structure is not None:
            return {
                kind.name: self.basis_file(kind.symbol, setting)
                for kind in structure.kinds
            }

        return {element: self.basis_file(element, setting) for element in elements}
