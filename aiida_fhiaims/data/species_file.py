"""
The class that represents Aims' `species_default` file
"""
from aiida.orm import SinglefileData


class BasisFile(SinglefileData):
    """The class for FHI-aims one basis file stored in AiiDA DB"""

    def __init__(self, file, **kwargs):
        super().__init__(file, **kwargs)
