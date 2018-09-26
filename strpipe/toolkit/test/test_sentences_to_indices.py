from ..sentences_to_indices import (
    sentences_to_indices_with_unk,
    sentences_to_indices_with_hash,
    indices_to_sentences,
)


def test_sentences_to_indices_with_unk():
    output = sentences_to_indices_with_unk(
        sentences=[
            ["alvin", "喜歡", "吃", "榴槤"],
            ["隼興", "喜歡", "蛋白質"],
        ],
        token2index={
            "<UNK>": 0,
            "喜歡": 1,
            "吃": 2,
            "榴槤": 3,
        },
    )
    assert output[0] == [
        [0, 1, 2, 3],
        [0, 1, 0],
    ]
    assert output[1] == [
        {0: "alvin"},
        {0: "隼興", 2: "蛋白質"},
    ]


def test_indices_to_sentences():
    output = indices_to_sentences(
        indices=[
            [0, 1, 2, 3],
            [0, 1, 0],
        ],
        index2token={
            '0': "<UNK>",
            '1': "喜歡",
            '2': "吃",
            '3': "榴槤",
        },  # for serialization, key should be a string not int
        meta=[
            {0: "alvin"},
            {0: "隼興", 2: "蛋白質"},
        ]
    )
    assert output == [
        ["alvin", "喜歡", "吃", "榴槤"],
        ["隼興", "喜歡", "蛋白質"],
    ]


def test_sentence_to_indices_with_hash():
    output = sentences_to_indices_with_hash(
        sentences=[
            ["蔣勤彥", "喜歡", "吃", "榴槤"],
            ["薄餡", "喜歡", "吃", "小泡芙"],
        ],
        token2index={
            "喜歡": 0,
            "吃": 1,
            "榴槤": 2,
        },
    )
    assert output[0] == [
        [2, 0, 1, 2],
        [1, 0, 1, 0],
    ]
    assert output[1] == [
        {0: "蔣勤彥"},
        {0: "薄餡", 3: "小泡芙"},
    ]


def test_indices_to_sentences_wo_unk():
    output = indices_to_sentences(
        indices=[
            [0, 0, 1, 2],
            [0, 0, 1, 0],
        ],
        index2token={
            '0': "喜歡",
            '1': "吃",
            '2': "榴槤",
        },  # for serialization, key should be a string not int
        meta=[
            {0: "蔣勤彥"},
            {0: "薄餡", 3: "小泡芙"},
        ],
    )
    assert output == [
        ["蔣勤彥", "喜歡", "吃", "榴槤"],
        ["薄餡", "喜歡", "吃", "小泡芙"],
    ]
