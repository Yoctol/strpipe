from strpipe.data.types import STRING_LIST, STRING
from strpipe.ops.zhchar_tokenizer import ZhCharTokenizer


def test_correctly_created():
    tokenizer = ZhCharTokenizer()
    assert tokenizer.input_type == STRING
    assert tokenizer.output_type == STRING_LIST


def test_fit():
    tokenizer = ZhCharTokenizer()
    input_data = [
        '薄餡想要喝9杯鮮奶茶',
        '餅乾12.5元',
        '_4int_年',
        '這顆apple好吃ohoh',
        '股價_5float8_元',
        '_float_',
        'ohoh_int_ohoh',
    ]
    state = tokenizer.fit(input_data)
    assert state is None


def test_transform():
    tokenizer = ZhCharTokenizer()

    state = None
    input_data = [
        '薄餡想要喝900杯鮮奶茶',
        '餅乾12.5元',
        '_4int_年',
        '這顆apple好吃ohoh',
        '股價_5float3_元',
        '_float_',
        'ohoh_int_ohoh',
        'I want a cup of water, please.',
    ]

    expected_output = [
        ['薄', '餡', '想', '要', '喝', '900', '杯', '鮮', '奶', '茶'],
        ['餅', '乾', '12.5', '元'],
        ['_4int_', '年'],
        ['這', '顆', 'apple', '好', '吃', 'ohoh'],
        ['股', '價', '_5float3_', '元'],
        ['_float_'],
        ['ohoh', '_int_', 'ohoh'],
        ['I', ' ', 'want', ' ', 'a', ' ', 'cup', ' ', 'of',
         ' ', 'water', ',', ' ', 'please', '.'],
    ]
    output_data, tx_info = tokenizer.transform(state, input_data)
    assert output_data == expected_output
    assert tx_info is None


def test_inverse_transform():
    tokenizer = ZhCharTokenizer()
    state = None
    tx_info = None
    input_data = [
        ['薄', '餡', '想', '要', '喝', '900', '杯', '鮮', '奶', '茶'],
        ['餅', '乾', '12.5', '元'],
        ['_4int_', '年'],
        ['這', '顆', 'apple', '好', '吃', 'ohoh'],
        ['股', '價', '_5float3_', '元'],
        ['_float_'],
        ['ohoh', '_int_', 'ohoh'],
        ['I', ' ', 'want', ' ', 'a', ' ', 'cup', ' ', 'of',
         ' ', 'water', ',', ' ', 'please', '.'],
    ]
    expected_output = [
        '薄餡想要喝900杯鮮奶茶',
        '餅乾12.5元',
        '_4int_年',
        '這顆apple好吃ohoh',
        '股價_5float3_元',
        '_float_',
        'ohoh_int_ohoh',
        'I want a cup of water, please.',
    ]

    output_data = tokenizer.inverse_transform(state, input_data, tx_info)
    assert output_data == expected_output
