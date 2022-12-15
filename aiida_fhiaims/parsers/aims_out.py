"""
FHI-aims standard output parser for AiiDA
"""
from aiida.common import exceptions
from aiida.engine import ExitCode
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

        Checks that the ProcessNode being passed was produced by a AimsCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)
        # noinspection PyTypeChecker
        if not issubclass(node.process_class, AimsCalculation):
            raise exceptions.ParsingError("Can only parse AimsCalculation")
        self.OUTPUT_FILE_NAME = self.node.base.attributes.get("output_filename")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        return ExitCode(0)
