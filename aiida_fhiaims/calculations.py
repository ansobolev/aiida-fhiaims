"""
Calculations provided by aiida_fhiaims.
"""
from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import Dict, StructureData


class AimsCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the aims.x executable.
    """

    _OUTPUT_FILE_NAME = "aims.out"
    _RETRIEVE_LIST = ["aims.json", _OUTPUT_FILE_NAME]

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 2,
        }
        spec.inputs["metadata"]["options"]["parser_name"].default = "fhiaims"

        # new ports
        spec.input(
            "metadata.options.output_filename",
            valid_type=str,
            default=cls._OUTPUT_FILE_NAME,
        )
        spec.input(
            "parameters",
            valid_type=Dict,
            help="FHI-aims parameters dictionary",
        )
        spec.input(
            "structure",
            valid_type=StructureData,
            help="Atomic structure to be calculated",
        )
        spec.output(
            "fhiaims.out",
            valid_type=Dict,
            help="Output values of AIMS calculation",
        )

        spec.exit_code(
            300,
            "ERROR_MISSING_OUTPUT_FILES",
            message="Calculation did not produce all expected output files.",
        )

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param aiida.common.folders.Folder folder: an `aiida.common.folders.Folder` where the plugin should temporarily
            place all files needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        code_info = datastructures.CodeInfo()
        code_info.cmdline_params = self.inputs.parameters.cmdline_params(
            file1_name=self.inputs.file1.filename, file2_name=self.inputs.file2.filename
        )
        code_info.code_uuid = self.inputs.code.uuid
        code_info.stdout_name = self.metadata.options.output_filename
        code_info.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calc_info = datastructures.CalcInfo()
        calc_info.codes_info = [code_info]
        calc_info.local_copy_list = [
            (
                self.inputs.file1.uuid,
                self.inputs.file1.filename,
                self.inputs.file1.filename,
            ),
            (
                self.inputs.file2.uuid,
                self.inputs.file2.filename,
                self.inputs.file2.filename,
            ),
        ]
        calc_info.retrieve_list = self._RETRIEVE_LIST

        return calc_info
