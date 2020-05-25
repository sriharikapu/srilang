#!/usr/bin/env python3

import json
from copy import deepcopy

import pytest

from srilang.cli.srilang_json import _parse_args
from srilang.exceptions import JSONError

FOO_CODE = """
import contracts.bar as Bar

@public
def foo(a: address) -> bool:
    return Bar(a).bar(1)
"""

BAR_CODE = """
@public
def bar(a: uint256) -> bool:
    return True
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


def test_to_stdout(tmp_path, capfd):
    path = tmp_path.joinpath('input.json')
    with path.open('w') as fp:
        json.dump(INPUT_JSON, fp)
    _parse_args([path.absolute().as_posix()])
    out, _ = capfd.readouterr()
    output_json = json.loads(out)
    assert 'errors' not in output_json
    assert 'contracts/foo.sri' in output_json['sources']
    assert 'contracts/bar.sri' in output_json['sources']


def test_to_file(tmp_path):
    path = tmp_path.joinpath('input.json')
    with path.open('w') as fp:
        json.dump(INPUT_JSON, fp)
    output_path = tmp_path.joinpath('output.json')
    _parse_args([path.absolute().as_posix(), '-o', output_path.absolute().as_posix()])
    assert output_path.exists()
    with output_path.open() as fp:
        output_json = json.load(fp)
    assert 'errors' not in output_json
    assert 'contracts/foo.sri' in output_json['sources']
    assert 'contracts/bar.sri' in output_json['sources']


def test_pretty_json(tmp_path, capfd):
    path = tmp_path.joinpath('input.json')
    with path.open('w') as fp:
        json.dump(INPUT_JSON, fp)
    _parse_args([path.absolute().as_posix()])
    out1, _ = capfd.readouterr()
    _parse_args([path.absolute().as_posix(), '--pretty-json'])
    out2, _ = capfd.readouterr()
    assert len(out2) > len(out1)
    assert json.loads(out1) == json.loads(out2)


def test_traceback(tmp_path, capfd):
    path = tmp_path.joinpath('input.json')
    input_json = deepcopy(INPUT_JSON)
    del input_json['sources']
    with path.open('w') as fp:
        json.dump(input_json, fp)
    _parse_args([path.absolute().as_posix()])
    out, _ = capfd.readouterr()
    output_json = json.loads(out)
    assert 'errors' in output_json
    with pytest.raises(JSONError):
        _parse_args([path.absolute().as_posix(), '--traceback'])