from ..add_start_end_token import (
    add_start_end_token_in_sentences,
    remove_start_end_token_in_sentences,
)


def test_add_start_end_token_in_sentences_default():
    input_list = [
        ['隼興', '喜歡', '蛋白質'],
        [''],
        ['勤彥', '喜歡', '新加坡', '的', '榴槤'],
        ['1', '2', 'aaa'],
    ]
    output = add_start_end_token_in_sentences(input_list)
    assert input_list == [
        ['隼興', '喜歡', '蛋白質'],
        [''],
        ['勤彥', '喜歡', '新加坡', '的', '榴槤'],
        ['1', '2', 'aaa'],
    ]
    assert output[0] == [
        ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
        ['<SOS>', '', '<EOS>'],
        ['<SOS>', '勤彥', '喜歡', '新加坡', '的', '榴槤', '<EOS>'],
        ['<SOS>', '1', '2', 'aaa', '<EOS>'],
    ]
    assert output[1] == [
        [True, True],
        [True, True],
        [True, True],
        [True, True],
    ]


def test_remove_start_end_token_in_sentences_default():
    output = remove_start_end_token_in_sentences(
        [
            ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
            ['<SOS>', '', '<EOS>'],
            ['<SOS>', '勤彥', '喜歡', '新加坡', '的', '榴槤', '<EOS>'],
            ['<SOS>', '1', '2', 'aaa', '<EOS>'],
        ],
        [
            [True, True],
            [True, True],
            [True, True],
            [True, True],
        ],
    )
    assert output == [
        ['隼興', '喜歡', '蛋白質'],
        [''],
        ['勤彥', '喜歡', '新加坡', '的', '榴槤'],
        ['1', '2', 'aaa'],
    ]
