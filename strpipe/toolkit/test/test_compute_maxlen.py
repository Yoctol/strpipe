from ..compute_maxlen import compute_maxlen


def test_compute_maxlen_tokens():
    assert compute_maxlen(
        [
            ['隼興', '喜歡', '蛋白質'],
            [''],
            ['勤彥', '喜歡', '新加坡', '的', '榴槤'],
            ['1', '2', 'aaa'],
        ],
    ) == 5
