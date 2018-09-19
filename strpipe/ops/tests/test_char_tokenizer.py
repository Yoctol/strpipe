from strpipe.data.types import STRING_LIST, STRING
from strpipe.ops.char_tokenizer import CharTokenizer


def test_correctly_created():
    tokenizer = CharTokenizer()
    assert tokenizer.input_type == STRING
    assert tokenizer.output_type == STRING_LIST


def test_fit():
    tokenizer = CharTokenizer()
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
    tokenizer = CharTokenizer()

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
        ['薄', '餡', '想', '要', '喝', '9', '0', '0', '杯', '鮮', '奶', '茶'],
        ['餅', '乾', '1', '2', '.', '5', '元'],
        ['_', '4', 'i', 'n', 't', '_', '年'],
        ['這', '顆', 'a', 'p', 'p', 'l', 'e', '好', '吃', 'o', 'h', 'o', 'h'],
        ['股', '價', '_', '5', 'f', 'l', 'o', 'a', 't', '3', '_', '元'],
        ['_', 'f', 'l', 'o', 'a', 't', '_'],
        ['o', 'h', 'o', 'h', '_', 'i', 'n', 't', '_', 'o', 'h', 'o', 'h'],
        ['I', ' ', 'w', 'a', 'n', 't', ' ', 'a', ' ', 'c', 'u', 'p', ' ',
         'o', 'f', ' ', 'w', 'a', 't', 'e', 'r', ',', ' ',
         'p', 'l', 'e', 'a', 's', 'e', '.'],
    ]
    output_data, tx_info = tokenizer.transform(state, input_data)
    assert output_data == expected_output
    assert tx_info is None


def test_inverse_transform():
    tokenizer = CharTokenizer()
    state = None
    tx_info = None
    input_data = [
        ['薄', '餡', '想', '要', '喝', '9', '0', '0', '杯', '鮮', '奶', '茶'],
        ['餅', '乾', '1', '2', '.', '5', '元'],
        ['_', '4', 'i', 'n', 't', '_', '年'],
        ['這', '顆', 'a', 'p', 'p', 'l', 'e', '好', '吃', 'o', 'h', 'o', 'h'],
        ['股', '價', '_', '5', 'f', 'l', 'o', 'a', 't', '3', '_', '元'],
        ['_', 'f', 'l', 'o', 'a', 't', '_'],
        ['o', 'h', 'o', 'h', '_', 'i', 'n', 't', '_', 'o', 'h', 'o', 'h'],
        ['I', ' ', 'w', 'a', 'n', 't', ' ', 'a', ' ', 'c', 'u', 'p', ' ',
         'o', 'f', ' ', 'w', 'a', 't', 'e', 'r', ',', ' ',
         'p', 'l', 'e', 'a', 's', 'e', '.'],
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
