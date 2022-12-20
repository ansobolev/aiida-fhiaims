"""Tests for helpers module"""


from aiida_fhiaims.helpers import get_code, get_computer


def test_computer():
    """Test getting `localhost` computer helper"""
    computer = get_computer()
    assert computer.hostname == "localhost-test"
    assert computer.transport_type == "core.local"


def test_code():
    """Test getting `Code` endpoint"""
    computer = get_computer()
    code = get_code("fhiaims", computer, executable="diff")
    assert code.label == "aims.x"
