import pytest

from ..invert_dictionary import invert_dictionary


def test_invert_dictionary():
    output = invert_dictionary(
        {
            'a': 0,
            'b': 1,
            'c': 2,
        },
    )
    assert output == {
        0: 'a',
        1: 'b',
        2: 'c',
    }


def test_invert_dictionary_duplicated_value():
    with pytest.raises(KeyError):
        invert_dictionary(
            {
                'a': 0,
                'b': 1,
                'c': 1,
            },
        )


def test_invert_dictionary_can_serialize():
    output = invert_dictionary(
        {
            'a': 0,
            'b': 1,
            'c': 2,
        },
        serializable=True,
    )
    assert output == {
        '0': 'a',
        '1': 'b',
        '2': 'c',
    }
