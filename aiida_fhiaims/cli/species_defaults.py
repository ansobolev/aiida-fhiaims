"""
Command line interface for dealing with FHI-aims' `species_defaults` basis sets
"""
import sys

from aiida.cmdline.commands.cmd_data import verdi_data
from aiida.cmdline.utils import decorators
from aiida.orm import QueryBuilder
from aiida.plugins import GroupFactory

# from aiida.cmdline.params.types import DataParamType

AimsBasisFamily = GroupFactory("fhiaims.species_family")


@verdi_data.group("species-defaults")
def species_defaults():
    """Command line interface for FHIAims species_defaults"""


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


# @species_default_cli.command("export")
# @click.argument("node", metavar="IDENTIFIER", type=DataParamType())
# @click.option(
#     "--outfile",
#     "-o",
#     type=click.Path(dir_okay=False),
#     help="Write output to file (default: print to stdout).",
# )
# @decorators.with_dbenv()
# def export(node, outfile):
#     """Export an AimsParameters node (identified by PK, UUID or label) to plain text."""
#     string = str(node)
#
#     if outfile:
#         with open(outfile, "w") as f:
#             f.write(string)
#     else:
#         click.echo(string)
