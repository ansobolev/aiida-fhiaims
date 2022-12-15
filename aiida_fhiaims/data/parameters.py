"""A module defining the class for storing FHI-aims parameters"""

from aiida.orm import Dict

__all__ = ("AimsParameters",)


class AimsParameters(Dict):
    """The class for storing FHI-aims parameters. Is subclassed from Dict in order to facilitate storing and caching
    several default parameters.
    """

    def __init__(self, *, relativistic=True, json=True, **kwargs):
        value = kwargs.pop("value", None) or kwargs.pop("dict")

        if "species_defaults" not in value or any(
            x not in value["species_defaults"] for x in ("family", "setting")
        ):
            raise ValueError(
                "No or incomplete species_defaults found in AimsParameters"
            )

        if relativistic and "relativistic" not in value:
            value["relativistic"] = "atomic_zora scalar"
        if "output" in value:
            value["output"] = set(value["output"])
        else:
            value["output"] = set()
        if json:
            value["output"].add("json_log")
        super().__init__(value=value, **kwargs)
