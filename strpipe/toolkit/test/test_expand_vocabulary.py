from ..expand_vocabulary import expand_vocabulary


def test_expand_vocabulary():
    output = expand_vocabulary(
        token2index={
            '八皇后': 0,
            '九皇后': 1,
            'pyladies': 2,
            '隼興': 3,
            '超': 4,
            '想去': 5,
        },
        tokens=['<sos>', '九皇后', '<eos>', '<unk>', '<sos>'],
    )
    assert output == {
        '八皇后': 0,
        '九皇后': 1,
        'pyladies': 2,
        '隼興': 3,
        '超': 4,
        '想去': 5,
        '<sos>': 6,
        '<eos>': 7,
        '<unk>': 8,
    }
