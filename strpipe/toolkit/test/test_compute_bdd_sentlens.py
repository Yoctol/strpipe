from ..compute_bdd_sentlens import compute_bounded_sentlens


def test_compute_bounded_sentlens_default():
    output = compute_bounded_sentlens(
        sentences=[
            [],
            ['1', '2', '3'],
            ['1', '2', '3', '4', '5'],
        ],
    )
    assert output == [0, 3, 5]


def test_compute_bounded_sentlens_limited():
    output = compute_bounded_sentlens(
        sentences=[
            [],
            ['1', '2', '3'],
            ['1', '2', '3', '4', '5'],
        ],
        maxlen=4,
    )
    assert output == [0, 3, 4]


def test_compute_bounded_sentlens_zero():
    output = compute_bounded_sentlens(
        sentences=[
            [],
            ['1', '2', '3'],
            ['1', '2', '3', '4', '5'],
        ],
        maxlen=0,
    )
    assert output == [0, 3, 5]
