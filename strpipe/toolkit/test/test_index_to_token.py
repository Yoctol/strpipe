from ..index_to_token import batch_indices_to_tokens


def test_index_to_token():
    output = batch_indices_to_tokens(
        indices=[[0, 1, 2], [3, 1, 1, 2]],
        index2word={
            0: '<SOS>',
            1: 'gb',
            2: '去',
            3: '重訓',
        },
    )
    assert output == [
        ['<SOS>', 'gb', '去'],
        ['重訓', 'gb', 'gb', '去'],
    ]
