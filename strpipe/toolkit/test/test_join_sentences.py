from ..join_sentences import join_sentences, split_strs


def test_join_sentences_default():
    output = join_sentences(
        sentences=[
            ['隼興', '是', '女性', '之', '友'],
            ['這是', '男性', '的', '凝視'],
            ['男朋友', '餐盒', '是', '父權', '便當'],
        ],
    )
    assert output[0] == [
        '隼興是女性之友',
        '這是男性的凝視',
        '男朋友餐盒是父權便當',
    ]
    assert output[1] == [
        [2, 3, 5, 6],
        [2, 4, 5],
        [3, 5, 6, 8],
    ]


def test_join_sentences_with_special_token():
    special_token = '隼興'
    output = join_sentences(
        sentences=[
            ['隼興', '是', '女性', '之', '友'],
            ['這是', '男性', '的', '凝視'],
            ['男朋友', '餐盒', '是', '父權', '便當'],
        ],
        by_=special_token,
    )
    assert output[0] == [
        '隼興隼興是隼興女性隼興之隼興友',
        '這是隼興男性隼興的隼興凝視',
        '男朋友隼興餐盒隼興是隼興父權隼興便當',
    ]
    assert output[1] == [
        [2, 5, 9, 12],
        [2, 6, 9],
        [3, 7, 10, 14],
    ]


def test_split_strs_default():
    output = split_strs(
        input_strs=[
            '隼興是女性之友',
            '這是男性的凝視',
            '男朋友餐盒是父權便當',
        ],
        meta=[
            [2, 3, 5, 6],
            [2, 4, 5],
            [3, 5, 6, 8],
        ]
    )
    assert output == [
        ['隼興', '是', '女性', '之', '友'],
        ['這是', '男性', '的', '凝視'],
        ['男朋友', '餐盒', '是', '父權', '便當'],
    ]


def test_split_strs_with_special_token():
    special_token = '隼興'

    output = split_strs(
        input_strs=[
            '隼興隼興是隼興女性隼興之隼興友',
            '這是隼興男性隼興的隼興凝視',
            '男朋友隼興餐盒隼興是隼興父權隼興便當',
        ],
        meta=[
            [2, 5, 9, 12],
            [2, 6, 9],
            [3, 7, 10, 14],
        ],
        sep=special_token,
    )
    assert output == [
        ['隼興', '是', '女性', '之', '友'],
        ['這是', '男性', '的', '凝視'],
        ['男朋友', '餐盒', '是', '父權', '便當'],
    ]


def test_split_strs_without_meta_n_sep():
    output = split_strs(
        input_strs=[
            '隼興是女性之友',
            '這是男性的凝視',
            '男朋友餐盒是父權便當',
        ],
    )
    assert output == [
        ['隼', '興', '是', '女', '性', '之', '友'],
        ['這', '是', '男', '性', '的', '凝', '視'],
        ['男', '朋', '友', '餐', '盒', '是', '父', '權', '便', '當'],
    ]


def test_split_strs_without_meta_with_sep():
    output = split_strs(
        input_strs=[
            '隼興 是 女性 之 友',
            '這是 男性 的 凝視',
            '男朋友 餐盒 是 父權 便當',
        ],
        sep=' ',
    )
    assert output == [
        ['隼興', '是', '女性', '之', '友'],
        ['這是', '男性', '的', '凝視'],
        ['男朋友', '餐盒', '是', '父權', '便當'],
    ]
