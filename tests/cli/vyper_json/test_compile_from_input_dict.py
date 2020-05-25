#!/usr/bin/env python3

from copy import deepcopy

import pytest

import srilang
from srilang.cli.srilang_json import (
    TRANSLATE_MAP,
    compile_from_input_dict,
    exc_handler_raises,
    exc_handler_to_dict,
)
from srilang.exceptions import JSONError, SyntaxException, TypeMismatch

FOO_CODE = """
import contracts.bar as Bar

@public
def foo(a: address) -> bool:
    return Bar(a).bar(1)

@public
def baz() -> uint256:
    return self.balance
"""

BAR_CODE = """
@public
def bar(a: uint256) -> bool:
    return True
"""

BAD_SYNTAX_CODE = """
def bar()>:
"""

BAD_COMPILER_CODE = """
@public
def oopsie(a: uint256) -> bool:
    return 42
"""

BAR_ABI = [{
    'name': 'bar',
    'outputs': [{'type': 'bool', 'name': 'out'}],
    'inputs': [{'type': 'uint256', 'name': 'a'}],
    'constant': False,
    'payable': False,
    'type': 'function',
    'gas': 313
}]

INPUT_JSON = {
    'language': "srilang",
    'sources': {
        'contracts/foo.sri': {'content': FOO_CODE},
        'contracts/bar.sri': {'content': BAR_CODE},
    },
    'interfaces': {
        'contracts/bar.json': {'abi': BAR_ABI}
    },
    'settings': {
        'outputSelection': {'*': ["*"]}
    }

}


def test_root_folder_not_exists():
    with pytest.raises(FileNotFoundError):
        compile_from_input_dict({}, root_folder="/path/that/does/not/exist")


def test_wrong_language():
    with pytest.raises(JSONError):
        compile_from_input_dict({'language': "Solidity"})


def test_exc_handler_raises_syntax():
    input_json = deepcopy(INPUT_JSON)
    input_json['sources']['badcode.sri'] = {'content': BAD_SYNTAX_CODE}
    with pytest.raises(SyntaxException):
        compile_from_input_dict(input_json, exc_handler_raises)


def test_exc_handler_to_dict_syntax():
    input_json = deepcopy(INPUT_JSON)
    input_json['sources']['badcode.sri'] = {'content': BAD_SYNTAX_CODE}
    result, _ = compile_from_input_dict(input_json, exc_handler_to_dict)
    assert 'errors' in result
    assert len(result['errors']) == 1
    error = result['errors'][0]
    assert error['component'] == "parser"
    assert error['type'] == "SyntaxException"


def test_exc_handler_raises_compiler():
    input_json = deepcopy(INPUT_JSON)
    input_json['sources']['badcode.sri'] = {'content': BAD_COMPILER_CODE}
    with pytest.raises(TypeMismatch):
        compile_from_input_dict(input_json, exc_handler_raises)


def test_exc_handler_to_dict_compiler():
    input_json = deepcopy(INPUT_JSON)
    input_json['sources']['badcode.sri'] = {'content': BAD_COMPILER_CODE}
    result, _ = compile_from_input_dict(input_json, exc_handler_to_dict)
    assert sorted(result.keys()) == ['compiler', 'errors']
    assert result['compiler'] == f"srilang-{srilang.__version__}"
    assert len(result['errors']) == 1
    error = result['errors'][0]
    assert error['component'] == "compiler"
    assert error['type'] == "TypeMismatch"


def test_source_ids_increment():
    input_json = deepcopy(INPUT_JSON)
    input_json['settings']['outputSelection'] = {'*': ['evm.deployedBytecode.sourceMap']}
    result, _ = compile_from_input_dict(input_json)
    assert result['contracts/bar.sri']['source_map']['pc_pos_map_compressed'].startswith('-1:-1:0')
    assert result['contracts/foo.sri']['source_map']['pc_pos_map_compressed'].startswith('-1:-1:1')


def test_outputs():
    result, _ = compile_from_input_dict(INPUT_JSON)
    assert sorted(result.keys()) == ['contracts/bar.sri', 'contracts/foo.sri']
    assert sorted(result['contracts/bar.sri'].keys()) == sorted(TRANSLATE_MAP.values())


def test_relative_import_paths():
    input_json = deepcopy(INPUT_JSON)
    input_json['sources']['contracts/potato/baz/baz.sri'] = {'content': """from ... import foo"""}
    input_json['sources']['contracts/potato/baz/potato.sri'] = {'content': """from . import baz"""}
    input_json['sources']['contracts/potato/footato.sri'] = {'content': """from baz import baz"""}
    compile_from_input_dict(input_json)


def test_evm_version():
    # should compile differently because of SELFBALANCE
    input_json = deepcopy(INPUT_JSON)
    input_json['settings']['evmVersion'] = "byzantium"
    compiled = compile_from_input_dict(input_json)
    input_json['settings']['evmVersion'] = "istanbul"
    assert compiled != compile_from_input_dict(input_json)