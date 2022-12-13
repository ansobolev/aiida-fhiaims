"""
The class that represents Aims' `species_default` file
"""
import re

from aiida.orm import SinglefileData

from . import chemical_symbols

__all__ = ("BasisFile",)

label_re = re.compile(r"([A-Za-z]*)_([A-Za-z]*)")


class BasisFile(SinglefileData):
    """The class for FHI-aims one basis file stored in AiiDA DB"""

    _element = None
    _setting = None

    def __init__(self, file, element, setting, **kwargs):
        label = kwargs.pop("label", f"{element}_{setting}")
        super().__init__(file, label=label, **kwargs)
        self._element = element
        self._setting = setting

    @property
    def element(self):
        """A chemical element for which the basis file is valid"""
        if self._element is None:
            self._element = label_re.match(self.label).groups()[0]
        return self._element

    @property
    def setting(self):
        """A basis file setting (light, tight, ...)"""
        if self._setting is None:
            self._setting = label_re.match(self.label).groups()[1]
        return self._setting

    @property
    def file_name(self):
        """The default file name for the basis file"""
        return f"{chemical_symbols.index(self._element):02}_{self._element}_default"
