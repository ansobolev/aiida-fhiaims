""" Helper functions for working with input files."""
from pathlib import Path
import shutil
import tempfile

from aiida.common.exceptions import NotExistent
from aiida.orm import Code, Computer

from aiida_fhiaims.data.species_family import BasisFamily

LOCALHOST_NAME = "localhost-test"


def remove_headers(folder):
    """Removes changing header from ASE-generated files so that MD5 sums for the input files don't change
    throughout the runs
    """
    if not isinstance(folder, Path):
        folder = Path(folder)
    for f_name in ("geometry.in", "control.in"):
        with open(folder / f_name) as f:
            content = f.readlines()

        for i, line in enumerate(content):
            if not line.startswith("#"):
                with open(folder / f_name, "w") as f:
                    print("".join(content[i:]), file=f)
                break


def get_computer(name=LOCALHOST_NAME, workdir=None):
    """Get AiiDA computer.
    Loads computer 'name' from the database, if exists.
    Sets up local computer 'name', if it isn't found in the DB.

    Args:
        name: Name of computer to load or set up.
        workdir: path to work directory
            Used only when creating a new computer.

    Returns:
        :obj:`aiida.orm.computers.Computer`: The computer node
    """

    try:
        computer = Computer.objects.get(label=name)
    except NotExistent:
        if workdir is None:
            workdir = tempfile.mkdtemp()

        computer = Computer(
            label=name,
            description="localhost computer set up by aiida_diff tests",
            hostname=name,
            workdir=workdir,
            transport_type="core.local",
            scheduler_type="core.direct",
        )
        computer.store()
        computer.set_minimum_job_poll_interval(0.0)
        computer.configure()

    return computer


def get_code(entry_point, computer):
    """Get local code.
    Sets up code for given entry point on given computer.

    Args:
        entry_point: Entry point of calculation plugin
        computer: (local) AiiDA computer
    Returns:
        :obj:`aiida.orm.nodes.data.code.Code`: The code node
    """

    executable = "aims.x"
    codes = Code.objects.find(  # pylint: disable=no-member
        filters={"label": executable}
    )
    if codes:
        return codes[0]

    path = shutil.which(executable)
    code = Code(
        input_plugin_name=entry_point,
        remote_computer_exec=[computer, path],
    )
    code.label = executable
    return code.store()


def get_species_family(name, species_dir=None):
    """Gets basis family (or creates, if not existent)"""
    try:
        family = BasisFamily.collection.get(label=name)
    except NotExistent as ex:
        if species_dir is None:
            raise NotExistent(f"No family with given name '{name}' found") from ex
        family = BasisFamily.from_folder(species_dir / name, label=name)
    return family
