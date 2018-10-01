import pytest

from strpipe.data.types import STRING_LIST
from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.ops.pad import Pad

from .state_serialization_issues import (
    serializable,
    unchange_after_serialize,
)


def test_pad_correctly_created():
    def yield_padders():
        yield Pad()
        yield Pad(pad_token='<pad>')
    for padder in yield_padders():
        assert padder.input_type == STRING_LIST
        assert padder.output_type == STRING_LIST


def test_fit():
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
    serializable(state)
    unchange_after_serialize(state)


def test_fit_raise_error_pad():
    padder = Pad()

    input_data = [
        [DefaultTokens.pad, 'a', 'p', 'p', 'l', 'e'],
    ]
    with pytest.raises(ValueError):
        padder.fit(input_data)


def test_pad_transform():
    pto = '<pad>'
    padder = Pad(pad_token=pto)
    state = {
        'maxlen': 7,
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


def test_inverse_transform():
    pto = '<pad>'
    padder = Pad(pad_token=pto)
    state = {
        'maxlen': 7,
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
    serializable(state)
    unchange_after_serialize(state)
