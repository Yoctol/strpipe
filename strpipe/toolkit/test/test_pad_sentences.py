from ..pad_sentences import pad_sentences


def test_pad_sentences_with_default_pad():
    output = pad_sentences(
        sentences=[
            ["隼興", "覺得", "有顆頭", "有點", "猥瑣"],
            ["藍莓", "結冰", "惹"],
            ["薩克斯風", "好用"],
            [""],
            [],
        ],
        maxlen=3,
    )
    assert output == [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<PAD>"],
        ["", "<PAD>", "<PAD>"],
        ["<PAD>", "<PAD>", "<PAD>"],
    ]


def test_pad_sentences_with_custom_pad():
    output = pad_sentences(
        sentences=[
            ["隼興", "覺得", "有顆頭", "有點", "猥瑣"],
            ["藍莓", "結冰", "惹"],
            ["薩克斯風", "好用"],
            [""],
            [],
        ],
        maxlen=3,
        pad_token="<CPH>",
    )
    assert output == [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<CPH>"],
        ["", "<CPH>", "<CPH>"],
        ["<CPH>", "<CPH>", "<CPH>"],
    ]
