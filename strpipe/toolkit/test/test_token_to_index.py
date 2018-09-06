import pytest

from ..token_to_index import (
    token_to_index_with_unk,
    token_to_index_with_hash,
)


def test_token_to_index_with_unk():
    output = token_to_index_with_unk(
        token="八皇后",
        token2index={
            "八皇后": 0,
            "<UNK>": 1,
        },
    )
    assert output == 0

    output = token_to_index_with_unk(
        token="八皇后",
        token2index={
            "九皇后": 0,
            "<UNK>": 1,
        },
    )
    assert output == 1


def test_raise_keyerror_when_unk_not_in_token2index():
    with pytest.raises(KeyError):
        token_to_index_with_unk(
            token="八皇后",
            token2index={
                "八皇后": 0,
                "九皇后": 1,
                "pyladies": 2,
            },
        )


def test_token_to_index_with_hash():
    output = token_to_index_with_hash(
        token="八皇后",
        token2index={
            "八皇后": 0,
            "九皇后": 1,
            "pyladies": 2,
            "隼興": 3,
            "超": 4,
            "想去": 5,
        },
    )
    assert output == 0

    output = token_to_index_with_hash(
        token="蛋白質",
        token2index={
            "ohoh": 0,
            "九皇后": 1,
            "pyladies": 2,
            "隼興": 3,
            "超": 4,
            "想去": 5,
        },
    )
    assert output == 5
