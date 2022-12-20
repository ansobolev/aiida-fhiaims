"""
Calculations provided by aiida_fhiaims.
"""
from pathlib import Path
from tempfile import TemporaryDirectory

from ase.calculators.aims import Aims

from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import Dict, StructureData

from aiida_fhiaims.data.parameters import AimsParameters
from aiida_fhiaims.data.species_family import BasisFamily
from aiida_fhiaims.helpers import remove_headers


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
        spec.inputs["metadata"]["options"]["withmpi"].default = True
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 2,
        }
        spec.inputs["metadata"]["options"]["parser_name"].default = "fhiaims.json"
        # new ports
        spec.input(
            "metadata.options.output_filename",
            valid_type=str,
            default=cls._OUTPUT_FILE_NAME,
        )
        spec.input(
            "parameters",
            valid_type=AimsParameters,
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
        # prepare input objects
        ase_struct = self.inputs.structure.get_ase()
        control_params = self.inputs.parameters.get_dict()
        # prepare input files
        basis_family = control_params.pop("species_defaults")
        bases = BasisFamily.get(label=basis_family["family"]).get_species_defaults(
            setting=basis_family["setting"], structure=self.inputs.structure
        )
        with TemporaryDirectory() as species_dir:
            for basis_file in bases.values():
                with open(Path(species_dir) / basis_file.filename, mode="w") as f:
                    print(basis_file.get_content(), file=f)
            control_params["species_dir"] = species_dir
            aims_calc = Aims(**control_params)
            ase_struct.set_calculator(aims_calc)
            aims_calc.directory = folder.abspath
            aims_calc.write_input(ase_struct)
            # the following is deleting all the time-specific info from inputs
            remove_headers(folder.abspath)
            (Path(folder.abspath) / "parameters.ase").unlink(missing_ok=True)

        code_info = datastructures.CodeInfo()
        code_info.code_uuid = self.inputs.code.uuid
        code_info.stdout_name = self.metadata.options.output_filename
        code_info.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calc_info = datastructures.CalcInfo()
        calc_info.codes_info = [code_info]
        calc_info.local_copy_list = []
        calc_info.retrieve_list = self._RETRIEVE_LIST

        return calc_info
