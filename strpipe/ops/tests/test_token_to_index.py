from strpipe.data.types import STRING_LIST
from strpipe.toolkit.default_tokens import DefaultTokens
from strpipe.ops.token_to_index import TokenToIndex

from .state_serialization_issues import (
    serializable,
    unchange_after_serialize,
)


def test_correctly_created():
    ti_mapper = TokenToIndex()
    assert ti_mapper.input_type == STRING_LIST
    assert ti_mapper.output_type == STRING_LIST


def test_fit_wo_default_token2index():
    ti_mapper = TokenToIndex()
    input_data = [
        ['a', 'p', 'p', 'l', 'e'],
        ['b', 'a', 'n', 'a', 'n', 'a'],
        ['e', 'a', 't'],
    ]
    state = ti_mapper.fit(input_data)

    assert isinstance(state, dict)
    assert set(state.keys()) == set(['token2index', 'index2token'])
    assert set(state['token2index'].keys()) == set(
        ['a', 'p', 'l', 'e', 'b', 'n', 't', DefaultTokens.unk])
    assert set(state['token2index'].values()) == set(
        [0, 1, 2, 3, 4, 5, 6, 7])
    assert len(state['token2index']) == len(state['index2token'])
    assert set(state['token2index'].keys()) == set(
        state['index2token'].values())
    # for serialization, key should be a string not int
    assert set(state['token2index'].values()) == set(
        [int(i) for i in state['index2token'].keys()])
    serializable(state)
    unchange_after_serialize(state)


def test_fit_with_default_token2index():
    unk_token = DefaultTokens.unk
    ti_mapper = TokenToIndex(
        token2index={
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
        },
        vocab_size=3,
    )
    input_data = [
        ['a', 'p', 'p', 'l', 'e'],
        ['b', 'a', 'n', 'a', 'n', 'a'],
        ['e', 'a', 't'],
    ]
    state = ti_mapper.fit(input_data)
    # vocab_size would not work when token2index is provided.
    assert state['token2index'] == {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, unk_token: 6,
    }
    serializable(state)
    unchange_after_serialize(state)


def test_transform():
    ti_mapper = TokenToIndex()
    unk_token = DefaultTokens.unk

    output_data, tx_info = ti_mapper.transform(
        state={
            'token2index': {
                unk_token: 0,
                "喜歡": 1,
                "吃": 2,
                "榴槤": 3,
            },
        },
        input_data=[
            ["alvin", "喜歡", "吃", "榴槤"],
            ["隼興", "喜歡", "蛋白質"],
        ],
    )
    assert len(output_data) == len(tx_info)
    assert output_data == [
        [0, 1, 2, 3],
        [0, 1, 0],
    ]
    assert tx_info == [
        {0: "alvin"},
        {0: "隼興", 2: "蛋白質"},
    ]


def test_inverse_transform():
    ti_mapper = TokenToIndex()
    unk_token = DefaultTokens.unk
    output_data = ti_mapper.inverse_transform(
        state={
            'index2token': {
                '0': unk_token,
                '1': "喜歡",
                '2': "吃",
                '3': "榴槤",
            },
        },  # for serialization, key should be a string not int
        input_data=[
            [0, 1, 2, 3],
            [0, 1, 0],
        ],
        tx_info=[
            {0: "alvin"},
            {0: "隼興", 2: "蛋白質"},
        ],
    )
    assert len(output_data) == 2
    assert output_data == [
        ["alvin", "喜歡", "吃", "榴槤"],
        ["隼興", "喜歡", "蛋白質"],
    ]
