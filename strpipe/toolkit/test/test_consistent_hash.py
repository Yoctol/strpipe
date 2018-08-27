from ..consistent_hash import consistent_hash


def test_consistent_hash():
    output = consistent_hash("隼興", 100)
    assert output == 78
    output = consistent_hash("希臘優格", 100)
    assert output == 72
    output = consistent_hash("隼興", 100)
    assert output == 78
