"""
The class that represents Aims' `species_defaults` file family (light, tight, really_tight...)
"""
from aiida.orm import Group


class BasisFamily(Group):
    """The top-level basis family class for FHI-aims"""

    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
