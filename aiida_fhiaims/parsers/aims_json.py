"""
FHI-aims standard JSON parser for AiiDA
"""
import json

from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.orm import Dict
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory

AimsCalculation = CalculationFactory("fhiaims")


class AimsJSONParser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    OUTPUT_FILE_NAME = "aims.json"

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)
        # noinspection PyTypeChecker
        if not issubclass(node.process_class, AimsCalculation):
            raise exceptions.ParsingError("Can only parse AimsCalculation")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = [self.OUTPUT_FILE_NAME]
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # add output file
        self.logger.info(f"Parsing '{self.OUTPUT_FILE_NAME}'")
        with self.retrieved.open(self.OUTPUT_FILE_NAME) as handle:
            output = Dict(dict=json.load(handle))

        self.out("fhiaims.out", output)

        return ExitCode(0)
