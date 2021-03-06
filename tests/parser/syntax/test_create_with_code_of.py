import pytest
from pytest import raises

from srilang import compiler
from srilang.exceptions import SyntaxException

fail_list = [
    """
@public
def foo():
    x: address = create_forwarder_to(0x1234567890123456789012345678901234567890, value=4, value=9)
    """
]


@pytest.mark.parametrize('bad_code', fail_list)
def test_type_mismatch_exception(bad_code):
    with raises(SyntaxException):
        compiler.compile_code(bad_code)


valid_list = [
    """
@public
def foo():
    x: address = create_forwarder_to(0x1234567890123456789012345678901234567890)
    """,
    """
@public
def foo():
    x: address = create_forwarder_to(
        0x1234567890123456789012345678901234567890,
        value=as_wei_value(9, "wei")
    )
    """,
    """
@public
def foo():
    x: address = create_forwarder_to(0x1234567890123456789012345678901234567890, value=9)
    """
]


@pytest.mark.parametrize('good_code', valid_list)
def test_rlp_success(good_code):
    assert compiler.compile_code(good_code) is not None
