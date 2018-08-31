from ..add_start_end_token import add_start_end_token_in_sentences


def test_add_start_end_token_in_sentences_default():
    assert add_start_end_token_in_sentences(
        [
            ['隼興', '喜歡', '蛋白質'],
            [''],
            ['勤彥', '喜歡', '新加坡', '的', '榴槤'],
            ['1', '2', 'aaa'],
        ],
    ) == [
        ['<SOS>', '隼興', '喜歡', '蛋白質', '<EOS>'],
        ['<SOS>', '', '<EOS>'],
        ['<SOS>', '勤彥', '喜歡', '新加坡', '的', '榴槤', '<EOS>'],
        ['<SOS>', '1', '2', 'aaa', '<EOS>'],
    ]
