from ..default_tokens import DefaultTokens


def test_get_default_tokens():
    D = DefaultTokens
    assert D.sos == '<SOS>'
    assert D.eos == '<EOS>'
    assert D.unk == '<UNK>'
    assert D.pad == '<PAD>'
    assert D.nul == '\0'


def test_list_all_tokens():
    D = DefaultTokens
    output = D.list_all_tokens()
    assert output == {
        'sos': '<SOS>',
        'eos': '<EOS>',
        'unk': '<UNK>',
        'pad': '<PAD>',
        'nul': '\0'
    }
