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


def assert_dict_contains(d1, d2):
    '''assert d1 contains all the items in d2
    '''
    for k, v in d2.items():
        if d1[k] != v:
            raise AssertionError(
                "First dictionary has {}={} but expected is {}={}".format(k, d1[k], k, v))


def test_pad_sentences_with_default_pad(sentences):
    output = pad_sentences(
        sentences=sentences,
        maxlen=3,
    )
    assert output[0] == [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<PAD>"],
        ["", "<PAD>", "<PAD>"],
        ["<PAD>", "<PAD>", "<PAD>"],
    ]
    for d1, d2 in zip(output[1], [
            {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
            {'sentlen': 3, 'sentence_tail': []},
            {'sentlen': 2, 'sentence_tail': []},
            {'sentlen': 1, 'sentence_tail': []},
            {'sentlen': 0, 'sentence_tail': []},
        ]):
        assert_dict_contains(d1, d2)


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
    for d1, d2 in zip(output[1], [
            {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
            {'sentlen': 3, 'sentence_tail': []},
            {'sentlen': 2, 'sentence_tail': []},
            {'sentlen': 1, 'sentence_tail': []},
            {'sentlen': 0, 'sentence_tail': []},
        ]):
        assert_dict_contains(d1, d2)


@pytest.mark.parametrize("sos,eos,pad,maxlen,expected_padded_sentences,expected_meta", [
    (None, None, None, 3, [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<PAD>"],
        ["", "<PAD>", "<PAD>"],
        ["<PAD>", "<PAD>", "<PAD>"]], [
        {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': []},
        {'sentlen': 2, 'sentence_tail': []},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []}]
    ),
    (None, None, '<CPH>', 3, [
        ["隼興", "覺得", "有顆頭"],
        ["藍莓", "結冰", "惹"],
        ["薩克斯風", "好用", "<CPH>"],
        ["", "<CPH>", "<CPH>"],
        ["<CPH>", "<CPH>", "<CPH>"]], [
        {'sentlen': 5, 'sentence_tail': ["有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': []},
        {'sentlen': 2, 'sentence_tail': []},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []}]
    ),
    ('<YO>', None, None, 3, [
        ["<YO>", "隼興", "覺得"],
        ["<YO>", "藍莓", "結冰"],
        ["<YO>", "薩克斯風", "好用"],
        ["<YO>", "", "<CPH>"],
        ["<YO>", "<CPH>", "<CPH>"]], [
        {'sentlen': 5, 'sentence_tail': ["有顆頭", "有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': ["惹"]},
        {'sentlen': 2, 'sentence_tail': []},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []}]
    ),
    (None, '<BYE>', None, 3, [
        ["隼興", "覺得", "<BYE>"],
        ["藍莓", "結冰", "<BYE>"],
        ["薩克斯風", "好用", "<BYE>"],
        ["", "<BYE>", "<PAD>"],
        ["<BYE>", "<PAD>", "<PAD>"]], [
        {'sentlen': 5, 'sentence_tail': ["有顆頭", "有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': ["惹"]},
        {'sentlen': 2, 'sentence_tail': []},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []}]
    ),
    ('<A>', '<Z>', None, 3, [
        ["<A>", "隼興", "<Z>"],
        ["<A>", "藍莓", "<Z>"],
        ["<A>", "薩克斯風", "<Z>"],
        ["<A>", "", "<Z>"],
        ["<A>", "<Z>", "<PAD>"]], [
        {'sentlen': 5, 'sentence_tail': ["覺得", "有顆頭", "有點", "猥瑣"]},
        {'sentlen': 3, 'sentence_tail': ["結冰", "惹"]},
        {'sentlen': 2, 'sentence_tail': ["好用"]},
        {'sentlen': 1, 'sentence_tail': []},
        {'sentlen': 0, 'sentence_tail': []}]
    ),
], ids=[
    'default_pad',
    'custom_pad',
    'sos',
    'eos',
    'sos_and_eos',
])
def test_pad_sentences(sentences, sos, eos, pad, maxlen,
    expected_padded_sentences, expected_meta):

    kwargs = {
        'sentences': sentences,
        'sos_token': sos,
        'eos_token': eos,
        'pad_token': pad,
        'maxlen': maxlen
    }
    if sos is None:
        del kwargs['sos_token']
    if eos is None:
        del kwargs['eos_token']
    if pad is None:
        del kwargs['pad_token']

    padded_sentences, meta = pad_sentences(**kwargs)
    assert padded_sentences == expected_padded_sentences
    for d1, in d2 in zip(meta, expected_meta):
        assert_dict_contains(d1, d2)


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
