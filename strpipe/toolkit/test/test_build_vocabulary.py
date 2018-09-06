from ..build_vocabulary import build_vocabulary_from_sentences


def test_build_vocabulary_from_sentences():
    output = build_vocabulary_from_sentences(
        [
            ['隼興', '喜歡', '蛋白質'],
            ['蛋白質'],
        ],
    )
    assert set(output.keys()) == set(
        ['隼興', '喜歡', '蛋白質'],
    )
    assert set(output.values()) == set(
        list(range(3)),
    )


def test_build_vocabulary_from_sentences_with_limit_size():
    output = build_vocabulary_from_sentences(
        [
            ['隼興', '喜歡', '蛋白質'],
            ['蛋白質'],
            ['gb', '的', '下午茶', '是', '香蕉',
             '和', '茶葉蛋'],
            ['香蕉', '是', '澱粉'],
            ['茶葉蛋', '是', '蛋白質'],
        ],
        vocab_size=4,
    )
    assert set(output.keys()) == set(
        ['蛋白質', '是', '茶葉蛋', '香蕉'],
    )
    assert set(output.values()) == set(
        list(range(4)),
    )
