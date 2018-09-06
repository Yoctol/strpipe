import pytest

from ..pad_sentences import pad_sentences, unpad_sentences


@pytest.fixture
def sentences():
    return [
        ["隼興", "覺得", "有顆頭", "有點", "猥瑣"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用"],
        [""],
        [],
    ]


def test_pad_sentences_with_default_pad(sentences):
    output = pad_sentences(
        sentences=sentences,
        maxlen=3
    )
    assert output[0] == [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<PAD>"],
        ["", "<PAD>", "<PAD>"],
        ["<PAD>", "<PAD>", "<PAD>"],
    ]
    assert output[1] == [
        {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': []},
        {'sentlen': 2, 'sentence_tail': []},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []},
    ]


def test_pad_sentences_with_custom_pad(sentences):
    output = pad_sentences(
        sentences=sentences,
        maxlen=3,
        pad_token="<CPH>",
    )
    assert output[0] == [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<CPH>"],
        ["", "<CPH>", "<CPH>"],
        ["<CPH>", "<CPH>", "<CPH>"],
    ]
    assert output[1] == [
        {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': []},
        {'sentlen': 2, 'sentence_tail': []},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []},
    ]


def test_unpad_sentences(sentences):
    output = unpad_sentences(
        sentences=[
            ["隼興", "覺得", "有顆頭"],
            ["藍莓", "結冰", "惹"],
            ["薩克斯風", "好用", "<CPH>"],
            ["", "<CPH>", "<CPH>"],
            ["<CPH>", "<CPH>", "<CPH>"],
        ],
        meta=[
            {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
            {'sentlen': 3, 'sentence_tail': []},
            {'sentlen': 2, 'sentence_tail': []},
            {'sentlen': 1, 'sentence_tail': []},
            {'sentlen': 0, 'sentence_tail': []},
        ]
    )
    assert output == sentences
