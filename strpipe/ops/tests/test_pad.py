import json

import pytest

from strpipe.data.types import STRING_LIST
from strpipe.toolkit.default_tokens import DefaultTokens

from strpipe.ops.pad import Pad


def test_pad_correctly_created():
    def yield_padders():
        yield Pad()
        yield Pad(pad_token='<pad>')
        yield Pad(eos_token='<eos>')
        yield Pad(sos_token='<sos>')
        yield Pad(sos_token='<sos>', eos_token='<eos>')
    for padder in yield_padders():
        assert padder.input_type == STRING_LIST
        assert padder.output_type == STRING_LIST


@pytest.mark.parametrize('init_args,input_data,expected_maxlen', [
    (  # 1
        {},
        [
            ['a', 'p', 'p', 'l', 'e'],
            ['b', 'a', 'n', 'a', 'n', 'a'],
            ['e', 'a', 't'],
        ],
        6
    ),
    (  # 2
        {
            'sos_token': DefaultTokens.sos,
        },
        [
            ['one', 'plus', 'two']
        ],
        4
    ),
    (  # 3
        {
            'eos_token': DefaultTokens.sos,
        },
        [
            ['one', 'plus', 'two']
        ],
        4
    ),
    (  # 4
        {
            'eos_token': DefaultTokens.eos,
            'sos_token': DefaultTokens.sos
        },
        [
            ['one', 'plus', 'two']
        ],
        5
    )
])
def test_pad_fit(init_args, input_data, expected_maxlen):
    padder = Pad(**init_args)

    state = padder.fit(input_data)

    assert isinstance(state, dict)
    assert 'maxlen' in state
    assert state['maxlen'] == expected_maxlen
    assert 'pad_token' in state
    assert state['pad_token'] == init_args.get('pad_token') or DefaultTokens.pad
    if 'eos_token' in init_args:
        assert state['eos_token'] == init_args['eos_token']
    if 'sos_token' in init_args:
        assert state['sos_token'] == init_args['sos_token']
    assert json.dumps(state)  # serializable


@pytest.mark.parametrize('padder', [
    Pad(sos_token='<START_TOK>'),
    Pad(eos_token='<END_TOK>'),
    Pad(pad_token='<PADDING>'),
])
def test_pad_fit_checks_tokens_not_in_input_data(padder):
    input_data = [
        ["I'm", "ok"],
        ["<START_TOK>", "I", "already", "have", "tokens", "<END_TOK>", "<PADDING>"]
    ]
    with pytest.raises(ValueError):
        padder.fit(input_data)


@pytest.mark.parametrize('padder', [
    Pad(sos_token='<START_TOK>'),
    Pad(eos_token='<END_TOK>'),
    Pad(pad_token='<PADDING>'),
])
def test_pad_transform_checks_tokens_not_in_input_data(padder):
    input_data = [
        ["I'm", "ok"],
        ["<START_TOK>", "I", "already", "have", "tokens", "<END_TOK>", "<PADDING>"]
    ]
    state = padder.fit([
        ["1", "2"]
    ])
    with pytest.raises(ValueError):
        padder.transform(state, input_data)


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
