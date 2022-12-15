"""
Command line interface for dealing with FHI-aims' `species_defaults` basis sets
"""
from pathlib import Path
import sys

import click

from aiida.cmdline.commands.cmd_data import verdi_data
from aiida.cmdline.utils import decorators, echo
from aiida.orm import QueryBuilder
from aiida.plugins import GroupFactory

from aiida_fhiaims.data.species_family import BasisFamily

# from aiida.cmdline.params.types import DataParamType

AimsBasisFamily = GroupFactory("fhiaims.species_family")


@verdi_data.group("species-defaults")
def species_defaults():
    """Command line interface for FHIAims species_defaults"""


@species_defaults.command("install")
@click.argument("path", type=click.Path(exists=True), envvar="AIMS_SPECIES_DIR")
@decorators.with_dbenv()
def install(path):
    """Installs a set of `species_defaults` FHI-aims basis families (light, tight, really_tight...) from a given PATH.
    Defaults to the value of AIMS_SPECIES_DIR environmental variable.
    """
    path = Path(path)
    echo.echo(f"Trying to install basis families from {path.absolute()}... ", nl=False)
    dirs = [f for f in path.iterdir() if f.is_dir()]
    families = []
    for d in dirs:
        try:
            families.append(BasisFamily.from_folder(d, d.name))
        except FileNotFoundError:
            echo.echo_critical(" [FAILED]")
    echo.echo_success(" [OK]")
    family_data = [(f.label, f.pk) for f in families]
    echo.echo(
        f'Installed families: {", ".join([f"{label}<pk={pk}>" for (label, pk) in family_data])}'
    )


@species_defaults.command("list")
@decorators.with_dbenv()
def list_():  # pylint: disable=redefined-builtin
    """
    Display all AIMS basis families
    """
    qb = QueryBuilder()
    qb.append(AimsBasisFamily)
    results = qb.all()

    s = ""
    for result in results:
        obj = result[0]
        s += f"{str(obj)}, pk: {obj.pk}\n"
    sys.stdout.write(s)
