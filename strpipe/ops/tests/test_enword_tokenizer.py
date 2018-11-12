import pytest

from strpipe.data.types import STRING_LIST, STRING
from strpipe.ops.enword_tokenizer import EnWordTokenizer


@pytest.fixture(scope="module")
def setUp():
    return {
        "tokenizer": EnWordTokenizer(),
        "strs": [
            "I want to eat apple.",
            "How's it going today, Mr.Smith?",
            "They've been to Taiwan!",
        ],
        "tokens": [
            ['I', 'want', 'to', 'eat', 'apple', '.'],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'Smith', '?', ],
            ['They', "'", 've', 'been', 'to', 'Taiwan', '!'],
        ],
    }


def test_correctly_created(setUp):
    tokenizer = setUp['tokenizer']
    assert tokenizer.input_type == STRING
    assert tokenizer.output_type == STRING_LIST


def test_fit(setUp):
    tokenizer = setUp['tokenizer']
    input_data = setUp['strs']
    state = tokenizer.fit(input_data)
    assert state is None


def test_transform(setUp):
    tokenizer = setUp['tokenizer']
    input_data = setUp['strs']
    expected_output = setUp['tokens']
    state = None
    output_data, tx_info = tokenizer.transform(state, input_data)
    assert output_data == expected_output


def test_invertible(setUp):
    tokenizer = setUp['tokenizer']
    expected_output = setUp['strs']
    state = None
    output_data, tx_info = tokenizer.transform(state, expected_output)
    output_data = tokenizer.inverse_transform(state, output_data, tx_info)
    assert output_data == expected_output
