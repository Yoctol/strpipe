from ..build_vocabulary import build_vocabulary_from_sentences


def test_build_vocabulary_from_empty():
    empty_output = build_vocabulary_from_sentences([])
    assert set(empty_output.keys()) == set(
        ['<SOS>', '<EOS>', '<PAD>', '<UNK>'])
    assert set(empty_output.values()) == set([0, 1, 2, 3])


def test_build_vocabulary_with_same_tokens():
    output = build_vocabulary_from_sentences(
        [],
        sos_token='<SOS>',
        eos_token='<EOS>',
        unk_token='<EOS>',
        pad_token='<PAD>',
    )
    assert set(output.keys()) == set(
        ['<SOS>', '<EOS>', '<PAD>'])
    assert set(output.values()) == set([0, 1, 2])


def test_build_vocabulary_from_sentences():
    output = build_vocabulary_from_sentences(
        [
            ['隼興', '喜歡', '蛋白質'],
            ['蛋白質'],
        ],
    )
    assert set(output.keys()) == set(
        ['<SOS>', '<EOS>', '<PAD>',
         '<UNK>', '隼興', '喜歡', '蛋白質'],
    )
    assert set(output.values()) == set(
        list(range(7)),
    )


def test_build_vocabulary_from_sentences_with_limit_size():
    output = build_vocabulary_from_sentences(
        [
            ['隼興', '喜歡', '蛋白質'],
            ['蛋白質'],
        ],
        vocab_size=5,
    )
    assert set(output.keys()) == set(
        ['<SOS>', '<EOS>', '<PAD>',
         '<UNK>', '蛋白質'],
    )
    assert set(output.values()) == set(
        list(range(5)),
    )


def test_build_vocabulary_from_sentences_with_conflict():
    output = build_vocabulary_from_sentences(
        [
            ['<SOS>', '喜歡', '蛋白質', '<EOS>'],
            ['蛋白質'],
        ],
    )
    assert set(output.keys()) == set(
        ['<SOS>', '<EOS>', '<PAD>',
         '<UNK>', '喜歡', '蛋白質'],
    )
    assert set(output.values()) == set(
        list(range(6)),
    )
