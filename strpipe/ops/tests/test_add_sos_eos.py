import pytest

from strpipe.data.types import STRING_LIST
from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.ops.add_sos_eos import AddSosEos


def test_correctly_created():
    op = AddSosEos()
    assert op.input_type == STRING_LIST
    assert op.output_type == STRING_LIST


def test_fit_default():
    op = AddSosEos()
    input_data = [
        ['a', 'p', 'p', 'l', 'e'],
        ['b', 'a', 'n', 'a', 'n', 'a'],
        ['e', 'a', 't'],
    ]
    state = op.fit(input_data)
    assert state is None


def test_fit_raise_value_error_sos():
    op = AddSosEos()
    input_data = [
        ['a', 'p', DefaultTokens.sos, 'p', 'l', 'e'],
    ]
    with pytest.raises(ValueError):
        op.fit(input_data)


def test_fit_raise_value_error_eos():
    op = AddSosEos()
    input_data = [
        ['a', 'p', 'p', DefaultTokens.eos, 'l', 'e'],
    ]
    with pytest.raises(ValueError):
        op.fit(input_data)


def test_transform():
    op = AddSosEos()
    input_data = [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]
    state = None
    output_data, tx_info = op.transform(state, input_data)
    assert len(output_data) == len(tx_info)
    assert output_data == [
        ['<SOS>', '1', '2', '3', '<EOS>'],
        ['<SOS>', 'alvin', '喜歡', '吃', '榴槤', '<EOS>'],
        ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
    ]
    assert tx_info == [
        [True, True],
        [True, True],
        [True, True],
    ]


def test_transform_wo_sos():
    op = AddSosEos(sos_token=None)
    input_data = [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]
    state = None
    output_data, tx_info = op.transform(state, input_data)
    assert len(output_data) == len(tx_info)
    assert output_data == [
        ['1', '2', '3', '<EOS>'],
        ['alvin', '喜歡', '吃', '榴槤', '<EOS>'],
        ['隼興', '喜歡', '蛋白質', '<EOS>'],
    ]
    assert tx_info == [
        [False, True],
        [False, True],
        [False, True],
    ]


def test_transform_wo_eos():
    op = AddSosEos(eos_token=None)
    input_data = [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]
    state = None
    output_data, tx_info = op.transform(state, input_data)
    assert len(output_data) == len(tx_info)
    assert output_data == [
        ['<SOS>', '1', '2', '3'],
        ['<SOS>', 'alvin', '喜歡', '吃', '榴槤'],
        ['<SOS>', '隼興', '喜歡', '蛋白質'],
    ]
    assert tx_info == [
        [True, False],
        [True, False],
        [True, False],
    ]


def test_transform_wo_all():
    op = AddSosEos(
        sos_token=None,
        eos_token=None,
    )
    input_data = [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]
    state = None
    output_data, tx_info = op.transform(state, input_data)
    assert len(output_data) == len(tx_info)
    assert output_data == [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]
    assert tx_info == [
        [False, False],
        [False, False],
        [False, False],
    ]


def test_inverse_transform_default():
    op = AddSosEos()
    input_data = [
        ['<SOS>', '1', '2', '3', '<EOS>'],
        ['<SOS>', 'alvin', '喜歡', '吃', '榴槤', '<EOS>'],
        ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
    ]
    tx_info = [
        [True, True],
        [True, True],
        [True, True],
    ]
    output_data = op.inverse_transform(
        state=None,
        input_data=input_data,
        tx_info=tx_info,
    )
    assert output_data == [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]


def test_inverse_transform_wo_sos():
    op = AddSosEos(sos_token=None)
    input_data = [
        ['1', '2', '3', '<EOS>'],
        ['alvin', '喜歡', '吃', '榴槤', '<EOS>'],
        ['隼興', '喜歡', '蛋白質', '<EOS>'],
    ]
    tx_info = [
        [False, True],
        [False, True],
        [False, True],
    ]
    output_data = op.inverse_transform(
        state=None,
        input_data=input_data,
        tx_info=tx_info,
    )
    assert output_data == [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]


def test_inverse_transform_wo_eos():
    op = AddSosEos(eos_token=None)
    input_data = [
        ['<SOS>', '1', '2', '3'],
        ['<SOS>', 'alvin', '喜歡', '吃', '榴槤'],
        ['<SOS>', '隼興', '喜歡', '蛋白質'],
    ]
    tx_info = [
        [True, False],
        [True, False],
        [True, False],
    ]
    output_data = op.inverse_transform(
        state=None,
        input_data=input_data,
        tx_info=tx_info,
    )
    assert output_data == [
        ['1', '2', '3'],
        ['alvin', '喜歡', '吃', '榴槤'],
        ['隼興', '喜歡', '蛋白質'],
    ]


def test_inverse_transform_wo_all():
    op = AddSosEos(sos_token=None, eos_token=None)
    input_data = [
        ['<SOS>', '1', '2', '3', '<EOS>'],
        ['<SOS>', 'alvin', '喜歡', '吃', '榴槤', '<EOS>'],
        ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
    ]
    tx_info = [
        [False, False],
        [False, False],
        [False, False],
    ]
    output_data = op.inverse_transform(
        state=None,
        input_data=input_data,
        tx_info=tx_info,
    )
    assert output_data == [
        ['<SOS>', '1', '2', '3', '<EOS>'],
        ['<SOS>', 'alvin', '喜歡', '吃', '榴槤', '<EOS>'],
        ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
    ]
