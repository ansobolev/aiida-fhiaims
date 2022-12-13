"""Top-level file for aiida-fhiaims data nodes containing several submodule-wide constants"""

from ase.data import chemical_symbols as symbols

__all__ = ("chemical_symbols",)

chemical_symbols = [
    "Emptium",
] + symbols[1:]
