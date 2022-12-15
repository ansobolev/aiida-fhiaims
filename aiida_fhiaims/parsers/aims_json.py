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

        # add output node
        self.logger.info(f"Parsing '{self.OUTPUT_FILE_NAME}'")
        with self.retrieved.open(self.OUTPUT_FILE_NAME) as handle:
            output_data = json.load(handle)
        # group similar records from json into Dict records
        record_types = [r["record_type"] for r in output_data]
        result = {}
        for r_type in set(record_types):
            records = [r for r in output_data if r["record_type"] == r_type]
            if len(records) == 1:
                result[r_type] = records[0]
            else:
                result[r_type] = records

        self.out("fhiaims.out", Dict(result))
        return ExitCode(0)
