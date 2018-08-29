from ..default_tokens import DefaultTokens


def test_get_default_tokens():
    D = DefaultTokens
    assert D.sos_token == '<SOS>'
    assert D.eos_token == '<EOS>'
    assert D.unk_token == '<UNK>'
    assert D.pad_token == '<PAD>'


def test_list_all_tokens():
    D = DefaultTokens
    output = D.list_all_tokens()
    assert output == {
        'sos_token': '<SOS>',
        'eos_token': '<EOS>',
        'unk_token': '<UNK>',
        'pad_token': '<PAD>',
    }
