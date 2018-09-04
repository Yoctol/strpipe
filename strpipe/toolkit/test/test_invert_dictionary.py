import pytest

from ..invert_dictionary import invert_dictionary


def test_invert_dictionary():
    # TypeError: invert_dictionary() takes no keyword arguments
    # if input_dict={...}
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
        # TypeError: invert_dictionary() takes no keyword arguments
        # if input_dict={...}
        invert_dictionary(
            {
                'a': 0,
                'b': 1,
                'c': 1,
            },
        )
