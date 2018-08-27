from ..token_to_index import token_to_index_with_unk


def test_token_to_index_with_unk():
    output = token_to_index_with_unk(
        token="八皇后",
        word2index={
            "八皇后": 0,
            "<UNK>": 1,
        },
    )
    assert output == 0

    output = token_to_index_with_unk(
        token="八皇后",
        word2index={
            "九皇后": 0,
            "<UNK>": 1,
        },
    )
    assert output == 1
