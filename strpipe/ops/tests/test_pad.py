import json

import pytest

from strpipe.data.types import STRING_LIST
from strpipe.toolkit.default_tokens import DefaultTokens

from strpipe.ops.pad import Pad


def test_pad_correctly_created():
    def yield_padders():
        yield Pad()
        yield Pad(pad_token='<pad>')
        yield Pad(sos_token='<sos>', eos_token='<eos>')
    for padder in yield_padders():
        assert padder.input_type == STRING_LIST
        assert padder.output_type == STRING_LIST


def test_pad_init_needs_both_sos_and_eos_or_neither():
    with pytest.raises(ValueError):
        Pad(sos_token='<sos>')
    with pytest.raises(ValueError):
        Pad(eos_token='<eos>')


def test_pad_passing_state_needs_both_sos_and_eos_or_neither():
    padder = Pad()
    input_data = [
        [],
    ]
    output_data = [
        [DefaultTokens.pad],
    ]
    tx_info = [
        {'sentlen': 0, 'sentence_tail': []},
    ]

    state1 = {'maxlen': 0, 'pad_token': '<PAD>'}
    state2 = {'maxlen': 2, 'pad_token': '<PAD>', 'sos_token': '<sos>', 'eos_token': '<eos>'}
    state3 = {'maxlen': 2, 'pad_token': '<PAD>', 'sos_token': '<sos>'}
    state4 = {'maxlen': 2, 'pad_token': '<PAD>', 'eos_token': '<eos>'}
 

    output_data1, _ = padder.transform(state1, input_data)
    output_data2, _ = padder.transform(state2, input_data)
    with pytest.raises(ValueError):
        padder.transform(state3, input_data)
    with pytest.raises(ValueError):
        padder.transform(state4, input_data)

    padder.inverse_transform(state1, output_data1, tx_info)
    padder.inverse_transform(state2, output_data2, tx_info)
    with pytest.raises(ValueError):
        padder.inverse_transform(state3, output_data1, tx_info)
    with pytest.raises(ValueError):
        padder.inverse_transform(state4, output_data2, tx_info)


def test_pad_fit():
    padder = Pad()

    input_data = [
        ['a', 'p', 'p', 'l', 'e'],
        ['b', 'a', 'n', 'a', 'n', 'a'],
        ['e', 'a', 't'],
    ]

    state = padder.fit(input_data)

    assert isinstance(state, dict)
    assert 'maxlen' in state
    assert state['maxlen'] == 6
    assert 'pad_token' in state
    assert state['pad_token'] == DefaultTokens.pad
    assert json.dumps(state)  # serializable


def test_pad_fit_with_sos_and_eos():
    padder = Pad(sos_token=DefaultTokens.sos, eos_token=DefaultTokens.eos)

    input_data = [
        ['a', 'p', 'p', 'l', 'e'],
        ['b', 'a', 'n', 'a', 'n', 'a'],
        ['e', 'a', 't'],
    ]

    state = padder.fit(input_data)

    assert isinstance(state, dict)
    assert 'maxlen' in state
    assert state['maxlen'] == 6 + 2
    assert 'pad_token' in state
    assert state['pad_token'] == DefaultTokens.pad
    assert 'sos_token' in state
    assert state['sos_token'] == DefaultTokens.sos
    assert 'eos_token' in state
    assert state['eos_token'] == DefaultTokens.eos
    assert json.dumps(state)  # serializable


def test_pad_transform():
    padder = Pad()
    pto = '<pad>'
    state = {
        'maxlen': 7,
        'pad_token': pto,
    }

    input_data = [
        ['h', 'a', 'p', 'p', 'y'],  # shorter
        ['h', 'a', 'p', 'p', 'i', 'n', 'e', 's', 's'],  # longer
        ['h', 'a', 'p', 'p', 'i', 'l', 'y'],  # same length
    ]

    expected_output = [
        ['h', 'a', 'p', 'p', 'y', pto, pto],
        ['h', 'a', 'p', 'p', 'i', 'n', 'e'],
        ['h', 'a', 'p', 'p', 'i', 'l', 'y'],
    ]

    output_data, tx_info = padder.transform(state, input_data)
    assert output_data == expected_output
    assert len(tx_info) == len(output_data)
    sentlens = [t['sentlen'] for t in tx_info]
    sentence_tail = [t['sentence_tail'] for t in tx_info]
    assert sentlens == [5, 9, 7]
    assert sentence_tail == [[], ['s', 's'], []]


def test_pad_transform_with_sos_and_eos():
    padder = Pad()
    sto = '<YO>'
    pto = '<pad>'
    eto = '<BYE>'
    state = {
        'maxlen': 9,
        'pad_token': pto,
        'sos_token': sto,
        'eos_token': eto,

    }

    input_data = [
        ['h', 'a', 'p', 'p', 'y'],  # shorter
        ['h', 'a', 'p', 'p', 'i', 'n', 'e', 's', 's'],  # longer
        ['h', 'a', 'p', 'p', 'i', 'l', 'y'],  # same length
    ]

    expected_output = [
        [sto, 'h', 'a', 'p', 'p', 'y', eto, pto, pto],
        [sto, 'h', 'a', 'p', 'p', 'i', 'n', 'e', eto],
        [sto, 'h', 'a', 'p', 'p', 'i', 'l', 'y', eto],
    ]

    output_data, tx_info = padder.transform(state, input_data)
    assert output_data == expected_output
    assert len(tx_info) == len(output_data)
    sentlens = [t['sentlen'] for t in tx_info]
    sentence_tail = [t['sentence_tail'] for t in tx_info]
    assert sentlens == [5, 9, 7]
    assert sentence_tail == [[], ['s', 's'], []]


def test_pad_inverse_transform():
    padder = Pad()
    pto = '<pad>'
    state = {
        'maxlen': 7,
        'pad_token': pto,
    }

    output_data = [
        ['h', 'a', 'p', 'p', 'y', '<pad>', '<pad>'],
        ['h', 'a', 'p', 'p', 'i', 'n', 'e'],
        ['h', 'a', 'p', 'p', 'i', 'l', 'y'],
    ]
    tx_info = [
        {'sentlen': 5, 'sentence_tail': []},
        {'sentlen': 9, 'sentence_tail': ['s', 's']},
        {'sentlen': 7, 'sentence_tail': []},
    ]

    expected_tx_data = [
        ['h', 'a', 'p', 'p', 'y'],  # shorter
        ['h', 'a', 'p', 'p', 'i', 'n', 'e', 's', 's'],  # longer
        ['h', 'a', 'p', 'p', 'i', 'l', 'y'],  # same length
    ]
    tx_data = padder.inverse_transform(state, output_data, tx_info)
    assert tx_data == expected_tx_data


def test_pad_inverse_transform_with_sos_and_eos():
    padder = Pad()
    sto = '<YO>'
    pto = '<pad>'
    eto = '<BYE>'
    state = {
        'maxlen': 7,
        'pad_token': pto,
    }

    output_data = [
        [sto, 'h', 'a', 'p', 'p', 'y', eto, pto, pto],
        [sto, 'h', 'a', 'p', 'p', 'i', 'n', 'e', eto],
        [sto, 'h', 'a', 'p', 'p', 'i', 'l', 'y', eto],
    ]

    tx_info = [
        {'sentlen': 5, 'sentence_tail': []},
        {'sentlen': 9, 'sentence_tail': ['s', 's']},
        {'sentlen': 7, 'sentence_tail': []},
    ]

    expected_tx_data = [
        ['h', 'a', 'p', 'p', 'y'],  # shorter
        ['h', 'a', 'p', 'p', 'i', 'n', 'e', 's', 's'],  # longer
        ['h', 'a', 'p', 'p', 'i', 'l', 'y'],  # same length
    ]
    tx_data = padder.inverse_transform(state, output_data, tx_info)
    assert tx_data == expected_tx_data


def test_pad_with_custom_kwargs_fit():
    expected_other_token = 'other_token'
    expected_maxlen = 5

    padder = Pad(
        pad_token=expected_other_token,
        maxlen=expected_maxlen,
    )

    input_data = [
        ['a', 'p', 'p', 'l', 'e'],
        ['b', 'a', 'n', 'a', 'n', 'a'],
        ['e', 'a', 't']
    ]

    state = padder.fit(input_data)

    assert state['maxlen'] == expected_maxlen
    assert state['pad_token'] == expected_other_token
    assert json.dumps(state)  # serialzable
