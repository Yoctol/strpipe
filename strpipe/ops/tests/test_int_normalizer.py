import pytest

from strpipe.data.types import STRING
from strpipe.ops.int_normalizer import IntNormalizer


@pytest.fixture
def normalizer():
    normalizer = IntNormalizer()
    return normalizer


def test_correctly_created(normalizer):
    assert normalizer.input_type == STRING
    assert normalizer.output_type == STRING


def test_fit(normalizer):
    input_data = [
        '鮮檸檬多多　微糖 微冰 大杯 有 3 杯',
        '1234',
    ]
    state = normalizer.fit(input_data)
    assert state is None


def test_transform_n_inverse(normalizer):
    from text_normalizer.library import int_text_normalizer
    state = None
    input_data = [
        '鮮檸檬多多　微糖 微冰 大杯 有 3 杯',
    ]
    expected_output = [
        '鮮檸檬多多　微糖 微冰 大杯 有 _int_ 杯',
    ]
    output_data, meta = normalizer.transform(
        input_data=input_data,
        state=state,
    )
    _, expected_meta = int_text_normalizer.normalize(input_data[0])

    assert output_data == expected_output
    assert meta == [expected_meta]

    i_output_data = normalizer.inverse_transform(
        state=state,
        input_data=output_data,
        tx_info=meta,
    )
    assert i_output_data == input_data
