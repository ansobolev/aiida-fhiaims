""" Helper functions for working with input files."""
from pathlib import Path


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
