"""Tests for aiida-fhiaims Data classes"""

import pytest

from aiida_fhiaims.data.parameters import AimsParameters


def test_parameters():
    """A test fpr AimsParameters class"""
    param_dict = {"xc": "lda"}
    with pytest.raises(ValueError):
        AimsParameters(dict=param_dict)

    param_dict.update({"species_defaults": {"family": "good"}})
    with pytest.raises(ValueError):
        AimsParameters(dict=param_dict)

    param_dict["species_defaults"].update({"setting": "light"})
    params = AimsParameters(dict=param_dict)
    params_as_dict = params.get_dict()
    assert (
        "relativistic" in params_as_dict
        and params_as_dict["relativistic"] == "atomic-zora scalar"
    )
    assert "output" in params_as_dict and "json_log" in params_as_dict["output"]
