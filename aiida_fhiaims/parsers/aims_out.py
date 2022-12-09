"""
FHI-aims standard output parser for AiiDA
"""

from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

AimsCalculation = CalculationFactory("fhiaims")


class AimsOutParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        raise NotImplementedError
