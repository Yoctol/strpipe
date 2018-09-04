import json

from strpipe.data.types import STRING_LIST
from strpipe.toolkit.default_tokens import DefaultTokens

from strpipe.ops.pad import Pad


def test_pad_correctly_created():
    padder = Pad()
    assert padder.input_type == STRING_LIST
    assert padder.output_type == STRING_LIST


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
    assert json.dumps(state)  # serialzable


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
