from ..sentences_to_indices import (  # noqa
    sentence_to_indices,
    batch_sentences_to_indices,
)


def test_sentence_to_indices_default():
    output = sentence_to_indices(
        sentence=["alvin", "喜歡", "吃", "榴槤"],
        word2index={
            "<UNK>": 0,
            "喜歡": 1,
            "吃": 2,
            "榴槤": 3,
        },
    )
    assert output == [0, 1, 2, 3]


def test_sentence_to_indices_with_hash():
    output = sentence_to_indices(
        sentence=["蔣勤彥", "喜歡", "吃", "榴槤"],
        word2index={
            "喜歡": 0,
            "吃": 1,
            "榴槤": 2,
        },
        use_hash=True,
    )
    assert output == [2, 0, 1, 2]
